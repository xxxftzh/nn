"""Template baseline and softmax regression model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from dataset import DigitData, train_test_split


@dataclass
class ClassifierResult:
    name: str
    y_true: np.ndarray
    y_pred: np.ndarray
    probabilities: np.ndarray
    accuracy: float
    macro_f1: float
    confusion: np.ndarray
    loss_curve: list[float] | None
    weights: np.ndarray | None


def _softmax(logits: np.ndarray) -> np.ndarray:
    logits = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(logits)
    return exp / np.sum(exp, axis=1, keepdims=True)


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, np.ndarray]:
    classes = int(np.max(y_true)) + 1
    confusion = np.zeros((classes, classes), dtype=int)
    for truth, pred in zip(y_true, y_pred):
        confusion[truth, pred] += 1
    f1 = []
    for label in range(classes):
        tp = confusion[label, label]
        fp = confusion[:, label].sum() - tp
        fn = confusion[label].sum() - tp
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1.append(2 * precision * recall / max(precision + recall, 1e-9))
    return float(np.mean(y_true == y_pred)), float(np.mean(f1)), confusion


def template_baseline(data: DigitData) -> ClassifierResult:
    _, test_idx = train_test_split(data)
    templates = np.array([data.images[np.where(data.labels == label)[0]].mean(axis=0) for label in range(10)])
    distances = ((data.images[test_idx, None, :] - templates[None, :, :]) ** 2).mean(axis=2)
    scores = -distances
    probabilities = _softmax(scores * 16.0)
    y_pred = np.argmin(distances, axis=1)
    y_true = data.labels[test_idx]
    accuracy, macro_f1, confusion = _metrics(y_true, y_pred)
    return ClassifierResult("template_baseline", y_true, y_pred, probabilities, accuracy, macro_f1, confusion, None, None)


def softmax_regression(data: DigitData, epochs: int = 520, lr: float = 0.8, reg: float = 0.01) -> ClassifierResult:
    train_idx, test_idx = train_test_split(data)
    x_train = np.column_stack([data.images[train_idx], np.ones(len(train_idx))])
    x_test = np.column_stack([data.images[test_idx], np.ones(len(test_idx))])
    y_train = data.labels[train_idx]
    y_true = data.labels[test_idx]
    y_onehot = np.eye(10)[y_train]
    weights = np.zeros((x_train.shape[1], 10))
    losses = []
    for _ in range(epochs):
        probabilities = _softmax(x_train @ weights)
        loss = -float(np.mean(np.sum(y_onehot * np.log(probabilities + 1e-9), axis=1))) + reg * float(np.sum(weights[:-1] ** 2))
        losses.append(loss)
        grad = x_train.T @ (probabilities - y_onehot) / len(x_train)
        grad[:-1] += reg * weights[:-1]
        weights -= lr * grad
    probabilities = _softmax(x_test @ weights)
    y_pred = np.argmax(probabilities, axis=1)
    accuracy, macro_f1, confusion = _metrics(y_true, y_pred)
    return ClassifierResult("softmax_regression", y_true, y_pred, probabilities, accuracy, macro_f1, confusion, losses, weights[:-1])


def compare_models(data: DigitData) -> tuple[ClassifierResult, ClassifierResult]:
    return template_baseline(data), softmax_regression(data)
