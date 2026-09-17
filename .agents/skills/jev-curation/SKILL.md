---
name: jev-curation
description: Curate and expand the awesome-jev repository. Use when adding Jev projects or cases, collecting discussion evidence from X/Reddit/HN/blogs, promoting discussion items into main categories, refreshing README counts, or running periodic evidence sweeps.
---

# Jev Curation

Use this skill to maintain `awesome-jev` as a **strict, high-signal list of projects and practices built on Jev**.

## Goal

Keep the repository focused on two questions:

1. Where is Jev actually being used in public?
2. Which decision patterns transfer across domains?

This skill is for **curation**, not general AI news collection. Jev is a typed-decision model: `Choice`, `Score`, `Boolean`, each with confidence. Entries that do not involve a Jev decision do not belong here.

## Source of truth

Read these files before making changes:

- `README.md`
- `CONTRIBUTING.md`
- every file under `categories/`

`README.md` is the homepage aggregate, not the primary editing surface.
Update category files first, then refresh `README.md` from the current category files.
Always use `scripts/build-readme.py` instead of hand-editing the aggregate.

## Hard inclusion rules

Only include items that satisfy at least one of these:

- explicitly name `Jev` / `jev`
- explicitly cite TypeSafe AI's System One models
- clearly implement a typed-decision loop (typed question → typed answer + confidence → accept / reject / escalate)

And all of these:

- source is public and citable
- description is concrete
- entry stays **one sentence**
- item is **strictly Jev-relevant**, not a generic classifier, router, or LLM judge

Reject:

- generic classifiers, routers, or decision agents with no Jev involvement
- launch-hype commentary with no artifact
- private or uncitable claims
- things that need a paragraph to justify inclusion

## Category model

Use **main category pages** for stronger evidence such as:

- public repos
- project pages
- substantial write-ups
- benchmark or evaluation results

Use **`categories/related-practices-discussions.md`** for:

- X threads
- Reddit discussions
- Hacker News threads
- interviews
- blog mentions

when they show credible real practice signals but do not yet have a strong standalone repo or case page.

Main categories: classification-routing, verification-guardrails, scoring-ranking, agent-decisions, data-labeling-curation, evaluation-benchmarking, calibration-research, infra-sdks-integrations, related-practices-discussions.

Open categories still being seeded: content-moderation, compliance-legal, game-simulation, scientific-pipelines.

## Working strategy

### 1. Search broadly, classify narrowly

Preferred evidence channels:

- GitHub
- X / Twitter
- Reddit
- Hacker News
- Vercel AI Gateway / AI SDK ecosystem
- independent blogs / write-ups

### 2. Keep queries simple

Prefer medium-complexity searches such as:

- `jev typesafe`
- `typesafe-ai/jev`
- `jev Choice Score Boolean`
- `Jev System One Model`
- `jev classification routing`
- `jev verification guardrail`
- `Jev Diogo Almeida`

Avoid very long advanced-search expressions when the adapter is unstable.

### 3. Chinese + English

Search in both languages when useful. Useful Chinese patterns:

- `jev 大模型 决策`
- `TypeSafe Jev 分类`
- `Jev 类型化决策`

Keep Chinese queries narrow to avoid noisy generic matches.

## Promotion workflow

Use this exact ladder:

1. **Discussion lead found**
   - Add to `categories/related-practices-discussions.md` if it is credible and directly Jev-related.
2. **Evidence chain search**
   - Look for repo, project page, case page, or blog post.
3. **Promotion test**
   - Promote only if public evidence clearly shows a real Jev decision in use.
4. **Promote**
   - Move it into the best-fit main category.
5. **Deduplicate**
   - Remove the weaker discussion-only item if the main case now covers it.
6. **Refresh counts**
   - Run `scripts/build-readme.py` if category totals changed.

## Entry-writing rules

### Main categories

Format:

```md
- [Name](URL) - Industry: one-sentence description of the Jev use case.
```

Rules:

- one sentence only
- must mention the decision + the typed shape (`Choice` / `Score` / `Boolean`) + the gate or escalation
- prefer concrete verbs like `classifies`, `routes`, `gates`, `scores`, `verifies`
- include a number when the source provides one
- avoid hype

### Discussions page

Format:

```md
- [Name or thread title](URL) - Source/platform: one-sentence description of the Jev-related practice or discussion.
```

Rules:

- keep it factual
- describe the practice signal, not your opinion
- if it is mostly about transfer of the pattern, say that clearly

## Periodic maintenance loop

When invoked for a recurring sweep:

1. Read the current category files.
2. Search for 3-10 new public leads.
3. Filter aggressively.
4. Add only high-signal entries.
5. Attempt promotion for the strongest discussion leads.
6. Remove duplicates.
7. Recount category totals.
8. Refresh `README.md` so the homepage aggregate matches the current category files and counts.
9. Publish one short X post covering the round, then summarize what was added, promoted, and rejected.

## Suggested commands

Count entries:

```bash
python3 - <<'PY'
from pathlib import Path
for p in sorted(Path('categories').glob('*.md')):
    cnt = sum(1 for line in p.read_text().splitlines() if line.startswith('- ['))
    print(f'{p}:{cnt}')
PY
```

Example searches:

```bash
bb-browser site twitter/search 'jev typesafe' --json
bb-browser site google/search 'site:github.com "typesafe-ai/jev" OR "jev" typesafe | sed -n "1,120p"'
bb-browser site google/search 'site:news.ycombinator.com jev typesafe | sed -n "1,120p"'
bb-browser site google/search 'site:reddit.com jev typesafe model | sed -n "1,120p"'
opencli gh api repos/typesafe-ai/jev/readme
```

## Quality bar

**Promote slowly. Add discussions faster.**

If evidence is good but not strong enough for a main case, keep it in discussions.
Precision beats coverage. This model shipped in September 2026, so the corpus is small — resist padding it.

## Deliverable checklist

Before finishing, verify:

- entries are one sentence
- no generic classifiers or judges slipped in
- promoted items have stronger evidence than discussion-only items
- discussions page remains useful as a map of emerging practice
- README homepage aggregate matches the current category files

## Recommended invocation phrases

This skill should be used for prompts like:

- "继续搜集 awesome-jev"
- "做一轮 Jev 证据巡检"
- "把 discussions 里强条目升格"
- "更新 jev awesome list"
- "定期维护这个仓库"
