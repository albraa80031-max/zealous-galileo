# -*- coding: utf-8 -*-
"""دمج طلب تأجيل الرسم 6181 مع مرفقه في ملف واحد يُرفع للبوابة.

المرفق «قرار تقسيط الرسوم 25/03/2026» مصدره Google Drive:
المعرّف 1SfZWxIlkchnIITJYAJ9vUUrFG-ZSIjiR — باسم «الموافقة علي تقسيط المبلغ .pdf».
يُنزَّل بجوار هذا السكربت باسم «قرار_تقسيط_الرسوم_25032026.pdf» قبل التشغيل.
"""
import io
import os
import sys

import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TALAB = os.path.join(HERE, 'طلب_تأجيل_الرسم_6181_2026.pdf')
QARAR = os.path.join(HERE, 'قرار_تقسيط_الرسوم_25032026.pdf')
OUT = os.path.join(HERE, 'طلب_تأجيل_الرسم_6181_2026_مع_المرفق.pdf')

Q = 85  # ضغط JPEG — الصور الخام تُخرج ملفاً لا يقبله الرفع


def main():
    for f in (TALAB, QARAR):
        if not os.path.exists(f):
            sys.exit(f'ناقص: {f}')

    out = pymupdf.open()
    out.insert_pdf(pymupdf.open(TALAB))

    # المرفق صفحةٌ ممسوحة ضوئياً — تُدرَج صورةً مضغوطة بحجمٍ معقول
    src = pymupdf.open(QARAR)
    for pg in src:
        pix = pg.get_pixmap(dpi=150)
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=Q, optimize=True)
        page = out.new_page(width=595, height=842)
        m = 28.0
        w = 595 - 2 * m
        h = w * pix.height / pix.width
        if h > 842 - 2 * m:
            h = 842 - 2 * m
            w = h * pix.width / pix.height
        x = (595 - w) / 2
        y = (842 - h) / 2
        page.insert_image(pymupdf.Rect(x, y, x + w, y + h), stream=buf.getvalue())

    out.save(OUT, deflate=True, garbage=4)
    print(f'{OUT} — {out.page_count} صفحات — {os.path.getsize(OUT)//1024} كيلوبايت')


if __name__ == '__main__':
    main()
