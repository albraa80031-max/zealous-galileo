# -*- coding: utf-8 -*-
"""بناء صفحات لقطات المراسلات — صورة واحدة لكل صفحة A4، بلا أي تعليق عليها."""
import os, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__))
IMGS = [
    os.path.join(HERE, 'shots', 'wa_11072026.png'),
    os.path.join(HERE, 'shots', 'wa_receipts_19_28072026.png'),
]
M = 36.0
doc = pymupdf.open()
for p in IMGS:
    page = doc.new_page(width=595, height=842)
    iw, ih = pymupdf.Pixmap(p).width, pymupdf.Pixmap(p).height
    aw, ah = 595 - 2*M, 842 - 2*M
    s = min(aw/iw, ah/ih)
    w, h = iw*s, ih*s
    x = (595 - w)/2; y = (842 - h)/2
    page.insert_image(pymupdf.Rect(x, y, x+w, y+h), filename=p)
out = os.path.join(HERE, 'لقطات_المراسلات.pdf')
doc.save(out); print(os.path.basename(out), doc.page_count, 'صفحة')
