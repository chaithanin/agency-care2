/** Bus กลางในหน่วยความจำ — Inbox UI ฟังผ่าน SSE, Agency Care ฟังผ่าน webhook */
const listeners = new Set();

export function subscribe(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

export function emit(event, data) {
  const payload = { event, data, at: new Date().toISOString() };
  for (const fn of listeners) {
    try { fn(payload); } catch (err) { console.error('[events] listener error', err); }
  }
  return payload;
}
