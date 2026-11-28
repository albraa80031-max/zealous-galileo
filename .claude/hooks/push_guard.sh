#!/usr/bin/env bash
# PreToolUse(Bash): يمنع دفع مستندات قضائية حسّاسة إلى GitHub بلا موافقة صريحة.
# لا يمسّ السجل، ولا يمنع الدفع غير الحسّاس.
set -uo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')"

# لا شأن للحارس بغير git push
printf '%s' "$cmd" | grep -qE '(^|[;&|[:space:]])git[[:space:]]+push' || exit 0

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$root" || exit 0

# موافقة صريحة لهذه الدفعة فقط
if [ "${LEGAL_PUSH_APPROVED:-}" = "1" ]; then
  exit 0
fi

SENSITIVE_RE='^(\.claude/legal/|scratchpad/)'

upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
if [ -n "$upstream" ]; then
  files="$(git diff --name-only "$upstream"..HEAD 2>/dev/null || true)"
else
  files="$(git diff --name-only HEAD~1..HEAD 2>/dev/null || true)"
fi
files="$files
$(git diff --cached --name-only 2>/dev/null || true)
$(git diff --name-only 2>/dev/null || true)"

hits="$(printf '%s\n' "$files" | grep -E "$SENSITIVE_RE" | sort -u | head -12)"
[ -z "$hits" ] && exit 0

reason="هذه الدفعة تتضمّن مستندات قضائية أو ملفات الموكّل الحسّاسة:
${hits}

قاعدة الخصوصية: لا يُدفع ما يمسّ .claude/legal/ أو scratchpad/ إلى GitHub قبل موافقة الموكّل الصريحة على هذه الدفعة بعينها.

اعرض على الموكّل: ما الملفات، وماذا تغيّر فيها، ولماذا تُدفع الآن — ثم انتظر موافقته. موافقة سابقة على دفعة أخرى لا تكفي."

jq -n --arg r "$reason" \
  '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"ask",permissionDecisionReason:$r}}'
exit 0
