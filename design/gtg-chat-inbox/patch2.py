# -*- coding: utf-8 -*-
import io

def edit(path, subs):
    s = io.open(path, encoding='utf-8').read()
    miss = []
    for a, b in subs:
        if a not in s:
            miss.append(a[:60])
        s = s.replace(a, b, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print(path, 'ok' if not miss else 'MISSING: ' + ' | '.join(miss))

# ── Main: รายการสั้นลงหนึ่งแถว + select พอดีคอลัมน์ ────────────────────
edit('build1.py', [
  ('  ("นภ","คุณนภัส ก.","LINE","ขอบคุณมากค่ะ เดี๋ยวปรึกษาที่บ้านก่อนนะคะ","เมื่อวาน","New Lead","muted","Nok",False),\n', ''),
  ('{select("Hot Lead", 280)}', '{select("Hot Lead", 252)}'),
])

# ── Automations: แผงขวาแคบลง ───────────────────────────────────────────
edit('build3.py', [
  ('<span style="width:48px;flex:none;color:{T["muted"]}">{t}</span>',
   '<span style="width:42px;flex:none;color:{T["muted"]}">{t}</span>'),
  ('<span style="width:140px;flex:none">{who}</span>',
   '<span style="width:104px;flex:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{who}</span>'),
])

# ── Broadcast: ย้ายแคมเปญเก่าไปคอลัมน์ขวาแบบย่อ ────────────────────────
old_past = """        {card(label("แคมเปญที่ส่งไปแล้ว") + '<div style="height:10px"></div>'
          + f'<div style="display:flex;align-items:center;gap:14px;padding-bottom:8px;font-size:11px;font-family:{DISPLAY};font-weight:600;letter-spacing:.04em;color:{T["muted"]}">'
          + f'<span style="flex:1">ชื่อแคมเปญ</span><span style="width:110px;flex:none">ส่งเมื่อ</span>'
          + f'<span style="width:70px;flex:none;text-align:right">ผู้รับ</span><span style="width:70px;flex:none;text-align:right">สำเร็จ</span>'
          + f'<span style="width:60px;flex:none;text-align:right">ล้มเหลว</span></div>' + past_rows)}
"""
compact = """        {card(label("แคมเปญล่าสุด") + '<div style="height:12px"></div>' + compact_rows)}
"""
edit('build3.py', [
  (old_past, ''),
  ('        {card(f\'<div style="display:flex;align-items:flex-start;gap:10px">\'\n          + f\'<span style="color:{T["warn"]};flex:none;margin-top:1px">{ic("shield",17,1.6,T["warn"])}</span>\'',
   compact + '        {card(f\'<div style="display:flex;align-items:flex-start;gap:10px">\'\n          + f\'<span style="color:{T["warn"]};flex:none;margin-top:1px">{ic("shield",17,1.6,T["warn"])}</span>\''),
])
# เพิ่มตัวแปร compact_rows หลัง past_rows
edit('build3.py', [
  ('broadcast = f\'\'\'<div style="width:1440px;',
   '''compact_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid {T["line"]};font-size:12.5px">'
  f'<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{name}</span>'
  f'<span style="flex:none;color:{T["muted"]};font-size:11.5px">{date}</span>'
  f'<span style="flex:none;color:{T["ok"]};font-variant-numeric:tabular-nums">{ok}</span></div>'
  for name, date, total, ok, fail in PAST)

broadcast = f\'\'\'<div style="width:1440px;'''),
])

# ── Dashboard: ย่อความกว้างการ์ด/กราฟให้พอดี drawer 252px ───────────────
edit('build4.py', [
  ('PW, PH, PX, PY = 780, 196, 40, 14', 'PW, PH, PX, PY = 656, 196, 36, 14'),
  ("f'<svg width=\"836\" height=\"250\" viewBox=\"0 0 836 250\" role=\"img\">'",
   "f'<svg width=\"720\" height=\"250\" viewBox=\"0 0 720 250\" role=\"img\">'"),
  ('width:856px;flex:none;background:{T[\'surface\']}', 'width:760px;flex:none;background:{T[\'surface\']}'),
  ('width:{v / fmax * 242:.0f}px', 'width:{v / fmax * 178:.0f}px'),
  ('<span style="width:82px;flex:none;font-size:12.5px;color:{T["muted"]}">{n}</span>',
   '<span style="width:74px;flex:none;font-size:12.5px;color:{T["muted"]}">{n}</span>'),
  ('width:{v / lmax * 360:.0f}px', 'width:{v / lmax * 296:.0f}px'),
  ('width:{p / 100 * 596:.0f}px', 'width:{p / 100 * 468:.0f}px'),
])

# ── Settings › ช่องทาง: ตัดบรรทัดที่ยาวเกินความสูง ─────────────────────
edit('build5.py', [
  ('("ตรวจลายเซ็น X-Line-Signature","เปิดอยู่"),("ข้อความเดือนนี้","1,580 / 10,000"),\n           ("เชื่อมต่อเมื่อ","12 ก.ย. 2569 โดย Admin GTG")',
   '("ตรวจลายเซ็น X-Line-Signature","เปิดอยู่"),("ข้อความเดือนนี้","1,580 / 10,000")'),
  ('("ต้องมีก่อน","Meta Business verification และเทมเพลตที่อนุมัติแล้ว"),\n           ("ค่าใช้จ่าย","คิดตามจำนวนบทสนทนา ไม่ใช่จำนวนข้อความ")',
   '("ต้องมีก่อน","Meta Business verification และเทมเพลตที่อนุมัติแล้ว")'),
])

# ── Settings › Integrations: คอลัมน์ขวาแคบลง + ตารางกระชับ + log สั้นลง ──
edit('build5.py', [
  ('<div style="width:376px;flex:none;display:flex;flex-direction:column;gap:16px">',
   '<div style="width:330px;flex:none;display:flex;flex-direction:column;gap:16px">'),
  ('''KEYS = [("Agency Care (production)", "gtg_7f3a…", "read, write", "12 ก.ย. 2569", "วันนี้ 09:21 น.", "ใช้งานอยู่", "accent"),
        ("Agency Care (staging)", "gtg_b1c9…", "read", "12 ก.ย. 2569", "8 ก.ย. 2569", "ใช้งานอยู่", "accent"),
        ("รายงานการตลาด (เก่า)", "gtg_20df…", "read", "3 ส.ค. 2569", "28 ส.ค. 2569", "เพิกถอนแล้ว", "muted")]''',
   '''KEYS = [("Agency Care (production)", "gtg_7f3a…", "read, write", "วันนี้ 09:21 น.", "ใช้งานอยู่", "ok"),
        ("Agency Care (staging)", "gtg_b1c9…", "read", "8 ก.ย. 2569", "ใช้งานอยู่", "ok"),
        ("รายงานการตลาด (เก่า)", "gtg_20df…", "read", "28 ส.ค. 2569", "เพิกถอนแล้ว", "muted")]'''),
  ('''  f'<span style="width:110px;flex:none">{mono(k)}</span>'
  f'<span style="width:110px;flex:none;color:{T["muted"]}">{sc}</span>'
  f'<span style="width:110px;flex:none;color:{T["muted"]}">{cr}</span>'
  f'<span style="width:130px;flex:none;color:{T["muted"]}">{lu}</span>'
  f'<span style="width:100px;flex:none">{pill(st,tone)}</span>'
  f'<span style="color:{T["muted"]};flex:none">{ic("dots",16)}</span></div>'
  for n, k, sc, cr, lu, st, tone in KEYS)''',
   '''  f'<span style="width:96px;flex:none">{mono(k)}</span>'
  f'<span style="width:86px;flex:none;color:{T["muted"]}">{sc}</span>'
  f'<span style="width:116px;flex:none;color:{T["muted"]}">{lu}</span>'
  f'<span style="width:92px;flex:none">{pill(st,tone)}</span>'
  f'<span style="color:{T["muted"]};flex:none">{ic("dots",16)}</span></div>'
  for n, k, sc, lu, st, tone in KEYS)'''),
  ('''+ f'<span style="flex:1">ชื่อ</span><span style="width:110px;flex:none">คีย์</span><span style="width:110px;flex:none">สิทธิ์</span>'
            + f'<span style="width:110px;flex:none">สร้างเมื่อ</span><span style="width:130px;flex:none">ใช้ล่าสุด</span>'
            + f'<span style="width:100px;flex:none">สถานะ</span><span style="width:16px;flex:none"></span></div>' ''',
   '''+ f'<span style="flex:1">ชื่อ</span><span style="width:96px;flex:none">คีย์</span><span style="width:86px;flex:none">สิทธิ์</span>'
            + f'<span style="width:116px;flex:none">ใช้ล่าสุด</span>'
            + f'<span style="width:92px;flex:none">สถานะ</span><span style="width:16px;flex:none"></span></div>' '''),
  ('''              ("contact.lifecycle_changed","504","08:52:11 น.","หมดเวลา","danger"),
              ("conversation.created","200","08:40:02 น.","สำเร็จ","muted")]''',
   '''              ("contact.lifecycle_changed","504","08:52:11 น.","หมดเวลา","danger")]'''),
])
