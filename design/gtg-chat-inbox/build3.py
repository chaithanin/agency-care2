# -*- coding: utf-8 -*-
exec(open('gen.py', encoding='utf-8').read())

# ── Automations ─────────────────────────────────────────────────────────
RULES = [
  ("ทักทายข้อความแรกตามภาษา","ข้อความแรกของบทสนทนา","เปิด","1,284 ครั้ง",True),
  ("มอบหมายเซลส์แบบวนรอบ","บทสนทนาใหม่","เปิด","1,284 ครั้ง",False),
  ("แท็กจากคีย์เวิร์ด","ทุกข้อความเข้า","เปิด","3,902 ครั้ง",False),
  ("เตือน admin เมื่อไม่มีคนตอบ 15 นาที","ตั้งเวลา","เปิด","34 ครั้ง",False),
  ("ปิดเคสอัตโนมัติหลังเงียบ 7 วัน","ตั้งเวลา","ปิดอยู่","—",False),
]
rule_rows = []
for name, trig, status, runs, active in RULES:
    on = status == "เปิด"
    knob = (f'<span style="width:30px;height:17px;border-radius:999px;flex:none;background:{T["accent"] if on else T["line"]};'
            f'display:flex;align-items:center;justify-content:{"flex-end" if on else "flex-start"};padding:2px">'
            f'<span style="width:13px;height:13px;border-radius:50%;background:#fff"></span></span>')
    rule_rows.append(
      f'<div style="display:flex;gap:11px;align-items:flex-start;padding:13px 16px;border-bottom:1px solid {T["line"]};'
      f'background:{T["inb"] if active else T["surface"]};border-left:3px solid {T["accent"] if active else "transparent"}">'
      f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:5px">'
      f'<span style="font-weight:600;font-size:13.5px;line-height:1.45">{name}</span>'
      f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:11.5px;color:{T["muted"]}">'
      f'{ic("bolt",13)}{trig}<span style="color:{T["line"]}">·</span>{runs}</div></div>{knob}</div>')

def node(kind, title, body, tone="accent"):
    kinds = {"trigger":("TRIGGER","bolt"), "condition":("CONDITION","filter"), "action":("ACTION","send")}
    tag, icon_name = kinds[kind]
    return (f'<div style="background:{T["surface"]};border:1px solid {T["line"]};border-radius:12px;padding:14px 16px;'
            f'display:flex;flex-direction:column;gap:10px;width:452px">'
            f'<div style="display:flex;align-items:center;gap:10px">'
            f'<span style="width:28px;height:28px;border-radius:8px;background:{T["card"]};color:{T["accentLight"]};'
            f'display:flex;align-items:center;justify-content:center">{ic(icon_name,15)}</span>'
            f'<span style="font-family:{DISPLAY};font-size:10.5px;font-weight:600;letter-spacing:.1em;color:{T["muted"]}">{tag}</span>'
            f'<span style="font-weight:600;font-size:14px">{title}</span>'
            f'<div style="flex:1"></div><span style="color:{T["muted"]}">{ic("dots",16)}</span></div>'
            f'{body}</div>')

def connector():
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;width:452px">'
            f'<span style="width:1px;height:11px;background:{T["line"]}"></span>'
            f'<span style="width:22px;height:22px;border-radius:50%;border:1px dashed {T["line"]};color:{T["muted"]};'
            f'background:{T["surface"]};display:flex;align-items:center;justify-content:center">{ic("plus",12)}</span>'
            f'<span style="width:1px;height:11px;background:{T["line"]}"></span></div>')

trigger_body = (f'<div style="display:flex;align-items:center;gap:10px">{select("บทสนทนาใหม่",210)}{select("ทุกช่องทาง",160)}</div>'
                f'<span style="font-size:12.5px;color:{T["muted"]};line-height:1.6">ทำงานเมื่อมีข้อความแรกของบทสนทนาเข้ามา — ข้อความถัดไปในบทสนทนาเดิมจะไม่ทำซ้ำ</span>')
cond_body = (f'<div style="display:flex;align-items:center;gap:10px">{select("ภาษาที่ตรวจพบ",170)}{select("เท่ากับ",110)}{select("ไทย",110)}</div>'
             f'<div style="display:flex;align-items:center;gap:8px;font-size:12.5px;color:{T["accentLight"]}">{ic("plus",14)}เพิ่มเงื่อนไข</div>')
