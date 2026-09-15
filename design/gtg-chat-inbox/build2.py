# -*- coding: utf-8 -*-
exec(open('gen.py', encoding='utf-8').read())

def th(text, w=None, align="left"):
    w = f'width:{w}px;flex:none;' if w else 'flex:1;'
    return (f'<div style="{w}text-align:{align};font-family:{DISPLAY};font-size:11.5px;font-weight:600;'
            f'letter-spacing:.04em;color:{T["muted"]}">{text}</div>')

def td(html, w=None, align="left"):
    w = f'width:{w}px;flex:none;' if w else 'flex:1;min-width:0;'
    return f'<div style="{w}text-align:{align};font-size:13px;overflow:hidden">{html}</div>'

def checkbox(on=False):
    if on:
        return (f'<span style="width:16px;height:16px;flex:none;border-radius:4px;background:{T["accent"]};border:1px solid {T["accent"]};'
                f'color:#fff;display:flex;align-items:center;justify-content:center">{ic("check",11,2.4,"#fff")}</span>')
    return f'<span style="width:16px;height:16px;flex:none;border-radius:4px;border:1px solid {T["line"]};background:{T["surface"]}"></span>'

# ── Contacts ────────────────────────────────────────────────────────────
STAGES = [("ทั้งหมด","1,284",True),("New Lead","612",False),("Hot Lead","281",False),("Payment","74",False),("Customer","291",False),("Lost","26",False)]
stage_chips = "".join(
  f'<div style="display:flex;align-items:center;gap:7px;height:32px;padding:0 13px;border-radius:999px;font-size:13px;'
  + (f'background:{T["accent"]};color:#fff;border:1px solid {T["accent"]}' if on else f'background:{T["surface"]};color:{T["ink"]};border:1px solid {T["line"]}')
  + f'">{name}<span style="opacity:.7;font-variant-numeric:tabular-nums">{n}</span></div>'
  for name, n, on in STAGES)

PEOPLE = [
  ("สม","คุณสมชาย ส.","LINE","Hot Lead","accent","villa · seaview","Marina Golden Bay","Ploy","09:24 น.",True),
  ("AP","Anna Petrova","LINE","New Lead","muted","condo · investment","The Panora","Ivan","09:11 น.",False),
  ("ИВ","Иван Волков","Facebook","New Lead","muted","villa","—","—","08:57 น.",False),
  ("ธน","คุณธนากร ว.","WhatsApp","Payment","accent","condo","Copacabana","Ploy","08:40 น.",False),
  ("MT","Mya Thu","LINE","Hot Lead","accent","condo · rental","The Panora","Nok","เมื่อวาน",False),
  ("CW","Chen Wei","Facebook","New Lead","muted","seaview","—","—","เมื่อวาน",False),
  ("นภ","คุณนภัส ก.","LINE","New Lead","muted","pricing","Marina Golden Bay","Nok","เมื่อวาน",False),
  ("JD","James Doyle","WhatsApp","Customer","accent","investment","Copacabana","Ploy","2 วันก่อน",False),
]
prows = []
for ini, name, ch, stage, tone, tags, project, owner, seen, sel in PEOPLE:
    prows.append(
      f'<div style="display:flex;align-items:center;gap:14px;padding:12px 18px;border-bottom:1px solid {T["line"]};'
      f'background:{T["inb"] if sel else T["surface"]}">'
      f'{checkbox(sel)}'
      + td(f'<div style="display:flex;align-items:center;gap:10px">{avatar(ini,32)}<span style="font-weight:600;white-space:nowrap">{name}</span></div>')
      + td(chan(ch), 120) + td(pill(stage,tone), 110)
      + td(f'<span style="color:{T["muted"]}">{tags}</span>', 190)
      + td(project, 180) + td(owner, 90)
      + td(f'<span style="color:{T["muted"]}">{seen}</span>', 100, "right")
      + f'</div>')

