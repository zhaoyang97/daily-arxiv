# 📅 2026-03-24 精选笔记

> 共 **15** 篇

---

### [3DCity-LLM: Empowering Multi-modality Large Language Models for 3D City-scale Perception and Understanding](3dcity-llm.md)

🧩 多模态/VLM / 3D理解 / 城市级感知

提出 3DCity-LLM，将多模态 LLM 扩展到 3D 城市级感知：通过粗到细四分支编码（文本/物体/关系/场景）处理城市尺度下数千异质物体的空间关系，构建 120 万样本的 3DCity-LLM-1.2M 数据集覆盖 7 类任务，在 BLEU-4（30.64）和逻辑性（7.33/10）上超越 City-VLM。

---

### [AeroScene: Progressive Scene Synthesis for Aerial Robotics](aeroscene.md)

🧊 3D视觉 / 场景生成 / 无人机

提出 AeroScene，面向无人机仿真的层次化 3D 场景生成模型：通过可学习的 tokenizability 分数将物体路由到粗/细分支 + 跨尺度渐进注意力（top-down/bottom-up 交替）+ 碰撞/一致性/语义三重引导，在自建 1016 场景数据集上碰撞率 6.2%，无人机导航成功率 91%。

---

### [CoMaTrack: Competitive Multi-Agent Game-Theoretic Tracking with Vision-Language-Action Models](comatrack.md)

🎬 视频理解 / 具身智能 / 多智能体

将具身视觉追踪（EVT）从单智能体模仿学习转变为多智能体对抗博弈 RL：tracker 和 opponent 在动态对抗环境中共同进化，用 3B VLM 超越所有 7B 模型的 SOTA（STT 92.1%, DT 74.2%, AT 57.5%），并发布首个对抗式 EVT benchmark。

---

### [E3Flow: Efficient Hybrid SE(3)-Equivariant Visuomotor Flow Policy via Spherical Harmonics](e3flow.md)

🧊 3D视觉 / 机器人操作 / 等变学习

首次统一 SE(3) 等变学习和 rectified flow，提出 E3Flow：用球谐函数保证旋转等变性 + Feature Enhancement Module 融合点云和图像 + flow matching 实现 7× 快速推理，在 MimicGen 8 任务上达 79% 成功率（+3.12% vs SDP）且推理快 7 倍。

---

### [ForeSea: AI Forensic Search with Multi-modal Queries for Video Surveillance](foresea.md)

🎬 视频理解 / 监控分析 / VideoRAG

提出 ForeSea，一个面向监控视频的多模态 RAG 系统（人物跟踪→多模态嵌入→VideoLLM 推理），以及 ForeSeaQA——首个支持图文混合查询+时间戳定位的监控视频 QA benchmark（1041 问题/6 子任务），在准确率（66.0%）和时间 IoU（13.6%）上均超越现有 VideoRAG 方法。

---

### [GeoTikzBridge: Advancing Multimodal Code Generation for Geometric Perception and Reasoning](geotikzbridge.md)

🧩 多模态/VLM / 几何推理 / 代码生成

提出 GeoTikzBridge，一个几何图像到 TikZ 代码的生成框架：通过迭代自精炼从 145K 种子对扩展到 250 万高质量几何图-代码对（CLIP 过滤+局部化代码变换增强），构建 GeoTikz-Base (2.5M) 和 GeoTikz-Instruct (419K) 数据集，InternVL3-78B 达 0.860 CLIP-S / 92.3% 代码成功率，即插即用集成下游任务。

---

### [I3DM: Implicit 3D-aware Memory Retrieval and Injection for Consistent Video Scene Generation](i3dm.md)

🧊 3D视觉 / 视频生成 / 场景一致性

提出 I3DM，用隐式 3D 感知的记忆检索+注入机制解决长视频场景重访时的"转头即忘"问题：利用预训练 NVS 模型的中间特征评估视角相关性（无需显式 3D 重建），贪心最大覆盖算法选互补帧，联合微调 NVS+DiT 注入对齐记忆，在 Re10K 上 PSNR 24.73dB（+8.7dB vs WorldPlay）。

---

### [InterDyad: Interactive Dyadic Speech-to-Video Generation by Querying Intermediate Visual Guidance](interdyad.md)

🎬 视频理解 / 数字人 / 多人对话生成

