#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"

# ---------------------------------------------------------------------------
# 可选标签（issue #138）
#
# 条目可以带一个可选的标签块，位置在链接与分隔符之间：
#
#   - [name](url) `{agent: pi, type: proxy}` - Description.
#
# 标签块放在分隔符之前而不是行尾：这样 `- [Name](URL) - Description` 的语法不变，
# 而且在分类文件里标签自成一列（描述会换行，放在行尾在源码里就看不见了）。
# 标签不是句子的一部分，所以「每条一句」的规则不受影响。
# ---------------------------------------------------------------------------

# agent：标签带色，同一种 agent 全表同色。色值锚定厂商品牌色后再压暗到
# 白字对比度 >= 4.5:1（WCAG AA）；原始品牌色都不达标（Anthropic 陶土 #D97757
# 与 OpenAI 绿 #10A37F 都是 2.9:1）。
AGENT_LABELS = {
    "multi":       ("Multi",       "1F6FEB"),
    "claude-code": ("Claude Code", "C1512C"),
    "pi":          ("Pi",          "8250DF"),
    "codex":       ("Codex",       "0D8668"),
    "cursor":      ("Cursor",      "BF3989"),
    "cline":       ("Cline",       "996C00"),
}

# `opencode` 曾经在这里，2026-09-22 移除。它是因为一次误判进来的：扫描把
# `jev-agent-skill` 描述里的 "OpenCode Zen's free tier" 当成了 OpenCode 编码 agent，
# 而那是该项目路由所用的 LLM 网关。该条目的地标签一直是 claude-code，全库也从未
# 有任何条目使用 opencode 标签 —— 所以词表里没有一条证据支持它。
# 真正出现 OpenCode 项目时再加回来（见 issue #154）。

# type：整个轴统一灰色 —— 只有 agent 承担色相，「用哪个 agent」才能扫得出来，
# 也避免两个 badge 看起来像两个同等分量的声明。
TYPE_LABELS = {
    "api", "cli", "proxy", "plugin", "library", "hosted", "self-hosted",
}
TYPE_COLOR = "4B5563"

ENTRY_RE = re.compile(r"^(- \[[^\]]+\]\([^)]+\))(?:\s*`\{([^}]*)\}`)?\s*-\s*(.+)$")


def parse_tags(raw: str) -> tuple[dict[str, str], list[str]]:
    """解析 `agent: pi, type: proxy`，返回 (标签, 未知项)。"""
    tags: dict[str, str] = {}
    unknown: list[str] = []
    for pair in raw.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if ":" not in pair:
            unknown.append(pair)
            continue
        kind, value = (part.strip().lower() for part in pair.split(":", 1))
        if kind == "agent" and value in AGENT_LABELS:
            tags["agent"] = value
        elif kind == "type" and value in TYPE_LABELS:
            tags["type"] = value
        else:
            unknown.append(f"{kind}: {value}")
    return tags, unknown


def badge_html(kind: str, value: str) -> str:
    if kind == "agent":
        label, color = AGENT_LABELS[value]
        text = "agent-" + label.replace(" ", "%20")
        alt = f"agent: {label}"
    else:
        color, text, alt = TYPE_COLOR, f"type-{value}", f"type: {value}"
    return f"![{alt}](https://img.shields.io/badge/{text}-{color}?style=flat-square)"


def render_entry(line: str) -> tuple[str, dict[str, str]]:
    """把条目里的标签块换成 badges，返回 (渲染后的行, 标签)。"""
    m = ENTRY_RE.match(line)
    if not m:
        return line, {}
    head, raw_tags, desc = m.group(1), m.group(2) or "", m.group(3)
    if not raw_tags:
        return line, {}
    tags, unknown = parse_tags(raw_tags)
    if unknown:
        print(f"⚠️  unknown tag(s) {unknown} — {line[:80]}")
    badges = " ".join(badge_html(k, tags[k]) for k in ("agent", "type") if k in tags)
    if not badges:
        return f"{head} - {desc}", {}
    return f"{head} {badges} - {desc}", tags

