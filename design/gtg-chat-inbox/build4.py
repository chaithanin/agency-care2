# -*- coding: utf-8 -*-
exec(open('gen.py', encoding='utf-8').read())

S1 = "#7c6ff0"   # ชุดสี categorical ที่ผ่าน validator (teal ใกล้แบรนด์ แต่ chroma พอ)
S2 = "#b8800f"
S3 = "#2f9fd0"
GRID = "rgba(255,255,255,0.08)"
AXIS = "#7f7d9c"

# ── KPI tiles ───────────────────────────────────────────────────────────
def tile(title, value, unit, delta, good=True, sub=""):
    arrow = "m4 9 4-4 4 4" if good else "m4 5 4 4 4-4"
    col = T['ok'] if good else T['warn']
    return (f'<div style="flex:1;background:{T["surface"]};border:1px solid {T["line"]};border-radius:16px;padding:15px 16px;'
            f'display:flex;flex-direction:column;gap:7px">'
            f'<span style="font-size:12.5px;color:{T["muted"]}">{title}</span>'
            f'<div style="display:flex;align-items:baseline;gap:6px">'
            f'<span style="font-family:{DISPLAY};font-weight:700;font-size:28px;line-height:1;font-variant-numeric:tabular-nums">{value}</span>'
            f'<span style="font-size:13px;color:{T["muted"]}">{unit}</span></div>'
            f'<div style="display:flex;align-items:center;gap:6px;font-size:12px;color:{T["muted"]}">'
            f'<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="{arrow}"/><path d="M8 5v7"/></svg>'
            f'<span style="color:{col}">{delta}</span>{sub}</div></div>')

tiles = "".join([
  tile("บทสนทนาที่เปิดอยู่", "24", "เคส", "+6", True, "จากสัปดาห์ก่อน"),
  tile("ยังไม่มีคนรับ", "3", "เคส", "−74", True, "หลังเปิดกฎมอบหมาย"),
  tile("เวลาตอบครั้งแรกเฉลี่ย", "4:12", "นาที", "−1:38", True, "จากสัปดาห์ก่อน"),
  tile("ปิดเคสวันนี้", "18", "เคส", "+3", True, "จากเมื่อวาน"),
])

# ── บทสนทนาเปิด/ปิด 14 วัน ───────────────────────────────────────────────
DAYS = ["2 ก.ย.","3","4","5","6","7","8","9","10","11","12","13","14","15"]
OPENED = [18,22,19,26,31,24,12,9,27,29,33,28,15,11]
CLOSED = [15,20,21,24,28,26,14,11,24,31,30,26,18,13]
PW, PH, PX, PY = 628, 196, 34, 14
YMAX = 36
step = PW / len(DAYS)
bw = 17
bars = []
for i, (o, c) in enumerate(zip(OPENED, CLOSED)):
    gx = PX + i * step + (step - (bw * 2 + 3)) / 2
    for j, (v, col) in enumerate(((o, S1), (c, S2))):
        h = v / YMAX * PH
        x = gx + j * (bw + 3)
        bars.append(f'<rect x="{x:.1f}" y="{PY + PH - h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="{col}"/>')
grid = []
for gv in (0, 12, 24, 36):
    gy = PY + PH - gv / YMAX * PH
    grid.append(f'<line x1="{PX}" y1="{gy:.1f}" x2="{PX + PW}" y2="{gy:.1f}" stroke="{GRID}" stroke-width="1"/>')
    grid.append(f'<text x="{PX - 10}" y="{gy + 3.5:.1f}" text-anchor="end" font-size="10.5" fill="{AXIS}" font-family="{BODY}">{gv}</text>')
xlabels = "".join(
  f'<text x="{PX + i * step + step / 2:.1f}" y="{PY + PH + 18}" text-anchor="middle" font-size="10.5" fill="{AXIS}" font-family="{BODY}">{d}</text>'
  for i, d in enumerate(DAYS))
