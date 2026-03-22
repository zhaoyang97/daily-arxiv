# 📅 2026-03-20 精选笔记

> 共 **20** 篇

---

### [AgroCoT: A Chain-of-Thought Benchmark for Evaluating Reasoning in Vision-Language Models for Agriculture](agrocot.md)

📄 多模态VLM / 农业AI

构建首个农业领域多模态 CoT 推理 benchmark（4759 对 VQA + 人工精修推理链），覆盖 5 大维度 15 类任务，系统评估 30 个 VLM（含 5 个闭源），发现 GPT-4.1 整体最强（SS 88.59, CoT Quality 49.78），开源模型推理能力普遍不足，GPT-5 因推理冗长反而低于 GPT-4.1。

---

### [AutoScreen-FW: An LLM-based Framework for Resume Screening](autoscreen-fw.md)

🦾 LLM Agent / NLP应用

提出 AutoScreen-FW，用开源 LLM（Qwen3-8B/Llama-3.1-8B）+ few-shot ICL 实现简历筛选，通过 clustering-based 样本选择策略使 Qwen3-8B 超越 GPT-5-nano 达 10.8%，同时保护数据隐私且提速 48.7%。

---

### [CubiD: Cubic Discrete Diffusion for Discrete Visual Generation on High-Dimensional Representations](cubid.md)

🎨 图像生成

提出 CubiD，在高维预训练表征（768-1024 维）上做细粒度 masked diffusion，通过 dimension-wise 量化保留语义丰富度，per-element masking 跨整个 3D tensor（h×w×d）独立 mask，在 ImageNet-256 上以 1.88 FID 达到离散生成 SOTA。

---

### [CycleCap: Improving VLMs Captioning Performance via Self-Supervised Cycle Consistency Fine-Tuning](cyclecap.md)

📄 多模态VLM

提出 CycleCap，用循环一致性作为自监督奖励（图像→Caption→重建图像，DreamSim 衡量一致性）配合 GRPO 微调 VLM captioning 能力，无需标注数据，在 CompreCap/CAPability/CapsBench 上稳定提升 1.3-3.2 分，且减少幻觉。

---

### [DuoTeach: Dual Role Self-Teaching for Coarse-to-Fine Decision Coordination in Vision-Language Models](duoteach.md)

🧠 多模态VLM / LLM推理

揭示 VLM 在层级分类中严重的跨层不一致问题（祖先-后代链条无效），提出 DuoTeach 自蒸馏框架——同一 VLM 既做教师（逐层条件推理）又做学生（单次调用预测完整路径），在 ImageNet-Animal 上 DWPA₀.₉₅ 从 0.69% 飙升至 30.93%，且在未见分类体系上零样本迁移保持增益。

---

### [FLAC: Few-shot Acoustic Synthesis with Multimodal Flow Matching](flac.md)

🧊 3D视觉 / 多模态

提出 FLAC，基于 flow matching 的概率生成模型，用声学参考 RIR + 空间位置 + 全景深度图三路条件信息在 few-shot 场景下合成声学一致的房间脉冲响应——仅用 1-shot 即可超越现有方法的 8-shot 表现（T60 误差 9.95% vs xRIR 的 14.47%）。

---

### [GenVideoLens: Where LVLMs Fall Short in AI-Generated Video Detection?](genvideolens.md)

🛡️ 多模态VLM / AI安全

构建 GenVideoLens 细粒度 benchmark（400 合成 + 100 真实视频，15 个真实性维度，6000+ 专家标注），系统诊断 11 个 LVLM 在 AI 生成视频检测中的薄弱环节：感知线索尚可，但光学一致性、物理交互和时序因果推理极差，且模型几乎不利用时序信息。

---

### [GriDiT: Factorized Grid-Based Diffusion for Efficient Long Image Sequence Generation](gridit.md)

🎨 图像生成 / 视频理解

提出 GriDiT 两阶段分解生成框架——Stage 1 将帧序列排成 K×K 网格图在低分辨率下建模帧间关联，Stage 2 逐帧超分重建——在 CT-RATE 医学影像上比 GenerateCT 快 3.4× 且 FVD 更优（998.43 vs 1092.3），支持 1024 帧长序列生成。

---

### [Harm or Humor: A Multimodal, Multilingual Benchmark for Overt and Covert Harmful Humor](harm-or-humor.md)

🛡️ 多模态VLM / AI安全

构建首个多模态（文本 3K + 图像 6K + 视频 1.2K）、多语言（英语/阿拉伯语）的有害幽默检测 benchmark，区分安全笑话、显式有害和隐式（隐蔽）有害三类，发现闭源模型显著优于开源模型，且阿拉伯语性能普遍落后英语。

---

### [Infinity-RoPE: Action-Controllable Infinite Video Generation Emerges From Autoregressive Self-Rollout](infinity-rope.md)

🎨 视频理解 / 图像生成

提出 Infinity-RoPE，通过 Block-Relativistic RoPE（移动参考系时序编码）+ KV Flush（仅保留 2 token 实现即时 prompt 响应）+ RoPE Cut（受控时序断裂实现场景转换），在 Wan2.1-T2V 上实现训练无关的无限长视频生成——60 秒视频 VBench Overall 0.8298（SOTA），12× 超训练长度且动态度保持 0.52（vs baseline 0.32-0.36）。

---

### [MLA: A Multisensory Language-Action Model for Multimodal Understanding and Forecasting in Robotic Manipulation](mla.md)

