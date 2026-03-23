# 📅 2026-03-11 精选笔记

> 共 **20** 篇

---

### [A²-Edit: Precise Reference-Guided Image Editing of Arbitrary Objects and Ambiguous Masks](a2-edit.md)

🎨 图像生成 / 图像编辑

提出 A²-Edit，统一的参考引导图像修复框架，通过 Mixture of Transformers (MoT) 动态路由不同类别的专家进行差异化建模，配合 Mask Annealing Training Strategy (MATS) 逐步放松掩码精度要求，支持任意物体类别和任意精度掩码的编辑。

---

### [CUAAudit: Meta-Evaluation of Vision-Language Models as Auditors of Autonomous Computer-Use Agents](cuaaudit.md)

📄 多模态VLM / Agent评估

系统性地评估了 5 个 VLM 作为 Computer-Use Agent (CUA) 自动审计员的能力，跨三大操作系统基准测试，从准确率、置信度校准和模型间一致性三个维度揭示了当前 VLM 审计方法的局限。

---

### [DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control](dit4dit.md)

🤖 机器人 / 视频生成

提出 DiT4DiT，将视频扩散 Transformer 与动作扩散 Transformer 级联，通过双 flow-matching 目标联合训练，从视频去噪中间特征中提取时序条件来预测机器人动作，在 LIBERO (98.6%) 和 RoboCasa-GR1 (50.8%) 上达到 SOTA，样本效率提升 10 倍。

---

### [FairFAL: Federated Active Learning Under Extreme Non-IID and Global Class Imbalance](fed-active-learning.md)

🛡️ AI安全 / 联邦学习

系统性研究了联邦主动学习中全局/局部模型作为查询选择器的优劣，发现类别平衡采样（尤其是少数类采集）是性能关键，提出 FairFAL 框架通过自适应模型选择 + 原型引导伪标签 + 两阶段不确定性-多样性采样实现类别公平的联邦主动学习。

---

### [Fuel Gauge: Estimating Chain-of-Thought Length Ahead of Time in Large Multimodal Models](fuel-gauge.md)

⚡ 多模态VLM / LLM效率

提出 Fuel Gauge，首个运行时 CoT 长度预测框架——发现 LMM 内部存在"燃料信号"指示推理剩余长度，用 82K 参数的微型网络提取该信号，实现预测性 KV 缓存分配（内存分配频率降低 13.37 倍）和 CoT 长度调控（缓解过度/不足思考）。

---

### [Geometric Autoencoder for Diffusion Models](geometric-autoencoder.md)

🎨 图像生成 / 扩散模型

提出 Geometric Autoencoder (GAE)，通过构建低维语义监督目标、潜在空间归一化替代KL散度、动态噪声采样三大设计，系统性解决了潜在扩散模型中语义判别性、重建保真度和潜在空间紧凑性的统一难题，在 ImageNet 256×256 上以 32 维潜在空间达到 1.31 gFID (无CFG)。

---

### [HyPER-GAN: 基于混合Patch的图像翻译实现实时真实感增强](hyper-gan.md)

🎨 图像生成

提出 HyPER-GAN，一种轻量级 U-Net 风格生成器 + 混合 patch 训练策略的图像翻译方法，在 1080p 分辨率下以 33.7 FPS 实现实时合成图像真实感增强，同时保持语义一致性。

---

### [IMTBench: 面向图像内机器翻译的多场景跨模态协同评估基准](imtbench.md)

📄 多模态VLM

提出 IMTBench，一个包含 2500 个样本、覆盖 4 种场景和 9 种语言的图像内机器翻译（IIMT）评估基准，配套翻译质量、背景保持、视觉质量和跨模态对齐四维评估体系，系统性对比了级联系统与统一多模态模型的表现。

---

### [LIDA: Attribution as Retrieval — Model-Agnostic AI-Generated Image Attribution](lida-attribution.md)

🎨 图像生成 / AI安全

将 AI 生成图像归因问题从分类重新定义为实例检索问题，提出 LIDA 框架——通过低位平面指纹提取 + 无监督预训练 + 少样本归因适配，实现模型无关的零样本/少样本深伪检测和归因 SOTA。

---

### [LookaheadKV: Fast and Accurate KV Cache Eviction by Glimpsing into the Future without Generation](lookaheadkv.md)

⚡ 模型压缩 / LLM效率

提出 LookaheadKV，用可学习 lookahead token + 专用 LoRA 模块预测 KV cache 的真实重要性分数，无需显式生成 draft 响应，在保持 draft-based 方法精度的同时降低驱逐开销高达 14.5 倍。

