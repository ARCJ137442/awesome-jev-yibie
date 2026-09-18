# Calibration & Research

Use this category for work that studies or exploits Jev's calibrated confidence — RLCD-style training, probability quality, threshold selection, uncertainty analysis.

## Submission format

```md
- [Name](URL) - Industry: one-sentence description of the Jev use case.
```

## Entries

- [decider](https://github.com/Mapika/decider) - Open models: reproduces the System One shape with a Qwen3.5-2B fine-tune that emits typed decisions with calibrated probabilities in one pass.
- [openjev](https://github.com/zhihz/openjev) - Open research: independent local preview that answers bilingual probability questions from context, questions, and candidate answers, inspired by TypeSafe Jev.
- [Parallel Constrained Decoding (Qwen2.5-1B-RLCD)](https://huggingface.co/spaces/drinkmoonshine/parallel-constrained-decoding) - Open research: RLCD-trained Qwen2.5-1B demo exploring open-source parallel constrained decoding as an alternative to Jev.
- [NanoJev](https://github.com/TianyuCodings/NanoJev) - Open replica: a 0.6B parallel decision model that returns full probability distributions with no output-token decoding, shipped with its training pipeline, weights, and dataset.
- [open-alternative-jev](https://github.com/ikermoel/open-alternative-jev) - Open alternative: runs a Jev-shaped decision model locally on your own GPU.
- [mini-jev](https://github.com/r-ms/mini-jev) - Local reproduction: implements Jev's typed-decision interface on top of a local LLM.
- [Jev-compatible public API](https://x.com/ekzhang1/status/2100651678110515383) - Open research: a public Jev-shaped API backed by an open Qwen3.6-35B-A3B model so anyone can try the typed-decision interface.