# tooltip ที่วันจันทร์ 12 ก.ย. (index 10)
tip_x = PX + 10 * step + step / 2
tooltip = (f'<g><line x1="{tip_x:.1f}" y1="{PY}" x2="{tip_x:.1f}" y2="{PY + PH}" stroke="{AXIS}" stroke-width="1" stroke-dasharray="3 3"/>'
  f'<rect x="{tip_x - 74:.1f}" y="{PY - 6}" width="148" height="62" rx="9" fill="#241f3a"/>'
  f'<text x="{tip_x - 60:.1f}" y="{PY + 12}" font-size="11" fill="{T["muted"]}" font-family="{BODY}">12 ก.ย. 2569</text>'
  f'<circle cx="{tip_x - 62:.1f}" cy="{PY + 26}" r="4" fill="{S1}"/>'
  f'<text x="{tip_x - 52:.1f}" y="{PY + 30}" font-size="11.5" fill="#fff" font-family="{BODY}">เปิดใหม่</text>'
  f'<text x="{tip_x + 62:.1f}" y="{PY + 30}" font-size="11.5" fill="#fff" text-anchor="end" font-family="{BODY}">33</text>'
  f'<circle cx="{tip_x - 62:.1f}" cy="{PY + 43}" r="4" fill="{S2}"/>'
  f'<text x="{tip_x - 52:.1f}" y="{PY + 47}" font-size="11.5" fill="#fff" font-family="{BODY}">ปิดแล้ว</text>'
  f'<text x="{tip_x + 62:.1f}" y="{PY + 47}" font-size="11.5" fill="#fff" text-anchor="end" font-family="{BODY}">30</text></g>')

def legend(items):
    return ('<div style="display:flex;align-items:center;gap:16px">' + "".join(
      f'<span style="display:inline-flex;align-items:center;gap:7px;font-size:12px;color:{T["muted"]}">'
      f'<span style="width:10px;height:10px;border-radius:3px;background:{c}"></span>{n}</span>' for n, c in items) + '</div>')

trend_chart = (f'<svg width="688" height="250" viewBox="0 0 688 250" role="img">'
  f'{"".join(grid)}{"".join(bars)}{xlabels}{tooltip}</svg>')

# ── Lifecycle funnel ────────────────────────────────────────────────────
FUNNEL = [("New Lead",612,"#3f3a6b"),("Hot Lead",281,"#5b4fd6"),("Payment",74,"#7c6ff0"),("Customer",291,"#9d93f5")]
fmax = max(v for _, v, _ in FUNNEL)
funnel_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:12px">'
  f'<span style="width:74px;flex:none;font-size:12.5px;color:{T["muted"]}">{n}</span>'
  f'<span style="height:26px;border-radius:4px;background:{c};width:{v / fmax * 178:.0f}px;flex:none"></span>'
  f'<span style="font-size:13px;font-weight:600;font-variant-numeric:tabular-nums">{v:,}</span></div>'
  for n, v, c in FUNNEL)

# ── ภาระงานต่อเซลส์ ──────────────────────────────────────────────────────
LOAD = [("Ploy (Sales)",11,S1),("Nok (Sales)",7,S1),("Ivan (Sales RU)",6,S1),("ยังไม่มีคนรับ",3,S2)]
lmax = 12
load_rows = "".join(
  f'<div style="display:flex;align-items:center;gap:12px">'
  f'<span style="width:118px;flex:none;font-size:12.5px;color:{T["muted"]}">{n}</span>'
  f'<span style="height:22px;border-radius:4px;background:{c};width:{v / lmax * 296:.0f}px;flex:none"></span>'
  f'<span style="font-size:13px;font-weight:600;font-variant-numeric:tabular-nums">{v}</span></div>'
  for n, v, c in LOAD)

# ── สัดส่วนช่องทาง ────────────────────────────────────────────────────────
SHARE = [("LINE",62,S1),("Facebook",24,S2),("WhatsApp",14,S3)]
share_bar = "".join(
  f'<span style="height:34px;background:{c};width:{p / 100 * 468:.0f}px;flex:none;display:flex;align-items:center;'
  f'justify-content:center;color:#fff;font-size:12.5px;font-weight:600">{p}%</span>'
  for _, p, c in SHARE)
