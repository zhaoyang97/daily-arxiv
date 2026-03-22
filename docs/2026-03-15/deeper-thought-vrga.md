# Deeper Thought, Weaker Aim: Understanding and Mitigating Perceptual Impairment during Reasoning in MLLMs

**日期**: 2026-03-15  
**arXiv**: [2603.14184](https://arxiv.org/abs/2603.14184)  
**代码**: [VRGA](https://github.com/Ivine11/VRGA)  
**领域**: 多模态VLM / LLM推理  
**关键词**: CoT reasoning, attention dispersion, visual grounding, VQA, training-free

## 一句话总结
揭示 CoT 推理导致 MLLM 视觉注意力分散（"想得越深、瞄得越偏"），发现有效视觉 head 满足 $R_\text{img}$高 + $H_\text{img}$低（高图像关注 + 低空间熵）的线性关系，提出 VRGA 框架在推理时选择性增强 question-relevant 区域注意力，无训练地提升 VQA 准确率 1-6 分。

## 研究背景与动机

1. **领域现状**: CoT 推理在文本 LLM 上效果显著，但迁移到 MLLM 的视觉 QA 任务时常导致准确率下降——"reasoning 反而降分"。

2. **现有痛点**: 现有解释认为"推理过程中感知能力下降"，尝试通过注入额外视觉 token 或外部工具缓解。但分析发现，失败案例中多数视觉描述是正确的——不是"看不到"，而是"看错地方"。

3. **核心矛盾**: CoT prompt 不影响模型"看到什么"，但改变了模型"看哪里"——注意力从 question-relevant 区域分散到全图，导致即使描述正确也答错。

4. **切入角度**: 从注意力的**空间分布**（而非总量）入手分析。发现正确回答的 RRAR（相关区域注意力比）一致高于错误回答；CoT 模式的 RRAR 一致低于 Direct 模式。

5. **核心 idea**: 识别出"视觉处理 head"（高 $R_\text{img}$ + 低 $H_\text{img}$），在推理时选择性增强这些 head 对 question-relevant 区域的注意力。

## 方法详解

### 关键发现

1. **$R_\text{img}$ 与 $H_\text{img}$ 的线性关系**: 跨 5 个模型，Pearson r > 0.9。说明有效视觉处理 head 天然同时具备高图像关注和低空间熵。

2. **EFR = $H_\text{img} / R_\text{img}$** 是识别视觉 head 的好指标：EFR 低 + $R_\text{img}$ 高的 head 在 RRAR 上一致最好。

3. **头级消融验证**: 按 EFR 选择的 head 被 mask 后，准确率暴跌（Qwen2.5-VL-3B: 87.64→24.31），远超随机 mask，说明选择的 head 确实是视觉推理的关键。

### VRGA 框架

**Phase 1: 定位 question-relevant 区域**
1. 用 EFR + $R_\text{img}$ 选择视觉焦点 head $\mathcal{H}_v$
2. 识别背景 head $\mathcal{H}_b$（低层、低 $R_\text{img}$、高熵）
3. 构造精炼注意力图：$\mathbf{A}_\text{refined} = \text{Norm}(\frac{1}{|\mathcal{H}_v|}\sum \mathbf{A}_h - \lambda \cdot \frac{1}{|\mathcal{H}_b|}\sum \mathbf{A}_h)$
4. 阈值 $\tau$ 选取高注意力 token 作为 relevant 区域 $\mathcal{T}_q$

**Phase 2: 注意力重加权**
- 在生成阶段，增强视觉 head 对 $\mathcal{T}_q$ 中 token 的注意力权重
- 无需训练、无需真值标注

### 设计动机
- 减去背景 head 注意力消除 attention sink 噪声
- 只增强少数精选的视觉 head，不全局干预，保留推理流畅性

## 实验关键数据

### Head Masking 验证

| 模型 | Baseline | Random Mask | EFR-Guided Mask |
|------|----------|-------------|-----------------|
| Qwen2.5-VL-3B | 87.64 | 83.38 | **24.31** |
| Qwen2.5-VL-7B | 86.88 | 86.95 | **40.52** |

### VRGA 效果

| 模型 | Baseline | +VRGA |
|------|----------|-------|
| Qwen2.5-VL-3B (HaloQuest) | 58.87 | **59.03** |
| Qwen2.5-VL-3B (HallusionBench) | 53.40 | **54.90** |
| Qwen3-VL-30B (MMStar) | 66.1 | **67.1** |

### 关键发现
- CoT prompt 系统性降低 RRAR：$\bar{\Gamma}_\text{reason} < \bar{\Gamma}_\text{direct} < \bar{\Gamma}_\text{region-guided}$
- Region-guided prompt 效果最好——说明注意力分散是核心问题
- $R_\text{img}$-$H_\text{img}$ 线性关系在 5 个不同架构中一致（r > 0.9），是视觉处理的普遍规律
- EFR-guided head masking 导致灾难性下降（24.31%），证明这些 head 是视觉推理的命脉

## 亮点与洞察
- **"Deeper Thought, Weaker Aim" 的洞察**: CoT 不是让模型"看不见"，而是让模型"看散了"——从"感知退化"转向"注意力分散"的更精确诊断
- **$R_\text{img}$-$H_\text{img}$ 线性关系**: 跨模型的普遍规律，为自动识别视觉处理 head 提供了免标注方法
- **背景 head 减除**: 巧妙利用低层非视觉 head 来消除 attention sink 噪声

## 局限性 / 可改进方向
- VRGA 提升幅度在大模型上较小（Qwen3-VL-30B 只提 1 分），可能大模型本身注意力分散程度低
- 阈值 $\tau$ 和 $\lambda$ 需要调节，对不同任务可能需要不同设置
- 目前只在 VQA 上验证，对视频 QA、多轮对话等场景待探索

## 相关工作与启发
- **vs OutRo (同期)**: 都是推理时注意力干预，但 OutRo 关注 sink token 全局信息，VRGA 关注区域选择性
- **vs ICoT/DeepEyes**: 需要训练 + 全局注入视觉信息 → VRGA 免训练 + 选择性增强
- **vs Liu et al.**: 只发现"注意力总量下降" → VRGA 进一步分析空间分布

## 评分
- 新颖性: ⭐⭐⭐⭐ "注意力分散"假说比"感知退化"更精确，EFR 指标实用
- 实验充分度: ⭐⭐⭐⭐ 5 个模型的分析 + 多 benchmark 验证，但提升幅度较小
- 写作质量: ⭐⭐⭐⭐⭐ 分析从观察到假说到验证到方法，逻辑链完整
- 价值: ⭐⭐⭐⭐ 对理解 MLLM reasoning 退化有重要贡献
