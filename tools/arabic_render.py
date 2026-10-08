# -*- coding: utf-8 -*-
"""مُصيِّر مستندات عربية RTL — DOCX + PDF. أُعيد بناؤه 07/10/2026."""
import re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import weasyprint

FONT = "Amiri"
LRI, PDI = "⁦", "⁩"   # عزل أرقام تنعكس بصرياً في RTL

# رمز مختلط (AJCAPCICIVS2026/0000279، بريد، لوحة) يُعزل كوحدة قبل الأرقام العادية
_BND = r'(?<![0-9A-Za-z_\u2066\u2069])'   # يسمح بحرف عربي قبله، ويمنع لاتينياً أو رقماً
_MIX = re.compile(_BND + r'([A-Za-z][\w.]*(?:[/\-_@][\w.]+)+)')
_NUM = re.compile(_BND + r'(\d[\d,.:/\-]*\d|\d)(?![0-9A-Za-z_])')

def iso(t):
    """يعزل كل رقم/تاريخ/رمز مختلط حتى لا ينعكس بصرياً في RTL."""
    t = _MIX.sub(lambda m: LRI + m.group(0) + PDI, t)
    out, i = [], 0
    for m in re.finditer('\u2066[^\u2069]*\u2069', t):          # لا يُعاد عزل المعزول
        out.append(_NUM.sub(lambda x: LRI + x.group(0) + PDI, t[i:m.start()]))
        out.append(m.group(0)); i = m.end()
    out.append(_NUM.sub(lambda x: LRI + x.group(0) + PDI, t[i:]))
    return ''.join(out)

# ---------- DOCX ----------
def _bidi(pPr):
    for tag in ('w:bidi',):
        e = OxmlElement(tag); pPr.append(e)

def _rtl_run(run, bold=False, size=12.5):
    run.font.name = FONT; run.font.size = Pt(size); run.bold = bold
    rPr = run._element.get_or_add_rPr()
    for t in ('w:rtl', 'w:cs'):
        rPr.append(OxmlElement(t))
    rF = OxmlElement('w:rFonts')
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'):
        rF.set(qn(a), FONT)
    rPr.append(rF)

def _para(doc, text, bold=False, size=12.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space=6):
    p = doc.add_paragraph(); p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space); pf.line_spacing = 1.6
    _bidi(p._p.get_or_add_pPr())
    _rtl_run(p.add_run(iso(text)), bold, size)
    return p

def render_docx(blocks, path, title=None):
    doc = Document()
    for s in doc.sections:
        s.right_margin = s.left_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2.0)
    st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(12.5)
    if title: _para(doc, title, True, 15, WD_ALIGN_PARAGRAPH.CENTER, 12)
    for kind, val in blocks:
        if kind == 'h1':      _para(doc, val, True, 14, WD_ALIGN_PARAGRAPH.CENTER, 10)
        elif kind == 'h2':    _para(doc, val, True, 13, WD_ALIGN_PARAGRAPH.RIGHT, 8)
        elif kind == 'p':     _para(doc, val)
        elif kind == 'li':    _para(doc, "• " + val, space=4)
        elif kind == 'spacer':doc.add_paragraph()
        elif kind == 'table':
            t = doc.add_table(rows=0, cols=len(val[0])); t.style = 'Table Grid'
            tblPr = t._tbl.tblPr; tblPr.append(OxmlElement('w:bidiVisual'))
            for ri, row in enumerate(val):
                cells = t.add_row().cells
                for ci, cell in enumerate(row):
                    cells[ci].text = ''
                    p = cells[ci].paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    _bidi(p._p.get_or_add_pPr())
                    _rtl_run(p.add_run(iso(str(cell))), ri == 0, 11.5)
    doc.save(path)

# ---------- PDF ----------
_CSS = """
@page { size: A4; margin: 2.0cm 2.2cm;
        @bottom-center { content: counter(page);
                         font-family: "Amiri", serif; font-size: 9pt; color:#555; } }
body { font-family: "Amiri","FreeSans",serif; direction: rtl; text-align: justify;
       font-size: 12.5pt; line-height: 1.65; }
h1 { font-size: 15pt; text-align: center; margin: 0 0 12pt; }
h2 { font-size: 13.5pt; text-align: center; margin: 14pt 0 8pt; }
h3 { font-size: 12.5pt; margin: 12pt 0 6pt; }
p  { margin: 0 0 6pt; }
ul { margin: 0 0 6pt; padding-right: 18pt; }
table { width:100%; border-collapse: collapse; direction: rtl; margin: 8pt 0; }
th,td { border: 0.6pt solid #444; padding: 4pt 6pt; font-size: 11.5pt; text-align: right; }
th { background: #eee; font-weight: bold; }
"""
def _esc(t):
    return (iso(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))

def render_pdf(blocks, path, title=None):
    h = ['<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8">',
         f'<style>{_CSS}</style><body>']
    if title: h.append(f"<h1>{_esc(title)}</h1>")
    for kind, val in blocks:
        if kind == 'h1':      h.append(f"<h2>{_esc(val)}</h2>")
        elif kind == 'h2':    h.append(f"<h3>{_esc(val)}</h3>")
        elif kind == 'p':     h.append(f"<p>{_esc(val)}</p>")
        elif kind == 'li':    h.append(f"<ul><li>{_esc(val)}</li></ul>")
        elif kind == 'spacer':h.append('<p>&nbsp;</p>')
        elif kind == 'table':
            h.append('<table>')
            for ri,row in enumerate(val):
                tag = 'th' if ri==0 else 'td'
                h.append('<tr>' + ''.join(f"<{tag}>{_esc(str(c))}</{tag}>" for c in row) + '</tr>')
            h.append('</table>')
    h.append('</body></html>')
    weasyprint.HTML(string=''.join(h)).write_pdf(path)
