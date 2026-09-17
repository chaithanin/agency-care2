from shell import *

# ═══════ 5. Promotion Selling Quota ═══════
UNITS = [("A101","Available","2BR · 68 sqm","฿ 6,480,000","—"),
         ("A102","Reserved","2BR · 68 sqm","฿ 6,480,000","K. May · 15 Sep"),
         ("A103","Sold","1BR · 42 sqm","฿ 4,200,000","K. John · 12 Sep"),
         ("A104","Available","1BR · 42 sqm","฿ 4,200,000","—"),
         ("A105","Sold","2BR · 71 sqm","฿ 6,900,000","K. May · 08 Sep")]
u_rows = "".join(
    f'<tr><td style="width:40px"><div style="width:17px;height:17px;border-radius:5px;'
    f'border:1.5px solid {DIVIDER}"></div></td>'
    f'<td style="font-weight:700">{c}</td><td>{flow_chip(s)}</td>'
    f'<td class="mut">{t}</td><td>{p}</td><td class="mut" style="font-size:13px">{by}</td></tr>'
    for c, s, t, p, by in UNITS)

counts = f"""<div class="row" style="gap:28px;flex-wrap:wrap;background:{SURFACE};
     border:1px solid {DIVIDER};border-radius:16px;padding:16px 20px">
  {big("20","Total Units")}{big("8","Available",SUCCESS)}{big("4","Reserved",WARNING)}
  {big("8","Sold",TXT3)}
  <div style="width:1px;height:44px;background:{DIVIDER}"></div>
  {big("8","Remaining",PRIMARY_L)}
</div>"""

move = f"""<div class="col" style="gap:12px;background:rgba(251,191,36,.08);
     border:1px solid rgba(251,191,36,.35);border-radius:16px;padding:15px 17px">
  <div class="row" style="gap:10px">{icon(I_WARN,16,WARNING)}
    <span class="b2" style="font-weight:700;color:{WARNING}">ย้ายยูนิตข้ามโปรโมชัน</span></div>
  <div class="row" style="gap:14px;align-items:center;flex-wrap:wrap">
    <span class="b2" style="font-weight:700">A101</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT2}">Campaign A</span>
    <span style="color:{TXT3}">→</span>
    <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">Campaign B</span>
  </div>
  <div class="col" style="gap:7px">
    <div class="row" style="gap:10px">{icon(I_CHECK,15,SUCCESS)}
      <span class="b2" style="color:{TXT2}">ยูนิตยัง Available — ย้ายได้</span></div>
    <div class="row" style="gap:10px">{icon(I_WARN,15,ERROR)}
      <span class="b2" style="color:{TXT2}">ถ้าเป็น Reserved หรือ Sold แล้ว
        <b>ห้ามย้าย</b> เพราะลูกค้าตกลงเงื่อนไขของโปรโมชันเดิมไปแล้ว</span></div>
    <div class="row" style="gap:10px">{icon(I_WARN,15,ERROR)}
      <span class="b2" style="color:{TXT2}">ยูนิตหนึ่งอยู่ได้ทีละโปรโมชันเดียวในช่วงเวลาเดียวกัน</span></div>
  </div>
  <p class="cap mut" style="margin:0">ทุกการย้ายเก็บประวัติ ใครย้าย เมื่อไหร่ จากแคมเปญไหนไปไหน
    และตอนนั้นยูนิตสถานะอะไร</p>
</div>"""

body = f"""{note_box("ok","ตาราง Unit มีอยู่แล้ว พร้อมฟิลด์ status = available / reserved / booked / sold "
          "และผูกกับ project อยู่แล้ว — ใช้ของเดิม ห้ามสร้างตารางยูนิตใหม่")}
{panel("Summer Campaign — Selling Quota", flow_chip("Approved"), counts)}
{panel("ยูนิตในโควตา", f'<button class="btn sm out">+ เพิ่มยูนิต</button>',
  f'<table><thead><tr><th style="width:40px"></th><th style="width:110px">Unit</th>'
  f'<th style="width:150px">สถานะ</th><th style="width:190px">แบบห้อง</th>'
  f'<th style="width:180px">ราคา</th><th>จองโดย</th></tr></thead><tbody>{u_rows}</tbody></table>',
  note="สถานะดึงจากตาราง Unit ตรง ๆ ไม่ใช่เก็บซ้ำในโปรโมชัน — ขายแล้วตัวเลขเปลี่ยนเอง")}
{move}
{note_box("error","ห้ามเก็บโควตาเป็นตัวเลข เช่น 20 Units — ต้องผูกกับยูนิตจริงเป็นรายตัว "
          "ไม่งั้นตัวเลข Available กับ Sold จะไม่มีทางตรงกับความจริง")}"""

open("Quota.dc.html","w").write(
    sheet("5 · Promotion Selling Quota — ผูกกับยูนิตจริง",
          "โควตาคือรายชื่อยูนิต ไม่ใช่ตัวเลข", body, 1360, 1200, badge="ต่อยอดของเดิม"))
print("Quota.dc.html")

