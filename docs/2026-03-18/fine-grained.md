# Fine-Grained Post-Training Quantization for LVLMs with Quantization-aware Integrated Gradients

**日期**: 2026-03-18 | **arXiv**: [2603.17809](https://arxiv.org/abs/2603.17809) | **领域**: 多模态/VLM / 模型压缩
**关键词**: 量化, LVLM, token级敏感度, 积分梯度, 3-bit

## 一句话总结
用量化感知积分梯度在 token 级别测量量化敏感度（而非模态级别），在 3-bit 权重量化下提升 LLaVA-onevision-7B 1.60%，与全精度差距仅 1.33%。

## 亮点
- Token 级量化敏感度 > 模态级：不同 token 对量化的敏感度差异很大
- 3-bit 量化仅损失 1.33%——极致压缩

## 评分: 新颖性⭐⭐⭐⭐ | 实验⭐⭐⭐⭐ | 价值⭐⭐⭐⭐

---
