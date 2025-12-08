import os
import markdown2
from jinja2 import Template
from typing import Dict, Any
from .utils import logger

DEFAULT_TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>LLM Security Report</title></head>
<body>
<h1>LLM Security Tool — Report</h1>
<p><strong>Model:</strong> {{ model }}</p>
<h2>Summary</h2>
<p>{{ summary }}</p>

{% for section in sections %}
  <h3>{{ section.title }}</h3>
  {% for item in section.items %}
    <pre>{{ item | e }}</pre>
  {% endfor %}
{% endfor %}

<h2>Mitigations</h2>
<ul>
  {% for m in mitigations %}
    <li>{{ m }}</li>
  {% endfor %}
</ul>
</body>
</html>
"""

def generate_md(results: Dict[str, Any], model: str, out_path: str):
    lines = []
    lines.append(f"# LLM Security Report\n\n**Model**: {model}\n\n")
    # Summary
    lines.append("## Summary\n")
    lines.append(results.get("summary", "No summary provided.") + "\n\n")
    # sections
    for k, v in results.items():
        if k == "summary":
            continue
        lines.append(f"## {k}\n")
        lines.append("```\n")
        import json
        lines.append(json.dumps(v, indent=2))
        lines.append("\n```\n")
    # mitigations
    lines.append("## Recommended mitigations\n")
    for m in results.get("mitigations", []):
        lines.append(f"- {m}\n")
    md = "".join(lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    logger.info("Wrote markdown report to %s", out_path)
    # also create HTML
    html = markdown2.markdown(md)
    html_path = os.path.splitext(out_path)[0] + ".html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info("Wrote HTML report to %s", html_path)
    return out_path, html_path

def generate_html_from_results(results: Dict[str, Any], model: str, out_path: str):
    template = Template(DEFAULT_TEMPLATE)
    html = template.render(model=model, summary=results.get("summary", ""), sections=results.get("sections", []), mitigations=results.get("mitigations", []))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info("Wrote HTML report to %s", out_path)
    return out_path
