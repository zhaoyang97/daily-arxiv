# Revisiting the Perception-Distortion Trade-off with Spatial-Semantic Guided Super-Resolution

**日期**: 2026-03-14  
**arXiv**: [2603.14112](https://arxiv.org/abs/2603.14112)  
**代码**: [SpaSemSR](https://hssmac.github.io/SpaSemSR_web/)  
**领域**: 图像生成 / 超分辨率  
**关键词**: super-resolution, perception-distortion trade-off, spatial guidance, semantic guidance, diffusion

## 一句话总结
提出 SpaSemSR，通过空间锚定文本引导（Grounded-SAM 检测目标+坐标编码融入 prompt）和语义增强视觉引导（双分支编码器+VAE/SAM 先验约束），用 Spatial-Semantic ControlNet 自适应融合到 Stable Diffusion 中，在超分任务上同时改善感知质量和保真度，缓解感知-失真 trade-off。

## 研究背景与动机

1. **领域现状**: 图像超分面临感知-失真 trade-off：GAN 方法低失真但纹理模糊；扩散方法纹理逼真但会幻觉和牺牲保真度。

2. **核心矛盾**: 现有方法在感知质量（CLIP-IQA/MUSIQ）和像素保真度（PSNR/SSIM）之间只能取其一。

3. **核心 idea**: 引入两种互补引导——空间锚定的文本引导提供"每个目标在哪"的精确语义，视觉引导提供低层+高层特征先验——共同约束扩散生成。

## 方法详解

### 关键设计

1. **空间锚定文本引导**: Grounded-SAM 检测目标 → 用正弦位置编码将目标坐标融入文本 prompt → SpaTextAtten 层将空间化语义注入 SD

2. **语义增强视觉引导**: 双分支编码器（低层像素特征+高层 SAM 语义特征）→ 预训练 VAE 和 SAM 先验约束 → SemImgAtten 层自适应融合

3. **Spatial-Semantic ControlNet**: 联合两种引导信号，通过专门设计的注意力层注入 Stable Diffusion

## 实验关键数据

| 数据集 | PSNR↑ | SSIM↑ | CLIP-IQA↑ | MUSIQ↑ |
|--------|-------|-------|-----------|--------|
| DIV2K-Val | 21.31 | 0.534 | 0.693 | 63.32 |
| RealSR | 25.74 | 0.731 | 0.589 | 62.96 |

### 关键发现
- 在感知和保真度上都取得比纯 GAN 或纯扩散更好的平衡
- 空间锚定提供的位置信息有效减少了扩散模型的幻觉
- 双分支视觉引导比单一编码器效果更好

## 评分
- 新颖性: ⭐⭐⭐ 空间语义引导的想法有新意，但整体框架偏工程集成
- 实验充分度: ⭐⭐⭐⭐ 多指标多数据集评估
- 价值: ⭐⭐⭐⭐ 缓解感知-失真 trade-off 是超分的核心问题
