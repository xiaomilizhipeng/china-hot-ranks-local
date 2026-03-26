#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$ROOT/briefs"
SCRIPT="$ROOT/skill/china-hot-ranks-local/scripts/hot_ranks_local.py"
TODAY="$(TZ=Asia/Shanghai date +%F)"
OUT_FILE="$OUT_DIR/${TODAY}-hot-ranks.md"
TMP_FILE="$(mktemp)"
mkdir -p "$OUT_DIR"
python3 "$SCRIPT" all --limit 10 > "$TMP_FILE"
{
  echo "# 每日热榜"
  echo
  echo "生成时间：$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S %Z')"
  echo
  cat "$TMP_FILE"
} > "$OUT_FILE"
cat "$OUT_FILE"
rm -f "$TMP_FILE"
