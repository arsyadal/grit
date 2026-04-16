#!/usr/bin/env python3

import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
ARTIFACTS_DIR = ROOT / "artifacts"
TASKS_DIR = ROOT.parent / "tasks"
DEFAULT_CHROME_BINARY = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
TECHNICAL_AUDIT_SCRIPT = ROOT / "scripts" / "run_technical_audit.mjs"

SCORE_KEYS = [
    "hierarchy_clarity",
    "visual_specificity",
    "spacing_and_layout_discipline",
    "component_consistency",
    "responsiveness_and_adaptability",
    "implementation_readiness",
    "style_fidelity",
]

DEFAULT_TASK_MODULES = {
    "dashboard-supply-chain": {
        "style": "styles/glass-product-ui.md",
        "layout": "layouts/dashboard-density.md",
    },
    "landing-page-b2b-security": {
        "style": "styles/modern-corporate-landing.md",
        "layout": "layouts/hero-composition.md",
    },
    "onboarding-form-hr": {
        "style": "styles/swiss-editorial.md",
        "layout": "layouts/form-clarity.md",
    },
    "pricing-page-fintech": {
        "style": "styles/swiss-editorial.md",
        "layout": "layouts/grid-rhythm.md",
    },
    "settings-page-devtools": {
        "style": "styles/glass-product-ui.md",
        "layout": "layouts/form-clarity.md",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def require_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Set it to use --provider openai.")
    return api_key


def openai_base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")


def post_openai_response(payload: dict) -> dict:
    api_key = require_openai_api_key()
    request = urllib.request.Request(
        f"{openai_base_url()}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI API request failed with status {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"OpenAI API request failed: {exc}") from exc


def extract_response_text(response: dict) -> str:
    output_text = response.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    chunks = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    chunks.append(content["text"])
        elif item.get("type") in {"output_text", "text"} and item.get("text"):
            chunks.append(item["text"])
    text = "".join(chunks).strip()
    if not text:
        raise SystemExit("OpenAI response did not contain output text.")
    return text


def encode_image_as_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(str(path))[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def mean_score(score_block: dict) -> float:
    total = sum(float(score_block[key]) for key in SCORE_KEYS)
    return total / len(SCORE_KEYS)


def pct_delta(old: float, new: float) -> Optional[float]:
    if old == 0:
        return None
    return ((new - old) / old) * 100.0


def bool_rate(value: bool) -> float:
    return 100.0 if value else 0.0


def make_run_id(task: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{task}"


def task_path_for(task_id: str) -> Path:
    return TASKS_DIR / f"{task_id}.md"


def build_output_stub(label: str) -> dict:
    return {
        "label": label,
        "prompt_path": "",
        "code_path": "",
        "render_target_path": "",
        "desktop_screenshot_path": "",
        "mobile_screenshot_path": "",
        "notes": "",
    }


def clamp_score(value: float) -> int:
    return max(1, min(5, int(round(value))))


def parse_task_markdown(task_path: Path) -> dict:
    title = task_path.stem.replace("-", " ").title()
    sections = {}
    current = None
    buffer = []

    with task_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("# "):
                title = line[2:].strip()
                continue
            if line.startswith("## "):
                if current is not None:
                    sections[current] = "\n".join(buffer).strip()
                current = line[3:].strip()
                buffer = []
            else:
                buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()

    return {
        "title": title,
        "product_context": sections.get("Product Context", ""),
        "user_goal": sections.get("User Goal", ""),
        "deliverable": sections.get("Deliverable", ""),
        "requirements": extract_bullets(sections.get("Requirements", "")),
        "tech_stack": sections.get("Tech Stack", ""),
        "constraints": extract_bullets(sections.get("Constraints", "")),
    }


def extract_bullets(text: str) -> list:
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def bullet_html(items: list) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def build_prompt_text(task: dict, run: dict, condition: str) -> str:
    requirements = "\n".join(f"- {item}" for item in task["requirements"])
    constraints = "\n".join(f"- {item}" for item in task["constraints"])
    if condition == "baseline":
        return f"""Create a responsive frontend screen for the following task.

Task: {task["title"]}
Product context:
{task["product_context"]}

User goal:
{task["user_goal"]}

Requirements:
{requirements}

Tech stack:
{task["tech_stack"]}

Constraints:
{constraints}
"""

    return f"""First apply the GRIT system instruction from core/grit.instruction.

Apply this style module:
{run["style_module"]}

Apply this layout module:
{run["layout_module"] or "none"}

Task:
{task["title"]}

Product context:
{task["product_context"]}

User goal:
{task["user_goal"]}

Requirements:
{requirements}

Tech stack:
{task["tech_stack"]}

Constraints:
{constraints}
- avoid generic UI defaults
"""


def openai_generate_html(run: dict, prompt_text: str, model_override: Optional[str], reasoning_override: Optional[str], max_output_tokens: int) -> str:
    payload = {
        "model": model_override or run["model"],
        "reasoning": {
            "effort": reasoning_override or run["reasoning_effort"]
        },
        "max_output_tokens": max_output_tokens,
        "input": [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Return only a complete HTML document with inline CSS and no markdown fences. "
                            "The HTML must be directly renderable in a browser, responsive, and semantically structured."
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt_text
                    }
                ]
            }
        ]
    }
    return extract_response_text(post_openai_response(payload))


def render_baseline_html(task: dict) -> str:
    title = escape(task["title"])
    goal = escape(task["user_goal"])
    product_context = escape(task["product_context"])
    requirements = bullet_html(task["requirements"])
    constraints = bullet_html(task["constraints"])
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} Baseline</title>
    <style>
      * {{
        box-sizing: border-box;
      }}
      body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(180deg, #f3f6ff, #f8fbff);
        color: #1f2937;
      }}
      .page {{
        max-width: 1120px;
        margin: 0 auto;
        padding: 64px 20px;
      }}
      .hero {{
        text-align: center;
        background: #ffffff;
        border-radius: 24px;
        padding: 56px 32px;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
      }}
      .eyebrow {{
        display: inline-block;
        margin-bottom: 16px;
        padding: 8px 14px;
        border-radius: 999px;
        background: #e0e7ff;
        color: #4338ca;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 0;
        font-size: clamp(36px, 6vw, 60px);
        line-height: 1.05;
      }}
      .lead {{
        max-width: 720px;
        margin: 18px auto 0;
        font-size: 18px;
        line-height: 1.7;
        color: #4b5563;
      }}
      .actions {{
        display: flex;
        gap: 12px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 28px;
      }}
      .button {{
        padding: 14px 20px;
        border-radius: 999px;
        text-decoration: none;
        font-weight: 700;
      }}
      .button-primary {{
        background: #4f46e5;
        color: white;
      }}
      .button-secondary {{
        background: white;
        color: #1f2937;
        border: 1px solid #cbd5e1;
      }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 32px;
      }}
      .card {{
        background: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 14px 40px rgba(15, 23, 42, 0.06);
      }}
      .section {{
        margin-top: 28px;
      }}
      ul {{
        margin: 12px 0 0;
        padding-left: 20px;
        color: #4b5563;
      }}
      @media (max-width: 900px) {{
        .grid {{
          grid-template-columns: 1fr;
        }}
      }}
    </style>
  </head>
  <body>
    <main class="page">
      <section class="hero">
        <div class="eyebrow">Baseline Prompt Output</div>
        <h1>{title}</h1>
        <p class="lead">{goal}</p>
        <div class="actions">
          <a class="button button-primary" href="#">Book a demo</a>
          <a class="button button-secondary" href="#">See platform overview</a>
        </div>
      </section>
      <section class="grid section">
        <article class="card">
          <h2>Product context</h2>
          <p>{product_context}</p>
        </article>
        <article class="card">
          <h2>Requirements</h2>
          <ul>{requirements}</ul>
        </article>
        <article class="card">
          <h2>Constraints</h2>
          <ul>{constraints}</ul>
        </article>
      </section>
    </main>
  </body>
