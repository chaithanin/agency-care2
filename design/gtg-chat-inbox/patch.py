# -*- coding: utf-8 -*-
import io, re, glob

SUBS = [
  # พื้นหลังหน้า = body background จริงของ Agency Care
  ("background:{T['bg']};font-family:{BODY}", "background:{PAGE_BG};background-repeat:no-repeat;font-family:{BODY}"),
  # ฟองข้อความ: ขาออกใช้ gradient ปุ่ม primary, ระบบอัตโนมัติใช้ violet tint
  ('bgc = "#2F8C7C" if kind == "auto" else T[\'accent\']',
   'bgc = "rgba(124,111,240,0.30)" if kind == "auto" else BTN_GRAD'),
  # ข้อความ/ไอคอนสีม่วงบนพื้นมืด ใช้ primary.light เพื่อคอนทราสต์
  ('color:{T["accent"]}', 'color:{T["accentLight"]}'),
  ("color:{T['accent']}", "color:{T['accentLight']}"),
  (',T["accent"])', ',T["accentLight"])'),
  (",T['accent'])", ",T['accentLight'])"),
  # คอลัมน์ Inbox ให้พอดีกับ drawer 252px
  ('width:330px;flex:none;border-right', 'width:310px;flex:none;border-right'),
  ('width:316px;flex:none;border-left', 'width:300px;flex:none;border-left'),
]

LOGIN = [
  ("""<div style="width:620px;flex:none;background:{T['accent']};color:#fff;""",
   """<div style="width:560px;flex:none;background:linear-gradient(160deg,#1a1533 0%,#231b45 45%,#3b2f77 100%);color:#fff;"""),
  ('color:#CFE6DF;font-size:14px', 'color:rgba(236,235,245,0.78);font-size:14px'),
  ('color:#7FD3C0', 'color:{T["accentLight"]}'),
  ('color:#9FCEC3', 'color:{T["muted"]}'),
  ('height:42px;border-radius:9px;background:{T[\'accent\']};color:#fff',
   'height:44px;border-radius:12px;background:{BTN_GRAD};box-shadow:{BTN_SHADOW};color:#fff'),
  ('height:42px;border-radius:9px;border:1px solid {T[\'line\']};background:{T[\'surface\']}',
   'height:44px;border-radius:12px;border:1px solid rgba(255,255,255,0.14);background:rgba(255,255,255,0.03)'),
  ("""border:1px solid {T['accentLight']};background:{T['accent']};color:#fff""",
   """border:1px solid {T['accent']};background:{T['accent']};color:#fff"""),
]

DASH = [
  ('S1 = "#00897A"', 'S1 = "#7c6ff0"'),
  ('S2 = "#B45309"', 'S2 = "#b8800f"'),
  ('S3 = "#3B5BA5"', 'S3 = "#2f9fd0"'),
  ('GRID = "#E8EDEB"', 'GRID = "rgba(255,255,255,0.08)"'),
  ('AXIS = "#8CA09A"', 'AXIS = "#7f7d9c"'),
  ('col = S1 if good else S2', "col = T['ok'] if good else T['warn']"),
  ('fill="{T["ink"]}"', 'fill="#241f3a"'),
  ('fill="#CBD8D4"', 'fill="{T["muted"]}"'),
  ('("New Lead",612,"#B9E0D8"),("Hot Lead",281,"#6FC2B1"),("Payment",74,"#2FA08C"),("Customer",291,S1)',
   '("New Lead",612,"#3f3a6b"),("Hot Lead",281,"#5b4fd6"),("Payment",74,"#7c6ff0"),("Customer",291,"#9d93f5")'),
]

INTEG = [
  ('background:{T["ink"]};border-radius:10px;padding:14px;color:#D7E4E0',
   'background:#0d0b17;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px;color:#C9C5E6'),
  ('border:1px solid #BFDBD3', 'border:1px solid rgba(124,111,240,0.35)'),
]

def apply(path, subs):
    s = io.open(path, encoding='utf-8').read()
    n = 0
    for a, b in subs:
        if a in s:
            n += s.count(a)
            s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8').write(s)
    return n

total = 0
for f in sorted(glob.glob('build*.py')):
    total += apply(f, SUBS)
total += apply('build1.py', LOGIN)
total += apply('build4.py', DASH)
total += apply('build5.py', INTEG)
print('applied', total, 'replacements')
