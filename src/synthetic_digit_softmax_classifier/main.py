"""Run synthetic digit softmax classifier demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dataset import make_dataset
from model import compare_models
from visualization import create_visualizations


def build_metrics(output: Path, seed: int = 211) -> dict[str, object]:
    data = make_dataset(seed=seed)
    baseline, optimized = compare_models(data)
    outputs = create_visualizations(data, baseline, optimized, output)
    metrics = {
        "project": "synthetic_digit_softmax_classifier",
        "sample_count": int(len(data.labels)),
        "baseline_template": {"accuracy": round(baseline.accuracy, 4), "macro_f1": round(baseline.macro_f1, 4)},
        "optimized_softmax": {
            "accuracy": round(optimized.accuracy, 4),
            "macro_f1": round(optimized.macro_f1, 4),
            "final_loss": round((optimized.loss_curve or [0])[-1], 6),
        },
        "improvement": {
            "accuracy_delta": round(optimized.accuracy - baseline.accuracy, 4),
            "macro_f1_delta": round(optimized.macro_f1 - baseline.macro_f1, 4),
        },
        "generated_files": [p.name for p in outputs],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=211)
    parser.add_argument("--output", type=Path, default=Path("assets"))
    args = parser.parse_args()
    print(json.dumps(build_metrics(args.output, args.seed), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
