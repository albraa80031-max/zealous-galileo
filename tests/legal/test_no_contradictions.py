"""ادعاءان متنافيان لا يبقيان قائمين معاً في ملف القضايا."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

import legal_checks as L  # noqa: E402

SYNTHETIC_BAD = """# ملف تجريبي

## قسم أ

التأمين في هذا المسار لا يلزم إطلاقاً.

## قسم ب

التأمين في هذا المسار نعم يلزم.
"""


def test_detector_catches_a_known_contradiction():
    """برهان أن الكاشف يعمل — على نصّ تجريبي لا على ملف قضية."""
    assert L.find_contradictions(SYNTHETIC_BAD)


def test_quarantine_silences_a_block():
    """كتلة تحمل ⛔ لا يُحتجّ بما فيها."""
    quarantined = SYNTHETIC_BAD.replace("## قسم أ", "## قسم أ\n\n> ⛔ موقوف")
    assert not L.find_contradictions(quarantined)


def test_case_file_has_no_live_contradictions(case_text):
    found = L.find_contradictions(case_text)
    assert not found, "ادعاءات متنافية قائمة: " + str(found)
