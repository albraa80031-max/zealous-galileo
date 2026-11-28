"""قارئ أقسام ملف القضايا — يمنع القراءة الجزئية التي تقطع الأقسام الفرعية.

نشأ من خطأ 27/10/2026: قُرئ القسم 3.3 بـ
    sed -n '/^### 3.3 /,/^#### /p'
فتوقّف عند أول عنوان فرعي، وبقي القرار الحاسم (المهلة حتى 24/11/2026)
خارج المقروء — فبُني جواب خاطئ على قراءة ناقصة.

الاستعمال:
    python3 tools/case_section.py --list
    python3 tools/case_section.py --section 3.3        # ومعه 3.3.1 و3.3.2
    python3 tools/case_section.py --find "24/11"
"""

import argparse
import re
import sys
from pathlib import Path

CASE_FILE = Path(".claude/legal/CASE_FILE.md")
HEADING = re.compile(r"^(#{2,6})\s+(.*)$")
# رقم القسم في أول العنوان، مثل «3.3» أو «3.3.1» أو «5.1»
NUMBER = re.compile(r"^(\d+(?:\.\d+)*)\.?\s")   # يقبل «3.3 » و«1. » معاً


def _headings(lines):
    out = []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        num = NUMBER.match(title)
        out.append((i, level, num.group(1) if num else None, title))
    return out


def resolve(root, section):
    path = Path(root) / CASE_FILE
    lines = path.read_text(encoding="utf-8").splitlines()
    heads = _headings(lines)

    start = level = None
    for i, lvl, num, _ in heads:
        if num == section:
            start, level = i, lvl
            break
    if start is None:
        return None, None, lines

    # النهاية = أول عنوان بمستوى **مساوٍ أو أعلى** — فتدخل الأقسام الفرعية
    end = len(lines)
    for i, lvl, _, _ in heads:
        if i > start and lvl <= level:
            end = i
            break
    return start, end, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", help="رقم القسم، مثل 3.3")
    ap.add_argument("--list", action="store_true", help="اعرض الأقسام ومداها")
    ap.add_argument("--find", help="ابحث عن نصّ وأظهر القسم الذي يقع فيه")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    path = Path(args.root) / CASE_FILE
    if not path.exists():
        print(f"⛔ {CASE_FILE} غير موجود", file=sys.stderr)
        return 2
    lines = path.read_text(encoding="utf-8").splitlines()
    heads = _headings(lines)

    if args.list:
        for i, lvl, num, title in heads:
            if num:
                s, e, _ = resolve(args.root, num)
                print(f"{num:<8} سطر {s+1:>5}–{e:<5} ({e-s:>3} سطراً)  {'  '*(lvl-3)}{title}")
        return 0

    if args.find:
        hits = [i for i, l in enumerate(lines) if args.find in l]
        if not hits:
            print("لا نتائج")
            return 1
        for i in hits:
            owner = None
            for hi, _, num, title in heads:
                if hi <= i and num:
                    owner = (num, title)
            where = f"{owner[0]} — {owner[1]}" if owner else "قبل أي قسم"
            print(f"سطر {i+1} · القسم {where}\n    {lines[i].strip()[:160]}\n")
        return 0

    if not args.section:
        ap.error("مرّر --section أو --list أو --find")

    start, end, lines = resolve(args.root, args.section)
    if start is None:
        print(f"⛔ لا قسم برقم {args.section} — جرّب --list", file=sys.stderr)
        return 2
    print("\n".join(lines[start:end]))
    print(f"\n— [{args.section}: الأسطر {start+1}–{end}، شاملةً أقسامه الفرعية]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
