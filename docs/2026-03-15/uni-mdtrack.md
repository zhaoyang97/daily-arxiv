# Uni-MDTrack: Learning Decoupled Memory and Dynamic States for Parameter-Efficient Visual Tracking in All Modality

**日期**: 2026-03-15  
**arXiv**: [2603.14452](https://arxiv.org/abs/2603.14452)  
**代码**: 无  
**领域**: 视频理解 / 目标检测  
**关键词**: visual tracking, memory compression, SSM, parameter-efficient, multi-modal

## 一句话总结
提出 Uni-MDTrack，用 Memory-Aware Compression Prompt (MCP) 将记忆库压缩为固定 token + Dynamic State Fusion (DSF) 用 SSM 捕捉目标连续动态状态，仅训练 <30% 参数即在 RGB/RGB-D/T/E/Language 五种模态 10 个数据集上达到 SOTA。

## 研究背景与动机

1. **领域现状**: One-stream Transformer tracker 在模板-搜索区域关系建模上已很强，但缺乏有效的时空上下文建模。
2. **现有痛点**: (a) 记忆库方法只在 prediction head 前融合，不够深；(b) 辅助模板法增加序列长度、计算开销大；(c) 时间传播 token 同时关注模板和搜索区域，更像"模板增强器"而非动态状态表示。
3. **核心 idea**: MCP 用可学习 query 将记忆库压缩为固定数量 token，在 backbone 每层深度交互；DSF 用 SSM 只从搜索区域特征更新目标动态状态，避免模板污染。

## 方法详解

### 整体框架
模板 + 搜索区域 + 记忆库 → MCP 将记忆压缩为固定 token 并深度融入 backbone → DSF 用 SSM 从搜索区域提取目标动态状态 → 多阶段融合 → 预测头输出跟踪结果。

### 关键设计
1. **MCP (Memory-Aware Compression Prompt)**:
   - 做什么：将可变长记忆库压缩为固定 16 个 memory token
   - 核心思路：$N_M$ 个可学习 query token $\mathbf{q}$ 通过 cross-attention 对记忆库 $\mathbf{F}_m$ 做动态聚合：$\mathbf{Attn} = \text{Softmax}[\mathbf{Q} \cdot \mathbf{K} / \sqrt{d} + \text{ALiBi}(\mathbf{F}_m)]$，输出 memory-aware token concat 到输入序列在全层参与自注意力
   - ALiBi 位置偏置: $-\mathbf{m}_h \times |j - N_{mb}|$，赋予近帧更高权重，同时实现推理时记忆长度免训练外推（理论证明尾部质量指数衰减，不影响已训练分布）
   - 设计动机：传统记忆库在 prediction head 前融合太浅，MCP 让记忆信息在每一层深度影响特征学习

2. **DSF (Dynamic State Fusion)**:
   - 做什么：持续捕捉目标的连续动态状态变化
   - 核心思路：基于 Mamba SSM 的状态更新 $h(t) = \bar{\mathbf{A}} \odot h(t-1) + \bar{\mathbf{B}} \odot \mathbf{S}_1$，只用搜索区域特征更新（排除模板干扰）。4 个 DSF 模块分布在 backbone 的 4 个阶段，通过 input/output fusion layer (cross-attention) 实现渐进融合
   - 设计动机：现有时间传播 token 同时关注模板和搜索区域，更像"模板增强器"而非动态状态。DSF 专注搜索区域的状态演化
   - 与先前 SSM tracker 的区别: MambaVT/MCITrack 用 SSM 作 backbone（需设计扫描策略），DSF 用 SSM 作 PEFT 适配器（首创）

3. **统一多模态设计**: 6 通道输入（RGB 3ch + D/T/E 3ch），对纯 RGB 任务复制 RGB 通道。文本通过 CLIP-L 提取 [cls] token。一个模型覆盖 RGB/RGB-D/T/E/Language 五种模态。

## 实验关键数据

### 计算效率

| 方法 | 可训练参数(M) | 总参数(M) | FLOPs(G) |
|------|-------------|----------|----------|
| HIPTrack | 34.1 | 66.9 | 120.4 |
| LoRAT-B384 | 13.0 | 97.0 | 99.1 |
| SPMTrack-B | 29.2 | — | 115.3 |
| **Uni-MDTrack-B** | **27.1** | **27.9** | **88.2** |
| Uni-MDTrack-L | 54.9 | 257.4 | 287.4 |

### RGB 跟踪性能

| 方法 | LaSOT AUC% | TrackingNet AUC% | LaSOText AUC% |
|------|-----------|-----------------|---------------|
| SUTrack-B224 | 73.2 | 85.7 | 53.1 |
| SUTrack-L384 | 75.2 | 87.7 | — |
| LoRAT-B384 | 72.1 | 85.6 | 51.5 |
| SPMTrack-B | 73.4 | 86.0 | — |
| **Uni-MDTrack-B** | **74.7** | **86.1** | **54.3** |
| **Uni-MDTrack-L** | **76.1** | **88.0** | **55.2** |

### 多模态跟踪性能

| 方法 | LasHeR SR% (RGB-T) | VisEvent F-Score% (RGB-E) | DepthTrack Re% (RGB-D) |
|------|-------------------|-------------------------|------------------------|
| SUTrack-B224 | 59.9 | 65.1 | 65.7 |
| FlexTrack (ICCV25) | 62.0 | 67.0 | 66.9 |
| **Uni-MDTrack-B** | **61.2** | **65.9** | **66.3** |
| **Uni-MDTrack-L** | **62.1** | **67.4** | **67.2** |

### 关键发现
- 10 个数据集跨 5 种模态全部 SOTA 或 competitive，<30% 可训练参数
- RGB-only：Uni-MDTrack-B 比 SUTrack-B224 LaSOT AUC 高 +1.5%
- MCP 和 DSF 可作为 plug-and-play 组件，分别为基线 tracker 带来稳定提升

## 亮点与洞察
- **记忆压缩的深度交互**：MCP 让记忆从"在输出端打补丁"变为"在全层深度融合"，显著提升时空上下文利用
- **SSM 用于跟踪动态状态的首次探索**：Mamba 的状态建模天然适合跟踪场景中目标的连续状态演化
- **多模态统一架构**：一个模型覆盖 5 种模态 10 个数据集，避免了为每种模态训练独立模型

## 相关工作对比
- **vs HIPTrack**: 仅在 prediction head 前融合记忆，MCP 全层深度交互，FLOPs 66.9G vs 27.9G
- **vs SPMTrack**: 传播 token 同时关注模板和搜索区域，DSF 仅用搜索区域验证去除模板污染的重要性
- **vs MambaVT/MambaLT**: 用 SSM 替代 backbone 需复杂扫描策略，DSF 作为 PEFT 插件更轻量


## 相关工作对比
- **vs HIPTrack**: 仅在 prediction head 前融合记忆，MCP 全层深度交互，FLOPs 66.9G vs 27.9G
- **vs SPMTrack**: 传播 token 同时关注模板和搜索区域，DSF 仅用搜索区域验证去除模板污染的重要性
- **vs MambaVT/MambaLT**: 用 SSM 替代 backbone 需复杂扫描策略，DSF 作为 PEFT 插件更轻量


## 局限性 / 可改进方向
- MCP 的记忆 token 数量（16）是固定的，可能不是所有场景的最优选择
- DSF 的效果依赖 Mamba SSM 的长程建模能力在跟踪任务中的适用性
- 未在超长序列（>1000 帧）上验证 ALiBi 外推的实际效果

## 评分
- 新颖性: ⭐⭐⭐⭐ MCP 的记忆压缩 + DSF 的 SSM 动态状态是好的组合
- 实验充分度: ⭐⭐⭐⭐⭐ 10 个数据集 + 5 种模态 + 即插即用验证
- 写作质量: ⭐⭐⭐⭐ 理论分析（SSM 外推、ALiBi 边界）有深度
- 价值: ⭐⭐⭐⭐ 参数高效多模态跟踪的实用框架
