"""بوابة فحص المسوّدات قبل الاعتماد — نموذج أولي.

الاستعمال:
    python3 tools/draft_gate.py --case 3.8 scratchpad/munazaa/ishkal_doc.py

تُخرج تقريراً بقسمين:
  [آلي]  ما يمكن إثباته برمجياً — يُرفض عليه
  [بشري] ما يحتاج حكماً قانونياً أو مراجعة مستقلة — يُعرض ولا يُحسم

⚠️ اجتياز البوابة لا يعني أن المسوّدة صحيحة قانوناً.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import legal_checks as L  # noqa: E402

HUMAN_CHECKLIST = [
    "هل كل مادة قانونية مذكورة قُرئت من نصّها الرسمي، ونفاذها اليوم متحقَّق منه؟",
    "هل لكل سند درجة إثبات معلنة (مستند رسمي / كشف مصدَّق / صورة مراسلة / إفادة شفوية)؟",
    "هل راجع الطلبَ من لم يصغه — مراجعة مستقلة بلا سياق المحادثة؟",
    "هل نوع الطلب وحدّ الحقل والمرفقات الإلزامية مؤكَّدة من البوابة لا بالتخمين؟",
    "هل في المسوّدة جملة يقتنصها الخصم؟",
    "هل تُفصح المسوّدة عن أكثر مما يلزم (خصوصية الموكّل)؟",
]


def run(path, case_id, root):
    text = Path(path).read_text(encoding="utf-8")
    guard = L.load_guard(root)
    findings = []

    for fid, phrase, owner in L.find_cross_case(text, guard, case_id):
        findings.append(("❌", f"إحالة لقضية أخرى: {fid} «{phrase}» تخصّ {owner}"))

    for bid, pattern, reason in L.find_banned_numbers(text, guard):
        findings.append(("❌", f"رقم محظور: {bid} «{pattern}» — {reason}"))

    unsourced = L.find_unsourced_numbers(text)
    for line_no, snippet in unsourced:
        findings.append(("⚠️", f"رقم/تاريخ بلا مصدر في السطر {line_no}: {snippet}"))

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--case", required=True, help="رقم قسم القضية، مثل 3.8")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    findings = run(args.draft, args.case, root)

    blocking = [f for f in findings if f[0] == "❌"]
    warnings = [f for f in findings if f[0] == "⚠️"]

    print(f"\n=== بوابة المسوّدات — {args.draft} (قضية {args.case}) ===\n")
    print("[آلي — مانع]")
    print("  لا شيء." if not blocking else "")
    for _, msg in blocking:
        print(f"  ❌ {msg}")

    print(f"\n[آلي — تنبيه] {len(warnings)} بند")
    for _, msg in warnings[:10]:
        print(f"  ⚠️ {msg}")
    if len(warnings) > 10:
        print(f"  … و{len(warnings) - 10} غيرها")

    print("\n[بشري — لا يُحسم آلياً]")
    for item in HUMAN_CHECKLIST:
        print(f"  ☐ {item}")

    print("\n⚠️ اجتياز الفحص الآلي لا يعني صحة المسوّدة قانوناً.\n")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
