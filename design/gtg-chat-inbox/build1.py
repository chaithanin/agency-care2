# -*- coding: utf-8 -*-
exec(open('gen.py', encoding='utf-8').read())

# ── Login ───────────────────────────────────────────────────────────────
bullets = "".join(
  f'<div style="display:flex;align-items:flex-start;gap:10px;color:rgba(236,235,245,0.78);font-size:14px">'
  f'<span style="margin-top:3px;color:{T["accentLight"]}">{ic("check",16,1.8)}</span><span>{t}</span></div>'
  for t in ["ทุกช่องทางแชทรวมอยู่ในกล่องเดียว",
            "มอบหมายงานและติดตาม lifecycle ของลูกค้าได้ในที่เดียว",
            "ต่อกับ Agency Care ผ่าน API และ webhook"])

login = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']}">
  <div style="width:560px;flex:none;background:linear-gradient(160deg,#1a1533 0%,#231b45 45%,#3b2f77 100%);color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:56px 56px 48px">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:40px;height:40px;border-radius:12px;background:#fff;color:{T['accentLight']};display:flex;align-items:center;justify-content:center;font-family:{DISPLAY};font-weight:700;font-size:17px">G</div>
      <span style="font-family:{DISPLAY};font-weight:600;font-size:17px;letter-spacing:.01em">GTG Chat</span>
    </div>
    <div style="display:flex;flex-direction:column;gap:24px;max-width:430px">
      <h1 style="margin:0;font-family:{DISPLAY};font-weight:700;font-size:40px;line-height:1.2;text-wrap:balance">กล่องข้อความเดียว<br>สำหรับลูกค้าทุกช่องทาง</h1>
      <div style="display:flex;flex-direction:column;gap:12px">{bullets}</div>
    </div>
    <div style="font-size:12.5px;color:{T["muted"]}">ระบบภายในของ GTG · เชื่อมกับ Agency Care</div>
  </div>

  <div style="flex:1;display:flex;align-items:center;justify-content:center;padding:40px">
    <div style="width:400px;display:flex;flex-direction:column;gap:22px">
      <div style="display:flex;flex-direction:column;gap:6px">
        <h2 style="margin:0;font-family:{DISPLAY};font-weight:600;font-size:26px">เข้าสู่ระบบ</h2>
        <span style="font-size:13.5px;color:{T['muted']}">ใช้บัญชีอีเมลของบริษัท</span>
      </div>
      <div style="display:flex;flex-direction:column;gap:14px">
        {field("อีเมล", "ploy@gtg.co.th")}
        {field("รหัสผ่าน", "••••••••••••")}
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;font-size:13px">
        <div style="display:flex;align-items:center;gap:8px;color:{T['muted']}">
          <span style="width:16px;height:16px;border-radius:4px;border:1px solid {T['accent']};background:{T['accent']};color:#fff;display:flex;align-items:center;justify-content:center">{ic("check",11,2.4,"#fff")}</span>
          จำฉันไว้ในเครื่องนี้
        </div>
        <a href="#">ลืมรหัสผ่าน</a>
      </div>
      <div style="height:44px;border-radius:12px;background:{BTN_GRAD};box-shadow:{BTN_SHADOW};color:#fff;display:flex;align-items:center;justify-content:center;font-family:{DISPLAY};font-weight:600;font-size:15px">เข้าสู่ระบบ</div>
      <div style="display:flex;align-items:center;gap:12px;color:{T['muted']};font-size:12px">
        <span style="flex:1;height:1px;background:{T['line']}"></span>หรือ<span style="flex:1;height:1px;background:{T['line']}"></span>
      </div>
      <div style="height:44px;border-radius:12px;border:1px solid rgba(255,255,255,0.14);background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center;gap:9px;font-size:14px">{ic("mail",17)}ใช้บัญชี Google Workspace ของ GTG</div>
      <div style="font-size:12px;color:{T['muted']};text-align:center;line-height:1.7">การเข้าใช้งานถูกบันทึกไว้ทั้งหมด<br>หากลืมรหัสผ่านให้ติดต่อผู้ดูแลระบบ</div>
    </div>
  </div>
