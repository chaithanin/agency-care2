# -*- coding: utf-8 -*-
"""Broadcast + Settings › Integrations — เลย์เอาต์ที่พอดีความสูง 900px หลังใช้ drawer 252px"""
exec(open('gen.py', encoding='utf-8').read())

def mono(text, size=12):
    return f'<span style="font-family:{MONO};font-size:{size}px">{text}</span>'

# ══ Broadcast ═══════════════════════════════════════════════════════════
cond = lambda a, op, b: (f'<div style="display:flex;align-items:center;gap:10px">{select(a,180)}{select(op,120)}{select(b,190)}'
                         f'<span style="color:{T["muted"]}">{ic("dots",16)}</span></div>')
recipients = ('<div style="display:flex;flex-direction:column;gap:10px">'
  + cond("Lifecycle stage", "คือ", "Hot Lead")
  + cond("แท็ก", "มีอย่างน้อยหนึ่ง", "seaview, villa")
  + cond("ช่องทาง", "คือ", "LINE")
  + f'<div style="display:flex;align-items:center;gap:8px;font-size:12.5px;color:{T["accentLight"]}">{ic("plus",14)}เพิ่มเงื่อนไข</div></div>')

PAST = [("โปรฯ ปีใหม่ Marina Golden Bay","2 ม.ค.","1,164"),
        ("เปิดตัวเฟส 2 The Panora","18 ธ.ค.","931"),
        ("เชิญชมห้องตัวอย่าง Copacabana","3 ธ.ค.","598")]
compact_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid {T["line"]};font-size:12.5px">'
  f'<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{n}</span>'
  f'<span style="flex:none;color:{T["muted"]};font-size:11.5px">{d}</span>'
  f'<span style="flex:none;color:{T["ok"]};font-variant-numeric:tabular-nums">{ok}</span></div>'
  for n, d, ok in PAST)

