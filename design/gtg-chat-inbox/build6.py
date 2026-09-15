# -*- coding: utf-8 -*-
exec(open('gen.py', encoding='utf-8').read())

def tabbar(active):
    items = []
    for key, lbl in [("inbox","Inbox"),("users","Contacts"),("chart","Dashboard"),("settings","ตั้งค่า")]:
        on = key == active
        col = T['accent'] if on else T['muted']
        badge = (f'<span style="position:absolute;top:-3px;right:-9px;min-width:16px;height:16px;border-radius:999px;'
                 f'background:{T["warn"]};color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center;padding:0 4px">3</span>') if key == "inbox" else ""
        items.append(
          f'<div style="flex:1;height:52px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;color:{col}">'
          f'<span style="position:relative;display:flex">{ic(key,22)}{badge}</span>'
          f'<span style="font-family:{DISPLAY};font-size:10.5px;font-weight:600">{lbl}</span></div>')
    return (f'<div style="flex:none;border-top:1px solid {T["line"]};background:{T["surface"]};display:flex;'
            f'padding:6px 4px 14px">{"".join(items)}</div>')

# ── Mobile Inbox ────────────────────────────────────────────────────────
MTABS = [("ทั้งหมด","24",True),("ยังไม่มีคนรับ","3",False),("ของฉัน","8",False)]
mtabs = "".join(
  f'<div style="display:flex;align-items:center;gap:6px;height:32px;padding:0 13px;border-radius:999px;font-size:13px;flex:none;'
  + (f'background:{T["accent"]};color:#fff' if on else f'background:{T["surface"]};color:{T["muted"]};border:1px solid {T["line"]}')
  + f'">{n}<span style="opacity:.8">{c}</span></div>' for n, c, on in MTABS)

MCONVS = [
  ("สม","คุณสมชาย ส.","LINE","คุณ: สะดวกเข้าชมวันเสาร์ 10:00 น. ไหมครับ","09:24","Hot Lead","accent","Ploy"),
  ("AP","Anna Petrova","LINE","Is the seaview unit still available?","09:11","New Lead","muted","Ivan"),
  ("ИВ","Иван Волков","Facebook","Здравствуйте, интересует вилла","08:57","New Lead","muted",None),
  ("ธน","คุณธนากร ว.","WhatsApp","โอนเงินจองแล้วครับ ส่งสลิปให้ทางนี้","08:40","Payment","accent","Ploy"),
  ("MT","Mya Thu","LINE","ขอดูห้องตัวอย่างวันเสาร์ได้ไหมคะ","เมื่อวาน","Hot Lead","accent","Nok"),
  ("CW","Chen Wei","Facebook","请问还有海景公寓吗","เมื่อวาน","New Lead","muted",None),
]
mrows = "".join(
  f'<div style="display:flex;gap:12px;padding:14px 16px;border-bottom:1px solid {T["line"]};background:{T["surface"]}">'
  f'{avatar(ini,44)}'
  f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:5px">'
  f'<div style="display:flex;align-items:baseline;gap:8px">'
  f'<span style="font-weight:600;font-size:14.5px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{name}</span>'
  f'<span style="font-size:11.5px;color:{T["muted"]};flex:none">{time}</span></div>'
  f'<span style="font-size:13px;color:{T["muted"]};overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{snip}</span>'
  f'<div style="display:flex;align-items:center;gap:7px">{chan(ch)}{pill(stage,tone)}'
  + (pill(who,"muted") if who else pill("ยังไม่มีคนรับ","warn")) + '</div></div></div>'
  for ini, name, ch, snip, time, stage, tone, who in MCONVS)

mobile_inbox = f'''<div style="width:390px;height:844px;display:flex;flex-direction:column;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  <div style="flex:none;height:56px;display:flex;align-items:center;gap:12px;padding:0 16px;background:{T['surface']};border-bottom:1px solid {T['line']}">
    <span style="font-family:{DISPLAY};font-weight:600;font-size:18px">Inbox</span>
    <div style="flex:1"></div>
    <span style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:{T['muted']}">{ic("search",21)}</span>
    <span style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:{T['muted']}">{ic("filter",21)}</span>
    {avatar("PL",34)}
  </div>
  <div style="flex:none;display:flex;gap:6px;padding:12px 14px;background:{T['bg']};border-bottom:1px solid {T['line']};overflow:hidden">{mtabs}</div>
  <div style="flex:1;overflow:hidden;display:flex;flex-direction:column">{mrows}</div>
  {tabbar("inbox")}
</div>'''
write("MobileInbox.dc.html", mobile_inbox)

