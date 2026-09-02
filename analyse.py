#!/usr/bin/env python3
"""
Analysis of the experiment output.

Reads results/runs.csv and produces:
    results/summary.csv          headline figures per configuration
    results/by_category.csv      attack success rate per payload category
    results/propagation.csv      where in the pipeline the canary survives to
    results/asr_chart.png        bar chart for the paper (if matplotlib present)
    results/tables.md            tables ready to paste into the paper
"""
import csv, json, statistics
from collections import defaultdict
from pathlib import Path

RESULTS = Path(__file__).parent / "results"
CONFIGS = ["baseline", "delimiting", "warning", "provenance"]
LABEL = {"baseline": "Baseline (no defence)",
         "delimiting": "Structural delimiting",
         "warning": "Warning only (control)",
         "provenance": "Provenance-Aware Middleware"}


def pct(n, d):
    return 0.0 if d == 0 else round(100.0 * n / d, 1)


def main():
    rows = list(csv.DictReader(open(RESULTS / "runs.csv", encoding="utf-8")))
    meta = json.loads((RESULTS / "metadata.json").read_text())

    inj = [r for r in rows if r["doc_type"] == "injected"]
    cln = [r for r in rows if r["doc_type"] == "clean"]

    # ---------------------------------------------------------------- summary
    summary = []
    for c in CONFIGS:
        ci = [r for r in inj if r["config"] == c]
        cc = [r for r in cln if r["config"] == c]
        infected = sum(int(r["infected"]) for r in ci)
        lat = [float(r["latency_s"]) for r in rows if r["config"] == c]
        completed = sum(int(r["task_completed"] or 0) for r in cc)
        refused_inj = sum(int(r.get("refused") or 0) for r in ci)
        refused_cln = sum(int(r.get("refused") or 0) for r in cc)
        summary.append({
            "configuration": LABEL[c],
            "injected_runs": len(ci),
            "infected_runs": infected,
            "attack_success_rate_pct": pct(infected, len(ci)),
            "refusal_rate_injected_pct": pct(refused_inj, len(ci)),
            "clean_runs": len(cc),
            "task_completion_pct": pct(completed, len(cc)),
            "refusal_rate_clean_pct": pct(refused_cln, len(cc)),
            "median_latency_s": round(statistics.median(lat), 2) if lat else 0,
        })

    with open(RESULTS / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader(); w.writerows(summary)

    # ----------------------------------------------------------- by category
    cats = sorted({r["category"] for r in inj})
    bycat = []
    for cat in cats:
        row = {"payload_category": cat}
        for c in CONFIGS:
            sel = [r for r in inj if r["config"] == c and r["category"] == cat]
            row[LABEL[c]] = pct(sum(int(r["infected"]) for r in sel), len(sel))
        bycat.append(row)
    with open(RESULTS / "by_category.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(bycat[0].keys()))
        w.writeheader(); w.writerows(bycat)

    # ---------------------------------------------------------- propagation
    prop = []
    for c in CONFIGS:
        sel = [r for r in inj if r["config"] == c]
        prop.append({
            "configuration": LABEL[c],
            "reached_retriever_pct": pct(sum(int(r["canary_at_retriever"]) for r in sel), len(sel)),
            "reached_analyst_pct": pct(sum(int(r["canary_at_analyst"]) for r in sel), len(sel)),
            "reached_executive_pct": pct(sum(int(r["infected"]) for r in sel), len(sel)),
        })
    with open(RESULTS / "propagation.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(prop[0].keys()))
        w.writeheader(); w.writerows(prop)

    # --------------------------------------------------------------- chart
    # Written as SVG using only the standard library, so the script has no
    # third-party dependencies. SVG can be inserted directly into Word
    # (Insert > Pictures > This Device) and stays sharp at any size.
    def svg_bar_chart(path, labels, values, title, ylabel="Attack success rate (%)"):
        W, H = 720, 420
        left, right, top, bottom = 90, 30, 70, 90
        pw, ph = W - left - right, H - top - bottom
        colours = ["#b03a2e", "#b7950b", "#7d6608", "#1e6f5c"]
        n = len(values)
        slot = pw / n
        bw = slot * 0.55
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="Times New Roman, serif">',
            f'<rect width="{W}" height="{H}" fill="white"/>',
        ]
        # y gridlines and ticks at 0,20,...,100
        for v in range(0, 101, 20):
            y = top + ph - (v / 100.0) * ph
            parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+pw}" y2="{y:.1f}" '
                         f'stroke="#dddddd" stroke-width="1"/>')
            parts.append(f'<text x="{left-10}" y="{y+4:.1f}" font-size="13" '
                         f'text-anchor="end" fill="#333333">{v}</text>')
        # bars
        for i, (lab, val) in enumerate(zip(labels, values)):
            x = left + i * slot + (slot - bw) / 2
            h = (val / 100.0) * ph
            y = top + ph - h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" '
                         f'fill="{colours[i % len(colours)]}"/>')
            parts.append(f'<text x="{x+bw/2:.1f}" y="{y-8:.1f}" font-size="14" '
                         f'font-weight="bold" text-anchor="middle" fill="#000000">{val}%</text>')
            # wrap the label onto two lines at the first space after 12 chars
            words, line1, line2 = lab.split(), "", ""
            for w in words:
                if len(line1) < 14 and not line2:
                    line1 = (line1 + " " + w).strip()
                else:
                    line2 = (line2 + " " + w).strip()
            parts.append(f'<text x="{x+bw/2:.1f}" y="{top+ph+22}" font-size="13" '
                         f'text-anchor="middle" fill="#000000">{line1}</text>')
            if line2:
                parts.append(f'<text x="{x+bw/2:.1f}" y="{top+ph+40}" font-size="13" '
                             f'text-anchor="middle" fill="#000000">{line2}</text>')
        # axes
        parts.append(f'<line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" '
                     f'stroke="#000000" stroke-width="1.2"/>')
        parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" '
                     f'stroke="#000000" stroke-width="1.2"/>')
        # labels
        parts.append(f'<text x="{left+pw/2:.0f}" y="26" font-size="16" font-weight="bold" '
                     f'text-anchor="middle">{title}</text>')
        parts.append(f'<text x="{left+pw/2:.0f}" y="46" font-size="12" fill="#555555" '
                     f'text-anchor="middle">{subtitle}</text>')
        parts.append(f'<text x="22" y="{top+ph/2:.0f}" font-size="13" text-anchor="middle" '
                     f'transform="rotate(-90 22 {top+ph/2:.0f})">{ylabel}</text>')
        parts.append('</svg>')
        Path(path).write_text("\n".join(parts), encoding="utf-8")

    subtitle = (f"{meta['model']} | {meta['n_injected_documents']} injected documents | "
                f"{meta['repeats']} repeat(s) | temperature {meta['temperature']}")
    svg_bar_chart(RESULTS / "asr_chart.svg",
                  [s["configuration"].replace(" (no defence)", "").replace("-Aware", "-Aware ")
                   for s in summary],
                  [s["attack_success_rate_pct"] for s in summary],
                  "Attack success rate by configuration")
    chart = "results/asr_chart.svg written (insert into Word with Insert > Pictures)"

    # optional: also write a PNG if matplotlib happens to be usable
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        names = [s["configuration"].replace(" (", "\n(") for s in summary]
        vals = [s["attack_success_rate_pct"] for s in summary]
        bars = ax.bar(names, vals, color=["#b03a2e", "#b7950b", "#7d6608", "#1e6f5c"])
        ax.set_ylabel("Attack success rate (%)"); ax.set_ylim(0, 105)
        ax.set_title("Attack success rate by configuration\n" + subtitle, fontsize=9)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + 2, f"{v}%", ha="center", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); plt.savefig(RESULTS / "asr_chart.png", dpi=200)
        chart += " and results/asr_chart.png"
    except Exception:
        pass

    # -------------------------------------------------------------- markdown
    def md(rows_, headers):
        out = ["| " + " | ".join(headers) + " |",
               "|" + "|".join(["---"] * len(headers)) + "|"]
        for r in rows_:
            out.append("| " + " | ".join(str(r[h]) for h in headers) + " |")
        return "\n".join(out)

    lines = [
        f"# Experimental results",
        f"\nModel: `{meta['model']}` via {meta['backend']} | temperature {meta['temperature']} | "
        f"seed(s) {meta.get('seeds', meta.get('seed'))} | {meta['repeats']} repeat(s) | "
        f"{meta['total_pipeline_runs']} pipeline runs, {meta['total_model_calls']} model calls",
        f"\n## Table A - Headline results per configuration\n",
        md(summary, list(summary[0].keys())),
        f"\n## Table B - Attack success rate by payload category (%)\n",
        md(bycat, list(bycat[0].keys())),
        f"\n## Table C - How far the injected instruction propagated (%)\n",
        md(prop, list(prop[0].keys())),
    ]
    (RESULTS / "tables.md").write_text("\n".join(lines), encoding="utf-8")

    # ---------------------------------------------------------------- stdout
    print("\n=== HEADLINE RESULTS ===")
    for s in summary:
        print(f"  {s['configuration']:32s} ASR {s['attack_success_rate_pct']:5.1f}%   "
              f"utility {s['task_completion_pct']:5.1f}%   "
              f"refusal(inj) {s['refusal_rate_injected_pct']:5.1f}%   "
              f"refusal(clean) {s['refusal_rate_clean_pct']:5.1f}%   "
              f"lat {s['median_latency_s']}s")
    print("\n=== BY PAYLOAD CATEGORY (ASR %) ===")
    for r in bycat:
        print(f"  {r['payload_category']:10s} " +
              "  ".join(f"{LABEL[c][:12]}={r[LABEL[c]]:5.1f}" for c in CONFIGS))
    print("\n=== PROPAGATION (% of injected runs) ===")
    for r in prop:
        print(f"  {r['configuration']:32s} retriever {r['reached_retriever_pct']:5.1f}  "
              f"analyst {r['reached_analyst_pct']:5.1f}  executive {r['reached_executive_pct']:5.1f}")
    print(f"\n{chart}")
    print("results/summary.csv, by_category.csv, propagation.csv, tables.md written")


if __name__ == "__main__":
    main()
