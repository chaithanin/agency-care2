from shell import *

# ═══════ 7. Training & Test ═══════
chain = f"""<div class="row" style="gap:10px;flex-wrap:wrap;align-items:center">
  {"".join(
    f'<span class="chip" style="border:1px solid {DIVIDER};color:{TXT2}">{s}</span>'
    f'{"" if i==7 else f"<span style=color:{TXT3}>→</span>"}'
    for i, s in enumerate(["SOP / JD / Rules","Training Course","Learning Material",
                           "5 Questions","Submit Test","Score","Pass / Fail","Training Record"]))}
</div>"""

course = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Course","Agency Visit SOP", required=True)}
    {field("Version","2.0", w=120)}
    {field("Passing Score","80%", w=150, required=True)}
    {field("มาจาก","SOP-014", w=150)}
  </div>
  <div class="row" style="gap:14px">
    {field("มอบหมายให้","Sales · Agency Support", w=300)}
    {field("กำหนดส่ง","30 Sep 2026", w=190)}
    {field("ลองได้กี่ครั้ง","ไม่จำกัด", w=170)}
    <div class="col grow"></div>
  </div>
  {note_box("info","เนื้อหาอ่านได้จาก SOP, JD, Rules &amp; Regulation, Training Material "
            "และ 6-Step Process ที่มีอยู่แล้ว — Course คือการห่อเนื้อหาเดิมด้วยแบบทดสอบ "
            "ไม่ใช่เขียนเนื้อหาใหม่")}
</div>"""

def q(no, text, opts, correct):
    rows = "".join(
        f'<div class="row" style="gap:10px;padding:4px 0">'
        f'<div style="width:16px;height:16px;border-radius:999px;'
        f'{"border:2px solid "+SUCCESS if i==correct else "border:1.5px solid "+DIVIDER};'
        f'display:grid;place-items:center;flex-shrink:0">'
        f'{f"<div style=width:7px;height:7px;border-radius:999px;background:{SUCCESS}></div>" if i==correct else ""}'
        f'</div><span class="b2" style="color:{TXT if i==correct else TXT2}">{o}</span>'
        f'{f"<span class=cap style=color:{SUCCESS};font-weight:700>เฉลย</span>" if i==correct else ""}'
        f'</div>' for i, o in enumerate(opts))
    return (f'<div class="col" style="gap:8px;padding:12px 0;border-bottom:1px solid {DIVIDER}">'
            f'<span class="b2" style="font-weight:700">Question {no} — {text}</span>{rows}</div>')

quiz = (q(1,"ก่อนไปเยี่ยมเอเจนซี่ ต้องทำอะไรก่อน",
          ["โทรนัดล่วงหน้าและบันทึกใน Activity Plan","ไปถึงแล้วค่อยแจ้ง",
           "ส่งไลน์บอกวันก่อนไป","ให้เอเจนซี่เป็นคนนัดมาเอง"], 0)
      + q(2,"ใครเป็นผู้อนุมัติการเบิกของแจก",
          ["หัวหน้าทีมขาย","Manager","Agency Support","อนุมัติเองได้ถ้าไม่เกิน 5,000"], 1))

result = f"""<div class="col" style="gap:14px;width:340px;flex-shrink:0;background:{SURFACE};
     border:1px solid {DIVIDER};border-radius:18px;padding:18px 20px">
  <h4 class="sec">Training Result</h4>
  <div class="col" style="gap:9px">
    <div class="row"><span class="cap mut grow">Employee</span>
      <span class="b2" style="font-weight:600">John Smith</span></div>
    <div class="row"><span class="cap mut grow">Course</span>
      <span class="b2" style="font-weight:600">Agency Visit SOP</span></div>
    <div class="row"><span class="cap mut grow">Version</span>
      <span class="b2">2.0</span></div>
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row" style="gap:20px;align-items:center">
    <div class="col" style="gap:1px">
      <span style="font-size:30px;font-weight:700;letter-spacing:-0.02em">4 / 5</span>
      <span class="cap mut">คะแนน</span></div>
    <div class="col" style="gap:1px">
      <span style="font-size:30px;font-weight:700;color:{SUCCESS}">80%</span>
      <span class="cap mut">ผ่านเกณฑ์ 80%</span></div>
    <span class="grow"></span>{flow_chip("PASS")}
  </div>
</div>"""

HIST = [("Attempt 1","12 Sep 2026","3 / 5","60%","FAIL"),
        ("Attempt 2","17 Sep 2026","4 / 5","80%","PASS")]
h_rows = "".join(
    f'<tr><td style="font-weight:600">{a}</td><td class="mut">{d}</td>'
    f'<td>{s}</td><td style="font-weight:600">{p}</td><td>{flow_chip(r)}</td></tr>'
    for a, d, s, p, r in HIST)

body = f"""{note_box("warn","ตาราง TrainingRecord เดิมเป็นบันทึกการเข้าอบรม (ชื่อคอร์ส วันที่ ชั่วโมง ผู้เข้าร่วม) "
          "ไม่ใช่ระบบคอร์สที่มีข้อสอบ — ต้องเพิ่มตารางใหม่ Course · Question · Attempt "
          "และ<b>ห้ามแก้ TrainingRecord เดิม</b> เพราะมีข้อมูลอบรมย้อนหลังอยู่")}
{panel("โครงสร้าง", "", chain)}
{panel("Agency Visit SOP v2.0", flow_chip("Approved"), course)}
{panel("คำถาม 5 ข้อ", f'<span class="cap mut">แสดง 2 ข้อแรก</span>',
  f'<div class="row" style="gap:24px;align-items:flex-start">'
  f'<div class="col grow" style="gap:0">{quiz}</div>{result}</div>')}
{panel("ประวัติการสอบ — John Smith", f'<span class="cap mut">เก็บทุกครั้งที่สอบ</span>',
  f'<table><thead><tr><th style="width:150px">ครั้งที่</th><th style="width:170px">วันที่</th>'
  f'<th style="width:130px">คะแนน</th><th style="width:130px">เปอร์เซ็นต์</th>'
  f'<th style="width:130px">ผล</th></tr></thead><tbody>{h_rows}</tbody></table>',
  note="เก็บ Employee · Course · Version · วันเริ่ม · วันจบ · คะแนน · ผ่านไม่ผ่าน · จำนวนครั้ง · ครั้งล่าสุด · ใบรับรอง")}
{note_box("error","ผูกผลสอบกับ <b>เวอร์ชันของคอร์ส</b> เสมอ — "
          "แก้ SOP แล้วออกเวอร์ชันใหม่ ผลสอบเก่าต้องยังอ้างเวอร์ชันเดิมได้ "
          "ไม่งั้นจะตอบไม่ได้ว่าคนนี้สอบผ่านเนื้อหาชุดไหน")}"""

open("Training.dc.html","w").write(
    sheet("7 · SOP / JD / Rules → Training &amp; Test",
          "จาก Knowledge Base อย่างเดียว เป็น ความรู้ + อบรม + วัดผล",
          body, 1420, 1560, badge="ของใหม่ + ต่อยอด"))
print("Training.dc.html")
