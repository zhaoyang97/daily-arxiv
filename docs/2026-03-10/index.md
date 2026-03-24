# 📅 2026-03-10 精选笔记

> 共 **20** 篇

---

### [Ego: Embedding-Guided Personalization of Vision-Language Models](ego-vlm.md)

🧩 多模态/VLM / 个性化

提出 Ego，一种无需训练的 VLM 个性化方法——利用模型自身的注意力机制从参考图像中提取最具代表性的视觉 token 子集作为概念记忆，推理时通过 in-context 软提示使模型识别和推理个性化概念。在单/多概念、视频个性化场景中均达到 SOTA，且仅需 1.4 秒完成概念引入。

---

### [EXPLORE-Bench: Egocentric Scene Prediction with Long-Horizon Reasoning](explore-bench.md)

🤖 机器人 / 具身智能

提出 EXPLORE-Bench 基准——给定初始场景图像和一系列原子动作描述（平均 113 步），要求 MLLM 预测所有动作执行后的最终场景状态。包含 1,157 个实例，在物体/属性/关系三层级做细粒度评估。实验揭示 GPT-5.2、Gemini-3 等 MLLM 与人类差距显著。

---

### [InfiniteDance: Scalable 3D Dance Generation Towards in-the-wild Generalization](infinitedance.md)

🎨 图像生成 / 3D动作生成

提出 InfiniteDance 框架，从数据和模型两端同时 scale up 3D 舞蹈生成：(1) 自动化管线从单目视频重建 100.69 小时高质量 3D 舞蹈数据集（含 30 种舞种），核心是 Foot Restoration Diffusion Model 修复脚部伪影；(2) ChoreoLLaMA 基于 LLaMA 架构 + RAG 检索增强 + Cadence-MoE 节奏专家混合，实现对野外音乐的泛化舞蹈生成。

---

### [IntroSVG: Introspective Generator-Critic Framework for Text-to-SVG Generation](introsvg.md)

🎨 多模态/VLM / 图像生成

提出 IntroSVG，用统一 VLM 同时担任"生成器"和"评审者"，通过 SFT 学会生成 SVG 和评估渲染结果 → DPO 对齐偏好 → 推理时执行"生成-评审-修正"迭代循环，实现高质量 Text-to-SVG 生成。在 FID 和美学评分上超越 GPT-5/Gemini 2.5 Pro 等闭源模型。

---

### [LLM-MRD: LLM-Guided Multi-View Reasoning Distillation for Fake News Detection](llm-mrd.md)

🧩 多模态/VLM / 假新闻检测

提出 LLM-MRD，一个教师-学生框架：LLM 教师从文本/视觉/跨模态三个视角生成深度推理链作为监督信号，通过校准蒸馏（Calibration Distillation）将推理知识高效转移到轻量学生模型，在三个多模态假新闻检测基准上平均提升 ACC 5.19%、F1-Fake 6.33%。

---

### [MDTrack: Modality-Aware Fusion and Decoupled Temporal Propagation for Multi-Modal Object Tracking](mdtrack.md)

🎬 视频理解 / 多模态跟踪

提出 MDTrack，通过 MoE（Mixture of Experts）实现模态感知融合（为 IR/Event/Depth/RGB 分配专用专家）+ 双 SSM（State Space Model）实现解耦时序传播（RGB 和 X 模态各自独立更新隐状态），在 5 个多模态跟踪基准上达到 SOTA。

---

### [NanoBench: A Multi-Task Benchmark Dataset for Nano-Quadrotor System Identification, Control, and State Estimation](nanobench.md)

🤖 机器人 / 纳米四旋翼

发布 NanoBench——首个在商用纳米级四旋翼（Crazyflie 2.1, 27g）上同时提供执行器命令、控制器内部状态和估计器输出（配合毫米级 Vicon 地面真值）的开源多任务基准数据集，包含 170+ 飞行轨迹，定义了系统辨识、控制器评测和状态估计三种标准化评估协议。

---

### [OddGridBench: Exposing the Lack of Fine-Grained Visual Discrepancy Sensitivity in MLLMs](oddgridbench.md)

🧩 多模态/VLM / 基准评测

提出 OddGridBench 基准——1,400+ 张网格图像中需找出在颜色/大小/旋转/位置上有细微差异的"odd one"，揭示所有 MLLM（包括 GPT-5、Gemini 2.5 Pro）在细粒度视觉差异感知上远低于人类（68% vs 87%）。进而提出 OddGrid-GRPO（课程学习 + 距离感知奖励）将 Qwen3-VL-2B 从 17% 提升到 83%。

