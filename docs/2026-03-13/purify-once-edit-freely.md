# Purify Once, Edit Freely: Breaking Image Protections under Model Mismatch

**日期**: 2026-03-13  
**arXiv**: [2603.13028](https://arxiv.org/abs/2603.13028)  
**代码**: 未公开  
**领域**: AI安全 / 图像保护  
**关键词**: adversarial perturbation, image protection, purification attack, model mismatch, diffusion transformer

## 一句话总结
揭示对抗性图像保护方法的严重缺陷——提出 VAE-Trans 和 EditorClean 两种净化器，利用模型架构不匹配和扩散 Transformer 的重建能力，在 6 种保护方法 × 2100 个编辑任务上将 PSNR 提升 3-6 dB、FID 降低 50-70%，证明"净化一次，自由编辑"的攻击模式。

## 研究背景与动机
- 扩散模型使高保真图像编辑成为可能，但也带来未授权风格模仿和有害内容生成风险
- 主动保护方法（PhotoGuard、GLAZE、Mist 等）在图像中嵌入对抗性扰动来干扰编辑
- 但这些保护针对特定代理模型优化——攻击者使用不同模型时保护可能失效

## 方法详解

### 统一净化框架
- 防御者在发布前嵌入扰动 → 攻击者在发布后净化 → 自由编辑

### 两种净化器
1. **VAE-Trans**: 微调 VAE 编码器，通过潜空间投影修正受保护图像
2. **EditorClean**: 用 Diffusion Transformer（架构异构）做指令引导重建 → 利用扰动跨架构迁移性差的特点

### 关键发现
- 保护性扰动跨异构模型迁移性很差——模型不匹配本身就是天然的净化器
- 一旦净化成功，保护信号基本被擦除 → 后续可自由编辑
- 6 种保护方法全部被攻破

## 实验关键数据
- EditorClean vs 未净化: PSNR +3-6 dB, FID -50-70%
- EditorClean vs 现有净化基线: PSNR +~2 dB, FID -30%

## 亮点与洞察
- 揭示了当前图像保护的根本困境——扰动优化在代理模型上，但无法控制下游使用什么模型
- 架构异构性（U-Net vs DiT）提供了天然的净化机会

## 评分
- 新颖性: ⭐⭐⭐⭐ 首次系统评估模型不匹配下的保护存活性
- 实验充分度: ⭐⭐⭐⭐⭐ 6 种保护方法 × 2100 编辑任务，覆盖全面
- 价值: ⭐⭐⭐⭐⭐ 对图像安全社区意义重大——推动更鲁棒的保护设计
