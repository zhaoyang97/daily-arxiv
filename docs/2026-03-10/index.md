# 📅 2026-03-10 精选笔记

> 共 **20** 篇

---

### [Chain of Event-Centric Causal Thought for Physically Plausible Video Generation](causal-thought-video.md)

🎨 图像生成 / 视频生成

将物理现象建模为因果关联的事件序列——通过物理公式驱动的事件链推理（PECR）分解物理过程为可控阶段，配合转移感知跨模态提示（TCP）模块逐步生成语义+视觉提示，使扩散模型能生成涵盖逐步物理演变过程的物理合理视频。

---

### [Does the Question Really Matter? Training-Free Data Selection for Vision-Language SFT](cvs-data-selection.md)

🧩 多模态/VLM / 数据选择

提出 CVS（Conditional Verdict Shift），一种无需训练的 VLM 数据选择方法——利用冻结 VLLM 作为评估器，比较加入问题前后模型对答案有效性判断的变化，筛选真正需要视觉-语言联合推理的样本。在 Vision-Flan 上仅用 10%/15% 数据超越全量训练 3.5%/4.8%。

---

### [Test-time Ego-Exo-centric Adaptation for Action Anticipation via Multi-Label Prototype Growing and Dual-Clue Consistency](ego-exo-adaptation.md)

🤖 机器人 / 跨视角适应

首次探索测试时自我-异我视角适应用于动作预测（TE2A3 任务）——提出 DCPGN 框架，通过多标签原型增长模块（ML-PGM，Top-K 伪标签 + 置信度加权 + 熵优先队列更新记忆库）和双线索一致性模块（DCCM，视觉线索→空间对象 + 文本线索→时序动作进展 + KL 散度约束一致性），在 EgoMe-anti 和 EgoExoLearn 基准上大幅超越现有 TTA 方法。

---

### [Ego: Embedding-Guided Personalization of Vision-Language Models](ego-vlm.md)

🧩 多模态/VLM / 个性化

提出 Ego，一种无需训练的 VLM 个性化方法——利用模型自身的注意力机制从参考图像中提取最具代表性的视觉 token 子集作为概念记忆，推理时通过 in-context 软提示使模型识别和推理个性化概念。在单/多概念、视频个性化场景中均达到 SOTA，且仅需 1.4 秒完成概念引入。

---

### [EvoPrompt: Evolving Prompt Adaptation for Vision-Language Models](evolving-prompt.md)

🧩 多模态/VLM / 提示学习

提出 EvoPrompt，通过"演化轨迹感知"的提示学习范式来防止适配时的灾难性遗忘——核心设计包括：模态共享提示投射器（MPP，统一嵌入空间→层级提示）、增量幅度-方向解耦（冻结早期学到的语义方向，仅训练幅度系数）、特征几何正则化（FGR，强制特征去相关防止表示坍塌）。在 11 个数据集的 base-to-novel 泛化、跨数据集迁移、域泛化和少样本学习中达到 SOTA。

---

### [EXPLORE-Bench: Egocentric Scene Prediction with Long-Horizon Reasoning](explore-bench.md)

🤖 机器人 / 具身智能

提出 EXPLORE-Bench 基准——给定初始场景图像和一系列原子动作描述（平均 113 步），要求 MLLM 预测所有动作执行后的最终场景状态。包含 1,157 个实例，在物体/属性/关系三层级做细粒度评估。实验揭示 GPT-5.2、Gemini-3 等 MLLM 与人类差距显著。

---

### [FrameDiT: Diffusion Transformer with Frame-Level Matrix Attention for Efficient Video Generation](framedit.md)

🎨 图像生成 / 视频生成

提出帧级矩阵注意力机制——将每帧表示为矩阵而非展平 token 序列，通过 Frobenius 内积计算帧间相似度进行时间建模，实现全 3D 注意力的表达能力与局部注意力的计算效率平衡，在多个视频生成基准上达到 SOTA。

---

### [InfiniteDance: Scalable 3D Dance Generation Towards in-the-wild Generalization](infinitedance.md)

🎨 图像生成 / 3D动作生成

提出 InfiniteDance 框架，从数据和模型两端同时 scale up 3D 舞蹈生成：(1) 自动化管线从单目视频重建 100.69 小时高质量 3D 舞蹈数据集（含 30 种舞种），核心是 Foot Restoration Diffusion Model 修复脚部伪影；(2) ChoreoLLaMA 基于 LLaMA 架构 + RAG 检索增强 + Cadence-MoE 节奏专家混合，实现对野外音乐的泛化舞蹈生成。

---

### [IntroSVG: Introspective Generator-Critic Framework for Text-to-SVG Generation](introsvg.md)

🎨 多模态/VLM / 图像生成

提出 IntroSVG，用统一 VLM 同时担任"生成器"和"评审者"，通过 SFT 学会生成 SVG 和评估渲染结果 → DPO 对齐偏好 → 推理时执行"生成-评审-修正"迭代循环，实现高质量 Text-to-SVG 生成。在 FID 和美学评分上超越 GPT-5/Gemini 2.5 Pro 等闭源模型。

