# 📅 2026-03-12 精选笔记

> 共 **20** 篇

---

### [Ada3Drift: Adaptive Training-Time Drifting for One-Step 3D Visuomotor Robotic Manipulation](ada3drift.md)

🧊 3D视觉 / 机器人操作

提出 Ada3Drift，将扩散策略的迭代精炼从推理时转移到训练时——通过训练时漂移场（吸引预测到专家模式 + 排斥模式平均）+ sigmoid 调度 + 多温度聚合，实现 1 NFE 单步 3D 视觉运动策略，在 Adroit/Meta-World/RoboTwin 和真机上达到 SOTA 且比扩散策略快 10×。

---

### [DocSage: An Information Structuring Agent for Multi-Doc Multi-Entity Question Answering](docsage.md)

🦾 LLM Agent / 多文档QA

提出 DocSage，一个面向多文档多实体问答（MDMEQA）的端到端 Agent 框架——通过动态 Schema 发现（ASK 算法交互式推断查询特定的最小可连接模式）→ 逻辑感知的结构化抽取（CLEAR 机制跨记录逻辑一致性校验）→ Schema 引导的关系推理（SQL 驱动的精确事实定位和多跳推理），在两个 MDMEQA benchmark 上超越 SOTA 长上下文 LLM 和 RAG 系统 27%+。

---

### [DVD: Deterministic Video Depth Estimation with Generative Priors](dvd.md)

🧊 3D视觉 / 深度估计

提出 DVD，首个将预训练视频扩散模型确定性地转化为单步深度回归器的框架，通过复用扩散时间步作为结构锚点 + 隐空间流形矫正（LMR）恢复锐利边界 + 全局仿射一致性实现无缝长视频推理，零样本 SOTA 且仅需基线方法 1/163 的任务特定数据。

---

### [DyWeight: Dynamic Gradient Weighting for Few-Step Diffusion Sampling](dyweight.md)

🎨 图像生成 / 扩散模型加速

提出 DyWeight，一种基于学习的多步 ODE 求解器，通过放松经典数值约束（∑w≠1）实现动态梯度加权 + 隐式时间校准（time shifting & scaling），将梯度聚合与步长调节隐式耦合，仅需末端监督即可单轮优化——CIFAR-10 上 5 NFE 达到 3.02 FID（iPNDM: 7.77, S4S-Alt: 3.73），FLUX.1-dev 上全面超越 DPM-Solver++ 和 iPNDM。

---

### [Controllable Egocentric Video Generation via Occlusion-Aware Sparse 3D Hand Joints](ego-video-3d-hand.md)

🎬 视频理解 / 第一人称视频生成

提出一种以稀疏 3D 手部关节为控制信号的第一人称视频生成框架，通过遮挡感知的源特征提取（惩罚被遮挡关节的不可靠信号）+ 3D 深度加权的目标帧特征传播 + 3D 几何嵌入注入，在严重遮挡下实现高保真手部控制，并天然支持跨具身（人手→机械手）泛化。

---

### [EndoCoT: Scaling Endogenous Chain-of-Thought Reasoning in Diffusion Models](endocot.md)

🎨 图像生成 / 扩散模型推理

提出 EndoCoT，通过在 MLLM 中迭代精炼隐式思维状态并桥接到 DiT 去噪过程，实现扩散模型内生的链式思维推理，在 Maze/TSP/Sudoku/VSP 四个视觉推理 benchmark 上平均 92.1% 准确率，超越最强基线 DiffThinker 8.3 个百分点。

---

### [Explicit Logic Channel for Validation and Enhancement of MLLMs on Zero-Shot Tasks](explicit-logic.md)

📄 多模态VLM / 可信推理

提出显式逻辑通道（ELC），与 MLLM 的隐式黑箱推理并行运行——用 LLM 提取事实/关系 + VFM 视觉定位 + 概率逻辑推理，无需标注即可通过双通道一致率（CR）评估和选择模型，融合两通道还能提升零样本 VLC 任务性能。

---

### [GRADE: Benchmarking Discipline-Informed Reasoning in Image Editing](grade.md)

🎨 图像生成 / Benchmark

提出 GRADE，首个面向学科知识推理的图像编辑 benchmark，涵盖 10 个学科 520 个样本，通过学科推理/视觉一致性/逻辑可读性三维评估协议揭示当前 20 个 SOTA 模型在知识密集型编辑场景下的显著不足。

---

### [HomeSafe-Bench: Evaluating VLMs on Unsafe Action Detection for Household Embodied Agents](homesafe-bench.md)

🎬 视频理解 / 具身安全

提出 HomeSafe-Bench，首个面向家庭场景具身智能体的不安全动作检测 benchmark，包含 438 个跨 6 个功能区域的案例，并提出 HD-Guard 层级双脑架构（轻量 FastBrain 高频筛 + 异步 SlowBrain 深度推理）实现实时安全监控。

---

### [Beyond Single-Sample: Reliable Multi-Sample Distillation for Video Understanding](multi-sample-distill.md)

🎬 视频理解 / 知识蒸馏

提出 R-MSD（Reliable Multi-Sample Distillation），针对视频 LVLM 蒸馏中教师采样方差导致的监督噪声问题，通过多样本质量感知信号匹配 + 在线 critic 对抗蒸馏，4B 学生在 VideoMME +1.5%、Video-MMMU +3.2%、MathVerse +3.6%。

---

