#!/usr/bin/env bash
# AI Mouse — one-shot demo (no API key, never sends email)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  . .venv/bin/activate
  pip install -q -r requirements.txt
else
  # shellcheck disable=SC1091
  . .venv/bin/activate
fi

echo "=== 1/3 email draft (auto_send=false) ==="
python -m src.pipeline.run --image tests/sample.png --transcript "回复并接受" --mode do --do
echo
echo "=== 2/3 chart PNG ==="
python -m src.pipeline.run --image tests/sample.png --transcript "把 units 做成图表" --mode do --do
echo
echo "=== 3/3 expense local record ==="
python -m src.pipeline.run --image tests/sample.png --transcript "归档报销" --mode do --do
echo
echo "Done. Artifacts:"
ls -1 out/drafts/reply_*.md 2>/dev/null | tail -1
ls -1 out/charts/chart_*.png 2>/dev/null | tail -1
echo "out/expenses.json"
