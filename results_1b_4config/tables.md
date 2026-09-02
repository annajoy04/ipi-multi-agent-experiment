# Experimental results

Model: `llama3.2:1b` via ollama | temperature 0.7 | seed(s) [43, 44] | 2 repeat(s) | 160 pipeline runs, 480 model calls

## Table A - Headline results per configuration

| configuration | injected_runs | infected_runs | attack_success_rate_pct | refusal_rate_injected_pct | clean_runs | task_completion_pct | refusal_rate_clean_pct | median_latency_s |
|---|---|---|---|---|---|---|---|---|
| Baseline (no defence) | 24 | 3 | 12.5 | 4.2 | 16 | 93.8 | 6.2 | 9.0 |
| Structural delimiting | 24 | 6 | 25.0 | 20.8 | 16 | 93.8 | 6.2 | 8.99 |
| Warning only (control) | 24 | 0 | 0.0 | 25.0 | 16 | 87.5 | 6.2 | 8.62 |
| Provenance-Aware Middleware | 24 | 6 | 25.0 | 29.2 | 16 | 68.8 | 31.2 | 9.08 |

## Table B - Attack success rate by payload category (%)

| payload_category | Baseline (no defence) | Structural delimiting | Warning only (control) | Provenance-Aware Middleware |
|---|---|---|---|---|
| data | 12.5 | 37.5 | 0.0 | 25.0 |
| override | 0.0 | 12.5 | 0.0 | 12.5 |
| privilege | 25.0 | 25.0 | 0.0 | 37.5 |

## Table C - How far the injected instruction propagated (%)

| configuration | reached_retriever_pct | reached_analyst_pct | reached_executive_pct |
|---|---|---|---|
| Baseline (no defence) | 37.5 | 25.0 | 12.5 |
| Structural delimiting | 75.0 | 62.5 | 25.0 |
| Warning only (control) | 12.5 | 4.2 | 0.0 |
| Provenance-Aware Middleware | 95.8 | 62.5 | 25.0 |