---

### [Benchmarking Political Persuasion Risks Across Frontier Large Language Models](political-persuasion.md)

🗣️ LLM/NLP / AI安全

通过两项大规模调查实验（N=19,145）对比 7 个前沿 LLM 的政治说服力，发现现代 LLM 已超越传统人类竞选广告的说服效果；Claude 系列最具说服力，Grok 最弱；信息型提示的效果高度依赖模型选择。

---

### [VLM-Loc: Localization in Point Cloud Maps via Vision-Language Models](vlm-loc.md)

🧊 3D视觉 / 点云定位

提出 VLM-Loc，利用大型视觉语言模型（VLM）进行文本到点云（T2P）定位——将点云转为 BEV 图像 + 场景图作为结构化输入，引入部分节点分配（PNA）机制显式关联文本线索与场景图节点，实现可解释的空间推理定位。在自建 CityLoc 基准上 Recall@5m 超越前 SOTA CMMLoc 14.20%。

---

### [Does the Question Really Matter? Training-Free Data Selection for Vision-Language SFT](cvs-data-selection.md)

🧩 多模态/VLM / 数据选择

提出 CVS（Conditional Verdict Shift），一种无需训练的 VLM 数据选择方法——利用冻结 VLLM 比较加入问题前后对答案有效性判断的变化，筛选真正需要视觉-语言联合推理的样本。在 Vision-Flan 上仅用 10%/15% 数据超越全量训练 3.5%/4.8%。

---

### [Evolving Prompt Adaptation for Vision-Language Models](evolving-prompt.md)

🧩 多模态/VLM / 提示学习

提出动态演化提示自适应方法，通过演化算法在测试时动态搜索最优文本提示以应对分布漂移，无需目标域数据标签即可实现高效模型适应。

---

### [MORE-R1: Guiding LVLM for Multimodal Object-Entity Relation Extraction via Stepwise Reasoning with RL](more-r1.md)

🧩 多模态/VLM / 信息抽取

将多模态对象-实体关系抽取形式化为 RL 问题，通过 SFT 冷启动 + GRPO 优化 + 渐进采样策略，显著提升 LVLM 在关系抽取上的推理能力和可扩展性。

---

### [Test-time Ego-Exo-centric Adaptation for Action Anticipation](ego-exo-adaptation.md)

🤖 机器人 / 跨视角适应

首次定义测试时自我-异我视角适应任务，通过多标签原型增长和双线索一致性约束，实现源视角训练模型在目标视角的在线自适应。

---

### [FrameDiT: Diffusion Transformer with Frame-Level Matrix Attention for Efficient Video Generation](framedit.md)

🎨 图像生成 / 视频生成

提出帧级矩阵注意力——将每帧表示为矩阵而非展平 token，通过 Frobenius 内积计算帧间相似度，实现全 3D 注意力的表达能力与局部注意力的计算效率平衡。

---

### [VQ-Memory: Beyond Short-Horizon for Robust Long-Horizon Manipulation](vq-memory.md)

🤖 机器人 / 强化学习

提出 VQ-Memory——通过 VQ-VAE 将关节状态历史编码为离散语义 token 并聚类压缩，使 VLA 模型能处理长视野非马尔可夫操纵任务。配套发布 RuleSafe 基准。

---

### [Latent-DARM: Bridging Discrete Diffusion And Autoregressive Models For Reasoning](latent-darm.md)

🧠 LLM推理 / 多智能体

设计规划官-执行官框架，通过学习投影网络在隐空间直接连接扩散模型和自回归模型，以仅 2.2% 的 token 预算达到 DeepSeek-R1 的竞争性能。

---

### [RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning](rubicap.md)

🎨 图像生成 / 密集字幕

通过动态合成图像特定的评估准则（rubrics）指导 GRPO 强化学习，使 7B 模型在密集字幕 CapArena 上超越 GPT-4V 和人类专家标注。

---

### [Chain of Event-Centric Causal Thought for Physically Plausible Video Generation](causal-thought-video.md)

🎨 图像生成 / 视频生成

将物理现象建模为因果事件序列，用物理公式驱动事件分解 + 语义-视觉双提示，使扩散模型生成包含逐步物理演变的合理视频。

---

### [Kinodynamic Motion Retargeting for Humanoid Locomotion](kinodynamic-motion.md)

🤖 机器人 / 运动规划

将人类运动重定向形式化为多接触整体轨迹优化，集成 GRF 约束消除脚滑/穿地等物理不一致性，显著提升下游模仿学习效率。

---
