# -*- coding: utf-8 -*-
"""دمج ملف 6181: الصحيفة + غلاف الحافظة + الكشفان."""
import sys, os, pymupdf
ATT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SAHIFA = os.path.join(HERE, '..', 'munazaa', 'صحيفة_دعوى_منازعة_موضوعية_6181_2026.pdf')

def merge(parts, out):
    d = pymupdf.open()
    for p in parts:
        d.insert_pdf(pymupdf.open(p))
    d.save(out); n = d.page_count; d.close()
    print(os.path.basename(out), n, 'صفحة')

hafiza_parts = [
    os.path.join(HERE, 'غلاف_الحافظة.pdf'),
    os.path.join(ATT, 'كشف_الحساب_المصدق_صفحات_الدفعات_الخمس.pdf'),
    os.path.join(ATT, 'كشف_بطاقة_نون_6668_صفحتا_قيد_170.pdf'),
]
H = os.path.join(HERE, 'حافظة_مستندات_6181_2026.pdf')
merge(hafiza_parts, H)
merge([SAHIFA, H], os.path.join(HERE, 'الملف_الكامل_6181_2026.pdf'))