# ═══════ 6. Internal / External Message ═══════
internal = f"""<div class="col" style="gap:12px;border:1px solid rgba(239,68,68,.35);
     background:rgba(239,68,68,.05);border-radius:16px;padding:16px 18px">
  <div class="row" style="gap:10px">{flow_chip("Internal")}
    <span class="cap mut">เห็นเฉพาะ Sales · Agency Support · Management</span></div>
  <div class="fld" style="min-height:130px;color:{TXT2}">ต้นทุนห้องชุดนี้อยู่ที่ 5.2 ล้าน
ต่อรองได้ถึง 5.6 ล้านโดยไม่ต้องขออนุมัติ
ต่ำกว่านั้นให้ส่ง Manager

คู่แข่งที่ Jomtien เพิ่งลดราคาลง 8% เดือนนี้
ลูกค้าที่มาจาก ABC Property ให้ค่าคอม 3.5% ไม่ใช่ 3%</div>
  {note_box("error","ข้อความนี้ห้ามหลุดออกนอกบริษัทเด็ดขาด — "
            "ไม่มีปุ่มส่งในการ์ดนี้ และ API ต้องไม่มี endpoint ที่ส่งข้อความ internal ออกช่องทางภายนอก")}
</div>"""

external = f"""<div class="col" style="gap:12px;border:1px solid rgba(34,197,94,.35);
     background:rgba(34,197,94,.05);border-radius:16px;padding:16px 18px">
  <div class="row" style="gap:10px">{flow_chip("External")}
    <span class="cap mut">ส่งให้ลูกค้า เอเจนซี่ และโซเชียลได้</span></div>
  <div class="fld" style="min-height:130px;color:{TXT2}">Marina Residence — Summer Campaign

เริ่มต้น 4.2 ล้านบาท
ฟรีค่าโอน ฟรีเฟอร์นิเจอร์ครบชุด
จำนวนจำกัด 20 ยูนิต ถึง 31 ตุลาคม 2569

สอบถามเพิ่มเติม 038-123-456</div>
  <div class="row" style="gap:10px;flex-wrap:wrap">
    <button class="btn sm out">Send via LINE</button>
    <button class="btn sm out">Send via Email</button>
    <button class="btn sm out">Publish to Social</button>
    <span class="grow"></span>
    <button class="btn sm">Preview ก่อนส่ง</button>
  </div>
</div>"""

preview = f"""<div class="col" style="gap:12px;width:330px;flex-shrink:0;background:{SURFACE};
     border:1px solid {DIVIDER};border-radius:18px;padding:16px 18px">
  <h4 class="sec">External Message Preview</h4>
  <div class="col" style="gap:8px;background:#FFFFFF;border-radius:4px 16px 16px 16px;padding:13px 15px">
    <span style="font-size:13px;font-weight:700;color:#0F172A">Marina Residence — Summer Campaign</span>
    <span style="font-size:12px;line-height:1.55;color:#334155">เริ่มต้น 4.2 ล้านบาท<br>
      ฟรีค่าโอน ฟรีเฟอร์นิเจอร์ครบชุด<br>จำนวนจำกัด 20 ยูนิต ถึง 31 ต.ค. 2569</span>
    <div style="border-top:1px solid #E2E8F0;padding-top:8px;text-align:center;
         font-size:12px;font-weight:600;color:#2563EB">สอบถามเพิ่มเติม</div>
  </div>
  <div class="col" style="gap:6px">
    <div class="row"><span class="cap mut grow">ช่องทาง</span>
      <span class="cap" style="color:{TXT2}">LINE</span></div>
    <div class="row"><span class="cap mut grow">ผู้รับ</span>
      <span class="cap" style="color:{TXT2}">Agencies · 291 คน</span></div>
  </div>
  <div class="row" style="gap:10px">
    <button class="btn sm out">Edit</button>
    <button class="btn sm">Send</button>
  </div>
</div>"""

body2 = f"""{panel("Summer Campaign — ข้อความสองชุด", "",
  f'<div class="row" style="gap:20px;align-items:flex-start">'
  f'<div class="col grow" style="gap:16px">{internal}{external}</div>{preview}</div>')}
{panel("สิทธิ์ที่ต้องแยกให้ขาด", "",
  f'<table><thead><tr><th>การกระทำ</th><th style="width:210px">Internal Message</th>'
  f'<th style="width:210px">External Message</th></tr></thead><tbody>'
  f'<tr><td>เขียนและแก้</td><td>Sales · Agency Support · Manager · Admin</td>'
  f'<td>Marketing · Manager · Admin</td></tr>'
  f'<tr><td>อ่าน</td><td>เฉพาะพนักงานบริษัท</td><td>ทุกคนที่เข้าระบบได้</td></tr>'
  f'<tr><td>ส่งออกช่องทางภายนอก</td>'
  f'<td style="color:{ERROR};font-weight:700">ไม่มีสิทธิ์ — ไม่มี endpoint</td>'
  f'<td>Manager · Admin</td></tr>'
  f'<tr><td>คัดลอกข้าม</td>'
  f'<td colspan="2" style="color:{ERROR};font-weight:600">'
  f'ห้ามมีปุ่ม "คัดลอกจาก Internal ไป External"</td></tr>'
  f'</tbody></table>',
  note="กันข้อมูลภายในหลุดออกไปหาลูกค้าและเอเจนซี่")}"""

open("Message.dc.html","w").write(
    sheet("6 · Internal / External Message",
          "หนึ่งโปรโมชันมีข้อความสองชุดที่แยกสิทธิ์กันเด็ดขาด",
          body2, 1420, 1240, badge="ของใหม่"))
print("Message.dc.html")
