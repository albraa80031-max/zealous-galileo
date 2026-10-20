"""بنية ملف القضايا: لا عنوان H1 دخيل، وترويسة غير متأخرة."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

import legal_checks as L  # noqa: E402


def test_detector_catches_stray_h1():
    bad = "# العنوان\n\nنص\n\n# عنوان دخيل\n"
    assert any("دخيل" in p for p in L.check_structure(bad))


def test_case_file_structure(case_text):
    problems = L.check_structure(case_text)
    assert not problems, "عيوب بنيوية: " + " | ".join(problems)
