# -*- coding: utf-8 -*-
"""بناء صفحات لقطات المراسلات — صورة واحدة لكل صفحة A4، بلا أي تعليق عليها."""
import os, io, pymupdf
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
IMGS = [
    os.path.join(HERE, 'shots', 'wa_11072026.png'),
    os.path.join(HERE, 'shots', 'wa_receipts_19_28072026.png'),
]
M = 36.0
Q = 85           # ضغط JPEG — PNG الخام يُخرج ملفاً 15 ميغابايت لا يقبله الرفع
doc = pymupdf.open()
for p in IMGS:
    im = Image.open(p).convert('RGB')
    iw, ih = im.size
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=Q, optimize=True)
    page = doc.new_page(width=595, height=842)
    aw, ah = 595 - 2*M, 842 - 2*M
    s = min(aw/iw, ah/ih)
    w, h = iw*s, ih*s
    x = (595 - w)/2; y = (842 - h)/2
    page.insert_image(pymupdf.Rect(x, y, x+w, y+h), stream=buf.getvalue())
out = os.path.join(HERE, 'لقطات_المراسلات.pdf')
doc.save(out, deflate=True, garbage=4); print(os.path.basename(out), doc.page_count, 'صفحة')