act1_body = (f'<div style="border:1px solid {T["line"]};border-radius:9px;padding:11px 13px;font-size:13px;line-height:1.7;background:{T["bg"]}">'
             f'สวัสดีค่ะ ขอบคุณที่ติดต่อ GTG ทีมงานกำลังตรวจสอบและจะตอบกลับโดยเร็วที่สุดค่ะ</div>'
             f'<div style="display:flex;align-items:center;gap:10px;font-size:12px;color:{T["muted"]}">'
             f'ข้อความตามภาษา: <span style="color:{T["ink"]}">ไทย</span> · อังกฤษ · รัสเซีย</div>')
act2_body = (f'<div style="display:flex;align-items:center;gap:10px">{select("มอบหมายแบบวนรอบ",196)}{select("ทีม Sales (3 คน)",178)}</div>'
             f'<span style="font-size:12px;color:{T["muted"]}">เลือกคนที่ถือเคสเปิดอยู่น้อยที่สุด</span>')

RUNS = [
  ("09:18","คุณสมชาย ส.","ส่งข้อความทักทาย (ไทย)","สำเร็จ"),
  ("09:18","คุณสมชาย ส.","มอบหมายให้ Ploy","สำเร็จ"),
  ("09:11","Anna Petrova","ส่งข้อความทักทาย (อังกฤษ)","สำเร็จ"),
  ("08:57","Иван Волков","มอบหมายแบบวนรอบ","ไม่มีเซลส์ว่าง"),
]
run_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid {T["line"]};font-size:12.5px">'
  f'<span style="width:42px;flex:none;color:{T["muted"]}">{t}</span>'
  f'<span style="width:104px;flex:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{who}</span>'
  f'<span style="flex:1;color:{T["muted"]}">{what}</span>'
  f'{pill(st, "muted" if st=="สำเร็จ" else "warn")}</div>'
  for t, who, what, st in RUNS)

automations = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  {rail("bolt")}
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar("Automations", btn("ประวัติการทำงาน","ghost","clock") + btn("สร้างกฎใหม่","primary","plus"))}
    <div style="flex:1;display:flex;min-height:0">
      <div style="width:310px;flex:none;border-right:1px solid {T['line']};background:{T['surface']};display:flex;flex-direction:column">
        <div style="padding:12px 16px;border-bottom:1px solid {T['line']};background:{T['bg']};display:flex;align-items:center;gap:10px">
          {search_box("ค้นหากฎ", 200)}<span style="font-size:12px;color:{T['muted']}">5 กฎ</span>
        </div>
        {"".join(rule_rows)}
        <div style="padding:14px 16px;font-size:12px;color:{T['muted']};line-height:1.7">กฎทำงานจากบนลงล่าง<br>ลากเพื่อสลับลำดับได้</div>
      </div>

      <div style="flex:1;min-width:0;overflow:hidden;display:flex">
        <div style="flex:1;padding:14px 18px;display:flex;flex-direction:column;gap:0;align-items:center;overflow:hidden">
          <div style="width:452px;display:flex;align-items:center;gap:10px;margin-bottom:12px">
            <span style="font-family:{DISPLAY};font-weight:600;font-size:16px">ทักทายข้อความแรกตามภาษา</span>
            {pill("เปิดใช้งาน","accent")}
            <div style="flex:1"></div>{btn("ทดสอบกฎ","ghost","bolt",30)}{btn("บันทึก","primary",None,30)}
          </div>
          {node("trigger","เมื่อมีบทสนทนาใหม่", trigger_body)}
          {connector()}
          {node("condition","ถ้าภาษาของข้อความคือไทย", cond_body)}
          {connector()}
          {node("action","ส่งข้อความทักทาย", act1_body)}
          {connector()}
          {node("action","มอบหมายเซลส์", act2_body)}
        </div>
        <div style="width:330px;flex:none;border-left:1px solid {T['line']};background:{T['surface']};padding:18px;display:flex;flex-direction:column;gap:16px">
          {label("การทำงานล่าสุด")}
          <div style="display:flex;flex-direction:column">{run_rows}</div>
          <div style="border:1px solid {T['line']};border-radius:10px;padding:13px;background:{T['bg']};display:flex;flex-direction:column;gap:7px">
            <span style="font-size:12.5px;font-weight:600">ผลกับคิวงาน 7 วันล่าสุด</span>
            <span style="font-size:12px;color:{T['muted']};line-height:1.7">เคสที่ไม่มีคนรับลดจาก <span style="color:{T['ink']}">77</span> เหลือ <span style="color:{T['accentLight']};font-weight:600">3</span> หลังเปิดกฎมอบหมายอัตโนมัติ</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>'''
write("Automations.dc.html", automations)