---

### [Kinodynamic Motion Retargeting for Humanoid Locomotion via Multi-Contact Whole-Body Trajectory Optimization](kinodynamic-motion.md)

🤖 机器人 / 运动规划

提出 KDMR（KinoDynamic Motion Retargeting）框架——将人类运动重定向形式化为多接触整体轨迹优化问题，集成地面反作用力（GRF）约束，通过运动学优化→动力学优化两阶段消除脚滑/穿地等物理不一致性，显著提升下游模仿学习的样本效率。

---

### [Latent-DARM: Bridging Discrete Diffusion And Autoregressive Models For Reasoning](latent-darm.md)

🧠 LLM推理 / 多智能体

提出 Latent-DARM——首个在隐空间（而非文本空间）桥接离散扩散语言模型（DDLM，作为规划者）和自回归模型（ARM，作为执行者）的多智能体协作框架。通过训练 Linear-GELU-Linear 投影器将 DDLM 最后隐层特征映射到 ARM 嵌入空间，让 DDLM 的全局推理能力和 ARM 的顺序流畅性互补，在 DART-5 上从 27% 提升到 36%，在 AIME 2024 上从 0% 提升到 14%，且仅使用 DeepSeek-R1 2.2% 的 token 预算。

---

### [LLM-MRD: LLM-Guided Multi-View Reasoning Distillation for Fake News Detection](llm-mrd.md)

🧩 多模态/VLM / 假新闻检测

提出 LLM-MRD，一个教师-学生框架：LLM 教师从文本/视觉/跨模态三个视角生成深度推理链作为监督信号，通过校准蒸馏（Calibration Distillation）将推理知识高效转移到轻量学生模型，在三个多模态假新闻检测基准上平均提升 ACC 5.19%、F1-Fake 6.33%。

---

### [MDTrack: Modality-Aware Fusion and Decoupled Temporal Propagation for Multi-Modal Object Tracking](mdtrack.md)

🎬 视频理解 / 多模态跟踪

提出 MDTrack，通过 MoE（Mixture of Experts）实现模态感知融合（为 IR/Event/Depth/RGB 分配专用专家）+ 双 SSM（State Space Model）实现解耦时序传播（RGB 和 X 模态各自独立更新隐状态），在 5 个多模态跟踪基准上达到 SOTA。

---

### [MORE-R1: Guiding LVLM for Multimodal Object-Entity Relation Extraction via Stepwise Reasoning with Reinforcement Learning](more-r1.md)

🧩 多模态/VLM / 信息抽取

首次将 LVLM 成功应用于多模态对象-实体关系抽取（MORE）任务——通过两阶段训练（GPT-4o 生成推理链 SFT 冷启动 → GRPO 强化学习 + 渐进样本混合策略），让 Qwen2.5-VL-7B 学会 6 步结构化推理来抽取跨模态关系，F1 Score 达到 67.80%，超越前 SOTA REMOTE 6.1%。

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

### [RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning](rubicap.md)

🎨 图像生成 / 密集字幕

提出 RubiCap，通过 LLM 自动合成**样本特定的评估准则（rubrics）**解决密集字幕中 RL 的验证瓶颈——教师委员会（5 个 VLM）提取共识 → 诊断学生缺陷 → 生成分级二元准则 → LLM 裁判逐条评分产生多维度 RL 奖励。7B 模型在盲排中 rank-1 比例超过 72B 和 32B 前沿模型，幻觉率最低；3B 模型作为标注器生成的数据做 VLM 预训练效果优于 GPT-4V。

---

### [VLM-Loc: Localization in Point Cloud Maps via Vision-Language Models](vlm-loc.md)

🧊 3D视觉 / 点云定位

提出 VLM-Loc，利用大型视觉语言模型（VLM）进行文本到点云（T2P）定位——将点云转为 BEV 图像 + 场景图作为结构化输入，引入部分节点分配（PNA）机制显式关联文本线索与场景图节点，实现可解释的空间推理定位。在自建 CityLoc 基准上 Recall@5m 超越前 SOTA CMMLoc 14.20%。

---

### [Beyond Short-Horizon: VQ-Memory for Robust Long-Horizon Manipulation in Non-Markovian Simulation Benchmarks](vq-memory.md)

🤖 机器人 / 强化学习

提出 RuleSafe 基准（LLM 生成的多阶段解锁规则，产生非马尔可夫长视野操纵任务）和 VQ-Memory 模块——通过 VQ-VAE 将关节状态历史编码为离散 token 再做 K-means 聚类（256→4 码字，~20 倍压缩），提供紧凑且噪声鲁棒的时序记忆表示，在 DP3/RDT/CogACT/π0 等 4 种策略上一致提升长视野操纵成功率（如 π0 从 0% 提升到 45%）。

---
