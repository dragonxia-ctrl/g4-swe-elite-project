# G4-SWE Elite — Gemma 4 Developer Agent Competition starter

This repository contains a declarative ADK-style agent submission and local packaging/structural validation scripts.

## Important status

This is an **engineering starter, not a leaderboard-validated winning solution**. The Kaggle harness compiler is authoritative. Before submitting, run the official Getting Started notebook / competition validator against this package. In particular, confirm the installed `adk-submission` and `swegemma` versions accept the `agent_tool`, `skills`, and `generate_content_config` fields used here.

## Layout

- `submission/agent.yaml`: required root agent configuration.
- `submission/prompts/system.md`: main agent operating policy.
- `submission/sub_agents/repo_analyst.yaml`: read-only code-graph analyst.
- `submission/skills/`: progressive navigation and repair protocols.
- `scripts/build_submission.py`: creates a Kaggle-ready `submission.zip` with `agent.yaml` at archive root.
- `scripts/validate_submission.py`: structural checks and optional YAML parsing.

## Build

```bash
python scripts/validate_submission.py
python scripts/build_submission.py --model gemma-4-31b-it-qat-w4a16-ct
```

Supported model identifiers (as published in the competition rules at the time this project was prepared):

- `gemma-4-31b-it-qat-w4a16-ct`
- `gemma-4-12b-it-qat-w4a16-ct`
- `gemma-4-e4b-it-qat-w4a16-ct`
- `gemma-4-e2b-it-qat-w4a16-ct`

All agents in one submission must use the same base model. The build script updates the root and sub-agent configs together.

## Kaggle workflow

1. Join the competition and accept its rules.
2. Open the official Getting Started notebook and attach the competition, model, and wheelhouse inputs as instructed there.
3. Upload this project or copy the `submission/` contents into the notebook workspace.
4. Run the structural validator and then the official harness compilation/validation cell.
5. Run a small local/dev evaluation if the competition notebook exposes one.
6. Only after successful official validation, submit the generated `submission.zip`.

Official references:
- https://www.kaggle.com/competitions/gemma-4-developer-agent
- https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent

## Design choices

The first version deliberately uses one writer (the root agent) and one read-only analyst. This reduces conflicting edits while retaining parallelizable localization expertise. The prompt uses progressive narrowing: exact search → semantic search → graph neighborhood → source/test inspection. It then enforces minimal diffs and targeted tests.

No LoRA weights are included. Add adapters only after collecting legal, reproducible training traces and verifying compatibility with the exact competition runtime. A LoRA is not automatically an improvement.

## Next experiments

- Ablate the analyst sub-agent: on/off.
- Compare all permitted model sizes under the same task set and time budget.
- Compare semantic-search k=5/8/12 and graph-neighbor limits 10/20/30.
- Compare targeted-only testing with targeted + adjacent regression testing.
- Record per-task success, elapsed time, tool calls, patch size, and failure category.
