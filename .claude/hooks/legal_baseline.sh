#!/usr/bin/env bash
# SessionStart: record the CASE_FILE.md fingerprint so the Stop hook can tell
# whether this session ever wrote to the case file.
set -uo pipefail

payload="$(cat)"
sid="$(printf '%s' "$payload" | jq -r '.session_id // "unknown"')"
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
state_dir="${HOME}/.claude/legal-hook-state"

mkdir -p "$state_dir"

# Write the baseline ONCE. A resume of the same conversation must not
# re-baseline against an already-updated file, or the work done before the
# resume looks like work never recorded. The sentinel is never cleared here
# for the same reason: "once per session" has to survive a resume.
if [ ! -s "$state_dir/${sid}.base" ]; then
  sha1sum "$root/.claude/legal/CASE_FILE.md" 2>/dev/null | awk '{print $1}' \
    > "$state_dir/${sid}.base" || true
fi
exit 0
