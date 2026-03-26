#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/xp/openclaw"
OUT_DIR="$ROOT/briefs"
HOT_SCRIPT="$ROOT/skills/china-hot-ranks-local/scripts/hot_ranks_local.py"
TOPIC_SCRIPT="$ROOT/skills/wechat-topic-selector/scripts/topic_selector.py"
TOPIC_DIRECTION="${WECHAT_TOPIC_DIRECTION:-AI 技术}"
TODAY="$(TZ=Asia/Shanghai date +%F)"
OUT_FILE="$OUT_DIR/${TODAY}-hot-ranks.md"
TOPIC_JSON="$OUT_DIR/${TODAY}-topic-results.json"
TMP_HOT="$(mktemp)"
TMP_TOPIC="$(mktemp)"

mkdir -p "$OUT_DIR"

python3 "$HOT_SCRIPT" all --limit 10 > "$TMP_HOT"
python3 "$TOPIC_SCRIPT" -d "$TOPIC_DIRECTION" -p github,csdn,bilibili,baidu -n 3 --quiet --output-json "$TOPIC_JSON" > "$TMP_TOPIC"

{
  echo "# 每日热榜与公众号选题"
  echo
  echo "生成时间：$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "选题方向：$TOPIC_DIRECTION"
  echo
  cat "$TMP_HOT"
  echo
  echo "============================================================"
  echo
  cat "$TMP_TOPIC"
} > "$OUT_FILE"

cat "$OUT_FILE"
rm -f "$TMP_HOT" "$TMP_TOPIC"
