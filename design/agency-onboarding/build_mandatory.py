from tokens import *
from build_perm_audit import std_page

# รายการบังคับ — แยกว่าอันไหนใช้กฎเดิมของระบบ อันไหนเป็นของ onboarding เอง
# (src, label, cond)  cond=None คือบังคับเสมอ
REUSE, NEW = "reuse", "new"
GROUPS = [
 ("A. Agency Profile", "ใช้กฎเดิม missingAgencyProfile() ฝั่ง API ไม่สร้างรายการใหม่", [
   (REUSE,"Agency Name", None),
   (REUSE,"Owner / Contact Person", None),
   (REUSE,"Phone", None),
   (REUSE,"Email", None),
   (REUSE,"Office Type", None),
   (REUSE,"Province", None),
   (REUSE,"Zone", None),
   (REUSE,"Agency Photo — อย่างน้อย 1 รูป", None),
   (REUSE,"Number of Sales Agents", None),
   (REUSE,"Existing Project / Relationship", None),
   (REUSE,"Last Sale Date", "เฉพาะเมื่อไม่ได้ติ๊ก New Agency"),
   (REUSE,"Last Units Sold", "เฉพาะเมื่อไม่ได้ติ๊ก New Agency"),
   (REUSE,"Total Units Sold", "เฉพาะเมื่อไม่ได้ติ๊ก New Agency"),
   (REUSE,"Address", "เฉพาะ Physical Office และ Booth"),
   (REUSE,"Google Map Link (lat/lng)", "เฉพาะ Physical Office และ Booth"),
   (REUSE,"รายละเอียดความสัมพันธ์อย่างน้อย 1 รายการ", "เฉพาะเมื่อเลือก Have"),
 ]),
 ("B. Documents &amp; Bank", "ของใหม่ — onboarding เป็นตัวบังคับให้เอกสารครบและถูกยืนยัน", [
   (NEW,"Company Registration / DBD — Verified", None),
   (NEW,"Owner ID / Passport — Verified", None),
   (NEW,"Bank Book — Verified", None),
   (NEW,"Commission Authorization — Verified", None),
   (NEW,"Bank Account Type + เลขบัญชี", None),
   (NEW,"Authorization Letter", "เฉพาะเมื่อเลือก Owner Personal Account"),
 ]),
 ("C. Communication (Phase 2)", "", [
   (NEW,"สร้าง LINE Group แล้ว", None),
   (NEW,"Agency Owner และทีมขายอยู่ในกลุ่ม", None),
   (NEW,"ทีมภายในอยู่ในกลุ่มครบ", None),
   (NEW,"Assign Seller แล้ว", None),
   (NEW,"Seller อ่าน Agency Background แล้ว", None),
 ]),
 ("D. System Entry (Phase 3)", "", [
   (NEW,"บันทึก Venio Agency ID", None),
   (NEW,"ลงทะเบียน agency ใน Venio", None),
   (NEW,"อัปโหลดเอกสารเข้า Venio", None),
   (NEW,"กรอก Initial Agency Report ครบ", None),
 ]),
 ("E. First Communication (Phase 4)", "", [
   (NEW,"ส่ง Welcome Communication", None),
   (NEW,"ส่ง Marketing Package", None),
   (NEW,"บันทึกวันที่ส่งและช่องทาง", None),
 ]),
 ("F. Agreement (Phase 5)", "", [
   (NEW,"ส่งเอกสารให้ Agency Support", None),
   (NEW,"เตรียมสัญญาแล้ว", None),
   (NEW,"ประชุมครั้งที่สองเสร็จ", None),
   (NEW,"เซ็นสัญญาและอัปโหลดแล้ว", None),
   (NEW,"ตกลง Sales Plan และ Monthly Goal", None),
 ]),
 ("G. Post-Onboarding (Phase 6)", "", [
   (NEW,"ส่ง Sales Materials ให้แล้ว", None),
   (NEW,"บันทึก Agency Visit ครั้งแรก", None),
 ]),
]

base = sum(1 for _, _, items in GROUPS for _, _, c in items if c is None)
cond = sum(1 for _, _, items in GROUPS for _, _, c in items if c is not None)