share_legend = "".join(
  f'<div style="display:flex;align-items:center;gap:9px;font-size:12.5px">'
  f'<span style="width:10px;height:10px;border-radius:3px;background:{c};flex:none"></span>'
  f'<span style="flex:1">{n}</span>'
  f'<span style="color:{T["muted"]};font-variant-numeric:tabular-nums">{int(p / 100 * 1284):,} ผู้ติดต่อ</span></div>'
  for n, p, c in SHARE)

dashboard = f'''<div style="width:1440px;height:900px;display:flex;background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY};color:{T['ink']};overflow:hidden">
  {rail("chart")}
  <div style="flex:1;display:flex;flex-direction:column;min-width:0">
    {topbar("Dashboard", select("14 วันล่าสุด",160) + '<div style="width:8px"></div>' + select("ทุกช่องทาง",150) + '<div style="width:8px"></div>' + btn("ส่งออกรายงาน","ghost","arrowdown"))}
    <div style="flex:1;padding:20px 24px;display:flex;flex-direction:column;gap:18px;overflow:hidden">
      <div style="display:flex;gap:14px">{tiles}</div>

      <div style="display:flex;gap:14px;align-items:stretch">
        <div style="width:718px;flex:none;background:{T['surface']};border:1px solid {T['line']};border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:12px">
          <div style="display:flex;align-items:center;gap:14px">
            <span style="font-family:{DISPLAY};font-weight:600;font-size:14.5px">บทสนทนาเปิดใหม่และปิด · 14 วันล่าสุด</span>
            <div style="flex:1"></div>{legend([("เปิดใหม่",S1),("ปิดแล้ว",S2)])}
          </div>
          {trend_chart}
        </div>
        <div style="flex:1;background:{T['surface']};border:1px solid {T['line']};border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:14px">
          <span style="font-family:{DISPLAY};font-weight:600;font-size:14.5px">Lifecycle ของผู้ติดต่อ</span>
          <div style="display:flex;flex-direction:column;gap:13px">{funnel_rows}</div>
          <div style="margin-top:auto;border-top:1px solid {T['line']};padding-top:12px;display:flex;flex-direction:column;gap:6px">
            <div style="display:flex;justify-content:space-between;font-size:12.5px"><span style="color:{T['muted']}">ผู้ติดต่อทั้งหมด</span><span style="font-weight:600">1,284</span></div>
            <div style="display:flex;justify-content:space-between;font-size:12.5px"><span style="color:{T['muted']}">แปลงเป็น Customer</span><span style="font-weight:600">22.6%</span></div>
          </div>
        </div>
      </div>

      <div style="display:flex;gap:14px;align-items:stretch">
        <div style="flex:1;background:{T['surface']};border:1px solid {T['line']};border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:14px">
          <span style="font-family:{DISPLAY};font-weight:600;font-size:14.5px">ภาระงานต่อเซลส์ (เคสที่เปิดอยู่)</span>
          <div style="display:flex;flex-direction:column;gap:12px">{load_rows}</div>
          <span style="margin-top:auto;font-size:12px;color:{T['muted']};line-height:1.6">เกณฑ์เตือนเมื่อเซลส์คนใดถือเกิน 15 เคส · ตั้งค่าได้ที่ Automations</span>
        </div>
        <div style="flex:1;background:{T['surface']};border:1px solid {T['line']};border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:14px">
          <span style="font-family:{DISPLAY};font-weight:600;font-size:14.5px">สัดส่วนช่องทางที่ลูกค้าติดต่อเข้ามา</span>
          <div style="display:flex;gap:2px;border-radius:6px;overflow:hidden">{share_bar}</div>
          <div style="display:flex;flex-direction:column;gap:10px">{share_legend}</div>
          <span style="margin-top:auto;font-size:12px;color:{T['muted']};line-height:1.6">Instagram ยังไม่เปิดใช้งาน · เพิ่มได้ที่ ตั้งค่า › ช่องทาง</span>
        </div>
      </div>
    </div>
  </div>
</div>'''
write("Dashboard.dc.html", dashboard)
