# 📅 2026-03-23 精选笔记

> 共 **20** 篇

---

### [ADaFuSE: Adaptive Diffusion-generated Image and Text Fusion for Interactive Text-to-Image Retrieval](adafuse.md)

📄 信息检索 / 多模态融合

提出 ADaFuSE，用自适应门控 + 语义感知 MoE 双分支替代扩散增强交互式文本-图像检索 (I-TIR) 中的静态加法融合，动态校准文本与扩散生成图像的融合权重，在 4 个 I-TIR 基准上以仅 5.29% 的参数增量超越 DAR 最高 3.49% Hits@10，被 SIGIR 2026 录用。

---

### [BayesMM: Adapting Point Cloud Analysis via Multimodal Bayesian Distribution Learning](bayesmm.md)

🧊 3D视觉 / 点云分析

提出 BayesMM，用高斯分布建模文本先验和流式视觉特征，通过贝叶斯模型平均自动调节两模态权重，实现 training-free 的测试时点云分析适配，在多个点云基准上平均提升 4%+ 鲁棒性。

---

### [Back to Point: Exploring Point-Language Models for Zero-Shot 3D Anomaly Detection](btp-3d-ad.md)

🧊 3D视觉 / AI安全

首次将预训练 Point-Language Model (PLM) 应用于零样本 3D 异常检测，提出 BTP 框架，通过多粒度特征嵌入模块 (MGFEM) 和几何特征创建模块 (GFCM) 直接在点云空间实现细粒度异常定位，避免了传统 VLM 方法的 3D→2D 投影信息损失。

---

### [CatRAG: Functor-Guided Structural Debiasing with Retrieval Augmentation for Fair LLMs](catrag.md)

🛡️ AI安全 / LLM公平性

提出 CatRAG，结合范畴论驱动的 functor 投影（在 embedding 空间压制人口统计属性方向）与多样性感知的 RAG 检索（注入反刻板印象证据），在 BBQ 基准上将 Llama-3 准确率从 48.9% 提升至 81.2%，偏差分数从 0.63 降至近零 0.01，且在三个开源 LLM 上一致有效。

---

### [Structured Visual Narratives Undermine Safety Alignment in Multimodal Large Language Models](comicjailbreak.md)

🛡️ 多模态VLM / AI安全

提出 ComicJailbreak——用三格漫画模板将恶意目标嵌入视觉叙事中的越狱基准（1167 个攻击实例，10 类危害，5 种任务），在 15 个 SOTA MLLM 上实测显示漫画攻击的 EASR 超过 90%（多个商业模型），且现有防御（AdaShield/AsD）虽降低攻击成功率但严重过度拒绝正常请求。

---

### [CORE: Concept-aware Continual Unlearning for Large Vision-Language Models](core-unlearning.md)

📄 多模态VLM / 机器遗忘

提出 CORE（COncept-aware REfuser）框架，将 LVLM 持续遗忘问题转化为概念级精细操作——通过概念模块提取细粒度视觉属性与文本意图，概念调制器识别每个遗忘类别的概念组合，再用混合拒绝专家（mixture of refusers）基于概念相关性路由生成精准拒绝响应，在 16 个持续遗忘任务序列中同时避免不相关拒绝和过度拒绝。

---

### [Let's Think with Images Efficiently! An Interleaved-Modal Chain-of-Thought Reasoning Framework with Dynamic and Precise Visual Thoughts (DaP-ICoT)](dap-icot.md)

🧠 多模态VLM / LLM推理

针对交错模态思维链（ICoT）中静态视觉插入冗余和碎片化视觉 token 不连贯两大问题，提出 DaP-ICoT 框架：通过置信度感知的动态视觉思维集成（DVTI）和基于 SAM2 分割的精确视觉思维引导（PVTG），在 SOTA 推理精度下减少 72.6% 的 token 消耗。

---

### [DiT-Flow: Speech Enhancement Robust to Multiple Distortions based on Flow Matching in Latent Space and Diffusion Transformers](dit-flow.md)

📄 音频处理 / 模型效率

提出 DiT-Flow，一个基于 Flow Matching + Diffusion Transformer (uDiT) 的语音增强框架，在 VAE 潜空间中操作，配合自建的 StillSonicSet 数据集和 MoELoRA 参数高效适配策略（仅 4.9% 参数），实现对噪声/混响/压缩等多种失真的鲁棒增强。

---

### [EAGER: Efficient Failure Management for Multi-Agent Systems with Reasoning Trace Representation](eager.md)

🦾 自监督学习 / LLM Agent

提出 EAGER，通过推理域对比学习将多智能体推理轨迹编码为统一表示空间，实现基于历史故障模式的实时逐步故障检测（5 秒内）、反思式缓解和根因诊断，在三个开源 MAS 上异常检测 F1 达 73-86%，并将 RCLAgent 的 R@1 从 28.47% 提升至 30.19%。

---

### [EgoGroups: A Benchmark For Detecting Social Groups of People in the Wild](egogroups.md)

📄 多模态VLM / 社会群体检测

构建首个第一人称视角的社交群体检测数据集 EgoGroups，覆盖 65 个国家、三种人群密度和四种天气/时段条件，密集标注人物和社交群体，系统评估 SOTA VLM/LLM 和监督模型，发现 VLM 在零样本设置下可超越监督基线，且人群密度和文化区域显著影响模型性能。

---