def grp(title, note, items):
    rows = ""
    for src, label, c in items:
        if src == REUSE:
            tag = f'<span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">กฎเดิม</span>'
        else:
            tag = f'<span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">ของ onboarding</span>'
        condc = (f'<span class="cap" style="color:{WARNING}">{c}</span>' if c
                 else '<span class="cap mut">บังคับเสมอ</span>')
        rows += (f'<tr><td style="font-weight:600">{label}</td>'
                 f'<td style="width:150px">{tag}</td><td style="width:330px">{condc}</td></tr>')
    n_all = len(items)
    n_cond = sum(1 for _, _, c in items if c is not None)
    cnt = f"{n_all - n_cond} เสมอ" + (f" + {n_cond} มีเงื่อนไข" if n_cond else "")
    note_html = f'<p class="cap mut" style="margin:0">{note}</p>' if note else ""
    return f"""<div class="card pad col" style="gap:12px">
  <div class="row" style="gap:12px"><h3 class="sec grow">{title}</h3>
    <span class="cap mut">{cnt}</span></div>
  {note_html}
  <table><tbody>{rows}</tbody></table>
</div>"""

summary = f"""<div class="card pad col" style="gap:16px">
  <div class="row" style="gap:28px;align-items:center;flex-wrap:wrap">
    <div class="col" style="gap:2px">
      <div style="font-size:32px;font-weight:700;letter-spacing:-0.02em;color:{TXT}">{base}</div>
      <div class="cap mut">รายการที่บังคับเสมอ</div></div>
    <div style="width:1px;height:46px;background:{DIVIDER}"></div>
    <div class="col" style="gap:2px">
      <div style="font-size:32px;font-weight:700;letter-spacing:-0.02em;color:{WARNING}">{cond}</div>
      <div class="cap mut">รายการที่ขึ้นกับเงื่อนไข</div></div>
    <div style="width:1px;height:46px;background:{DIVIDER}"></div>
    <div class="col grow" style="gap:4px">
      <div class="b2" style="font-weight:700">ตัวหารไม่คงที่ — คำนวณต่อเอเจนซี่</div>
      <div class="cap mut">อย่างน้อย {base} · มากสุด {base + cond} ข้อ
        แล้วแต่ว่าเป็น New Agency, ประเภทออฟฟิศ, ความสัมพันธ์เดิม และประเภทบัญชีธนาคาร</div>
    </div>
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px">
    <div class="col" style="gap:7px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 16px">
      <span class="b2" style="font-weight:700">ABC Property Pattaya</span>
      <span class="cap mut">มีประวัติขาย · Physical Office · มีความสัมพันธ์เดิม · บัญชีส่วนตัวเจ้าของ</span>
      <span class="b2" style="color:{PRIMARY_L};font-weight:700">รวม {base + cond} ข้อ</span>
    </div>
    <div class="col" style="gap:7px;background:{SURFACE};border:1px solid {DIVIDER};
         border-radius:16px;padding:14px 16px">
      <span class="b2" style="font-weight:700">Siam Estate Bangkok</span>
      <span class="cap mut">New Agency · Non-Physical Office · ไม่มีความสัมพันธ์เดิม · บัญชีบริษัท</span>
      <span class="b2" style="color:{PRIMARY_L};font-weight:700">รวม {base} ข้อ</span>
    </div>
  </div>
</div>"""

