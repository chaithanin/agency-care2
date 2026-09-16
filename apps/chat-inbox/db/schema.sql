-- GTG Chat Inbox — schema สำหรับ prototype (SQLite)
-- ยึดโครงเดียวกับที่วางไว้ใน roadmap สัปดาห์ 1 เพื่อย้ายไป PostgreSQL ได้ภายหลัง
-- หลักคิด: "คน 1 คน" (contacts) แยกจาก "บัญชีของเขาในแต่ละช่องทาง" (contact_channels)

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  email           TEXT NOT NULL UNIQUE,
  name            TEXT NOT NULL,
  role            TEXT NOT NULL CHECK (role IN ('admin','agent')),
  active          INTEGER NOT NULL DEFAULT 1,
  created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 1 แถว = 1 บัญชีช่องทาง เช่น LINE OA ของ GTG, เพจ Facebook
CREATE TABLE IF NOT EXISTS channels (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  provider        TEXT NOT NULL CHECK (provider IN ('line','facebook','whatsapp','mock')),
  name            TEXT NOT NULL,
  external_id     TEXT,                    -- LINE bot user id / FB page id
  config_json     TEXT NOT NULL DEFAULT '{}',
  active          INTEGER NOT NULL DEFAULT 1,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (provider, external_id)
);

