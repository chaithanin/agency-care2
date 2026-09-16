from shell import *

# ── Phase 2 — Communication Setup ────────────────────────────
line_body = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px">
    {field("Group Name","GTG × ABC Property Pattaya")}
    {field("LINE Group Link","line.me/ti/g/8xK2mQ")}
    {field("Created Date","15 Sep 2026", w=180)}
  </div>
  <div class="col" style="gap:0">
    <p class="lbl">Members Checklist</p>
    <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px">
      {check("Agency Owner")}{check("Assigned Seller")}
      {check("Agency Sales Team")}{check("Marketing")}
      {check("Management")}{check("Project Manager", False)}
      {check("Agency Support")}<span></span>
    </div>
  </div>
  <div class="row" style="gap:10px">
    <button class="btn sm">Mark LINE Group Created</button>
    <span class="chip" style="color:{SUCCESS};background:rgba(34,197,94,.15)">Created 15 Sep</span>
  </div>
</div>"""

seller_body = f"""<div class="col" style="gap:14px">
  <div class="row" style="gap:14px;align-items:flex-end">
    <div class="col" style="gap:0;flex-grow:1">
      <p class="lbl">Account Manager</p>
      <div class="row fld" style="gap:8px"><span class="grow">K. Somchai Rattana</span>{icon(I_CHEV,15,TXT3)}</div>
    </div>
    <button class="btn">Assign Account Manager</button>
  </div>
  <div class="row" style="gap:10px;background:rgba(59,130,246,.10);
       border:1px solid rgba(59,130,246,.30);border-radius:14px;padding:11px 14px">
    <span class="b2" style="color:{PRIMARY_L};font-weight:600">Assigned to: K. Somchai Rattana</span>
    <span class="grow"></span>
    <span class="cap mut">since 15 Sep 2026</span>
  </div>
  <div class="col" style="gap:0">
    {check("Seller assigned")}
    {check("Seller added to LINE group")}
    {check("Seller reviewed Agency Background", False)}
  </div>
</div>"""

body = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 2 — Communication Setup</h2>
  <span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">2 of 3 done</span>
</div>
{panel("Agency LINE Group", "", line_body)}
{panel("Assigned Seller", "", seller_body,
       note="The seller must be briefed on the agency background before the first contact.")}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Phase 3</button>
</div>"""
open("Phase2.dc.html","w").write(detail_page(2, body, 1240, pct=31, status="IN PROGRESS", done=12, total=39, outstanding=5))
print("Phase2.dc.html")

# ── Phase 3 — System Entry & Digital Setup ───────────────────
venio_body = f"""<div class="col" style="gap:16px">
  <div class="col" style="gap:0">
    {check("Agency profile registered")}
    {check("Contacts added")}
    {check("Social media added")}
    {check("Seller assigned")}
    {check("Bank information added")}
    {check("Owner ID uploaded", False)}
    {check("All documents verified", False)}
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row" style="gap:14px;align-items:flex-end">
    {field("Venio Agency ID","VEN-000283", w=260)}
    <button class="btn out">{icon(I_EXT,14,TXT2)} &nbsp;Open in Venio</button>
    <span class="grow"></span>
    <span class="cap mut">Manual verification — API sync not available yet</span>
  </div>
</div>"""

task_rows = ""
for t, owner, due, pr, st in [
    ("Send price list &amp; matrix","K. Somchai","17 Sep 2026","High","Open"),
    ("Collect Owner passport copy","Agency Support","18 Sep 2026","High","Open"),
    ("Arrange office visit","K. Somchai","22 Sep 2026","Normal","Planned")]:
    pc = ERROR if pr == "High" else TXT3
    pbg = "rgba(239,68,68,.15)" if pr == "High" else "rgba(107,114,128,.18)"
    task_rows += (f'<tr><td style="font-weight:600">{t}</td><td class="mut">{owner}</td>'
                  f'<td>{due}</td><td><span class="chip" style="color:{pc};background:{pbg}">{pr}</span></td>'
                  f'<td class="mut">{st}</td></tr>')

report_body = f"""<div class="col" style="gap:14px">
  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px">
    <div class="col" style="gap:0"><p class="lbl">Meeting Summary</p>
      <div class="fld" style="min-height:72px;color:{TXT2}">First meeting 15 Sep at GTG office.
        Owner plus two sales staff attended. Walked through three projects.</div></div>
    <div class="col" style="gap:0"><p class="lbl">Agency Needs</p>
      <div class="fld" style="min-height:72px;color:{TXT2}">Printed brochures in Russian,
        a floor-standing display, and updated availability every week.</div></div>
    <div class="col" style="gap:0"><p class="lbl">Opportunities</p>
      <div class="fld" style="min-height:72px;color:{TXT2}">Two buyers already looking in
        Jomtien at 4–6 MB. Agency runs a Russian-language channel with real reach.</div></div>
    <div class="col" style="gap:0"><p class="lbl">Potential Customers</p>
      <div class="fld" style="min-height:72px;color:{TXT2}">Mr. Ivan K. — 1BR investment;
        Ms. Elena V. — 2BR sea view, viewing next week.</div></div>
  </div>
  <div style="height:1px;background:{DIVIDER}"></div>
  <div class="row"><h4 class="sec grow">Follow-up Tasks</h4>
    <button class="btn sm out">{icon(I_PLUS,13,TXT2)} &nbsp;Add Task</button></div>
  <table><thead><tr><th>Task Name</th><th style="width:150px">Owner</th>
    <th style="width:140px">Due Date</th><th style="width:110px">Priority</th>
    <th style="width:110px">Status</th></tr></thead><tbody>{task_rows}</tbody></table>
</div>"""

body3 = f"""<div class="row" style="gap:12px">
  <h2 class="h6 grow">Phase 3 — System Entry &amp; Digital Setup</h2>
  <span class="chip" style="color:{PRIMARY_L};background:rgba(59,130,246,.16)">5 of 7 done</span>
</div>
{panel("Venio CRM Setup", f'<span class="cap mut">5 / 7</span>', venio_body)}
{panel("Initial Agency Report", "", report_body)}
<div class="row" style="gap:10px;justify-content:flex-end">
  <button class="btn out">Back</button>
  <button class="btn">Continue to Phase 4</button>
</div>"""
open("Phase3.dc.html","w").write(detail_page(3, body3, 1620, pct=46, status="IN PROGRESS", done=18, total=39, outstanding=2))
print("Phase3.dc.html")