broadcast = page(rail("megaphone") + f'''
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar("Chat Broadcast", btn("บันทึกฉบับร่าง","ghost") + '<div style="width:10px"></div>' + btn("ตั้งเวลาส่ง","primary","clock"), "ส่งข้อความถึงกลุ่มลูกค้าตามแท็กและ lifecycle stage")}
    <div style="flex:1;display:flex;gap:18px;padding:8px 28px 24px;min-height:0;overflow:hidden">
      <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:16px">
        {card(label("แคมเปญ") + '<div style="height:12px"></div>'
          + f'<div style="display:flex;gap:12px">{field("ชื่อแคมเปญ (เห็นเฉพาะภายใน)", "เชิญชมพูลวิลล่าวิวทะเล เสาร์ 20 ก.ย.")}{field("ช่องทางที่ส่ง", "LINE", 180)}</div>')}
        {card(label("ผู้รับ") + '<div style="height:12px"></div>' + recipients + '<div style="height:14px"></div>'
          + f'<div style="display:flex;align-items:center;gap:14px;background:{T["card"]};border:1px solid rgba(124,111,240,0.28);border-radius:12px;padding:13px 16px">'
          + f'<span style="font-weight:800;font-size:24px;color:{T["accentLight"]};font-variant-numeric:tabular-nums">1,240</span>'
          + f'<span style="font-size:12.5px;color:{T["muted"]};line-height:1.65">คนที่ตรงเงื่อนไข · ในนี้ 96 คนไม่ได้คุยกับเราใน 24 ชม. ที่ผ่านมา<br>ระบบจะสลับไปใช้เทมเพลตที่อนุมัติแล้วให้อัตโนมัติ</span></div>')}
        {card(label("ข้อความ") + '<div style="height:12px"></div>'
          + f'<div style="border:1px solid rgba(255,255,255,0.14);border-radius:12px;padding:13px 15px;font-size:13.5px;line-height:1.75;min-height:104px;background:rgba(255,255,255,0.03)">'
          + f'สวัสดีค่ะ คุณ<span style="background:{T["card"]};color:{T["accentLight"]};border-radius:6px;padding:1px 7px;font-size:12.5px">ชื่อลูกค้า</span> '
          + 'GTG ขอเชิญชมพูลวิลล่าวิวทะเล โครงการ Marina Golden Bay วันเสาร์ที่ 20 ก.ย. เวลา 10:00 น. มีรถรับส่งจากพัทยาใต้ฟรีค่ะ<br>กดตอบกลับข้อความนี้เพื่อจองรอบเข้าชมได้เลยค่ะ</div>'
          + f'<div style="height:10px"></div><div style="display:flex;align-items:center;gap:16px;font-size:12px;color:{T["muted"]}">'
          + f'<span style="display:flex;align-items:center;gap:6px">{ic("plus",14)}แทรกตัวแปร</span>'
          + f'<span style="display:flex;align-items:center;gap:6px">{ic("note",14)}เลือกเทมเพลต</span>'
          + '<div style="flex:1"></div>238 / 1,000 อักขระ</div>')}
      </div>

      <div style="width:330px;flex:none;display:flex;flex-direction:column;gap:16px">
        {card(label("ตัวอย่างบนเครื่องลูกค้า") + '<div style="height:14px"></div>'
          + f'<div style="background:rgba(255,255,255,0.03);border:1px solid {T["cardBorder"]};border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:10px">'
          + f'<div style="display:flex;align-items:center;gap:9px">{avatar("G",30)}<div style="display:flex;flex-direction:column">'
          + f'<span style="font-size:12.5px;font-weight:700">GTG Property</span><span style="font-size:11px;color:{T["muted"]}">LINE Official Account</span></div></div>'
          + f'<div style="background:rgba(255,255,255,0.06);border-radius:14px 14px 14px 4px;padding:11px 13px;font-size:13px;line-height:1.7">'
          + 'สวัสดีค่ะ คุณสมชาย GTG ขอเชิญชมพูลวิลล่าวิวทะเล โครงการ Marina Golden Bay วันเสาร์ที่ 20 ก.ย. 10:00 น. ค่ะ</div></div>')}
        {card(label("กำหนดส่ง") + '<div style="height:12px"></div>'
          + f'<div style="display:flex;gap:10px">{select("18 ก.ย. 2569",148)}{select("09:00 น.",114)}</div>'
          + f'<div style="height:12px"></div><div style="display:flex;flex-direction:column;gap:8px;font-size:12.5px;color:{T["muted"]}">'
          + f'<div style="display:flex;justify-content:space-between"><span>ทยอยส่ง</span><span style="color:{T["ink"]}">60 ข้อความ / นาที</span></div>'
          + f'<div style="display:flex;justify-content:space-between"><span>ใช้เวลาโดยประมาณ</span><span style="color:{T["ink"]}">21 นาที</span></div></div>')}
        {card(label("แคมเปญล่าสุด") + '<div style="height:10px"></div>' + compact_rows)}
        {card(f'<div style="display:flex;align-items:flex-start;gap:10px">'
          + f'<span style="color:{T["warn"]};flex:none;margin-top:1px">{ic("shield",17,1.7,T["warn"])}</span>'
          + f'<div style="font-size:12.5px;color:{T["muted"]};line-height:1.7">ผู้รับ 96 คนพ้นหน้าต่าง 24 ชั่วโมงแล้ว ระบบจะข้ามให้อัตโนมัติ · <span style="color:{T["accentLight"]}">ดูรายชื่อ</span></div></div>', 14)}
      </div>
    </div>
  </div>''')
write("Broadcast.dc.html", broadcast)

# ══ Settings › Integrations (Agency Care API) ═══════════════════════════
SUBNAV = ["ทั่วไป","ช่องทาง","ผู้ใช้และสิทธิ์","Custom fields","ข้อความสำเร็จรูป","Integrations","การแจ้งเตือน"]
def subnav(active):
    items = "".join(
      f'<div style="display:flex;align-items:center;height:36px;padding:0 12px;border-radius:12px;font-size:13.5px;'
      + (f'background:{NAV_ACTIVE};color:#fff;font-weight:700' if n == active else f'color:{T["muted"]}')
      + f'">{n}</div>' for n in SUBNAV)
    return (f'<div style="width:212px;flex:none;border-right:1px solid {T["cardBorder"]};padding:8px 10px;'
            f'display:flex;flex-direction:column;gap:3px">{items}</div>')

KEYS = [("Agency Care (production)","gtg_7f3a…","read, write","วันนี้ 09:21 น.","ใช้งานอยู่","ok"),
        ("Agency Care (staging)","gtg_b1c9…","read","8 ก.ย. 2569","ใช้งานอยู่","ok"),
        ("รายงานการตลาด (เก่า)","gtg_20df…","read","28 ส.ค. 2569","เพิกถอนแล้ว","muted")]
