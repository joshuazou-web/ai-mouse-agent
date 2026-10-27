"""CLI: python -m src.pipeline.run [--image path] [--transcript text] [--mode point|speak|do]
              [--entry point|capture_region] [--do]

--entry capture_region = Ask-key bypass (框选/区域截图)，与 point 并列进入同一 Do；不是第四卖点。
"""
import argparse, json, sys
from .capture import capture, VALID_ENTRIES
from .understand import understand

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--image")
    p.add_argument("--transcript")
    p.add_argument("--mode", choices=["point", "speak", "do"], default="point")
    p.add_argument("--entry", choices=list(VALID_ENTRIES), default="point",
                   help="point (default) or capture_region (Ask bypass)")
    p.add_argument("--do", action="store_true", help="run Do layer after understand (never sends)")
    a = p.parse_args(argv)
    img = capture(a.image, entry=a.entry)
    intent = understand(img, a.transcript, a.mode, capture_entry=a.entry)
    print(json.dumps(intent, ensure_ascii=False, indent=2))
    if a.do:
        from src.do import do, DoError
        try:
            for path in do(intent):
                print("WROTE", path)
        except DoError as e:
            print(f"ERROR: {e}", file=sys.stderr); return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