🤖 机器人 / 多模态VLM

提出 MLA，编码器无关的多感官 VLA 模型，通过 token 级对比学习将 2D 图像、3D 点云和触觉信号统一对齐到 LLM 嵌入空间，加上未来多感官状态预测后训练，在真实世界和 RLBench 上分别超越 π₀ +12%/+16%。

---

### [MMSearch-Plus: Benchmarking Provenance-Aware Search for Multimodal Browsing Agents](mmsearch-plus.md)

🦾 LLM Agent / 多模态VLM

构建 MMSearch-Plus benchmark（311 个需要"时空外推"的多模态搜索任务），要求 agent 从图像中的细粒度视觉线索推断像素之外的事实（如日期/事件/地点），最强模型 o3 仅达 37.6%——提出 Set-of-Mark 区域裁剪模块持续带来 +3.9% 提升。

---

### [Mobile-VideoGPT: Fast and Accurate Model for Mobile Video Understanding](mobile-videogpt.md)

🎬 视频理解 / LLM效率

设计 Mobile-VideoGPT，双编码器架构（CLIP-B/16 空间特征 + VideoMamba-M 时序特征）+ 高效 token 投射器 + Qwen-2.5 0.5B SLM，仅 0.5B 参数/1GB 模型/3GB 显存，在 Jetson Orin Nano 上 7.3 tokens/sec，ActivityNet-QA 上 51.6%（超 LLaVA-OneVision-0.5B）。

---

### [Modality Equilibrium Matters: Minor-Modality-Aware Adaptive Alternating for Cross-Modal Memory Enhancement](modality-equilibrium.md)

⚡ 多模态VLM / LLM效率

提出 Equilibrium Deviation Metric (EDM) 量化模态不平衡程度，理论证明弱→强优化顺序在交替训练中收敛界最紧，设计 EDM 引导的动态交替训练 + 跨模态记忆模块，在 CREMA-D 上 +3.36%、Kinetics-400 上 +3.51% SOTA，且在缺失模态条件下保持鲁棒。

---

### [Multi-Scale Distillation for RGB-D Anomaly Detection on the PD-REAL Dataset](multi-scale-distill.md)

🧊 3D视觉 / 异常检测

构建首个低成本真实世界 RGB-D 异常检测数据集 PD-REAL（Play-Doh 手工物体，15 类 × 6 种异常 × 3 光照，3500+ 样本），提出多尺度教师-学生蒸馏框架用于 RGB-D 异常检测，Mean AUPRO 达 0.952。

---

### [Multimodal OCR: Parse Anything from Documents](multimodal-ocr.md)

📄 多模态VLM / 文档理解

提出 MOCR 范式将文档中的图表、图标、UI 等图形元素从"像素裁剪"升级为"可渲染结构化代码（SVG）"的一等解析目标，通过从头训练 1.2B 视觉编码器 + Qwen2.5-1.5B 解码器的 3B 模型在 olmOCR-Bench 上达到 83.9 SOTA，在 UniSVG 图形解析上以 0.902 超越 Gemini 3 Pro 的 0.735。

---

### [SEAR: Simple and Efficient Adaptation of Visual Geometric Transformers for RGB+Thermal 3D Reconstruction](sear.md)

🧊 3D视觉 / 多模态VLM

提出 SEAR，通过轻量 LoRA 微调（仅 ~5% 参数可训练）将预训练 VGGT 模型适配到 RGB+热成像跨模态 3D 重建，无需配对/同步数据，在位姿估计上 AUC@30 达 70.0（vs COLMAP 57.6），推理速度 200× 快于 MINIMA_ROMA，且在烟雾遮挡等极端条件下保持鲁棒。

---

### [T-QPM: Enabling Temporal Out-Of-Distribution Detection and Domain Generalization for Vision-Language Models](t-qpm.md)

🛡️ 多模态VLM / AI安全

提出 T-QPM 框架，用四路跨模态匹配分数（语义匹配、视觉典型性、Caption-文本对齐、Caption-视觉对齐）扩展 DPM，配合时间步特定原型和三组件训练损失，在动态开放世界中实现时序鲁棒的 OOD 检测——CLEAR100 上 FPR95 从 DPM 的 41.53 降至 17.42，ImageNet 上 AUROC 达 98.79。

---

### [TexEditor: Structure-Preserving Text-Driven Texture Editing](texeditor.md)

🎨 图像生成 / 图像编辑

提出 TexEditor，通过场景级合成数据（TexBlender, 5000 对）+ RL 训练（指令遵循奖励 + 基于线框 SSIM 的结构保持损失）+ 真实世界 benchmark（TexBench, 825 张），在纹理编辑中实现指令遵循（0.858）和结构保持（0.929）的双重 SOTA，超越 Nano Banana Pro。

---

### [VEGA-3D: Generation Models Know Space — Unleashing Implicit 3D Priors for Scene Understanding](vega-3d.md)

🧊 3D视觉 / 多模态VLM

提出 VEGA-3D，将冻结的视频生成模型（Wan2.1）作为"隐式世界模拟器"，通过噪声注入激活其中间层的 3D 几何先验，经 token 级自适应门控融合注入 MLLM 的语义流中，无需任何显式 3D 标注即可在 ScanRefer/SQA3D/VSI-Bench/LIBERO 上超越依赖 3D 监督的 SOTA。

---
