# Decision-Level Ordinal Modeling for Multimodal Essay Scoring with Large Language Models

**日期**: 2026-03-16  
**arXiv**: [2603.14891](https://arxiv.org/abs/2603.14891)  
**领域**: 多模态/VLM / NLP理解  
**关键词**: 自动作文评分, 序数回归, 决策级建模, 门控融合, LLM评分

## 一句话总结
将 LLM 作文评分从隐式 token 生成重构为显式序数决策——复用 LM head 在预定义分数 token 上提取 score-wise logits，提出 DLOM-GF 门控融合多模态评分和 DLOM-DA 距离感知正则化，在 EssayJudge 和 ASAP/ASAP++ 上一致超越生成式基线。

## 研究背景与动机

1. **领域现状**: LLM 已成为自动作文评分(AES)的主流方法，通常将评分表述为自回归 token 生成——生成分数文本后解析。

2. **现有痛点**: (a) 生成式评分使决策隐式化，受解码策略/prompt 设计/tokenization 影响大；(b) AES 本质是序数问题（相邻分数误差 < 远距分数误差），但生成框架不显式建模序数结构；(c) 多模态 AES 中视觉输入的有用性因文章/维度而异，固定融合不灵活。

3. **核心 idea**: 将语义理解（SFT LLM）与评分决策（序数 score-logit 空间）解耦，在决策层面显式操作序数结构。

## 方法详解

### DLOM: 决策级序数建模

- 复用 LLM 的 LM head（词表投影层），不解码，直接提取最后 token 在预定义分数 token 集 $\mathcal{S}$ 上的 logits
- $\mathbf{z} = \text{Logits}(e,v)_L[\mathcal{S}] \in \mathbb{R}^{K+1}$，预测 $\hat{y} = \arg\max_k z_k$
- 无需解码、无需额外分类头，直接在序数分数空间做决策

### DLOM-GF: 多模态门控融合

- 分别获取纯文本分支 $\mathbf{z}^{(t)}$ 和多模态分支 $\mathbf{z}^{(m)}$ 的 score logits
- 拼接后通过轻量门控网络预测融合权重 $\alpha$
- 最终 logits: $\mathbf{z} = \alpha \cdot \mathbf{z}^{(m)} + (1-\alpha) \cdot \mathbf{z}^{(t)}$
- 完全在决策层融合，自适应估计模态可靠性

### DLOM-DA: 距离感知正则化（文本场景）

- 计算预测分布的期望分数 $\mathbb{E}[s] = \sum p_k \cdot k$
- SmoothL1 惩罚期望分数与真实分数的偏差
- 最终损失: $\mathcal{L} = \mathcal{L}_{CE} + \lambda \mathcal{L}_{dist}$，$\lambda$ 可学习

## 实验关键数据

### EssayJudge (多模态)

| 方法 | 平均 QWK |
|------|---------|
| SFT-Gen (基线) | 0.492 |
| DLOM | 0.504 (+1.2%) |
| DLOM-GF | **0.516** (+2.4%) |

### ASAP/ASAP++ (纯文本)

| 方法 | 平均 QWK (trait) | 平均 QWK (prompt) |
|------|-----------------|------------------|
| ArTS | 0.689 | 0.717 |
| SFT-Gen | 0.646 | 0.676 |
| DLOM | 0.685 | 0.713 |
| DLOM-DA | **0.697** | **0.720** |

### 关键消融

- 在生成式模型上加序数 loss 反而降低性能（0.472-0.481 vs 基线 0.492），说明序数建模必须在决策层而非 loss 层
- 纯文本决策 0.454 < 多模态决策 0.501 < DLOM-GF 0.516，决策级融合有额外增益

## 亮点与洞察
- **决策层 vs 表示层**: 序数结构在决策层建模比在 loss 层正则化更有效——直接改变预测空间比间接约束生成更合理
- **LM head 复用**: 巧妙利用 LLM 已学习的 token 偏好分布，免去新分类头
- **门控融合可解释性**: 可直接观察 $\alpha$ 值理解模型在每个 trait 上的模态偏好

## 局限性 / 可改进方向
- 仅在 Qwen 系列上验证，需更多架构验证泛化性
- DLOM-DA 仅在纯文本场景探索，未与多模态融合结合
- EssayJudge 数据集较小（1,054 篇），交叉验证方差较大
- 绝对提升幅度有限（+2.4%），但在 QWK 这种严格指标上已不小

## 评分
- 新颖性: ⭐⭐⭐⭐ 决策级序数建模视角新颖，与生成范式形成有趣对比
- 实验充分度: ⭐⭐⭐⭐ 多模态+纯文本双基准验证，消融完整
- 写作质量: ⭐⭐⭐⭐⭐ 动机→方法→实验逻辑链严谨，定位清晰
- 价值: ⭐⭐⭐ 应用场景较窄，但方法论对其他序数评估任务有借鉴价值
