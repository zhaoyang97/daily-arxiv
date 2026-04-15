# Relax Forcing: Relaxed KV-Memory for Consistent Long Video Generation

**日期**: 2026-03-22  
**arXiv**: [2603.21366](https://arxiv.org/abs/2603.21366)  
**代码**: [项目主页](https://zengqunzhao.github.io/Relax-Forcing)  
**领域**: 视频理解  
**关键词**: long video generation, autoregressive diffusion, KV memory, temporal consistency, sparse conditioning

## 一句话总结
提出 Relax Forcing，用结构化稀疏 KV-Memory 替代稠密时序缓存来生成一致的长视频——将历史帧分解为 Sink（全局锚点）/History（动态选择的中程运动）/Tail（近程连续性）三个功能角色，在 60 秒视频生成上比 Deep Forcing 提升 1.24%，动态度提升 66.8%。

## 研究背景与动机

1. **领域现状**: 自回归视频扩散可以生成长视频（30s+），但随时间推移质量逐渐退化。Self-Forcing 训练减少了 exposure bias，但误差累积仍然存在。

2. **现有痛点**: (a) 稠密 KV-Memory 不可扩展——增加上下文长度不一定改善质量；(b) 历史帧的**时间位置**比**数量**更重要——不是越多越好；(c) 长视频中运动动态度容易坍缩为静态重复。

3. **关键发现**: 通过实验分析发现，中程历史帧（mid-range）的后半段比前半段或非常近的帧更有信息量，且稠密记忆中大量帧是冗余的。

4. **核心 idea**: 将时序上下文按功能分解为三类——Sink 提供全局外观锚定，Tail 提供近程运动延续，History 从中程动态选择最有信息量的帧——用 relaxation score 平衡稳定性和冗余性。

## 方法详解

### 整体框架
Chunk-wise AR 生成 → 每步重建稀疏记忆 $\mathcal{M}_i = \mathcal{S} \cup \mathcal{H}_i \cup \mathcal{T}_i$ → Sink (~2帧) 固定为早期帧、Tail (~1帧) 为最近帧、History (~1帧) 从中程候选池动态选择 → Hybrid RoPE 编码 → 稀疏 attention 生成下一 chunk。

### 关键设计

1. **三角色时序记忆分解**:
    - **Sink（锚点）**: 视频最早几帧，提供全局外观/风格一致性
    - **Tail（尾部）**: 最近生成的帧，保证短程运动连续性
    - **History（历史）**: 从中程候选池动态选择，传递运动结构和主题演变
    - 每种角色只需 1-2 帧，总记忆远小于稠密方式

2. **Relaxation Score 动态选帧**:
    - $r(h) = S(h) - \lambda R(h)$
    - $S(h)$: 与 Sink 原型的相似度（稳定性分）——越像 Sink 越能维持一致性
    - $R(h)$: 与 Tail 原型的相似度（冗余分）——越像 Tail 说明信息冗余
    - 候选池限制在中程后半段（实验发现后半段更有信息量）
    - 取 Top-K 作为 History 帧

3. **Hybrid RoPE 编码**:
    - Tail 使用绝对时序索引（保留真实时间位置）
    - Sink 和 History 使用相对索引（锚定在 Tail 之前）
    - 避免远距离帧被"压缩"到近程上下文窗口中

## 实验关键数据

### 主实验（VBench-Long）

| 方法 | 30s Overall | 60s Overall | Dynamic Degree |
|------|------------|------------|----------------|
| Self Forcing | 79.1% | — | 36.62 |
| Deep Forcing | 79.94% | 79.64% | ~40 |
| **Relax Forcing** | **80.87%** | **80.88%** | **65.67** |

### 消融实验

| 配置 | Overall | Dynamic | Subject Consistency |
|------|---------|---------|-------------------|
| Sink only | 良好 | 低（运动受限） | 高 |
| History only | — | 高 | 低（无锚点漂移） |
| Tail only | — | — | 短程好/长程差 |
| Sink + History + Tail | **最优** | **最优** | **平衡** |

### 关键发现
- 动态度 (Dynamic Degree) 提升 66.8% 是最显著的改进——从 36.62 到 65.67
- 60 秒生成比 30 秒更鲁棒（baseline 退化但 Relax Forcing 保持）
- 时序位置比记忆总量更重要——少量精选帧 > 大量稠密帧

## 亮点与洞察
- **"质量 > 数量"的记忆策略**: 首次系统分析长视频 AR 扩散中时序记忆的功能角色，证明稀疏精选优于稠密
- **三角色分解直觉清晰**: Sink/History/Tail 的功能划分与人类记忆的"schema/episodic/working memory"类比
- **Relaxation Score 设计精巧**: 平衡稳定性和冗余性，自然地选出"最有信息量"的历史帧

## 局限性 / 可改进方向
- 超参数（Sink/History/Tail 数量、$\lambda$ 平衡系数）需要手动调节
- 仅在 Self-Forcing 框架上验证，对其他 AR 方法的适用性未知
- 未深入分析"为什么中程后半段比前半段更有信息量"的原因
- 只在 VBench-Long 上评估

## 评分
- 新颖性: ⭐⭐⭐⭐ 时序记忆功能分解的视角新颖
- 实验充分度: ⭐⭐⭐⭐ 多时长、细粒度消融
- 价值: ⭐⭐⭐⭐ 解决长视频生成的关键难题
