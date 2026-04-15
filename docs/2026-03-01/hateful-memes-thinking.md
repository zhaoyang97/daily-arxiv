# Can Thinking Models Think to Detect Hateful Memes?

**日期**: 2026-03-01  
**arXiv**: [2603.01225](https://arxiv.org/abs/2603.01225)  
**代码**: 即将公开  
**领域**: 多模态/VLM / AI安全  
**关键词**: hateful meme detection, GRPO, chain-of-thought, thinking MLLM, reinforcement learning

## 一句话总结

提出基于 GRPO 强化学习的后训练框架，通过 CoT 蒸馏 + 多奖励联合优化（格式/标签/长度/语义），将 thinking-based MLLM（Qwen3-VL-8B）用于仇恨 meme 检测，在 Hateful Memes 基准上达到 81.2% 准确率（SOTA），同时生成高质量解释。

## 研究背景与动机

1. **领域现状**：仇恨 meme 融合图像和文本，单模态线索不足以判断——图片和文字分别看可能无害，但组合后传达仇恨意图。这要求模型具备组合式多模态推理能力。
2. **现有方法的局限**：
    - 早期方法（CNN + OCR、传统 ML）无法捕捉图文交互的细腻含义
    - 近期 MLLM 方法主要依赖 SFT + 粗粒度二分类标签，缺乏显式推理过程
    - 少数工作探索了 CoT 提示，但 CoT 在提升分类准确率的同时会降低解释质量（BERTScore 下降 1.6-12.5 分），存在分类-解释 trade-off
3. **核心矛盾**：thinking-based MLLM 的 CoT 推理能力在 meme 分析中的潜力未被充分开发——零样本 CoT 提示有帮助但不够，需要任务特定的后训练来同时优化推理和解释。
4. **切入角度**：用 GRPO（DeepSeek-R1 引入的 RL 方法）对 thinking MLLM 进行后训练，用规则奖励显式鼓励高质量推理链，而非依赖学习的评估模型。

## 方法详解

### 整体框架

给定一张 meme（图像 + OCR 文本），构建 instruction-following 输入（包含二分类标签、保护类别/攻击类型等细粒度标注、OCR 文本和分类指南）。模型输出结构化序列：`<think>推理过程</think> Label: 预测标签 Explanation: 解释`。训练采用两阶段后训练：SFT 预热 → GRPO 强化学习。推理时采样多个候选并打分选择最优。

### 关键设计

1. **CoT 蒸馏数据扩展**
    - 做什么：用 GPT-4.1 为每条 meme 生成分步推理链（CoTD），补充原始 Hateful Memes 数据集
    - 核心思路：以 meme 图像、OCR 文本、标注指南和二分类/细粒度标签为条件，提示 GPT-4.1 生成推理过程，明确禁止直接复制参考解释以防标签泄露。生成的 CoT 放在 `<think>` 标签内，仅训练时使用。
    - 质量验证：用 InternVL3.5 和 Phi-3.5 双模型作为 LLM-as-a-Judge，在信息性、清晰性、合理性和忠实性四维度评分（5 分制），平均 4.36-4.63 分，评委间一致性 $r_{wg(j)}^* = 0.94$，说明 CoT 质量可靠。

2. **SFT 预热阶段**
    - 做什么：标准 SFT 初始化，对齐模型到结构化输出格式和任务监督
    - 核心思路：三种变体——(a) Cls+Exp（无 CoT，仅二分类+解释），(b) Cls+FG+Exp（加细粒度标签），(c) Cls+FG+Exp+CoTD（加蒸馏 CoT）。对无 CoT 变体保留空 `<think></think>` 标签以保持格式一致。选最佳 checkpoint（按验证集 loss）。
    - 设计动机：先 SFT 再 RL 已被证明更稳定。消融证实冷启动 GRPO（不做 SFT）性能最差（76.8% vs 81.2%）。

3. **GRPO 优化阶段**
    - 做什么：对 SFT 初始化的模型进行 RL 后训练，强化高质量推理
    - 核心思路：对每条输入采样 $K=16$ 个候选输出，计算组合奖励：
     $$R(y) = 0.5 \cdot R_{\text{fmt}} + 0.4 \cdot R_{\text{lbl}} + 0.05 \cdot R_{\text{len}} + 0.05 \cdot R_{\text{met}}$$
     - $R_{\text{fmt}}$：格式一致性（有推理/预测/解释组件）
     - $R_{\text{lbl}}$：标签正确性
     - $R_{\text{len}}$：长度正则（高斯型，目标约 100 词，$\sigma=20$）
     - $R_{\text{met}}$：METEOR 语义相似度（与 gold rationale 比较）
     用组内平均奖励作 baseline 计算归一化优势，PPO-style clipped surrogate + KL 正则（$\beta=0.04$, clip $\epsilon=0.2$）。
   - 设计动机：GRPO 不需要额外训练 reward model，用规则奖励直接可计算；多奖励组合确保格式/准确性/解释质量同时优化。

### 损失函数 / 训练策略

- SFT 阶段：标准负对数似然损失，AdamW，cosine lr with warmup 0.05，3 epoch
- GRPO 阶段：clipped surrogate + KL 正则化，$\beta_{\text{KL}}=0.04$，采样 16 个候选，最大 4096 token，temperature 1.0，top-p 0.85
- 硬件：4×NVIDIA H200，DeepSpeed ZeRO-3，全参数训练

## 实验关键数据

### 主实验

在 Hateful Memes 测试集（2000 样本）上与 SOTA 方法对比：

| 方法 | Acc.↑ | W-F1↑ | M-F1↑ | BS↑ | MET↑ |
|------|-------|-------|-------|-----|------|
| Kiela et al. (2020) | 69.47 | – | – | – | – |
| Pro-Cap (2022) | 72.98 | – | – | – | – |
| Wu et al. (2024) | 76.4 | – | – | – | – |
| Burbi et al. (2023) | 77.7 | – | – | – | – |
| Mei et al. (2024) | 78.8 | – | – | – | – |
| MemeIntel (2025) | 79.9 | 0.80 | 0.79 | 0.78 | 0.49 |
| **Proposed** | **81.2** | **0.81** | **0.79** | **0.78** | **0.52** |

准确率 81.2% 超越此前 SOTA（MemeIntel 79.9%）1.3 个百分点，METEOR 提升约 3%（0.49→0.52），BERTScore 持平。

### 消融实验

| 配置 | Acc.↑ | W-F1↑ | M-F1↑ | BS↑ | MET↑ |
|------|-------|-------|-------|-----|------|
| SFT (Cls+Exp) | 77.0 | 0.77 | 0.75 | 0.77 | 0.48 |
| SFT (Cls+FG+Exp) | 78.1 | 0.78 | 0.77 | 0.77 | 0.48 |
| SFT (Cls+FG+Exp, CoTD) | 79.2 | 0.79 | 0.78 | 0.78 | 0.50 |
| GRPO (Cold Start) | 76.8 | 0.77 | 0.75 | 0.73 | 0.47 |
| SFT-Cls+Exp → GRPO | 80.4 | 0.80 | 0.78 | 0.76 | 0.50 |
| SFT-Cls+FG+Exp → GRPO | 81.1 | 0.81 | 0.79 | 0.77 | 0.52 |
| SFT-Cls+FG+Exp-CoTD → GRPO | **81.2** | **0.81** | **0.79** | **0.78** | **0.52** |

### 关键发现

- **SFT 预热至关重要**：冷启动 GRPO（76.8%）远低于 SFT+GRPO 组合（81.2%），RL 无法同时学习格式和任务。
- **细粒度标签有帮助**：加入保护类别/攻击类型后 SFT 提升 1.1%（77.0→78.1），GRPO 后依然保持优势。
- **CoT 蒸馏锦上添花**：CoTD 在 SFT 阶段提升最大（+1.1%），但在 GRPO 后增益变小（81.1→81.2），说明 GRPO 本身就能发现推理路径。
- **CoT collapse 现象**：CoTD 初始化的 GRPO 训练中，模型倾向压缩 `<think>` 段长度来提高奖励——这是一种 RL 捷径，未来需要控制推理 token 预算的奖励设计。
- **零样本分析**：CoT 提示对 thinking 模型（Qwen-T）分类提升最大（+4.6% Acc），但对所有模型的解释质量均有损害（BERTScore 下降），说明 CoT 使输出偏离简洁参考解释的分布。

## 亮点与洞察

- **GRPO 用于多模态内容审核**是新颖的应用。组合奖励设计（格式+标签+长度+METEOR）简单但有效，避免了额外训练 reward model 的成本。
- **发现 CoT collapse 现象**很有价值：RL 会驱使模型通过压缩推理链来作弊提升奖励，这对所有用 GRPO 训练推理模型的工作都有警示意义。作者建议加入推理长度约束奖励。
- **系统性的 CoT 效果分析**：在 7 个 MLLM 上对比 CoT 开/关的效果，发现 CoT 在分类和解释间存在 trade-off，这是很实用的经验发现。

## 局限性 / 可改进方向

- **单一基准**：仅在 Hateful Memes（~11k 样本）上验证，未测试跨域/跨语言泛化。
- **CoT 蒸馏依赖闭源模型**：GPT-4.1 生成的推理链可能引入偏见和不忠实推理，影响可复现性。
- **GRPO 计算开销大**：每条输入采样 16 个候选，训练成本高。
- **CoT collapse 未解决**：论文发现了问题但仅讨论了可能的缓解方向，未实际验证。

## 相关工作与启发

- **vs MemeIntel (EMNLP 2025)**: 同组前作，用 SFT + 人工验证推理训练。本文加入 GRPO 后训练 + CoT 蒸馏，准确率提升 1.3%。
- **vs 多 Agent 辩论框架 (Lin et al. 2024)**: 用多个 LLM agent 交换推理后决策，推理成本更高。本文用单模型 + RL 更高效。
- **启发**：GRPO + 多维规则奖励的范式可迁移到其他内容审核任务（假新闻检测、有害视频等），但需注意 CoT collapse 风险。

## 评分

- 新颖性: ⭐⭐⭐ GRPO 用于 meme 检测有新意，但 GRPO 本身是已有技术
- 实验充分度: ⭐⭐⭐⭐ 零样本/SFT/GRPO 层层消融，7 个 baseline 模型对比
- 写作质量: ⭐⭐⭐⭐ 结构清晰，实验分析深入（特别是训练动态分析）
- 价值: ⭐⭐⭐ 应用导向强，但受限于单一基准和数据集规模
