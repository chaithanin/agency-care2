from shell import *

# ── Phase 4 — First Communication Package ────────────────────
welcome = "".join(check(x, d) for x, d in [
    ("Thank you for meeting us", True), ("Introduce GTG Team", True),
    ("Explain support system", True), ("Invite agency to work together", False)])

MK = [("Project Photos",True),("Project Videos",True),("Project Albums",True),
      ("Project Links",True),("3D Virtual Tour",False),("Google Drive Marketing Folder",True),
      ("Sales Kit",False),("Price List",True),("Matrix",False)]
mk = "".join(check(x, d) for x, d in MK)

meta = f"""<div class="col" style="gap:14px;width:290px;flex-shrink:0">
  {field("Shared Date","14 Sep 2026")}
  {field("Shared By","K. Somchai")}
  <div class="col" style="gap:0">
    <p class="lbl">Communication Channel</p>
    <div class="row" style="gap:8px">
      <span class="chip" style="background:rgba(34,197,94,.15);color:{SUCCESS}">LINE</span>
      <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Email</span>
      <span class="chip" style="border:1px solid {DIVIDER};color:{TXT3}">Other</span>
    </div>
  </div>
</div>"""

body = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 4 — First Communication Package</h2>
  <span class="chip" style="color:{WARNING};background:rgba(251,191,36,.15)">Waiting agency confirmation</span>
</div>
{panel("Welcome Communication", f'<span class="cap mut">3 / 4</span>',
       f'<div class="col" style="gap:0">{welcome}</div>')}
{panel("Marketing Package", f'<span class="cap mut">6 / 9</span>',
  f'''<div class="row" style="gap:28px;align-items:flex-start">
        <div class="grow" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px">{mk}</div>
        <div style="width:1px;align-self:stretch;background:{DIVIDER}"></div>
        {meta}
      </div>''')}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Phase 5</button>
</div>"""
open("Phase4.dc.html","w").write(detail_page(4, body, 1240))
print("Phase4.dc.html")

# ── Phase 5 — Agreement & Formal Setup ───────────────────────
STAGES = ["Not Started","Sent to Agency Support","Preparing Agreement","Waiting Signature","Signed"]
ACTIVE = 3
cells = []
for i, s in enumerate(STAGES):
    if i < ACTIVE:   c, bgc, bd = SUCCESS, "rgba(34,197,94,.15)", SUCCESS
    elif i == ACTIVE: c, bgc, bd = WARNING, "rgba(251,191,36,.15)", WARNING
    else:             c, bgc, bd = TXT3, "transparent", DIVIDER
    arrow = "" if i == len(STAGES)-1 else f'<span style="color:{TXT3};font-size:15px">→</span>'
    cells.append(f'<div class="row" style="gap:10px"><span class="chip" '
                 f'style="color:{c};background:{bgc};border:1px solid {bd}">{s}</span>{arrow}</div>')
flow = f'<div class="row" style="gap:10px;flex-wrap:wrap">{"".join(cells)}</div>'

AG = [("Agency Support informed",True),("Documents sent to Agency Support",True),
      ("Agreement prepared",True),("Second meeting completed",True),
      ("Agreement reviewed",True),("Agreement signed",False),
      ("Special Promotion signed",False),("Sales Plan discussed",True),
      ("Monthly Goal defined",True),("Agreement uploaded to Venio",False)]
ag = "".join(check(x, d) for x, d in AG)

upload = f"""<div class="col" style="gap:12px">
  <div class="row" style="gap:10px;justify-content:center;border:1.5px dashed {DIVIDER};
       border-radius:16px;padding:20px">
    {icon(I_UP,20,TXT3)}
    <span class="b2 mut">Upload signed Agency Agreement (PDF)</span>
  </div>
  <div class="row" style="gap:10px;background:rgba(251,191,36,.10);
       border:1px solid rgba(251,191,36,.35);border-radius:14px;padding:11px 14px">
    {icon(I_CLOCK,16,WARNING)}
    <span class="b2" style="color:{WARNING};font-weight:600">Waiting signature — 4 days</span>
    <span class="grow"></span>
    <button class="btn sm out">Send reminder</button>
  </div>
</div>"""

body5 = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 5 — Agreement &amp; Formal Setup</h2>
  {status_chip("NEED ATTENTION")}
</div>
{panel("Agreement Status", "", flow)}
{panel("Agreement Checklist", f'<span class="cap mut">7 / 10</span>',
  f'<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px">{ag}</div>')}
{panel("Signed Agency Agreement", "", upload,
       note="Verified by and verified at are recorded on every status change and kept in the audit log.")}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Phase 6</button>
</div>"""
open("Phase5.dc.html","w").write(detail_page(5, body5, 1400, pct=71, status="NEED ATTENTION"))
print("Phase5.dc.html")
