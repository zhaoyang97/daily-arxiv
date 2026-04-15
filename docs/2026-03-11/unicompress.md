# UniCompress: Token Compression for Unified Vision-Language Understanding and Generation

**日期**: 2026-03-11  
**arXiv**: [2603.11320](https://arxiv.org/abs/2603.11320)  
**代码**: 暂未看到公开仓库  
**领域**: 多模态模型效率 / Token 压缩  
**关键词**: token compression, unified model, global meta tokens, decompressor, plug-in

## 一句话总结
提出 UniCompress：在不改 LLM 主干的前提下，对统一视觉-语言模型加入“压缩器 + 全局元 token + 解压器”，把视觉 token 压缩到 1/4，同时保持理解任务小幅掉点，并把推理延迟最多降低 41.8%。

## 研究背景与动机

1. **问题来源**: 统一模型需要同一套视觉 token 同时服务“理解”和“生成”。
2. **核心矛盾**:
    - 理解任务对 token 粒度相对不敏感
    - 生成任务对细节和空间结构非常敏感
3. **痛点**: 直接剪枝/下采样虽然节省算力，但会显著伤害生成质量（文中指出可超过 15%）。

## 方法详解

### 整体思路
给现有 tokenizer 外挂三件套：
- 全局语义提取器（global tokens）
- 局部压缩器（pooling）
- 全局引导解压器（autoregressive decompressor）

并采用两阶段训练：
- Stage 1：只训 tokenizer 侧模块（压缩-重建）
- Stage 2：冻结 tokenizer，微调 LLM 适应压缩 token

### 核心模块

1. **Global Meta Tokens**
- 用可学习 query 对密集视觉 token 做 cross-attention
- 提取 $N_g$ 个全局 token，作为场景级语义锚点

2. **压缩器**
- 对视觉 token 网格做 $s\times s$ 平均池化，序列长度从 $T$ 变为 $T/s^2$
- 例：256 -> 64（4x 压缩）

3. **全局引导解压器**
- 输入：压缩后的局部 token + 全局 token
- 输出：恢复到高分辨率密集 token，再交给图像解码器
- 作用：补回压缩丢失的长程结构和细节纹理

## 实验关键数据

### 理解任务（示例）

| 方法 | GQA | MME | POPE | Seed-bench |
|------|-----|-----|------|-----------|
| VARGPT | 58.12 | 1290.65 | 88.04 | 50.54 |
| VARGPT-Compressed | 55.90 | 1272.80 | 84.99 | 48.41 |
| BAGEL | 60.05 | 1312.40 | 89.20 | 51.10 |
| BAGEL-Compressed | 59.10 | 1304.10 | 88.60 | 50.80 |

### 生成任务（示例）

| 方法 | FID ↓ | CLIP ↑ |
|------|-------|--------|
| VARGPT | 14.77 | 24.2 |
| VARGPT-Compressed | 15.02 | 21.6 |
| BAGEL | 12.73 | 32.0 |
| BAGEL-Compressed | 17.22 | 28.8 |

### 关键结论
- 4x 压缩下理解性能通常仅小幅下降
- 生成质量下降因模型而异，部分模型影响较明显
- 速度收益显著：推理延迟最高降低 41.8%，训练时间缩短 15.4%

## 亮点与洞察
- 不是单纯剪 token，而是“压缩 + 可恢复”思路，更符合统一模型需求
- 全局 token 对生成质量保持至关重要
- 插件式设计使其可迁移到多种统一模型，不用重训整个系统

## 局限性
- 固定压缩率（如 4x）在不同图像复杂度下可能不最优
- 部分模型生成质量损失仍偏大（如 BAGEL 的 FID 劣化）
- 还缺更系统的内容自适应压缩实验

## 评分
- 新颖性: ⭐⭐⭐⭐
- 实验充分度: ⭐⭐⭐⭐
- 写作质量: ⭐⭐⭐⭐
- 价值: ⭐⭐⭐⭐（对统一模型落地非常实用）
