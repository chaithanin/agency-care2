from shell import *

# ═══════ 2. Purchase Request ═══════
trigger = f"""<div class="row" style="gap:12px;flex-wrap:wrap;align-items:center">
  <span class="b2" style="color:{TXT2}">สต็อกลดลง</span><span style="color:{TXT3}">→</span>
  <span class="chip" style="color:{ERROR};background:rgba(239,68,68,.15)">ถึง Minimum Stock</span>
  <span style="color:{TXT3}">→</span>
  <span class="b2" style="color:{TXT2}">แจ้งเตือน</span><span style="color:{TXT3}">→</span>
  <span class="b2" style="color:{TXT2}">สร้าง Purchase Request</span>
</div>"""

PR_ITEMS = [("Marina Brochure","500 ชิ้น","฿ 12,500","Main Warehouse"),
            ("Marina Gift Set","200 ชุด","฿ 36,000","Marketing Warehouse")]
pr_rows = "".join(
    f'<tr><td style="font-weight:600">{n}</td><td>{q}</td><td>{b}</td><td class="mut">{w}</td></tr>'
    for n, q, b, w in PR_ITEMS)

pr = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("PR Number","PR-2026-0182", w=190)}
    {field("Project","Marina Residence", w=220)}
    {field("ผู้ขอ","K. Pim", w=170)}
    {field("ผู้อนุมัติ","K. Warun (Manager)")}
  </div>
  <table><thead><tr><th>รายการ</th><th style="width:150px">จำนวน</th>
    <th style="width:150px">งบประมาณ</th><th style="width:210px">เข้าที่เก็บ</th>
  </tr></thead><tbody>{pr_rows}</tbody></table>
  <div class="row" style="gap:10px">
    <span class="grow"></span>
    <span class="cap mut">รวม</span>
    <span class="b2" style="font-weight:700">฿ 48,500</span>
  </div>
</div>"""

reject = f"""<div class="col" style="gap:12px;background:rgba(239,68,68,.07);
     border:1px solid rgba(239,68,68,.32);border-radius:16px;padding:15px 17px">
  <div class="row" style="gap:10px">{icon(I_WARN,16,ERROR)}
    <span class="b2" style="font-weight:700;color:{ERROR}">กรณีไม่อนุมัติ</span></div>
  {flow_line(["Pending Approval","Rejected"], active="Rejected")}
  <div class="col" style="gap:0">
    <p class="lbl">เหตุผล (บังคับกรอก)</p>
    <div class="fld" style="color:{TXT2}">งบเดือนนี้เต็มแล้ว ขอเลื่อนไปต้นเดือนหน้า
      และลดจำนวน brochure เหลือ 300</div>
  </div>
  <p class="cap mut" style="margin:0">ผู้ขอแก้แล้วส่งใหม่ได้ — PR เดิมไม่ถูกลบ
    เก็บประวัติทุกครั้งที่ส่งว่าใครตีกลับเพราะอะไร</p>