</div>'''
write("Login.dc.html", login)

# ── Inbox (Main) ────────────────────────────────────────────────────────
TABS = [("ทั้งหมด","24",True),("ยังไม่มีคนรับ","3",False),("มอบหมายแล้ว","21",False),("ของฉัน","8",False),("ปิดแล้ว","162",False)]
tabs_html = "".join(
  f'<div style="display:flex;align-items:center;gap:6px;height:28px;padding:0 11px;border-radius:999px;font-size:12.5px;'
  + (f'background:{T["accent"]};color:#fff;border:1px solid {T["accent"]}' if on else f'background:{T["surface"]};color:{T["muted"]};border:1px solid {T["line"]}')
  + f'">{name}<span style="opacity:.8;font-variant-numeric:tabular-nums">{n}</span></div>'
  for name, n, on in TABS)

CONVS = [
  ("สม","คุณสมชาย ส.","LINE","คุณ: สะดวกเข้าชมวันเสาร์ 10:00 น. ไหมครับ","09:24","Hot Lead","accent","Ploy",True),
  ("AP","Anna Petrova","LINE","Is the seaview unit still available?","09:11","New Lead","muted","Ivan",False),
  ("ИВ","Иван Волков","Facebook","Здравствуйте, интересует вилла с бассейном","08:57","New Lead","muted",None,False),
  ("ธน","คุณธนากร ว.","WhatsApp","โอนเงินจองแล้วครับ ส่งสลิปให้ทางนี้","08:40","Payment","accent","Ploy",False),
  ("MT","Mya Thu","LINE","ขอดูห้องตัวอย่างวันเสาร์ได้ไหมคะ","เมื่อวาน","Hot Lead","accent","Nok",False),
  ("CW","Chen Wei","Facebook","请问还有海景公寓吗","เมื่อวาน","New Lead","muted",None,False),
]
rows = []
for ini, name, ch, snippet, time, stage, tone, who, active in CONVS:
    bgc = T['inb'] if active else T['surface']
    bar = f'border-left:3px solid {T["accent"]};padding-left:13px' if active else f'border-left:3px solid transparent;padding-left:13px'
    assignee = pill(who, "muted") if who else pill("ยังไม่มีคนรับ", "warn")
    rows.append(
      f'<div style="display:flex;gap:11px;padding:13px 16px 13px 0;background:{bgc};{bar};border-bottom:1px solid {T["line"]}">'
      f'{avatar(ini,36)}'
      f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:4px">'
      f'<div style="display:flex;align-items:baseline;gap:8px">'
      f'<span style="font-weight:600;font-size:14px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{name}</span>'
      f'<span style="font-size:11.5px;color:{T["muted"]};flex:none">{time}</span></div>'
      f'<div style="font-size:13px;color:{T["muted"]};overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{snippet}</div>'
      f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">{chan(ch)}{pill(stage,tone)}{assignee}</div>'
      f'</div></div>')

MSGS = [
  ("in","คุณสมชาย ส.","09:18","สวัสดีครับ สนใจพูลวิลล่า 3 ห้องนอน แถวบางเสร่ ราคาเท่าไหร่ครับ"),
  ("auto","ระบบอัตโนมัติ","09:18","สวัสดีค่ะ ขอบคุณที่ติดต่อ GTG ทีมงานกำลังตรวจสอบและจะตอบกลับโดยเร็วที่สุดค่ะ"),
  ("in","คุณสมชาย ส.","09:20","ถ้ามีวิวทะเลจะดีมากครับ งบประมาณราว 12–15 ล้าน"),
  ("out","Ploy","09:22","พูลวิลล่า 3 ห้องนอน โครงการ Marina Golden Bay เริ่ม 12.9 ล้านครับ ตอนนี้เหลือวิวทะเล 2 ยูนิตครับ"),
  ("out","Ploy","09:24","สะดวกเข้าชมวันเสาร์ 10:00 น. ไหมครับ ผมจองรถรับส่งจากในเมืองให้ได้ครับ"),
]
msgs = []
for kind, who, time, text in MSGS:
    if kind == "in":
        msgs.append(
          f'<div style="align-self:flex-start;max-width:560px;display:flex;flex-direction:column;gap:3px">'
          f'<span style="font-size:11px;color:{T["muted"]}">{who} · {time}</span>'
          f'<div style="background:{T["inb"]};border-radius:14px 14px 14px 4px;padding:10px 14px;font-size:14px;line-height:1.65">{text}</div></div>')
    else:
        bgc = "rgba(124,111,240,0.30)" if kind == "auto" else BTN_GRAD
        tagtxt = "ระบบอัตโนมัติ" if kind == "auto" else who
        msgs.append(
          f'<div style="align-self:flex-end;max-width:560px;display:flex;flex-direction:column;gap:3px;align-items:flex-end">'
          f'<span style="font-size:11px;color:{T["muted"]}">{tagtxt} · {time}</span>'
          f'<div style="background:{bgc};color:#fff;border-radius:14px 14px 4px 14px;padding:10px 14px;font-size:14px;line-height:1.65">{text}</div></div>')

def kv(k, v):
    return (f'<div style="display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px dashed {T["line"]};font-size:13px">'
            f'<span style="color:{T["muted"]}">{k}</span><span style="text-align:right">{v}</span></div>')

tags_html = "".join(pill(t,"accent") for t in ["villa","pricing","seaview"])
fields_html = "".join(kv(k,v) for k,v in [
  ("โครงการที่สนใจ","Marina Golden Bay"),("งบประมาณ","12–15 ล้าน"),("สัญชาติ","ไทย"),("วัตถุประสงค์","อยู่เอง")])

panel = f'''<div style="width:300px;flex:none;border-left:1px solid {T['line']};background:{T['surface']};padding:18px;display:flex;flex-direction:column;gap:18px;overflow:hidden">
  <div style="display:flex;align-items:center;gap:12px">
    {avatar("สม",44)}
    <div style="display:flex;flex-direction:column;gap:2px">
      <span style="font-family:{DISPLAY};font-weight:600;font-size:15px">คุณสมชาย ส.</span>
      <span style="font-size:12px;color:{T['muted']}">ลูกค้าตั้งแต่ 12 ก.ย. 2569</span>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:2px">
    {kv("ภาษา","ไทย")}{kv("โทรศัพท์","08X-XXX-4412")}{kv("อีเมล","—")}{kv("เจ้าของเคส","Ploy (Sales)")}
  </div>
  <div style="display:flex;flex-direction:column;gap:9px">
    {label("Lifecycle stage")}
    {select("Hot Lead", 252)}
    <div style="display:flex;align-items:center;gap:6px;font-size:11.5px;color:{T['muted']}">{ic("clock",13)}เปลี่ยนโดย Ploy เมื่อ 09:21</div>
  </div>
  <div style="display:flex;flex-direction:column;gap:9px">
    {label("แท็ก")}
    <div style="display:flex;flex-wrap:wrap;gap:6px">{tags_html}
      <span style="display:inline-flex;align-items:center;gap:4px;height:22px;padding:0 9px;border-radius:999px;border:1px dashed {T['line']};color:{T['muted']};font-size:11.5px">{ic("plus",12)}เพิ่ม</span>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:6px">
    {label("ข้อมูลเพิ่มเติม")}
    <div style="display:flex;flex-direction:column;gap:2px">{fields_html}</div>
  </div>
  <div style="margin-top:auto;border:1px solid {T['line']};border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:8px;background:{T['bg']}">
    <div style="display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600">{ic("link",15,1.6,T['accentLight'])}Agency Care</div>
    <div style="font-size:12px;color:{T['muted']};line-height:1.6">ส่ง stage ล่าสุดให้แล้วเมื่อ 09:21 · ตอบกลับ 200</div>
    <a href="#" style="font-size:12.5px">เปิดผู้ติดต่อใน Agency Care</a>
  </div>
