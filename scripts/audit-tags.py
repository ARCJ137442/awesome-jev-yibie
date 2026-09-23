#!/usr/bin/env python3
"""Cross-check entry tags against what the entry text actually says.

Two directions, treated differently because the rules differ:

  error   a tagged entry whose name and description never mention the agent it
          claims. Tags are optional, but a tag that is present has to be
          supported by the source — that is the rule in CONTRIBUTING.md.

  notice  an untagged entry that does name an agent. Not a failure: tags are
          optional, and naming an agent is not the same as targeting it. It is
          printed so a reviewer can look, and so the gap is visible.

What this cannot do is decide whether a project *targets* the agent it
mentions. "OpenCode Zen's free tier" is a gateway an entry routes through, not
the OpenCode agent — see issue #154. This is the cheap check that runs first;
anything it cannot settle stays a human decision.

Usage: python3 scripts/audit-tags.py [categories_dir]
"""
from __future__ import annotations

import pathlib
import re
import sys

# What an entry must mention for the agent tag to be supported.
# `multi` is a judgement about breadth, so no single name can confirm it.
SUPPORT = {
    "claude-code": r"claude[ -]?code",
    "pi":          r"\bpi\b",
    "codex":       r"\bcodex\b",
    "cursor":      r"\bcursor\b",
    "cline":       r"\bcline\b",
    "multi":       None,
}

ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)(?:\s*`\{([^}]*)\}`)?\s*-\s*(.+)$")


def parse_tags(raw: str) -> dict[str, str]:
    tags = {}
    for pair in (raw or "").split(","):
        key, _, value = pair.partition(":")
        if key.strip():
            tags[key.strip()] = value.strip()
    return tags


def audit(root: pathlib.Path) -> tuple[list, list]:
    unsupported, unnoticed = [], []

    for path in sorted(root.glob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = ENTRY_RE.match(line)
            if not match:
                continue
            name, _url, raw, description = match.groups()
            agent = parse_tags(raw).get("agent")
            # The agent may be named in the entry title as well as the sentence.
            haystack = f"{name} {description}"

            if agent and SUPPORT.get(agent):
                if not re.search(SUPPORT[agent], haystack, re.I):
                    unsupported.append((name, agent, path.name))
            elif not agent:
                named = [
                    candidate
                    for candidate, pattern in SUPPORT.items()
                    if pattern and re.search(pattern, haystack, re.I)
                ]
                if named:
                    unnoticed.append((name, named, path.name))

    return unsupported, unnoticed


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[1] if len(argv) > 1 else "categories")
    if not root.is_dir():
        raise SystemExit(f"{root}: not a directory")

    unsupported, unnoticed = audit(root)

    for name, named, filename in unnoticed:
        print(f"notice: {name} ({filename}) mentions {', '.join(named)} but carries no tag")

    for name, agent, filename in unsupported:
        print(f"error: {name} ({filename}) is tagged {agent}, which its text does not mention")

    if unsupported:
        print(f"\n{len(unsupported)} tag(s) unsupported by the entry text.")
        return 1

    print(f"tags check out ({len(unnoticed)} notice(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
