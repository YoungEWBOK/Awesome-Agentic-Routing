# Contributing

## Scope

This list covers routing across independent models and agents: query-level model selection, cascades, capability representations, sequential routing, orchestration, and evaluation. Surveys and research software are included. Network routing and expert routing inside a single MoE model are outside the current scope.

## Paper entries

Edit `data/curated.json`, then run `python scripts/render_catalog.py` to regenerate the README and resource notes.

Each entry records the title, authors, first-release year, paper URL, venue, category, method, and task setting. Describe the method directly. Numerical results should include the dataset, model pool, metric, and comparison conditions if reported in the list.

Use publisher proceedings, ACL Anthology, OpenReview, or the authors' paper record for venue information. Label workshops and Findings separately from main-conference papers. An author-reported acceptance is marked with †. Use `arXiv YYYY` when no venue is recorded; this does not establish that the work is unpublished elsewhere.

## Code and resources

Add `code_url` only when a paper, author page, or repository README establishes the connection to that paper. Record the attribution URL in `code_source` and the check date in `code_checked_on`. Matching repository names alone is insufficient. Third-party implementations must be labeled separately.

Keep `code_url` null when no public implementation has been verified. A paper may report supplementary code without providing a public repository; record that distinction in `resource_note`. Model weights, datasets, and project pages can be added under `resources` when linked by the authors.

The README is a compact index. Longer methodological comparisons belong in `READING_GUIDE.zh-CN.md`; source and availability notes are rendered in `docs/resources.md`.

## arXiv updates

The workflow checks each Friday at **09:17 Asia/Shanghai (01:17 UTC)**. It searches when 14 local calendar days have elapsed since the last successful run. Manual runs search immediately and restart the interval. With initialization on 2026-11-06, the next scheduled search is expected on 2026-11-20.

New submissions are retrieved from the last successful search date with a seven-day overlap. Previously tracked papers are checked for revisions. Results are deduplicated by arXiv ID and screened using title/abstract keywords. `RECENT.md` contains the resulting reading queue; it is not automatically merged into the main list. Code attribution and venue changes are reviewed manually.

The initial search covers 35 days plus the overlap. Keyword filtering can miss relevant work or include unrelated papers. It does not discover every revision to an older, untracked paper. Search parameters are in `data/search.json`.

## Local commands

Python 3.9 or later is required. The scripts use the standard library.

```bash
python scripts/render_catalog.py
python -m unittest discover -s tests -v
python scripts/update_arxiv.py --dry-run
python scripts/update_arxiv.py
python scripts/update_arxiv.py --scheduled
```

## Workflow failures

The workflow uses `GITHUB_TOKEN` with `contents: write` and commits only `RECENT.md`, candidate metadata, and update state. It uses ordinary pushes and respects branch protection.

Failed requests, incomplete metadata, pagination errors, or result-limit errors stop the update without advancing the last successful search date. A failed push also leaves the remote update state unchanged. Inspect Actions logs and rerun **Biweekly arXiv update** after resolving the error. A concurrent branch update should be handled by rerunning from the new branch head, not by force-pushing.

GitHub may delay scheduled runs or disable schedules in inactive public repositories. Permission and branch-protection changes require explicit maintenance; the updater does not change them.

References: [arXiv API](https://info.arxiv.org/help/api/user-manual.html), [GitHub scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
