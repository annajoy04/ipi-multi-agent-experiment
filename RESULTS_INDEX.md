# Which results folder supports which part of the paper

| Folder | Condition | Used for |
|---|---|---|
| `results_3b_4config_temp07` | Llama 3.2 3B, T=0.7, seeds 43/44/45, 3 repeats, 4 configurations | **Primary results.** Tables III, IV, V, VI and Figures 3 and 4 |
| `results_temp0_deterministic` | Llama 3.2 3B, T=0, seed 42, 3 repeats | Deterministic condition, Table VI |
| `results_temp07_stochastic` | Llama 3.2 3B, T=0.7, 3 configurations (before the control was added) | Earlier run, retained for transparency |
| `results_1b_4config` | Llama 3.2 1B, T=0.7, seeds 43/44, 2 repeats, 4 configurations | Smaller-model condition, Table VIII |

Each folder contains:

- `runs.csv` — one row per pipeline run: configuration, repeat, document, category,
  infected, refused, canary presence at each stage, latency, and the final output text
- `summary.csv`, `by_category.csv`, `propagation.csv` — the aggregated figures quoted in the paper
- `metadata.json` — model, temperature, seeds, run counts, wall-clock duration
- `tables.md` — the same figures in readable form

To reproduce: see README.md.
