# 📅 2026-03-17 精选笔记

> 共 **20** 篇

---

### [360° Image Perception with MLLMs: A Comprehensive Benchmark and Training-Free Method](360bench.md)

👁️ 多模态/VLM

提出 360Bench（7K分辨率360°图像+7个子任务+人工标注）和 Free360（无训练场景图VQA框架），在投影感知任务上提升14%，揭示最强模型(46.5%)与人类(86.3%)的巨大差距。

---

### [BATQuant: Outlier-resilient MXFP4 Quantization via Learnable Block-wise Optimization](batquant.md)

👁️ 多模态/VLM / 模型压缩

提出 BATQuant，通过块对齐的仿射变换（而非全局旋转）处理 MXFP4 量化中的异常值问题，用 Global-Private Kronecker 分解将参数量降低 79%，在 W4A4KV16 激进配置下恢复多模态基准 96.43% 的全精度性能。

---

### [BUSSARD: Normalizing Flows for Bijective Universal Scene-Specific Anomalous Relationship Detection](bussard.md)

👁️ 多模态/VLM

用正则化流+LLM嵌入检测场景图中的异常物体-关系-物体三元组，比基线高10% AUROC且推理快5×，对同义词变化鲁棒。

---

### [CIRCLES: Retrieving Counterfactuals Improves Visual In-Context Learning](circles.md)

👁️ 多模态/VLM

提出 CIRCLES 框架，通过组合图像检索（CIR）主动构造反事实风格的示例集，替代传统基于相似度的被动检索，使 VLM 在视觉上下文学习中学习因果属性关系而非虚假关联，在细粒度分类和 VQA 上一致超越 RICES 等基线。

---

### [HeBA: Heterogeneous Bottleneck Adapters for Robust Vision-Language Models](heba.md)

👁️ 多模态/VLM

提出 HeBA，一种异构瓶颈适配器框架，为 CLIP 的视觉和文本分支分别设计卷积和线性适配器（压缩而非扩展），配合 Kaiming 初始化替代零初始化，在 11 个 few-shot 基准上以 81.35% 调和平均达到新 SOTA。

---

### [Hidden Clones: Exposing and Fixing Family Bias in Vision-Language Model Ensembles](hidden-clones.md)

👁️ 多模态/VLM

揭示 VLM 集成中的家族相关误差（有效独立投票者仅 2.5-3.6 个），提出 Learned Candidate Scoring (LCS) 在 VQAv2/TextVQA/GQA 上分别提升 0.68/0.61/2.45%，VQAv2 达 87.83%。

---

### [Hyperbolic Multimodal Generative Representation Learning for Generalized Zero-Shot Multimodal Information Extraction](hyperbolic-mmgr.md)

👁️ 多模态/VLM

在双曲空间中学习多模态生成表示，用于泛化零样本多模态信息抽取，结合图表示和语言模型实现层次化语义知识融合。

---

### [IOMM: Rethinking UMM Visual Generation — Masked Modeling for Efficient Image-Only Pre-training](iomm.md)

🎨 多模态/VLM / 图像生成

提出 IOMM 框架，通过两阶段训练（纯图像自监督预训练 + 混合数据微调）构建统一多模态模型的视觉生成组件，用掩码图像建模防止自条件坍塌，仅 1050 H800 GPU 小时即在 GenEval 上达到 0.89 超越 BAGEL-7B。

---

### [MolmoBot: Large-Scale Simulation Enables Zero-Shot Manipulation](molmobot.md)

🤖 机器人

通过 MolmoBot-Engine 生成 180 万仿真操作轨迹训练 VLA 策略，实现完全零样本 sim-to-real 迁移——在桌面抓取上 79.2% 成功率（π0.5 仅 39.2%），同时支持移动操作（开门/开抽屉/移动抓取），全部开源。

---

### [Parallel In-context Learning for Large Vision Language Models](parallel-icl.md)

👁️ 多模态/VLM

提出 Parallel-ICL，将长示例上下文分割为并行处理的小块，通过加权 Product-of-Experts 融合，在保持完整上下文ICL性能的同时大幅降低推理延迟。