# ── Mobile conversation ─────────────────────────────────────────────────
MMSGS = [
  ("in","09:18","สวัสดีครับ สนใจพูลวิลล่า 3 ห้องนอน แถวบางเสร่ ราคาเท่าไหร่ครับ"),
  ("auto","09:18","สวัสดีค่ะ ขอบคุณที่ติดต่อ GTG ทีมงานกำลังตรวจสอบและจะตอบกลับโดยเร็วที่สุดค่ะ"),
  ("in","09:20","ถ้ามีวิวทะเลจะดีมากครับ งบราว 12–15 ล้าน"),
  ("out","09:22","พูลวิลล่า 3 ห้องนอน Marina Golden Bay เริ่ม 12.9 ล้านครับ เหลือวิวทะเล 2 ยูนิต"),
  ("out","09:24","สะดวกเข้าชมวันเสาร์ 10:00 น. ไหมครับ"),
]
mm = []
for kind, time, text in MMSGS:
    if kind == "in":
        mm.append(f'<div style="align-self:flex-start;max-width:280px;display:flex;flex-direction:column;gap:3px">'
                  f'<div style="background:{T["surface"]};border:1px solid {T["line"]};border-radius:14px 14px 14px 4px;padding:10px 13px;font-size:14px;line-height:1.6">{text}</div>'
                  f'<span style="font-size:10.5px;color:{T["muted"]}">{time} น.</span></div>')
    else:
        bgc = "rgba(124,111,240,0.30)" if kind == "auto" else BTN_GRAD
        who = "ระบบอัตโนมัติ · " if kind == "auto" else ""
        mm.append(f'<div style="align-self:flex-end;max-width:280px;display:flex;flex-direction:column;gap:3px;align-items:flex-end">'
                  f'<div style="background:{bgc};color:#fff;border-radius:14px 14px 4px 14px;padding:10px 13px;font-size:14px;line-height:1.6">{text}</div>'
                  f'<span style="font-size:10.5px;color:{T["muted"]}">{who}{time} น.</span></div>')

mobile_chat = f'''<div style="width:390px;height:844px;display:flex;flex-direction:column;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  <div style="flex:none;height:60px;display:flex;align-items:center;gap:10px;padding:0 8px 0 4px;background:{T['surface']};border-bottom:1px solid {T['line']}">
    <span style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:{T['ink']}">{ic("back",22)}</span>
    {avatar("สม",36)}
    <div style="flex:1;display:flex;flex-direction:column;gap:1px;min-width:0">
      <span style="font-family:{DISPLAY};font-weight:600;font-size:15px">คุณสมชาย ส.</span>
      <div style="display:flex;align-items:center;gap:7px">{chan("LINE")}{pill("Hot Lead","accent")}</div>
    </div>
    <span style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:{T['muted']}">{ic("dots",20)}</span>
  </div>
  <div style="flex:none;display:flex;align-items:center;gap:8px;padding:9px 16px;background:{T['card']};font-size:12px;color:{T['accentLight']}">
    {ic("users",14)}มอบหมายให้ Ploy โดยระบบอัตโนมัติ
    <div style="flex:1"></div><span style="color:{T['muted']}">เปลี่ยน</span>
  </div>
  <div style="flex:1;overflow:hidden;padding:16px;display:flex;flex-direction:column;gap:12px">{"".join(mm)}</div>
  <div style="flex:none;border-top:1px solid {T['line']};background:{T['surface']};padding:10px 12px 16px;display:flex;align-items:flex-end;gap:10px">
    <span style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:{T['muted']}">{ic("note",21)}</span>
    <div style="flex:1;min-height:44px;display:flex;align-items:center;border:1px solid {T['line']};border-radius:22px;padding:0 16px;color:{T['muted']};font-size:14px">พิมพ์ข้อความ…</div>
    <span style="width:44px;height:44px;border-radius:50%;background:{T['accent']};color:#fff;display:flex;align-items:center;justify-content:center">{ic("send",20,1.7,"#fff")}</span>
  </div>
</div>'''
write("MobileChat.dc.html", mobile_chat)
