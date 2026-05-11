# 合成手写数字 Softmax 多分类

本项目实现了一个面向神经网络课程的 Softmax 回归多分类模块。项目使用 8x8 数字模板生成合成手写数字样本，并加入平移、噪声和少量像素翻转扰动，构造一个不依赖外部数据集的分类实验。

## 功能内容

- 构建 0 到 9 的 8x8 合成数字数据集。
- 实现模板匹配 `template_baseline` 基线方法。
- 使用 Numpy 实现 `softmax_regression`，包含 Softmax、交叉熵和梯度下降训练。
- 统计准确率、Macro-F1 和混淆矩阵。
- 生成样本图、混淆矩阵、Softmax 权重图和指标对比图。
- 输出 `predictions.csv` 和 `metrics.json`，方便复现实验和写提交说明。

## 运行方法

```bash
python main.py --output assets
```

## 项目意义

该模块对应神经网络课程中的 Softmax 多分类基础。通过可视化每个类别的权重图，可以直观看到模型学习到的数字笔画区域，也能解释交叉熵训练如何把像素输入映射到类别概率。

## 测试

```bash
python -m pytest tests
```
