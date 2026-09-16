from shell import *

# ══════════ 7. STEP 3 — PREVIEW ══════════
phone = f"""<div class="col" style="gap:0;width:330px;flex-shrink:0;background:#1B2430;
     border:1px solid {DIVIDER};border-radius:20px;padding:18px 16px;gap:12px">
  <div class="row" style="gap:9px">
    <div style="width:30px;height:30px;border-radius:999px;background:{SUCCESS};
         display:grid;place-items:center;font-size:11px;font-weight:800;color:#0F172A">GTG</div>
    <span class="b2" style="font-weight:600">Global Top Group</span>
  </div>
  <div class="col" style="gap:8px;background:#FFFFFF;border-radius:4px 16px 16px 16px;padding:12px 14px">
    <div style="width:100%;height:110px;border-radius:8px;background:#E2E8F0"></div>
    <span style="font-size:13px;font-weight:700;color:#0F172A">MARINA SEPTEMBER UPDATE</span>
    <span style="font-size:12px;line-height:1.5;color:#334155">อัปเดตความคืบหน้า Marina Golden Bay
      เดือนกันยายน — งานโครงสร้างชั้น 24 เสร็จแล้ว พร้อมราคาและยูนิตคงเหลือล่าสุด</span>
    <div style="border-top:1px solid #E2E8F0;padding-top:9px;text-align:center;
         font-size:12px;font-weight:600;color:#2563EB">ดู Price List</div>
  </div>
</div>"""

def sum_row(label, n, color=None, muted=False):
    c = color or (TXT3 if muted else TXT)
    return (f'<div class="row" style="padding:7px 0"><span class="b2 grow" '
            f'style="color:{TXT3 if muted else TXT2}">{label}</span>'
            f'<span class="b2" style="font-weight:700;color:{c}">{n}</span></div>')

summary = f"""<div class="col grow" style="gap:14px">
  <div class="col" style="gap:0;background:{SURFACE};border:1px solid {DIVIDER};
       border-radius:16px;padding:16px 18px">
    <div class="row" style="padding-bottom:9px;border-bottom:1px solid {DIVIDER}">
      <span class="b2 grow" style="font-weight:700">Total recipients</span>
      <span style="font-size:20px;font-weight:700;color:{PRIMARY_L}">284</span>
    </div>
    {sum_row("Agency contacts", "284")}
  </div>

  <div class="col" style="gap:0;background:rgba(251,191,36,.07);
       border:1px solid rgba(251,191,36,.35);border-radius:16px;padding:16px 18px">
    <div class="row" style="padding-bottom:9px;border-bottom:1px solid {DIVIDER}">
      <span class="b2 grow" style="font-weight:700;color:{WARNING}">ถูกตัดออก</span>
      <span class="b2" style="font-weight:700;color:{WARNING}">36</span>
    </div>
    {sum_row("Blocked — บล็อก OA แล้ว", "12", muted=True)}
    {sum_row("Inactive — เลิกติดตามแล้ว", "3", muted=True)}
    {sum_row("Unclassified — ยังไม่จัดประเภท", "21", muted=True)}
    <p class="cap mut" style="margin:9px 0 0">ตัดออกตั้งแต่ตอนนับ ไม่ได้ส่งแล้วค่อยล้มเหลว
      จำนวนที่เห็นคือจำนวนที่จะได้รับจริง</p>
  </div>

  <div class="row" style="gap:10px;background:rgba(59,130,246,.10);
       border:1px solid rgba(59,130,246,.30);border-radius:14px;padding:11px 14px">
    {icon(I_CLOCK,16,PRIMARY_L)}
    <span class="b2" style="color:{PRIMARY_L};font-weight:600">
      โควตาคงเหลือ 7,312 ข้อความ — พอสำหรับการส่งครั้งนี้</span>
  </div>
</div>"""

