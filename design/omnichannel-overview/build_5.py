from shell import *

RIO  = f'<span class="chip" style="color:{S_AQUA};background:rgba(25,158,112,.16)">respond.io</span>'
AC   = f'<span class="chip" style="color:{S_BLUE};background:rgba(57,135,229,.16)">Agency Care</span>'
JOIN = f'<span class="chip" style="color:{S_ORANGE};background:rgba(217,89,38,.16)">ต้อง join</span>'

ROWS = [
 ("Total / New Contacts", RIO, "นับจากตาราง mirror ของ contact", "ทุก 15 นาที"),
 ("Audience — Customer / Agency / Sales / Unclassified", JOIN,
  "type มาจาก line_contact_roles ของ Agency Care · ตัวคนมาจาก respond.io", "ทุก 15 นาที"),
 ("Active Conversations", RIO, "contact ที่ status = open", "ทุก 5 นาที"),
 ("Conversations by channel", RIO, "group ตาม source ของ contact channel", "ทุก 15 นาที"),
 ("Avg. First Response / Avg. Response", RIO,
  "คำนวณจาก timestamp ของข้อความ — <b>ต้อง precompute</b> เรียกสดไม่ได้", "ทุกชั่วโมง"),
 ("Resolution Rate / Avg. Resolution", RIO, "จากเวลาที่ conversation เปลี่ยนเป็น close", "ทุกชั่วโมง"),
 ("SLA — within 5 / 15 / over 30 min", RIO, "แจกแจงจาก first response ที่ precompute ไว้", "ทุกชั่วโมง"),
 ("New Leads", AC, "CustomerLead ที่สร้างในช่วงเวลาที่เลือก", "ทันที"),
 ("Lead Journey 7 ขั้น", AC, "จาก dealStages / reportStatus ของ CustomerLead", "ทันที"),
 ("Project Interest", AC, "จาก interestedProjects ของ CustomerLead", "ทันที"),
 ("Reservations / Closed", AC, "จาก Booking และ Deal ของระบบเดิม", "ทันที"),
 ("Customer vs Agency", JOIN, "นับคนจาก respond.io แยกด้วย role ของ Agency Care", "ทุก 15 นาที"),
 ("Broadcast — Sent / Delivered / Read", AC, "จากตาราง Broadcast และ BroadcastRecipient", "ทันที"),
 ("Team Performance", JOIN,
  "assignee มาจาก respond.io · แม็ปเป็นพนักงานด้วย employee.lineUserId", "ทุกชั่วโมง"),
 ("Needs Your Attention", JOIN, "รวมเงื่อนไขจากทั้งสองฝั่ง", "ทุก 5 นาที"),
]
rows = "".join(
    f'<tr><td style="font-weight:600">{m}</td><td style="width:130px">{src}</td>'
    f'<td style="color:{TXT2}">{how}</td><td class="mut" style="width:120px;font-size:13px">{fr}</td></tr>'
    for m, src, how, fr in ROWS)

table = f"""<div class="card pad col" style="gap:14px">
  <div class="row" style="gap:12px"><h3 class="sec grow">ตัวเลขแต่ละตัวมาจากไหน</h3>
    <div class="row" style="gap:8px">{RIO}{AC}{JOIN}</div></div>
  <table><thead><tr><th>Metric</th><th>แหล่งข้อมูล</th><th>คิดจากอะไร</th>
    <th>ความถี่ที่อัปเดต</th></tr></thead><tbody>{rows}</tbody></table>
</div>"""