CREATE TABLE IF NOT EXISTS contacts (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  display_name    TEXT NOT NULL,
  language        TEXT NOT NULL DEFAULT 'th',
  lifecycle_stage TEXT NOT NULL DEFAULT 'new_lead'
                    CHECK (lifecycle_stage IN ('new_lead','hot_lead','payment','customer','lost')),
  owner_user_id   INTEGER REFERENCES users(id),
  phone           TEXT,
  email           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_contacts_stage ON contacts(lifecycle_stage);
CREATE INDEX IF NOT EXISTS idx_contacts_name  ON contacts(display_name);

CREATE TABLE IF NOT EXISTS contact_channels (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id       INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  channel_id       INTEGER NOT NULL REFERENCES channels(id),
  external_user_id TEXT NOT NULL,          -- LINE userId / FB PSID
  profile_json     TEXT NOT NULL DEFAULT '{}',
  created_at       TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (channel_id, external_user_id)
);

CREATE TABLE IF NOT EXISTS conversations (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id       INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  channel_id       INTEGER NOT NULL REFERENCES channels(id),
  status           TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','closed')),
  assignee_user_id INTEGER REFERENCES users(id),
  opened_at        TEXT NOT NULL DEFAULT (datetime('now')),
  closed_at        TEXT,
  last_message_at  TEXT NOT NULL DEFAULT (datetime('now')),
  first_inbound_at TEXT,                   -- ใช้คำนวณเวลาตอบเฉลี่ย
  first_reply_at   TEXT,
  created_at       TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_conv_status ON conversations(status, last_message_at DESC);
CREATE INDEX IF NOT EXISTS idx_conv_assignee ON conversations(assignee_user_id);

CREATE TABLE IF NOT EXISTS messages (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id     INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  contact_id          INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  channel_id          INTEGER NOT NULL REFERENCES channels(id),
  direction           TEXT NOT NULL CHECK (direction IN ('in','out')),
  sender_user_id      INTEGER REFERENCES users(id),   -- null = ลูกค้า หรือ ระบบ
  source              TEXT NOT NULL DEFAULT 'human'
                        CHECK (source IN ('human','automation','api','contact')),
  text                TEXT NOT NULL DEFAULT '',
  external_message_id TEXT,
  payload_json        TEXT NOT NULL DEFAULT '{}',
  created_at          TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (channel_id, external_message_id)
);
CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id, id);

CREATE TABLE IF NOT EXISTS tags (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name  TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS contact_tags (
  contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  tag_id     INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (contact_id, tag_id)
);

-- custom fields แบบ definition + value (แอดมินเพิ่มช่องเองได้)
CREATE TABLE IF NOT EXISTS custom_field_defs (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  key          TEXT NOT NULL UNIQUE,
  label        TEXT NOT NULL,
  type         TEXT NOT NULL CHECK (type IN ('text','number','select','date')),
  options_json TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS contact_field_values (
  contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  field_id   INTEGER NOT NULL REFERENCES custom_field_defs(id) ON DELETE CASCADE,
  value      TEXT,
  PRIMARY KEY (contact_id, field_id)
);

-- ประวัติการเปลี่ยน stage: ต้นทางของ webhook ที่ Agency Care รอฟัง
CREATE TABLE IF NOT EXISTS lifecycle_events (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id     INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  from_stage     TEXT,
  to_stage       TEXT NOT NULL,
  changed_by     TEXT NOT NULL DEFAULT 'system',   -- ชื่อ user หรือ 'agency-care-api'
  created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_lifecycle_contact ON lifecycle_events(contact_id, id);

-- Integrations: กุญแจที่ Agency Care ใช้เรียกเรา (เก็บเฉพาะ hash)
CREATE TABLE IF NOT EXISTS api_keys (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  name         TEXT NOT NULL,
  prefix       TEXT NOT NULL,             -- 8 ตัวแรก ไว้ให้ดูว่าใบไหน
  key_hash     TEXT NOT NULL UNIQUE,      -- sha256 ของคีย์เต็ม
  scopes       TEXT NOT NULL DEFAULT 'read',
  active       INTEGER NOT NULL DEFAULT 1,
  created_at   TEXT NOT NULL DEFAULT (datetime('now')),
  last_used_at TEXT
);

-- Webhook ขาออกไปหา Agency Care
CREATE TABLE IF NOT EXISTS webhooks_out (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  url        TEXT NOT NULL,
  secret     TEXT NOT NULL,
  events     TEXT NOT NULL DEFAULT 'contact.lifecycle_changed',
  active     INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS webhook_deliveries (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  webhook_id    INTEGER NOT NULL REFERENCES webhooks_out(id) ON DELETE CASCADE,
  event         TEXT NOT NULL,
  payload_json  TEXT NOT NULL,
  status        TEXT NOT NULL CHECK (status IN ('pending','ok','failed')),
  response_code INTEGER,
  error         TEXT,
  attempts      INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- กฎอัตโนมัติแบบย่อ (trigger -> action) ของสัปดาห์ 11-12
CREATE TABLE IF NOT EXISTS automation_rules (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  trigger     TEXT NOT NULL CHECK (trigger IN ('conversation.created','message.received')),
  config_json TEXT NOT NULL DEFAULT '{}',
  action      TEXT NOT NULL CHECK (action IN ('send_greeting','assign_round_robin','add_tag_by_keyword')),
  enabled     INTEGER NOT NULL DEFAULT 1,
  sort_order  INTEGER NOT NULL DEFAULT 100
);
CREATE TABLE IF NOT EXISTS automation_runs (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_id         INTEGER NOT NULL REFERENCES automation_rules(id) ON DELETE CASCADE,
  conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
  result          TEXT NOT NULL,
  created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- respond.io — ตารางกระจกเงา เก็บข้อมูลดิบที่ดึงมาแบบไม่แปลง
-- แยกจากตารางหลักโดยตั้งใจ การ pull จึงไม่มีทางทำข้อมูลของระบบเสีย
-- การแปลงเข้าตารางหลักทำแยกขั้นตอน (src/integrations/respondio/map.js)
-- ============================================================

CREATE TABLE IF NOT EXISTS respondio_contacts (
  id            INTEGER PRIMARY KEY,          -- id จาก respond.io
  first_name    TEXT,
  last_name     TEXT,
  phone         TEXT,
  email         TEXT,
  language      TEXT,
  country_code  TEXT,
  profile_pic   TEXT,
  lifecycle     TEXT,
  status        TEXT,                          -- open / close
  assignee_id   INTEGER,
  assignee_name TEXT,
  tags_json     TEXT NOT NULL DEFAULT '[]',
  fields_json   TEXT NOT NULL DEFAULT '[]',    -- custom_fields ดิบ
  created_at    INTEGER,                       -- epoch จาก respond.io
  synced_at     TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_rio_contacts_phone ON respondio_contacts(phone);
CREATE INDEX IF NOT EXISTS idx_rio_contacts_email ON respondio_contacts(email);

CREATE TABLE IF NOT EXISTS respondio_contact_channels (
  id                        INTEGER PRIMARY KEY,
  contact_id                INTEGER NOT NULL REFERENCES respondio_contacts(id) ON DELETE CASCADE,
  name                      TEXT,
  source                    TEXT,              -- line / whatsapp / facebook / ...
  meta_json                 TEXT,
  last_message_time         INTEGER,
  last_incoming_message_time INTEGER,
  created_at                INTEGER,
  synced_at                 TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_rio_cc_contact ON respondio_contact_channels(contact_id);

CREATE TABLE IF NOT EXISTS respondio_messages (
  id           INTEGER PRIMARY KEY,
  contact_id   INTEGER NOT NULL REFERENCES respondio_contacts(id) ON DELETE CASCADE,
  channel_id   INTEGER,
  traffic      TEXT,                            -- incoming / outgoing
  type         TEXT,                            -- text / attachment / email / ...
  text         TEXT,
  payload_json TEXT,                            -- ตัวข้อความดิบทั้งก้อน
  status       TEXT,                            -- สถานะล่าสุด: sent / delivered / read / failed
  timestamp    INTEGER,
  synced_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_rio_msg_contact ON respondio_messages(contact_id, timestamp DESC);

CREATE TABLE IF NOT EXISTS respondio_users (
  id         INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name  TEXT,
  email      TEXT,
  synced_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS respondio_channels (
  id        INTEGER PRIMARY KEY,
  name      TEXT,
  source    TEXT,
  meta_json TEXT,
  synced_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS respondio_custom_fields (
  id         INTEGER PRIMARY KEY,
  name       TEXT,
  type       TEXT,
  meta_json  TEXT,
  synced_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS respondio_tags (
  name      TEXT PRIMARY KEY,
  synced_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS respondio_closing_notes (
  id         INTEGER PRIMARY KEY,
  name       TEXT,
  meta_json  TEXT,
  synced_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- จับคู่ contact ของ respond.io กับ contact ในระบบ
CREATE TABLE IF NOT EXISTS respondio_contact_links (
  respondio_contact_id INTEGER PRIMARY KEY REFERENCES respondio_contacts(id) ON DELETE CASCADE,
  contact_id           INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  matched_by           TEXT NOT NULL,          -- phone / email / created
  linked_at            TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_rio_link_contact ON respondio_contact_links(contact_id);

-- บันทึกการ sync แต่ละรอบ ไว้ดูย้อนหลังและทำ incremental
CREATE TABLE IF NOT EXISTS respondio_sync_runs (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  resource    TEXT NOT NULL,
  started_at  TEXT NOT NULL DEFAULT (datetime('now')),
  finished_at TEXT,
  ok          INTEGER NOT NULL DEFAULT 0,
  fetched     INTEGER NOT NULL DEFAULT 0,
  error       TEXT
);