</div>'''

inbox = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  {rail("inbox")}
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar("Inbox", search_box("ค้นหาชื่อ เบอร์ หรือข้อความ", 260) + '<div style="width:10px"></div>' + btn("ตัวกรอง", "ghost", "filter") + btn("มอบหมายเป็นชุด", "ghost", "users"))}
    <div style="flex:1;display:flex;min-height:0">
      <div style="width:310px;flex:none;border-right:1px solid {T['line']};background:{T['surface']};display:flex;flex-direction:column;min-height:0">
        <div style="padding:12px 14px;display:flex;flex-wrap:wrap;gap:6px;border-bottom:1px solid {T['line']};background:{T['bg']}">{tabs_html}</div>
        <div style="padding:9px 14px;display:flex;align-items:center;gap:8px;border-bottom:1px solid {T['line']};font-size:12px;color:{T['muted']}">
          ช่องทาง{dot(CHAN['LINE'])}LINE{dot(CHAN['Facebook'])}Facebook{dot(CHAN['WhatsApp'])}WhatsApp
          <div style="flex:1"></div>ล่าสุดก่อน {ic("chevdown",13)}
        </div>
        <div style="flex:1;overflow:hidden;display:flex;flex-direction:column">{"".join(rows)}</div>
      </div>

      <div style="flex:1;display:flex;flex-direction:column;min-width:0;background:{T['bg']}">
        <div style="height:60px;flex:none;display:flex;align-items:center;gap:10px;padding:0 20px;background:{T['surface']};border-bottom:1px solid {T['line']}">
          {avatar("สม",34)}
          <div style="display:flex;flex-direction:column">
            <span style="font-family:{DISPLAY};font-weight:600;font-size:15px">คุณสมชาย ส.</span>
            <div style="display:flex;align-items:center;gap:8px">{chan("LINE")}<span style="font-size:11.5px;color:{T['muted']}">ตอบครั้งแรกใน 2 นาที</span></div>
          </div>
          <div style="flex:1"></div>
          {select("Ploy (Sales)", 164)}{btn("ปิดเคส","ghost","check")}
          <div style="color:{T['muted']};padding:0 2px">{ic("dots",18)}</div>
        </div>
        <div style="flex:1;overflow:hidden;padding:20px 24px;display:flex;flex-direction:column;gap:14px">{"".join(msgs)}</div>
        <div style="flex:none;border-top:1px solid {T['line']};background:{T['surface']};padding:12px 16px;display:flex;flex-direction:column;gap:10px">
          <div style="display:flex;align-items:center;gap:14px;color:{T['muted']};font-size:12.5px">
            <span style="display:flex;align-items:center;gap:6px">{ic("note",15)}ข้อความสำเร็จรูป</span>
            <span style="display:flex;align-items:center;gap:6px">{ic("bolt",15)}ให้ AI ร่างคำตอบ</span>
            <div style="flex:1"></div>
            <span>ตอบผ่าน LINE · เหลือโควตาเดือนนี้ 8,420 ข้อความ</span>
          </div>
          <div style="display:flex;gap:10px;align-items:flex-end">
            <div style="flex:1;min-height:44px;border:1px solid {T['line']};border-radius:10px;padding:11px 13px;color:{T['muted']};font-size:13.5px;background:{T['surface']}">พิมพ์ข้อความ… (Enter ส่ง / Shift+Enter ขึ้นบรรทัดใหม่)</div>
            <div style="width:46px;height:44px;border-radius:10px;background:{T['accent']};color:#fff;display:flex;align-items:center;justify-content:center">{ic("send",19,1.7,"#fff")}</div>
          </div>
        </div>
      </div>
      {panel}
    </div>
  </div>
</div>'''
write("Main.dc.html", inbox)