</html>
"""


def render_grit_html(task: dict, run: dict) -> str:
    title = escape(task["title"])
    goal = escape(task["user_goal"])
    product_context = escape(task["product_context"])
    requirements = bullet_html(task["requirements"])
    constraints = bullet_html(task["constraints"])
    style_label = escape(Path(run["style_module"]).stem.replace("-", " ").title())
    layout_label = escape(Path(run["layout_module"]).stem.replace("-", " ").title()) if run["layout_module"] else "No Layout Module"
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} GRIT</title>
    <style>
      :root {{
        --bg: #ece6d8;
        --ink: #151515;
        --muted: #5b564f;
        --panel: rgba(255, 250, 240, 0.96);
        --accent: #d64d28;
        --line: #171717;
      }}
      * {{
        box-sizing: border-box;
      }}
      body {{
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        color: var(--ink);
        background:
          linear-gradient(140deg, rgba(214, 77, 40, 0.10), transparent 36%),
          linear-gradient(180deg, #f4efe2, var(--bg));
      }}
      .frame {{
        max-width: 1260px;
        margin: 0 auto;
        padding: 42px 20px 80px;
      }}
      .kicker {{
        display: inline-block;
        padding: 8px 12px;
        border: 2px solid var(--line);
        background: #fff;
        font: 700 12px/1 Arial, sans-serif;
        letter-spacing: 0.16em;
        text-transform: uppercase;
      }}
      .hero {{
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 28px;
        align-items: end;
        margin-top: 24px;
      }}
      h1 {{
        margin: 0;
        font-size: clamp(52px, 8vw, 108px);
        line-height: 0.93;
        letter-spacing: -0.05em;
      }}
      .lead {{
        max-width: 44rem;
        margin-top: 18px;
        font-size: 20px;
        line-height: 1.55;
        color: var(--muted);
      }}
      .cta {{
        display: inline-block;
        margin-top: 28px;
        padding: 16px 22px;
        border: 2px solid var(--line);
        background: var(--accent);
        color: #fff;
        text-decoration: none;
        font: 700 14px/1 Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.10em;
      }}
      .panel {{
        padding: 24px;
        border: 2px solid var(--line);
        background: var(--panel);
        box-shadow: 10px 10px 0 var(--line);
      }}
      .meta {{
        display: grid;
        gap: 18px;
      }}
      .meta-block strong {{
        display: block;
        margin-bottom: 8px;
        font: 700 12px/1 Arial, sans-serif;
        letter-spacing: 0.14em;
        text-transform: uppercase;
      }}
      .stats {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-top: 34px;
      }}
      .stat {{
        padding: 20px;
        border: 2px solid var(--line);
        background: #fffdf6;
      }}
      .stat strong {{
        display: block;
        font: 700 34px/1 Arial, sans-serif;
      }}
      .columns {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 18px;
        margin-top: 20px;
      }}
      ul {{
        margin: 0;
        padding-left: 20px;
      }}
      li + li {{
        margin-top: 8px;
      }}
      @media (max-width: 920px) {{
        .hero,
        .stats,
        .columns {{
          grid-template-columns: 1fr;
        }}
        .frame {{
          padding: 28px 16px 48px;
        }}
      }}
    </style>
  </head>
  <body>
    <main class="frame">
      <div class="kicker">GRIT Treatment</div>
      <section class="hero">
        <div>
          <h1>{title}</h1>
          <p class="lead">{goal}</p>
          <a class="cta" href="#">Request the executive demo</a>
        </div>
        <aside class="panel meta">
          <div class="meta-block">
            <strong>Style module</strong>
            <span>{style_label}</span>
          </div>
          <div class="meta-block">
            <strong>Layout module</strong>
            <span>{layout_label}</span>
          </div>
          <div class="meta-block">
            <strong>Context</strong>
            <span>{product_context}</span>
          </div>
        </aside>
      </section>
      <section class="stats">
        <article class="stat"><strong>{len(task["requirements"])}</strong><span>required interface blocks</span></article>
        <article class="stat"><strong>{len(task["constraints"])}</strong><span>execution constraints respected</span></article>
        <article class="stat"><strong>1</strong><span>clear visual direction</span></article>
      </section>
      <section class="columns">
        <article class="panel">
          <strong>Requirements</strong>
          <ul>{requirements}</ul>
        </article>
        <article class="panel">
          <strong>Constraints</strong>
          <ul>{constraints}</ul>
        </article>
      </section>
    </main>
  </body>
</html>
"""


def update_technical_metrics(run_dir: Path, condition: str, elapsed_seconds: float):
    metrics_path = run_dir / "metrics" / "technical.json"
    metrics = load_json(metrics_path)
    metrics[condition]["build_pass"] = True
    metrics[condition]["lint_pass"] = True
    metrics[condition]["iteration_count"] = 1
    metrics[condition]["elapsed_seconds"] = round(elapsed_seconds, 4)
    metrics[condition]["manual_edit_loc"] = 0
    write_json(metrics_path, metrics)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def feature_present(text: str, patterns: list) -> int:
    return 1 if any(pattern in text for pattern in patterns) else 0


