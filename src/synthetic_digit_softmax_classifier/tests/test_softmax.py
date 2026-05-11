from __future__ import annotations

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from dataset import make_dataset
from main import build_metrics
from model import compare_models


def test_softmax_matches_template_baseline() -> None:
    data = make_dataset(seed=211)
    baseline, optimized = compare_models(data)
    assert optimized.accuracy >= baseline.accuracy
    assert optimized.macro_f1 >= baseline.macro_f1
    assert optimized.loss_curve is not None
    assert optimized.loss_curve[-1] < optimized.loss_curve[0]


def test_main_exports_assets(tmp_path: Path) -> None:
    metrics = build_metrics(tmp_path, seed=211)
    assert metrics["optimized_softmax"]["accuracy"] >= metrics["baseline_template"]["accuracy"]
    assert (tmp_path / "digit_samples.png").exists()
    assert (tmp_path / "confusion_matrix.png").exists()
    assert (tmp_path / "softmax_weight_maps.png").exists()
    assert (tmp_path / "metric_comparison.png").exists()
