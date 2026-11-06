"""Render the paper index and resource notes from data/curated.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    ('surveys', 'Surveys', 'Surveys of model selection, cascading, and inference efficiency.'),
    ('prediction', 'Query routing: quality and cost prediction', 'The router selects a model before response generation, using predicted quality, cost, or latency.'),
    ('representation', 'Query routing: representations and transfer', 'These methods study query-model compatibility, capability profiles, or adaptation to new candidate models.'),
    ('cascading', 'Cascading and response verification', 'The policy observes an answer or confidence signal before deciding whether to stop or call another model.'),
    ('sequential', 'Sequential and budget-aware routing', 'Model choices are made across dialogue turns, task steps, or token-generation steps. Previous outputs, user history, and remaining resources enter different formulations.'),
    ('orchestration', 'Model and agent orchestration', 'The controller chooses model or tool calls, agent roles, or subtask assignments. The action space varies across papers.'),
    ('benchmarks', 'Benchmarks and evaluation', 'Evaluation resources for query-level selection and routing within agent trajectories.'),
    ('infrastructure', 'Software and infrastructure', 'Shared implementations and evaluation pipelines for routing research.'),
]


def anchor(text):
    return text.lower().replace(':', '').replace(' ', '-')


def cell(text):
    return text.replace('|', '&#124;').replace('\n', ' ')


def venue(p):
    text = p['publication'] + (' †' if p.get('publication_note') else '')
    return f"[{text}]({p['publication_url']})" if p.get('publication_url') else text


def render_readme(papers):
    checked = max(p['checked_on'] for p in papers)
    lines = ['# Awesome Agentic Routing', '',
             'Research on model selection, LLM routing, cascades, and agent orchestration.', '',
             '[中文阅读指南](READING_GUIDE.zh-CN.md) · [Code and other resources](docs/resources.md) · [Recent arXiv papers](RECENT.md) · [Contributing](CONTRIBUTING.md)', '',
             f'{len(papers)} papers · 2023–2026 · Updated {checked}', '',
             '## Contents', '']
    lines += [f'- [{heading}](#{anchor(heading)})' for _, heading, _ in SECTIONS]
    lines += ['', '## Scope and notation', '',
              'The list covers routing across independent models and agents, from single-query selection to decisions within multi-step tasks. Papers are grouped by their main decision setting; a method may also be relevant to other sections.', '',
              '**Venue** links to the publication record when available. **†** indicates acceptance reported by the authors. **arXiv** identifies the manuscript version when no venue is recorded here. **Code** links to author implementations; **—** means no public implementation was located in the checked sources. Dates refer to the linked records, not necessarily the first preprint.', '']
    for category, heading, description in SECTIONS:
        lines += ['## ' + heading, '', description, '',
                  '| Paper | Venue | Method / setting | Code |',
                  '| --- | --- | --- | --- |']
        for p in sorted((p for p in papers if p['category'] == category), key=lambda p: (-p['year'], p['name'])):
            title = p['title'].replace('E$^3$-Orch', 'E³-Orch')
            paper = f"**{p['name']}**<br>[{cell(title)}]({p['url']})"
            method = cell(p['method']) + '<br><sub>' + cell(p['setting']) + '</sub>'
            code = f"[GitHub]({p['code_url']})" if p.get('code_url') else '—'
            lines.append(f'| {paper} | {venue(p)} | {method} | {code} |')
        lines.append('')
    lines += ['## Reading and updates', '',
              'The [Chinese reading guide](READING_GUIDE.zh-CN.md) compares problem formulations, supervision, and evaluation. [Resource notes](docs/resources.md) include code provenance and available data, models, and project pages. The [coverage review](docs/coverage.md) records additions identified by comparison with related collections.', '',
              '[Recent arXiv papers](RECENT.md) are collected every two weeks. This feed is screened by keywords and kept separate from the main list; code links and publication changes are checked manually. The schedule and maintenance commands are documented in [CONTRIBUTING.md](CONTRIBUTING.md).', '',
              '## Related collections', '',
              '- [MilkThink-Lab / Awesome-Routing-LLMs](https://github.com/MilkThink-Lab/Awesome-Routing-LLMs) — a broader routing bibliography; its categorized tables informed the organization of this list.', '',
              'Corrections and paper suggestions are welcome through issues or pull requests.', '']
    return '\n'.join(lines)


def render_resources(papers):
    checked = max(p['code_checked_on'] for p in papers)
    lines = ['# Code, data, and source notes', '', '[Paper index](../README.md)', '',
             f'Links checked on {checked}. Author attribution was established from the paper, author page, or a repository README that identifies the paper. Availability does not imply that the implementation has been reproduced.', '',
             '## Author implementations', '', '| Paper | Code | Attribution source |', '| --- | --- | --- |']
    for p in sorted(papers, key=lambda p: p['name'].lower()):
        if p.get('code_url'):
            label = p['code_url'].removeprefix('https://github.com/')
            lines.append(f"| [{p['name']}]({p['url']}) | [{label}]({p['code_url']}) | [Source]({p['code_source']}) |")
    lines += ['', '## Additional resources', '', '| Paper | Resources |', '| --- | --- |']
    for p in papers:
        if p.get('resources'):
            links = ' · '.join(f"[{r['label']}]({r['url']})" for r in p['resources'])
            lines.append(f"| {p['name']} | {links} |")
    lines += ['', '## Resource notes', '']
    for p in papers:
        if p.get('resource_note'):
            lines.append(f"- **[{p['name']}]({p['url']})**: {p['resource_note']}")
    lines += ['', 'No verified implementation link is recorded for ' + ', '.join(p['name'] for p in papers if not p.get('code_url') and p['category'] != 'surveys') + '. Availability details are noted above where known; an unset link does not establish that code has never been released.', '',
              '## Publication records', '', '| Paper | Recorded venue / version |', '| --- | --- |']
    for p in sorted(papers, key=lambda p: p['name'].lower()):
        lines.append(f"| [{p['name']}]({p['url']}) | {venue(p)} |")
    lines += ['', '† Acceptance reported in the authors\' arXiv record. The full author lists and verification notes are retained in [the catalog](../data/curated.json).', '',
              'The JAIR record for *Doing More with Less* was checked against [Crossref](https://api.crossref.org/works/10.1613/jair.1.19801). FrugalGPT\'s TMLR publication and repository are also listed on [Lingjiao Chen\'s author page](https://lingjiaochen.com/).', '']
    return '\n'.join(lines)


def main():
    papers = json.loads((ROOT / 'data/curated.json').read_text(encoding='utf-8'))
    (ROOT / 'README.md').write_text(render_readme(papers), encoding='utf-8')
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/resources.md').write_text(render_resources(papers), encoding='utf-8')
    print(f'Rendered {len(papers)} papers and resource notes.')


if __name__ == '__main__':
    main()
