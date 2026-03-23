# VisDoT: Enhancing Visual Reasoning through Human-Like Interpretation Grounding and Decomposition of Thought

**日期**: 2026-03-12  
**arXiv**: [2603.11631](https://arxiv.org/abs/2603.11631)  
**代码**: 无  
**领域**: 多模态VLM / 图表推理  
**关键词**: chart understanding, decomposition of thought, visual reasoning, graphical perception, VQA

## 一句话总结
提出 VisDoT 框架，基于图形感知理论定义四类感知任务（Position/Length/Pattern/Extract），引入分解思维（DoT）提示将复杂视觉问题拆分为感知子问题→逻辑子问题的链式推理，微调 InternVL 在 ChartQA 上提升 11.2%，超越 GPT-4o，且零样本迁移到开放域 VQA 也有效。

## 研究背景与动机

1. **领域现状**: LVLM 在图表/图形理解上仍然薄弱——缺乏可靠检测视觉基元（颜色、位置、长度等）并与语义对齐的能力。

2. **现有痛点**: 现有 CoT 推理策略对文本推理有效，但对需要视觉定位的推理场景增益有限。用户查询不提及图例标签或轴名时，LVLM 性能严重下降。

3. **核心 idea**: 模拟人类图形解读的认知过程——先做视觉感知（识别位置、长度、图案），再做逻辑推理。将 VQA 重新定义为感知+逻辑的组合任务。

## 方法详解

### 整体框架
图表图像 + 问题 → DoT 提示引导 → Phase 1: 问题分解（感知子问题 + 逻辑子问题）→ Phase 2: 逐步求解 → 最终答案。

### 关键设计

1. **四类感知任务（基于图形感知理论）**:
   - **Position**: 沿公共尺度比较对象位置，是最准确的感知通道
   - **Length**: 无畸变的视觉属性，作为位置的辅助线索
   - **Pattern**: 链接图案线索到图例以区分类别
   - **Extract**: 读取显式数值，类似 OCR

2. **DoT（Decomposition of Thought）提示**:
   - 将 $P(A|I,Q) = \sum P(\{Q_1^p,...,Q_n^l\}|Q) \cdot \prod P(A_i|I,Q_i,A_{<i})$
   - 强制感知子问题 $Q^p$ 在逻辑子问题 $Q^l$ 之前
   - 每个子问题的答案依赖于图像和之前的答案，支持上下文感知的多步推理

3. **VisDoTQA 数据集**: 331,969 个 QA 对，GPT-4o 生成问题，LLaMA-3.2-90B 生成 DoT 答案

## 实验关键数据

### 主实验

| 模型 | ChartQA Avg | ChartQAPro Avg | VisDoTQA Avg |
|------|------------|---------------|-------------|
| GPT-4o | 85.7 | 37.67 | 57.14 |
| Gemini-Flash-2.0 | 85.12 | 46.85 | 61.96 |
| InternVL-4B (baseline) | 75.08 | 17.81 | 34.20 |
| **InternVL-4B + VisDoT** | **86.28** | **31.91** | **67.40** |

### 消融实验

| 配置 | ChartQA | 说明 |
|------|---------|------|
| CoT (传统链式思维) | 79.5% | 标准 CoT 效果有限 |
| DoT (感知→逻辑分解) | **86.3%** | 分解为感知+逻辑显著提升 |

### 关键发现
- 4B 模型 + VisDoT 超越 GPT-4o（86.3% vs 85.7%）
- DoT 在 POPE (+1.43%) 和 MMMU (+2.2%) 等开放域 VQA 也有提升，说明感知-逻辑分离策略通用
- 感知优先（先做视觉定位再推理）是关键——移除感知优先约束性能下降

## 亮点与洞察
- **从认知心理学出发的感知任务定义**非常有理论基础——Position/Length/Pattern/Extract 与人类图形解读认知对齐
- **DoT vs CoT**：CoT 只做文本推理，DoT 先做视觉感知再推理，从根本上解决了 CoT 在视觉任务上增益有限的问题
- 小模型(4B) + 正确训练策略可以超越大闭源模型

## 局限性 / 可改进方向
- VisDoTQA 的生成依赖 GPT-4o，数据构建不完全开源
- 仅在图表/图形场景深入验证，其他视觉推理场景覆盖有限
- 四类感知任务是手动定义的，可能遗漏某些重要感知维度

## 评分
- 新颖性: ⭐⭐⭐⭐ DoT 和图形感知理论的结合是新颖贡献
- 实验充分度: ⭐⭐⭐⭐ 多 benchmark + CoT/DoT 对比 + 开放域验证
- 写作质量: ⭐⭐⭐⭐ 理论推导清晰
- 价值: ⭐⭐⭐⭐ 对图表理解和通用视觉推理都有参考价值
