# SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained T2I Generation

**日期**: 2026-03-23  
**arXiv**: [2603.22228](https://arxiv.org/abs/2603.22228)  
**代码**: [SpatialReward](https://github.com/LivingFutureLab/SpatialReward)  
**领域**: 图像生成 / 空间一致性  
**关键词**: spatial reward, text-to-image, reinforcement learning, verifiable reward, chain-of-thought

## 一句话总结
提出 SpatialReward，通过 Prompt 分解→专家检测器精确定位→VLM CoT 推理三阶段流水线构建可验证的空间 reward model，配合 SpatRelBench 基准（覆盖朝向、3D 关系、文字放置），在 SD3.5/FLUX 上用 RL 训练显著提升空间一致性。

## 研究背景与动机

1. **领域现状**: T2I 模型通过 RL+reward model 优化语义对齐和视觉质量（GRPO 等），但现有 reward model 主要关注全局语义和粗粒度质量。

2. **现有痛点**: 两类 RM 的弱点互补但各有盲区——结构化方法（GenEval）依赖固定格式 prompt + 预定义检测器，泛化差；整体评分方法（CLIPScore/VisionReward）处理任意 prompt 但缺乏空间细粒度验证，无法检测位置错误。

3. **核心矛盾**: 图像在全局语义上看起来合理，但物体位置关系（左右、上下、前后、朝向）经常出错。现有 RM "看不到"这些空间错误。

4. **切入角度**: 受逻辑推理领域"可验证 reward"成功的启发，用专家检测器提供客观可验证的位置/属性事实，再用 VLM 做 CoT 推理评估复杂空间关系。

5. **核心 idea**: Prompt 分解 + 专家检测器（可验证事实） + VLM CoT（复杂推理）= 可验证的空间 reward model。

## 方法详解

### 整体框架
标准 Flow-GRPO RL 训练 + SpatialReward 替代传统 RM。SpatialReward 三阶段：(a) Prompt Decomposer 解析结构化约束；(b) 专家检测器验证物体属性/位置/文字；(c) VLM CoT 推理评估复杂空间关系。

### 关键设计

1. **Prompt Decomposer**:
    - 将自由文本 prompt 解析为结构化约束集 $\mathcal{C} = (\text{tag}, \mathcal{C}_{inc}, \mathcal{C}_{exc})$
    - 每个原子约束包含：物体类别、数量、属性、空间关系、文字内容
    - 用 100k 元数据-prompt 对训练 Qwen2.5-VL-7B 做分解

2. **细粒度可验证 Reward**:
    - 存在性 reward: $\mathcal{R}_{presence} = \mathbb{I}(\hat{N}_c > 0)$
    - 计数 reward: $\mathcal{R}_{count} = \exp(-|\hat{N}_c - N_c^*|)$
    - 颜色 reward: CLIP 分类器在裁剪区域评估
    - 朝向 reward: $\mathcal{R}_{ori} = \mathbb{I}(|\theta_{det} - \theta^*| \leq \delta_\theta)$
    - 深度 reward: 单目深度估计验证前后关系
    - 文字 reward: OCR 检测 + IoA 定位验证

3. **Spatial CoT 推理**:
    - 用 Qwen2.5-VL 做 CoT backbone
    - 输入包括目标关系、检测框、前阶段各属性 reward 分数
    - VLM 逐步推理：解释属性 reward → 几何分析 → 判断关系是否成立
    - 包含/排除约束分别给正/负分：$\mathcal{R}_{total} = \sum_{inc} \mathcal{R}^+ - \sum_{exc} \mathcal{R}^-$

### SpatRelBench 基准
覆盖 6 个维度：位置-文字 OCR、计数-文字 OCR、复杂空间关系、朝向、3D 空间关系，比 GenEval 和 T2I-CompBench 更全面。

## 实验关键数据

### GenEval + SpatRelBench 对比

| Reward Model | GenEval Overall | SpatRelBench Overall |
|-------------|-----------------|---------------------|
| SD3.5-M (baseline) | 0.67 | 0.23 |
| + PickScore | 0.74 | 0.24 |
| + ImageReward | - | - |
| + **SpatialReward** | **最佳** | **最佳** |
| GPT Image 1 | 0.84 | 0.37 |

### 关键发现
- SpatialReward 在 GenEval 和 SpatRelBench 上均超越 PickScore/ImageReward 等 holistic RM
- 朝向和 3D 空间关系是所有模型最薄弱的维度（GPT Image 1 仅 0.15/0.45）
- 可验证 reward 的关键在于检测器提供"事实基础"，避免 VLM 幻觉

## 亮点与洞察
- **可验证 reward 从推理迁移到视觉**: 将 DeepSeek-R1 式的 rule-based verifiable reward 思路扩展到图像空间评估
- **检测器+VLM 协作**：检测器提供客观事实，VLM 做需要语义理解的复杂推理，各司其职
- **SpatRelBench 填补空白**: 朝向、3D 位关系、文字放置是之前 benchmark 不覆盖的

## 局限性 / 可改进方向
- 检测器本身的精度和泛化性限制了 reward 质量
- CoT 推理依赖 VLM（Qwen2.5-VL），可能引入推理错误
- multi-stage pipeline 推理开销大，RL 训练效率可能受影响
- SpatRelBench 规模相对较小（1k objects）

## 评分
- 新颖性: ⭐⭐⭐⭐ 可验证 reward 在 T2I 空间评估中的新应用
- 实验充分度: ⭐⭐⭐⭐ SD3.5 和 FLUX 两个基座，多 reward model 对比
- 写作质量: ⭐⭐⭐⭐ 框架清晰，公式规范
- 价值: ⭐⭐⭐⭐ 对 T2I 空间控制和 RL tuning 有实际意义
