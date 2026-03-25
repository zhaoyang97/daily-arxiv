# 📅 2026-03-09 精选笔记

> 共 **20** 篇

---

### [BuildMamba: 基于视觉状态空间模型的多任务建筑分割与高度估计](buildmamba.md)

🛰️ 3D 视觉 / 遥感图像分析

提出 BuildMamba，基于 VMamba 视觉状态空间模型构建统一多任务框架，通过 Mamba 注意力模块、空间感知 Mamba-FPN 和掩码感知高度精修模块，实现仅从单张 RGB 卫星图像同时进行建筑分割和高度估计，在三个基准上刷新 SOTA。

---

### [Beyond Heuristic Prompting: A Concept-Guided Bayesian Framework for Zero-Shot Image Recognition](cgbc.md)

🧩 多模态/VLM

将 VLM 的零样本图像识别重新建模为概念空间上的贝叶斯边际化推断——用 LLM 驱动的四阶段流水线生成判别性、组合性、多样性的概念集合，再用自适应 soft-trim likelihood 下调离群概念权重，在 11 个数据集上一致超过 SOTA 零样本方法。

---

### [CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation](coco-code-cot.md)

🎨 图像生成

提出 CoCo 框架，将可执行代码作为 Chain-of-Thought 中间表示，先生成代码渲染结构化草图，再精细化编辑生成最终高质量图像，在结构化 T2I 生成任务上大幅超越现有方法。

---

### [ELLMob: Event-Driven Human Mobility Generation with Self-Aligned LLM Framework](ellmob.md)

🗣️ LLM/NLP 应用

提出 ELLMob 框架，基于模糊痕迹理论 (Fuzzy-Trace Theory) 构建自对齐 LLM 管道，通过提取和迭代对齐"习惯要旨"与"事件要旨"来调和日常出行惯性与突发事件约束的竞争，首次实现事件驱动的人类出行轨迹生成。

---

### [EvoStage: 基于 LLM 的演化分阶段自动算法设计](evo-stage.md)

📄 LLM / 自动算法设计

提出 EvoStage，将算法设计任务分解为多阶段子任务，结合多智能体系统和"全局-局部视角"机制，利用 LLM 在演化框架中逐阶段设计算法并获取中间反馈，在芯片布局等工业场景中仅用 25 次评估即超越人类专家设计和现有 LLM 方法。

---

### [FinToolBench: Evaluating LLM Agents for Real-World Financial Tool Use](fintoolbench.md)

🦾 LLM Agent

构建首个可执行的金融工具使用 benchmark FinToolBench（760 个真实金融 API + 295 条工具依赖查询），提出超越二元执行成功的评估维度——时效性/意图约束/监管域对齐三个合规指标，以及 FATR 金融感知工具检索 baseline。

---

### [HiAR: 基于层级去噪的高效自回归长视频生成](hiar.md)

📄 图像/视频生成

提出 HiAR，一种层级去噪框架，颠倒传统自回归视频生成的顺序——在每个去噪步骤内对所有块进行因果生成而非逐块完成，使每块始终以相同噪声水平的上下文为条件，从而抑制误差累积并实现约 1.8× 加速，在 VBench 20s 生成中取得最佳总分和最低时间漂移。

---

### [HMR-1: Hierarchical Massage Robot with Vision-Language-Model for Embodied Healthcare](hmr-1.md)

🤖 机器人

构建首个大规模穴位按摩多模态数据集 MedMassage-12K（12190 图像 + 174177 QA 对），提出分层按摩机器人框架 HMR-1——高层用微调的 Qwen-VL 理解语言指令并定位穴位，低层用 RANSAC+IK 规划运动轨迹，在 Franka Panda 上完成真实物理按摩实验。

---

### [IMSE: Intrinsic Mixture of Spectral Experts Fine-tuning for Test-Time Adaptation](imse.md)

⚡ LLM效率

将 ViT 线性层通过 SVD 分解为"谱专家"（rank-1 成分），只微调奇异值（spectral code）实现参数高效自适应，提出多样性最大化损失缓解熵最小化导致的特征坍缩，并设计域感知谱码检索机制实现 CTTA 中的域知识保存和快速复用，在 TTA/CTTA/Gradual CTTA 上全面 SOTA。

---

### [MERLIN: Building Low-SNR Robust Multimodal LLMs for Electromagnetic Signals](merlin.md)

🧩 多模态/VLM

构建电磁（EM）信号领域的完整 MLLM 基础设施：EM-100k 大规模数据集（10万信号-文本对）+ EM-Bench 评估基准（14个子任务4200 QA 对）+ MERLIN 两阶段训练框架（基础预训练 + 知识蒸馏增强低信噪比鲁棒性），通过 Denoising Subspace Module 将低 SNR 特征投射到干净子空间。

