# Steering Generative Models for Accessibility: EasyRead Image Generation

**日期**: 2026-03-14  
**arXiv**: [2603.13695](https://arxiv.org/abs/2603.13695)  
**代码**: [EasyRead](https://github.com/easyread-dsl/easyread_project.git)  
**领域**: 图像生成 / 可访问性  
**关键词**: EasyRead, pictogram, accessibility, LoRA fine-tuning, cognitive disability

## 一句话总结
针对智力障碍和低识字率人群的 EasyRead 象形图生成需求，在 OpenMoji/ARASAAC/LDS 混合数据集上用 LoRA rank-16 微调 SD v1.5，提出 EasyRead Score (ERS) 综合评估指标，生成风格统一的简洁象形图（ERS 提升 17.5%，CLIP 相似度 +28%）。

## 研究背景与动机

1. **领域现状**: EasyRead 象形图帮助智力障碍者和低识字人群理解信息，但大规模手工设计成本高。现代扩散模型生成的图像过于复杂，违反 EasyRead 的简洁性和清晰性原则。

2. **核心矛盾**: 通用生成模型优化的是视觉丰富度和真实感，与 EasyRead 要求的简洁、高对比度、低复杂度相矛盾。

3. **核心 idea**: 在精选的象形图数据集上用 LoRA 微调，引导扩散模型生成符合认知可访问性的简洁图像。

## 方法详解

### 数据准备
- OpenMoji (4295 图标) + ARASAAC (11972 象形图) + LDS (927 象形图)
- BLIP 自动生成文本描述
- ARASAAC 系统化增广（背景颜色、肤色、发色）

### 微调与评估
- SD v1.5 + LoRA rank-16，仅微调 UNet 注意力层
- **EasyRead Score (ERS)**: 6 个维度的综合指标 — 调色板复杂度、边缘密度、显著性集中度、对比度、笔画粗细、居中度

## 实验关键数据

| 指标 | SD v1.5 | EasyRead (Ours) | 提升 |
|------|---------|----------------|------|
| ERS | 0.40±0.07 | 0.47±0.06 | +17.5% |
| CLIP Similarity | 24.33 | 31.15 | +28% |

### 关键发现
- 微调后图像更简洁、中心化、高对比度，符合 EasyRead 设计原则
- 与 Global Symbols 和 Nano Banana Pro 等商业方案效果相当
- 不同随机种子下风格一致性良好

## 亮点与洞察
- **EasyRead Score 的设计**是有价值的度量贡献 — 首次将认知可访问性原则量化
- **社会影响导向的 AI 研究** — 用生成式 AI 降低无障碍内容制作成本

## 局限性
- 仅基于 SD v1.5，更新架构（SDXL、Flux）未探索
- ERS 指标的有效性未通过目标用户研究验证
- 生成内容的文化适配性未评估

## 评分
- 新颖性: ⭐⭐⭐ 技术方法标准（LoRA 微调），但应用场景新颖
- 实验充分度: ⭐⭐⭐ 缺少用户研究
- 写作质量: ⭐⭐⭐⭐ 问题动机清晰
- 价值: ⭐⭐⭐⭐ 开创了生成式 AI 辅助无障碍设计的方向