key_head = (f'<div style="display:flex;align-items:center;gap:12px;padding-bottom:8px;font-size:11.5px;font-weight:700;'
            f'letter-spacing:.04em;text-transform:uppercase;color:{T["muted"]}">'
            f'<span style="flex:1">ชื่อ</span><span style="width:92px;flex:none">คีย์</span>'
            f'<span style="width:80px;flex:none">สิทธิ์</span><span style="width:104px;flex:none">ใช้ล่าสุด</span>'
            f'<span style="width:88px;flex:none">สถานะ</span></div>')
key_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid {T["cardBorder"]};font-size:13px">'
  f'<span style="flex:1;min-width:0;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{n}</span>'
  f'<span style="width:92px;flex:none">{mono(k,11.5)}</span>'
  f'<span style="width:80px;flex:none;color:{T["muted"]};font-size:12px">{sc}</span>'
  f'<span style="width:104px;flex:none;color:{T["muted"]};font-size:12px">{lu}</span>'
  f'<span style="width:88px;flex:none">{pill(st,tone)}</span></div>'
  for n, k, sc, lu, st, tone in KEYS)

def event_chip(name, on):
    box = (f'<span style="width:15px;height:15px;flex:none;border-radius:5px;background:{T["accent"]};'
           f'display:flex;align-items:center;justify-content:center">{ic("check",10,2.6,"#fff")}</span>') if on else \
          f'<span style="width:15px;height:15px;flex:none;border-radius:5px;border:1px solid rgba(255,255,255,0.22)"></span>'
    col = T['ink'] if on else T['muted']
    return (f'<span style="display:inline-flex;align-items:center;gap:8px;height:32px;padding:0 12px;border-radius:9px;'
            f'border:1px solid {"rgba(124,111,240,0.35)" if on else "rgba(255,255,255,0.10)"};'
            f'background:{"rgba(124,111,240,0.12)" if on else "transparent"};color:{col};font-family:{MONO};font-size:11.5px">{box}{name}</span>')

DELIVERIES = [("contact.lifecycle_changed","200","09:21:04","สำเร็จ","ok"),
              ("contact.lifecycle_changed","504","08:52:11","หมดเวลา","danger")]
del_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid {T["cardBorder"]};font-size:12.5px">'
  f'<span style="flex:1;min-width:0">{mono(ev,11.5)}</span>'
  f'<span style="width:44px;flex:none;font-family:{MONO};color:{T["danger"] if code != "200" else T["muted"]}">{code}</span>'
  f'<span style="width:68px;flex:none;color:{T["muted"]}">{tm} น.</span>'
  f'<span style="width:82px;flex:none">{pill(st,tone)}</span>'
  + (f'<span style="width:48px;flex:none;text-align:right;color:{T["accentLight"]};font-size:12px">ส่งซ้ำ</span>'
     if code != "200" else '<span style="width:48px;flex:none"></span>') + '</div>'
  for ev, code, tm, st, tone in DELIVERIES)

CODE_LINES = [
  ('curl -H "X-API-Key: $GTG_KEY" \\', T['ink']),
  ('  "https://chat.gtg.co.th/api/v1/', T['ink']),
  ('   contacts?stage=hot_lead"', T['ink']),
  ('', T['muted']),
  ('# ตรวจลายเซ็นฝั่งรับ webhook', T['muted']),
  ('sha256 = hmac(secret,', T['ink']),
  ('  timestamp + "." + rawBody)', T['ink']),
]
code_html = "".join(
  f'<div style="color:{c};white-space:pre">{l if l else "&nbsp;"}</div>' for l, c in CODE_LINES)

ENDPOINTS = [("GET","/api/v1/contacts"),("GET","/api/v1/contacts/:id"),
             ("POST","/api/v1/contacts/:id/lifecycle"),("GET","/api/v1/conversations"),
             ("GET","/api/v1/conversations/:id/messages"),("POST","/api/v1/conversations/:id/messages"),
             ("GET","/api/v1/stats/dashboard")]
ep_rows = "".join(
  f'<div style="display:flex;gap:9px;align-items:baseline;padding:6px 0;border-bottom:1px dashed {T["cardBorder"]};font-size:11.5px">'
  f'<span style="width:36px;flex:none;color:{T["accentLight"]};font-family:{MONO};font-weight:500">{m}</span>'
  f'<span style="font-family:{MONO};color:{T["ink"]};word-break:break-all">{p}</span></div>' for m, p in ENDPOINTS)