arch = f"""<div class="card pad col" style="gap:14px">
  <h3 class="sec">สถาปัตยกรรม — ห้ามเรียก respond.io สดตอนเปิดหน้า</h3>
  <div class="row" style="gap:14px;align-items:center;flex-wrap:wrap">
    <div class="col" style="gap:4px;background:{SURFACE};border:1px solid {S_AQUA};
         border-radius:16px;padding:14px 18px;min-width:180px">
      <span class="b2" style="font-weight:700;color:{S_AQUA}">respond.io API</span>
      <span class="cap mut">contact · message · channel</span></div>
    <span style="color:{TXT3};font-size:20px">→</span>
    <div class="col" style="gap:4px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 18px;min-width:180px">
      <span class="b2" style="font-weight:700">ตาราง mirror</span>
      <span class="cap mut">respondio_* ในฐานข้อมูลเรา</span></div>
    <span style="color:{TXT3};font-size:20px">→</span>
    <div class="col" style="gap:4px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 18px;min-width:180px">
      <span class="b2" style="font-weight:700">ตารางสรุปรายวัน</span>
      <span class="cap mut">omnichannel_daily_stats</span></div>
    <span style="color:{TXT3};font-size:20px">→</span>
    <div class="col" style="gap:4px;background:{SURFACE};border:1px solid {S_BLUE};
         border-radius:16px;padding:14px 18px;min-width:180px">
      <span class="b2" style="font-weight:700;color:{S_BLUE}">หน้า Dashboard</span>
      <span class="cap mut">อ่านจากตารางสรุปอย่างเดียว</span></div>
  </div>
  <div class="col" style="gap:9px">
    <div class="row" style="gap:10px"><span style="color:{ST_CRIT};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}"><b>ห้ามเรียก respond.io ตอนผู้ใช้เปิดหน้า</b> —
        Avg. First Response ต้องไล่ข้อความของ contact หมื่นกว่าคน เรียกสดจะช้าและชน rate limit ทันที</span></div>
    <div class="row" style="gap:10px"><span style="color:{ST_CRIT};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">คำนวณล่วงหน้าเก็บเป็นตารางสรุปรายวัน
        แล้วหน้า dashboard query จากตารางนั้น เปิดหน้าต้องเสร็จภายใน 1 วินาที</span></div>
    <div class="row" style="gap:10px"><span style="color:{ST_WARN};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">ทุกตัวเลขต้องบอกเวลาที่ซิงก์ล่าสุด —
        ผู้บริหารต้องรู้ว่ากำลังดูข้อมูลสดหรือข้อมูลเมื่อชั่วโมงที่แล้ว</span></div>
    <div class="row" style="gap:10px"><span style="color:{ST_WARN};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">ถ้าซิงก์ล้มเหลว ให้แสดงข้อมูลเก่าพร้อมป้ายเตือน
        <b>ห้ามแสดงศูนย์</b> — ศูนย์ที่ไม่ใช่ศูนย์จริงทำให้ตัดสินใจผิด</span></div>
  </div>
</div>"""

gaps = f"""<div class="card pad col" style="gap:12px;border-color:rgba(236,131,90,.35);
     background:rgba(236,131,90,.06)">
  <h3 class="sec" style="color:{ST_SERIOUS}">ช่องว่างที่ต้องรู้ก่อนเริ่ม</h3>
  <div class="col" style="gap:9px">
    <div class="row" style="gap:10px"><span style="color:{ST_SERIOUS};font-weight:700">1</span>
      <span class="b2" style="color:{TXT2}"><b>respond.io ไม่รู้จัก Lead Journey และ Project</b> —
        ข้อมูลพวกนี้อยู่ใน Agency Care เท่านั้น จะเชื่อมได้ต้องจับคู่ contact กับ CustomerLead ก่อน
        ซึ่งเป็นงานของโมดูล LINE Contacts</span></div>
    <div class="row" style="gap:10px"><span style="color:{ST_SERIOUS};font-weight:700">2</span>
      <span class="b2" style="color:{TXT2}"><b>contact ที่ยังไม่จับคู่ จะไม่ปรากฏใน funnel</b> —
        ต้องแสดงจำนวนที่หลุดออกไปให้เห็น ไม่ใช่ซ่อนเงียบ ๆ</span></div>
    <div class="row" style="gap:10px"><span style="color:{ST_SERIOUS};font-weight:700">3</span>
      <span class="b2" style="color:{TXT2}"><b>Facebook / Instagram / WhatsApp / Website</b>
        มาถึงเราผ่าน respond.io เท่านั้น ยังไม่มีการเชื่อมตรง —
        ถ้าช่องทางไหนยังไม่ได้ต่อเข้า respond.io จะไม่มีข้อมูลในหน้านี้เลย</span></div>
    <div class="row" style="gap:10px"><span style="color:{ST_SERIOUS};font-weight:700">4</span>
      <span class="b2" style="color:{TXT2}"><b>ข้อมูลย้อนหลังมีเท่าที่ซิงก์มา</b> —
        วันแรกที่เปิดใช้ กราฟแนวโน้มจะว่าง ต้องบอกผู้ใช้ตรง ๆ ไม่ใช่ปล่อยให้เห็นกราฟแบน ๆ
        แล้วคิดว่าธุรกิจเงียบ</span></div>
  </div>
</div>"""

open("DataSources.dc.html","w").write(
    dash("Omnichannel Overview — Data Sources",
         "ตัวเลขแต่ละตัวมาจากไหน คำนวณยังไง และอัปเดตบ่อยแค่ไหน",
         table + arch + gaps, 1400, 1500))
print("DataSources.dc.html")
