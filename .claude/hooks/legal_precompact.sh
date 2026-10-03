#!/usr/bin/env bash
# PreCompact: the conversation is about to be summarised, so anything not yet
# written to CASE_FILE.md is about to be lost. Remind before that happens.
set -uo pipefail

payload="$(cat)"
sid="$(printf '%s' "$payload" | jq -r '.session_id // "unknown"')"
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
state_dir="${HOME}/.claude/legal-hook-state"
base_file="$state_dir/${sid}.base"
case_file="$root/.claude/legal/CASE_FILE.md"

now="$(sha1sum "$case_file" 2>/dev/null | awk '{print $1}')"
base="$(cat "$base_file" 2>/dev/null || true)"

if [ -n "$base" ] && [ "$now" = "$base" ]; then
  state="CASE_FILE.md has NOT been written to in this session."
else
  state="CASE_FILE.md was already written to in this session; only add what is still missing."
fi

msg="تنبيه: السياق على وشك التلخيص — حدّث ملف القضايا الآن (/legal-update) قبل أن يضيع."
ctx="Context is about to be compacted. ${state} Before continuing, run the /legal-update skill: record in .claude/legal/CASE_FILE.md every development from this session (decisions, filed requests, documents received, payments, corrected errors, open gaps), then commit and push it. Follow CLAUDE.md: never record the account password. This is the only durable memory this agent has — unwritten facts are lost at compaction."

jq -n --arg m "$msg" --arg c "$ctx" \
  '{systemMessage:$m, hookSpecificOutput:{hookEventName:"PreCompact", additionalContext:$c}}'
exit 0
