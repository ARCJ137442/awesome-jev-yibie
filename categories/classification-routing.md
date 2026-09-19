# Classification & Routing

Use this category for programs where Jev sorts incoming state into categories or picks the next destination — tickets, intents, alerts, documents, or traffic.

## Submission format

```md
- [Name](URL) - Industry: one-sentence description of the Jev use case.
```

## Entries

- [Notra](https://github.com/usenotra/notra) - Marketing analytics: production GEO platform whose `NOTRA_JEV_CLASSIFIERS` flag routes brand-visibility classifiers off an LLM and onto Jev `Boolean` decisions at a 0.5 threshold, targeting 300 ms p50.
- [jev-router](https://github.com/gargpratyush/jev-router) - Developer tooling: routes Claude Code tasks to the cheapest capable model by asking Jev to choose among candidates.
- [jev-router (prismhq)](https://github.com/prismhq/jev-router) - LLM infrastructure: open-source LiteLLM-based router where a Jev decision picks which model serves each request.
- [pi-jev-router](https://github.com/mejiasd3v/pi-jev-router) - Coding agents: adds automatic per-request model routing to the Pi coding agent through Jev decisions on Vercel AI Gateway.
- [jcm-router](https://github.com/adarshmishra07/jcm-router) - Coding agents: local proxy that picks the Claude model and reasoning effort per message with a Jev decision while leaving the cached main chat untouched.
- [jev-agent-skill-router](https://github.com/GodsBoy/jev-agent-skill-router) - Agent infrastructure: routes agent skill selection through typed, confidence-aware Jev decisions so weak matches are declined instead of guessed.
- [typesafe-jev CV screener](https://github.com/gtaras7/typesafe-jev) - Recruiting: screens a folder of CVs with Jev typed judgments against an editable policy, re-scoring candidates for free when the policy changes.
- [Jev email intent workflow](https://github.com/GiesN/typesafe-jev-workflow) - Back-office automation: async LangGraph workflow gets a typed Jev `Choice` (`invoice` or `general`) and routes each inbound email to the matching handler.
- [unclutter](https://github.com/kitze/unclutter) - Browser tooling: WXT extension where Jev decides per page element whether it is clutter, removing it under reusable template rules.
- [typesafe-adblock](https://github.com/realZachi/typesafe-adblock) - Browser tooling: Chrome extension that asks Jev whether each DOM element is an ad, turning ad blocking into a stream of per-element typed questions.
- [DiffJury](https://github.com/raihankhan-rk/diffjury) - Code review: routes each pull request by risk with Jev before a human reviewer is assigned, doubling as a review coach.
- [HA-Jev](https://github.com/AboveColin/HA-Jev) - Smart home: Home Assistant integration that answers questions about the house as a probability, a choice, or a score.
- [secondlayer](https://github.com/ryanwaits/secondlayer) - Fault triage: self-hosted Stacks data service whose Slack gate and fault-triage paths both run on Jev decisions.
- [new-api-typesafe-plugin](https://github.com/FFatTiger/new-api-plugin-typesafe) - LLM gateway: adds a native `/v1/systemone` endpoint to new-api so typed decisions sit behind the same gateway as chat models.
- [duet-agent](https://github.com/dzhng/duet-agent) - Agent harness: keeps a Jev-backed routing table for deciding which model should serve a request.
- [json-render](https://github.com/vercel-labs/json-render) - Generative UI: Vercel Labs' UI framework uses Jev in its compose path to pick which components and actions a rendered interface should contain.
- [omo-jevlike-router](https://github.com/islee23520/omo-jevlike-router) - Skill routing: shrinks the skill catalog in a system prompt with one forward pass over a frozen Qwen, routing each request Jev-style.
- [jev-cookbook](https://github.com/nexibeo/jev-cookbook) - Developer education: 15 runnable Node recipes that route support tickets, file documents, categorize bank transactions and label Gmail with Jev `Choice` and `Noul` questions, sending low-confidence answers to human review.
- [flue-jev-demo](https://github.com/matthewp/flue-jev-demo) - Agent routing: routes a Flue agent's work with Jev through Cloudflare AI Gateway.
- [sift](https://github.com/bohutang/sift) - Content labelling: Chrome extension that labels every post in an X timeline - substance, humour, chit-chat, promo, junk, or AI-written - with Jev decisions.
