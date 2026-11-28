"""تعليمات الوكلاء لا تشير إلى مسار غير موجود ولا إلى كتلة غير مدعومة."""

import re

SUPPORTED = {"h1", "h2", "p", "li", "spacer", "pagebreak", "table"}
# مسار فعلي فقط: يحوي "/" — لا اسم ملف مجرّد ورد في نصّ
PATH_RE = re.compile(r"`([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.(?:py|md|json|sh))`")
# اسم كتلة معلن — يلتقط الصيغتين: `('h1', …)` و `("h1"|"sub"|…)`
# حدّ معروف: صيغة ثالثة (بلا علامة تنصيص، أو داخل جدول بلا أقواس) تمرّ.
BLOCK_NAME_RE = re.compile(r"""[`(|]\s*['"]([a-z][a-z0-9]{0,8})['"]""")


def _instruction_files(root):
    files = [root / "CLAUDE.md"]
    files += sorted((root / ".claude" / "agents").glob("*.md"))
    files += sorted((root / ".claude" / "skills").rglob("SKILL.md"))
    return [f for f in files if f.exists()]


def test_every_referenced_path_exists(root):
    missing = []
    for f in _instruction_files(root):
        for m in PATH_RE.findall(f.read_text(encoding="utf-8")):
            if m.startswith(("http", "pay.")) or "*" in m:
                continue
            if not (root / m).exists():
                missing.append(f"{f.name} -> {m}")
    assert not missing, "مسارات مذكورة وغير موجودة: " + " | ".join(missing)


def test_renderer_block_names_match_implementation(root):
    src = (root / "tools" / "arabic_render.py").read_text(encoding="utf-8")
    implemented = set(re.findall(r"kind == '([a-z0-9]+)'", src))
    assert implemented == SUPPORTED, f"المُصيِّر يقبل {implemented}"

    agent = (root / ".claude" / "agents" / "legal-uae.md").read_text(encoding="utf-8")
    declared = set(BLOCK_NAME_RE.findall(agent))
    unsupported = declared - SUPPORTED
    assert not unsupported, f"كتل معلنة غير مدعومة: {unsupported}"
