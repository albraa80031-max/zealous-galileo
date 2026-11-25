"""فحوص آلية لطبقة العمل القانوني.

⚠️ حدود هذه الأداة — تُقرأ قبل الاعتماد عليها:

تكشف آلياً (قابل للبرمجة):
  • رقم أو تاريخ في مسوّدة بلا مصدر مذكور قربه
  • ادعاءان متنافيان قائمان معاً في ملف القضايا
  • إحالة إلى واقعة مسجَّلة لقضية أخرى
  • مادة قانونية غير مقيَّدة في سجل التشريعات المتحقَّق منه
  • عيوب بنيوية: ترتيب العناوين، عنوان دخيل، تاريخ ترويسة متأخر

لا تكشف ولا تدّعي (يحتاج حكماً قانونياً بشرياً أو مراجعة مستقلة):
  • صحة تفسير النص القانوني أو نفاذه اليوم
  • كفاية السند أو وزنه الإثباتي
  • ملاءمة الطلب للإجراء المتاح في البوابة
  • سلامة الاستراتيجية أو توقيت التقديم

نجاح كل الفحوص يعني «لا عيب آلي مكتشف» — ولا يعني أن المسوّدة صحيحة قانوناً.
"""

import json
import re
import subprocess
from datetime import date
from pathlib import Path

EXCLUDED_SECTIONS = ("أخطاء وقعت",)

CONTRADICTION_PAIRS = [
    ("التأمين: لا يلزم مقابل يلزم", r"التأمين[^\n]{0,40}لا يلزم", r"التأمين[^\n]{0,40}نعم يلزم"),
    ("نسبة المخاطرة: 1:10 مقابل 1:2", r"1 إلى 10|1 : 10", r"≈ 1 : 2"),
]

# علامات تدل على أن الرقم مسنَد لمصدر في السطر نفسه
SOURCE_MARKERS = (
    "مرجع",
    "الطلب",
    "إيصال",
    "ص.",
    "صفحة",
    "كشف",
    "التقرير",
    "القرار",
    "المادة",
    "م.",
    "الإخطار",
    "الصيغة",
    "حساب",
    "IBAN",
    "AE",
)

MONEY = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b")


def _as_date(s):
    try:
        dd, mm, yy = (int(x) for x in s.split("/"))
        return date(yy, mm, dd)
    except ValueError:
        return None


DATE = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")


def load_guard(root):
    path = Path(root) / ".claude" / "legal" / "contamination_guard.json"
    return json.loads(path.read_text(encoding="utf-8"))


def blocks(text):
    """(عنوان الكتلة، رقم أول سطر، أسطر الكتلة)."""
    lines = text.split("\n")
    heads = [i for i, ln in enumerate(lines) if ln.startswith("#")]
    heads.append(len(lines))
    out = []
    for j in range(len(heads) - 1):
        start, end = heads[j], heads[j + 1]
        out.append((lines[start], start + 1, lines[start:end]))
    return out


def live_hits(text, pattern):
    """الأسطر المطابقة في كتل غير موقوفة بلافتة ⛔ وغير مستثناة."""
    hits = []
    for title, first, body in blocks(text):
        if any(x in title for x in EXCLUDED_SECTIONS):
            continue
        if any("⛔" in ln for ln in body):
            continue
        for k, ln in enumerate(body):
            if "~~" in ln or "⛔" in ln:
                continue
            if re.search(pattern, ln):
                hits.append(first + k)
    return hits


def find_contradictions(text, pairs=None):
    pairs = pairs or CONTRADICTION_PAIRS
    found = []
    for name, left, right in pairs:
        a = set(live_hits(text, left))
        b = set(live_hits(text, right))
        if a and b and (a - b) and (b - a):
            found.append((name, sorted(a), sorted(b)))
    return found


def find_unsourced_numbers(draft_text, window=2):
    """أرقام مالية أو تواريخ لا تحمل علامة مصدر في محيطها.

    ⚠️ كاشف تقريبي عالي الحساسية ومنخفض الدقة — مخرجه **تنبيه لا منع**.
    وجود علامة مصدر لا يثبت صحتها؛ غيابها لا يثبت انعدامها.
    """
    lines = draft_text.split("\n")
    out = []
    for i, ln in enumerate(lines, 1):
        if not (MONEY.search(ln) or DATE.search(ln)):
            continue
        lo = max(0, i - 1 - window)
        hi = min(len(lines), i + window)
        context = "\n".join(lines[lo:hi])
        if any(m in context for m in SOURCE_MARKERS):
            continue
        out.append((i, ln.strip()[:90]))
    return out


def fact_variants(fact):
    """كل صياغات الواقعة — الرقم والحروف معاً."""
    return [fact["phrase"]] + list(fact.get("phrase_variants", []))


def find_cross_case(draft_text, guard, case_id):
    """عبارات مسجَّلة لقضية أخرى ظهرت في مسوّدة هذه القضية."""
    out = []
    for fact in guard["facts"]:
        if fact["owner"] == case_id:
            continue
        for variant in fact_variants(fact):
            if variant in draft_text:
                out.append((fact["id"], variant, fact["owner_name"]))
                break
    return out


def find_banned_numbers(draft_text, guard):
    out = []
    for item in guard["unsourced_numbers"]:
        if item["pattern"] in draft_text:
            out.append((item["id"], item["pattern"], item["reason"]))
    return out


CASE_FILE = Path(__file__).resolve().parent.parent / ".claude" / "legal" / "CASE_FILE.md"


def _last_write_date(path=CASE_FILE):
    """تاريخ آخر كتابة فعلية في الملف، من git. ويسقط إلى اليوم إن تعذّر."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            capture_output=True, text=True, timeout=10,
            cwd=str(Path(__file__).resolve().parent.parent),
        ).stdout.strip()
        y, m, d = (int(x) for x in out.split("-"))
        return date(y, m, d)
    except Exception:
        return date.today()


def check_structure(text, ref_date=None):
    """عيوب بنيوية في ملف القضايا.

    ⚠️ `ref_date` هو التاريخ الذي يُقاس عليه «الماضي» — وافتراضه **تاريخ آخر
    كتابة في الملف**، لا اليوم. ونشأ هذا من خلل رُصد 25/11/2026: كان القياس
    على `date.today()`، فكلّما مرّ تاريخُ موعدٍ مستقبليٍّ مذكورٍ في الملف
    (مهلة، جلسة) صار «ماضياً» وسقط الفحص **بلا أي تعديل** — وCI يسقط من
    تلقائه كل ستّ ساعات. والموعد المستقبلي ليس تطوّراً يستوجب تحديث الترويسة.
    """
    problems = []
    lines = text.split("\n")

    for i, ln in enumerate(lines[1:], 2):
        if re.match(r"^# [^#]", ln):
            problems.append(f"عنوان H1 دخيل في السطر {i}: {ln.strip()[:60]}")

    header = next((ln for ln in lines[:8] if "آخر تحديث" in ln), "")
    hdr = DATE.search(header)
    ref = ref_date or _last_write_date()
    past = [d for d in DATE.findall(text) if _as_date(d) and _as_date(d) <= ref]
    if hdr and past:
        newest = max(past, key=_as_date)
        if _as_date(hdr.group()) < _as_date(newest):
            problems.append(f"تاريخ الترويسة {hdr.group()} أقدم من أحدث تاريخ ماضٍ {newest}")
    return problems