---

### [Adaptive Collaboration with Humans: Metacognitive Policy Optimization for Multi-Agent LLMs](metacognitive.md)

🦾 LLM Agent

提出 HILA 框架，通过元认知策略优化让多 Agent 系统学会何时自主解题、何时求助人类专家，配合双循环策略优化（内循环 RL 优化决策 + 外循环持续学习吸收专家知识），打破纯自治多 Agent 系统的知识天花板。

---

### [QualiTeacher: Quality-Conditioned Pseudo-Labeling for Real-World Image Restoration](qualiteacher.md)

🎨 图像生成

将伪标签质量从需要过滤的噪声转化为条件监督信号——将 NR-IQA 分数注入学生网络使其学习质量分级的修复流形，结合基于 DPO 的偏好优化确保分数-质量单调映射，使学生网络能外推到超越教师的修复质量。

---

### [RetroAgent: From Solving to Evolving via Retrospective Dual Intrinsic Feedback](retroagent.md)

🦾 LLM Agent / 强化学习

提出 RetroAgent 框架，通过回顾式自我反思机制生成双重内在反馈（数值反馈鼓励探索 + 语言反馈利用经验），使 LLM Agent 从"一次性解题"进化为"持续自我演进"，在四个 Agent 任务上大幅超越现有方法。

---

### [Can Vision-Language Models Solve the Shell Game?](shell-game.md)

🎬 视频理解

揭示当前 SOTA VLM 在视觉实体追踪（shell game 任务）上接近随机水平，提出 VET-Bench 诊断基准和 SGCoT 方法（时空定位的 CoT 推理），通过微调实现超过 90% 的追踪精度。

---

### [SOT-GLP: Local-Global Prompt Learning via Sparse Optimal Transport](sot-glp.md)

🧩 多模态/VLM

提出 SOT-GLP——用稀疏最优传输将显著 patch 均衡分配给各类别专属 local prompt，结合全局 prompt 保持整体对齐，在 11 个 benchmark 16-shot 上达到 85.1% 平均精度，并发现无投影版本在 OOD 检测上达 94.2% AUC 的 SOTA。

---

### [SWIFT: Sliding Window Reconstruction for Few-Shot Training-Free Generated Video Attribution](swift.md)

🎬 视频理解 / 生成视频溯源

提出 SWIFT，利用视频生成模型 3D VAE 的时序压缩特性，通过滑动窗口进行正常/破坏两轮重建，以重建损失比值作为归因信号，实现少样本甚至零样本的生成视频溯源。

---

### [TALON: Test-time Adaptive Learning for On-the-Fly Category Discovery](talon.md)

📦 模型压缩

提出 TALON，首次将测试时自适应（TTA）框架引入 On-the-Fly Category Discovery 任务——通过语义感知的原型更新和稳定的编码器自适应，让模型在推理阶段持续从未标注数据流中学习新类别，同时用 margin-aware logit calibration 预留嵌入空间，在 7 个基准上大幅超越 hash-based SOTA。

---

### [Controllable Complex Human Motion Video Generation via Text-to-Skeleton Cascades](text-skeleton-cascade.md)

🎨 图像生成

提出两阶段级联框架生成复杂人体动作视频：第一阶段用自回归 Transformer 从文本生成 2D 骨架序列，第二阶段用 DINO-ALF（多层自适应融合）外观编码器驱动 pose-conditioned 视频扩散模型，在翻跟头、武术等复杂动作上显著优于现有方法。

---

### [Reading ≠ Seeing: 诊断并弥合 VLM 中的排版感知差距](typo-vlm.md)

📄 多模态 / VLM

揭示了当前 VLM 的"排版盲"现象——能完美阅读文字内容却无法感知其视觉呈现（字体、字号、字重、颜色），构建了 FontBench 基准系统诊断这一问题，发现了结构化的感知层次（颜色≫字族>字号>字重），并证明 LoRA 微调可部分缓解但字重感知需要架构层面创新。

---

### [UIS-Digger: Towards Comprehensive Research Agent Systems for Real-world Unindexed Information Seeking](uis-digger.md)

🗣️ LLM/NLP

发现并形式化"未索引信息检索（UIS）"问题——搜索引擎无法直接索引的信息（动态页面/嵌入文件/深层链接），构建首个 UIS-QA benchmark（110 条专家标注 QA 对），并提出 UIS-Digger 四 agent 协作框架（双模浏览器+文件解析+SFT/RFT 两阶段训练），用 ~30B 参数模型达到 27.27% 超越 O3+GPT-4.1 驱动的系统。

---