contacts = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  {rail("users")}
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar("Contacts", search_box("ค้นหาชื่อ เบอร์ หรืออีเมล", 280) + '<div style="width:10px"></div>' + btn("ส่งออก CSV","ghost","arrowdown") + btn("สร้าง Broadcast","primary","megaphone"))}
    <div style="padding:16px 22px;display:flex;flex-direction:column;gap:12px;border-bottom:1px solid {T['line']};background:{T['surface']}">
      <div style="display:flex;flex-wrap:wrap;gap:8px">{stage_chips}</div>
      <div style="display:flex;align-items:center;gap:10px">
        {select("ทุกช่องทาง",150)}{select("ทุกแท็ก",150)}{select("เจ้าของ: ทุกคน",170)}{select("อัปเดต: 30 วันล่าสุด",200)}
        <div style="flex:1"></div>
        <span style="font-size:12.5px;color:{T['muted']}">เลือกไว้ 1 จาก 1,284 รายชื่อ</span>
        {btn("เปลี่ยน stage เป็นชุด","ghost","tag")}
      </div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;min-height:0;padding:18px 22px">
      <div style="flex:1;background:{T['surface']};border:1px solid {T['line']};border-radius:12px;overflow:hidden;display:flex;flex-direction:column">
        <div style="display:flex;align-items:center;gap:14px;padding:11px 18px;border-bottom:1px solid {T['line']};background:{T['bg']}">
          {checkbox(False)}{th("ชื่อ")}{th("ช่องทาง",120)}{th("Lifecycle",110)}{th("แท็ก",190)}{th("โครงการที่สนใจ",180)}{th("เจ้าของ",90)}{th("ติดต่อล่าสุด",100,"right")}
        </div>
        {"".join(prows)}
        <div style="margin-top:auto;display:flex;align-items:center;gap:12px;padding:12px 18px;border-top:1px solid {T['line']};font-size:12.5px;color:{T['muted']}">
          แสดง 1–9 จาก 1,284
          <div style="flex:1"></div>
          <span style="display:flex;align-items:center;gap:6px">แถวต่อหน้า {select("25",78)}</span>
          <div style="display:flex;gap:6px">
            <span style="width:30px;height:30px;border:1px solid {T['line']};border-radius:8px;display:flex;align-items:center;justify-content:center;background:{T['surface']};transform:rotate(180deg)">{ic("chevron",14)}</span>
            <span style="width:30px;height:30px;border:1px solid {T['line']};border-radius:8px;display:flex;align-items:center;justify-content:center;background:{T['surface']}">{ic("chevron",14)}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>'''
write("Contacts.dc.html", contacts)

# ── Contact detail ──────────────────────────────────────────────────────
STEPS = [("New Lead", True), ("Hot Lead", True), ("Payment", False), ("Customer", False)]
steps_html = []
for i,(name,done) in enumerate(STEPS):
    active = i == 1
    bgc = T['accent'] if done else T['surface']
    fg = "#fff" if done else T['muted']
    bd = T['accent'] if done else T['line']
    ring = f'box-shadow:0 0 0 4px {T["card"]};' if active else ''
    steps_html.append(
      f'<div style="display:flex;align-items:center;gap:10px">'
      f'<div style="display:flex;align-items:center;gap:9px">'
      f'<span style="width:26px;height:26px;border-radius:50%;background:{bgc};border:1px solid {bd};color:{fg};{ring}'
      f'display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600">{ic("check",13,2.2,"#fff") if done else i+1}</span>'
      f'<span style="font-size:13px;font-weight:{"600" if active else "400"};color:{T["ink"] if done else T["muted"]}">{name}</span></div>'
      + (f'<span style="width:42px;height:1px;background:{T["line"]}"></span>' if i < len(STEPS)-1 else "") + '</div>')

TIMELINE = [
  ("bolt","09:18","ระบบอัตโนมัติ","ส่งข้อความทักทายภาษาไทย และมอบหมายให้ Ploy แบบวนรอบ"),
  ("tag","09:19","ระบบอัตโนมัติ","เพิ่มแท็ก villa, pricing จากคำในข้อความ"),
  ("inbox","09:22","Ploy","ตอบกลับเรื่องราคา Marina Golden Bay 12.9 ล้าน"),
  ("check","09:21","Ploy","เปลี่ยน stage จาก New Lead เป็น Hot Lead"),
  ("link","09:21","ระบบ","ส่ง webhook contact.lifecycle_changed ให้ Agency Care · 200 OK"),
  ("note","09:25","Ploy","บันทึกโน้ต: นัดเข้าชมโครงการเสาร์ 10:00 น. ขอรถรับส่งจากพัทยาใต้"),
]
tl = []
for i,(icon_name, time, who, text) in enumerate(TIMELINE):
    tl.append(
      f'<div style="display:flex;gap:12px">'
      f'<div style="display:flex;flex-direction:column;align-items:center;flex:none">'
      f'<span style="width:30px;height:30px;border-radius:50%;background:{T["card"]};color:{T["accentLight"]};display:flex;align-items:center;justify-content:center">{ic(icon_name,15)}</span>'
      + (f'<span style="flex:1;width:1px;background:{T["line"]};margin:4px 0"></span>' if i < len(TIMELINE)-1 else "")
      + f'</div>'
      f'<div style="padding-bottom:16px;display:flex;flex-direction:column;gap:3px">'
      f'<div style="display:flex;align-items:baseline;gap:8px"><span style="font-weight:600;font-size:13px">{who}</span>'
      f'<span style="font-size:11.5px;color:{T["muted"]}">{time} น.</span></div>'
      f'<span style="font-size:13px;color:{T["muted"]};line-height:1.65">{text}</span></div></div>')

def infoline(k, v):
    return (f'<div style="display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px dashed {T["line"]};font-size:13px">'
            f'<span style="color:{T["muted"]}">{k}</span><span style="text-align:right">{v}</span></div>')

detail = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  {rail("users")}
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar('<span style="color:' + T['muted'] + '">Contacts ›</span> คุณสมชาย ส.', btn("เปิดบทสนทนา","ghost","inbox") + btn("แก้ไข","primary","plus"))}
    <div style="padding:8px 24px 16px;display:flex;flex-direction:column;gap:14px;overflow:hidden">
      <div style="display:flex;align-items:center;gap:18px;background:{T['surface']};border:1px solid {T['line']};border-radius:16px;padding:14px 18px">
        {avatar("สม",52)}
        <div style="display:flex;flex-direction:column;gap:5px">
          <span style="font-family:{DISPLAY};font-weight:600;font-size:19px">คุณสมชาย ส.</span>
          <div style="display:flex;align-items:center;gap:10px">{chan("LINE")}{pill("Hot Lead","accent")}{pill("เจ้าของ: Ploy","muted")}</div>
        </div>
        <div style="flex:1"></div>
        <div style="display:flex;align-items:center;gap:0">{"".join(steps_html)}</div>
      </div>

      <div style="display:flex;gap:18px;align-items:flex-start">
        <div style="width:344px;flex:none;display:flex;flex-direction:column;gap:16px">
          {card(label("ข้อมูลผู้ติดต่อ") + '<div style="height:10px"></div>' + "".join(infoline(k,v) for k,v in [("ภาษา","ไทย"),("โทรศัพท์","08X-XXX-4412"),("อีเมล","—"),("สร้างเมื่อ","12 ก.ย. 2569"),("ติดต่อล่าสุด","วันนี้ 09:24 น.")]))}
          {card(label("ข้อมูลเพิ่มเติม") + '<div style="height:10px"></div>' + "".join(infoline(k,v) for k,v in [("โครงการที่สนใจ","Marina Golden Bay"),("งบประมาณ","12–15 ล้าน"),("สัญชาติ","ไทย"),("วัตถุประสงค์","อยู่เอง")]))}
          {card(label("ช่องทางที่ผูกไว้") + '<div style="height:12px"></div>'
            + f'<div style="display:flex;flex-direction:column;gap:10px">'
            + f'<div style="display:flex;align-items:center;gap:10px;font-size:13px">{dot(CHAN["LINE"])}LINE<span style="flex:1"></span><span style="font-family:{MONO};font-size:11.5px;color:{T["muted"]}">U4a9…c71</span></div>'
            + f'<div style="display:flex;align-items:center;gap:10px;font-size:13px">{dot(CHAN["WhatsApp"])}WhatsApp<span style="flex:1"></span><span style="font-family:{MONO};font-size:11.5px;color:{T["muted"]}">+66 8X XXX 4412</span></div>'
            + f'<div style="display:flex;align-items:center;gap:7px;font-size:12.5px;color:{T["accentLight"]}">{ic("plus",14)}รวมผู้ติดต่อซ้ำ</div></div>')}
        </div>

        <div style="flex:1;min-width:0">
          {card(
            '<div style="display:flex;align-items:center;gap:14px">' + label("ไทม์ไลน์") +
            f'<div style="flex:1"></div><span style="font-size:12.5px;color:{T["muted"]}">ทั้งหมด</span>'
            f'<span style="font-size:12.5px;color:{T["muted"]}">ข้อความ</span>'
            f'<span style="font-size:12.5px;color:{T["accentLight"]};font-weight:600">กิจกรรมระบบ</span></div>'
            + '<div style="height:16px"></div>' + "".join(tl), 20)}
        </div>

        <div style="width:300px;flex:none;display:flex;flex-direction:column;gap:16px">
          {card(label("แท็ก") + '<div style="height:12px"></div><div style="display:flex;flex-wrap:wrap;gap:6px">'
                + "".join(pill(t,"accent") for t in ["villa","pricing","seaview"])
                + f'<span style="display:inline-flex;align-items:center;gap:4px;height:22px;padding:0 9px;border-radius:999px;border:1px dashed {T["line"]};color:{T["muted"]};font-size:11.5px">{ic("plus",12)}เพิ่ม</span></div>')}
          {card(label("บทสนทนา") + '<div style="height:12px"></div>'
                + f'<div style="display:flex;flex-direction:column;gap:12px">'
                + f'<div style="display:flex;align-items:center;gap:9px;font-size:13px">{dot(CHAN["LINE"])}<span style="flex:1">LINE · เปิดอยู่</span><span style="color:{T["muted"]};font-size:11.5px">09:24</span></div>'
                + f'<div style="display:flex;align-items:center;gap:9px;font-size:13px">{dot(CHAN["WhatsApp"])}<span style="flex:1">WhatsApp · ปิดแล้ว</span><span style="color:{T["muted"]};font-size:11.5px">8 ก.ย.</span></div></div>')}
          {card(f'<div style="display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600">{ic("link",15,1.6,T["accentLight"])}Agency Care</div>'
                + f'<div style="height:8px"></div><div style="font-size:12px;color:{T["muted"]};line-height:1.7">ซิงก์ล่าสุด 09:21 น. · webhook ตอบ 200<br>รหัสอ้างอิง <span style="font-family:{MONO}">AC-1284</span></div>'
                + '<div style="height:10px"></div><a href="#" style="font-size:12.5px">เปิดใน Agency Care</a>')}
        </div>
      </div>
    </div>
  </div>
</div>'''
write("ContactDetail.dc.html", detail)