---

### [Cross-modal Learning for Plankton Recognition](plankton-recognition.md)

👁️ 多模态/VLM

将CLIP启发的对比学习应用于明场显微图像+光学剖面的跨模态浮游生物识别，用少量标注数据实现高精度分类和跨域泛化。

---

### [Proxy-GRM: Learning Transferable Rubrics via Proxy-Guided Critique for VLM Reward Models](proxy-grm.md)

👁️ 多模态/VLM / LLM对齐

提出 Proxy-GRM，通过训练独立的代理评估器验证生成式奖励模型（GRM）产生的评估准则（rubric）的可迁移性，将该验证信号作为 RL 奖励闭环优化 rubric 质量，仅用 ~50K 数据在三个 VLM 奖励基准上达到 SOTA。

---

### [RaDAR: Relation-aware Diffusion-Asymmetric Graph Contrastive Learning for Recommendation](radar-recsys.md)

🎨 图像生成 / 推荐系统

提出 RaDAR，结合扩散引导的图增强和非对称对比学习用于推荐系统，通过关系感知的边细化在噪声和稀疏条件下显著超越 SOTA。

---

### [SemTok: Semantic One-Dimensional Tokenizer for Image Reconstruction and Generation](semtok.md)

🎨 图像生成

提出 SemTok，将2D图像压缩为语义对齐的1D token序列，通过语义对齐约束实现SOTA图像重建保真度，为下游自回归生成提供紧凑输入。

---

### [V-DyKnow: A Dynamic Benchmark for Time-Sensitive Knowledge in Vision Language Models](v-dyknow.md)

👁️ 多模态/VLM

提出 V-DyKnow，一个动态基准用于评估 VLM 的时效性事实知识——通过 Wikidata 在评估时获取最新事实作为标准答案，发现 VLM 频繁输出过时信息（开源模型仅 3-32% 正确），且视觉输入比文本输入的事实召回显著退化。

---

### [VIEW2SPACE: Studying Multi-View Visual Reasoning from Sparse Observations](view2space.md)

🧊 3D视觉

提出 VIEW2SPACE 基准（2000个3D场景，3M QA对），评估从稀疏多视图进行3D推理的能力，提出基于视觉证据的 Grounded Chain-of-Thought 方法实现 +52% mIoU 提升并可迁移到真实世界。

---

### [VIGOR: Video Geometry-Oriented Reward for Temporal Generative Alignment](vigor.md)

🎨 图像生成 / 视频理解

提出基于 VGGT 几何基础模型的逐点重投影误差奖励，通过几何感知采样聚焦关键区域，支持 SFT/DPO 后训练和因果视频模型的测试时缩放（TTS），有效缓解视频生成中的物体变形、空间漂移和深度违规等几何不一致问题。

---

### [VisBrowse-Bench: Benchmarking Visual-Native Search for Multimodal Browsing Agents](visbrowse-bench.md)

👁️ 多模态/VLM / LLM Agent

提出 VisBrowse-Bench，一个 169 道专家构造的多模态 VQA 基准，要求浏览 Agent 在搜索过程中主动获取和推理视觉信息（而非仅靠反向图像搜索获取实体名后退化为文本搜索），最强模型 Claude-4.6-Opus 仅达 47.6% 准确率。

---

### [Visual Distraction Undermines Moral Reasoning in Vision-Language Models](visual-distraction-moral.md)

🤖 机器人 / AI安全

提出 Moral Dilemma Simulation (MDS) 基准，揭示视觉输入会绕过 VLM 的文本安全机制——视觉模态激活直觉式推理路径，覆盖纯文本场景中的审慎推理，导致道德判断退化。

---

### [WorldCam: Interactive Autoregressive 3D Gaming Worlds with Camera Pose as Unifying Representation](worldcam.md)

🎨 图像生成

以相机位姿(6-DoF)为统一几何表示，通过视频扩散模型实现交互式3D游戏世界生成，支持精确动作控制、长程导航和一致的3D几何，使用3000分钟标注游戏数据训练。

---
