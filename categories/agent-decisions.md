# Agent Decisions

Use this category for programs where Jev supplies the decision step inside an agentic loop — tool choice, escalation, retry or stop, next-action selection.

## Submission format

```md
- [Name](URL) - Industry: one-sentence description of the Jev use case.
```

## Entries

- [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) - Browser automation: browser-use's ultrafast agent where Jev decides each next action and element to click, calling a language model only when text must be typed.
- [pi-typesafe-jev](https://github.com/legacybridge-tech/pi-typesafe-jev) - Coding agents: exposes System One judgments as five Pi tools so a model makes narrow semantic judgments while code and users keep control of thresholds, weights, and actions.
- [jev-judgment](https://github.com/HyunjunJeon/jev-judgment) - Coding agents: agent skill that sends closed coding-agent judgments to Jev so verdicts stay typed, cheap, and comparable across runs.
- [limpet](https://github.com/noplan-inc/limpet) - Coding agents: Stop hook that keeps an agent from finishing too early by judging plain-language completion rules with Jev.
- [robo-harness](https://github.com/grmkris/robo-harness) - Robotics: SO-101 arm workbench where a Jev decision runner picks bounded joint steps from typed candidate actions under a spend budget.
- [dsh-auto-mode](https://git.allen-software.com/allenh1/dsh-auto-mode) - Coding agents: DeepSeek Harness permission preset whose end-prompt step has Jev answer the open questions an agent leaves in its final message, steering them back only when a choice clears 0.6 confidence and an autonomy-safety Noul clears 0.5, and returning the turn to the human otherwise.
- [augustus](https://github.com/24601/Augustus) - Coding agents: agent skill that maps Choice, Score, and Noul onto classical methods so an agent can place typed judgment in software, with a composition algebra, question-design diagnosis, and a validation gate that requires a falsifying experiment.
- [yoshi](https://github.com/compozy/yoshi) - Context management: proxy for Claude Code and Codex where Jev judges which conversation history is still needed before pruning.
- [pi-jev (TheoOliveira)](https://github.com/TheoOliveira/pi-jev) - Coding agents: semantic tool routing and typed System One decisions for the Pi coding agent.
- [pi-quiet-ask](https://github.com/HyunjunJeon/pi-quiet-ask) - Coding agents: gives the Pi agent a quiet Jev decision layer for judgments it would otherwise hand to a chat model.
- [fastbrowse](https://github.com/agent-labs-dev/fastbrowse) - Browser agents: Jev picks each action from what is on the page while an LLM reads and plans.
- [super-jev](https://github.com/Kevthetech143/super-jev) - Decision harness: turns a Jev answer into a bounded action instead of leaving the caller to interpret it.
