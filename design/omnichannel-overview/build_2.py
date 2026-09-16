from shell import *

# ══════ 2. Funnel + Project Interest ══════
STAGES = [("NEW LEADS",1284,100),("CONTACTED",986,77),("QUALIFIED",721,56),
          ("INTERESTED",486,38),("VIEWING",218,17),("RESERVATION",74,6),("CLOSED",32,2)]
rows = []
for i,(name,n,pct) in enumerate(STAGES):
    conv = "" if i == 0 else f"{round(STAGES[i][1]/STAGES[i-1][1]*100)}%"
    drop = "" if i == 0 else f"−{STAGES[i-1][1]-n:,}"
    arrow = ("" if i == 0 else
      f'<div class="row" style="gap:10px;padding:3px 0 3px 212px">'
      f'<span class="cap" style="color:{TXT3}">↓</span>'
      f'<span class="cap" style="color:{TXT2};font-weight:600">{conv}</span>'
      f'<span class="cap mut">{drop}</span></div>')
    rows.append(arrow + f"""<div class="row" style="gap:14px;align-items:center">
  <span class="b2" style="width:150px;flex-shrink:0;font-weight:600;letter-spacing:.03em;
        font-size:12px;color:{TXT2}">{name}</span>
  <span class="b2" style="width:62px;flex-shrink:0;text-align:right;font-weight:700">{n:,}</span>
  <div style="width:420px;flex-shrink:0;height:22px;background:{SURFACE};border-radius:4px">
    <div style="width:{pct}%;height:22px;background:{S_BLUE};border-radius:4px"></div>
  </div>
</div>""")

key = f"""<div class="row" style="gap:22px;flex-wrap:wrap;background:{SURFACE};
     border:1px solid {DIVIDER};border-radius:16px;padding:13px 16px">
  <div class="col" style="gap:2px"><span class="cap mut">New → Qualified</span>
    <span class="b2" style="font-weight:700;color:{S_BLUE}">56%</span></div>
  <div class="col" style="gap:2px"><span class="cap mut">Qualified → Viewing</span>
    <span class="b2" style="font-weight:700;color:{S_BLUE}">30%</span></div>
  <div class="col" style="gap:2px"><span class="cap mut">Viewing → Reservation</span>
    <span class="b2" style="font-weight:700;color:{S_BLUE}">34%</span></div>
  <div class="col" style="gap:2px"><span class="cap mut">Reservation → Closed</span>
    <span class="b2" style="font-weight:700;color:{S_BLUE}">43%</span></div>
  <span class="grow"></span>
  <div class="col" style="gap:2px"><span class="cap mut">New → Closed</span>
    <span class="b2" style="font-weight:700">2.5%</span></div>
</div>"""

proj_seg = f"""<div class="row" style="gap:6px;flex-wrap:wrap">
  <span class="chip" style="background:rgba(59,130,246,.16);color:{PRIMARY_L}">All Projects</span>
  <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">LOVE IT</span>
  <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Marina Golden Bay</span>
  <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Harmonia</span>
  <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">LUMINA</span>
</div>"""

funnel = panel("Lead Journey", proj_seg,
  f'<div class="col" style="gap:0">{"".join(rows)}</div>{key}',
  note="เปอร์เซ็นต์ระหว่างขั้นคืออัตราที่เดินต่อได้ ตัวเลขสีจางคือจำนวนที่หลุดออกไป")

# ── Project Interest ──
PROJ = [("LOVE IT Wongamat",38,"488 leads","142 convo","64 viewing","21 reservation"),
        ("Marina Golden Bay",27,"347 leads","98 convo","41 viewing","14 reservation"),
        ("Harmonia City Garden",21,"270 leads","74 convo","28 viewing","9 reservation"),
        ("LUMINA",14,"179 leads","46 convo","19 viewing","6 reservation")]
prows = ""
for name, pct, leads, convo, view, resv in PROJ:
    prows += f"""<div class="col" style="gap:7px;padding:11px 0;border-bottom:1px solid {DIVIDER}">
  <div class="row" style="gap:14px;align-items:center">
    <span class="b2" style="width:190px;flex-shrink:0;font-weight:600">{name}</span>
    <div style="width:260px;flex-shrink:0;height:14px;background:{SURFACE};border-radius:4px">
      <div style="width:{pct}%;height:14px;background:{S_BLUE};border-radius:4px"></div>
    </div>
    <span class="b2" style="font-weight:700;width:46px">{pct}%</span>
  </div>
  <div class="row" style="gap:18px;padding-left:204px;flex-wrap:wrap">
    <span class="cap mut">{leads}</span><span class="cap mut">{convo}</span>
    <span class="cap mut">{view}</span><span class="cap mut">{resv}</span>
  </div>
</div>"""

project = panel("Project Interest", f'<span class="cap mut">สัดส่วนจากบทสนทนา ไม่ใช่จากยอดขาย</span>',
  f'<div class="col" style="gap:0">{prows}</div>')

open("Funnel.dc.html","w").write(
    dash("Omnichannel Overview — Lead Journey &amp; Projects",
         "Lead เดินไปถึงขั้นไหน และโครงการไหนมี demand จริงจากการคุย",
         f'<div class="row" style="gap:18px;align-items:flex-start">{funnel}{project}</div>',
         1560, 960))
print("Funnel.dc.html")
