# Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion

**日期**: 2026-03-06  
**arXiv**: [2603.06577](https://arxiv.org/abs/2603.06577)  
**代码**: https://omni-diffusion.github.io  
**领域**: 图像生成  
**关键词**: discrete diffusion, multimodal, any-to-any, mask-based generation, unified model

## 一句话总结
首个基于 mask-based 离散扩散模型的 any-to-any 多模态语言模型——Omni-Diffusion 通过统一的 mask token 预测直接建模文本/图像/语音的联合分布，配合三阶段渐进训练和专用推理策略，在多模态理解和生成任务上达到可比甚至超越自回归方法的性能。

## 研究背景与动机

1. **领域现状**：多模态大模型（MLLMs）几乎全部采用自回归架构作为 backbone。虽然离散扩散模型在 NLP 和图像生成各自领域已展示潜力，但尚未被用于构建统一的多模态系统。

2. **现有痛点**：(a) 自回归模型逐 token 解码效率低，无法并行生成；(b) 现有 any-to-any 模型（如 NExT-GPT）用 LLM 生成文本，再用额外模型转换到其他模态——不是真正统一的表示空间；(c) 离散扩散的灵活性优势（控制生成结构、格式、风格）在多模态设置中未被探索。

3. **核心矛盾**：要实现真正的 any-to-any 多模态统一模型，需要一个能在同一框架下处理理解和生成、同时支持多种模态的 backbone——自回归架构有天然局限（顺序生成、无法控制生成顺序）。

4. **切入角度**：mask-based 离散扩散模型天然适合多模态统一——它通过 mask token 预测工作，对所有模态的离散 token 一视同仁，还支持并行解码和灵活控制生成。

5. **核心 idea**：用 mask-based 离散扩散模型（Dream-7B）作为 backbone，直接建模文本+图像+语音离散 token 的联合分布，实现统一的多模态理解和生成。

## 方法详解

### 整体框架
多模态输入（文本/图像/语音）→ 各自分词器转为离散 token（文本词表 + MAGVIT-v2 图像 8192 码本 + GLM-4-Voice 语音 16384 码本）→ 拼接为统一序列 + 特殊起止 token → mask-based 离散扩散模型（Dream-7B）做统一 mask token 预测 → 输出所需模态 token → 各自解码器重建。

### 关键设计

1. **统一 mask token 预测**:
    - 做什么：在一个框架下对所有模态执行相同的 mask-unmask 训练
    - 核心思路：对统一序列 $x_0$ 按随机比率 $r$（从时间步 $t \sim [0,1]$ 导出）替换为 [MASK]，模型预测原始 token。Loss: $L = -\mathbb{E}[\sum_i \mathbb{I}[x_t^i = \text{MASK}] \log p_\theta(x_0^i | x_t)]$
    - 设计动机：无模态特定优化，所有模态在同一表示空间中自动对齐

2. **三阶段渐进训练**:
    - Stage 1（视觉-语言预对齐）：文本↔图像任务（T2I + captioning）
    - Stage 2（语音-视觉-语言联合对齐）：加入 ASR + TTS 数据
    - Stage 3（语音驱动视觉交互）：用构造的 SDVI 数据集（>30K spoken VQA + 30K speech-to-image）
    - 设计动机：不同模态的数据分布差异大，渐进扩展保证训练稳定性

3. **推理优化策略**:
    - **Position Penalty**：早期推理阶段降低序列尾部 token 的 logits，防止首尾同时解码导致图像重复模式
    - **Special Token Pre-infilling**：在初始 mask 序列的 0.25L 处填入 [begin-of-speech]，使模型前段生成文本、后段生成语音，实现文本语义引导语音生成
    - **Adaptive Token Length**：根据文本/语音长度相关性自适应分配初始序列长度（TTS: 3.5×文本长, ASR: 0.2×语音长）
    - **Attenuated Tail-Pad Masking**：训练时对 pad token 降低 mask 比率（γ<1），防止模型过拟合到生成 pad

### 损失函数
标准 cross-entropy mask token 预测 loss，无模态特定 loss。

## 实验关键数据

### 主实验（VQA + 图像生成）

| 方法 | 类型 | POPE↑ | MME-P↑ | CLIP-T↑ | CLIP-I↑ |
|------|------|:---:|:---:|:---:|:---:|
| LLaVA | Visual LLM | 76.3 | 809.6 | - | - |
| InstructBLIP | Visual LLM | 78.9 | 1212.8 | - | - |
| AnyGPT | Any-to-Any | 67.7 | - | - | 0.650 |
| NExT-GPT | Any-to-Any | - | - | 0.225 | 0.691 |
| **Omni-Diffusion** | **Any-to-Any** | **76.6** | **1216.7** | **0.235** | **0.667** |

### 语音任务

| 方法 | LibriSpeech WER↓ | LibriTTS WER↓ |
|------|:---:|:---:|
| GLM-4-Voice | 2.82 | 5.64 |
| AnyGPT | 8.50 | - |
| **Omni-Diffusion** | **7.05** | **3.07** |

### 关键发现
- 作为 any-to-any 模型，Omni-Diffusion 在 VQA 上达到专用 Visual LLM（InstructBLIP）水平（POPE 76.6 vs 78.9），远超其他 any-to-any 模型
- TTS WER 3.07 接近专用 TTS 模型 CosyVoice（2.89），大幅超越语音 LLM
- 图像生成只需 10 步就保持不错质量（CLIP-T 0.226 vs 256 步 0.235），体现扩散模型并行解码优势
- 语音→图像和文本→图像生成质量相近（CLIP-I 0.645 vs 0.667），证明跨模态对齐有效

## 亮点与洞察
- **离散扩散作为统一多模态 backbone 的首次验证**：证明了 mask-based diffusion 可以替代自回归架构做多模态 foundation model，开辟了新的架构范式
- **Position Penalty 和 Pre-infilling 策略巧妙利用了扩散模型的灵活性**：自回归模型无法做到的"控制生成顺序"和"预填充中间 token"，是扩散模型的独特优势
- **少步推理保持质量**：10 步就能生成合理图像，对比自回归模型需要逐 token 生成数百 token，效率优势明显

## 局限性 / 可改进方向
- 图像生成质量（CLIP-T 0.235）仍低于专用图像生成模型
- 基于 MAGVIT-v2 的图像 tokenizer 分辨率和质量受限
- 目前只支持文本/图像/语音三种模态，视频等未涵盖
- Dream-7B backbone 的参数量限制了模型能力上限

## 相关工作与启发
- **vs AnyGPT**: 同为 any-to-any，但 AnyGPT 用自回归架构，VQA 和语音性能均不如 Omni-Diffusion
- **vs NExT-GPT**: NExT-GPT 依赖外部扩散模型做图像生成，Omni-Diffusion 是端到端统一
- **vs Dream-7B (backbone)**: Dream 是纯文本扩散 LLM，Omni-Diffusion 扩展到多模态

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首个基于离散扩散的 any-to-any 多模态模型，架构范式创新
- 实验充分度: ⭐⭐⭐⭐ 覆盖语音/视觉/跨模态多个 benchmark，有采样效率分析
- 写作质量: ⭐⭐⭐⭐ 方法描述清晰，训练和推理策略讲解到位
- 价值: ⭐⭐⭐⭐⭐ 为多模态 foundation model 的架构选择提供了重要的新方向
