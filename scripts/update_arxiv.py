"""Discover arXiv reading candidates; never automatically promote them to curated.

Python 3.9+, standard library only. Run from any working directory.
"""
import argparse
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/", "x": "http://arxiv.org/schemas/atom"}
SHANGHAI = timezone(timedelta(hours=8))


def read_json(path, default=None):
    if not path.exists() and default is not None:
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalized_title(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


def parse_feed(raw):
    root = ET.fromstring(raw)
    if root.tag != "{" + NS["a"] + "}feed":
        raise ValueError("Expected an arXiv Atom feed")
    papers = []
    for entry in root.findall("a:entry", NS):
        def value(key):
            return " ".join((entry.findtext(key, default="", namespaces=NS)).split())
        identifier = value("a:id")
        match = re.fullmatch(r"https?://arxiv.org/abs/(\d{4}\.\d{4,5})(v\d+)?", identifier)
        if not match:
            raise ValueError("arXiv returned an error or unsupported identifier: " + identifier)
        title, published, updated = value("a:title"), value("a:published"), value("a:updated")
        if not title or not published or not updated:
            raise ValueError("Incomplete paper metadata: " + identifier)
        datetime.fromisoformat(published.replace("Z", "+00:00"))
        datetime.fromisoformat(updated.replace("Z", "+00:00"))
        papers.append({
            "arxiv_id": match[1], "version": match[2] or "",
            "title": title, "authors": [n.text for n in entry.findall("a:author/a:name", NS)],
            "published": published, "updated": updated,
            "url": "https://arxiv.org/abs/" + match[1],
            "abstract": value("a:summary"),
            "journal_ref": value("x:journal_ref"), "comment": value("x:comment"),
        })
    total = root.findtext("o:totalResults", namespaces=NS)
    if total is None:
        raise ValueError("Missing totalResults; refusing to treat a malformed feed as empty")
    return int(total), papers


class ArxivClient:
    def __init__(self):
        self.last_request = 0.0

    def fetch(self, params):
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        for attempt in range(3):
            time.sleep(max(0, 3.1 - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "Awesome-Agentic-Routing/1.0 (+https://github.com/YoungEWBOK/Awesome-Agentic-Routing)"})
                with urllib.request.urlopen(request, timeout=45) as response:
                    return parse_feed(response.read())
            except (OSError, ValueError, ET.ParseError):
                if attempt == 2:
                    raise
                time.sleep(3 * (attempt + 1))


def search(client, query, config):
    papers, start = [], 0
    while True:
        total, page = client.fetch({"search_query": query, "start": start,
                                    "max_results": config["page_size"],
                                    "sortBy": "submittedDate", "sortOrder": "ascending"})
        if total > config["max_results"]:
            raise RuntimeError("Search exceeds configured result limit; narrow the date window before retrying")
        if start < total and not page:
            raise RuntimeError("Incomplete pagination; last successful search date will not advance")
        papers.extend(page)
        start += len(page)
        if start >= total:
            return papers


def relevance(paper):
    title = paper["title"].lower()
    text = title + " " + paper["abstract"].lower()
    routing = re.search(r"rout(?:e|er|ers|ing)|orchestrat|delegat|cascad|model selection|model recommendation", text)
    language = re.search(r"\bllms?\b|language models?", text)
    if not routing or not language:
        return None
    # Require selection among models/agents, rather than any use of routing in an LLM paper.
    selection = re.search(
        r"\b(?:llms?|language models?|models?|agents?)[ -]+(?:routing|router|selection|recommendation|cascad\w*)\b"
        r"|\b(?:routing|orchestration|orchestrator|delegation)\b.{0,65}\b(?:llms?|language models?|multi[- ]agent|agents)\b"
        r"|\b(?:multi[- ]model|multi[- ]llm|agentic|multi[- ]agent)[ -]+(?:routing|orchestrat\w*)\b",
        text)
    if not selection:
        return None
    internal = re.search(r"token|gradient routing|adapter routing|key routing|attention|mixture.of.experts|retriever routing|retrieval routing|peer routing|routing collisions|pcb routing|vision.language|unlearning|fine.tuning|time.series|circuit", title)
    explicit_model_routing = re.search(r"\b(?:llm|language model|multi[- ]model|agentic)[ -]+routing\b", title)
    if internal and not explicit_model_routing:
        return None
    if re.search(r"\bllm[- ]orchestrated\b", title) and not re.search(r"model selection|model routing|agent selection", paper["abstract"].lower()):
        return None
    focused_title = re.search(r"llm.{0,20}rout|model.{0,12}rout|rout.{0,16}llm|rout.{0,16}language.model|agent.{0,16}rout|multi.agent.{0,20}orchestrat|agentic.orchestrat|model.orchestrat|sub.agent.delegat|model selection|model recommendation", title)
    pool_selection = re.search(r"(?:select|choos|switch|assign|allocat|delegat|rout)\w*.{0,55}(?:models|agents)|(?:model|llm|agent) pool|heterogeneous (?:models|llms|agents)|multi.model|multi.llm", text)
    if not focused_title and not pool_selection:
        return None
    # A retrieval heuristic, not a scientific-quality score.
    if re.search(r"agent|multi.turn|multi.step|long.horizon|workflow|tool.use|tool.call", text):
        return "Agentic routing / orchestration"
    if re.search(r"survey|benchmark", title):
        return "Survey / evaluation"
    return "Model / LLM routing and cascading"


def due(now, state, interval):
    previous = state.get("last_success")
    if not previous:
        return True
    last_date = datetime.fromisoformat(previous).astimezone(SHANGHAI).date()
    return (now.astimezone(SHANGHAI).date() - last_date).days >= interval


def merge_candidates(existing, incoming, curated, today):
    curated_ids = {p.get("arxiv_id") for p in curated}
    curated_titles = {normalized_title(p["title"]) for p in curated}
    merged = {p["arxiv_id"]: p for p in existing
              if p["arxiv_id"] not in curated_ids and normalized_title(p["title"]) not in curated_titles}
    added, revised = 0, 0
    for paper in incoming:
        group = relevance(paper)
        if not group or paper["arxiv_id"] in curated_ids or normalized_title(paper["title"]) in curated_titles:
            merged.pop(paper["arxiv_id"], None)
            continue
        old = merged.get(paper["arxiv_id"])
        if old and old["updated"] > paper["updated"]:
            continue
        item = {k: v for k, v in paper.items() if k != "abstract"}
        item.update({"group": group, "status": "Pending reading; not a quality endorsement",
                     "first_seen": old["first_seen"] if old else today,
                     "abstract_excerpt": " ".join(paper["abstract"].split()[:24])})
        if old is None:
            added += 1
        elif item != old:
            revised += 1
        merged[paper["arxiv_id"]] = item
    return sorted(merged.values(), key=lambda p: (p["published"], p["arxiv_id"]), reverse=True), added, revised


def md(text):
    return html.escape(" ".join(text.split()), quote=False).replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;").replace("*", "&#42;").replace("_", "&#95;").replace("`", "&#96;")


def render_recent(papers, state):
    lines = ["# Recent arXiv candidates / 最新待读论文", "",
             "[Back to curated list](README.md) · [Reading guide](READING_GUIDE.zh-CN.md)", "",
             "Automatically retrieved across model routing, LLM routing, and agent routing/orchestration, then grouped by title/abstract keywords. Inclusion here is **not** a quality endorsement or evidence of peer review. Read the paper before promoting it to the curated list. False positives may appear; search is not exhaustive.", "",
             "自动检索仅负责发现与去重；这里的论文尚待精读，不等同于精选推荐。正式发表状态请以出版页面为准。", "",
             "Last successful search (UTC): " + state["last_success"],
             "Search window (new submissions): " + state["window_start"] + " — " + state["window_end"],
             "", "Already tracked candidates are also checked for revisions. Curated entries are maintained separately.", "",
             f"Tracking **{len(papers)}** candidates. Showing up to 30 most recently submitted papers per group; [all candidate metadata](data/candidates.json).", ""]
    if not papers:
        lines += ["No unreviewed candidates matched this search yet.", ""]
    for group in ["Agentic routing / orchestration", "Survey / evaluation", "Model / LLM routing and cascading"]:
        subset = [p for p in papers if p["group"] == group]
        if not subset:
            continue
        lines += ["## " + group, ""]
        for p in subset[:30]:
            authors = ", ".join(p["authors"][:3]) + (" et al." if len(p["authors"]) > 3 else "")
            lines += ["- **[" + md(p["title"]) + "](" + p["url"] + ")**",
                      "  - " + md(authors) + " · Submitted " + p["published"][:10] + " · Updated " + p["updated"][:10] + " · " + p["version"],
                      "  - Abstract excerpt (first 24 words): “" + md(p["abstract_excerpt"]) + "…”", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scheduled", action="store_true", help="Skip unless 14 local calendar days have elapsed")
    parser.add_argument("--dry-run", action="store_true", help="Query arXiv without writing files")
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    config = read_json(ROOT / "data/search.json")
    state = read_json(ROOT / "data/update_state.json", {})
    if args.scheduled and not due(now, state, config["interval_days"]):
        print("Not due: fewer than 14 days since the last successful search.")
        return
    previous = datetime.fromisoformat(state["last_success"]) if state.get("last_success") else now - timedelta(days=config["initial_lookback_days"])
    start = previous - timedelta(days=config["overlap_days"])
    query = config["query"] + " AND submittedDate:[" + start.strftime("%Y%m%d0000") + " TO " + now.strftime("%Y%m%d%H%M") + "]"
    curated = read_json(ROOT / "data/curated.json")
    existing = read_json(ROOT / "data/candidates.json", [])
    client = ArxivClient()
    incoming = search(client, query, config)
    # Revisions to older tracked candidates are not covered by submittedDate.
    ids = [p["arxiv_id"] for p in existing]
    for offset in range(0, len(ids), 100):
        batch = ids[offset:offset + 100]
        _, refreshed = client.fetch({"id_list": ",".join(batch), "max_results": len(batch)})
        if {p["arxiv_id"] for p in refreshed} != set(batch):
            raise RuntimeError("Incomplete revision lookup; retry without advancing the search date")
        incoming.extend(refreshed)
    candidates, added, revised = merge_candidates(existing, incoming, curated, now.date().isoformat())
    next_state = {"last_success": now.isoformat(timespec="seconds"),
                  "window_start": start.date().isoformat(), "window_end": now.date().isoformat(),
                  "fetched_records": len(incoming), "candidate_count": len(candidates),
                  "added": added, "revised": revised}
    report = f"arXiv search completed: {len(candidates)} candidates, {added} new, {revised} revised."
    print(report)
    if args.dry_run:
        return
    # Network and parsing must finish successfully before any persisted date changes.
    write_json(ROOT / "data/candidates.json", candidates)
    (ROOT / "RECENT.md").write_text(render_recent(candidates, next_state), encoding="utf-8")
    write_json(ROOT / "data/update_state.json", next_state)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as handle:
            handle.write(report + "\n\nSee RECENT.md. Candidates require reading before curation.\n")


if __name__ == "__main__":
    main()
