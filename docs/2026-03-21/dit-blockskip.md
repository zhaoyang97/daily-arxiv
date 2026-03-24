# Memory-Efficient Fine-Tuning Diffusion Transformers via Dynamic Patch Sampling and Block Skipping

**日期**: 2026-03-21
**arXiv**: [2603.20755](https://arxiv.org/abs/2603.20755)
**代码**: 无（Qualcomm AI Research）
**领域**: 图像生成 / 扩散模型 / 高效微调
**关键词**: DiT-BlockSkip, FLUX, SANA, Dynamic Patch Sampling, Block Skipping, Residual Feature, LoRA, Personalization

## 一句话总结

提出 DiT-BlockSkip：(1) 时间步感知的动态 patch 采样——高时间步大 patch 学全局结构、低时间步小 patch 学细节，统一 resize 到低分辨率；(2) 基于 cross-attention masking 识别关键 block 后跳过非关键 block 并预计算残差特征。在 FLUX/SANA 上，30% 跳过率+256 分辨率训练即可达到 LoRA@512 水平（DINO 0.7194 vs 0.7324），内存减少约 71%。

## 研究背景与动机

1. **领域现状**: DiT 架构（如 FLUX、SANA）已成为 T2I 生成的主流，支持高质量个性化内容创作。LoRA 等 PEFT 方法减少了可训练参数，但仍需完整反向传播，内存开销大。
2. **现有痛点**: FLUX 的 LoRA 微调需要 22.84 GiB 参数内存；PEFT 方法虽减少参数，但 base model 参数 + 激活值内存不减；量化方法会牺牲精度；零阶优化（ZOODiP）不稳定且需 30000 步收敛。
3. **核心矛盾**: DiT 模型越深越大，个性化微调的内存需求势不可挡，但实际部署场景（手机、IoT 设备）资源极度受限。现有高效微调技术大多针对 U-Net，DiT 架构尚待探索。
4. **本文要解决什么**: 在不修改模型架构或去噪目标的前提下，大幅降低 DiT 个性化微调的训练内存消耗，同时保持个性化质量。
5. **切入角度**: 两个正交维度同时压缩——(1) 空间维度：降低训练分辨率但通过动态 patch 保留信息；(2) 深度维度：跳过非关键 block 但通过预计算残差特征弥补。
6. **核心 idea 一句话**: 高时间步用大 patch 学结构、低时间步用小 patch 学细节（动态 patch 采样），加上跳过首末 block + 预计算残差特征（block skipping），两者结合实现 DiT 微调内存减少 71%。

## 方法详解

### 整体框架

DiT-BlockSkip 由两个正交组件组成：(1) Dynamic Patch Sampling 在输入空间降低内存；(2) Block Skipping with Residual Feature 在模型深度上降低内存。两者结合应用于 LoRA 微调管线。训练流程为：预计算 skipped blocks 的残差特征 → 在低分辨率 patch 上仅微调 unskipped blocks 的 LoRA 权重。

### 关键设计

**设计一：时间步感知的动态 Patch 采样**

- **做什么**: 根据当前扩散时间步 $t$ 动态调整 crop 尺寸：$f(s_{\min}, s_{\max}, t) = s_{\min} + \frac{t}{T}(s_{\max} - s_{\min})$。高时间步 → 大 patch（全局结构），低时间步 → 小 patch（局部细节）。所有 patch 统一 resize 到 $s_{\min} \times s_{\min}$（如 256×256）。
- **核心思路**: 扩散模型的时间步特性——高时间步对应高噪声（学全局结构），低时间步对应低噪声（学精细细节），动态 patch 尺寸与此特性对齐。
- **设计动机**: 简单 resize 到低分辨率会丢失细节（DINO 0.7164），而动态 patch 采样在同样 256 分辨率下保留了更多信息（DINO 0.7253）。patch 尺寸按 VAE encoder 的下采样因子（如 16）离散化。

**设计二：基于 Cross-Attention Masking 的 Block 选择**

- **做什么**: 先用 LoRA 微调整个 DiT，然后在推理时对连续 14 个 block 施加 cross-attention masking（image query → text key），观察哪些 block 被 mask 后主体消失。
- **核心思路**: 发现中层 block 对个性化至关重要——mask 首/末 block 几乎无影响，但 mask 中层 block 会导致目标主体完全消失。
- **设计动机**: DiT 不像 U-Net 有天然的层次结构（空间下采样），每个 block 的功能不直观。cross-attention masking 提供了一种无需额外训练的 block 重要性度量方法。最终策略：跳过前 $n^*$ 和后 $m^*$ 个 block，保留中间层，通过 $(n^*, m^*) = \arg\min_{n+m=k} \sum_j [D(x_g^{(j)}, \hat{x}_n^{(j)}) + D(x_g^{(j)}, \tilde{x}_m^{(j)})]$ 优化。

**设计三：残差特征预计算**

- **做什么**: 对跳过的 block 预先计算残差特征 $\Delta f_{i,i+l} = f_{i+l} - f_{i}$（即 block 组的输入输出之差）。微调时直接将残差加到 unskipped block 的输出上：$f'_{i+l} = f'_i + \Delta f_{i,i+l}$。
- **核心思路**: 朴素跳过会导致训练/推理前向路径不匹配，残差特征弥补了 skip 带来的特征漂移。
- **设计动机**: 消融实验表明，不加残差特征时 30% 跳过 DINO 仅 0.4313（崩溃），加上后恢复到 0.7282（接近 LoRA 的 0.7324）。预计算开销相对可控（推理通常 20-50 步）。

### 损失函数 / 训练策略

- **训练损失**: Conditional flow matching loss（FLUX/SANA 原生目标），未修改去噪目标。
- **LoRA 注入**: 仅在 unskipped blocks 中注入 LoRA，跳过的 block 参数从 GPU offload。
- **内存节省来源**: (1) base model 参数减少（offload skipped blocks）；(2) 前向/反向内存减少（低分辨率 + 更少 block）；(3) 优化器状态减少（只更新 unskipped blocks 的 LoRA）。
- 训练数据：DreamBooth 数据集 30 个主体，每主体 4-6 张图。每主体 25 个 class-specific 提示词。

## 实验关键数据

### 主实验

**FLUX 模型对比:**

| 方法 | Skip Ratio | 训练分辨率 | DINO↑ | CLIP-I↑ | CLIP-T↑ |
|------|-----------|-----------|-------|---------|---------|
| TI | – | 512 | 0.3384 | 0.6140 | 0.2005 |
| DreamBooth | – | 512 | 0.7131 | 0.8122 | 0.3073 |
| LoRA | – | 512 | 0.7324 | 0.8146 | 0.3173 |
| LISA | – | 512 | 0.7387 | 0.8194 | 0.3177 |
| HollowedNet | 30% | 512 | 0.4899 | 0.7031 | 0.3094 |
| **Ours** | **30%** | **256** | **0.7194** | **0.8036** | **0.3199** |
| Ours | 40% | 256 | 0.7171 | 0.8034 | 0.3194 |
| Ours | 50% | 256 | 0.6963 | 0.7877 | 0.3184 |

### 消融实验

**Dynamic Patch Sampling 消融 (FLUX):**

| 方法 | 分辨率 | DINO↑ | CLIP-I↑ |
|------|--------|-------|---------|
| LoRA (baseline) | 512 | 0.7324 | 0.8146 |
| + Simple Resize | 256 | 0.7164 | 0.8044 |
| **+ Dynamic Patch Sampling** | 256 | **0.7253** | **0.8099** |

**Block Skipping ± Residual Feature 消融:**

| 方法 | Skip 30% DINO | Skip 40% DINO | Skip 50% DINO |
|------|--------------|--------------|--------------|
| Block Skip (无残差) | 0.4313 | 0.4338 | 0.4301 |
| Block Skip + Residual | 0.7282 | 0.7303 | 0.7150 |

**Skip 位置消融 (50%):**

| 策略 | DINO↑ | CLIP-I↑ |
|------|-------|---------|
| 跳前 50% blocks | 0.6651 | 0.7646 |
| 跳后 50% blocks | 0.4808 | 0.7111 |
| **Ours (首末跳过)** | **0.7150** | **0.8035** |

### 关键发现

1. **动态 Patch 采样显著优于简单 resize**: 0.7253 vs 0.7164 (DINO)，仅改变采样策略不改模型就能在低分辨率下保留细节。
2. **残差特征预计算是"生死线"**: 无残差时 skip 30% DINO 仅 0.43（完全崩溃），加残差后恢复到 0.73。
3. **中层 block 对个性化至关重要**: 跳后 50% block 导致 DINO 仅 0.48，跳前 50% 为 0.67，首末均跳（保留中间）为 0.72。
4. **30% skip 几乎无损**: DINO 0.7194 vs LoRA@512 的 0.7324，差距仅 1.8%，但内存节省约 42%。
5. 用户研究显示文本忠实度上 Ours 甚至优于 LoRA (45.6% vs 29.4% 偏好)。
6. HollowedNet 在 DiT 上表现很差（DINO 0.49），证明 U-Net 的 block 跳过策略不能直接迁移到 DiT。

## 亮点与洞察

- **两个正交维度的组合**: 空间（patch sampling）+ 深度（block skipping）独立有效且可叠加，是一种优雅的框架设计。
- **Cross-attention masking 揭示 DiT 结构**: 发现 DiT 的中层 block 对个性化最关键，与 U-Net 的浅层低频/深层高频的层次结构截然不同。这一发现对 DiT 的可解释性研究有启发。
- **残差特征预计算解决 train-inference mismatch**: 简单有效，通过弥补 skip 带来的特征漂移，使重度 skip（50%）仍可工作。
- **实用导向**: 来自 Qualcomm AI Research，目标明确是 on-device 部署（手机、IoT）。

## 局限性 / 可改进方向

1. 残差特征是用原始（非 LoRA）权重预计算的，与微调后的特征不完全匹配——随着微调更深入可能出现偏移。
2. 仅在 DreamBooth 个性化场景验证，缺少 style transfer、concept composition 等更复杂个性化任务。
3. 推理阶段不涉及 skip（仅训练时），推理时仍需完整模型——对部署的好处仅在微调阶段。
4. Block 选择策略依赖预先用 LoRA 微调 30 个主体的代理搜索，有一定一次性计算开销。
5. 可探索自适应 skip ratio（根据主体复杂度动态调整），而非固定比例。

## 相关工作与启发

- **vs LoRA (baseline)**: DiT-BlockSkip 以 LoRA 为 upper bound，30% skip@256 实现 98.2% 的 DINO 保留率，同时大幅降低内存。
- **vs HollowedNet (U-Net skip)**: HollowedNet 在 FLUX 上 DINO 仅 0.49，证明 U-Net 的经验性 block skip 不能迁移到 DiT。DiT-BlockSkip 的 cross-attention 引导选择策略是关键改进。
- **vs ZOODiP (零阶优化)**: ZOODiP 需 30000 步且不稳定，TI 在 DiT 上也效果差，说明梯度 free 方法不适合 DiT 微调。
- **vs LISA/LoRA-FA**: 这些 LLM 高效微调方法在大模型（FLUX）上有效但在轻量模型（SANA）上退化，适用性不如 DiT-BlockSkip。

## 评分

| 维度 | 分数 (1-5) | 说明 |
|------|-----------|------|
| 新颖性 | 4.0 | 时间步感知 patch 采样 + cross-attention 引导 block skip 组合新颖 |
| 实验充分度 | 4.0 | 两个 base model、多种基线、详细消融、用户研究，实验扎实 |
| 写作质量 | 4.0 | 来自 Qualcomm + KAIST，论文结构清晰，图表丰富 |
| 价值 | 4.0 | 对 DiT 个性化微调的实际部署有直接推动作用 |

