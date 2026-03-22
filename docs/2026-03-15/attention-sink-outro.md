# On the Nature of Attention Sink that Shapes Decoding Strategy in MLLMs

**日期**: 2026-03-15  
**arXiv**: [2603.14337](https://arxiv.org/abs/2603.14337)  
**代码**: 无  
**领域**: 多模态VLM  
**关键词**: attention sink, MLLM, inference-time, video QA, OutRo

## 一句话总结
系统分析 MLLM 中 attention sink 现象的本质，发现 sink token 的 value 表示编码了结构化全局信息（而非无用），据此提出 OutRo——通过将非 sink 位置的 head output 旋转向 sink value 方向 + 放松 sink token 的因果 mask，在 7 个视频 QA benchmark 上一致提升性能，仅 1.1× 解码开销。

## 研究背景与动机

1. **领域现状**: Attention sink 现象已在 LLM 和 VLM 中广泛观察——模型将大量注意力分配给语义上无关的 token（如 BOS、标点、背景 patch）。主流观点将 sink head 视为冗余/不活跃头，可以剪枝提效。

2. **现有痛点**: 现有工作把 sink 当作可移除的噪声，但实验发现剪枝 sink head 有时提升有时降低性能——不能简单视为冗余。sink token 的表示特性（key/value）一直被忽视。

3. **核心矛盾**: 如果 attention sink 真的无用，为什么移除后模型反而会退步？sink token 是否在隐式地承担某种功能？

4. **切入角度**: 不关注 head 层面的剪枝，转而分析 sink **token 自身**的表示。通过几何分析发现 sink value 虽然 norm 小，但方向一致，编码了全局信息。

5. **核心 idea**: Sink token 是全局信息的载体。利用这一发现，将 non-sink token 的 head output 旋转向 sink value 方向（对齐全局信息），并放松 sink token 的因果约束（增强信息聚合）。

## 方法详解

### 分析发现（三个核心问题）

**Q1: 如何识别 sink token？** 对比 VLM 标准 (Φ_VLM) 和 LLM 标准 (Φ_LLM)：Φ_VLM 在深层把大多数 token 都标为 sink（过度识别），而 Φ_LLM 只识别极少数稳定的 sink token。结论：Φ_LLM 更适用于通用 MLLM。

**Q2: Sink head = 冗余？** 逐 head 消融实验显示，高 sink 注意力的 head 可能提升也可能降低性能——sink attention 不能预测 head 重要性。

**Q3: Sink 编码全局信息？** Sink key/value norm 小但结构化（Fig.4），key 与 query 方向高度对齐（高 cosine similarity），移除 sink key 主导维度后 sink 注意力模式崩塌且性能下降（Zero-K 实验）。旋转 head output 向 sink value 方向 → 性能提升；放松 sink 因果 mask → 性能提升。

### OutRo 方法

1. **Head Output Rotation**:
   - 做什么：将 non-sink 位置的 attention head output 向 sink value 方向旋转
   - 核心思路：投影 head output 到 sink value 向量方向，加上投影分量后 rescale
   - 设计动机：让所有 token 表示与 sink 编码的全局信息方向对齐

2. **Causal Mask Relaxation for Sink Tokens**:
   - 做什么：从 sink 行为开始显著的层开始，允许 sink token attend 到后续 token
   - 核心思路：选择性放松 causal mask，让 sink 能聚合更多全局上下文
   - 设计动机：sink token 已经自然地编码全局信息，给它更多信息来源只会更好

### 关键优势
- **不需要 attention map 访问**：在 head output 级别操作，兼容 FlashAttention
- **不需要额外 forward pass**：不像 contrastive decoding 需要多次前向
- **仅 1.1× 解码开销**

## 实验关键数据

### 主实验（视频 QA）

在 6 个 MLLM（包括 Qwen2.5-VL、VideoLLaMA3 等）× 7 个 benchmark 上一致提升。

| 干预 | AVHBench (A→V) | AVHBench (V→A) |
|------|----------------|----------------|
| Baseline | 80.11 | 75.41 |
| + Rotation | **80.81** | **75.72** |

### 消融实验

| 实验 | 结论 |
|------|------|
| Zero-K (去 sink key 主导维度) | 性能大幅下降（Qwen2.5-VL: 41.26→14.75） |
| Head ablation | Sink score 不能预测 head 重要性 |
| Rotation only | 稳定提升 |
| Injection (mask relaxation) | 额外小幅提升 |

### 关键发现
- Φ_VLM 标准在视频 MLLM 中严重过度识别 sink（深层几乎所有 token 都被标为 sink）
- Zero-K 最致命——只去掉 top-1 维度就能摧毁 sink 注意力模式，且性能暴跌
- Sink value 虽然 norm 小，但方向一致且有功能意义——是全局信息的压缩载体

## 亮点与洞察
- **重新定义 attention sink**: 从"可剪枝的冗余"到"全局信息载体"，概念转变有深度
- **旋转操作的优雅性**: 不修改模型权重，不需要训练，不需要 attention map，仅 head output 级别操作
- **跨模态一般性**: 分析从视频 MLLM 到 audio-visual LLM 都验证，不限于图像 VLM

## 局限性 / 可改进方向
- 旋转的强度如何自适应控制？当前似乎是固定比例
- 只在推理时干预，能否把 sink 的功能理解应用到训练？
- 实验主要在视频 QA 上，对生成任务（如 image captioning）是否同样有效未验证

## 相关工作与启发
- **vs SinkPruning（Qiu 等）**: 之前的工作剪枝 sink head → 本文证明 sink 不能简单剪枝
- **vs DCoT（Liu 等）**: contrastive decoding 需要多次 forward → OutRo 仅 1.1× 开销
- **vs Register Tokens（Darcet 等）**: ViT 中加专门的 register token → OutRo 利用已有的 sink token

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 对 attention sink 的重新理解有深度和原创性
- 实验充分度: ⭐⭐⭐⭐⭐ 6 个模型 × 7 个 benchmark + 系统的分析实验
- 写作质量: ⭐⭐⭐⭐⭐ Q1-Q3 的分析结构清晰优雅
- 价值: ⭐⭐⭐⭐ 推理时免训练提升 MLLM，实用性好