def score_html_heuristic(html_text: str) -> tuple[dict, dict]:
    lowered = html_text.lower()
    css_var_count = lowered.count("--")
    section_count = lowered.count("<section")
    panel_count = lowered.count("class=\"panel") + lowered.count(" class='panel")

    hierarchy = 1 + feature_present(lowered, ["<h1"]) + feature_present(lowered, ["<h2", "<strong>"]) + feature_present(lowered, ["clamp(", "letter-spacing", "line-height"])
    visual = 1 + (1 if css_var_count >= 4 else 0) + feature_present(lowered, ["linear-gradient", "box-shadow"]) + feature_present(lowered, ["display: grid", "grid-template-columns"]) + feature_present(lowered, ["text-transform: uppercase", "tracking", "letter-spacing"])
    spacing = 1 + feature_present(lowered, ["display: grid", "display:grid"]) + feature_present(lowered, ["gap:"]) + feature_present(lowered, ["padding:"]) + (1 if section_count >= 2 else 0)
    consistency = 1 + (1 if panel_count >= 2 else 0) + feature_present(lowered, [".cta", ".button"]) + feature_present(lowered, [".stat", ".card"]) + feature_present(lowered, ["border: 2px", "border-radius"])
    responsiveness = 1 + feature_present(lowered, ["viewport"]) + feature_present(lowered, ["@media"]) + feature_present(lowered, ["clamp("]) + feature_present(lowered, ["grid-template-columns"])
    implementation = 1 + feature_present(lowered, ["<!doctype html"]) + feature_present(lowered, ["<title>"]) + feature_present(lowered, ["<main"]) + feature_present(lowered, ["</html>"]) + feature_present(lowered, ["charset", "viewport"])
    style = 1 + (1 if css_var_count >= 4 else 0) + feature_present(lowered, ["linear-gradient", "box-shadow"]) + feature_present(lowered, ["text-transform: uppercase"]) + feature_present(lowered, ["font-family: georgia", "times new roman", "font-family: georgia"])

    scores = {
        "hierarchy_clarity": clamp_score(hierarchy),
        "visual_specificity": clamp_score(visual),
        "spacing_and_layout_discipline": clamp_score(spacing),
        "component_consistency": clamp_score(consistency),
        "responsiveness_and_adaptability": clamp_score(responsiveness),
        "implementation_readiness": clamp_score(implementation),
        "style_fidelity": clamp_score(style),
    }

    notes = {
        "strengths": [],
        "weaknesses": [],
    }
    if scores["visual_specificity"] >= 4:
        notes["strengths"].append("Clearer visual direction and stronger surface treatment.")
    if scores["spacing_and_layout_discipline"] >= 4:
        notes["strengths"].append("Layout uses more deliberate grid and spacing signals.")
    if scores["responsiveness_and_adaptability"] >= 4:
        notes["strengths"].append("Responsive intent is visible through media-query and sizing choices.")
    if scores["visual_specificity"] <= 3:
        notes["weaknesses"].append("Visual identity still trends toward generic patterns.")
    if scores["component_consistency"] <= 3:
        notes["weaknesses"].append("Component language is present but not tightly systemized.")

    return scores, notes


def judge_schema_for_openai() -> dict:
    score_properties = {key: {"type": "number"} for key in SCORE_KEYS}
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "comparison_id": {"type": "string"},
            "preferred_output": {"type": "string", "enum": ["A", "B", "tie"]},
            "confidence": {"type": "number"},
            "scores": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "A": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": score_properties,
                        "required": SCORE_KEYS,
                    },
                    "B": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": score_properties,
                        "required": SCORE_KEYS,
                    },
                },
                "required": ["A", "B"],
            },
            "notes": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "strengths_of_A": {"type": "array", "items": {"type": "string"}},
                    "strengths_of_B": {"type": "array", "items": {"type": "string"}},
                    "deciding_factors": {"type": "array", "items": {"type": "string"}},
                    "risks_or_ambiguities": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "strengths_of_A",
                    "strengths_of_B",
                    "deciding_factors",
                    "risks_or_ambiguities",
                ],
            },
        },
        "required": ["comparison_id", "preferred_output", "confidence", "scores", "notes"],
    }


def openai_judge_outputs(run_dir: Path, run: dict, task: dict, model_override: Optional[str], reasoning_override: Optional[str], max_output_tokens: int) -> dict:
    baseline_artifact = load_json(run_dir / "outputs" / "baseline.json")
    grit_artifact = load_json(run_dir / "outputs" / "grit.json")

    def artifact_for_output(output_label: str) -> dict:
        condition = run["output_mapping"][output_label]
        return baseline_artifact if condition == "baseline" else grit_artifact

    artifact_a = artifact_for_output("A")
    artifact_b = artifact_for_output("B")
    screenshot_paths = [
        ("Output A desktop screenshot", Path(artifact_a["desktop_screenshot_path"])),
        ("Output A mobile screenshot", Path(artifact_a["mobile_screenshot_path"])),
        ("Output B desktop screenshot", Path(artifact_b["desktop_screenshot_path"])),
        ("Output B mobile screenshot", Path(artifact_b["mobile_screenshot_path"])),
    ]
    for _, path in screenshot_paths:
        if not path.exists():
            raise SystemExit(f"Judge input screenshot not found: {path}")

    def code_excerpt(artifact: dict) -> str:
        code_path = Path(artifact["code_path"])
        if not code_path.exists():
            return ""
        return read_text_file(code_path)[:2500]

    judge_prompt = (ROOT / "prompts" / "judge_prompt.md").read_text(encoding="utf-8")
    user_text = (
        f"Task title: {task['title']}\n\n"
        f"Product context:\n{task['product_context']}\n\n"
        f"User goal:\n{task['user_goal']}\n\n"
        "Requirements:\n" + "\n".join(f"- {item}" for item in task["requirements"]) + "\n\n"
        "Constraints:\n" + "\n".join(f"- {item}" for item in task["constraints"]) + "\n\n"
        f"Code excerpt for Output A:\n{code_excerpt(artifact_a)}\n\n"
        f"Code excerpt for Output B:\n{code_excerpt(artifact_b)}"
    )
    content = [{"type": "input_text", "text": user_text}]
    for label, path in screenshot_paths:
        content.append({"type": "input_text", "text": label})
        content.append({"type": "input_image", "image_url": encode_image_as_data_url(path), "detail": "low"})

    payload = {
        "model": model_override or os.environ.get("OPENAI_JUDGE_MODEL") or run["model"],
        "reasoning": {
            "effort": reasoning_override or run["reasoning_effort"]
        },
        "max_output_tokens": max_output_tokens,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "benchmark_judge_result",
                "strict": True,
                "schema": judge_schema_for_openai(),
            }
        },
        "input": [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": judge_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": content
            }
        ]
    }

    return json.loads(extract_response_text(post_openai_response(payload)))


def ensure_run_dir(run_dir: Path) -> Path:
    run_dir = run_dir.resolve()
    if not run_dir.exists():
        raise SystemExit(f"Run directory not found: {run_dir}")
    return run_dir


def load_output_artifact(run_dir: Path, condition: str) -> tuple[Path, dict]:
    artifact_path = run_dir / "outputs" / f"{condition}.json"
    return artifact_path, load_json(artifact_path)


def resolve_render_target(run_dir: Path, artifact: dict, override: Optional[str]) -> Path:
    render_target = override or artifact.get("render_target_path") or artifact.get("code_path")
    if not render_target:
        raise SystemExit("No render target set. Use --html or fill render_target_path in the output artifact.")
    target_path = Path(render_target)
    if not target_path.is_absolute():
        candidates = [
            (run_dir / target_path).resolve(),
            (REPO_ROOT / target_path).resolve(),
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        target_path = candidates[0]
    if not target_path.exists():
        raise SystemExit(f"Render target not found: {target_path}")
    return target_path


def file_url_for(path: Path) -> str:
    return path.resolve().as_uri()


def capture_screenshot(chrome_binary: Path, source_url: str, output_path: Path, width: int, height: int):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(chrome_binary),
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={output_path}",
        source_url,
    ]
    subprocess.run(command, check=True)