body = f"""{steps(3)}
{panel("Preview", f'<span class="chip" style="color:{SECOND};background:rgba(167,139,250,.16)">Agencies</span>',
  f'<div class="row" style="gap:28px;align-items:flex-start">{phone}'
  f'<div style="width:1px;align-self:stretch;background:{DIVIDER}"></div>{summary}</div>')}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Next — Send</button>
</div>"""
open("Step3Preview.dc.html","w").write(
    page_shell("OVERVIEW", body, 1240, 1000, title="New Announcement",
               subtitle="ขั้นที่ 3 จาก 4 — ตรวจก่อนส่ง"))
print("Step3Preview.dc.html")

# ══════════ 8. STEP 4 — SEND / SCHEDULE ══════════
def opt_card(title, note, on=False, body=""):
    dot = (f'<div style="width:19px;height:19px;border-radius:999px;border:2px solid {PRIMARY};'
           f'display:grid;place-items:center"><div style="width:9px;height:9px;border-radius:999px;'
           f'background:{PRIMARY}"></div></div>' if on else
           f'<div style="width:19px;height:19px;border-radius:999px;border:2px solid {DIVIDER}"></div>')
    bd = f"1px solid {PRIMARY}" if on else f"1px solid {DIVIDER}"
    bg = "rgba(59,130,246,.08)" if on else SURFACE
    return f"""<div class="col" style="gap:12px;border:{bd};background:{bg};border-radius:16px;padding:15px 17px">
  <div class="row" style="gap:12px;align-items:center">{dot}
    <div class="col grow" style="gap:2px">
      <span class="b2" style="font-weight:700">{title}</span>
      <span class="cap mut">{note}</span></div></div>
  {body}
</div>"""

sched_fields = f"""<div class="row" style="gap:14px">
  {field("Date","18 Sep 2026", w=190)}
  {field("Time","09:00", w=140)}
  {field("Timezone","Asia/Bangkok (GMT+7)", w=230)}
  <div class="col grow"></div>
</div>"""

body2 = f"""{steps(4)}
<div class="card pad row" style="gap:16px;flex-wrap:wrap">
  <div class="col" style="gap:2px"><span class="cap mut">Audience</span>
    <span class="b2" style="font-weight:700">Agencies</span></div>
  <div style="width:1px;height:34px;background:{DIVIDER}"></div>
  <div class="col" style="gap:2px"><span class="cap mut">Recipients</span>
    <span class="b2" style="font-weight:700">284</span></div>
  <div style="width:1px;height:34px;background:{DIVIDER}"></div>
  <div class="col" style="gap:2px"><span class="cap mut">Title</span>
    <span class="b2" style="font-weight:700">MARINA SEPTEMBER UPDATE</span></div>
  <span class="grow"></span>
  <button class="btn sm out">แก้ไข</button>
</div>
{panel("Send or Schedule", "",
  f'<div class="col" style="gap:12px">'
  f'{opt_card("Send Now","ส่งทันทีที่กดยืนยัน", on=True)}'
  f'{opt_card("Schedule","ตั้งเวลาส่งล่วงหน้า", body=sched_fields)}</div>')}
<div class="card pad row" style="gap:12px;border-color:rgba(34,197,94,.35);background:rgba(34,197,94,.07)">
  {icon(I_CHECK,18,SUCCESS)}
  <span class="b2 grow" style="color:{SUCCESS}">ระบบจะบันทึกรายชื่อผู้รับทั้ง 284 คนไว้ตอนส่ง —
    ย้อนดูได้เสมอว่าครั้งนี้ส่งหาใครบ้าง แม้บทบาทของเขาจะเปลี่ยนไปในอนาคต</span>
</div>
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn out">Save as draft</button>
  <button class="btn">Send to 284 recipients</button>
</div>"""
open("Step4Send.dc.html","w").write(
    page_shell("OVERVIEW", body2, 1240, 940, title="New Announcement",
               subtitle="ขั้นที่ 4 จาก 4 — ส่งหรือตั้งเวลา"))
print("Step4Send.dc.html")
