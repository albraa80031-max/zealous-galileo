# -*- coding: utf-8 -*-
"""دمج إيصالَي التحويل في ملف واحد يُرفق بطلب إعادة الاحتساب في 161/2025.

المصدر: Google Drive —
  1Qd5I_9zBc7T1R4UaD_HvoXTXXQeKJ6r- → إيصال 1,000 بتاريخ 24/11/2026
  1RUoZkzOt4WX8uZz1iFIRdBaORaU7IEWK → إيصال 500 بتاريخ 27/11/2026
يُنزَّلان بجوار هذا السكربت بالاسمين أدناه قبل التشغيل.
"""
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = ['إيصال_1000_24112026.pdf', 'إيصال_500_27112026.pdf']
OUT = os.path.join(HERE, 'إيصالا_السداد_161_2025.pdf')


def main():
    out = pymupdf.open()
    for name in SRC:
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            sys.exit(f'ناقص: {p}')
        out.insert_pdf(pymupdf.open(p))
    out.save(OUT, deflate=True, garbage=4)
    print(f'{OUT} — {out.page_count} صفحتان — {os.path.getsize(OUT)//1024} كيلوبايت')


if __name__ == '__main__':
    main()
