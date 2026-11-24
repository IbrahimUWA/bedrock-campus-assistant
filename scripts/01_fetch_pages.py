"""Step 1: download the public pages listed in data/sources.json as clean text.

Each page becomes data/pages/<slug>.md plus <slug>.md.metadata.json. The
sidecar file is the Bedrock Knowledge Base metadata format, so every
retrieved chunk carries its source URL and the answer can cite it.

Runs without AWS. Respects robots.txt and waits between requests.
"""
import datetime
import json
import re
import time
import urllib.robotparser
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "pages"
USER_AGENT = "campus-assistant-demo/1.0 (one-off educational fetch)"
DROP = ["script", "style", "noscript", "nav", "header", "footer", "form", "svg", "iframe", "aside", "button"]
BLOCKS = ["h1", "h2", "h3", "h4", "p", "li", "tr", "dt", "dd"]


def page_to_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    for tag in soup(DROP):
        tag.decompose()
    main = soup.find("main") or soup.body or soup
    lines, seen = [], set()
    for el in main.find_all(BLOCKS):
        # Skip containers whose text is repeated by a nested block.
        if el.name in ("li", "dd") and el.find(["p", "li"]):
            continue
        if el.name == "tr":
            text = " | ".join(c.get_text(" ", strip=True) for c in el.find_all(["th", "td"]))
        else:
            text = el.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) < 3 or text in seen:
            continue
        seen.add(text)
        if el.name in ("h1", "h2", "h3", "h4"):
            lines.append("\n" + "#" * int(el.name[1]) + " " + text + "\n")
        elif el.name == "li":
            lines.append("- " + text)
        else:
            lines.append(text)
    return title, "\n".join(lines).strip() + "\n"


def main() -> None:
    urls = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))["pages"]
    OUT.mkdir(parents=True, exist_ok=True)
    robots = {}
    today = datetime.date.today().isoformat()
    for url in urls:
        host = urlparse(url)
        base = f"{host.scheme}://{host.netloc}"
        if base not in robots:
            rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
            rp.read()
            robots[base] = rp
        if not robots[base].can_fetch(USER_AGENT, url):
            print(f"skip (robots.txt): {url}")
            continue
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()
        title, text = page_to_text(resp.text)
        slug = re.sub(r"[^a-z0-9]+", "-", host.path.strip("/").lower()).strip("-") or "home"
        (OUT / f"{slug}.md").write_text(f"# {title}\n\nSource: {resp.url}\n\n{text}", encoding="utf-8")
        meta = {"metadataAttributes": {"source_url": resp.url, "title": title, "fetched": today}}
        (OUT / f"{slug}.md.metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"{len(text.split()):>6} words  {slug}.md")
        time.sleep(1.5)


if __name__ == "__main__":
    main()
