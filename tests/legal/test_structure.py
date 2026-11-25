"""بنية ملف القضايا: لا عنوان H1 دخيل، وترويسة غير متأخرة."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

import legal_checks as L  # noqa: E402


def test_detector_catches_stray_h1():
    bad = "# العنوان\n\nنص\n\n# عنوان دخيل\n"
    assert any("دخيل" in p for p in L.check_structure(bad))


def test_case_file_structure(case_text):
    problems = L.check_structure(case_text)
    assert not problems, "عيوب بنيوية: " + " | ".join(problems)


def test_future_deadline_passing_does_not_break_the_guard():
    """موعدٌ مستقبليّ يصير ماضياً لا يُسقط الفحص — خلل رُصد 25/11/2026.

    كان القياس على `date.today()`، فكلّما مرّ موعدٌ مذكورٌ في الملف (مهلة،
    جلسة) سقط الفحص بلا أي تعديل، وCI يسقط من تلقائه كل ستّ ساعات.
    والقياس الآن على تاريخ آخر كتابة فعلية في الملف.
    """
    نصّ = "# س\n\n> آخر تحديث: 17/11/2026\n\nمهلة السداد حتى 24/11/2026.\n"
    assert L.check_structure(نصّ, ref_date=date(2026, 11, 17)) == []
    # وما وُجد الحارس له يبقى قائماً: واقعة مسجَّلة أحدث من الترويسة
    واقعة = "# س\n\n> آخر تحديث: 28/10/2026\n\nوفي 03/11/2026 صدر القرار.\n"
    assert any("أقدم من أحدث" in p for p in L.check_structure(واقعة, ref_date=date(2026, 11, 17)))
