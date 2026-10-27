"""Understand: image (+ optional transcript) -> INTENT_SCHEMA JSON.

Provider order:
1) OPENAI_API_KEY  -> OpenAI-compatible vision (OPENAI_BASE_URL / VISION_MODEL)
2) ANTHROPIC_API_KEY -> Anthropic Claude vision (ANTHROPIC_MODEL)
3) neither -> clearly-labelled MOCK (keyword route for 3 locked tasks)
"""
import base64, json, os, re
from pathlib import Path
import jsonschema

SCHEMA = json.loads((Path(__file__).resolve().parents[2] / "schema" / "intent_schema.json").read_text())
SCHEMA_HINT = (
    "Locked tasks only: draft_email (reply-and-accept draft, never send), "
    "make_chart (produce chart image), log_record (local expense JSON). "
    "proposed_action.auto_send must be false. Return ONLY JSON matching this schema:\n"
    + json.dumps(SCHEMA)
)

def _enforce_safety(d: dict) -> dict:
    pa = d.setdefault("proposed_action", {})
    pa["auto_send"] = False
    if pa.get("kind") not in ("none", "draft", "render_image", "write_local_record"):
        pa["kind"] = "draft"
    return d

def _route_mock(transcript: str | None) -> tuple[str, str, str]:
    t = (transcript or "").strip()
    if re.search(r"回复|接受|reply|accept", t, re.I):
        return ("draft_email", "draft", "mock: route to email reply draft (auto_send=false)")
    if re.search(r"图表|做成图|chart|graph", t, re.I):
        return ("make_chart", "render_image", "mock: route to chart image render")
    if re.search(r"报销|归档|收据|账单|expense|receipt", t, re.I):
        return ("log_record", "write_local_record", "mock: route to local expense record")
    if t:
        return ("summarize", "none", "mock output, no LLM called")
    return ("explain", "none", "mock output, no LLM called")

def _mock(image: str, transcript: str | None, mode: str) -> dict:
    task_type, kind, detail = _route_mock(transcript)
    return {
        "mode": mode,
        "intent": f"[MOCK] {transcript or 'explain selected region'}",
        "task_type": task_type,
        "summary": f"[MOCK — no API key] Placeholder understanding of {Path(image).name}",
        "entities": [{"type": "image_file", "value": Path(image).name}],
        "proposed_action": {"kind": kind, "auto_send": False, "detail": detail},
        "confidence": 0.0,
        "source": "mock",
    }

def _vision_openai(image: str, transcript: str | None, mode: str) -> dict:
    from openai import OpenAI
    client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL") or None)
    b64 = base64.b64encode(Path(image).read_bytes()).decode()
    prompt = (
        "You are a screen-assistant intent parser for SimTech AI mouse agent. "
        + (f"Spoken request: \"{transcript}\". " if transcript else "")
        + f"mode='{mode}'. " + SCHEMA_HINT
    )
    r = client.chat.completions.create(
        model=os.getenv("VISION_MODEL", "gpt-4o-mini"),
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            ],
        }],
    )
    d = json.loads(r.choices[0].message.content)
    d["source"] = "vision_llm"
    return d

def _vision_anthropic(image: str, transcript: str | None, mode: str) -> dict:
    import anthropic
    client = anthropic.Anthropic()
    raw = Path(image).read_bytes()
    # Detect media type from extension; default png
    suffix = Path(image).suffix.lower()
    media = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}.get(suffix, "image/png")
    prompt = (
        "You are a screen-assistant intent parser for SimTech AI mouse agent. "
        + (f"Spoken request: \"{transcript}\". " if transcript else "")
        + f"mode='{mode}'. " + SCHEMA_HINT
    )
    r = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": media, "data": base64.b64encode(raw).decode()},
                },
                {"type": "text", "text": prompt},
            ],
        }],
    )
    text = "".join(getattr(b, "text", "") for b in r.content)
    # Strip optional markdown fences
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    d = json.loads(text)
    d["source"] = "vision_llm"
    return d

def _pick_provider() -> str:
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    return "mock"

def understand(image: str, transcript: str | None = None, mode: str = "point", capture_entry: str = "point") -> dict:
    if capture_entry not in ("point", "capture_region"):
        raise ValueError(f"capture_entry must be point|capture_region, got {capture_entry!r}")
    provider = _pick_provider()
    if provider == "openai":
        d = _vision_openai(image, transcript, mode)
    elif provider == "anthropic":
        d = _vision_anthropic(image, transcript, mode)
    else:
        d = _mock(image, transcript, mode)
    d["capture_entry"] = capture_entry
    # Tag entity for Ask bypass demos
    if capture_entry == "capture_region":
        ents = d.setdefault("entities", [])
        if not any(e.get("type") == "capture_entry" for e in ents):
            ents.append({"type": "capture_entry", "value": "capture_region"})
    d = _enforce_safety(d)
    jsonschema.validate(d, SCHEMA)
    return d
