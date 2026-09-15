import { all, get, run } from '../db.js';
import { assignConversation, sendOutbound, addTag } from './inbox.js';

const parseJson = (s, fallback = {}) => { try { return JSON.parse(s ?? ''); } catch { return fallback; } };

const GREETINGS = {
  th: 'สวัสดีค่ะ ขอบคุณที่ติดต่อ GTG ทีมงานกำลังตรวจสอบและจะตอบกลับโดยเร็วที่สุดค่ะ',
  en: 'Hello! Thanks for reaching out to GTG. Our team will get back to you shortly.',
  ru: 'Здравствуйте! Спасибо за обращение в GTG. Мы ответим вам в ближайшее время.',
};

/** เดาภาษาจากตัวอักษรในข้อความ — พอสำหรับ prototype */
export function detectLanguage(text = '') {
  if (/[฀-๿]/.test(text)) return 'th';
  if (/[Ѐ-ӿ]/.test(text)) return 'ru';
  return 'en';
}

/** มอบหมายแบบวนรอบ: เลือก agent ที่ถือเคส open น้อยที่สุด (เท่ากันให้เอาคนที่รับล่าสุดนานสุด) */
export function pickRoundRobinAgent() {
  const rows = all(
    `SELECT u.id, u.name,
            (SELECT COUNT(*) FROM conversations c WHERE c.assignee_user_id = u.id AND c.status = 'open') AS load,
            (SELECT COALESCE(MAX(c2.id), 0) FROM conversations c2 WHERE c2.assignee_user_id = u.id) AS last_taken
       FROM users u
      WHERE u.role = 'agent' AND u.active = 1
      ORDER BY load ASC, last_taken ASC, u.id ASC
      LIMIT 1`,
  );
  return rows[0] || null;
}

/**
 * รันกฎทั้งหมดหลังมีข้อความเข้า
 * ctx = { conversationId, contactId, text, conversationCreated }
 */
export async function runAutomations(ctx) {
  const rules = all('SELECT * FROM automation_rules WHERE enabled = 1 ORDER BY sort_order, id');
  const fired = [];

  for (const rule of rules) {
    if (rule.trigger === 'conversation.created' && !ctx.conversationCreated) continue;
    const cfg = parseJson(rule.config_json);
    let result = 'skipped';

    try {
      if (rule.action === 'assign_round_robin') {
        const conv = get('SELECT * FROM conversations WHERE id = ?', [ctx.conversationId]);
        if (conv && conv.assignee_user_id === null) {
          const agent = pickRoundRobinAgent();
          if (agent) {
            assignConversation(ctx.conversationId, agent.id, rule.name);
            result = `assigned:${agent.name}`;
          } else {
            result = 'no_agent_available';
          }
        }
      } else if (rule.action === 'send_greeting') {
        const lang = detectLanguage(ctx.text);
        const text = cfg.messages?.[lang] || GREETINGS[lang] || GREETINGS.en;
        run('UPDATE contacts SET language = ? WHERE id = ?', [lang, ctx.contactId]);
        await sendOutbound({ conversationId: ctx.conversationId, text, source: 'automation' });
        result = `greeted:${lang}`;
      } else if (rule.action === 'add_tag_by_keyword') {
        const lower = (ctx.text || '').toLowerCase();
        const hits = Object.entries(cfg.keywords || {})
          .filter(([keyword]) => lower.includes(keyword.toLowerCase()))
          .map(([, tag]) => tag);
        for (const tag of hits) addTag(ctx.contactId, tag);
        result = hits.length ? `tagged:${hits.join('|')}` : 'no_keyword';
      }
    } catch (err) {
      result = `error:${String(err.message).slice(0, 120)}`;
      console.error(`[automation] กฎ "${rule.name}" ล้มเหลว:`, err.message);
    }

    run('INSERT INTO automation_runs (rule_id, conversation_id, result) VALUES (?, ?, ?)',
      [rule.id, ctx.conversationId, result]);
    if (result !== 'skipped') fired.push({ rule: rule.name, result });
  }
  return fired;
}
