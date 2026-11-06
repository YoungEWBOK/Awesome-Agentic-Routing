"""Render the curated reading list from data/curated.json (no network)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    ("surveys", "Surveys"),
    ("foundations", "Foundations: model selection and cascading"),
    ("sequential", "Sequential and budget-aware agentic routing"),
    ("orchestration", "Multi-model and multi-agent orchestration"),
    ("capabilities", "Capability representation and experience"),
    ("evaluation", "Benchmarks and evaluation"),
]


def main():
    papers = json.loads((ROOT / "data/curated.json").read_text(encoding="utf-8"))
    lines = ["# Awesome Agentic Routing", "",
             "A curated reading list on choosing **which model or agent should act next**, under evolving task state, quality requirements, and resource constraints.", "",
             "[中文阅读路线](READING_GUIDE.zh-CN.md) · [Recent arXiv candidates](RECENT.md) · [Contributing and update policy](CONTRIBUTING.md) · [Machine-readable catalog](data/curated.json)", "",
             "Maintained by [YoungEWBOK](https://github.com/YoungEWBOK). Initial collection: **2023–2026**. Last editorial review: **" + max(p["checked_on"] for p in papers) + "**. **" + str(len(papers)) + " selected papers.**", "",
             "## Scope", "",
             "The core is routing **during** agent execution: selecting models, agents, or intelligent tools as the interaction changes. We also include the routing/cascading foundations and evaluation work needed to understand it. Model-internal MoE routing, network/PCB routing, and generic agent frameworks without a routing contribution are outside the main scope.", "",
             "| Decision | What changes? | Starting points |", "| --- | --- | --- |",
             "| Query routing | The model answering one input | RouteLLM, GraphRouter |",
             "| Cascading | Whether to stop or escalate after an answer | FrugalGPT |",
             "| Sequential routing | The next model, given history and budget | BAAR, MTRouter, DialRouter |",
             "| Orchestration | Calls, roles, subtasks, and their dependencies | Router-R1, MasRouter, ToolOrchestra, E³-Orch |",
             "| Evaluation | Whether a local replacement preserves final success | TwinRouterBench |", "",
             "These are reading categories, not mutually exclusive definitions. User dialogue turns, internal model calls, and environment interaction steps must be distinguished.", "",
             "## Start here", "",
             "1. **Dynamic Model Routing and Cascading** — read the design space and evaluation sections.",
             "2. **RouteLLM + FrugalGPT** — compare deciding before versus after generation.",
             "3. **BAAR + MTRouter** — understand path dependence, budgets, and outcome prediction.",
             "4. **SkillOrchestra** — compare explicit capability knowledge with learned routing policies.",
             "5. **TwinRouterBench** — examine static labels versus live downstream execution.",
             "6. **Router-R1 → ToolOrchestra → E³-Orch** — expand into learned orchestration.", "",
             "## How to read this list", "",
             "Selection reflects problem relevance, conceptual value, and inspectable evidence, not a numerical ranking or a guarantee of reproducibility. Each entry explains its contribution and a question worth checking. Initial review depth is metadata/abstract plus selected method sections; these are not reproduction reports.", "",
             "**Publication labels:** explicit venues are backed by a linked publication source or attributed to the authors' arXiv notice. **arXiv version** means we cite that version and have not independently established a publication venue; it does not assert the work has never been peer reviewed. Dates are first-release years, which may differ from venue years.", ""]
    for key, heading in SECTIONS:
        lines += ["## " + heading, ""]
        for p in papers:
            if p["category"] != key:
                continue
            author = p["authors"][0] + (" et al." if len(p["authors"]) > 1 else "")
            status = "[" + p["publication"] + "](" + p["publication_url"] + ")" if p.get("publication_url") else p["publication"]
            lines += ["### " + p["name"], "",
                      "**[" + p["title"] + "](" + p["url"] + ")**", "",
                      author + " · " + str(p["year"]) + " · " + status, "",
                      "- **Why read:** " + p["why_read"],
                      "- **Read critically:** " + p["reading_question"], ""]
    lines += ["## Biweekly arXiv discovery", "",
              "[The workflow](.github/workflows/arxiv-update.yml) checks on Fridays at **09:17 Asia/Shanghai (01:17 UTC)** and searches when at least 14 local calendar days have elapsed since the previous successful search. It can also be run manually from Actions. The first scheduled search after initialization on 2026-11-06 is expected on **2026-11-20**. GitHub may delay scheduled jobs.", "",
              "New matching papers are published to [RECENT.md](RECENT.md), with version-aware deduplication and a seven-day discovery overlap. Existing candidates are refreshed for revisions. The curated list is edited after reading; the automation does not certify scientific quality or promote candidates automatically. It uses the public arXiv API and GitHub's built-in workflow token, with no paid model API or extra secret required.", "",
              "A successful search updates its date even when it finds no new candidates. Failed or incomplete searches leave the last successful date unchanged. See [maintenance instructions](CONTRIBUTING.md) for limitations and recovery.", ""]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Rendered {len(papers)} curated entries.")


if __name__ == "__main__":
    main()