CATEGORIES = [
    "classification-routing.md",
    "adaptive-realtime-ui.md",
    "verification-guardrails.md",
    "scoring-ranking.md",
    "agent-decisions.md",
    "data-labeling-curation.md",
    "evaluation-benchmarking.md",
    "calibration-research.md",
    "infra-sdks-integrations.md",
    "game-simulation.md",
    "finance-trading.md",
    "compliance-legal.md",
    "content-moderation.md",
    "related-practices-discussions.md",
]

OPEN_TRACKING = [
    "scientific-pipelines.md",
]

ALL_FILES = CATEGORIES + OPEN_TRACKING


class Category:
    def __init__(self, filename: str, title: str, count: int, lines: list[str],
                 tagged: list[tuple[str, dict[str, str]]] | None = None) -> None:
        self.filename = filename
        self.title = title
        self.count = count
        self.lines = lines
        self.tagged = tagged or []

    @property
    def path(self) -> str:
        return f"categories/{self.filename}"


def github_anchor(title: str) -> str:
    anchor = title.strip().lower()
    anchor = re.sub(r"[^a-z0-9\- /]", "", anchor)
    anchor = anchor.replace("/", "-")
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


def pluralize(count: int) -> str:
    return "entry" if count == 1 else "entries"


def parse_category(filename: str) -> Category:
    path = REPO_ROOT / "categories" / filename
    lines = path.read_text().splitlines()

    try:
        title = next(line[2:].strip() for line in lines if line.startswith("# "))
    except StopIteration as exc:
        raise ValueError(f"missing title in {path}") from exc

    try:
        entries_index = lines.index("## Entries")
    except ValueError as exc:
        raise ValueError(f"missing '## Entries' section in {path}") from exc

    raw_entry_lines = lines[entries_index + 1 :]
    while raw_entry_lines and not raw_entry_lines[0].strip():
        raw_entry_lines.pop(0)
    while raw_entry_lines and not raw_entry_lines[-1].strip():
        raw_entry_lines.pop()

    count = sum(1 for line in raw_entry_lines if line.startswith("- ["))

    rendered: list[str] = []
    tagged: list[tuple[str, dict[str, str]]] = []
    previous_blank = False
    for line in raw_entry_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            if rendered and not previous_blank:
                rendered.append("")
                previous_blank = True
            continue
        if line.startswith("### "):
            rendered.append(line)
            previous_blank = False
            continue
        if line.startswith("- ["):
            out_line, tags = render_entry(line)
            rendered.append(out_line)
            if tags:
                name = re.match(r"- \[([^\]]+)\]\(([^)]+)\)", line)
                tagged.append(((name.group(1), name.group(2)) if name else (line, ""), tags))
            previous_blank = False

    while rendered and not rendered[-1].strip():
        rendered.pop()

    if count == 0:
        rendered = ["_No direct Jev examples added yet._"]

    return Category(filename=filename, title=title, count=count, lines=rendered, tagged=tagged)


def bullet_line(category: Category) -> str:
    return f"- [{category.title}]({category.path}) — {category.count} {pluralize(category.count)}"


def full_section(category: Category) -> list[str]:
    lines = [f"### {category.title}", "", f"Source file: [`{category.path}`]({category.path})", ""]
    lines.extend(category.lines)
    lines.append("")
    return lines


def check_duplicates(categories: dict[str, Category]) -> list[tuple[str, list[str]]]:
    """Find entries whose primary source URL appears in more than one category."""
    url_map: dict[str, list[str]] = {}
    for category in categories.values():
        for line in category.lines:
            if not line.startswith("- ["):
                continue
            m = re.search(r"\((https?://[^)\s]+)\)", line)
            if m:
                key = m.group(1).lower().rstrip("/")
                url_map.setdefault(key, []).append(category.filename)
    return [(url, files) for url, files in url_map.items() if len(files) > 1]


