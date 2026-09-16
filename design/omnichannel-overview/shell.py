from tokens import *

HUB_TABS = ["CRM 360°", "Reports", "KPI", "Omnichannel Overview"]

def hub(active="Omnichannel Overview"):
    out = []
    for t in HUB_TABS:
        on = t == active
        style = (f"background:rgba(59,130,246,.16);border:1px solid {PRIMARY};color:{PRIMARY_L};font-weight:700"
                 if on else f"border:1px solid {DIVIDER};color:{TXT2};font-weight:600")
        out.append(f'<div style="padding:6px 18px;border-radius:999px;font-size:13px;{style}">{t}</div>')
    return f'<div class="row" style="gap:6px;flex-wrap:wrap">{"".join(out)}</div>'

def dash(title, subtitle, body, w, h):
    inner = f"""<div class="col" style="padding:26px 30px;gap:18px">
  {hub()}
  <div class="row" style="gap:12px">
    <div class="col grow" style="gap:3px">
      <h1 class="h5">{title}</h1>
      <p class="cap mut" style="margin:0">{subtitle}</p>
    </div>
  </div>
  {body}
</div>"""
    return page(inner, w, h)

def panel(title, right="", body="", note=None, grow=True):
    note_html = f'<p class="cap mut" style="margin:0">{note}</p>' if note else ""
    g = "grow" if grow else ""
    return f"""<div class="card pad col {g}" style="gap:14px">
  <div class="row" style="gap:12px"><h3 class="sec grow">{title}</h3>{right}</div>
  {note_html}
  {body}
</div>"""

def kpi(label, value, delta=None, delta_good=True):
    d = ""
    if delta:
        c = ST_GOOD if delta_good else ST_CRIT
        arrow = "▲" if delta_good else "▼"
        d = f'<span class="cap" style="color:{c};font-weight:700">{arrow} {delta}</span>'
    return f"""<div class="col" style="background:{PAPER};border:1px solid {DIVIDER};border-radius:18px;
     padding:15px 18px;gap:3px;flex-grow:1;min-width:158px">
  <span class="cap mut" style="font-weight:600;letter-spacing:.03em">{label}</span>
  <div class="row" style="gap:8px;align-items:baseline">
    <span style="font-size:24px;font-weight:700;letter-spacing:-0.02em">{value}</span>{d}
  </div>
</div>"""

def legend(items):
    """items = [(label, color)] — ทุกกราฟตั้งแต่ 2 series ขึ้นไปต้องมี"""
    out = "".join(
        f'<div class="row" style="gap:7px"><span style="width:11px;height:11px;border-radius:3px;'
        f'background:{c};display:inline-block"></span>'
        f'<span class="cap" style="color:{TXT2}">{l}</span></div>' for l, c in items)
    return f'<div class="row" style="gap:18px;flex-wrap:wrap">{out}</div>'

def hbar(label, pct, value, color, width=300):
    """แถบนอน — ปลายมน 4px ยึดกับเส้นฐาน มีเลขกำกับตรง ไม่ต้องอ่านจากแกน"""
    return f"""<div class="row" style="gap:14px;align-items:center">
  <span class="b2" style="width:200px;flex-shrink:0;color:{TXT2}">{label}</span>
  <div style="width:{width}px;flex-shrink:0;height:14px;background:{SURFACE};border-radius:4px">
    <div style="width:{pct}%;height:14px;background:{color};border-radius:4px"></div>
  </div>
  <span class="b2" style="font-weight:700;width:52px">{pct}%</span>
  <span class="cap mut">{value}</span>
</div>"""

def donut(slices, size=170, thickness=26):
    """โดนัท SVG — ชิ้นติดกันเว้นช่องสีพื้น 2px ตามสเปก"""
    import math
    r = (size - thickness) / 2
    cx = cy = size / 2
    circ = 2 * math.pi * r
    gap = 2.0
    out, offset = [], 0.0
    for label, pct, color in slices:
        length = circ * pct / 100
        seg = max(length - gap, 1)
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
            f'stroke-width="{thickness}" stroke-dasharray="{seg:.2f} {circ - seg:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"></circle>')
        offset += length
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{SURFACE}" '
            f'stroke-width="{thickness}"></circle>{"".join(out)}</svg>')

def line_chart(series, labels, w=980, h=230, ymax=None):
    """กราฟเส้น — เส้นหนา 2px จุด 8px แกนและกริดถอยหลัง"""
    pad_l, pad_b, pad_t, pad_r = 44, 26, 12, 12
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    ymax = ymax or max(max(v for v in s[1]) for s in series)
    step = iw / (len(labels) - 1)
    grid = "".join(
        f'<line x1="{pad_l}" y1="{pad_t + ih * i / 4:.1f}" x2="{w - pad_r}" '
        f'y2="{pad_t + ih * i / 4:.1f}" stroke="{GRID}" stroke-width="1"></line>' for i in range(5))
    yl = "".join(
        f'<text x="{pad_l - 9}" y="{pad_t + ih * i / 4 + 4:.1f}" text-anchor="end" '
        f'font-size="11" fill="{TXT3}">{int(ymax * (4 - i) / 4)}</text>' for i in range(5))
    xl = "".join(
        f'<text x="{pad_l + step * i:.1f}" y="{h - 6}" text-anchor="middle" '
        f'font-size="11" fill="{TXT3}">{l}</text>' for i, l in enumerate(labels))
    paths = []
    for name, vals, color in series:
        pts = [(pad_l + step * i, pad_t + ih - ih * v / ymax) for i, v in enumerate(vals)]
        d = " ".join(("M" if i == 0 else "L") + f"{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
        paths.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" '
                     f'stroke-linecap="round" stroke-linejoin="round"></path>')
        # จุดสุดท้ายใส่วงแหวนสีพื้น 2px กันทับกัน
        x, y = pts[-1]
        paths.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" '
                     f'stroke="{PAPER}" stroke-width="2"></circle>')
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{grid}{yl}{xl}{"".join(paths)}</svg>'
