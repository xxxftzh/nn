"""Visualization for synthetic digit classification."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from dataset import DigitData
from model import ClassifierResult


def _prepare(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)


def plot_samples(data: DigitData, out: Path) -> Path:
    _prepare(out)
    path = out / "digit_samples.png"
    fig, axes = plt.subplots(2, 10, figsize=(10, 2.4))
    for label in range(10):
        idx = np.where(data.labels == label)[0][:2]
        for row in range(2):
            axes[row, label].imshow(data.images[idx[row]].reshape(8, 8), cmap="gray", vmin=0, vmax=1)
            axes[row, label].axis("off")
            if row == 0:
                axes[row, label].set_title(str(label))
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def plot_confusion(result: ClassifierResult, out: Path) -> Path:
    _prepare(out)
    path = out / "confusion_matrix.png"
    plt.figure(figsize=(6.5, 5.8))
    plt.imshow(result.confusion, cmap="Blues")
    plt.colorbar(label="count")
    for y in range(10):
        for x in range(10):
            plt.text(x, y, str(result.confusion[y, x]), ha="center", va="center", fontsize=8)
    plt.title("Softmax regression confusion matrix")
    plt.xlabel("predicted")
    plt.ylabel("true")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def plot_weight_maps(result: ClassifierResult, out: Path) -> Path:
    _prepare(out)
    path = out / "softmax_weight_maps.png"
    if result.weights is None:
        raise ValueError("weights required")
    fig, axes = plt.subplots(2, 5, figsize=(8, 3.8))
    vmax = float(np.max(np.abs(result.weights)))
    for label, ax in enumerate(axes.ravel()):
        ax.imshow(result.weights[:, label].reshape(8, 8), cmap="coolwarm", vmin=-vmax, vmax=vmax)
        ax.set_title(str(label))
        ax.axis("off")
    plt.suptitle("Learned softmax class weight maps")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def plot_metrics(baseline: ClassifierResult, optimized: ClassifierResult, out: Path) -> Path:
    _prepare(out)
    path = out / "metric_comparison.png"
    labels = ["accuracy", "macro F1"]
    x = np.arange(len(labels))
    plt.figure(figsize=(7, 5))
    plt.bar(x - 0.18, [baseline.accuracy, baseline.macro_f1], width=0.36, color="#eb5757", label="template")
    plt.bar(x + 0.18, [optimized.accuracy, optimized.macro_f1], width=0.36, color="#2f80ed", label="softmax")
    plt.xticks(x, labels)
    plt.ylim(0, 1.05)
    plt.grid(axis="y", linestyle="--", alpha=0.35)
    plt.title("Classification metric comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def write_predictions(result: ClassifierResult, out: Path) -> Path:
    _prepare(out)
    path = out / "predictions.csv"
    with path.open("w", encoding="utf-8") as f:
        f.write("row,true_label,predicted_label,confidence\n")
        for i, (truth, pred, probs) in enumerate(zip(result.y_true, result.y_pred, result.probabilities)):
            f.write(f"{i},{truth},{pred},{float(np.max(probs)):.5f}\n")
    return path


def create_visualizations(data: DigitData, baseline: ClassifierResult, optimized: ClassifierResult, out: Path) -> list[Path]:
    return [
        plot_samples(data, out),
        plot_confusion(optimized, out),
        plot_weight_maps(optimized, out),
        plot_metrics(baseline, optimized, out),
        write_predictions(optimized, out),
    ]
