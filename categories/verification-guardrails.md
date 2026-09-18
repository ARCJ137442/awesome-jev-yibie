# Verification & Guardrails

Use this category for programs where Jev gates output — verifying claims, reviewing diffs, checking generated content, or blocking unsafe agent actions before they ship.

## Submission format

```md
- [Name](URL) - Industry: one-sentence description of the Jev use case.
```

## Entries

- [is-malicious](https://github.com/luantak/is-malicious) - Software supply-chain security: asks Jev `Noul` checks about source and build files, escalates suspicious chunks for a second pass, and returns implicated files and lines before execution.
- [jev-review](https://github.com/devagrawal09/jev-review) - Software engineering: staged code-review workflow and local dashboard where Jev gates each review stage before a change advances.
- [pi-jev](https://github.com/y0usaf/pi-jev) - Agent safety: adds a measured tool-call gate to the Pi coding agent so risky calls are checked by Jev before execution.
- [OpenWork](https://github.com/different-ai/openwork) - Engineering workflow: wires Jev into its eval testkit as a verification judge so agent-produced work is gated by typed verdicts rather than a text model.
- [jev-guard](https://github.com/leepokai/jev-guard) - Agent security: prompt-injection and dangerous-action guard for Claude Code, Codex, Pi, and ACP agents, with Jev deciding what to block.
- [Foreman](https://github.com/thruwire/foreman) - Software factory: sits above Codex workers and has Jev independently judge whether an implementation is complete, its tests sufficient, or a human is needed.
- [jev-code](https://github.com/devagrawal09/jev-code) - Coding agents: bounded Jev workflows that keep agent judgments typed instead of free-form.
- [opencompany](https://github.com/useopencompany/opencompany) - Agent workspace: runs its approval review through Jev so workspace actions are gated by a typed decision.
- [jev-git](https://github.com/AkashPriyadarshii/jev-git) - Developer tooling: sub-second Git pre-commit & pre-push reflex gate that screens staged diffs for secrets and destructive commands using Jev.
