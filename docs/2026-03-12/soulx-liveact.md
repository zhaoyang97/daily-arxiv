# SoulX-LiveAct: Towards Hour-Scale Real-Time Human Animation with Neighbor Forcing and ConvKV Memory

**日期**: 2026-03-12  
**arXiv**: [2603.11746](https://arxiv.org/abs/2603.11746)  
**代码**: 无  
**领域**: 图像生成 / 人物动画  
**关键词**: autoregressive diffusion, neighbor forcing, KV cache compression, real-time, hour-scale video

## 一句话总结
提出 SoulX-LiveAct，通过 Neighbor Forcing（传播同一扩散步的邻近帧 latent 而非跨步状态）解决 AR 扩散的训练-推理分布不匹配问题，配合 ConvKV Memory（1D 卷积压缩 KV cache）实现恒定内存的小时级视频生成，在 2×H100 上以 20 FPS 实时生成 720×416 人物动画。

## 研究背景与动机

1. **领域现状**: 自回归扩散模型（AR Diffusion）结合扩散与因果 AR 生成，支持流式推理，但不同方法在如何沿 AR 链传播时间信息上差异巨大。

2. **现有痛点**: (i) Teacher Forcing 用 ground-truth 条件化但推理时没有 GT；Diffusion Forcing/Self Forcing 传播不同扩散步的状态，导致训练-推理语义不匹配。(ii) KV cache 随帧数线性增长，无法支持小时级生成。

3. **关键发现**: 将因果注意力 mask 直接加到非 AR 扩散模型上时，若参考 latent 选择同一扩散步的前一 chunk（而非不同步的状态），模型可以零样本生成主体一致、时间稳定的视频。

4. **核心 idea**: Neighbor Forcing——沿 AR 链传播同一扩散步的邻近帧 latent，保持分布对齐；ConvKV Memory——用轻量 1D 卷积压缩历史 KV 到固定长度，实现恒定内存推理。

## 方法详解

### 整体框架
基于 DiT + Flow Matching 架构，块式 AR 扩散。分两阶段训练：Stage 1 用 Neighbor Forcing 训练音频/文本对齐；Stage 2 引入 ConvKV Memory + DMD 蒸馏实现 3 步推理。

### 关键设计

1. **Neighbor Forcing（邻近强制）**:
    - 做什么：在 AR 链中传播同一扩散步 $t$ 的前序帧 latent 作为条件
    - 核心思路：$\mathcal{L}(\theta) = \mathbb{E}_{t}[\|(\epsilon - x) - G_\theta(x_t, t, Mask)\|^2]$，所有块在共享扩散步下优化，用块级因果注意力 mask
    - 理论支撑：固定扩散步 $t$ 时，时间邻近帧的 latent 在 latent 流形上几何接近且分布统计对齐（噪声语义一致）
    - 设计动机：避免跨步对齐的困难，直接在单一噪声空间内学习时间依赖，天然支持 KV cache 复用

2. **ConvKV Memory（1D 卷积 KV 压缩）**:
    - 做什么：将历史 KV cache 压缩到固定长度，实现恒定内存的无限长视频生成
    - 核心思路：用 1D 卷积（kernel=stride=$\lambda$=5）将每 5 个 chunk 的 KV 压缩为 1 个，配合 RoPE 位置编码重置：$M_t^{s:e} = (RoPE(Conv_\theta(k_t^{s:e}), frep^s), RoPE(Conv_\theta(v_t^{s:e}), frep^s))$
    - 推理时 KV 分三部分：参考图像状态(2 chunks) + 长期记忆(2 chunks 压缩) + 短期记忆(2 chunks 未压缩)
    - 设计动机：Neighbor Forcing 的步对齐特性使历史 KV 高度可压缩，仅增加 1.9% 推理时间

3. **实时推理优化**:
    - 端到端自适应 FP8 精度 + 序列并行 + 算子融合
    - 每帧仅需 27.2 TFLOPs（512×512 分辨率）
    - 2×H100 实现 20 FPS

### 训练策略
- Stage 1: 300 小时多模态配对数据训练音频交叉注意力
- Stage 2: 400 步 DMD 蒸馏 + ConvKV Memory 联合训练，3 步推理

## 实验关键数据

### 主实验（HDTF 数据集）

| 模型 | Sync-C↑ | Sync-D↓ | FID↓ | FVD↓ | Temporal Quality↑ |
|------|---------|---------|------|------|-------------------|
| OmniAvatar | 5.13 | 10.19 | 27.90 | 268.47 | 86.1 |
| InfiniteTalk | 7.12 | 8.01 | 18.15 | 169.88 | 94.5 |
| Live-Avatar | 7.68 | 8.38 | 15.85 | 206.20 | 91.8 |
| **Ours** | **9.40** | **6.76** | **10.05** | **69.43** | **97.6** |

### 消融实验

| 配置 | 说明 |
|------|------|
| Block size: first=6, rest=8 | 最优块大小配置 |
| 无 ConvKV Memory | KV cache 线性增长，无法支持长视频 |
| 压缩比 λ=5 | 5:1 压缩 KV，仅增加 1.9% 延迟 |

### 关键发现
- Neighbor Forcing 在零样本下即可使非 AR 模型产生时间一致视频，说明关键在于条件表示的选择而非架构
- FVD 指标上（69.43 vs 169.88）大幅领先，说明时间一致性极佳
- 小时级视频生成不退化——ConvKV Memory 有效维持长程记忆

## 亮点与洞察
- **Neighbor Forcing 的洞察极其优雅**：同一扩散步的邻近帧 latent 在噪声空间中自然对齐，无需复杂的跨步对齐策略。从一个实验观察出发，推导出理论原因，再设计完整系统
- **ConvKV Memory 的简洁性**：仅用 1D 卷积 + RoPE 重置就实现了恒定内存推理，增加 1.9% 延迟，设计极其轻量
- **工程化到位**：FP8 + 序列并行 + 算子融合，2×H100 实现 20 FPS 实时推理

## 局限性 / 可改进方向
- 仅在人物动画（talking head / 全身动作）场景验证，通用视频生成能力未探索
- 压缩比 λ=5 是固定的，自适应压缩可能进一步优化
- 依赖 WAN 2.1 预训练权重，新场景需要重新微调

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ Neighbor Forcing 概念新颖且有理论支撑
- 实验充分度: ⭐⭐⭐⭐ 多数据集 + 消融 + 实时性能验证
- 写作质量: ⭐⭐⭐⭐ 对比表格清晰，方法动机明确
- 价值: ⭐⭐⭐⭐⭐ 对实时长视频生成有重要参考价值
