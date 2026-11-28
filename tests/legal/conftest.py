"""مسارات مشتركة لاختبارات طبقة العمل القانوني.

⚠️ **بيانات القضايا لا تُدفع إلى GitHub** (قاعدة CLAUDE.md رقم 9). فملفّا
`contamination_guard.json` و`REVIEW_LOG.md` يبقيان محليَّين، ونسخة
`CASE_FILE.md` في المستودع قد تكون أقدم من المحلية.

ولذلك تُعامَل **وجود `contamination_guard.json`** علامةً على أن الطبقة
القانونية الخاصة حاضرة ومحدَّثة. فإن غاب، تُتجاوَز (skip) الاختبارات
المعتمدة على بيانات القضايا، وتبقى اختبارات الأدوات والمراجع والمُصيِّر
عاملة. فالتجاوز هنا **ليس نجاحاً** — هو إعلان بأن البيانات غير متاحة.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
LEGAL = ROOT / ".claude" / "legal"
GUARD = LEGAL / "contamination_guard.json"
CASE = LEGAL / "CASE_FILE.md"

SKIP_REASON = "بيانات القضايا الخاصة غير متاحة في هذه البيئة (contamination_guard.json مفقود) — لا تُدفع إلى GitHub"


def _require_private_data():
    if not GUARD.exists():
        pytest.skip(SKIP_REASON)


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture(scope="session")
def case_text():
    _require_private_data()
    if not CASE.exists():
        pytest.skip("CASE_FILE.md غير موجود")
    return CASE.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def guard():
    _require_private_data()
    return json.loads(GUARD.read_text(encoding="utf-8"))