def build_readme() -> str:
    categories = {filename: parse_category(filename) for filename in ALL_FILES}

    open_categories = [categories[name] for name in OPEN_TRACKING]

    # ---------- duplicate detection ----------
    duplicates = check_duplicates(categories)
    if duplicates:
        print("⚠️  WARNING: duplicate sources detected:")
        for url, files in duplicates:
            print(f"    {url} appears in {', '.join(files)}")
        print()

    # ---------- build ----------
    non_empty = [
        category
        for category in categories.values()
        if category.count > 0 and category.filename not in OPEN_TRACKING
    ]

    out: list[str] = [
        "# awesome-jev",
        "",
        "<!-- Generated by scripts/build-readme.py. Edit category files, then rebuild README. -->",
        "",
        "A curated awesome list of public projects and practices built on [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), TypeSafe AI's System One model for typed decisions.",
        "",
        "This README is the homepage aggregate of the current category files, so the latest accepted entries are visible here without drilling into subpages.",
        "",
        "Jev is not a chat model. It takes unstructured state plus a **typed question** and returns a **typed decision** — a choice, a score, or a boolean, each with a confidence. That makes it a drop-in decision layer for software: classification, routing, rubric scoring, verification, and agent guardrails. This list tracks who is actually building with it, and which patterns transfer across industries.",
        "",
        "The repository treats all categories equally — each entry lives in exactly one category, chosen by its direct Jev application domain. A dedicated **Related Practices / Discussions** category captures credible public practice signals — X threads, Reddit discussions, and interviews — that describe real Jev usage even when no strong standalone case page exists yet.",
        "",
        "> [!WARNING]\n"
        "> **A listing is not an endorsement.** This project applies *inclusion* rules only — public, citable, genuinely uses Jev for a typed decision, one-sentence summary. It does **not** review code quality, security, maturity, or whether a project runs at all.\n"
        ">\n"
        "> **Treat same-day bulk submissions with particular care.** Several repositories published together by one author, sharing a scaffold and a thin commit history, can satisfy every inclusion rule and still be unproven. Volume is not evidence of quality. See [Curation is not endorsement](#curation-is-not-endorsement) for a checklist to run before adopting anything here.",
        "",
        "## Why this list",
        "",
        "Most Jev discussion is scattered across launch threads, model-gateway listings, and one-off prototypes. This list answers two practical questions quickly:",
        "",
        "- Where is Jev already making real decisions in production workflows?",
        "- Which decision patterns transfer across industries?",
        "",
        "This is not a comprehensive database. It is a high-signal, fast-scanning field guide.",
        "",
        "## Inclusion criteria",
        "",
        "An entry should meet all of the following:",
        "",
        "- The source is public and citable.",
        "- The example **uses Jev** (or a documented Jev port/derivative) for a concrete decision task — not a generic classifier, router, or LLM judge with no Jev involvement.",
        "- The source explicitly names `Jev`/`jev`, cites TypeSafe AI's System One models, or shows a typed-decision loop (typed question → typed answer with confidence → accept/reject/escalate).",
        "- The summary explains the scenario, method, and value in one sentence.",
        "",
        "We do **not** include:",
        "",
        "- Generic classifiers, routers, or research agents that merely resemble the pattern without using Jev.",
        "- Pure theory or opinion without a concrete practice.",
        "- Launch-hype commentary with no working artifact or reproducible result.",
        "- Long write-ups inside the list itself.",
        "- Sources that are private, inaccessible, or too vague to classify.",
        "",
        "## Curation is not endorsement",
        "",
        "Inclusion means one thing: the entry satisfies the inclusion rules above. It is not a quality review, a security audit, or a recommendation. We do not verify that a project compiles, that its tests pass, that its published numbers reproduce, or that its license permits your use.",
        "",
        "This matters most for projects that arrive in bulk. When one author releases several repositories on the same day, they commonly share a single scaffold — the same `AGENTS.md`, `CLAUDE.md`, `STATE.md`, and `CHANGELOG.md` — land in one or two commits each, and may ship considerably more prose than code. Such projects can be entirely legitimate; they are simply **unproven**. Treat them as leads, not as validated tools.",
        "",
        "Before adopting an entry, check it yourself:",
        "",
        "| Check | Why it matters |",
        "| --- | --- |",
        "| Does the code actually call the Jev API? | An entry can read well on a README alone. Look for a real request carrying typed questions, and a parsed answer coming back. |",
        "| Is there a runnable check? | A test, an example with expected output, or a public demo. No check means no evidence that it works. |",
        "| Do the numbers have a source? | Any accuracy, latency, cost, or volume figure should be traceable to the linked page. We strip claims we cannot verify, but the project page itself may still carry them. |",
        "| How much of the repository is code? | Some projects are mostly prompt documents. That can be legitimate — just know which one you are getting. |",
        "| Is there a license? | A few entries have none, which limits reuse and redistribution. |",
        "",
        "Found something wrong? Open an issue or a pull request — **removal is as valid a contribution as addition.** Rules for AI-assisted work, project depth, and submission rate live in [CONTRIBUTING.md](CONTRIBUTING.md#ai-assisted-work-and-bulk-submissions).",
        "",
        "## Current coverage",
        "",
    ]

    out.extend(
        bullet_line(category) for category in categories.values() if category.filename not in OPEN_TRACKING
    )
    out.extend(
        [
            "",
            "### Open categories still being seeded",
            "",
        ]
    )
    out.extend(bullet_line(category) for category in open_categories)
    out.extend(
        [
            "",
            "Each entry lives in exactly one category. When a project could fit multiple categories, we choose the one closest to its direct application domain.",
            "",
            "## Browse by category",
            "",
        ]
    )

    for category in non_empty:
        out.append(f"- [{category.title}](#{github_anchor(category.title)}) ([source]({category.path}))")

    # 「按 coding agent 检索」——标签存在时才有这一段。
    # 这是标签真正的用途：读者想知道「我手上跑的那个 agent 能不能用」，
    # 而不是想读一排 badge。
    by_agent: dict[str, list[tuple[str, str]]] = {}
    for category in non_empty:
        for (name, url), tags in category.tagged:
            if "agent" in tags:
                by_agent.setdefault(tags["agent"], []).append((name, url))

    if by_agent:
        out.extend(["", "## Find by coding agent", "",
                    "Optional tags on an entry name the coding agent it targets and the kind of integration it is. "
                    "Most entries carry none — they are added only when the source itself supports the classification.", ""])
        for agent in sorted(by_agent, key=lambda a: (-len(by_agent[a]), a)):
            label = AGENT_LABELS[agent][0]
            items = " · ".join(f"[{n}]({u})" for n, u in by_agent[agent])
            out.append(f"- **{label}** ({len(by_agent[agent])}) — {items}")

    out.extend(
        [
            "",
            "## Full list",
            "",
        ]
    )

    for category in non_empty:
        out.extend(full_section(category))

    out.extend(
        [
            "## Submission format",
            "",
            "Use exactly one line per entry:",
            "",
            "```md",
            "- [Name](URL) - Industry: one-sentence description of the Jev use case.",
            "```",
            "",
            "## How to contribute",
            "",
            "1. Pick the category that best matches the direct Jev application domain.",
            "2. Add a single-line entry in the required format to the category file, not directly to the README aggregate.",
            "3. Keep the summary concrete and scannable.",
            "4. Prefer examples that clearly show scenario + typed decision + value.",
            "",
            "See [CONTRIBUTING.md](CONTRIBUTING.md) for details.",
            "",
            "## License",
            "",
            "MIT",
            "",
        ]
    )

    return "\n".join(out)


def main() -> None:
    README_PATH.write_text(build_readme())


if __name__ == "__main__":
    main()
