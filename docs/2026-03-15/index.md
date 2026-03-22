# 📅 2026-03-15 精选笔记

> 共 **20** 篇

---

### [AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents](agentprocessbench.md)

🦾 LLM Agent

首个面向 tool-use agent 的步级有效性评估基准（1000 条轨迹 / 8509 步人工标注），采用三元标签 (+1/0/-1) 和误差传播规则，揭示弱模型因 early termination 导致虚高正确率、当前 LLM 难以区分 neutral 和 erroneous 动作。

---

### [On the Nature of Attention Sink that Shapes Decoding Strategy in MLLMs](attention-sink-outro.md)

📄 多模态VLM

系统分析 MLLM 中 attention sink 现象的本质，发现 sink token 的 value 表示编码了结构化全局信息（而非无用），据此提出 OutRo——通过将非 sink 位置的 head output 旋转向 sink value 方向 + 放松 sink token 的因果 mask，在 7 个视频 QA benchmark 上一致提升性能，仅 1.1× 解码开销。

---

### [Balancing Multimodal Domain Generalization via Gradient Modulation and Projection](balancing-multimodal-dg.md)

🎬 视频理解 / 多模态VLM

提出 GMP 策略，通过 IGDM 解耦分类/域不变梯度并用语义+域信心调制 + CAGP 检测梯度冲突并投影到无冲突方向，在 EPIC-Kitchens 视频-音频跨域泛化中目标域提升 2.3%（传统方法仅 ±0.65%）。

---

### [CangjieBench: Benchmarking LLMs on a Low-Resource General-Purpose Programming Language](cangjiebench.md)

🧠 NLP生成 / LLM推理

为新兴仓颉编程语言创建首个零污染 benchmark（248 个手工翻译样本），覆盖函数级和类级任务，评估四种生成范式（直接/语法约束/RAG/Agent），发现 Code-to-Code 翻译存在负迁移、语法约束最佳性价比、Agent 最高准确但 token 消耗大。

---

### [ChArtist: Generating Pictorial Charts with Unified Spatial and Subject Control](chartist.md)

🎨 图像生成

提出 ChArtist，基于 FLUX DiT 训练两个 LoRA（空间控制+主题控制），用 skeleton-based 图表表示和 Spatially-Gated Attention 生成保真且视觉丰富的图形化图表，配套 30K 三元组数据集和统一数据准确度评估指标。

---

### [DC-ViT: Modulating Spatial and Channel Interactions for Multi-Channel Images](dc-vit.md)

🛰️ 多通道图像处理 / 遥感

提出 DC-ViT，将 ViT 自注意力解耦为空间路径（通道内）和通道路径（跨通道），通过选择性层级通道交互和分层聚合，在 CHAMMI/JUMP-CP/So2Sat 三个多通道图像基准上大幅超越 ChannelViT（+7.14% OOD）。

---

### [Deeper Thought, Weaker Aim: Understanding and Mitigating Perceptual Impairment during Reasoning in MLLMs](deeper-thought-vrga.md)

🧠 多模态VLM / LLM推理

揭示 CoT 推理导致 MLLM 视觉注意力分散（"想得越深、瞄得越偏"），发现有效视觉 head 满足 $R_\text{img}$高 + $H_\text{img}$低（高图像关注 + 低空间熵）的线性关系，提出 VRGA 框架在推理时选择性增强 question-relevant 区域注意力，无训练地提升 VQA 准确率 1-6 分。

---

### [DiFlowDubber: Discrete Flow Matching for Automated Video Dubbing](diflowdubber.md)

🎨 图像生成 / 视频理解

提出 DiFlowDubber，用 Discrete Flow Matching 生成骨干将大规模 TTS 预训练知识迁移到视频配音，通过 FaPro 模块从面部表情捕获韵律先验 + Synchronizer 模块实现视频-文本-语音三模态对齐，在 Chem 和 V2C 数据集上超越 SOTA。

---

### [DualTSR: Unified Dual-Diffusion Transformer for Scene Text Image Super-Resolution](dualtsr.md)

🎨 图像生成 / NLP生成

提出 DualTSR，用单一多模态 Transformer 同时建模图像超分（Conditional Flow Matching）和文字识别（Discrete Diffusion），去除对外部 OCR 的依赖，在中文场景文字超分上取得最优感知质量和文字保真度。

---

### [ES-Merging: Biological MLLM Merging via Embedding Space Signals](es-merging.md)

📦 多模态VLM / 模型压缩

提出 ES-Merging，用 embedding space 信号（而非 parameter space 启发式）估计 merging 系数，在 layer-wise 粗粒度和 element-wise 细粒度两个层面融合生物领域的分子/蛋白质/细胞三个 MLLM，在跨模态交互预测任务上超越所有现有 merging 方法甚至超过 task-specific fine-tuned 模型。

---

### [Fair Benchmarking of Emerging One-Step Generative Models Against Multistep Diffusion and Flow Models](fair-benchmarking-onestep.md)

