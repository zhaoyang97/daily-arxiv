# MURE: Hierarchical Multi-Resolution Encoding via Vision-Language Models for Visual Document Retrieval

**日期**: 2026-03-07  
**arXiv**: [2603.13349](https://arxiv.org/abs/2603.13349)  
**代码**: 无  
**领域**: 多模态/VLM  
**关键词**: visual document retrieval, multi-resolution encoding, Matryoshka representation, token compression, VLM

## 一句话总结
提出 MURE，通过多分辨率采样 + Resolution-level Matryoshka 表示学习 + 语义感知层次聚类压缩，实现视觉文档检索中粗细粒度特征的统一编码——仅用 ColPali 50% 的视觉 token 就超越其性能，在 ViDoRe V1/V2 上达到 PaliGemma 系列 SOTA。

## 研究背景与动机

1. **领域现状**: 视觉文档检索（VDR）将文档页面作为整体视觉输入处理（而非 OCR→文本），保留了布局和视觉信息。当前方法基于 VLM 编码文档图像。

2. **现有痛点**: (a) 固定分辨率方法（如 ColPali 336×336）丢失高分辨率文档的精细信息；(b) 原生分辨率方法保留细节但生成大量视觉 token，导致索引存储和延迟开销巨大；(c) 两种方法都局限于单一静态视角，无法同时捕获高层布局结构和底层局部细节。

3. **核心矛盾**: 文档检索需要同时理解全局布局（如"美国在地图上的颜色"）和局部细节（如"图例中某颜色代表什么"），但现有方法只能二选一。

4. **切入角度**: 多分辨率采样——像"光学变焦"一样在不同尺度上观察文档，然后融合不同粒度的特征。

5. **核心 idea**: X-VisEmb 范式——多分辨率采样编码 → 跨粒度特征融合 → 自适应表示蒸馏，MURE 是这一范式的具体实现。

## 方法详解

### 整体框架
文档图像 $\mathbf{I}$ → 多分辨率采样（1×1, 1×2, 2×2, 2×3 网格） → 共享 VLM 视觉编码器处理每个尺度 → 拼接多尺度特征序列 → LLM backbone 自注意力融合 → 线性投影 → Resolution-level Matryoshka 嵌套表示 → 推理时语义聚类压缩到目标 token 数 → Late Interaction (MaxSim) 检索评分。

### 关键设计

1. **多分辨率采样与编码**:
    - 做什么：在不同网格尺度（$\mathcal{G} = \{1\times1, 1\times2, 2\times2, 2\times3\}$）上采样文档图像
    - 核心思路：每个尺度将图像分割为对应网格的子区域，调整到固定大小送入共享 SigLIP 编码器 + 投影层，得到 $\mathbf{V}^{(k)} \in \mathbb{R}^{M_k \times d}$
    - 设计动机：初步实验显示组合最优粒度在 ViDoRe V1/V2 上分别带来 +4.8%/+24.1% 的相对提升，证明多尺度感知的巨大潜力

2. **Resolution-level Matryoshka 表示学习 (RMRL)**:
    - 做什么：将不同分辨率的特征嵌套成俄罗斯套娃结构
    - 核心思路：$\mathbf{D}^{(k)} = \text{Concat}(\mathbf{H}^{(1)}, ..., \mathbf{H}^{(k)})$，从最粗到最细逐级嵌套。训练时用加权多级 InfoNCE loss：$\mathcal{L} = \sum_k w_k \cdot \mathcal{L}_{NCE}^{(k)}$
    - 设计动机：(a) 允许在不同 token 预算下弹性部署；(b) 粗粒度表示被更细粒度共享，强制粗粒度学到高质量全局语义

3. **语义感知层次聚类压缩**:
    - 做什么：推理时将 token 数量压缩到目标预算
    - 核心思路：对嵌套表示的 token 做层次聚类，基于语义相似度合并冗余 token，用户可动态选择 512/1024/1536/Full 不同预算
    - 设计动机：实现效果-效率的灵活权衡——512 token 已超越 ColPali 的 1024 token

### 训练策略
- 基座：PaliGemma-3B + SigLIP-So400m 视觉编码器
- 多级加权 InfoNCE loss，权重 $w_k$ 平衡各尺度贡献
- In-batch negatives 对比学习

## 实验关键数据

### 主实验

| 模型 | Token数 | ViDoRe V1 (NDCG@5) | ViDoRe V2 (NDCG@5) |
|------|---------|-------------------|-------------------|
| **MURE_Full** | Full | **87.0** | **60.5** |
| MURE_1024 | 1024 | 86.4 | 59.1 |
| **MURE_512** | 512 | **85.7** | **58.2** |
| ColPali | 1024 | 84.9 | 54.5 |
| ColMate-Pali | 1024 | 85.1 | 55.8 |
| ColQwen2 | - | 89.2 | 57.5 |

### 消融/分析

| 配置 | ViDoRe V1 | 说明 |
|------|----------|------|
| 单一 1×1 | ~82 | 仅粗粒度，丢失细节 |
| 单一 2×3 | ~84 | 仅细粒度，丢失全局 |
| 多分辨率组合（Oracle） | ~89 | 每个 query 选最优粒度的上界 |
| MURE_512 | 85.7 | 仅用 50% token 超越 ColPali |
| MURE_Full | 87.0 | 接近 Oracle 上界 |

### 关键发现
- **50% token 超越 ColPali**: MURE_512（512 token）在 V1 上 85.7% vs ColPali 84.9%，存储减半且性能更好
- **跨域泛化强**: ViDoRe V2 是 out-of-domain，MURE_Full 60.5% vs ColPali 54.5%，相对提升 11%
- **Matryoshka 结构有效**: 嵌套训练使得各 token 预算都有良好表现，无需针对每个预算单独训练
- **多分辨率互补性大**: 初步实验 Oracle 组合在 V2 上相对单分辨率提升 24.1%，说明不同 query 确实需要不同粒度

## 亮点与洞察
- **X-VisEmb 范式**: "多分辨率采样→跨粒度融合→自适应蒸馏"的三阶段范式可推广到其他视觉任务
- **Matryoshka 推广到分辨率维度**: 原始 Matryoshka 在维度上嵌套，这里推广到分辨率/token 数量上嵌套，是巧妙的泛化
- **实用的弹性部署**: 单个模型支持多种 token 预算，部署时按资源约束灵活选择

## 局限性 / 可改进方向
- **仅基于 PaliGemma-3B**: 未在更大 VLM（如 Qwen2-VL）上验证
- **聚类压缩的质量**: 层次聚类可能合并语义不同但特征相近的 token
- **训练开销**: 多分辨率输入增加了训练时的计算量和显存需求
- **改进方向**: 学习自适应分辨率选择（而非固定网格集合），或用更先进的 token 合并策略

## 相关工作与启发
- **vs ColPali**: ColPali 用固定分辨率，MURE 通过多分辨率+压缩在更少 token 下超越
- **vs DSE/ColQwen2**: 使用更大 LLM backbone 的方法在 V1 上更强，但 MURE 在 PaliGemma-3B 范围内是 SOTA
- **启发**: 多分辨率感知的思路可用于视觉 RAG、文档问答等需要理解文档布局的场景

## 评分
- 新颖性: ⭐⭐⭐⭐ 多分辨率 + Matryoshka 结合的思路新颖，X-VisEmb 范式有推广价值
- 实验充分度: ⭐⭐⭐⭐ 两个基准、多 token 预算对比、初步实验验证假设
- 写作质量: ⭐⭐⭐⭐ 范式清晰，从假设到验证到方法的逻辑链完整
- 价值: ⭐⭐⭐⭐ 对视觉文档检索的效率-效果权衡有实际意义