---

### [Pointy: A Lightweight Transformer for Point Cloud Foundation Models](pointy.md)

🧊 3D视觉

提出 Pointy，一个轻量 Transformer 点云骨干网络（3.0M 参数），仅用 39K 点云训练就超越多个用 200K+ 数据训练的大型基础模型，接近用百万级多模态数据训练的 SOTA，证明精心设计的架构和训练协议比数据规模更重要。

---

### [Is this Idea Novel? An Automated Benchmark for Judgment of Research Ideas (RINoBench)](rinobench.md)

🗣️ LLM/NLP

提出 RINoBench，首个大规模研究 idea 新颖性判断基准——包含 1381 个经人类专家判断的研究 idea + 9 个自动评估指标，系统评测 SOTA LLM 能否准确判断 idea 新颖性，发现即便推理 LLM 生成的理由与人类相似，其新颖性评分仍显著偏离人类金标准。

---

### [Are Video Reasoning Models Ready to Go Outside? (ROVA)](rova.md)

🎬 多模态VLM / 视频理解

提出 ROVA 训练框架和 PVRBench 基准，通过结构化时空扰动生成 + 自反思难度感知课程学习 + 双分支对齐奖励优化，使视频推理模型在真实世界扰动（天气/遮挡/相机抖动/光照）下准确率相对提升 24%+，推理质量提升 9%+。

---

### [SignSparK: Efficient Multilingual Sign Language Production via Sparse Keyframe Learning](signspark.md)

🧊 3D视觉 / 手语生成

提出 SignSparK，基于稀疏关键帧训练的手语生成框架，通过 FAST 自动分割模型提取语言学关键帧 + Conditional Flow Matching 从关键帧锚点生成连续 3D 手语序列，实现 100 倍效率提升并覆盖 4 种手语的最大多语言 SLP 系统。

---

### [TennisExpert: Towards Expert-Level Analytical Sports Video Understanding](tennis-expert.md)

🎬 视频理解

构建了最大规模网球视频基准 TennisVL（202场比赛/40k+ rally片段），并提出 TennisExpert 框架——通过视频语义解析器 + 长短期记忆机制增强 Qwen3-VL-8B，实现超越 GPT-5、Gemini、Claude 的专家级网球战术解说生成。

---

### [UniCompress: Token Compression for Unified Vision-Language Understanding and Generation](unicompress.md)

📦 多模态VLM / 模型压缩

提出 UniCompress，面向统一视觉-语言模型的即插即用视觉 token 压缩框架，通过可学习全局元 token 引导的压缩-解压机制将视觉 token 压缩 4 倍，理解任务掉点 ≤3%，生成 FID 增加 ≤5，推理延迟降低 41.8%。

---

### [UniStitch: Unifying Semantic and Geometric Features for Image Stitching](unistitch.md)

📄 多模态VLM / 图像拼接

首次将传统几何特征（关键点）与学习语义特征统一到图像拼接框架中，通过 Neural Point Transformer 将稀疏离散关键点转换为密集 2D 几何图，再用 Adaptive Mixture of Experts 自适应融合两类特征，大幅超越单模态方法。

---

### [The Unlearning Mirage: A Dynamic Framework for Evaluating LLM Unlearning](unlearning-mirage.md)

🗣️ LLM/NLP / AI安全

提出动态评估框架，证明现有 LLM 遗忘方法是"海市蜃楼"——表面看似成功遗忘的信息通过多跳推理和实体别名查询即可恢复，原因在于遗忘仅破坏了主要计算通路而非全部通路。

---

### [V₀.₅: Generalist Value Model as a Prior for Sparse RL Rollouts](v05-value-model.md)

🧠 LLM推理 / 强化学习

提出 V₀.₅ 框架，将预训练的通用价值模型（V₀）作为统计先验与稀疏在线 rollout 的经验均值自适应融合，通过实时假设检验和动态预算分配构建鲁棒的优势基线，在 6 个数学推理基准上相比 GRPO/DAPO 提升 10%+。

---

### [WebVR: Benchmarking Multimodal LLMs for WebPage Recreation from Videos via Human-Aligned Visual Rubrics](webvr.md)

📄 多模态VLM / 代码生成

提出 WebVR，首个视频到网页生成基准——175 个合成网页 + 细粒度人对齐视觉评分体系，评估 19 个 MLLM 从演示视频忠实重建网页的能力，自动评估与人类偏好达 96% 一致率。

---
