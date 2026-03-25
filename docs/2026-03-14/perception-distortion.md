# Revisiting the Perception-Distortion Trade-off with Spatial-Semantic Guided Super-Resolution

**日期**: 2026-03-14  
**arXiv**: [2603.14112](https://arxiv.org/abs/2603.14112)  
**代码**: [SpaSemSR](https://hssmac.github.io/SpaSemSR_web/)  
**领域**: 图像生成 / 超分辨率  
**关键词**: super-resolution, perception-distortion trade-off, spatial guidance, semantic guidance, diffusion

## 一句话总结
提出 SpaSemSR 空间-语义引导扩散超分框架，通过空间锚定文本引导和语义增强视觉引导双路互补，在 DIV2K-Val 上 PSNR 21.31 超越全部扩散方法（StableSR 20.74），CLIP-IQA 0.693 大幅超越 GAN 方法（Real-ESRGAN 0.549），并在真实数据 RealSR/DRealSR 上全面领先，消融证实空间引导提升 PSNR +1.84，语义引导提升 CLIP-IQA +4.09%。

## 研究背景与动机
1. **感知-失真 trade-off**: Blau & Michaeli 2018 形式化证明了 SR 根本矛盾——提升保真度（PSNR/SSIM）必然牺牲感知质量（CLIP-IQA/MUSIQ），反之亦然
2. **GAN 方法局限**: Real-ESRGAN、BSRGAN 等 PSNR/SSIM 较好（DIV2K PSNR 21.86），但纹理过于平滑，CLIP-IQA 仅 0.549，感知质量差
3. **扩散方法局限**: DiffBIR、XPSR 等纹理逼真（XPSR CLIP-IQA 0.783），但频繁产生幻觉结构，PSNR 仅 20.56，保真度严重下降
4. **本文切入**: 引入两种互补引导——空间锚定文本引导提供"目标在哪里"的精确语义约束保真度，语义增强视觉引导提供低层结构+高层语义先验提升感知质量

## 方法详解

### 整体框架
基于 Stable Diffusion v2 + ControlNet 架构。两种引导通过 SpaTextAtten 和 SemImgAtten 注意力层注入扩散去噪过程。训练 200K 迭代，batch 32，lr 5e-5，512×512，4×RTX 6000 GPU 训练 3 天。

训练数据涵盖 DIV2K、DIV8K、Flickr2K、OutdoorSceneTraining、Unsplash2K 和 5K FFHQ 人脸，使用 Real-ESRGAN 退化管线合成 LR-HR 训练对。推理阶段 LR 先经退化移除模块（DRM）恢复清晰图，再由 Grounded-SAM 提取 bbox/标签，确保训练-推理一致性。

### 关键设计
1. **空间锚定文本引导**: Grounded-SAM 检测目标得到文本标签和 bbox 坐标，正弦位置编码将坐标编码后与 CLIP 文本嵌入逐目标融合，生成空间锚定文本表示 $\mathbf{e}_{\text{spa-text}}$。同时用 LLaVA 生成退化感知文本（描述模糊/噪声/压缩等退化类型），两类文本联合输入 ControlNet 和扩散模型
2. **语义增强视觉引导**: 双分支编码器——$\mathcal{E}_{\text{img}}$ 捕获 latent 结构 + $\mathcal{E}_{\text{sem}}$ 提取 SAM 语义。语义退化损失以预训练 VAE/SAM 在 HR 上的特征为监督目标，确保编码器在退化 LR 输入下仍能提取有意义的低层结构和高层语义
3. **Spatial-Semantic ControlNet**: SpaAtten（空间文本×视觉特征）和 DegAtten（退化文本×视觉特征）双路并行提取，再由 SpaSemAtten 融合两路输出，自适应平衡空间精度与语义一致性后注入扩散去噪

## 实验关键数据

### 主实验（DIV2K-Val ×4 SR，合成退化）
| 方法 | 类型 | PSNR↑ | SSIM↑ | CLIP-IQA↑ | MUSIQ↑ | MANIQA↑ |
|------|------|-------|-------|-----------|--------|---------|
| Real-ESRGAN | GAN | 21.86 | 0.575 | 0.549 | 58.80 | 0.378 |
| BSRGAN | GAN | 21.74 | 0.553 | 0.523 | 59.16 | 0.353 |
| StableSR | Diff | 20.74 | 0.489 | 0.661 | 63.19 | 0.400 |
| XPSR | Diff | 20.56 | 0.508 | 0.783 | 70.07 | 0.611 |
| DiffBIR | Diff | 20.57 | 0.474 | 0.736 | 69.93 | 0.576 |
| SeeSR | Diff | 21.00 | 0.536 | 0.707 | 68.81 | 0.515 |
| **SpaSemSR** | **Diff** | **21.31** | **0.534** | **0.693** | **63.32** | **0.495** |

### 真实数据（RealSR ×4 SR）
| 方法 | 类型 | PSNR↑ | SSIM↑ | CLIP-IQA↑ | MUSIQ↑ | MANIQA↑ |
|------|------|-------|-------|-----------|--------|---------|
| Real-ESRGAN | GAN | 25.69 | 0.761 | 0.449 | 60.37 | 0.373 |
| StableSR | Diff | 24.70 | 0.709 | 0.617 | 65.18 | 0.418 |
| XPSR | Diff | 23.74 | 0.673 | 0.742 | 71.45 | 0.629 |
| SeeSR | Diff | 25.15 | 0.721 | 0.670 | 69.82 | 0.540 |
| **SpaSemSR** | **Diff** | **25.74** | **0.731** | **0.589** | **62.96** | **0.464** |

### 消融实验（RealSR + DIV2K-Val）
| 变体 | RealSR PSNR↑ | RealSR SSIM↑ | DIV2K CLIP-IQA↑ | DIV2K MUSIQ↑ |
|------|-------------|-------------|-----------------|-------------|
| w/o spatial（无空间引导） | 23.90 | 0.690 | 0.693 | 63.32 |
| w/o semantic（无语义编码器） | 25.74 | 0.731 | 0.652 | 61.88 |
| w/o VAE（无 VAE 约束） | 25.74 | 0.731 | 0.661 | 62.14 |
| **Full SpaSemSR** | **25.74** | **0.731** | **0.693** | **63.32** |

### 关键发现
- RealSR 真实数据：PSNR 25.74 超越全部扩散方法（StableSR 24.70、XPSR 23.74）和 GAN 方法（Real-ESRGAN 25.69）
- DRealSR 真实数据：PSNR 28.97 全面领先（StableSR 28.07、BSRGAN 28.70、Real-ESRGAN 28.61）
- 空间引导是保真度关键：移除后 RealSR PSNR 暴跌 1.84（25.74→23.90），DIV2K PSNR 降 0.61（21.31→20.70）
- 语义引导是感知质量关键：DIV2K CLIP-IQA +4.09%（0.652→0.693），MANIQA +0.043（0.452→0.495）
- DRealSR 上空间引导效果同样显著：PSNR 从 26.72 跃升至 28.97（+2.25），SSIM 从 0.741 升至 0.783
- 感知指标对比 GAN：DIV2K CLIP-IQA 超 Real-ESRGAN 26.4%（0.693 vs 0.549），MANIQA 超 31.0%（0.495 vs 0.378）

## 亮点与洞察
- 首次将空间锚定（Grounded-SAM bbox + 正弦位置编码）引入文本引导超分，比 SeeSR/PASD 的全局 prompt 更精准对齐语义与区域
- 消融清晰展示了双引导互补性：空间管保真度、语义管感知质量，各自提升的指标维度几乎正交
- 推理时用 DRM 先恢复清晰图再提取 bbox 的设计巧妙解决了退化 LR 输入导致检测器失效的问题

## 局限性 / 可改进方向
- DIV2K PSNR 仍略低于 GAN 方法（21.31 vs Real-ESRGAN 21.86），扩散范式在保真度上仍有天花板
- CLIP-IQA 不如 XPSR（0.693 vs 0.783），说明保真度约束确实牺牲了部分极端感知质量
- 推理依赖 Grounded-SAM + LLaVA + DRM 等多个外部模型，pipeline 复杂度和延迟较高
- 未提供推理时间对比，多步扩散+多模型推理在实际部署中可能受限

## 相关工作与启发
- **vs XPSR**: XPSR CLIP-IQA 最强（0.783）但 PSNR 最低（20.56），SpaSemSR 选择了更均衡的 Pareto 点
- **vs FaithDiff**: 同样关注扩散保真度，但 FaithDiff PSNR 仅 20.63，缺乏空间锚定机制
- **vs SeeSR**: 同为语义引导扩散超分，但 SeeSR 用全局 prompt，SpaSemSR 的空间锚定使 PSNR 提升 0.31（DIV2K）、0.59（RealSR）

## 评分
- 新颖性: ⭐⭐⭐⭐ 空间锚定文本引导是新颖设计，首次将目标检测坐标编码注入超分
- 实验充分度: ⭐⭐⭐⭐⭐ 3 合成 + 2 真实数据集 × 5 指标 × 9 对比方法 + 完整消融
- 写作质量: ⭐⭐⭐⭐ trade-off 分析清晰，公式推导完整
- 价值: ⭐⭐⭐⭐ 为扩散超分提供了实用的保真度提升方案，新 Pareto 前沿点
