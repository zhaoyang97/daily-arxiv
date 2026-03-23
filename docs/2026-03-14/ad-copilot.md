# AD-Copilot: A Vision-Language Assistant for Industrial Anomaly Detection via Visual In-context Comparison

**日期**: 2026-03-14  
**arXiv**: [2603.13779](https://arxiv.org/abs/2603.13779)  
**代码**: [AD-Copilot](https://github.com/jam-cc/AD-Copilot) (即将开源)  
**领域**: 多模态VLM / 工业异常检测  
**关键词**: anomaly detection, MLLM, visual comparison, industrial inspection, cross-attention

## 一句话总结
提出 AD-Copilot，通过 Comparison Encoder（跨注意力提取图像对差异tokens）+ Chat-AD 大规模工业多模态数据集（62万样本）+ 四阶段渐进训练策略，使 7B MLLM 在工业异常检测 benchmark MMAD 上达到 82.3% 准确率，超越所有现有模型（含 GPT-4o）并接近人类专家水平。

## 研究背景与动机

1. **领域现状**: MLLM（如 Qwen2.5-VL、InternVL）在通用视觉理解上表现优秀，但在工业异常检测 (IAD) 上表现很差。现有 IAD 专用模型（AnomalyGPT 等）只是将 MVTec-AD 标注转成简单 VQA 对做微调，数据覆盖窄、语言多样性差。

2. **现有痛点**: (a) **缺乏大规模高质量工业多模态训练数据** — 工业图像与自然图像差异大（重复纹理、严格几何、细微缺陷），通用网络数据训练的 MLLM 缺少工业领域知识。(b) **MLLM 缺乏视觉级别的比较能力** — 现有模型独立编码每张图像，只能在语言空间做语义级比较，无法感知像素级细微差异（如微小划痕、颜色偏移）。

3. **核心矛盾**: 工业质检的本质是"与正常模板对比发现偏差"，但 MLLM 的独立编码架构天然不支持图像对的细粒度视觉比较。实验证实，给现有 MLLM 提供模板图像几乎不带来性能提升。

4. **切入角度**: 设计专门的视觉比较模块，在特征编码阶段就进行跨图像交互，而非等到语言推理阶段才比较。同时构建大规模对比式工业数据集（每个样本都配对正常模板）。

5. **核心 idea**: 用 Comparison Encoder 在视觉编码阶段做跨注意力提取图像对差异 tokens，配合大规模对比式工业数据和四阶段渐进训练，将通用 MLLM 变成工业检测专家。

## 方法详解

### 整体框架
基于 Qwen2.5-VL-7B，增加一个 Comparison Encoder 模块。输入为待检测图像 + 正常模板图像对，先经过 Vision Encoder 提取各自特征，然后 Comparison Encoder 对两张图像特征做跨注意力，生成 100 个 comparison tokens 编码它们的视觉差异，最后将原始图像 tokens + comparison tokens 一起送入 LLM 做推理。

### 关键设计

1. **Comparison Encoder**:
   - 做什么：在视觉编码阶段就捕捉两张图像之间的细粒度差异
   - 核心思路：受 DETR 启发，设计可学习的 comparison queries（100 个），通过跨注意力机制与配对图像特征交互。具体地，每张图像的细粒度特征与其配对图像做 cross-attention，然后 comparison queries 压缩交互结果为固定长度的 tokens
   - 设计动机：**不修改原始图像特征**，而是生成额外的 comparison tokens — 这保证了基础模型能力不退化，同时 comparison tokens 提供了补充性的差异线索。相比 OneDiff 等直接修改图像特征的做法更加安全
   - 支持流式处理：每张图像只与前一张配对（第一张自配对），可适配任意数量的输入图像

2. **Chat-AD 数据集**:
   - 做什么：构建最大规模的工业多模态数据集（62万样本，200万QA对，327个工业类别）
   - 核心思路：从 VIADUCT、Real-IAD、MANTA 等公开+私有数据集收集 112 万工业图像，每个 query 图像配对一个正常模板图像（对比式范式），然后通过 GPT-4o/Qwen2.5-VL-72B 生成对比描述、多轮对话、可验证 QA 和推理数据，经人工迭代精修确保质量
   - 设计动机：以"对比"为核心数据范式——生成的文本显式描述异常图像与正常模板之间的差异，而非简单的图像描述，直接强化视觉对比范式
   - 数据与 MMAD 测试集类别无重叠，避免数据泄漏

3. **四阶段渐进训练**:
   - **Stage 0 (学习比较)**: 在通用变化检测数据（CLEVR-Change, MagicBrush, Spot-the-diff，3万样本）上全参数微调 Comparison Encoder，冻结 LLM。教会比较模块感知视觉差异
   - **Stage 1 (工业对比)**: LoRA 微调 Comparison Encoder + LLM，用 21.8 万工业对比描述数据做领域对齐。文本显式强调异常 vs 正常的差异
   - **Stage 2 (多任务指令)**: 解锁所有模块端到端 LoRA 微调，用 29.8 万多轮对话数据覆盖判别/分类/描述/定位/分析等多种 IAD 任务。混合通用数据防止遗忘
   - **Stage 3 (推理强化)**: 基于 GRPO 的强化学习，用可验证的多选题和定位任务做奖励。奖励函数结合选择题准确率和 bbox IoU：$R(x,y) = \lambda R_{\text{fmt}}(y) + \mathbf{1}[C_{\text{pred}}=C_{\text{gt}}]$（多选题）或 $\mathbf{IoU}(B_{\text{pred}}, M_{\text{gt}})$（定位）

### 损失函数 / 训练策略
- SFT 阶段用标准 cross-entropy loss，RL 阶段用 GRPO + 组合奖励函数
- LoRA rank=64, α=128, 学习率 5e-5，cosine scheduler，各阶段 2 epochs
- 总训练成本约 2400 GPU hours（单节点）

## 实验关键数据

### 主实验（MMAD Benchmark, 1-shot）

| 模型 | 规模 | 异常判别 | 缺陷分类 | 缺陷定位 | 缺陷描述 | 物体分析 | 平均 |
|------|------|---------|---------|---------|---------|---------|------|
| GPT-4o | - | 68.63 | 65.80 | 55.62 | 73.21 | 82.80 | 74.92 |
| Qwen2.5-VL-72B | 72B | 72.66 | 62.31 | 67.16 | 73.56 | 86.78 | 76.96 |
| Qwen2.5-VL-7B | 7B | 71.10 | 56.02 | 60.69 | 64.13 | 83.67 | 72.19 |
| AD-Copilot | 7B | 73.64 | 67.89 | 64.08 | 80.60 | 87.78 | 78.71 |
| **AD-Copilot†** | **7B** | **73.95** | **74.29** | **76.40** | **84.92** | **87.67** | **82.29** |
| 人类专家 | - | 95.24 | 75.00 | 92.31 | 83.33 | 80.37 | 86.65 |

### 消融实验（训练阶段 + Comparison Encoder）

| 配置 | ACC | F1 | 说明 |
|------|-----|-----|------|
| Baseline (Qwen2.5-VL-7B) | 72.19 | 72.49 | 无微调 |
| + Stage 0-1 (无 CompEnc) | 77.28 | 65.65 | 只有 SFT |
| + Stage 0-1 (有 CompEnc) | 76.92 | 73.27 | CompEnc 大幅提升 F1 |
| + Stage 0-2 (有 CompEnc) | 78.74 | 75.14 | 多任务指令微调 |
| + Stage 0-3 (有 CompEnc) | 82.29 | 74.23 | RL 推理阶段 |

### 关键发现
- Comparison Encoder 对 F1 贡献最大：在 Stage 0-1 配置下 F1 从 65.65 → 73.27（+7.62%），说明视觉级比较对异常判别至关重要
- RL 阶段的 bbox 奖励不可或缺：去掉 bbox reward 后平均分从 82.29 降到 79.74，且异常判别骤降 8%
- 数据质量 > 数据数量：用粗标注替代精细标注后即使数据量相同，性能大幅下降
- 模板图像的作用被激活：移除模板（0-shot）ACC 从 82.29 → 79.15，说明 AD-Copilot 真正利用了模板进行对比
- Comparison Encoder 可跨模型迁移：直接插入 Qwen2.5-VL-3B 无需微调即可提升 F1 (+2.4%)

## 亮点与洞察
- **Comparison Encoder 的"不改原始特征"设计**非常巧妙 — 生成额外 tokens 而非修改原图特征，保证即插即用且不降低基础模型能力。这种设计哲学值得借鉴到其他需要多图比较的任务（如 change detection、医学影像对比）
- **对比式数据范式**把"模板对比"嵌入数据构造的每个环节，从根本上改变了模型的学习目标。这比简单 prompt engineering 要求模型比较两张图有效得多
- **跨 benchmark 的泛化能力**令人印象深刻 — 在通用变化描述任务 OmniDiff-Real 上也超越 GPT-4o，说明学到的是通用视觉比较能力而非过拟合工业领域

## 局限性 / 可改进方向
- 在异常判别和精细定位上仍与人类专家有明显差距（73.95 vs 95.24），异常判别能力有很大提升空间
- MMAD-BBox 上即使最优的 AD-Copilot 也只有 25.30 mIoU，工业缺陷的精确定位仍然困难
- Chat-AD 数据集包含私有数据，可能限制复现性
- Comparison Encoder 的 100 tokens 数量是固定的，对极高分辨率或极小缺陷可能不够
- 仅在 1-shot 训练，虽然能泛化到 multi-shot，但多模板融合策略可能进一步提升

## 相关工作与启发
- **vs AnomalyGPT/EIAD**: 早期 IAD-MLLM 只是把 MVTec 标注转成 VQA 做微调，数据规模和质量都不够。AD-Copilot 的 Chat-AD (62万) 从数据量和多样性上是质的飞跃
- **vs AnomalyR1/EMIT**: 这些方法用 RL 直接在 MMAD 数据上训练存在数据泄漏风险，AD-Copilot 的训练集-测试集无类别重叠更公平
- **vs OneDiff**: OneDiff 直接修改图像特征做差异提取，可能影响基础能力；AD-Copilot 生成独立的 comparison tokens 更安全
- 这种"在编码阶段做细粒度比较"的思路可以迁移到 few-shot learning、医学影像病灶对比、遥感变化检测等需要图像对比较的场景

## 评分
- 新颖性: ⭐⭐⭐⭐ Comparison Encoder 和对比式数据范式的结合是工业 IAD+MLLM 方向的系统性创新
- 实验充分度: ⭐⭐⭐⭐⭐ 4个benchmark + 多维度消融 + 数据缩放实验 + 跨模型迁移 + 注意力可视化，非常全面
- 写作质量: ⭐⭐⭐⭐ 结构清晰，动机表述有力，但篇幅较长有些冗余
- 价值: ⭐⭐⭐⭐ 首次在 7B 模型上超越 GPT-4o 和普通人类水平，对工业质检落地有实际意义
