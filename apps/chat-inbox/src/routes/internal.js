/**
 * API ของหน้า Inbox เอง (คนละชุดกับ API ที่ Agency Care เรียก)
 * prototype นี้ยังไม่มี login จริง — ใช้ header x-dev-user เป็นรหัสผู้ใช้
 * ของจริงต้องเปลี่ยนเป็น session ตาม roadmap สัปดาห์ 4-6
 */
import { all, get } from '../db.js';
import { sendJson, badRequest, notFound, parseQuery } from '../http.js';
import { subscribe } from '../services/events.js';
import {
  listConversations, conversationDetail, counters, sendOutbound,
  assignConversation, setConversationStatus, setLifecycleStage, addTag, setCustomField,
} from '../services/inbox.js';
import { LIFECYCLE_STAGES, config } from '../config.js';

function currentUser(req) {
  const id = Number(req.headers[config.devUserHeader]);
  if (!id) return null;
  return get('SELECT * FROM users WHERE id = ? AND active = 1', [id]) || null;
}

export function sseHandler(req, res) {
  res.writeHead(200, {
    'content-type': 'text/event-stream; charset=utf-8',
    'cache-control': 'no-cache, no-transform',
    connection: 'keep-alive',
  });
  res.write(`event: ready\ndata: {"ok":true}\n\n`);

  const unsubscribe = subscribe(({ event, data }) => {
    res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
  });
  const heartbeat = setInterval(() => res.write(': ping\n\n'), 25_000);
  req.on('close', () => { clearInterval(heartbeat); unsubscribe(); });
}

export async function handleInternal(req, res, url, method) {
  const route = url.pathname.split('/').filter(Boolean).slice(1); // ตัด "internal"
  const query = parseQuery(url);
  const user = currentUser(req);

  if (route[0] === 'me' && method === 'GET') {
    return sendJson(res, 200, {
      user: user ? { id: user.id, name: user.name, role: user.role } : null,
      users: all("SELECT id, name, role FROM users WHERE active = 1 ORDER BY role, name"),
      stages: LIFECYCLE_STAGES,
    });
  }

  if (route[0] === 'conversations' && route.length === 1 && method === 'GET') {
    // agent เห็นเฉพาะเคสของตัวเองเมื่อเลือกแท็บ mine — admin เห็นได้ทุกแท็บ
    const filter = query.filter || 'all';
    return sendJson(res, 200, {
      counters: counters(),
      data: listConversations({
        status: query.status || 'open',
        filter,
        assigneeUserId: user?.id ?? -1,
      }),
    });
  }

  if (route[0] === 'conversations' && route.length === 2 && method === 'GET') {
    return sendJson(res, 200, conversationDetail(Number(route[1])));
  }

  if (route[0] === 'conversations' && route[2] === 'reply' && method === 'POST') {
    if (!user) throw badRequest('ต้องเลือกผู้ใช้ก่อนตอบข้อความ');
    const text = req.body?.text;
    if (!text) throw badRequest('ต้องระบุ text');
    const sent = await sendOutbound({ conversationId: Number(route[1]), text, userId: user.id, source: 'human' });
    return sendJson(res, 201, sent);
  }

  if (route[0] === 'conversations' && route[2] === 'assign' && method === 'POST') {
    const assigneeId = req.body?.userId === null ? null : Number(req.body?.userId);
    const conv = assignConversation(Number(route[1]), Number.isFinite(assigneeId) ? assigneeId : null, user?.name || 'system');
    return sendJson(res, 200, { conversation: conv });
  }

  if (route[0] === 'conversations' && route[2] === 'status' && method === 'POST') {
    const conv = setConversationStatus(Number(route[1]), req.body?.status);
    return sendJson(res, 200, { conversation: conv });
  }

  if (route[0] === 'contacts' && route[2] === 'lifecycle' && method === 'POST') {
    const result = await setLifecycleStage(Number(route[1]), req.body?.stage, user?.name || 'system');
    return sendJson(res, 200, { contact: result.contact, changed: result.changed });
  }

  if (route[0] === 'contacts' && route[2] === 'tags' && method === 'POST') {
    const tag = addTag(Number(route[1]), req.body?.name);
    return sendJson(res, 201, { tag });
  }

  if (route[0] === 'contacts' && route[2] === 'fields' && method === 'POST') {
    const fields = setCustomField(Number(route[1]), req.body?.key, req.body?.value);
    return sendJson(res, 200, { fields });
  }

  if (route[0] === 'integrations' && method === 'GET') {
    return sendJson(res, 200, {
      apiKeys: all('SELECT id, name, prefix, scopes, active, last_used_at FROM api_keys ORDER BY id'),
      webhooks: all('SELECT id, name, url, events, active FROM webhooks_out ORDER BY id'),
      deliveries: all('SELECT id, webhook_id, event, status, response_code, error, created_at FROM webhook_deliveries ORDER BY id DESC LIMIT 20'),
    });
  }

  if (route[0] === 'automations' && method === 'GET') {
    return sendJson(res, 200, {
      rules: all('SELECT id, name, trigger, action, enabled FROM automation_rules ORDER BY sort_order, id'),
      runs: all(`SELECT r.id, r.result, r.created_at, ar.name AS rule, r.conversation_id
                   FROM automation_runs r JOIN automation_rules ar ON ar.id = r.rule_id
                  ORDER BY r.id DESC LIMIT 20`),
    });
  }

  throw notFound(`ไม่มี endpoint นี้: ${method} ${url.pathname}`);
}
