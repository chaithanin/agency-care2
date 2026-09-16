import { config } from '../../config.js';

/**
 * ตัวเชื่อม respond.io Developer API v2
 *
 * เอกสาร: https://developers.respond.io/docs/api/
 * base    https://api.respond.io/v2
 * auth    Authorization: Bearer <token>
 *
 * ทำตามที่ API กำหนด:
 *   - 429 มาพร้อม header Retry-After → รอแล้วลองใหม่
 *   - 5xx → ถอยแบบ exponential backoff
 *   - 4xx อื่น ๆ → ไม่ลองซ้ำ โยน error ทันทีเพราะลองไปก็ผิดเหมือนเดิม
 */

export class RespondIoError extends Error {
  constructor(message, { status, body, url } = {}) {
    super(message);
    this.name = 'RespondIoError';
    this.status = status;
    this.body = body;
    this.url = url;
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export class RespondIoClient {
  constructor(opts = {}) {
    const c = { ...config.respondio, ...opts };
    this.apiToken = c.apiToken;
    this.apiBase = String(c.apiBase).replace(/\/+$/, '');
    this.timeoutMs = c.timeoutMs;
    this.maxRetries = c.maxRetries;
    this.pageSize = c.pageSize;
    this.timezone = c.timezone;
    // ให้ test แทน fetch ได้โดยไม่ต้องยิงเน็ตจริง
    this.fetchImpl = opts.fetchImpl || globalThis.fetch;
    this.onRetry = opts.onRetry || (() => {});
  }

  get configured() {
    return Boolean(this.apiToken);
  }

  async request(method, path, { body, query } = {}) {
    if (!this.apiToken) {
      throw new RespondIoError('ยังไม่ได้ตั้ง RESPONDIO_API_TOKEN');
    }
    let url = this.apiBase + path;
    if (query && Object.keys(query).length) {
      const qs = new URLSearchParams();
      for (const [k, v] of Object.entries(query)) {
        if (v !== undefined && v !== null && v !== '') qs.set(k, String(v));
      }
      const s = qs.toString();
      if (s) url += (url.includes('?') ? '&' : '?') + s;
    }

    let lastErr;
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      const ac = new AbortController();
      const timer = setTimeout(() => ac.abort(), this.timeoutMs);
      let res;
      try {
        res = await this.fetchImpl(url, {
          method,
          headers: {
            Authorization: `Bearer ${this.apiToken}`,
            Accept: 'application/json',
            ...(body ? { 'Content-Type': 'application/json' } : {}),
          },
          body: body ? JSON.stringify(body) : undefined,
          signal: ac.signal,
        });
      } catch (err) {
        // เน็ตหลุด / timeout — ลองใหม่ได้
        clearTimeout(timer);
        lastErr = new RespondIoError(`เรียก ${method} ${path} ไม่สำเร็จ: ${err.message}`, { url });
        if (attempt === this.maxRetries) throw lastErr;
        const delay = 2 ** attempt * 500;
        this.onRetry({ attempt, delay, reason: err.message });
        await sleep(delay);
        continue;
      }
      clearTimeout(timer);

      const text = await res.text();
      let parsed;
      try { parsed = text ? JSON.parse(text) : null; } catch { parsed = text; }

      if (res.ok) return parsed;

      const retryable = res.status === 429 || res.status >= 500;
      if (!retryable || attempt === this.maxRetries) {
        throw new RespondIoError(
          `respond.io ตอบ ${res.status} ที่ ${method} ${path}`,
          { status: res.status, body: parsed, url },
        );
      }
      const retryAfter = Number(res.headers?.get?.('retry-after'));
      const delay = Number.isFinite(retryAfter) && retryAfter > 0
        ? retryAfter * 1000
        : 2 ** attempt * 500;
      this.onRetry({ attempt, delay, status: res.status });
      await sleep(delay);
    }
    throw lastErr;
  }

  get(path, query) { return this.request('GET', path, { query }); }
  post(path, body, query) { return this.request('POST', path, { body, query }); }

  /**
   * ไล่ทุกหน้าแบบ cursor แล้วคืนรายการรวม
   * respond.io คืน { items, pagination: { hasMore, next } }
   * @param {'GET'|'POST'} method
   */
  async *paginate(method, path, { body, query, max = Infinity } = {}) {
    let cursorId;
    let fetched = 0;
    for (;;) {
      const q = { limit: this.pageSize, ...query, ...(cursorId ? { cursorId } : {}) };
      const page = method === 'POST'
        ? await this.post(path, body, q)
        : await this.get(path, q);

      const items = Array.isArray(page) ? page : (page?.items ?? []);
      for (const item of items) {
        yield item;
        if (++fetched >= max) return;
      }

      const p = Array.isArray(page) ? null : page?.pagination;
      const next = p?.next ?? p?.cursorId ?? null;
      const hasMore = p?.hasMore ?? Boolean(next);
      if (!hasMore || !next || items.length === 0) return;
      cursorId = next;
    }
  }

  async collect(method, path, opts) {
    const out = [];
    for await (const item of this.paginate(method, path, opts)) out.push(item);
    return out;
  }

  // ── endpoint ที่ใช้ดึงข้อมูล ────────────────────────────────

  /** ข้อมูล workspace: channel / user / custom field / closing note */
  listChannels()      { return this.collect('GET', '/space/channel'); }
  listUsers()         { return this.collect('GET', '/space/user'); }
  listCustomFields()  { return this.collect('GET', '/space/custom_field'); }
  listClosingNotes()  { return this.collect('GET', '/space/closing_notes'); }

  /**
   * รายชื่อ contact ทั้งหมด — POST /contact/list รับ filter ได้
   * ส่ง filter ว่างไว้ = เอาทุกคน
   */
  listContacts({ search, filter, max } = {}) {
    return this.collect('POST', '/contact/list', {
      body: { timezone: this.timezone, ...(search ? { search } : {}), filter: filter || {} },
      max,
    });
  }

  getContact(identifier)  { return this.get(`/contact/${identifier}`); }
  listContactChannels(id) { return this.collect('GET', `/contact/id:${id}/channels`); }

  listMessages(contactId, { max } = {}) {
    return this.collect('GET', `/contact/id:${contactId}/message/list`, { max });
  }
}

export function createClient(opts) {
  return new RespondIoClient(opts);
}
