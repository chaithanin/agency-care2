from shell import *

# ═══════ 1. Construction Schedule Update ═══════
setting = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Project","Marina Residence", required=True)}
    {field("Update Frequency","Every 15 days", w=210)}
    {field("Deadline Time","17:00", w=150)}
  </div>
  <div class="row" style="gap:14px">
    {field("ผู้รับผิดชอบ","K. Somchai (Project Manager)", required=True)}
    {field("ผู้อนุมัติ","K. Warun (Manager)", required=True)}
  </div>
  <div class="row" style="gap:14px">
    {field("เตือนก่อนถึงกำหนด","3 วัน · 1 วัน", w=280)}
    {field("เตือนเมื่อเกินกำหนด","ทุกวันจนกว่าจะส่ง", w=280)}
    <div class="col grow"></div>
  </div>
  {note_box("info","วันที่กำหนดเองได้ทั้งหมด ไม่บังคับว่าต้องเป็นวันที่ 1 และ 16 — "
            "ระบบสร้างรอบถัดไปตามความถี่ที่ตั้งไว้ แต่แก้วันของแต่ละรอบทีหลังได้")}
</div>"""

ROUNDS = [("Round 1","05 Sep 2026","Approved","K. Somchai","06 Sep 14:20"),
          ("Round 2","20 Sep 2026","Due","K. Somchai","—"),
          ("Round 3","05 Oct 2026","Upcoming","K. Somchai","—"),
          ("Round 4","20 Oct 2026","Upcoming","K. Somchai","—")]
rows = ""
for name, due, st, who, sub in ROUNDS:
    rows += (f'<tr><td style="font-weight:600">{name}</td><td>{due}</td>'
             f'<td>{flow_chip(st)}</td><td class="mut">{who}</td>'
             f'<td class="mut" style="font-size:13px">{sub}</td>'
             f'<td><button class="btn sm out">เปิดดู</button></td></tr>')

overdue = f"""<tr style="background:rgba(239,68,68,.06)">
  <td style="font-weight:600">Round 2 — Love It Residence</td><td>14 Sep 2026</td>
  <td>{flow_chip("Overdue")}</td><td class="mut">K. Nira</td>
  <td class="mut" style="font-size:13px">เลยกำหนด 3 วัน</td>
  <td><button class="btn sm">ตามงาน</button></td></tr>"""

body = f"""{panel("ตั้งค่ารอบอัปเดต", f'<button class="btn sm out">+ เพิ่มโครงการ</button>', setting)}
{panel("รอบของ Marina Residence", flow_line(
   ["Upcoming","Due","Submitted","Under Review","Approved"], active="Due"),
  f'<table><thead><tr><th style="width:170px">รอบ</th><th style="width:150px">กำหนดส่ง</th>'
  f'<th style="width:150px">สถานะ</th><th style="width:190px">ผู้รับผิดชอบ</th>'
  f'<th style="width:180px">ส่งเมื่อ</th><th style="width:110px"></th></tr></thead>'
  f'<tbody>{rows}{overdue}</tbody></table>',
  note="Overdue เป็นสถานะที่ระบบคำนวณเอง ไม่ใช่ให้คนตั้ง — เลยเวลา deadline แล้วยังไม่ส่ง")}
{note_box("warn","เกินกำหนดแล้วยังต้องส่งได้ ห้ามล็อกไม่ให้ส่ง — "
          "แต่ต้องบันทึกว่าส่งช้ากี่วัน เพื่อให้รายงานย้อนหลังตรงความจริง")}"""

open("Construction.dc.html","w").write(
    sheet("1 · Construction Schedule Update",
          "กำหนดรอบเองได้ ไม่ผูกกับวันที่ 1 และ 16", body, 1360, 1080, badge="ของใหม่ทั้งหมด"))
print("Construction.dc.html")

# ═══════ 2. Inventory — Multi-Location Stock ═══════
LOCS = [("Main Warehouse","Warehouse",500),("Marina Showroom","Showroom",100),
        ("Sales Office","Sales Office",50)]
loc_rows = "".join(
    f'<tr><td style="font-weight:600">{n}</td><td class="mut">{t}</td>'
    f'<td style="text-align:right;font-weight:700">{q}</td>'
    f'<td><button class="btn sm out">โอนย้าย</button></td></tr>' for n, t, q in LOCS)

item = f"""<div class="row" style="gap:20px;align-items:flex-start">
  <div class="col grow" style="gap:12px">
    <div class="row" style="gap:14px">
      {field("Item","Marina Brochure", w=260)}
      {field("Project","Marina Residence", w=230)}
      {field("Category","Printed", w=160)}
      {field("Minimum Stock","150", w=150)}
    </div>
    <table><thead><tr><th>ที่เก็บ</th><th style="width:160px">ประเภท</th>
      <th style="width:120px;text-align:right">คงเหลือ</th><th style="width:120px"></th>
    </tr></thead><tbody>{loc_rows}
      <tr style="border-top:2px solid {DIVIDER}"><td style="font-weight:700">รวมทุกที่</td><td></td>
        <td style="text-align:right;font-weight:700;font-size:16px">650</td><td></td></tr>
    </tbody></table>
  </div>
  <div class="col" style="gap:10px;width:300px;flex-shrink:0;background:{SURFACE};
       border:1px solid {DIVIDER};border-radius:16px;padding:16px 18px">
    <h4 class="sec">โอนย้ายสต็อก</h4>
    {field("จาก","Main Warehouse  ·  500")}
    <div style="text-align:center;color:{TXT3}">↓</div>
    {field("ไป","Marina Showroom  ·  100")}
    {field("จำนวน","100", w=120)}
    {field("เหตุผล","เติมของหน้าโชว์รูม")}
    <button class="btn sm">บันทึกการโอน</button>
    <p class="cap mut" style="margin:0">หลังโอน: Main 400 · Showroom 200</p>
  </div>
