"""CLI: python -m src.do.run --intent intent.json"""
import argparse, json, sys
from . import do, DoError
def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument("--intent", required=True); p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    intent = json.load(open(a.intent, encoding="utf-8"))
    try:
        paths = do(intent, a.out) if a.out else do(intent)
    except DoError as e:
        print(f"ERROR: {e}", file=sys.stderr); return 2
    for x in paths: print(x)
    return 0
if __name__ == "__main__":
    sys.exit(main())
