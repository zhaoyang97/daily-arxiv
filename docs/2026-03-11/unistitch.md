# UniStitch: Unifying Semantic and Geometric Features for Image Stitching

**日期**: 2026-03-11  
**arXiv**: [2603.10568](https://arxiv.org/abs/2603.10568)  
**代码**: [github.com/MmelodYy/UniStitch](https://github.com/MmelodYy/UniStitch)  
**领域**: 多模态VLM / 图像拼接  
**关键词**: image stitching, semantic features, geometric features, Neural Point Transformer, Mixture of Experts

## 一句话总结
首次将传统几何特征（关键点）与学习语义特征统一到图像拼接框架中，通过 Neural Point Transformer 将稀疏离散关键点转换为密集 2D 几何图，再用 Adaptive Mixture of Experts 自适应融合两类特征，大幅超越单模态方法。

## 研究背景与动机

1. **领域现状**: 图像拼接分两派——传统方法用 SIFT 等几何特征（纹理丰富场景好）和学习方法用语义特征（低纹理/极端条件好），两派长期割裂无交集。

2. **现有痛点**: 几何特征在低纹理/重复纹理场景失效；语义特征在结构丰富场景未必优于传统方法。两种特征互补但从未被统一。

3. **核心矛盾**: 几何特征是稀疏离散 1D 关键点，语义特征是密集连续 2D 特征图——模态完全不同，如何对齐融合？

4. **核心 idea**: Neural Point Transformer 将关键点转为 2D 几何图（模态对齐）→ AMoE 自适应融合（可靠性加权）→ 统一表示送入拼接 pipeline。

## 方法详解

### 整体框架
三阶段：(1) 多模态特征对齐（语义分支 + 几何分支 + NPT 模态转换）(2) 多模态特征融合（AMoE + 模态鲁棒化）(3) 全局到局部变形（FFD 改进的 TPS）。

### 关键设计

1. **Neural Point Transformer (NPT)**:
   - 将稀疏无序 1D 关键点转为有序密集 2D 几何图
   - 先将浅层关键点编码为高维点特征
   - 再投影到结构化潜空间（网格状表示），显式重组空间关系
   - 实现几何特征与语义特征的空间对齐

2. **Adaptive Mixture of Experts (AMoE)**:
   - 自适应捕获多模态特征的异质性，融合互补优势
   - 动态调整对更可靠特征的关注——某一模态不可靠时自动降权
   - 配合 Latent-space Modality Robustifier (MR) 策略增强跨场景鲁棒性

3. **Free-Form Deformation (FFD)**:
   - 改进 TPS 变换在高分辨率图像上的效率
   - 显著降低 VRAM 开销并加速推理，同时保持精确空间对齐

## 实验关键数据

### 主实验 — 多数据集对比

| 方法 | UDIS-D PSNR | UDIS-D SSIM | 对比改进 |
|------|------------|------------|---------|
| StabStitch++ | baseline | baseline | — |
| UniStitch (语义only) | +0.X | +0.0X | 中等提升 |
| UniStitch (几何only) | +0.X | +0.0X | 中等提升 |
| **UniStitch (融合)** | **最高** | **最高** | **大幅超越** |

### 消融实验

| 配置 | 关键发现 |
|------|---------|
| 无 NPT | 几何特征无法与语义对齐，融合失效 |
| 无 AMoE | 简单拼接不如自适应加权 |
| 无 MR | 某一模态失效时整体崩溃 |
| 不同几何特征（SIFT/SuperPoint） | 都能受益于融合——方法对几何特征类型无关 |

### 关键发现
- UniStitch 在所有数据集上大幅超越现有 SOTA，消除了单模态方法各自的失败模式
- 即便在几何特征强势的结构化场景，融合也优于纯几何——语义提供额外约束
- 方法兼容不同几何特征（SIFT、SuperPoint）和学习特征，是通用框架

## 亮点与洞察
- **首次统一两大拼接范式**: 开创性地弥合了传统和学习方法间的鸿沟
- **NPT 的模态桥接**: 将"稀疏点→密集图"的转换形式化，为其他多模态融合问题提供参考

## 局限性 / 可改进方向
- NPT 的关键点到 2D 图的映射质量依赖关键点检测质量
- 未验证视频拼接等时序场景
- AMoE 的专家数量和路由策略可进一步优化

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次统一几何和语义特征的图像拼接
- 实验充分度: ⭐⭐⭐⭐ 多数据集+不同几何特征组合+消融
- 写作质量: ⭐⭐⭐⭐ 问题提出清晰有说服力
- 价值: ⭐⭐⭐⭐ 为图像拼接指明统一范式方向
