# CycleCap: Improving VLMs Captioning Performance via Self-Supervised Cycle Consistency Fine-Tuning

**日期**: 2026-03-20  
**arXiv**: [2603.18282](https://arxiv.org/abs/2603.18282)  
**代码**: 无  
**领域**: 多模态VLM  
**关键词**: image captioning, cycle consistency, GRPO, self-supervised, DreamSim

## 一句话总结
提出 CycleCap，用循环一致性作为自监督奖励（图像→Caption→重建图像，DreamSim 衡量一致性）配合 GRPO 微调 VLM captioning 能力，无需标注数据，在 CompreCap/CAPability/CapsBench 上稳定提升 1.3-3.2 分，且减少幻觉。

## 研究背景与动机

1. **领域现状**: VLM 在 image captioning 上仍存在描述过于笼统或产生幻觉的问题。现有改进方案要么需要昂贵的偏好标注数据（DPO-style），要么依赖 GPT-4 迭代精修（RICO）。

2. **现有痛点**: (a) 偏好数据标注成本高且难以规模化；(b) 测试时精修方法需要外部 API 调用，推理成本高；(c) 图像-文本对齐仍是根本挑战——模型倾向生成"安全但无信息"的描述。

3. **核心 idea**: 好的 caption 应该能唯一地"重建"原始图像——如果 text-to-image 模型从 caption 生成的图像与原图相似，说明 caption 准确、详细、无幻觉。用此循环一致性作为免标注的奖励信号。

## 方法详解

### 关键设计

1. **循环一致性奖励**:
   - Image → VLM → Caption → Frozen T2I model (SD3/FLUX.1-dev) → Reconstructed Image
   - 奖励 = DreamSim(原图, 重建图)——DreamSim 比 LPIPS 和 CLIP 更好平衡感知和语义
   - T2I 模型全程冻结，只更新 VLM 参数

2. **GRPO 微调**:
   - 每张图采样 n=8 个候选 caption
   - 计算组内相对优势（advantage）
   - 裁剪策略梯度 + KL 正则化
   - 训练数据：83K COCO 图像，1 epoch，LoRA rank 64

## 实验关键数据

### CompreCap (统一分数 0-100)

| 模型 | Base | +CycleCap | 提升 |
|------|------|-----------|------|
| InternVL3-1B | 60.24 | 62.49 | +2.25 |
| Qwen2-VL-2B | 59.35 | 62.09 | +2.74 |
| Qwen2.5-VL-3B | 59.21 | 62.42 | +3.21 |
| Qwen2-VL-7B | 61.73 | 63.06 | +1.33 |

### CAPability (0-100)

| 配置 | Qwen2-VL-7B |
|------|-------------|
| Base | 70.47 |
| +CycleCap (SD3) | 72.95 (+2.48) |
| +CycleCap (FLUX.1-dev) | **73.73 (+3.26)** |
| RICO-Flash | 62.93 |

### 幻觉减少 (MMHal, 0-6)
Qwen2-VL-7B: 3.85 → 4.02 (+0.17)

### 消融（奖励指标对比）
- **DreamSim**: 最佳整体表现（平衡感知+语义）
- LPIPS: 主要帮助 CompreCap，其他不稳定
- CLIP similarity: 弱，主要帮助幻觉鲁棒性

### 关键发现
- 更强的 T2I 模型带来更高提升：FLUX.1-dev > SD3
- 跨规模一致有效：1B-7B 参数模型都受益
- 可与监督方法叠加：CycleCap on RICO-Flash 达到 77.72 CapsBench

## 亮点与洞察
- **循环一致性**作为自监督信号的直觉极其自然：好 caption = 能重建原图——无需人工标注，理论上无限可扩展
- **免 API 调用**是重要工程优势：vs RICO 的迭代 GPT-4 精修，CycleCap 完全本地化
- DreamSim 作为奖励指标的选择有讲究——纯感知（LPIPS）或纯语义（CLIP）都不够好

## 局限性 / 可改进方向
- T2I 生成本身引入噪声——如果 T2I 模型对某些 caption 理解有偏差，奖励信号会不准
- GRPO 采样 8 个候选 × T2I 生成 → 训练成本仍不低
- 奖励信号质量受限于 T2I 模型能力——未来更强的 T2I 可进一步释放潜力

## 评分
- 新颖性: ⭐⭐⭐⭐ 循环一致性用于 captioning 训练的思路优雅
- 实验充分度: ⭐⭐⭐⭐ 多模型/多 benchmark/多奖励指标消融
- 价值: ⭐⭐⭐⭐ 免标注的 captioning 提升方案，实用且可扩展
