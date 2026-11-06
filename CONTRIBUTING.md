# Curation and maintenance

## What belongs here

Prioritize a clear routing/orchestration research question, a useful conceptual contribution, and evidence that can be inspected in the paper. Favor papers with informative evaluations and available artifacts, but do not equate venue, popularity, or code availability with quality. Keep a manageable reading path.

Model routing, LLM routing, and agent routing/orchestration are all first-class topics. Include query-level selection, cascading, quality/cost/latency optimization, cold-start models, transfer, surveys, and evaluation. Exclude unrelated network routing, model-internal MoE routing, generic agent applications, and papers whose only connection is the word “agent”.

## Add or revise a curated paper

1. Read the primary paper page and relevant problem/method/evaluation sections. Record the exact title, authors, first-release year, stable arXiv ID when available, and source URL.
2. Verify any venue claim with the publication page or clearly label author-reported acceptance. An arXiv-linked version is not proof of either peer review or lack of peer review.
3. Add an entry to `data/curated.json`, with a concise `why_read` and a concrete `reading_question`. Set `checked_on` and honestly describe `review_depth`. Do not add headline numerical claims without their exact setting.
4. Run `python scripts/render_catalog.py`. Update the Chinese guide when the reading path changes.
5. If promoting a candidate, remove it from `data/candidates.json` and regenerate `RECENT.md` using `render_recent` and the existing update state, or run the updater. Do not modify `first_seen` simply because a paper has a new version.

The repository uses arXiv IDs and normalized titles for ordinary deduplication, and Git for change history. No custom content hashes or frozen research contracts are needed.

## Automatic discovery

The workflow runs on the default branch. Its Friday trigger is **01:17 UTC / 09:17 Asia/Shanghai**. Scheduled searches are due after 14 local calendar days since the last successful search. With initialization on 2026-11-06, the next expected search is 2026-11-20. A manual run searches immediately and resets that successful-search date.

The search covers new submissions since the previous successful run plus a seven-day overlap. On the initial run it covers 35 days plus the overlap. It retrieves all result pages within the configured limit, then filters title/abstract keywords into model/LLM routing, agentic routing, and survey/evaluation candidates. It also requests current metadata for all previously tracked candidates, catching revisions outside the new-submission window.

Titles, authors, dates, links, and short abstract excerpts appear in `RECENT.md`. Candidates are **pending reading**, not selected recommendations. Full abstracts are used in memory for filtering and are not republished. Discovery cannot guarantee recall: terminology changes, indexing lag, and keyword false positives are possible. Older untracked revised papers and curated venue/title changes require editorial review.

The Python scripts require **Python 3.9+**, with no third-party packages or LLM API keys. The workflow uses the repository's temporary `GITHUB_TOKEN` with `contents: write` to commit only the reading inbox and search state. It does not change repository security settings or bypass branch protection.

```bash
python -m unittest discover -s tests -v
python scripts/update_arxiv.py --dry-run
python scripts/update_arxiv.py
python scripts/update_arxiv.py --scheduled
python scripts/render_catalog.py
```

## Failure and recovery

- HTTP, parsing, incomplete pagination, missing tracked IDs, or result-limit failures cause a failed run. No successful-search date is advanced. Check Actions logs and rerun after resolving the error; a larger missed interval is recovered from the previous successful date.
- A failed scheduled search is retried on the following Friday, or immediately through **Actions → Biweekly arXiv update → Run workflow**. A successful manual run restarts the 14-day interval.
- A concurrent change to the default branch can make the bot's ordinary push fail. It does not force-push; rerun from the new branch head.
- If write permission or branch protection blocks the bot, the run will fail visibly. Adjust the publishing method deliberately; do not weaken protection automatically.
- GitHub can delay scheduled jobs and can disable schedules in inactive public repositories. Check the Actions page if updates stop. No external notification or email service is configured.

References: [arXiv API documentation](https://info.arxiv.org/help/api/user-manual.html), [GitHub scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