### [FIM-Merging: Data-Free Layer-Adaptive Merging via Fisher Information for Long-to-Short Reasoning LLMs](fim-merging.md)

🧠 LLM推理 / 模型合并

提出 FIM-Merging，首次理论证明模型合并误差由 per-layer Hessian 范数约束，用 Fisher 信息矩阵作为无需校准数据的代理信号，实现层自适应合并系数分配。在 L2S（长推理→短推理）场景下，FIM-TIES 在 1.5B/7B 上均超越 ACM-TIES，MATH500 +6.2 点，同时输出长度缩短 92.6%。

---

### [GeoFusion-CAD: Structure-Aware Diffusion with Geometric State Space for Parametric 3D Design](geofusion-cad.md)

📦 模型压缩 / CAD生成

提出 GeoFusion-CAD，用层次化树结构编码 CAD 程序（联合捕获几何和拓扑信息），通过 G-Mamba 扩散编码器以线性时间复杂度 $O(Ld)$ 建模长程结构依赖，配合新构建的 DeepCAD-240 基准（序列长度 40-240），在长 CAD 序列生成上大幅超越 Transformer 方法，且保持高几何保真度和拓扑一致性。

---

### [Exploring Multimodal Prompts For Unsupervised Continuous Anomaly Detection](multimodal-ucad.md)

📄 多模态VLM / 异常检测

提出多模态持续异常检测框架，通过持续多模态提示记忆库（CMPMB，融合可学习文本提示+视觉提示）和缺陷语义引导自适应融合机制（DSG-AFM，含自适应归一化+动态融合策略），在 MVTec AD 和 VisA 上 AUROC 检测精度提升 4.4%，分割精度提升 14.8%。

---

### [Omni-WorldBench: Towards a Comprehensive Interaction-Centric Evaluation for World Models](omni-worldbench.md)

🧊 3D视觉 / 世界模型评测

提出 Omni-WorldBench，首个以交互响应为核心的世界模型评测基准：Omni-WorldSuite 提供三层交互级别（物体级→局部环境→全局）×多场景类型的系统化 prompt 套件，Omni-Metrics 用 agent-based 评估框架量化交互动作对状态转移的因果影响并融合为统一 AgenticScore，在 18 个世界模型上揭示交互响应的关键局限。

---

### [P-Flow: Prompting Visual Effects Generation](p-flow.md)

📄 视频生成 / 视觉特效定制

提出 P-Flow，一个 training-free 框架，通过测试时 prompt 优化（test-time prompt optimization）定制动态视觉特效——用 VLM 迭代比较参考特效视频和生成结果的差异来优化 prompt，配合 SVD-based 噪声先验增强和历史轨迹维护机制，无需微调模型即实现高保真跨场景特效迁移，在 FID-VID、FVD、Dynamic Degree 上全面超越训练-based 基线。

---

### [ResFlow-Tuner: Tuning Real-World Image Restoration at Inference via Test-Time Scaling](resflow-tuner.md)

🎨 图像生成 / 图像复原

提出 ResFlow-Tuner，基于 FLUX.1-dev flow matching 模型做真实世界图像复原，通过统一多模态融合（UMMF）编码条件信息 + 训练免费的 test-time scaling（推理时用 reward model 反馈动态调整去噪方向），在多个标准基准达到 SOTA。

---

### [RoboGate: Adaptive Failure Discovery for Safe Robot Policy Deployment](robogate.md)

🤖 机器人 / 安全验证 / 部署风险管理

提出 RoboGate 部署风险管理框架，通过两阶段自适应采样（Stage 1 LHS 全局 20K + Stage 2 边界聚焦 10K）在 8 维操作参数空间高效发现机器人抓放策略的失败边界，30K 次 Isaac Sim 实验获得闭式边界方程 $\mu^*(m)=(1.469+0.419m)/(3.691-1.400m)$、四个通用危险区，并暴露 VLA 模型（Octo-Small）在对抗场景仅 30.9% 成功率。

---

### [SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained T2I Generation](spatial-reward.md)

🎨 图像生成 / 空间一致性

提出 SpatialReward，通过 Prompt 分解→专家检测器精确定位→VLM CoT 推理三阶段流水线构建可验证的空间 reward model，配合 SpatRelBench 基准（覆盖朝向、3D 关系、文字放置），在 SD3.5/FLUX 上用 RL 训练显著提升空间一致性。

---

### [StreamingEval: A Unified Evaluation Protocol towards Realistic Streaming Video Understanding](streaming-eval.md)

🎬 视频理解 / 评测基准

提出 StreamingEval，首个统一评测框架同时衡量 Video-LLM 在真实流式约束（有限内存+实时帧率+因果推理）下的准确率、编码效率、解码延迟和存储开销，通过异步三进程流水线模拟真实流式场景，在 12 个代表性模型上揭示当前"在线"模型在严格流式约束下实际不可用。

---

### [Do World Action Models Generalize Better than VLAs? A Robustness Study](wam-vs-vla.md)

🤖 机器人 / 世界模型

系统对比 SOTA VLA 策略（π0.5、OpenVLA 等）和新兴的世界动作模型 WAM（Cosmos-Policy、LingBot-VA 等）在视觉/语言扰动下的鲁棒性，发现 WAM 凭借视频预训练获得的时空先验在噪声/光照/布局扰动下表现更好（LingBot-VA 74.2%、Cosmos-Policy 82.2%），但推理延迟高于 VLA 4.8 倍以上。

---
