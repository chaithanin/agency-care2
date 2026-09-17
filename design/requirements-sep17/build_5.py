from shell import *

# ═══════ 8. Notification ═══════
GROUPS = [
 ("Lead", [("New Lead",1,1,1),("Lead Assigned",1,1,1),("Lead Reassigned",1,1,0)]),
 ("Task", [("Task Assigned",1,1,1),("Task Due Soon",1,1,0),("Task Overdue",1,1,1),
           ("Task Completed",1,0,0)]),
 ("Inventory", [("Minimum Stock",1,1,1),("Out of Stock",1,1,1),
                ("Purchase Request Submitted",1,1,1),("Purchase Request Approved",1,1,1),
                ("Purchase Request Rejected",1,1,1),("Purchase Received",1,0,1)]),
 ("Construction", [("Update Upcoming",1,1,0),("Update Due",1,1,1),("Update Overdue",1,1,1),
                   ("Update Submitted",1,0,1),("Update Approved",1,1,1)]),
 ("Promotion", [("Promotion Created",1,0,0),("Promotion Starting",1,1,1),
                ("Promotion Expiring",1,1,1),("Quota Low",1,1,1),("Quota Sold Out",1,1,1)]),
 ("Training", [("Training Assigned",1,1,1),("Training Due",1,1,1),("Training Overdue",1,1,1),
               ("Test Passed",1,0,1),("Test Failed",1,1,1)]),
]
def dot(on):
    return (f'<div style="width:18px;height:18px;border-radius:5px;background:{SUCCESS};'
            f'display:grid;place-items:center;margin:0 auto">{icon(I_CHECK,12,"#0F172A")}</div>'
            if on else f'<div style="width:18px;height:18px;border-radius:5px;'
            f'border:1.5px solid {DIVIDER};margin:0 auto"></div>')

rows = ""
for grp, events in GROUPS:
    rows += (f'<tr><td colspan="4" style="padding-top:14px;border-bottom:0">'
             f'<span class="sec">{grp}</span></td></tr>')
    for name, sys_, line, mail in events:
        rows += (f'<tr><td style="color:{TXT2}">{name}</td>'
                 f'<td style="text-align:center">{dot(sys_)}</td>'
                 f'<td style="text-align:center">{dot(line)}</td>'
                 f'<td style="text-align:center">{dot(mail)}</td></tr>')

matrix = (f'<table><thead><tr><th>Event</th>'
          f'<th style="width:120px;text-align:center">System</th>'
          f'<th style="width:120px;text-align:center">LINE</th>'
          f'<th style="width:120px;text-align:center">Email</th></tr></thead>'
          f'<tbody>{rows}</tbody></table>')

roles = f"""<div class="col" style="gap:12px">
  <div class="row" style="gap:8px;flex-wrap:wrap">
    <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">ค่าเริ่มต้นของ Sales</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Manager</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Agency Support</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Marketing</span>
    <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Admin</span>
  </div>
  <p class="cap mut" style="margin:0">แอดมินตั้งค่าเริ่มต้นของแต่ละ role ได้
    แล้วผู้ใช้แต่ละคนปรับของตัวเองทีหลังได้ — ค่าของคนชนะค่าของ role เสมอ</p>
</div>"""

line_warn = note_box("warn", "LINE ส่งได้เฉพาะคนที่ผูก lineUserId แล้ว — คนที่ยังไม่ผูก "
    "ต้องแสดงว่า &quot;ยังผูก LINE ไม่ได้&quot; ในหน้าตั้งค่า ไม่ใช่ปล่อยให้ติ๊กแล้วเงียบหาย")

body = f"""{note_box("ok","ตาราง NotificationSetting · NotificationTemplate · NotificationLog มีอยู่แล้ว "
          "แต่ NotificationSetting เดิมเป็นค่ากลางตัวเดียวต่อประเภท (daily_brief, midday ...) "
          "ต้องเพิ่มตารางใหม่สำหรับค่าของแต่ละคนแต่ละ event และ<b>ห้ามแก้ของเดิม</b>")}
{panel("เลือกช่องทางต่อ event", roles, matrix,
  note="ไม่ใช้ Microsoft Teams · ปิดได้ทุกช่อง ยกเว้น System ที่เปิดค้างไว้เสมอสำหรับเหตุการณ์ที่ต้องรู้")}
{line_warn}
{note_box("error","ห้ามส่งซ้ำ — event เดียวกันต่อคนเดียวกันส่งได้ครั้งเดียว "
          "ใส่ unique key ที่ระดับฐานข้อมูล ไม่ใช่เช็กในโค้ดอย่างเดียว "
          "เพราะ scheduler ที่รันซ้อนกันจะยิงซ้ำทันที")}"""

open("Notification.dc.html","w").write(
    sheet("8 · Notification — System + LINE + Email",
          "ผู้ใช้เลือกได้ว่า event ไหนส่งช่องทางไหน", body, 1200, 1640, badge="ต่อยอดของเดิม"))
print("Notification.dc.html")