integrations = page(rail("settings") + f'''
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar('<span style="color:' + T['muted'] + '">Settings ›</span> Integrations',
            btn("เอกสาร API","ghost","link") + '<div style="width:10px"></div>' + btn("ออก API key ใหม่","primary","key"),
            "กุญแจและ webhook ที่ Agency Care ใช้คุยกับโมดูลแชท")}
    <div style="flex:1;display:flex;min-height:0;padding:6px 28px 20px;gap:16px">
      {subnav("Integrations")}
      <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">
        <div style="display:flex;align-items:flex-start;gap:12px;background:{T['card']};border:1px solid rgba(124,111,240,0.35);border-radius:16px;padding:14px 16px">
          <span style="color:{T['accentLight']};flex:none;margin-top:1px">{ic("key",18)}</span>
          <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:7px">
            <span style="font-size:13px;font-weight:700">คีย์ใหม่ของ Agency Care (production)</span>
            <div style="display:flex;align-items:center;gap:10px;background:rgba(0,0,0,0.28);border:1px solid rgba(124,111,240,0.3);border-radius:10px;padding:9px 12px">
              {mono("gtg_7f3a91c4e08b25da6c1f47b930ee5a02", 12)}<div style="flex:1"></div>
              <span style="color:{T['accentLight']};font-size:12.5px">คัดลอก</span>
            </div>
            <span style="font-size:12px;color:{T['muted']}">แสดงครั้งเดียว — ระบบเก็บไว้เป็น hash เท่านั้น ถ้าทำหายต้องออกใบใหม่</span>
          </div>
        </div>

        {card(f'<div style="display:flex;align-items:center;gap:12px">{label("API keys")}<div style="flex:1"></div>'
          + f'<span style="font-size:12px;color:{T["muted"]}">จำกัด 120 ครั้ง/นาที ต่อคีย์</span></div>'
          + '<div style="height:12px"></div>' + key_head + key_rows, 16)}

        {card(f'{label("Webhook ขาออก")}<div style="height:12px"></div>'
          + f'<div style="display:flex;gap:12px">{field("ปลายทาง", "https://agency-care.gtg.co.th/hooks/gtg-chat")}{field("Secret", "whsec_••••••9f21", 168, True)}</div>'
          + '<div style="height:12px"></div>'
          + f'<div style="display:flex;flex-wrap:wrap;gap:8px">{event_chip("contact.lifecycle_changed",True)}{event_chip("conversation.created",True)}{event_chip("message.received",False)}</div>'
          + '<div style="height:12px"></div>'
          + f'<div style="display:flex;align-items:center;gap:10px">{btn("ส่ง event ทดสอบ","ghost","send",32)}{btn("หมุน secret ใหม่","ghost",None,32)}'
          + f'<div style="flex:1"></div><span style="font-size:12px;color:{T["muted"]}">7 วันล่าสุด: สำเร็จ 1,241 · ล้มเหลว 3</span></div>', 16)}

        {card(f'<div style="display:flex;align-items:center;gap:12px">{label("บันทึกการส่ง")}<div style="flex:1"></div>'
          + f'<span style="font-size:12.5px;color:{T["accentLight"]}">ดูทั้งหมด</span></div><div style="height:10px"></div>' + del_rows, 16)}
      </div>

      <div style="width:296px;flex:none;display:flex;flex-direction:column;gap:14px">
        {card(f'{label("เรียกใช้จาก Agency Care")}<div style="height:12px"></div>'
          + f'<div style="background:#0d0b17;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:13px;'
          + f'font-family:{MONO};font-size:11px;line-height:1.85;overflow:hidden">{code_html}</div>'
          + f'<div style="height:10px"></div><span style="font-size:12px;color:{T["muted"]};line-height:1.7">ฝั่งรับต้องเทียบลายเซ็นแบบ timing-safe และปฏิเสธ timestamp ที่เก่ากว่า 5 นาที</span>', 16)}
        {card(f'{label("Endpoint ที่เปิดให้")}<div style="height:10px"></div>' + ep_rows, 16)}
      </div>
    </div>
  </div>''')
write("SettingsIntegrations.dc.html", integrations)