waiting = f"""<div class="card pad col" style="gap:16px">
  <h3 class="sec">สถานะ Waiting Agency — ระบบตั้งให้เอง</h3>

  <div class="row" style="gap:12px;flex-wrap:wrap;align-items:center">
    <span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">In Progress</span>
    <span class="cap mut">เงียบครบ</span>
    <span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">3 วัน</span>
    <span style="color:{TXT3}">→</span>
    <span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">Waiting Agency</span>
    <span class="cap mut">เงียบต่ออีก</span>
    <span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">4 วัน</span>
    <span style="color:{TXT3}">→</span>
    <span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">Need Attention</span>
  </div>

  <div style="height:1px;background:{DIVIDER}"></div>

  <div class="row" style="gap:16px;align-items:flex-start">
    <div class="col grow" style="gap:10px;background:rgba(34,197,94,.07);
         border:1px solid rgba(34,197,94,.30);border-radius:16px;padding:14px 16px">
      <div class="row" style="gap:9px">{icon(I_CHECK,16,SUCCESS)}
        <span class="b2" style="font-weight:700;color:{SUCCESS}">เหตุการณ์ที่รีเซ็ตตัวนับ</span></div>
      <div class="col" style="gap:6px">
        <span class="b2" style="color:{TXT2}">· อัปโหลดเอกสารเข้า onboarding</span>
        <span class="b2" style="color:{TXT2}">· ติ๊กหรือปลดติ๊ก checklist ข้อใดก็ได้</span>
      </div>
      <span class="cap mut">มีแค่สองอย่างนี้ — เพราะเป็นร่องรอยที่พิสูจน์ได้ว่างานเดินจริง</span>
    </div>
    <div class="col grow" style="gap:10px;background:rgba(107,114,128,.10);
         border:1px solid {DIVIDER};border-radius:16px;padding:14px 16px">
      <div class="row" style="gap:9px">{icon(I_CIRCLE,16,TXT3)}
        <span class="b2" style="font-weight:700;color:{TXT2}">ไม่รีเซ็ตตัวนับ</span></div>
      <div class="col" style="gap:6px">
        <span class="b2 mut">· ข้อความในกลุ่ม LINE</span>
        <span class="b2 mut">· เปิดดูหน้า onboarding</span>
        <span class="b2 mut">· แก้โน้ตภายในหรือแก้ข้อความในฟอร์ม</span>
        <span class="b2 mut">· เปลี่ยนผู้ดูแล</span>
      </div>
      <span class="cap mut">คุยกันเฉย ๆ ไม่นับว่าคืบหน้า</span>
    </div>
  </div>

  <div class="col" style="gap:9px">
    <div class="row" style="gap:10px"><span style="color:{SECOND};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">นับจากเหตุการณ์ล่าสุดในสองอย่างนั้น
        ไม่ได้นับจากวันที่สร้าง onboarding</span></div>
    <div class="row" style="gap:10px"><span style="color:{SECOND};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">เอเจนซี่ส่งเอกสารมาแล้วทีมเราอัปเข้าระบบ
        หรือติ๊ก checklist ให้ — ตัวนับรีเซ็ตและสถานะกลับเป็น In Progress เอง</span></div>
    <div class="row" style="gap:10px"><span style="color:{SECOND};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">เอกสารที่ถูก Reject ก็นับว่าเป็นการอัปโหลด —
        ตัวนับรีเซ็ต เพราะมีคนทำงานกับมันจริง</span></div>
    <div class="row" style="gap:10px"><span style="color:{SECOND};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">ผู้ใช้ตั้ง Waiting Agency เองไม่ได้ —
        เป็นสถานะที่ระบบคำนวณ เหมือนกับเปอร์เซ็นต์ความคืบหน้า</span></div>
    <div class="row" style="gap:10px"><span style="color:{SECOND};font-weight:700">·</span>
      <span class="b2" style="color:{TXT2}">Completed แล้วหยุดนับ —
        เอเจนซี่ย้ายไปอยู่ภายใต้กติกา Relationship Maintenance แทน</span></div>
  </div>

  <div class="row" style="gap:9px;background:rgba(59,130,246,.10);
       border:1px solid rgba(59,130,246,.30);border-radius:14px;padding:11px 14px">
    {icon(I_CLOCK,16,PRIMARY_L)}
    <span class="b2" style="color:{PRIMARY_L};font-weight:600">
      สองเหตุการณ์นี้อยู่ใน audit log อยู่แล้ว — ตัวนับอ่านจาก log ได้เลย ไม่ต้องเก็บฟิลด์เวลาเพิ่ม</span>
  </div>
</div>"""

body = summary + waiting + "".join(grp(t, n, i) for t, n, i in GROUPS)
open("Mandatory.dc.html","w").write(
    std_page("Onboarding — Mandatory Items &amp; Status Rules",
             f"อะไรบ้างที่ต้องครบก่อนกด Complete Onboarding · {base} ข้อเสมอ + {cond} ข้อตามเงื่อนไข",
             body, 1240, 2360))
print(f"Mandatory.dc.html — base {base} · conditional {cond} · max {base+cond}")
