# Experimental results

Model: `llama3.2:3b` via ollama | temperature 0.7 | seed(s) [43, 44, 45] | 3 repeat(s) | 180 pipeline runs, 540 model calls

## Table A - Headline results per configuration

| configuration | injected_runs | infected_runs | attack_success_rate_pct | clean_runs | task_completion_pct | median_latency_s |
|---|---|---|---|---|---|---|
| Baseline (no defence) | 36 | 16 | 44.4 | 24 | 100.0 | 10.21 |
| Structural delimiting | 36 | 7 | 19.4 | 24 | 100.0 | 10.14 |
| Provenance-Aware Middleware | 36 | 0 | 0.0 | 24 | 100.0 | 10.01 |

## Table B - Attack success rate by payload category (%)

| payload_category | Baseline (no defence) | Structural delimiting | Provenance-Aware Middleware |
|---|---|---|---|
| data | 50.0 | 41.7 | 0.0 |
| override | 41.7 | 0.0 | 0.0 |
| privilege | 41.7 | 16.7 | 0.0 |

## Table C - How far the injected instruction propagated (%)

| configuration | reached_retriever_pct | reached_analyst_pct | reached_executive_pct |
|---|---|---|---|
| Baseline (no defence) | 72.2 | 63.9 | 44.4 |
| Structural delimiting | 61.1 | 50.0 | 19.4 |
| Provenance-Aware Middleware | 41.7 | 25.0 | 0.0 |