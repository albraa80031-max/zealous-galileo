"""واقعة قضية لا تظهر في مسوّدة قضية أخرى، ورقم محظور لا يدخل مستنداً."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

import legal_checks as L  # noqa: E402

# سكربتات بناء مستندات 6181/2026 — قضيتها 3.8
DRAFTS_6181 = [
    "scratchpad/munazaa/ishkal.py",
    "scratchpad/munazaa/ishkal_doc.py",
    "scratchpad/munazaa/daawa.py",
    "scratchpad/munazaa/hafiza/cover.py",
]

WITHDRAWAL_MARKERS = ("⛔", "سُحب", "سحِب", "تخصّ", "لا وجود", "خطأ")


def test_detector_catches_a_cross_case_phrase(guard):
    draft = "ونصّ على 35 يوم من أي تاريخ لأي تاريخ."
    assert L.find_cross_case(draft, guard, case_id="3.8")


def test_detector_ignores_phrase_in_its_own_case(guard):
    draft = "ونصّ على 35 يوم من أي تاريخ لأي تاريخ."
    assert not L.find_cross_case(draft, guard, case_id="3.6.1")


def test_6181_drafts_are_clean(root, guard):
    problems = []
    for rel in DRAFTS_6181:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for fid, phrase, owner in L.find_cross_case(text, guard, case_id="3.8"):
            problems.append(f"{rel}: {fid} «{phrase}» تخصّ {owner}")
        for bid, pattern, reason in L.find_banned_numbers(text, guard):
            problems.append(f"{rel}: {bid} «{pattern}» — {reason}")
    assert not problems, "تلوث في مسوّدات 6181:\n" + "\n".join(problems)


def _case_section(line, current):
    """يتتبّع قسم القضية الجاري (### 3.x أو #### 3.x.y) ويُلغيه عند قسم أعلى."""
    import re

    m = re.match(r"^#{3,4} (3(?:\.\d+)+)", line)
    if m:
        return m.group(1)
    if re.match(r"^## ", line):
        return None
    return current


def test_case_file_cross_refs_are_marked_as_withdrawn(case_text, guard):
    """واقعة قضية لا تظهر داخل قسم قضية أخرى إلا موسومة بسحب أو خطأ.

    الأقسام غير القضائية (السجلات المالية، الأخطاء، المراجع) محايدة.
    """
    unmarked = []
    section = None
    for i, line in enumerate(case_text.split("\n"), 1):
        section = _case_section(line, section)
        if section is None:
            continue
        for fact in guard["facts"]:
            if fact["phrase"] not in line:
                continue
            if section.startswith(fact["owner"]) or fact["owner"].startswith(section):
                continue
            if any(m in line for m in WITHDRAWAL_MARKERS):
                continue
            unmarked.append(f"سطر {i} (قسم {section}): «{fact['phrase']}» تخصّ {fact['owner']}")
    assert not unmarked, "عبارة قضية أخرى بلا وسم سحب:\n" + "\n".join(unmarked)


# ───────── ت-3: تثبيت الواقعة التاريخية وحدود الكاشف ─────────
#
# حدود `find_cross_case` — مُختبَرة أدناه لا مُدّعاة:
#   • تطابق نصّي للعبارات المسجَّلة في `contamination_guard.json` وحدها.
#     واقعة غير مسجَّلة = غير مكشوفة. صياغة جديدة لعبارة مسجَّلة = غير مكشوفة.
#   • لا يقرأ سياق السطر: عبارة موسومة بالسحب تُلتقط كأنها تلوث
#     (الوسم يُراعى في `test_case_file_cross_refs_are_marked_as_withdrawn` فقط).
#   • لا يكشف نقل رقم أو تاريخ أو طرف بين قضيتين إن لم يُسجَّل.
# فنجاحه يعني «لا تلوث مسجَّل مكشوف» — لا «لا اختلاط بين القضايا».

HISTORIC_CONTAMINATION = [
    ("5433efe", "scratchpad/munazaa/ishkal.py"),
    ("5433efe", "scratchpad/munazaa/daawa.py"),
]


def test_detector_catches_the_real_historical_wording(guard):
    """التلوث الفعلي كُتب بالحروف لا بالرقم — والرقم وحده كان سيمرّ."""
    actual = "واتفق الطرفان على مدة خمسة وثلاثون يوماً للإيجار."
    assert L.find_cross_case(actual, guard, case_id="3.8")
    assert "35" not in actual


def test_detector_catches_each_registered_variant(guard):
    fact = next(f for f in guard["facts"] if f["id"] == "C-001")
    for variant in L.fact_variants(fact):
        assert L.find_cross_case(
            f"نصّ العقد يذكر {variant} صراحةً.", guard, case_id="3.8"
        ), f"متغيّر غير مكشوف: {variant}"


def test_clean_draft_is_not_flagged(guard):
    """سلبي: نصّ 6181 الحقيقي بلا عبارات القضية الأخرى يمرّ."""
    draft = (
        "استلم الموكّل المركبة بتاريخ 26/08/2026 وسدّد 3,495 درهماً "
        "بموجب كشف بطاقة نون وان فيزا."
    )
    assert not L.find_cross_case(draft, guard, case_id="3.8")
    assert not L.find_banned_numbers(draft, guard)


@pytest.mark.parametrize("rev,path", HISTORIC_CONTAMINATION)
def test_historical_contaminated_blob_is_detected(guard, rev, path):
    """تثبيت انحدار: نسخة 5433efe الملوّثة يجب أن تُرصد لو عادت.

    يُتجاوز الاختبار إن لم يتوفر تاريخ Git محلياً (نسخة سطحية).
    """
    import subprocess

    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        pytest.skip(f"النسخة {rev}:{path} غير متاحة محلياً")
    hits = L.find_cross_case(r.stdout, guard, case_id="3.8")
    assert hits, f"الكاشف لم يرصد التلوث الموثَّق في {rev}:{path}"
    assert any(fid == "C-001" for fid, _, _ in hits)


def test_detector_is_blind_to_withdrawal_markers(guard):
    """حدّ موثَّق: الكاشف نصّي، فيُنذر على عبارة مسحوبة صراحةً.

    مقصود — في مسوّدة قضائية لا يُقبل ذكر العبارة أصلاً. والاستثناء
    المسموح لملف القضايا محصور في فحص الوسم المستقل.
    """
    withdrawn = "⛔ سُحب السند: «خمسة وثلاثون يوماً» تخصّ مكتب التأجير السابق."
    assert L.find_cross_case(withdrawn, guard, case_id="3.8")
