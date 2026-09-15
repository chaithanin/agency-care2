# -*- coding: utf-8 -*-
exec(open('gen.py', encoding='utf-8').read())

SUBNAV = ["ทั่วไป","ช่องทาง","ผู้ใช้และสิทธิ์","Custom fields","ข้อความสำเร็จรูป","Integrations","การแจ้งเตือน","บันทึกการใช้งาน"]
def subnav(active):
    items = "".join(
      f'<div style="display:flex;align-items:center;gap:9px;height:38px;padding:0 12px;border-radius:9px;font-size:13.5px;'
      + (f'background:{T["card"]};color:{T["accentLight"]};font-weight:600' if n == active else f'color:{T["muted"]}')
      + f'">{n}</div>' for n in SUBNAV)
    return (f'<div style="width:236px;flex:none;border-right:1px solid {T["line"]};background:{T["surface"]};padding:16px 12px;'
            f'display:flex;flex-direction:column;gap:3px">'
            f'<div style="padding:0 12px 10px">{label("ตั้งค่า")}</div>{items}</div>')

def mono(text, size=12):
    return f'<span style="font-family:{MONO};font-size:{size}px">{text}</span>'

# ── Settings › ช่องทาง ───────────────────────────────────────────────────
def channel_card(name, color, status, tone, lines, actions):
    body = "".join(
      f'<div style="display:flex;justify-content:space-between;gap:16px;padding:8px 0;border-bottom:1px dashed {T["line"]};font-size:13px">'
      f'<span style="color:{T["muted"]}">{k}</span><span style="text-align:right">{v}</span></div>' for k, v in lines)
    return (f'<div style="background:{T["surface"]};border:1px solid {T["line"]};border-radius:16px;padding:15px 18px;'
            f'display:flex;flex-direction:column;gap:10px">'
            f'<div style="display:flex;align-items:center;gap:11px">'
            f'<span style="width:34px;height:34px;border-radius:10px;background:{color}1A;display:flex;align-items:center;justify-content:center">{dot(color,12)}</span>'
            f'<span style="font-family:{DISPLAY};font-weight:600;font-size:15px">{name}</span>{pill(status,tone)}'
            f'<div style="flex:1"></div>{actions}</div>'
            f'<div style="display:flex;flex-direction:column">{body}</div></div>')

copy_row = (f'<div style="display:flex;align-items:center;gap:8px">{mono("https://chat.gtg.co.th/webhook/line")}'
            f'<span style="color:{T["accentLight"]}">{ic("link",14)}</span></div>')

channels_screen = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  {rail("settings")}
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar('<span style="color:' + T['muted'] + '">ตั้งค่า ›</span> ช่องทาง', btn("เพิ่มช่องทาง","primary","plus"))}
    <div style="flex:1;display:flex;min-height:0">
      {subnav("ช่องทาง")}
      <div style="flex:1;padding:20px 24px;display:flex;flex-direction:column;gap:16px;overflow:hidden">
        {channel_card("LINE Official Account", CHAN["LINE"], "เชื่อมต่อแล้ว", "accent",
          [("ชื่อบัญชี","GTG Property @gtg-th"),("Webhook URL", copy_row),
           ("ตรวจลายเซ็น X-Line-Signature","เปิดอยู่"),("ข้อความเดือนนี้","1,580 / 10,000")],
          btn("ทดสอบการเชื่อมต่อ","ghost","bolt",30) + btn("ตั้งค่า","ghost",None,30))}
        {channel_card("Facebook Messenger", CHAN["Facebook"], "รอ App Review", "warn",
          [("เพจ","GTG Property Pattaya"),("สถานะคำขอ","ยื่นเมื่อ 8 ก.ย. · Meta ใช้เวลาโดยเฉลี่ย 2–4 สัปดาห์"),
           ("โหมดปัจจุบัน","ใช้ได้เฉพาะบัญชีทดสอบที่เพิ่มไว้ 3 บัญชี"),
           ("สิทธิ์ที่ขอ", mono("pages_messaging, pages_manage_metadata"))],
          btn("ดูสถานะที่ Meta","ghost","link",30))}
        {channel_card("WhatsApp Cloud API", CHAN["WhatsApp"], "ยังไม่เชื่อมต่อ", "muted",
          [("เบอร์ที่จะใช้","ยังไม่ได้ตั้งค่า"),("ต้องมีก่อน","Meta Business verification และเทมเพลตที่อนุมัติแล้ว")],
          btn("เชื่อมต่อ","primary","plus",30))}
        {channel_card("Instagram DM", CHAN["Instagram"], "ยังไม่เชื่อมต่อ", "muted",
          [("ใช้ Meta app เดิมร่วมกับ Messenger ได้","ต้องผ่าน App Review ของ Messenger ก่อน")],
          btn("เชื่อมต่อ","ghost","plus",30))}
      </div>
    </div>
  </div>
</div>'''
write("SettingsChannels.dc.html", channels_screen)
