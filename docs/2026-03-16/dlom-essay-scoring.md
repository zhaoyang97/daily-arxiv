# Decision-Level Ordinal Modeling for Multimodal Essay Scoring with Large Language Models

**日期**: 2026-03-16  
**arXiv**: [2603.14891](https://arxiv.org/abs/2603.14891)  
**领域**: 教育 NLP / 自动作文评分  
**关键词**: automated essay scoring, ordinal modeling, decision-level fusion, gated fusion, QWK

## 一句话总结
提出 DLOM：把 LLM 作文评分从“生成文本再解析分数”改为“在分数 token 上直接做决策”，并进一步给出多模态门控融合（DLOM-GF）与距离感知正则（DLOM-DA），在 EssayJudge 与 ASAP/ASAP++ 上稳定优于生成式基线。

## 背景与问题

- 生成式 AES 简单但决策隐式，容易受 prompt/解码/tokenization 影响
- 作文评分是天然序数任务：相邻分数错误不应等价于远距离错误
- 多模态评分中视觉信息贡献不稳定，固定融合策略不鲁棒

## 方法

### 1. DLOM：决策级序数建模
- 直接复用 LM head，不额外加分类头
- 从预定义分数 token 集 $\mathcal S$ 抽取 logits：

$$
\mathbf z=\text{Logits}(e,v)_L[\mathcal S],\quad \hat y=\arg\max_k z_k
$$

- 优点：避免“先生成再解析”误差链，决策可解释

### 2. DLOM-GF：多模态门控融合
- 文本分支 logits：$\mathbf z^{(t)}$
- 多模态分支 logits：$\mathbf z^{(m)}$
- 学习样本级权重 $\alpha$：

$$
\mathbf z=\alpha\mathbf z^{(m)}+(1-\alpha)\mathbf z^{(t)}
$$

### 3. DLOM-DA：距离感知正则
适用于文本场景，通过分布期望分数约束序数距离：

$$
\mathcal L=\mathcal L_{CE}+\lambda\mathcal L_{dist}
$$

其中 $\mathcal L_{dist}$ 对预测期望分数与真实分数的偏差做 SmoothL1 约束。

## 实验数据

### EssayJudge（多模态）

| 方法 | 平均 QWK |
|------|---------|
| SFT-Gen | 0.492 |
| DLOM | 0.504 |
| **DLOM-GF** | **0.516** |

### ASAP/ASAP++（文本）

| 方法 | trait QWK | prompt QWK |
|------|-----------|------------|
| ArTS | 0.689 | 0.717 |
| SFT-Gen | 0.646 | 0.676 |
| DLOM | 0.685 | 0.713 |
| **DLOM-DA** | **0.697** | **0.720** |

## 关键消融
- 在生成框架上直接叠序数 loss 反而退化（说明“位置错了”）
- 决策级建模和决策级融合均有稳定增益

## 亮点
- 把“语义理解”和“评分决策”解耦，问题建模更贴近 AES 本质
- 复用 LM head，几乎零结构改造
- 门控融合可解释性强，可分析不同 trait 的模态依赖

## 局限性
- 主要验证在 Qwen 系列，跨架构泛化需加强
- 多模态数据规模不大，置信区间仍值得报告
- 提升幅度中等，但 QWK 指标下仍具有实际意义

## 评分
- 新颖性: ⭐⭐⭐⭐
- 实验充分度: ⭐⭐⭐⭐
- 写作质量: ⭐⭐⭐⭐⭐
- 价值: ⭐⭐⭐（方法论价值高，场景相对垂直）