</div>"""

TX = [("17 Sep 14:20","Transfer","Main Warehouse → Marina Showroom","−100 / +100","K. Pim"),
      ("17 Sep 09:05","Distribution","Marina Showroom → ABC Property","−100","K. John"),
      ("16 Sep 16:40","Receive","Main Warehouse","+500","K. Pim"),
      ("15 Sep 11:12","Adjustment","Sales Office","−5  ของเสียหาย","K. May"),
      ("14 Sep 10:00","Return","ABC Property → Sales Office","+20","K. John")]
tx_rows = "".join(
    f'<tr><td class="mut" style="font-size:13px">{d}</td>'
    f'<td><span class="chip" style="border:1px solid {DIVIDER};color:{TXT2}">{k}</span></td>'
    f'<td style="color:{TXT2}">{w}</td><td style="font-weight:600">{q}</td>'
    f'<td class="mut">{by}</td></tr>' for d, k, w, q, by in TX)

body2 = f"""{note_box("error","ของเดิม PosmItem เก็บ stockQty ตัวเดียว = สต็อกรวม "
           "ต้องเปลี่ยนเป็นแยกตามที่เก็บ และห้ามลบ stockQty เดิมทิ้ง ให้คำนวณจากผลรวมแทน")}
{panel("Marina Brochure", flow_chip("Available"), item)}
{panel("ประวัติทุกธุรกรรม", f'<span class="cap mut">Receive · Issue · Transfer · Adjustment · Distribution · Return</span>',
  f'<table><thead><tr><th style="width:150px">เวลา</th><th style="width:140px">ประเภท</th>'
  f'<th>ที่เก็บ</th><th style="width:170px">จำนวน</th><th style="width:130px">ผู้ทำ</th>'
  f'</tr></thead><tbody>{tx_rows}</tbody></table>',
  note="ทุกการเปลี่ยนแปลงต้องมีแถวในนี้ ห้ามแก้ยอดตรง ๆ โดยไม่มีธุรกรรม")}"""

open("Inventory.dc.html","w").write(
    sheet("3 · Inventory — แยกสต็อกตามที่เก็บ",
          "Project → Location → Warehouse → Item · ของเดียวกันอยู่ได้หลายที่",
          body2, 1420, 1240, badge="เปลี่ยนโครงสร้างเดิม"))
print("Inventory.dc.html")
