# SemTok: Semantic One-Dimensional Tokenizer for Image Reconstruction and Generation

**日期**: 2026-03-17  
**arXiv**: [2603.16373](https://arxiv.org/abs/2603.16373)  
**领域**: 图像生成  
**关键词**: 1D图像token化, 语义对齐, MMDiT编码器, 自回归生成, 紧凑表示

## 一句话总结
提出 SemTok，用 MMDiT 编码器将 2D 图像压缩为语义对齐的 1D token 序列（~40 tokens/256×256），通过 SigLIP 约束+两阶段训练实现 SOTA 图像重建（5.04 rFID, 1.28 bpp），为 AR 生成提供紧凑输入。

## 研究背景与动机

1. **领域现状**: 图像 tokenizer（VQ-VAE/VQGAN）用 2D grid 结构（16×16=256 tokens），保留空间但存在冗余。

2. **现有痛点**: (a) 2D grid 相邻 patch 高度相关但独立编码——冗余；(b) 只有像素级监督——token 不携带高层语义；(c) AR 生成需规定顺序但 2D 无自然顺序。

3. **核心 idea**: 2D→1D 压缩 + SigLIP 语义约束 + 扩散预训练探索 latent 空间 + 精细化微调恢复纹理。

## 方法详解

### 整体框架
1. **编码器**: MMDiT + Plücker 嵌入 + 可学习查询 token → ~40 个 1D token
2. **量化**: 二进制球面量化器 (BSQ)
3. **解码器**: MMDiT 解码器重建CD图像
4. **语义约束**: 全局 token 用 L2 对齐 SigLIP 嵌入

### 关键设计
1. **Plücker 嵌入**: 6D Plücker 坐标编码 patch 空间位置——比标准位置编码更几何化
2. **SigLIP 语义对齐**: 迫使压缩保留语义而非仅像素
3. **两阶段训练**: 扩散预训练探索语义多样性 + 精细化恢复高频细节

## 实验关键数据

| 方法 | rFID↓ | bpp↓ | tokens |
|------|-------|------|--------|
| **SemTok** | **5.04** | **1.28** | ~40 |
| VQGAN | 5.11 | 1.38 | 256 |

40 token 意味 AR 生成 6.4× 加速。

## 亮点与洞察

- **"2D 是浪费的"**: 256 个 2D token 大量冗余，40 个语义 1D token 就够。
- **语义约束改变编码器学什么**: 无约束时携带局部像素，有约束时携带全局语义。
- **Plücker 嵌入的巧妙复用**: 3D 视觉的坐标编码在 2D tokenizer 中同样有效。

## 局限性
- 仅验证 256×256；码本大小未充分消融

## 相关工作与启发
- **vs TiTok**: 128 token 且无语义约束，SemTok 40 token+语义更紧凑
- 语义约束可推广到其他模态的 tokenizer

## 评分
- 新颖性: ⭐⭐⭐⭐ 语义1D tokenization + Plücker + 两阶段
- 实验充分度: ⭐⭐⭐⭐ ImageNet 重建+生成+消融
- 写作质量: ⭐⭐⭐⭐
- 价值: ⭐⭐⭐⭐ 对 AR 图像生成效率有直接贡献