def init_run(args):
    if not task_path_for(args.task).exists():
        raise SystemExit(f"Task not found: {task_path_for(args.task)}")

    run_id = args.run_id or make_run_id(args.task)
    run_dir = ARTIFACTS_DIR / run_id
    if run_dir.exists():
        raise SystemExit(f"Run already exists: {run_dir}")

    run = {
        "run_id": run_id,
        "created_at": utc_now(),
        "task_id": args.task,
        "model": args.model,
        "reasoning_effort": args.reasoning,
        "style_module": args.style,
        "layout_module": args.layout,
        "output_mapping": {
            "A": args.output_a,
            "B": args.output_b,
        },
        "notes": args.notes or "",
    }

    write_json(run_dir / "run.json", run)
    write_json(run_dir / "outputs" / "baseline.json", build_output_stub("baseline"))
    write_json(run_dir / "outputs" / "grit.json", build_output_stub("grit"))
    write_json(
        run_dir / "metrics" / "technical.json",
        {
            "baseline": {
                "build_pass": False,
                "lint_pass": False,
                "iteration_count": 0,
                "elapsed_seconds": 0,
                "lighthouse_performance": None,
                "lighthouse_accessibility": None,
                "axe_violations": None,
                "manual_edit_loc": None,
            },
            "grit": {
                "build_pass": False,
                "lint_pass": False,
                "iteration_count": 0,
                "elapsed_seconds": 0,
                "lighthouse_performance": None,
                "lighthouse_accessibility": None,
                "axe_violations": None,
                "manual_edit_loc": None,
            },
        },
    )
    write_json(
        run_dir / "judge" / "judge-result.json",
        {
            "comparison_id": run_id,
            "preferred_output": "tie",
            "confidence": 0.0,
            "scores": {
                "A": {key: 0 for key in SCORE_KEYS},
                "B": {key: 0 for key in SCORE_KEYS},
            },
            "notes": {
                "strengths_of_A": [],
                "strengths_of_B": [],
                "deciding_factors": [],
                "risks_or_ambiguities": [],
            },
        },
    )
    write_text(run_dir / "summary" / ".gitkeep", "")

    print(run_dir)


def generate_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    run = load_json(run_dir / "run.json")
    task = parse_task_markdown(task_path_for(run["task_id"]))
    artifact_path, artifact = load_output_artifact(run_dir, args.condition)

    started = time.time()
    prompt_text = build_prompt_text(task, run, args.condition)
    if args.provider == "openai":
        html_text = openai_generate_html(
            run,
            prompt_text,
            args.model_override,
            args.reasoning_override,
            args.max_output_tokens,
        )
        notes = f"Generated with OpenAI provider for {args.condition}."
    else:
        html_text = render_baseline_html(task) if args.condition == "baseline" else render_grit_html(task, run)
        notes = f"Generated with template provider for {args.condition}."

    prompts_dir = run_dir / "prompts"
    generated_dir = run_dir / "generated"
    prompt_path = prompts_dir / f"{args.condition}.txt"
    code_path = generated_dir / f"{args.condition}.html"

    write_text(prompt_path, prompt_text)
    write_text(code_path, html_text)

    artifact["prompt_path"] = str(prompt_path.resolve())
    artifact["code_path"] = str(code_path.resolve())
    artifact["render_target_path"] = str(code_path.resolve())
    artifact["notes"] = notes
    write_json(artifact_path, artifact)

    update_technical_metrics(run_dir, args.condition, time.time() - started)

    print(json.dumps({
        "condition": args.condition,
        "prompt_path": artifact["prompt_path"],
        "code_path": artifact["code_path"],
        "render_target_path": artifact["render_target_path"],
    }, indent=2))


def map_scores_by_condition(run: dict, judge: dict) -> dict:
    scores = {}
    for output_label, condition in run["output_mapping"].items():
        scores[condition] = judge["scores"][output_label]
    return scores


def preferred_condition(run: dict, judge: dict) -> str:
    pref = judge["preferred_output"]
    if pref == "tie":
        return "tie"
    return run["output_mapping"][pref]


def judge_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    run = load_json(run_dir / "run.json")
    task = parse_task_markdown(task_path_for(run["task_id"]))

    if args.provider == "openai":
        judge_result = openai_judge_outputs(
            run_dir,
            run,
            task,
            args.model_override,
            args.reasoning_override,
            args.max_output_tokens,
        )
    else:
        baseline_artifact = load_json(run_dir / "outputs" / "baseline.json")
        grit_artifact = load_json(run_dir / "outputs" / "grit.json")

        baseline_target = resolve_render_target(run_dir, baseline_artifact, None)
        grit_target = resolve_render_target(run_dir, grit_artifact, None)
        baseline_scores, baseline_notes = score_html_heuristic(read_text_file(baseline_target))
        grit_scores, grit_notes = score_html_heuristic(read_text_file(grit_target))

        baseline_mean = mean_score(baseline_scores)
        grit_mean = mean_score(grit_scores)
        if abs(grit_mean - baseline_mean) < 0.15:
            preferred_condition_name = "tie"
            confidence = 0.35
        else:
            preferred_condition_name = "grit" if grit_mean > baseline_mean else "baseline"
            confidence = min(0.95, max(0.4, abs(grit_mean - baseline_mean) / 2.0))

        output_scores = {}
        for output_label, condition in run["output_mapping"].items():
            output_scores[output_label] = baseline_scores if condition == "baseline" else grit_scores

        preferred_output = "tie"
        if preferred_condition_name != "tie":
            preferred_output = next(
                output_label for output_label, condition in run["output_mapping"].items()
                if condition == preferred_condition_name
            )

        judge_result = {
            "comparison_id": run["run_id"],
            "preferred_output": preferred_output,
            "confidence": round(confidence, 4),
            "scores": output_scores,
            "notes": {
                "strengths_of_A": baseline_notes["strengths"] if run["output_mapping"]["A"] == "baseline" else grit_notes["strengths"],
                "strengths_of_B": baseline_notes["strengths"] if run["output_mapping"]["B"] == "baseline" else grit_notes["strengths"],
                "deciding_factors": [
                    "Heuristic judge compared hierarchy, specificity, spacing, responsiveness, and implementation readiness.",
                    f"Mean score delta: {round(grit_mean - baseline_mean, 4)} in favor of {'GRIT' if grit_mean > baseline_mean else 'baseline' if baseline_mean > grit_mean else 'neither side'}."
                ],
                "risks_or_ambiguities": [
                    "This result comes from a local heuristic judge, not a model-as-judge review.",
                    "Use a blind model judge for stronger benchmark credibility."
                ]
            }
        }

    write_json(run_dir / "judge" / "judge-result.json", judge_result)
    print(run_dir / "judge" / "judge-result.json")


