#!/usr/bin/env bash
# Stop: if this session did legal work but never wrote to CASE_FILE.md, send
# Claude back to run /legal-update. Fires at most once per session.
set -uo pipefail

payload="$(cat)"
sid="$(printf '%s' "$payload" | jq -r '.session_id // "unknown"')"
transcript="$(printf '%s' "$payload" | jq -r '.transcript_path // ""')"
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
state_dir="${HOME}/.claude/legal-hook-state"
base_file="$state_dir/${sid}.base"
nudge_file="$state_dir/${sid}.nudged"
case_file="$root/.claude/legal/CASE_FILE.md"
min_lines="${LEGAL_HOOK_MIN_TURNS:-40}"

# Gate 1 — never nudge twice in one session.
[ -f "$nudge_file" ] && exit 0

# Gate 2 — need a baseline to compare against.
base="$(cat "$base_file" 2>/dev/null || true)"
[ -z "$base" ] && exit 0

# Gate 3 — the case file already changed: nothing to chase.
now="$(sha1sum "$case_file" 2>/dev/null | awk '{print $1}')"
[ "$now" != "$base" ] && exit 0

# Gate 4 — only a session of real length is worth interrupting.
[ -z "$transcript" ] || [ ! -f "$transcript" ] && exit 0
lines="$(wc -l < "$transcript" 2>/dev/null || echo 0)"
[ "$lines" -lt "$min_lines" ] && exit 0

# Gate 5 — only when the session actually touched the case files.
if ! grep -qE 'CASE_FILE|279/2026|161/2025|6181|3336/2026|1529/2025|قضي|محكم|تنفيذ|الخبير' \
     "$transcript" 2>/dev/null; then
  exit 0
fi

mkdir -p "$state_dir"
: > "$nudge_file"

reason="This session did work on the legal files but .claude/legal/CASE_FILE.md was never written to, and the conversation is the only other place that work exists. Before ending: run the /legal-update skill — record every development from this session (decisions, filed requests, documents received, payments, corrected errors, open gaps) in .claude/legal/CASE_FILE.md, then commit and push to the designated branch. Follow CLAUDE.md: never record the account password. If, after reading the session back, there is genuinely nothing new to record, say so in one line and stop. This reminder fires only once per session."

jq -n --arg r "$reason" \
  '{decision:"block", reason:$r, systemMessage:"ملف القضايا لم يُحدَّث في هذه الجلسة — تشغيل /legal-update."}'
exit 0
