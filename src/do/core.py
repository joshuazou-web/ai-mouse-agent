"""Do: intent JSON -> local artifacts. No network, no API key, never auto-send."""
import csv, datetime, json, platform, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_CSV = ROOT / "tests" / "sample_table.csv"

class DoError(Exception):
    pass

def _ts():
    return time.strftime("%Y%m%d_%H%M%S")

def _ents(intent, *types):
    return [e for e in intent.get("entities", []) if e.get("type") in types]

def _num(v):
    m = re.search(r"-?\d+(?:\.\d+)?", str(v).replace(",", ""))
    return float(m.group()) if m else None

def draft_email(intent, out: Path):
    d = out / "drafts"; d.mkdir(parents=True, exist_ok=True)
    subj = next((e["value"] for e in _ents(intent, "subject", "email_subject")), "your request")
    sender = next((e["value"] for e in _ents(intent, "sender", "person", "name")), "")
    subject = f"Re: {subj}"
    body = (f"Hi{(' ' + sender) if sender else ''},\n\n"
            "Thanks for reaching out. I'm happy to accept your request and will follow up with details shortly.\n\n"
            "Best regards,\n")
    f = d / f"reply_{_ts()}.md"
    f.write_text(f"<!-- AI Mouse DRAFT — auto_send=false, NOT sent -->\nSubject: {subject}\n\n{body}", encoding="utf-8")
    paths = [f]
    if platform.system() == "Darwin":
        esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
        a = d / "open_mail_reply.applescript"
        a.write_text(
            "-- AI Mouse: opens a Mail reply to the selected message and fills the body.\n"
            "-- Run manually: osascript out/drafts/open_mail_reply.applescript . It NEVER sends.\n"
            'tell application "Mail"\n  activate\n  set sel to selection\n'
            '  if (count of sel) > 0 then\n    set r to reply (item 1 of sel) with opening window\n'
            f'    set content of r to "{esc(body)}" & return & content of r\n'
            '  else\n'
            f'    make new outgoing message with properties {{subject:"{esc(subject)}", content:"{esc(body)}", visible:true}}\n'
            '  end if\nend tell\n', encoding="utf-8")
        paths.append(a)
    return paths

def _chart_data(intent):
    pts = []
    for e in intent.get("entities", []):
        n = _num(e.get("value"))
        if n is not None and e.get("type") not in ("image_file",):
            pts.append((e.get("label") or e.get("type") or f"v{len(pts)+1}", n))
    if pts:
        return pts, "intent entities"
    m = re.search(r"[\w./-]+\.csv", intent.get("proposed_action", {}).get("detail", "") or "")
    p = Path(m.group()) if m and Path(m.group()).exists() else SAMPLE_CSV
    with open(p, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    return [(r[0], float(r[1])) for r in rows[1:] if len(r) >= 2 and _num(r[1]) is not None], str(p)

def make_chart(intent, out: Path):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pts, src = _chart_data(intent)
    if not pts:
        raise DoError("make_chart: no numeric data found")
    d = out / "charts"; d.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([p[0] for p in pts], [p[1] for p in pts], color="#4a7bd0")
    ax.set_title(f"AI Mouse chart ({Path(src).name})")
    fig.tight_layout()
    f = d / f"chart_{_ts()}.png"; fig.savefig(f, dpi=120); plt.close(fig)
    return [f]

def log_record(intent, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    g = lambda *t: next((e["value"] for e in _ents(intent, *t)), None)
    amt = g("amount", "total", "price")
    row = {
        "merchant": g("merchant", "vendor", "store") or "unknown",
        "amount": _num(amt) if amt is not None else 0.0,
        "currency": g("currency") or "CNY",
        "date": g("date") or datetime.date.today().isoformat(),
        "note": intent.get("intent", ""),
        "source_image": g("image_file"),
    }
    f = out / "expenses.json"
    data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    data.append(row)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return [f]

HANDLERS = {"draft_email": draft_email, "make_chart": make_chart, "log_record": log_record}

def do(intent: dict, out_dir: str | Path = ROOT / "out") -> list[str]:
    pa = intent.get("proposed_action") or {}
    if pa.get("auto_send") is not False:
        raise DoError("refused: proposed_action.auto_send must be false")
    t = intent.get("task_type")
    if t not in HANDLERS:
        raise DoError(f"refused: unknown task_type {t!r}; supported: {sorted(HANDLERS)}")
    return [str(Path(p).resolve()) for p in HANDLERS[t](intent, Path(out_dir))]