### [MV-SAM3D: Adaptive Multi-View Fusion for Layout-Aware 3D Generation](mv-sam3d.md)

🧊 3D视觉 / 3D生成

提出 MV-SAM3D，一个免训练的多视角一致 3D 生成框架——通过 Multi-Diffusion 融合多视角速度预测（注意力熵加权估计观察置信度 + DDA 光线追踪几何可见性加权）+ 物理感知优化（生成中布局注入 + 后处理姿态优化），在 GSO-30 上 2 视角 CD 20.2（EscherNet: 21.5），5 视角 17.3。

---

### [One-Step Flow Policy: Self-Distillation for Fast Visuomotor Policies](one-step-flow-policy.md)

🎨 图像生成 / 机器人策略

提出 One-Step Flow Policy (OFP)，通过从零开始的自蒸馏框架（自一致性 loss + 自引导正则化 + warm-start），无需预训练教师即可实现单步动作生成——在 56 个仿真操作任务上 1-NFE 平均成功率 71.6%，超越 100 步 DP3 基线（66.4%），推理仅需 17.58 ms（加速 183×）。

---

### [OSCBench: Benchmarking Object State Change in Text-to-Video Generation](oscbench.md)

🎬 视频理解 / T2V Benchmark

提出 OSCBench，首个专门评估 T2V 生成中物体状态变化（Object State Change）的 benchmark，包含 1,120 个提示覆盖 140 个烹饪场景（常规/新颖/组合），通过 CoT 四维评估揭示即使 Veo-3.1-Fast 在 OSC 准确性上也仅 0.740，开源模型 Open-Sora-2.0 更低至 0.512。

---

### [SoulX-LiveAct: Towards Hour-Scale Real-Time Human Animation with Neighbor Forcing and ConvKV Memory](soulx-liveact.md)

🎨 图像生成 / 人物动画

提出 SoulX-LiveAct，通过 Neighbor Forcing（传播同一扩散步的邻近帧 latent 而非跨步状态）解决 AR 扩散的训练-推理分布不匹配问题，配合 ConvKV Memory（1D 卷积压缩 KV cache）实现恒定内存的小时级视频生成，在 2×H100 上以 20 FPS 实时生成 720×416 人物动画。

---

### [Video Streaming Thinking: VideoLLMs Can Watch and Think Simultaneously](video-streaming-thinking.md)

🎬 视频理解 / 流式推理

提出 Video Streaming Thinking (VST)，让 VideoLLM 在视频播放过程中主动交错生成 CoT 推理（而非等到查询后再推理），通过双记忆系统（短期视觉+长期文本语义）+ 两阶段后训练（SFT+RL）+ 知识图谱数据合成，在 StreamingBench 上达到 79.5%（超越 GPT-4o 6.2%），比 Video-R1 快 15.7 倍。

---

### [VisDoT: Enhancing Visual Reasoning through Human-Like Interpretation Grounding and Decomposition of Thought](visdot.md)

📄 多模态VLM / 图表推理

提出 VisDoT 框架，基于图形感知理论定义四类感知任务（Position/Length/Pattern/Extract），引入分解思维（DoT）提示将复杂视觉问题拆分为感知子问题→逻辑子问题的链式推理，微调 InternVL 在 ChartQA 上提升 11.2%，超越 GPT-4o，且零样本迁移到开放域 VQA 也有效。

---

### [VQQA: An Agentic Approach for Video Evaluation and Quality Improvement](vqqa.md)

🎬 视频理解 / 视频生成评估

提出 VQQA，一个多 Agent 视频评估与质量改进框架——通过三个 Agent（问题生成→视频问答→提示优化）构建闭环，将 VLM 的评估反馈作为"语义梯度"驱动 prompt 迭代优化，无需模型微调，在 T2V-CompBench 上对 CogVideoX-5B 提升 +11.57%（41.89%→53.46%），VBench2 上 +8.43%（41.98%→50.41%）。

---

### [Wasserstein Gradient Flows for Batch Bayesian Optimal Experimental Design](wasserstein-boed.md)

📄 贝叶斯优化 / 实验设计

将批量 BOED 问题提升到概率测度空间，通过熵正则化得到唯一 Gibbs 分布最小化器，推导 mean-field 和 i.i.d. 乘积族的 Wasserstein 梯度流，并用粒子时空离散化 + 双随机蒙特卡洛变体实现可扩展求解。

---

### [WAT: Online Video Understanding Needs Watching Before Thinking](wat.md)

🎬 视频理解 / 在线视频

提出 WAT（Watching Before Thinking），将在线视频理解解耦为查询无关的"观察"阶段（层级记忆：STM 高保真滑窗 + LTM 冗余感知淘汰）和查询触发的"思考"阶段（上下文感知检索 + RACL 对比学习），在 StreamingBench 上达到 77.7%、OVO-Bench 上 55.2%，显著超越现有开源在线 Video LLM。

---

### [WeEdit: A Dataset, Benchmark and Glyph-Guided Framework for Text-centric Image Editing](weedit.md)

🎨 图像生成 / 文本编辑

提出 WeEdit，首个面向图像中文字修改/翻译/重排的系统性方案——基于 HTML 的自动数据生成 pipeline 构建 330K 训练对（覆盖 15 种语言）+ 字形引导微调注入空间内容先验 + 多目标强化学习对齐指令遵循/文字清晰度/背景保持，在多语文字编辑上大幅超越现有开源模型。

---
