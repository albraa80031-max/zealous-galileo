"""المُصيِّر لا يُسقط كتلة بصمت — ببيانات تجريبية لا بقضية حقيقية."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

pymupdf = pytest.importorskip("pymupdf")
pytest.importorskip("weasyprint")
pytest.importorskip("docx")

from arabic_render import render_docx, render_pdf  # noqa: E402

BLOCKS = [
    ("h1", "عنوان المستند التجريبي"),
    ("h2", "عنوان فرعي"),
    ("p", "فقرة اختبار بتاريخ 05/08/2026 ومبلغ 1,234 درهماً."),
    ("li", "بند أول في قائمة"),
    ("li", "بند ثانٍ في قائمة"),
    ("spacer", None),
    (
        "table",
        [
            ["العمود الأول", "العمود الثاني"],
            ["قيمة أولى", "9,876"],
            ["قيمة ثانية", "11/07/2026"],
        ],
    ),
]

MARKERS = [
    "عنوان المستند التجريبي",
    "عنوان فرعي",
    "فقرة اختبار",
    "بند أول",
    "بند ثانٍ",
    "العمود الأول",
    "قيمة ثانية",
]


def test_pdf_keeps_every_block(tmp_path):
    out = tmp_path / "sample.pdf"
    render_pdf(BLOCKS, str(out))
    doc = pymupdf.open(out)
    text = "".join(page.get_text() for page in doc)
    missing = [m for m in MARKERS if m not in text]
    assert not missing, f"كتل سقطت من الـPDF: {missing}"


def test_docx_keeps_every_block(tmp_path):
    docx = pytest.importorskip("docx")
    out = tmp_path / "sample.docx"
    render_docx(BLOCKS, str(out))
    doc = docx.Document(str(out))
    text = "\n".join(p.text for p in doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            text += "\n" + "\t".join(c.text for c in row.cells)
    missing = [m for m in MARKERS if m not in text]
    assert not missing, f"كتل سقطت من الـDOCX: {missing}"


def test_unsupported_block_is_dropped_silently(tmp_path):
    """توثيق السلوك الخطر: اسم كتلة غير مدعوم يختفي بلا إنذار."""
    out = tmp_path / "bad.pdf"
    render_pdf([("h1", "عنوان"), ("note", "هذا النص لن يظهر")], str(out))
    text = "".join(p.get_text() for p in pymupdf.open(out))
    assert "عنوان" in text
    assert "لن يظهر" not in text
