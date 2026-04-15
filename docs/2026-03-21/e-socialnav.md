# E-SocialNav: Efficient Socially Compliant Navigation with Language Models

**日期**: 2026-03-21  
**arXiv**: [2603.20664](https://arxiv.org/abs/2603.20664)  
**代码**: https://github.com/Dr-LingXiao/ESocialNav  
**领域**: 机器人 / 社会导航 / 小语言模型  
**关键词**: Social Navigation, Small Language Model, SFT, DPO, Phi-2, SigLIP, 多模态

## 一句话总结

评估 GPT-4o/Claude 在社会导航中的零样本能力（效果很差），提出 E-SocialNav：基于 Phi-2-2.7B + SigLIP 的小语言模型，通过两阶段训练（SFT on 多轮对话 + DPO on 单轮偏好对）在小数据（265 张图）下超越零样本大模型，最佳配置 SFT(projector)+DPO(lora) 达到 SMS 0.846、FPS 2.354、AA 0.550。

## 研究背景与动机

1. **领域现状**: 语言模型日益被用于机器人导航，VLM-Social-Nav 等方法已用 GPT-4v 生成导航指令，但现有基准主要关注导航成功率而忽视社会合规性。
2. **现有痛点**: 大规模 LLM（GPT-4、Claude）推理延迟高、能耗大，无法在资源受限的机器人平台上实时部署；且缺乏对这些模型零样本社会导航能力的系统评估。
3. **核心矛盾**: 社会导航需要理解和预测人群意图、管理动态环境不确定性、平衡效率与安全舒适，但大模型部署成本高，小模型又缺乏足够的上下文理解与常识推理能力。
4. **本文要解决什么**: (1) 系统评估 GPT-4o 和 Claude 的零样本社会导航能力；(2) 设计一个高效的可训练小语言模型（SLM），在小数据条件下实现社会合规导航。
5. **切入角度**: 从 SLM + 视觉塔（VT）的选型出发，通过两阶段训练（SFT 学感知推理 + DPO 学偏好对齐）在有限数据下最大化性能。
6. **核心 idea 一句话**: 用 Phi-2-2.7B + SigLIP 构建轻量多模态模型，结合多轮对话 SFT 和单轮偏好 DPO 两阶段训练，以 2.7B 参数在社会导航任务上超越 GPT-4o 零样本。

## 方法详解

### 整体框架

E-SocialNav 由 Vision Tower (VT) + Projector + Small Language Model (SLM) 三部分组成。训练分两阶段：Stage I 在多轮对话数据上做 SFT（只训 projector），Stage II 在单轮偏好对数据上做 DPO（只训 LoRA adapter）。推理时接收机器人第一视角图像，输出社会合规的导航动作和理由。

### 关键设计

**设计一：多轮对话 SFT 数据集构建**

- **做什么**: 基于 SNEI 数据集（源自 SCAND 和 MuSoHu）构建 325 个样本，每个样本包含自车视角图像 + 五轮对话。265 训练 / 60 测试。
- **核心思路**: 多轮对话而非单轮让模型学习跨对话轮次的上下文感知推理，不仅学感知还学推理。
- **设计动机**: 小数据场景下，多轮对话能提供更丰富的监督信号，帮助模型建立从图像到导航决策的完整推理链。

**设计二：DPO 偏好对构建**

- **做什么**: 对每个输入构造 chosen/rejected 响应对。chosen 是人类标注的 ground-truth，rejected 通过修改 chosen 中的部分事实生成。
- **核心思路**: 不需要额外标注，直接从正确答案中"破坏"事实来生成负样本，如将"停下等待"改为"继续直行"。
- **设计动机**: 在标注稀缺的场景下，低成本构造高质量偏好对，让模型学到"哪些行为是社会合规的，哪些是不合规的"。

**设计三：VT 和 SLM 选型**

- **做什么**: 系统比较 CLIP/DINO/SigLIP 三种 VT 和 TinyLlama-1.1B/StableLM-1.6B/Phi-2-2.7B 三种 SLM 的组合。
- **核心思路**: SigLIP + Phi-2 组合在所有指标上最优。SigLIP 的 sigmoid 损失比 CLIP 的对比损失提供更好的视觉表征。
- **设计动机**: 在效率（参数量）和性能之间寻找最佳平衡点。

### 损失函数 / 训练策略

- **SFT 损失**: 标准 next-token NLL，仅计算 assistant response tokens，不含 prompt/image tokens。$\mathcal{L}_{\text{SFT}}(\theta) = \frac{1}{\sum_t N_t} \sum_{t=1}^T \sum_{n=1}^{N_t} [-\log \pi_\theta(y_{t,n} | x_t, y_{t,<n})]$
- **DPO 损失**: $\mathcal{L}_{\text{DPO}}(\theta) = -\frac{1}{T}\sum_{t=1}^T \log\sigma(\beta \Delta_\theta(t))$，其中 $\Delta_\theta(t) = \ell^+_\theta(t) - \ell^-_\theta(t)$，$\beta = 0.1$
- **训练策略**: Stage I 训 20 epochs（lr=5e-5, warmup 0.03, FlashAttention-2），Stage II DPO 训 5 epochs。4×A100，总训练时间 < 1 小时。Stage I 仅训 projector，Stage II 仅训 LoRA。

## 实验关键数据

### 主实验

| 模型 | VT | LM | SMS↑ | FPS↑ | AA↑ |
|------|----|----|------|------|-----|
| Claude (zero-shot) | - | - | 0.641 | 0.087 | 0.417 |
| GPT-4o (zero-shot) | - | - | 0.651 | 0.212 | 0.450 |
| Social-LLaVA | CLIP ViT-L/14 | Vicuna-7B | 0.813 | 1.113 | 0.483 |
| E-SocialNav SFT(proj) | SigLIP | Phi-2-2.7B | 0.828 | 1.828 | 0.433 |
| **E-SocialNav SFT(proj)+DPO(lora)** | SigLIP | Phi-2-2.7B | **0.846** | **2.354** | **0.550** |

### 消融实验

| VT | SLM | SMS↑ |
|----|-----|------|
| CLIP | Phi-2-2.7B | 0.768 |
| DINO | Phi-2-2.7B | 0.833 |
| SigLIP | TinyLlama-1.1B | 0.789 |
| SigLIP | StableLM-1.6B | 0.837 |
| **SigLIP** | **Phi-2-2.7B** | **0.846** |

### 关键发现

1. GPT-4o 和 Claude 零样本社会导航能力极差：SMS 仅 0.64-0.65，AA 仅 0.42-0.45，远低于微调模型。
2. 两阶段训练的递进提升明显：SFT(projector) SMS 0.828 → 加 DPO(lora) 后 SMS 0.846、AA 从 0.433 跃升到 0.550。
3. Stage I 仅训 projector 最佳（冻结 backbone），训 vision/lora 反而性能下降——小数据下过拟合风险。
4. SigLIP > DINO > CLIP 作为视觉编码器，Phi-2 > StableLM > TinyLlama 作为语言模型。
5. E-SocialNav 比 Social-LLaVA (7B) 参数量小 60%+，但 SMS 和 AA 均更优。

## 亮点与洞察

- **小数据大效果**: 仅 265 张训练图像就超越零样本大模型，说明任务特定数据 + 精心设计的训练策略 > 单纯的模型规模。
- **DPO 负样本构造方法巧妙**: 通过修改正确答案中的事实生成 rejected 响应，零额外标注成本。
- **两阶段解耦训练**: SFT 阶段只练"感知对齐"（projector），DPO 阶段只练"偏好对齐"（LoRA），各司其职避免干扰。
- **实际部署友好**: 2.7B 参数 + FPS 2.354，在资源受限平台上可实时运行。

## 局限性 / 可改进方向

1. 测试集仅 60 张样本，统计显著性不够强。
2. 失败案例分析显示模型倾向保守（预测 "stop" 而非 "turn left"），可能是标注偏差。
3. 缺少真实机器人部署实验，仅在数据集上评估。
4. DPO 负样本构造较为简单（仅修改事实），更复杂的错误模式（如程度错误、时机错误）未覆盖。
5. 可考虑 RLHF 替代 DPO 进一步提升，或扩展到多文化场景的社会规范。

## 相关工作与启发

- **vs Social-LLaVA (7B)**: E-SocialNav 以 2.7B 参数超越 7B 的 Social-LLaVA（SMS 0.846 vs 0.813），证明小模型+精调 > 大模型粗调。
- **vs VLM-Social-Nav (GPT-4v)**: GPT-4v 推理延迟高且无法 GPU 加速，E-SocialNav 达到 2.354 FPS，实用性远超。
- **vs 通用 SLM 工作**: 本文的贡献在于证明 SLM 在社会导航这一具身任务上同样有效，而非仅限于 NLP。

## 评分

| 维度 | 分数 (1-5) | 说明 |
|------|-----------|------|
| 新颖性 | 3.5 | SFT+DPO 二阶段训练是成熟方案，创新在于应用到社会导航 + 负样本构造 |
| 实验充分度 | 3.0 | 数据集小（265/60），缺少真实部署和更大规模验证 |
| 写作质量 | 3.5 | 结构清晰，公式完整，但篇幅较短 |
| 价值 | 3.5 | 证明了 SLM 在具身社会导航中的可行性，具有实际应用价值 |