提出 InterDyad，一个双人对话视频生成框架：通过 Interactivity Injector 注入参考视频的运动先验，MetaQuery 模态对齐机制将对话语音映射到交互模式空间，RoDG 解决极端头部姿态下的唇同步问题，在视觉质量、唇同步和新提出的交互指标上全面超越 MultiTalk/InfiniteTalk/LongCat。

---

### [MultiCam: On-the-fly Multi-Camera Pose Estimation Using Spatiotemporal Overlaps of Known Objects](multicam.md)

🧊 3D视觉 / AR / 相机位姿估计

提出 MultiCam，一个无标记的多相机位姿估计系统：利用场景中已知物体的时空视野重叠构建动态场景图，通过物体级 bundle adjustment 联合优化相机和物体位姿，在 YCB-V 和 T-LESS 数据集上超越现有方法，并发布了首个支持时序视野重叠的多相机多物体位姿数据集。

---

### [PEPO: Rethinking Token-Level Policy Optimization for Multimodal Chain-of-Thought](pepo.md)

🧩 多模态/VLM / LLM推理 / 强化学习

提出 PEPO（Perception-Exploration Policy Optimization），通过 token 级视觉感知先验（隐状态与视觉 token 的余弦相似度）和熵引导探索信号的自适应融合，重新加权 GRPO 策略梯度，在几何/视觉推理/视觉定位等任务上比标准 GRPO 提升 +3.67%，首次揭示多模态 CoT 中视觉锚定和推理探索的互补角色。

---

### [SMSP: A Plug-and-Play Strategy of Multi-Scale Perception for MLLMs to Perceive Visual Illusions](smsp.md)

🧩 多模态/VLM / 视觉感知 / 鲁棒性

发现 MLLM 在隐藏模式视觉错觉（如隐字画）上严重失败的根因是高频注意力偏置，提出 SMSP：通过 FFT 低通滤波（模拟眯眼）+ 空间缩放（模拟远距离观看）的即插即用感知调整策略，将 Qwen3-VL-8B 准确率从 13% 提升到 84%（+71%），无需任何重训练。

---

### [SpecEyes: Accelerating Agentic Multimodal LLMs via Speculative Perception and Planning](speceyes.md)

🧩 多模态/VLM / LLM效率 / Agentic AI

提出 SpecEyes，将投机推理从 token 级提升到 agent 级：四阶段 pipeline（大模型判断工具必要性→小模型无状态投机→认知门控验证→失败回退 agentic 路径），在 V* Bench/HR-Bench/POPE 上实现 1.1-3.35× 加速且保持甚至提升准确率（+6.7%），通过异构并行实现吞吐量倍增。

---

### [TreeTeaming: Autonomous Red-Teaming of Vision-Language Models via Hierarchical Strategy Exploration](treeteaming.md)

🧩 多模态/VLM / AI安全 / 红队测试

提出 TreeTeaming，首个自主进化的 VLM 红队框架：LLM 编排器动态扩展层次化策略树（探索新分支或深化已有路径），配合 11 种多模态工具的执行器 + 一致性检查器，在 12 个 VLM 上 11 个取得 SOTA 攻击成功率（GPT-4o 87.6%），发现超越已知公开越狱策略的新攻击范式。

---

### [UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation](unigrpo.md)

🎨 图像生成 / 强化学习 / 多模态统一模型

提出 UniGRPO，将 "Prompt → 推理 → 生成图像" 的多模态交错生成建模为统一 MDP，用 GRPO 联合优化文本推理和 Flow Matching 图像生成策略，去掉 CFG + 用速度场 MSE 正则替代 latent KL，在 TA 和 GenEval 上取得 SOTA（0.8381 / 0.90）。

---

### [ViBe: Ultra-High-Resolution Video Synthesis Born from Pure Images](vibe.md)

🎨 图像生成 / 视频生成 / 高分辨率

提出 ViBe，一个纯图像训练的超高分辨率视频生成框架：通过 Relay LoRA（两阶段解耦模态对齐与空间外推）+ GCLFA（全局粗粒度+局部细粒度注意力）+ HFATO（高频感知训练目标）将 Wan2.2 等视频 DiT 从 480P 升级到 4K，在 VBench 上超越了使用高分辨率视频数据训练的 SOTA（74.4 vs 73.6）。

---
