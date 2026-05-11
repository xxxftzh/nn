"""Synthetic digit dataset for softmax regression."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class DigitData:
    images: np.ndarray
    labels: np.ndarray
    image_size: int


TEMPLATES = [
    ["01111110", "11000011", "11000111", "11001111", "11110011", "11100011", "11000011", "01111110"],
    ["00011000", "00111000", "01111000", "00011000", "00011000", "00011000", "00011000", "01111110"],
    ["01111110", "11000011", "00000011", "00001110", "00111000", "01100000", "11000000", "11111111"],
    ["11111110", "00000011", "00000110", "00111100", "00000110", "00000011", "11000011", "01111110"],
    ["00001110", "00011110", "00110110", "01100110", "11111111", "00000110", "00000110", "00000110"],
    ["11111111", "11000000", "11000000", "11111110", "00000011", "00000011", "11000011", "01111110"],
    ["00111110", "01100000", "11000000", "11111110", "11000011", "11000011", "11000011", "01111110"],
    ["11111111", "00000011", "00000110", "00001100", "00011000", "00110000", "00110000", "00110000"],
    ["01111110", "11000011", "11000011", "01111110", "11000011", "11000011", "11000011", "01111110"],
    ["01111110", "11000011", "11000011", "11000011", "01111111", "00000011", "00000110", "01111100"],
]


def _template(label: int) -> np.ndarray:
    return np.array([[float(ch) for ch in row] for row in TEMPLATES[label]], dtype=float)


def _shift(image: np.ndarray, dy: int, dx: int) -> np.ndarray:
    out = np.zeros_like(image)
    sy0, sy1 = max(0, -dy), image.shape[0] - max(0, dy)
    sx0, sx1 = max(0, -dx), image.shape[1] - max(0, dx)
    dy0, dx0 = max(0, dy), max(0, dx)
    out[dy0 : dy0 + sy1 - sy0, dx0 : dx0 + sx1 - sx0] = image[sy0:sy1, sx0:sx1]
    return out


def make_dataset(seed: int = 211, samples_per_digit: int = 100) -> DigitData:
    rng = np.random.default_rng(seed)
    images, labels = [], []
    for label in range(10):
        base = _template(label)
        for _ in range(samples_per_digit):
            image = _shift(base, int(rng.integers(-1, 2)), int(rng.integers(-1, 2)))
            image = np.clip(image + rng.normal(0.0, 0.18, image.shape), 0.0, 1.0)
            dropout = rng.random(image.shape) < 0.035
            image = np.where(dropout, 1.0 - image, image)
            images.append(image.reshape(-1))
            labels.append(label)
    return DigitData(np.array(images), np.array(labels, dtype=int), 8)


def train_test_split(data: DigitData, test_ratio: float = 0.25, seed: int = 211) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    train, test = [], []
    for label in range(10):
        idx = np.where(data.labels == label)[0]
        rng.shuffle(idx)
        split = int(len(idx) * (1.0 - test_ratio))
        train.extend(idx[:split].tolist())
        test.extend(idx[split:].tolist())
    return np.array(train, dtype=int), np.array(test, dtype=int)
