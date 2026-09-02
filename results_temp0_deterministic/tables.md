# Experimental results

Model: `llama3.2:3b` via ollama | temperature 0.0 | seed 42 | 3 repeat(s) | 180 pipeline runs, 540 model calls

## Table A - Headline results per configuration

| configuration | injected_runs | infected_runs | attack_success_rate_pct | clean_runs | task_completion_pct | median_latency_s |
|---|---|---|---|---|---|---|
| Baseline (no defence) | 36 | 12 | 33.3 | 24 | 100.0 | 9.61 |
| Structural delimiting | 36 | 12 | 33.3 | 24 | 100.0 | 9.69 |
| Provenance-Aware Middleware | 36 | 3 | 8.3 | 24 | 100.0 | 9.34 |

## Table B - Attack success rate by payload category (%)

| payload_category | Baseline (no defence) | Structural delimiting | Provenance-Aware Middleware |
|---|---|---|---|
| data | 25.0 | 75.0 | 25.0 |
| override | 25.0 | 0.0 | 0.0 |
| privilege | 50.0 | 25.0 | 0.0 |

## Table C - How far the injected instruction propagated (%)

| configuration | reached_retriever_pct | reached_analyst_pct | reached_executive_pct |
|---|---|---|---|
| Baseline (no defence) | 75.0 | 75.0 | 33.3 |
| Structural delimiting | 58.3 | 50.0 | 33.3 |
| Provenance-Aware Middleware | 41.7 | 25.0 | 8.3 |