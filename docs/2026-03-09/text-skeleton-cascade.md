# Controllable Complex Human Motion Video Generation via Text-to-Skeleton Cascades

**日期**: 2026-03-09  
**arXiv**: [2603.08028](https://arxiv.org/abs/2603.08028)  
**代码**: 无（有 Project Page）  
**领域**: 图像生成  
**关键词**: human motion video, text-to-skeleton, pose-conditioned generation, DINO-ALF, autoregressive

## 一句话总结
提出两阶段级联框架生成复杂人体动作视频：第一阶段用自回归 Transformer 从文本生成 2D 骨架序列，第二阶段用 DINO-ALF（多层自适应融合）外观编码器驱动 pose-conditioned 视频扩散模型，在翻跟头、武术等复杂动作上显著优于现有方法。

## 研究背景与动机

1. **领域现状**: 文本到视频（T2V/TI2V）扩散模型在常规动作上效果不错，但对翻跟头、侧空翻、武术等**复杂非重复动作**仍然困难——产生不合理肢体轨迹、身体形状时间不一致、外观漂移。

2. **现有痛点**: (a) 纯文本条件时间上模糊——"做一个后空翻"无法指定逐帧关节轨迹；(b) Pose-conditioned 方法虽有效但需要用户提供完整骨架序列，对复杂动作来说获取成本极高；(c) 现有方法用 CLIP 编码参考图像，但 CLIP 是全局语义表示，缺少细粒度空间细节，在大变形/自遮挡下外观保持差。

3. **核心矛盾**: 文本控制不够精确 vs 精确的 pose 控制难以获取；CLIP 全局表示 vs 需要局部外观保持。

4. **切入角度**: 将问题解耦为运动规划（文本→骨架）和外观合成（骨架+参考图→视频），用自回归模型自动生成骨架，用 DINO 多层特征替代 CLIP 保持外观。

## 方法详解

### 整体框架
文本描述 → **Stage 1**: 自回归 Transformer 生成 2D 骨架序列（逐关节、逐帧token预测）→ **Stage 2**: 骨架序列 + 参考图像 → DINO-ALF 外观编码 + Pose encoder → DiT 视频扩散模型 → 输出视频。

### 关键设计

1. **自回归 Text-to-Skeleton 模型**:
    - 做什么：从文本描述生成 $T$ 帧 $J$ 个关节的 2D 骨架坐标序列
    - 核心思路：将连续坐标离散化为 $K$ 个 bin 的 token，按 frame-major, joint-minor 顺序串行化为 1D token 流 $\mathbf{z} = [s(x_{1,1}), s(y_{1,1}), \ldots]$，用 CLIP 文本编码器产生的 embedding 作为前缀，decoder-only Transformer 做 next-token 预测
    - 设计动机：自回归分解天然建模了复杂动作中的长程时间依赖和关节间协调性——每个关节的位置取决于之前所有帧和所有关节的配置

2. **DINO-ALF（Adaptive Layer Fusion）外观编码器**:
    - 做什么：从参考图像提取空间局部化的多层外观特征，注入视频扩散模型
    - 核心思路：提取 DINOv3 所有 12 层的 patch token，用可学习的层权重 $\alpha^{(\ell)}$（softmax 归一化）自适应融合 $\mathbf{a} = \sum_\ell \alpha^{(\ell)} \text{proj}(\mathbf{p}^{(\ell)})$，每层投影到统一维度再线性组合
    - 设计动机：DINO 浅层捕捉纹理细节，深层捕捉视角不变的语义，自适应融合让模型在大变形下同时利用局部纹理和全局语义

3. **Spatiotemporal Motion Encoder**:
    - 做什么：将渲染的骨架图像序列编码为时空对齐的 motion token
    - 核心思路：3D CNN 对渲染的 pose 图像序列做时空编码，输出与 latent 空间对齐的 context token
    - 设计动机：比直接用坐标更适合与 DiT 架构融合，保持空间对齐

4. **合成数据集**:
    - 用 Blender 构建 2000 个复杂人体动作视频（翻跟头、体操等），完全控制外观/动作/环境
    - 填补了现有 benchmark 缺少杂技类动作的空白，同时避免版权和隐私问题

### 训练策略
- Stage 1 用 teacher forcing + next-token cross-entropy 训练
- Stage 2 冻结 Wan2.1 DiT 主干，只训练 DINO-ALF cross-attention + LoRA adapters + motion encoder
- 训练时对 GT 骨架施加 stochastic augmentation（关节抖动/dropout/时间偏移）模拟预测误差，增强鲁棒性

## 实验关键数据

### 主实验 — Text-to-Skeleton (Motion-X Fitness)

| 方法 | FID ↓ | R-Precision Top-1 ↑ | Diversity ↑ |
|------|-------|----------------------|-------------|
| MDM | 42.3 | 0.312 | 5.81 |
| HumanDreamer | 38.7 | 0.345 | 6.12 |
| **Ours** | **31.5** | **0.401** | **6.58** |

### 主实验 — Pose-to-Video (VBench Metrics)

| 方法 | Temporal Consistency ↑ | Motion Smoothness ↑ | Subject Preservation ↑ |
|------|----------------------|--------------------|-----------------------|
| MagicAnimate | 0.891 | 0.923 | 0.847 |
| Animate-Anyone2 | 0.912 | 0.941 | 0.873 |
| **Ours (DINO-ALF)** | **0.937** | **0.958** | **0.912** |

### 消融实验

| 配置 | Subject Preservation | Motion Smoothness |
|------|---------------------|------------------|
| Full (DINO-ALF) | **0.912** | **0.958** |
| CLIP 替代 DINO-ALF | 0.865 | 0.943 |
| 单层 DINO（最后层） | 0.889 | 0.951 |
| w/o skeleton augmentation | 0.903 | 0.946 |

### 关键发现
- DINO-ALF 相比 CLIP 在 Subject Preservation 上提升显著（+4.7%），验证了细粒度局部特征的重要性
- 多层融合比单层好（+2.3%），浅层纹理细节不可缺少
- 骨架 augmentation 有效缓解了两阶段误差传播
- 在复杂动作（翻跟头、武术）上的优势比简单舞蹈更加明显

## 亮点与洞察
- **两阶段解耦设计**: 运动规划和外观合成分开处理，每个阶段可独立优化和替换，实用性强
- **DINO-ALF 的多层自适应融合**: 简洁优雅——可学习的层权重让模型自动决定不同层级特征的重要性，比复杂的 ReferenceNet 更轻量
- **合成数据填补空白**: 用 Blender 程序化生成杂技动作视频，避开了真实数据难以收集复杂动作的困境
- **骨架 augmentation 缓解级联误差**: 训练时模拟第一阶段的各类错误，让第二阶段更鲁棒

## 局限性 / 可改进方向
- 骨架只有 2D，缺少深度信息，对视角变化大的场景可能不够
- 第一阶段骨架质量直接影响最终视频——误差级联仍是瓶颈
- 合成数据集仅 2000 个视频，多样性有限
- 目前仅支持单人场景，多人交互未涉及

## 相关工作与启发
- **vs HumanDreamer**: 同为 text→skeleton→video 级联，但本文的自回归分解更自然地建模长程依赖
- **vs MagicAnimate/Champ**: 这些方法用 ReferenceNet 或 SMPL 做外观保持，重但精确；DINO-ALF 更轻量
- **vs CLIP-based conditioning**: CLIP 全局语义好但局部细节差，DINO patch 特征在大变形下优势明显

## 评分
- 新颖性: ⭐⭐⭐⭐ 两阶段级联框架合理，DINO-ALF 是实用创新
- 实验充分度: ⭐⭐⭐⭐ 合成数据集+Motion-X+VBench，多维度评估
- 写作质量: ⭐⭐⭐⭐ 问题分析清晰，方法详尽
- 价值: ⭐⭐⭐⭐ 复杂动作视频生成的实用方案
