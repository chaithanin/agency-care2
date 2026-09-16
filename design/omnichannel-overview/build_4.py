from shell import *

# ══════ 4. NEEDS YOUR ATTENTION ══════
ITEMS = [
 ("394","Unclassified contacts","มีคน follow เข้ามาแล้วยังไม่ได้ระบุว่าเป็นใคร",
  "ไปที่ LINE Contacts › Unclassified", ST_WARN),
 ("42","New leads without assigned seller","lead เข้ามาแล้วยังไม่มีคนดูแล",
  "ไปที่ Lead Registration › Unassigned", ST_CRIT),
 ("18","Conversations waiting > 30 min","ลูกค้าถามแล้วยังไม่มีใครตอบ",
  "ไปที่ Conversations › Overdue", ST_CRIT),
 ("12","Failed broadcasts","ส่งไม่สำเร็จ ส่วนใหญ่เพราะผู้รับบล็อก OA",
  "ไปที่ Broadcast › Send History", ST_SERIOUS),
 ("34","Agencies inactive > 30 days","เอเจนซี่ที่เงียบหายไปเกินหนึ่งเดือน",
  "ไปที่ Agency List › Inactive", ST_SERIOUS),
 ("21","Leads waiting for follow-up","เลยวันนัดติดตามแล้วยังไม่ได้ทำ",
  "ไปที่ Follow-up Board", ST_WARN),
 ("8","Customers requested viewing but no appointment","ขอดูห้องแล้วยังไม่มีนัด",
  "ไปที่ Appointments › Requested", ST_CRIT),
]
rows = ""
for n, title, why, action, color in ITEMS:
    rows += f"""<div class="row" style="gap:16px;align-items:center;padding:13px 0;
     border-bottom:1px solid {DIVIDER};cursor:pointer">
  {icon(I_WARN,18,color)}
  <span style="font-size:20px;font-weight:700;width:52px;flex-shrink:0;color:{color}">{n}</span>
  <div class="col grow" style="gap:2px">
    <span class="b2" style="font-weight:600">{title}</span>
    <span class="cap mut">{why}</span>
  </div>
  <span class="cap" style="color:{TXT2}">{action}</span>
  {icon(I_EXT,15,TXT3)}
</div>"""

attention = f"""<div class="card pad col" style="gap:12px;border-color:rgba(250,178,25,.35)">
  <div class="row" style="gap:12px">
    <h3 class="sec grow" style="color:{ST_WARN}">⚠ Needs Your Attention</h3>
    <span class="cap mut">7 เรื่อง · กดแต่ละแถวเพื่อไปทำงานต่อได้ทันที</span>
  </div>
  <div class="col" style="gap:0">{rows}</div>
  <p class="cap mut" style="margin:0">นี่คือจุดที่ทำให้หน้านี้เป็นเครื่องมือบริหาร ไม่ใช่แค่รายงาน —
    ทุกแถวพาไปยังหน้าที่แก้ปัญหานั้นได้จริง ไม่ใช่แค่บอกตัวเลข</p>
</div>"""

# ตัวอย่าง drill-down
drill = f"""<div class="card pad col" style="gap:12px">
  <div class="row" style="gap:12px">
    <h3 class="sec grow">ตัวอย่าง drill-down — กด "18 Conversations waiting &gt; 30 min"</h3>
  </div>
  <table>
    <thead><tr><th>Contact</th><th style="width:130px">Channel</th>
      <th style="width:150px">Assigned</th><th style="width:130px">Waiting</th>
      <th style="width:190px">Last message</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:600">Somchai P.</td>
        <td><span class="row" style="gap:8px"><span style="width:10px;height:10px;border-radius:3px;
          background:{S_BLUE}"></span>LINE</span></td>
        <td class="mut">K. May</td>
        <td style="color:{ST_CRIT};font-weight:700">1h 42m</td>
        <td class="mut" style="font-size:13px">"ห้องนี้ยังว่างไหมครับ"</td></tr>
      <tr><td style="font-weight:600">Anna K.</td>
        <td><span class="row" style="gap:8px"><span style="width:10px;height:10px;border-radius:3px;
          background:{S_ORANGE}"></span>Facebook</span></td>
        <td class="mut">— ยังไม่มีคนดูแล</td>
        <td style="color:{ST_CRIT};font-weight:700">58m</td>
        <td class="mut" style="font-size:13px">"ขอ price list Marina ครับ"</td></tr>
      <tr><td style="font-weight:600">Nadia R.</td>
        <td><span class="row" style="gap:8px"><span style="width:10px;height:10px;border-radius:3px;
          background:{S_AQUA}"></span>Instagram</span></td>
        <td class="mut">K. John</td>
        <td style="color:{ST_SERIOUS};font-weight:700">36m</td>
        <td class="mut" style="font-size:13px">"Is the pool view available?"</td></tr>
    </tbody>
  </table>
  <div class="row" style="gap:10px">
    <button class="btn sm out">Assign seller</button>
    <button class="btn sm">Open conversation</button>
  </div>
</div>"""

open("Attention.dc.html","w").write(
    dash("Omnichannel Overview — Needs Your Attention",
         "ตอนนี้มีอะไรที่ต้องเข้าไปจัดการทันที",
         attention + drill, 1400, 1100))
print("Attention.dc.html")
