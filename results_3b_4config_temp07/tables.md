# Experimental results

Model: `llama3.2:3b` via ollama | temperature 0.7 | seed(s) [43, 44, 45] | 3 repeat(s) | 240 pipeline runs, 720 model calls

## Table A - Headline results per configuration

| configuration | injected_runs | infected_runs | attack_success_rate_pct | refusal_rate_injected_pct | clean_runs | task_completion_pct | refusal_rate_clean_pct | median_latency_s |
|---|---|---|---|---|---|---|---|---|
| Baseline (no defence) | 36 | 16 | 44.4 | 2.8 | 24 | 100.0 | 0.0 | 10.36 |
| Structural delimiting | 36 | 7 | 19.4 | 0.0 | 24 | 100.0 | 0.0 | 10.4 |
| Warning only (control) | 36 | 5 | 13.9 | 8.3 | 24 | 100.0 | 0.0 | 10.23 |
| Provenance-Aware Middleware | 36 | 2 | 5.6 | 2.8 | 24 | 100.0 | 0.0 | 10.38 |

## Table B - Attack success rate by payload category (%)

| payload_category | Baseline (no defence) | Structural delimiting | Warning only (control) | Provenance-Aware Middleware |
|---|---|---|---|---|
| data | 50.0 | 41.7 | 25.0 | 0.0 |
| override | 41.7 | 0.0 | 8.3 | 0.0 |
| privilege | 41.7 | 16.7 | 8.3 | 16.7 |

## Table C - How far the injected instruction propagated (%)

| configuration | reached_retriever_pct | reached_analyst_pct | reached_executive_pct |
|---|---|---|---|
| Baseline (no defence) | 72.2 | 63.9 | 44.4 |
| Structural delimiting | 61.1 | 50.0 | 19.4 |
| Warning only (control) | 63.9 | 36.1 | 13.9 |
| Provenance-Aware Middleware | 41.7 | 27.8 | 5.6 |