🎨 图像生成

建立公平基准比较 8 个单步/多步生成模型，统一 CFG=7 + 双步评估（1步 vs 25步），提出 MMHM 综合指标平衡 FID/IS/CLIP/PickScore，揭示单步模型虽进步快但 25 步模型仍优，FID 优化与人类偏好存在系统性权衡。

---

### [FOCUS: Bridging Fine-Grained Recognition and Open-World Discovery across Domains](focus-fg-dg-gcd.md)

🔍 目标检测 / 域泛化

首次定义 Fine-Grained Domain-Generalized GCD (FG-DG-GCD) 问题，提出 FoCUS 框架结合 Domain-Consistent Parts Discovery (DCPD) 和 Uncertainty-Aware Feature Augmentation (UFA)，在 CUB/Cars/Aircraft 跨域细粒度基准上超越 GCD/FG-GCD/DG-GCD 基线 3-10%，计算效率提升 ~3×。

---

### [GenState-AI: State-Aware Dataset for Text-to-Video Retrieval on AI-Generated Videos](genstate-ai.md)

🎬 视频理解 / 多模态VLM

提出 GenState-AI benchmark，用 Wan2.2 生成 AI 视频，每个 query 配 temporal hard negative（改终态）和 semantic hard negative（换物体），三元组设计暴露现有 MLLM 检索模型在终态判断上的系统性失败。

---

### [GoldenStart: Q-Guided Priors and Entropy Control for Distilling Flow Policies](goldenstart.md)

🎨 图像生成 / 强化学习

提出 GoldenStart (GSFlow)，通过 Q-guided CVAE 学习高价值初始噪声分布（"golden start"）+ 熵正则化蒸馏实现探索-利用平衡，将 flow matching 策略蒸馏为高效的单步推理策略，在 OGBench 和 D4RL 上显著超越 FQL 等 SOTA。

---

### [LatSearch: Latent Reward-Guided Search for Faster Inference-Time Scaling in Video Diffusion](latsearch.md)

🎨 视频理解 / 图像生成

提出 LatSearch，在视频扩散推理过程中用 latent reward model 对中间去噪状态打分，配合 Reward-Guided Resampling and Pruning (RGRP) 策略进行搜索，在 VBench-2.0 上比 baseline 提升 3.35% 质量的同时仅需 2.13× 推理时间（相比 EvoSearch 的 10.15× 快近 5 倍）。

---

### [LongVidSearch: An Agentic Benchmark for Multi-hop Evidence Retrieval Planning in Long Videos](longvidsearch.md)


🎬 视频理解 / LLM Agent

提出 LongVidSearch benchmark（3000 QA / 447 长视频 / 平均 26 分钟），通过 N-1 adversarial ablation 严格保证 multi-hop 检索的必要性，用统一 tool 接口评估 agent 的检索规划能力，GPT-5 最高准确率仅 42.43%，揭示 multi-hop retrieval planning 是当前最大瓶颈。

---

### [PA³: Policy-Aware Agent Alignment through Chain-of-Thought](pa3-policy-alignment.md)

🧠 LLM推理 / LLM Agent

提出 PA³ 多阶段对齐方法训练 LLM agent 在 CoT 推理中自行回忆和应用业务策略（无需全部策略放入上下文），引入 PolicyRecall reward (Jaccard score) 和 Hallucination Penalty 用于 GRPO 训练，比基线提升 16 分，比同规模方法高 3 分且少用 40% token。

---

### [Safety-Potential Pruning for Enhancing Safety Prompts Against VLM Jailbreaking Without Retraining](safety-potential-pruning.md)

🛡️ 多模态VLM / AI安全

提出 Safety Subnetwork Hypothesis——VLM 内部存在稀疏的安全子网络，safety prompt 会选择性激活深层参数。据此提出 Safety-Potential Pruning，一次性剪枝对 safety prompt 不响应的权重，无需重训地将攻击成功率降低最多 22%。

---

### [Uni-MDTrack: Learning Decoupled Memory and Dynamic States for Parameter-Efficient Visual Tracking in All Modality](uni-mdtrack.md)

🎬 视频理解 / 目标检测

提出 Uni-MDTrack，用 Memory-Aware Compression Prompt (MCP) 将记忆库压缩为固定 token + Dynamic State Fusion (DSF) 用 SSM 捕捉目标连续动态状态，仅训练 <30% 参数即在 RGB/RGB-D/T/E/Language 五种模态 10 个数据集上达到 SOTA。

---

### [UniFusion: A Unified Image Fusion Framework with Robust Representation and Source-Aware Preservation](unifusion.md)

🎨 多模态VLM / 图像生成

提出 UniFusion，利用 DINOv3 语义先验 + reconstruction-alignment 机制 + bilevel optimization 策略，构建跨任务统一图像融合框架，在红外-可见光/医学/多曝光/多焦点四大融合任务上全面超越 TC-MoA 等 SOTA。

---