</div>"""

body = f"""{note_box("ok","ตาราง PurchaseRequest มีอยู่แล้วในระบบ พร้อม status ครบ "
          "draft · submitted · waiting_approval · approved · purchasing · ordered · received · completed "
          "รวมถึง PrItem, PrComment, PrActivity, PrAttachment และ approverId — "
          "งานนี้คือเชื่อมเข้ากับสต็อกและการแจ้งเตือน ไม่ใช่สร้างใหม่")}
{panel("จุดเริ่ม", "", trigger)}
{panel("PR-2026-0182", flow_chip("Pending Approval"), pr)}
{panel("สถานะ", "", flow_line(
   ["Draft","Pending Approval","Approved","Ordered","Received","Completed"], active="Pending Approval"),
  note="Manager เป็นผู้อนุมัติ — ตรวจสิทธิ์ฝั่ง server ไม่ใช่แค่ซ่อนปุ่ม")}
{reject}
{note_box("warn","ตอนกด Received ต้องเพิ่มสต็อกเข้าที่เก็บที่ระบุไว้ในแต่ละรายการ "
          "และสร้างธุรกรรม Receive ให้อัตโนมัติ ห้ามให้คนมาแก้ยอดเอง")}"""

open("Purchase.dc.html","w").write(
    sheet("2 · Inventory Purchase Request",
          "สต็อกถึงขั้นต่ำ → ขอซื้อ → Manager อนุมัติ → รับของ → เพิ่มสต็อก",
          body, 1360, 1300, badge="ต่อยอดของเดิม"))
print("Purchase.dc.html")

# ═══════ 4. Distribution ═══════
dist = f"""<div class="row" style="gap:20px;align-items:flex-start">
  <div class="col grow" style="gap:14px">
    <div class="row" style="gap:14px">
      {field("Agency","ABC Property", required=True)}
      {field("Project","Marina Residence", required=True)}
    </div>
    <div class="row" style="gap:14px">
      {field("Item","Marina Brochure", required=True)}
      {field("จำนวน","100", w=130, required=True)}
      {field("ตัดจากที่เก็บ","Marina Showroom", w=210, required=True)}
    </div>
    <div class="row" style="gap:14px">
      {field("วันที่","17 Sep 2026", w=180)}
      {field("ผู้ส่งมอบ","John", w=180)}
      {field("ผู้รับ","ABC Property")}
    </div>
    <div class="col" style="gap:0">
      <p class="lbl">หมายเหตุ</p>
      <div class="fld" style="color:{TXT2}">Delivered to agency office</div>
    </div>
  </div>
  <div class="col" style="gap:12px;width:310px;flex-shrink:0">
    <p class="lbl">หลักฐานการรับของ<span style="color:{ERROR}">&nbsp;*</span></p>
    <div class="row" style="gap:10px;flex-wrap:wrap">
      <div class="col" style="gap:5px;align-items:center">
        <div style="width:92px;height:92px;border-radius:12px;background:{SURFACE};
             border:1px solid {DIVIDER}"></div>
        <span class="cap mut" style="font-size:11px">delivery-receipt.jpg</span>
      </div>
      <div class="col" style="gap:5px;align-items:center">
        <div style="width:92px;height:92px;border-radius:12px;background:{SURFACE};
             border:1px solid {DIVIDER};display:grid;place-items:center">
          <span class="cap mut">PDF</span></div>
        <span class="cap mut" style="font-size:11px">signed-form.pdf</span>
      </div>
      <div style="width:92px;height:92px;border-radius:12px;border:1.5px dashed {DIVIDER};
           display:grid;place-items:center">{icon(I_PLUS,18,TXT3)}</div>
    </div>
    <p class="cap mut" style="margin:0">รับรูปภาพ · PDF · ใบรับของ · เอกสารเซ็นรับ ·
      รูปถ่ายตอนส่งของ</p>
  </div>
</div>"""

body2 = f"""{panel("บันทึกการแจกของ", f'<button class="btn sm">บันทึก</button>', dist)}
{note_box("error","ต้องมีหลักฐานอย่างน้อย 1 ไฟล์ถึงจะบันทึกได้ — "
          "ตรวจฝั่ง server ด้วย ไม่ใช่แค่ disable ปุ่ม")}
{note_box("warn","ไฟล์หลักฐานเป็นเอกสารที่ต้องใช้ตรวจสอบย้อนหลัง "
          "ต้องลงถังส่วนตัวผ่าน savePrivate() ไม่ใช่ถัง public — "
          "และต้องมี GCS_PRIVATE_BUCKET ตอน deploy ไม่งั้นไฟล์จะหายเหมือนที่เคยเกิดกับ Photo Evidence")}
{panel("ผลที่เกิดขึ้นเมื่อบันทึก", "",
  f'<div class="col" style="gap:9px">'
  f'<div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">1</span>'
  f'<span class="b2" style="color:{TXT2}">ตัดสต็อก Marina Showroom ลง 100 → เหลือ 100</span></div>'
  f'<div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">2</span>'
  f'<span class="b2" style="color:{TXT2}">สร้างธุรกรรมประเภท Distribution พร้อมลิงก์ไปที่ Agency</span></div>'
  f'<div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">3</span>'
  f'<span class="b2" style="color:{TXT2}">เก็บไฟล์หลักฐานผูกกับธุรกรรมนั้น ลบไม่ได้</span></div>'
  f'<div class="row" style="gap:10px"><span style="color:{PRIMARY_L};font-weight:700">4</span>'
  f'<span class="b2" style="color:{TXT2}">ถ้าสต็อกตกต่ำกว่าขั้นต่ำ ส่งแจ้งเตือนทันที</span></div></div>')}"""

open("Distribution.dc.html","w").write(
    sheet("4 · Brochure Distribution — ต้องมีหลักฐาน",
          "แจกของให้เอเจนซี่แล้วต้องแนบหลักฐานการรับ เก็บไว้ตรวจย้อนหลัง",
          body2, 1360, 1080, badge="ของใหม่"))
print("Distribution.dc.html")