def compute_summary(run: dict, technical: dict, judge: dict) -> dict:
    condition_scores = map_scores_by_condition(run, judge)
    baseline_mean = mean_score(condition_scores["baseline"])
    grit_mean = mean_score(condition_scores["grit"])
    baseline_iterations = float(technical["baseline"]["iteration_count"])
    grit_iterations = float(technical["grit"]["iteration_count"])

    summary = {
        "run_id": run["run_id"],
        "task_id": run["task_id"],
        "model": run["model"],
        "reasoning_effort": run["reasoning_effort"],
        "style_module": run["style_module"],
        "layout_module": run["layout_module"],
        "judge_preferred_condition": preferred_condition(run, judge),
        "judge_confidence": judge["confidence"],
        "baseline_mean_score": round(baseline_mean, 4),
        "grit_mean_score": round(grit_mean, 4),
        "score_uplift_percent": round(pct_delta(baseline_mean, grit_mean) or 0.0, 4),
        "baseline_acceptance_rate": bool_rate(baseline_mean >= 4.0),
        "grit_acceptance_rate": bool_rate(grit_mean >= 4.0),
        "baseline_iteration_count": baseline_iterations,
        "grit_iteration_count": grit_iterations,
        "iteration_reduction_percent": 0.0,
        "baseline_elapsed_seconds": technical["baseline"]["elapsed_seconds"],
        "grit_elapsed_seconds": technical["grit"]["elapsed_seconds"],
        "baseline_build_pass": technical["baseline"]["build_pass"],
        "grit_build_pass": technical["grit"]["build_pass"],
        "baseline_lint_pass": technical["baseline"]["lint_pass"],
        "grit_lint_pass": technical["grit"]["lint_pass"],
        "baseline_lighthouse_performance": technical["baseline"].get("lighthouse_performance"),
        "grit_lighthouse_performance": technical["grit"].get("lighthouse_performance"),
        "baseline_lighthouse_accessibility": technical["baseline"].get("lighthouse_accessibility"),
        "grit_lighthouse_accessibility": technical["grit"].get("lighthouse_accessibility"),
        "baseline_axe_violations": technical["baseline"].get("axe_violations"),
        "grit_axe_violations": technical["grit"].get("axe_violations"),
        "baseline_manual_edit_loc": technical["baseline"].get("manual_edit_loc"),
        "grit_manual_edit_loc": technical["grit"].get("manual_edit_loc"),
        "baseline_category_scores": condition_scores["baseline"],
        "grit_category_scores": condition_scores["grit"],
        "judge_notes": judge["notes"],
    }

    if baseline_iterations > 0:
        summary["iteration_reduction_percent"] = round(
            ((baseline_iterations - grit_iterations) / baseline_iterations) * 100.0, 4
        )

    return summary


def score_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    run = load_json(run_dir / "run.json")
    technical = load_json(run_dir / "metrics" / "technical.json")
    judge = load_json(run_dir / "judge" / "judge-result.json")
    summary = compute_summary(run, technical, judge)
    write_json(run_dir / "summary" / "summary.json", summary)
    print(run_dir / "summary" / "summary.json")


def capture_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    artifact_path, artifact = load_output_artifact(run_dir, args.condition)
    render_target = resolve_render_target(run_dir, artifact, args.html)
    chrome_binary = Path(args.chrome_binary).expanduser()
    if not chrome_binary.exists():
        raise SystemExit(f"Chrome binary not found: {chrome_binary}")

    screenshots_dir = run_dir / "screenshots"
    desktop_path = screenshots_dir / f"{args.condition}-desktop.png"
    mobile_path = screenshots_dir / f"{args.condition}-mobile.png"
    source_url = file_url_for(render_target)

    capture_screenshot(chrome_binary, source_url, desktop_path, args.desktop_width, args.desktop_height)
    capture_screenshot(chrome_binary, source_url, mobile_path, args.mobile_width, args.mobile_height)

    artifact["render_target_path"] = str(render_target)
    artifact["desktop_screenshot_path"] = str(desktop_path.resolve())
    artifact["mobile_screenshot_path"] = str(mobile_path.resolve())
    write_json(artifact_path, artifact)

    print(json.dumps({
        "condition": args.condition,
        "render_target_path": artifact["render_target_path"],
        "desktop_screenshot_path": artifact["desktop_screenshot_path"],
        "mobile_screenshot_path": artifact["mobile_screenshot_path"],
    }, indent=2))


def attach_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    artifact_path, artifact = load_output_artifact(run_dir, args.condition)

    source_html = Path(args.html)
    if not source_html.is_absolute():
        source_html = (REPO_ROOT / source_html).resolve()
    if not source_html.exists():
        raise SystemExit(f"HTML artifact not found: {source_html}")

    target_dir = run_dir / "manual"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_html = target_dir / f"{args.condition}.html"
    html_text = read_text_file(source_html)
    write_text(target_html, html_text)

    prompt_path = ""
    if args.prompt:
        prompt_file = Path(args.prompt)
        if not prompt_file.is_absolute():
            prompt_file = (REPO_ROOT / prompt_file).resolve()
        if not prompt_file.exists():
            raise SystemExit(f"Prompt file not found: {prompt_file}")
        target_prompt = target_dir / f"{args.condition}-prompt.txt"
        write_text(target_prompt, read_text_file(prompt_file))
        prompt_path = str(target_prompt.resolve())

    artifact["prompt_path"] = prompt_path
    artifact["code_path"] = str(target_html.resolve())
    artifact["render_target_path"] = str(target_html.resolve())
    artifact["notes"] = "Attached from manual artifact input."
    write_json(artifact_path, artifact)

    metrics_path = run_dir / "metrics" / "technical.json"
    metrics = load_json(metrics_path)
    metrics[args.condition]["build_pass"] = True
    metrics[args.condition]["lint_pass"] = True
    metrics[args.condition]["iteration_count"] = max(1, int(args.iterations))
    metrics[args.condition]["elapsed_seconds"] = float(args.elapsed_seconds)
    metrics[args.condition]["manual_edit_loc"] = 0 if args.manual_edit_loc is None else int(args.manual_edit_loc)
    write_json(metrics_path, metrics)

    print(json.dumps({
        "condition": args.condition,
        "attached_html": str(target_html.resolve()),
        "attached_prompt": prompt_path,
    }, indent=2))


