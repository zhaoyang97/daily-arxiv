# DocCogito: Aligning Layout Cognition and Step-Level Grounded Reasoning for Document Understanding

**日期**: 2026-03-08  
**arXiv**: [2603.07494](https://arxiv.org/abs/2603.07494)  
**代码**: 待发布  
**领域**: 多模态/VLM  
**关键词**: document understanding, layout perception, grounded reasoning, GRPO, Visual-Semantic Chain

## 一句话总结
提出 DocCogito，无 OCR 的文档理解框架——轻量 Layout Tower 将版面结构蒸馏为可学习的全局 [LAYOUT] token，同时用 Visual-Semantic Chain（VSC）把推理分解为 5 种原子操作的确定性结构化链，通过渐进式四阶段训练（Layout 预训练→VSC 冷启动→拒绝采样 SFT→GRPO+区域置信度奖励），在 DocVQA/InfoVQA/TextVQA/OCRBench 四个 benchmark 达 SOTA。

## 研究背景与动机

1. **领域现状**: 文档理解需要 MLLM 从复杂的表格/图表/表单中提取信息并推理。现有 MLLM 分别沿两条线推进：(a) 版面建模（DocLayLLM 引入 2D 位置编码 + 多模板 CoT；LayoutLLM 用 OCR + staged LayoutCoT）；(b) 用 CoT 提升推理可控性（DocThinker 用规则反馈做 CoT 规划）。
2. **现有痛点**: 这两条线各自发展但**缺乏耦合**——版面信息没被蒸馏为 CoT 过程的直接先验来引导定位，推理步骤也没被约束到持续聚焦对应证据区域。结果是模型在版面变化时会漂移到干扰区域，或用自由文本的 CoT 走捷径。同时自然语言 CoT 本身存在步骤粒度不一致、隐含假设多、语言描述歧义等问题，作为监督信号不稳定。
3. **核心矛盾**: 人类阅读文档是"先建立全局版面先验 → 再逐步收集证据 → 组合简单操作得到答案"，这种归纳偏置能泛化（全局浏览缩小搜索范围、逐步使用证据支持组合推理），但现有模型没有系统地实施这个过程。
4. **切入角度**: 把版面认知和推理执行**显式耦合**——用 Layout Tower 提供全局结构先验，用 VSC 替代自然语言 CoT 作为确定性、区域锚定的推理链，再用 GRPO + 区域置信度奖励强化两者的耦合。

## 方法详解

### 整体框架
DocCogito 采用标准 MLLM 架构（视觉编码器 + LLM），在此基础上增加一个轻量的 Layout Tower。输入文档图像 → 视觉编码器提取 patch 特征 → Layout Tower 生成全局 [LAYOUT] token → 拼接到文本 embedding 序列 → LLM 生成 VSC 格式的推理链和答案。训练分两大阶段：Stage 1 预训练 Layout Tower，Stage 2 多阶段后训练（VSC 冷启动 → 拒绝采样 SFT → GRPO）。

### 关键设计

1. **Layout Tower（轻量版面塔）**:
   - 做什么：从视觉 patch 特征中提取全局版面结构信息，生成单个 [LAYOUT] token 注入 LLM
   - 核心思路：给 patch embeddings $\mathbf{V} = \{\mathbf{v}_1, \dots, \mathbf{v}_N\}$ 经 LoRA 适配变换 $\mathbf{h}_i = \mathbf{v}_i + \Delta W_{\text{LoRA}} \mathbf{v}_i$，加位置编码后用 MLP 评分模块算每个 patch 的重要性 $\alpha_i = \text{Softmax}(\text{MLP}_\text{score}(\mathbf{h}_i + \mathbf{h}_{pos}))$，加权求和得全局 layout token $\mathbf{L} = \sum_{i=1}^N \alpha_i \cdot \mathbf{h}_i$。最后投影到语言空间并拼接文本 embedding
   - 设计动机：与 DocLayLLM 直接用 OCR bounding box 不同，Layout Tower 是端到端可学习的，从视觉特征中蒸馏版面结构，避免对 OCR 管线的依赖。低秩 LoRA 结构能以极少额外参数建模文档特有的结构子空间

2. **Visual-Semantic Chain（VSC，视觉-语义链）**:
   - 做什么：替代自然语言 CoT，用确定性的结构化表示监督推理过程
   - 核心思路：每个推理步骤表示为三元组 $\text{step} = \langle \text{op}, \text{region}, \text{args} \rangle$，其中 op 是原子操作符（Select/Read/Filter/Compare/Aggregate 五种），region 锚定到具体版面区域（header/table/cell 等），args 提供最小化可审计参数。完整推理链格式为 $\langle \text{question\_analysis}, \text{vsc}, \text{answer} \rangle$
   - 设计动机：自然语言 CoT 存在步骤粒度不一致、隐含假设、语言歧义三大问题，作为监督信号不稳定。VSC 通过固定的操作符集合和显式的区域引用消除这些歧义，更短更确定，同时覆盖了文档 QA 的常见推理模式

3. **区域置信度奖励（Region Confidence Reward）**:
   - 做什么：在 GRPO 中强化推理步骤与证据区域的对齐
   - 核心思路：对每个 VSC 步骤 $t$ 的区域 token $r_t$，计算模型的预测概率 $p_t = P_\theta(r_t \mid \mathcal{H}_t, x)$，长度归一化几何平均 $\tilde{r}_\text{reg} = \exp(\frac{1}{N}\sum_{t=1}^N \log p_t)$ 作为奖励
   - 设计动机：区域标签属于受限词表，首个区域 token 就能稳定指示区域正确性。这个奖励显式鼓励模型对正确区域分配高置信度，强化版面先验和 VSC 执行的耦合

### 损失函数 / 训练策略

**四阶段渐进训练**：

- **Stage 1 — Layout 预训练**（3 epochs, lr=1e-4）：冻结 LLM，只训 Layout Tower。用 20k 带 OCR 标注的 DocVQA 样本构建网格级监督 $\mathbf{Y}$，损失 $\mathcal{L} = \mathcal{L}_\text{KL} + 0.2 \cdot \mathcal{L}_\text{center}$（KL 散度 + 中心对齐）
- **Stage 2a — VSC 冷启动**（3 epochs, lr=1e-5）：用 4k 高质量 VSC 格式样本（来自 DocVQA 9 个类别，Qwen3-VL 标注+专家审核）做 SFT，防止早期策略坍缩
- **Stage 2b — 拒绝采样 SFT**（1 epoch, lr=5e-6）：在 100k 多领域 QA 语料上，模型生成回答，只保留结构有效且语义一致（F1 匹配）的样本做 SFT
- **Stage 2c — GRPO**（1 epoch, lr=1e-6）：复合奖励 $r = r_\text{ans} + 0.2 r_\text{qa} + 0.2 r_\text{vsc} + 0.2 r_\text{str} + 0.5 r_\text{reg}$，含答案正确性、问题分析、VSC 结构有效性、格式稳定性、区域置信度五项

## 实验关键数据

### 主实验

| 模型 | 参数 | DocVQA | InfoVQA | ChartQA | TextVQA | WTQ | OCRBench |
|------|------|--------|---------|---------|---------|-----|----------|
| Marten | 8.1B | 92.0 | 75.2 | 81.7 | 74.4 | 52.4 | 820 |
| InternVL2 | 8.1B | 91.6 | 74.8 | 83.3 | 77.4 | – | 794 |
| Qwen3-VL-4B | 4B | 89.0 | 74.6 | 80.4 | 79.1 | 54.4 | 775 |
| Qwen3-VL-8B | 8B | 91.6 | 75.7 | 81.3 | 80.7 | 57.1 | 804 |
| **DocCogito-4B** | 4B | **93.1** | 76.0 | 82.2 | 81.6 | 54.8 | 788 |
| **DocCogito-8B** | 8B | **93.2** | **78.6** | 82.5 | **82.4** | 58.3 | **841** |

8B 模型在 DocVQA (+1.2)、InfoVQA (+3.4)、TextVQA (+5.0)、OCRBench (+21) 达到新 SOTA。

### 消融实验

| 配置 | InfoVQA | TextVQA | ChartQA | WTQ |
|------|---------|---------|---------|-----|
| DocCogito-4B (完整) | 76.0 | 81.6 | 82.2 | 54.8 |
| w/o VSC-style CoT | 74.9 | 79.2 | 81.0 | 53.5 |
| w/o Layout Tower | 74.4 | 80.6 | 79.6 | 52.9 |
| w/o GRPO | 71.2 | 77.5 | 79.8 | 52.6 |
| w/o Layout Tower & GRPO | 71.8 | 77.1 | 80.8 | 53.4 |

### 关键发现
- **GRPO 贡献最大**：去掉 GRPO 在 InfoVQA 上掉了 4.8，TextVQA 上掉了 4.1，说明强化学习对多步推理校准至关重要
- **Layout Tower 对跨域泛化重要**：去掉后 ChartQA 掉 2.6（最大），说明表格/图表格外依赖全局版面先验
- **VSC 稳定提升**：去掉后 TextVQA 掉 2.4，证明结构化推理链在空间定位密集的场景效果显著
- **两者独立互补**：同时去掉 Layout Tower 和 GRPO 进一步恶化，说明版面表示和推理优化各自独立贡献
- **跨 backbone 泛化**：Qwen2.5VL-3B 上也有效（ChartQA 82.2 与 4B 相当），说明框架收益不依赖模型规模

## 亮点与洞察
- **VSC 替代自然语言 CoT 的思路很巧妙**：5 种原子操作就覆盖了文档 QA 的主要推理模式，结构化表示消除了自由文本 CoT 的歧义问题，且更短更可审计。这个思路可以迁移到其他需要可解释推理的场景（如医学等高风险领域）
- **区域置信度奖励设计优雅**：直接用模型自身对区域 token 的预测概率做奖励，无需额外标注或外部奖励模型。几何平均归一化处理也避免了长链偏移
- **渐进式训练 pipeline 设计系统**：从版面感知 → 推理格式 → 数据过滤 → 强化优化，每阶段解决不同问题，避免了一步到位训练的不稳定性

## 局限性 / 可改进方向
- **操作符集合有限**：5 种原子操作在当前 6 个 benchmark 上够用，但更复杂的推理场景（多页文档、跨文档推理）可能需要扩展操作符集
- **VSC 冷启动数据依赖 Qwen3-VL 标注**：4k 样本虽不多但仍需专家审核，如何自动化高质量 VSC 标注是实际部署的瓶颈
- **单页限制**：目前只处理单页文档，多页长文档的版面先验建模和跨页推理链尚未解决
- **ChartQA/WTQ 未达 SOTA**：这两个数值推理密集的 benchmark 上提升有限，可能因为 VSC 的 Aggregate 操作不够支撑复杂数值计算

## 相关工作与启发
- **vs DocLayLLM**: DocLayLLM 用 OCR bounding box + 2D positional embedding 做版面感知，配合多种 CoT 模板。DocCogito 做到无 OCR + 可学习的版面先验 + 统一的 VSC 推理链，更端到端且推理更可控
- **vs LayoutLLM**: LayoutLLM 用 staged LayoutCoT（问题分析→区域集中→答案形成），但仍是自然语言描述且依赖 OCR。DocCogito 的 VSC 用确定性操作符替代自然语言，更紧凑且减少歧义
- **vs DocThinker**: DocThinker 用规则反馈做 CoT 规划的 RL 优化，但缺乏版面认知。DocCogito 将版面先验和推理链在架构和训练两个层面同时耦合

## 评分
- 新颖性: ⭐⭐⭐⭐ VSC 替代自然语言 CoT + 区域置信度奖励是有意义的创新，但整体仍是"版面编码+CoT+GRPO"的组合
- 实验充分度: ⭐⭐⭐⭐ 6 个 benchmark + 完整消融 + 多 backbone 验证，OCRBench 子任务分解也做了
- 写作质量: ⭐⭐⭐⭐ 动机推导清晰，方法描述系统，附录材料丰富
- 价值: ⭐⭐⭐⭐ 为文档理解的可解释推理提供了系统方案，VSC 范式有后续拓展空间