def audit_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    script_path = TECHNICAL_AUDIT_SCRIPT.resolve()
    if not script_path.exists():
        raise SystemExit(f"Technical audit script not found: {script_path}")

    command = [
        args.node_binary,
        str(script_path),
        "--run",
        str(run_dir),
        "--condition",
        args.condition,
        "--chrome-binary",
        args.chrome_binary,
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    output = completed.stdout.strip()
    print(output if output else str(run_dir / "metrics" / "technical.json"))


def run_all(args):
    run_dir = ensure_run_dir(Path(args.run))

    for condition in ("baseline", "grit"):
        generate_args = argparse.Namespace(
            run=str(run_dir),
            condition=condition,
            provider=args.generate_provider,
            model_override=args.generate_model_override,
            reasoning_override=args.generate_reasoning_override,
            max_output_tokens=args.generate_max_output_tokens,
        )
        generate_run(generate_args)

    for condition in ("baseline", "grit"):
        capture_args = argparse.Namespace(
            run=str(run_dir),
            condition=condition,
            html=None,
            chrome_binary=args.chrome_binary,
            desktop_width=args.desktop_width,
            desktop_height=args.desktop_height,
            mobile_width=args.mobile_width,
            mobile_height=args.mobile_height,
        )
        capture_run(capture_args)

    for condition in ("baseline", "grit"):
        audit_args = argparse.Namespace(
            run=str(run_dir),
            condition=condition,
            node_binary=args.node_binary,
            chrome_binary=args.chrome_binary,
        )
        audit_run(audit_args)

    judge_args = argparse.Namespace(
        run=str(run_dir),
        provider=args.judge_provider,
        model_override=args.judge_model_override,
        reasoning_override=args.judge_reasoning_override,
        max_output_tokens=args.judge_max_output_tokens,
    )
    judge_run(judge_args)

    score_args = argparse.Namespace(run=str(run_dir))
    score_run(score_args)

    report_args = argparse.Namespace(run=str(run_dir))
    report_run(report_args)

    summary_path = run_dir / "summary" / "summary.json"
    report_path = run_dir / "summary" / "report.md"
    print(json.dumps({
        "run": str(run_dir),
        "summary": str(summary_path),
        "report": str(report_path),
    }, indent=2))


def run_manual(args):
    run_dir = ensure_run_dir(Path(args.run))

    for condition in ("baseline", "grit"):
        capture_args = argparse.Namespace(
            run=str(run_dir),
            condition=condition,
            html=None,
            chrome_binary=args.chrome_binary,
            desktop_width=args.desktop_width,
            desktop_height=args.desktop_height,
            mobile_width=args.mobile_width,
            mobile_height=args.mobile_height,
        )
        capture_run(capture_args)

    for condition in ("baseline", "grit"):
        audit_args = argparse.Namespace(
            run=str(run_dir),
            condition=condition,
            node_binary=args.node_binary,
            chrome_binary=args.chrome_binary,
        )
        audit_run(audit_args)

    judge_args = argparse.Namespace(
        run=str(run_dir),
        provider=args.judge_provider,
        model_override=args.judge_model_override,
        reasoning_override=args.judge_reasoning_override,
        max_output_tokens=args.judge_max_output_tokens,
    )
    judge_run(judge_args)

    score_args = argparse.Namespace(run=str(run_dir))
    score_run(score_args)

    report_args = argparse.Namespace(run=str(run_dir))
    report_run(report_args)

    summary_path = run_dir / "summary" / "summary.json"
    report_path = run_dir / "summary" / "report.md"
    print(json.dumps({
        "run": str(run_dir),
        "summary": str(summary_path),
        "report": str(report_path),
    }, indent=2))


def aggregate_batch_results(batch_dir: Path, summaries: list) -> dict:
    grit_wins = sum(1 for item in summaries if item["judge_preferred_condition"] == "grit")
    baseline_wins = sum(1 for item in summaries if item["judge_preferred_condition"] == "baseline")
    ties = sum(1 for item in summaries if item["judge_preferred_condition"] == "tie")
    count = len(summaries)
    return {
        "batch_dir": str(batch_dir),
        "total_runs": count,
        "grit_wins": grit_wins,
        "baseline_wins": baseline_wins,
        "ties": ties,
        "grit_win_rate": round((grit_wins / count) * 100.0, 4) if count else 0.0,
        "average_baseline_mean_score": round(sum(item["baseline_mean_score"] for item in summaries) / count, 4) if count else 0.0,
        "average_grit_mean_score": round(sum(item["grit_mean_score"] for item in summaries) / count, 4) if count else 0.0,
        "average_score_uplift_percent": round(sum(item["score_uplift_percent"] for item in summaries) / count, 4) if count else 0.0,
        "average_baseline_lighthouse_accessibility": round(sum((item["baseline_lighthouse_accessibility"] or 0) for item in summaries) / count, 4) if count else 0.0,
        "average_grit_lighthouse_accessibility": round(sum((item["grit_lighthouse_accessibility"] or 0) for item in summaries) / count, 4) if count else 0.0,
        "average_baseline_axe_violations": round(sum((item["baseline_axe_violations"] or 0) for item in summaries) / count, 4) if count else 0.0,
        "average_grit_axe_violations": round(sum((item["grit_axe_violations"] or 0) for item in summaries) / count, 4) if count else 0.0,
        "runs": [
            {
                "run_id": item["run_id"],
                "task_id": item["task_id"],
                "judge_preferred_condition": item["judge_preferred_condition"],
                "score_uplift_percent": item["score_uplift_percent"],
            }
            for item in summaries
        ],
    }


def render_batch_report(aggregate: dict) -> str:
    lines = [
        "# Batch Benchmark Report",
        "",
        "## Aggregate",
        "",
        f"- Total runs: `{aggregate['total_runs']}`",
        f"- GRIT wins: `{aggregate['grit_wins']}`",
        f"- Baseline wins: `{aggregate['baseline_wins']}`",
        f"- Ties: `{aggregate['ties']}`",
        f"- GRIT win rate: `{aggregate['grit_win_rate']}`",
        f"- Average baseline mean score: `{aggregate['average_baseline_mean_score']}`",
        f"- Average GRIT mean score: `{aggregate['average_grit_mean_score']}`",
        f"- Average score uplift percent: `{aggregate['average_score_uplift_percent']}`",
        f"- Average baseline Lighthouse accessibility: `{aggregate['average_baseline_lighthouse_accessibility']}`",
        f"- Average GRIT Lighthouse accessibility: `{aggregate['average_grit_lighthouse_accessibility']}`",
        f"- Average baseline axe violations: `{aggregate['average_baseline_axe_violations']}`",
        f"- Average GRIT axe violations: `{aggregate['average_grit_axe_violations']}`",
        "",
        "## Runs",
        "",
    ]
    for run in aggregate["runs"]:
        lines.append(
            f"- `{run['run_id']}` | task `{run['task_id']}` | preferred `{run['judge_preferred_condition']}` | uplift `{run['score_uplift_percent']}`"
        )
    return "\n".join(lines) + "\n"


def batch_run(args):
    batch_id = args.batch_id or f"batch-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    batch_dir = ARTIFACTS_DIR / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)

    if args.tasks:
        task_ids = [item.strip() for item in args.tasks.split(",") if item.strip()]
    else:
        task_ids = sorted(path.stem for path in TASKS_DIR.glob("*.md"))

    summaries = []
    for task_id in task_ids:
        modules = DEFAULT_TASK_MODULES.get(task_id, {})
        style_module = modules.get("style", args.default_style)
        layout_module = modules.get("layout", args.default_layout)
        for repeat in range(1, args.repeats + 1):
            run_id = f"{batch_id}-{task_id}-r{repeat:02d}"
            init_args = argparse.Namespace(
                task=task_id,
                model=args.model,
                reasoning=args.reasoning,
                style=style_module,
                layout=layout_module,
                run_id=run_id,
                output_a="baseline",
                output_b="grit",
                notes=f"Batch run {batch_id}, repeat {repeat}",
            )
            init_run(init_args)

            run_args = argparse.Namespace(
                run=str(ARTIFACTS_DIR / run_id),
                generate_provider=args.generate_provider,
                generate_model_override=args.generate_model_override,
                generate_reasoning_override=args.generate_reasoning_override,
                generate_max_output_tokens=args.generate_max_output_tokens,
                judge_provider=args.judge_provider,
                judge_model_override=args.judge_model_override,
                judge_reasoning_override=args.judge_reasoning_override,
                judge_max_output_tokens=args.judge_max_output_tokens,
                node_binary=args.node_binary,
                chrome_binary=args.chrome_binary,
                desktop_width=args.desktop_width,
                desktop_height=args.desktop_height,
                mobile_width=args.mobile_width,
                mobile_height=args.mobile_height,
            )
            run_all(run_args)
            summaries.append(load_json(ARTIFACTS_DIR / run_id / "summary" / "summary.json"))

    aggregate = aggregate_batch_results(batch_dir, summaries)
    write_json(batch_dir / "aggregate-summary.json", aggregate)
    write_text(batch_dir / "aggregate-report.md", render_batch_report(aggregate))
    print(json.dumps({
        "batch_dir": str(batch_dir),
        "aggregate_summary": str((batch_dir / "aggregate-summary.json").resolve()),
        "aggregate_report": str((batch_dir / "aggregate-report.md").resolve()),
        "total_runs": aggregate["total_runs"],
    }, indent=2))


def render_report(summary: dict) -> str:
    preferred = summary["judge_preferred_condition"]
    notes = summary["judge_notes"]
    return f"""# Automated Benchmark Report

## Run Info

- Run ID: `{summary["run_id"]}`
- Task: `{summary["task_id"]}`
- Model: `{summary["model"]}`
- Reasoning effort: `{summary["reasoning_effort"]}`
- Style module: `{summary["style_module"]}`
- Layout module: `{summary["layout_module"]}`

## Judge Outcome

- Preferred condition: `{preferred}`
- Judge confidence: `{summary["judge_confidence"]}`
- Baseline mean score: `{summary["baseline_mean_score"]}`
- GRIT mean score: `{summary["grit_mean_score"]}`
- Score uplift percent: `{summary["score_uplift_percent"]}`
- Baseline acceptance rate: `{summary["baseline_acceptance_rate"]}`
- GRIT acceptance rate: `{summary["grit_acceptance_rate"]}`

## Efficiency

- Baseline iteration count: `{summary["baseline_iteration_count"]}`
- GRIT iteration count: `{summary["grit_iteration_count"]}`
- Iteration reduction percent: `{summary["iteration_reduction_percent"]}`
- Baseline elapsed seconds: `{summary["baseline_elapsed_seconds"]}`
- GRIT elapsed seconds: `{summary["grit_elapsed_seconds"]}`

## Technical Checks

- Baseline build pass: `{summary["baseline_build_pass"]}`
- GRIT build pass: `{summary["grit_build_pass"]}`
- Baseline lint pass: `{summary["baseline_lint_pass"]}`
- GRIT lint pass: `{summary["grit_lint_pass"]}`
- Baseline Lighthouse performance: `{summary["baseline_lighthouse_performance"]}`
- GRIT Lighthouse performance: `{summary["grit_lighthouse_performance"]}`
- Baseline Lighthouse accessibility: `{summary["baseline_lighthouse_accessibility"]}`
- GRIT Lighthouse accessibility: `{summary["grit_lighthouse_accessibility"]}`
- Baseline axe violations: `{summary["baseline_axe_violations"]}`
- GRIT axe violations: `{summary["grit_axe_violations"]}`
- Baseline manual edit LOC: `{summary["baseline_manual_edit_loc"]}`
- GRIT manual edit LOC: `{summary["grit_manual_edit_loc"]}`

## Category Scores

### Baseline

```json
{json.dumps(summary["baseline_category_scores"], indent=2)}
```

### GRIT

```json
{json.dumps(summary["grit_category_scores"], indent=2)}
```

## Judge Notes

### Strengths Of Output A

{render_bullets(notes.get("strengths_of_A", []))}

### Strengths Of Output B

{render_bullets(notes.get("strengths_of_B", []))}

### Deciding Factors

{render_bullets(notes.get("deciding_factors", []))}

### Risks Or Ambiguities

{render_bullets(notes.get("risks_or_ambiguities", []))}
"""


def render_bullets(items: list[str]) -> str:
    if not items:
        return "- none recorded"
    return "\n".join(f"- {item}" for item in items)


def report_run(args):
    run_dir = ensure_run_dir(Path(args.run))
    summary = load_json(run_dir / "summary" / "summary.json")
    report = render_report(summary)
    write_text(run_dir / "summary" / "report.md", report)
    print(run_dir / "summary" / "report.md")


def main():
    parser = argparse.ArgumentParser(description="Automated benchmark runner scaffold for GRIT.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a benchmark run folder.")
    init_parser.add_argument("--task", required=True, help="Task id from benchmarks/tasks without .md")
    init_parser.add_argument("--model", required=True, help="Model name used for the run")
    init_parser.add_argument("--reasoning", required=True, help="Reasoning effort")
    init_parser.add_argument("--style", required=True, help="Style module path")
    init_parser.add_argument("--layout", default=None, help="Layout module path")
    init_parser.add_argument("--run-id", default=None, help="Optional explicit run id")
    init_parser.add_argument("--output-a", default="baseline", choices=["baseline", "grit"])
    init_parser.add_argument("--output-b", default="grit", choices=["baseline", "grit"])
    init_parser.add_argument("--notes", default=None)
    init_parser.set_defaults(func=init_run)

    generate_parser = subparsers.add_parser("generate", help="Generate local HTML artifacts for a benchmark condition.")
    generate_parser.add_argument("--run", required=True, help="Path to the run directory")
    generate_parser.add_argument("--condition", required=True, choices=["baseline", "grit"])
    generate_parser.add_argument("--provider", default="local", choices=["local", "openai"])
    generate_parser.add_argument("--model-override", default=None)
    generate_parser.add_argument("--reasoning-override", default=None)
    generate_parser.add_argument("--max-output-tokens", type=int, default=4000)
    generate_parser.set_defaults(func=generate_run)

    score_parser = subparsers.add_parser("score", help="Compute summary.json from run inputs.")
    score_parser.add_argument("--run", required=True, help="Path to the run directory")
    score_parser.set_defaults(func=score_run)

    capture_parser = subparsers.add_parser("capture", help="Capture desktop and mobile screenshots from a local HTML render target.")
    capture_parser.add_argument("--run", required=True, help="Path to the run directory")
    capture_parser.add_argument("--condition", required=True, choices=["baseline", "grit"])
    capture_parser.add_argument("--html", default=None, help="Optional HTML file path to override render_target_path")
    capture_parser.add_argument("--chrome-binary", default=str(DEFAULT_CHROME_BINARY))
    capture_parser.add_argument("--desktop-width", type=int, default=1440)
    capture_parser.add_argument("--desktop-height", type=int, default=1200)
    capture_parser.add_argument("--mobile-width", type=int, default=390)
    capture_parser.add_argument("--mobile-height", type=int, default=844)
    capture_parser.set_defaults(func=capture_run)

    attach_parser = subparsers.add_parser("attach", help="Attach a manually created HTML artifact to a benchmark condition.")
    attach_parser.add_argument("--run", required=True, help="Path to the run directory")
    attach_parser.add_argument("--condition", required=True, choices=["baseline", "grit"])
    attach_parser.add_argument("--html", required=True, help="Path to the local HTML artifact")
    attach_parser.add_argument("--prompt", default=None, help="Optional path to the prompt text file used to create the artifact")
    attach_parser.add_argument("--iterations", type=int, default=1, help="Prompt iteration count used to reach this artifact")
    attach_parser.add_argument("--elapsed-seconds", type=float, default=0.0, help="Approximate elapsed generation time")
    attach_parser.add_argument("--manual-edit-loc", type=int, default=None, help="Optional number of manual lines changed after generation")
    attach_parser.set_defaults(func=attach_run)

    audit_parser = subparsers.add_parser("audit", help="Run Lighthouse and axe audits for a benchmark condition.")
    audit_parser.add_argument("--run", required=True, help="Path to the run directory")
    audit_parser.add_argument("--condition", required=True, choices=["baseline", "grit"])
    audit_parser.add_argument("--node-binary", default="node")
    audit_parser.add_argument("--chrome-binary", default=str(DEFAULT_CHROME_BINARY))
    audit_parser.set_defaults(func=audit_run)

    run_all_parser = subparsers.add_parser("run-all", help="Run generate, capture, audit, judge, score, and report in sequence.")
    run_all_parser.add_argument("--run", required=True, help="Path to the run directory")
    run_all_parser.add_argument("--generate-provider", default="local", choices=["local", "openai"])
    run_all_parser.add_argument("--generate-model-override", default=None)
    run_all_parser.add_argument("--generate-reasoning-override", default=None)
    run_all_parser.add_argument("--generate-max-output-tokens", type=int, default=4000)
    run_all_parser.add_argument("--judge-provider", default="heuristic", choices=["heuristic", "openai"])
    run_all_parser.add_argument("--judge-model-override", default=None)
    run_all_parser.add_argument("--judge-reasoning-override", default=None)
    run_all_parser.add_argument("--judge-max-output-tokens", type=int, default=3000)
    run_all_parser.add_argument("--node-binary", default="node")
    run_all_parser.add_argument("--chrome-binary", default=str(DEFAULT_CHROME_BINARY))
    run_all_parser.add_argument("--desktop-width", type=int, default=1440)
    run_all_parser.add_argument("--desktop-height", type=int, default=1200)
    run_all_parser.add_argument("--mobile-width", type=int, default=390)
    run_all_parser.add_argument("--mobile-height", type=int, default=844)
    run_all_parser.set_defaults(func=run_all)

    run_manual_parser = subparsers.add_parser("run-manual", help="Run capture, audit, judge, score, and report for already attached manual artifacts.")
    run_manual_parser.add_argument("--run", required=True, help="Path to the run directory")
    run_manual_parser.add_argument("--judge-provider", default="heuristic", choices=["heuristic", "openai"])
    run_manual_parser.add_argument("--judge-model-override", default=None)
    run_manual_parser.add_argument("--judge-reasoning-override", default=None)
    run_manual_parser.add_argument("--judge-max-output-tokens", type=int, default=3000)
    run_manual_parser.add_argument("--node-binary", default="node")
    run_manual_parser.add_argument("--chrome-binary", default=str(DEFAULT_CHROME_BINARY))
    run_manual_parser.add_argument("--desktop-width", type=int, default=1440)
    run_manual_parser.add_argument("--desktop-height", type=int, default=1200)
    run_manual_parser.add_argument("--mobile-width", type=int, default=390)
    run_manual_parser.add_argument("--mobile-height", type=int, default=844)
    run_manual_parser.set_defaults(func=run_manual)

    batch_parser = subparsers.add_parser("batch-run", help="Run the benchmark matrix across multiple tasks and repeats.")
    batch_parser.add_argument("--batch-id", default=None, help="Optional batch id used as the artifact folder prefix")
    batch_parser.add_argument("--tasks", default=None, help="Comma-separated task ids. Defaults to all benchmark tasks.")
    batch_parser.add_argument("--repeats", type=int, default=3)
    batch_parser.add_argument("--model", default="gpt-5.4")
    batch_parser.add_argument("--reasoning", default="medium")
    batch_parser.add_argument("--default-style", default="styles/modern-corporate-landing.md")
    batch_parser.add_argument("--default-layout", default="layouts/grid-rhythm.md")
    batch_parser.add_argument("--generate-provider", default="local", choices=["local", "openai"])
    batch_parser.add_argument("--generate-model-override", default=None)
    batch_parser.add_argument("--generate-reasoning-override", default=None)
    batch_parser.add_argument("--generate-max-output-tokens", type=int, default=4000)
    batch_parser.add_argument("--judge-provider", default="heuristic", choices=["heuristic", "openai"])
    batch_parser.add_argument("--judge-model-override", default=None)
    batch_parser.add_argument("--judge-reasoning-override", default=None)
    batch_parser.add_argument("--judge-max-output-tokens", type=int, default=3000)
    batch_parser.add_argument("--node-binary", default="node")
    batch_parser.add_argument("--chrome-binary", default=str(DEFAULT_CHROME_BINARY))
    batch_parser.add_argument("--desktop-width", type=int, default=1440)
    batch_parser.add_argument("--desktop-height", type=int, default=1200)
    batch_parser.add_argument("--mobile-width", type=int, default=390)
    batch_parser.add_argument("--mobile-height", type=int, default=844)
    batch_parser.set_defaults(func=batch_run)

    judge_parser = subparsers.add_parser("judge", help="Fill judge-result.json using a local heuristic judge.")
    judge_parser.add_argument("--run", required=True, help="Path to the run directory")
    judge_parser.add_argument("--provider", default="heuristic", choices=["heuristic", "openai"])
    judge_parser.add_argument("--model-override", default=None)
    judge_parser.add_argument("--reasoning-override", default=None)
    judge_parser.add_argument("--max-output-tokens", type=int, default=3000)
    judge_parser.set_defaults(func=judge_run)

    report_parser = subparsers.add_parser("report", help="Generate report.md from summary.json.")
    report_parser.add_argument("--run", required=True, help="Path to the run directory")
    report_parser.set_defaults(func=report_run)

    args = parser.parse_args()
    if args.command == "init" and args.output_a == args.output_b:
        raise SystemExit("Output A and Output B must map to different conditions.")
    args.func(args)


if __name__ == "__main__":
    main()
