# 📅 2026-03-08 精选笔记

> 共 **20** 篇

---

### [AgriPath: A Systematic Exploration of Architectural Trade-offs for Crop Disease Classification](agripath.md)

🧩 多模态/VLM

系统对比 CNN（ResNet-50）、对比式 VLM（CLIP/SigLIP）和生成式 VLM（Qwen2.5-VL/SmolVLM）在作物病害分类中的架构权衡——构建 AgriPath-LF16 基准（111K 图像/16 种作物/41 种病害，显式区分实验室和田间图像），发现 CNN 域内最强但跨域崩溃（96.8%→4.5%），对比式 VLM 参数高效且跨域竞争力强，生成式 VLM 跨域最鲁棒但存在幻觉和格式失败。

---

### [AI Misuse in Education Is a Measurement Problem: Toward a Learning Visibility Framework](ai-misuse-education.md)

🛡️ AI安全

将教育中的 AI 滥用从"检测问题"重新定义为"测量/可见性问题"——提出学习可见性框架（Learning Visibility Framework），强调过程透明而非对抗检测，三个核心原则：明确 AI 使用规范、重视学习过程作为评估证据、建立透明的学习活动时间线。

---

### [AQuA: Toward Strategic Response Generation for Ambiguous Visual Questions](aqua.md)

🧩 多模态/VLM

提出 AQuA 数据集，将视觉问答中的歧义分为 4 个层级（无歧义/可推断/多解/需澄清），训练 VLM 根据歧义程度自适应选择回答策略——SFT + GRPO 微调后的 3B 模型超越 GPT-5 和 Gemini 2.5 Flash。

---

### [AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots](atomic-vla.md)

🤖 机器人

提出 AtomicVLA，统一任务规划与动作执行的端到端框架——VLM 自适应切换 Thinking（生成任务链+原子技能抽象）和 Acting（SG-MoE 动态路由到对应技能专家生成动作）模式，通过模块化技能库支持新技能持续学习无灾难性遗忘，在 LIBERO-LONG 上超越 π₀ 10%，真实 Franka 上持续学习提升 21%。

---

### [Bolbosh: Script-Aware Flow Matching for Kashmiri Text-to-Speech](bolbosh.md)

📄 NLP / 语音合成

为克什米尔语构建首个开源神经 TTS 系统——基于 OT-CFM（最优传输条件流匹配）的跨语言适配策略 + 三阶段声学增强管线，MOS 从多语言基线的 1.86 提升至 3.63。

---

### [C²-Explorer: Contiguity-Driven Task Allocation with Connectivity-Aware Task Representation for Decentralized Multi-UAV Exploration](c2-explorer.md)

🤖 机器人

提出 C²-Explorer，去中心化多无人机探索框架——用连通性图（CCL 分割空间为独立任务单元）替代拓扑无关的均匀网格分解，并将任务分配建模为带图邻接连续性惩罚的 CVRP 问题，在 3 个场景中平均探索时间降低 43.1%、路径长度降低 33.3%（vs RACER/FAME），并在真实无人机上验证可行性。

---

### [Constraints Matrix Diffusion based Generative Neural Solver for Vehicle Routing Problems](cmd-vrp.md)

🎨 图像生成

用图扩散模型生成约束矩阵作为拓扑先验掩码，融入自回归 VRP 求解器——通过局部/全局双指针解码器缓解全连接注意力的过平滑问题，在 CVRPlib 378 种组合配置上达到 SOTA。

---

### [Learning Context-Adaptive Motion Priors for Masked Motion Diffusion Models with Efficient Kinematic Attention Aggregation](context-motion-diffusion.md)

🧊 3D视觉/运动捕捉

提出 MMDM（Masked Motion Diffusion Model），将掩码自编码器与扩散模型融合——通过 Kinematic Attention Aggregation（KAA）机制高效融合关节级和姿态级表示，同一架构通过学习上下文自适应的运动先验适配运动补全/精炼/插帧三种任务，在 Shelf 数据集达 98.5% PCP，Campus 达 97.6% PCP。

---

### [DocCogito: Aligning Layout Cognition and Step-Level Grounded Reasoning for Document Understanding](doccogito.md)

🧩 多模态/VLM

提出 DocCogito，无 OCR 的文档理解框架——轻量 Layout Tower 将版面结构蒸馏为可学习的全局 [LAYOUT] token，同时用 Visual-Semantic Chain（VSC）把推理分解为 5 种原子操作的确定性结构化链，通过渐进式四阶段训练（Layout 预训练→VSC 冷启动→拒绝采样 SFT→GRPO+区域置信度奖励），在 DocVQA/InfoVQA/TextVQA/OCRBench 四个 benchmark 达 SOTA。

---

### [DogWeave: High-Fidelity 3D Canine Reconstruction from a Single Image via Normal Fusion and Conditional Inpainting](dogweave.md)

🧊 3D视觉

提出 DogWeave，从单张 RGB 图像重建高保真 3D 犬类模型——三阶段流程：BITE 粗网格初始化 → SDF+多视图法线融合精炼几何 → 条件 inpainting 生成纹理，仅用 ~7K 2D 图像训练无需 3D 监督，FID 优于 Hunyuan3D 约 9%。

---

### [Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence](holi-spatial.md)

🧊 3D视觉

提出 Holi-Spatial，首个全自动从原始视频生成大规模 3D 空间标注的 pipeline——三阶段流程（几何优化→图像级感知→场景级精炼）构建 Holi-Spatial-4M 数据集（12K 场景、320K 3D 框、1.2M 空间 QA），用于微调 VLM 提升空间推理能力，在 ScanNet++ 上 3D grounding AP50 提升 15%。

---

### [InterReal: A Unified Physics-Based Imitation Framework for Learning Human-Object Interaction Skills](interreal.md)

🤖 机器人/具身智能

提出 InterReal，基于物理仿真的统一人-物交互（HOI）模仿学习框架——通过 HOI 运动增广（IK 保持手-物接触下偏移物体位置）和双循环自动奖励学习（外循环 SAC meta-policy 基于跟踪误差梯度动态调节内循环 PPO 的多维奖励权重），在 Unitree G1 上搬箱/推箱任务成功率达 96.41%/87.45%，大幅超越 InterMimic（84.72%/79.10%）。

---

### [Benchmarking Large Language Models for Quebec Insurance: From Closed-Book to RAG](llm-quebec-insurance.md)

🧠 LLM推理

构建魁北克保险领域的 807 道选择题金标准基准 AEPC-QA（来自纸质非公开认证手册，无数据污染风险），系统评估 51 个 LLM 在闭卷和 RAG 范式下的表现——发现推理时计算（o3 达 78.68%）最强、RAG 对弱模型是"知识均衡器"（DeepSeek-reasoner +35pp）但对强模型可能导致"上下文干扰"灾难（Gemini-2.5-Pro -60pp）、领域特化小模型不如通用大模型（"专业化悖论"）。

---

### [Scalable Training of Mixture-of-Experts Models with Megatron Core](megatron-moe.md)

⚡ LLM效率

NVIDIA 的 Megatron-Core MoE 训练系统技术报告——系统性解决 MoE 训练的三面墙（内存墙/通信墙/计算效率墙），通过 Parallel Folding（解耦注意力和 MoE 层的并行配置）、Flex 通信后端（DeepEP/HybridEP）、细粒度激活重算+FP8/FP4 量化、Grouped GEMM+CUDA Graphs，在 GB300 上 DeepSeek-V3-685B 达 1,233 TFLOPS/GPU，Qwen3-235B 达 974 TFLOPS/GPU。

---

### [QdaVPR: A novel query-based domain-agnostic model for visual place recognition](qdavpr.md)

🎨 图像生成

提出 QdaVPR，基于 Bag-of-Queries 框架的域无关视觉地点识别——双层对抗学习（query 特征级+图像特征级）+ query 组合三元组监督，在 Nordland/Tokyo24-7 等跨域基准上达 SOTA，推理时无额外开销。

---

### [SeDa: A Unified System for Dataset Discovery and Multi-Entity Augmented Semantic Exploration](seda.md)

📄 数据管理/信息检索

构建 SeDa 统一数据集发现系统——整合 200+ 平台的 760 万+ 数据集，通过 LLM 辅助的模式推断和元数据归一化、图结构主题标注（D2T/D2D2T/T2T 三路径召回+LLM 语义合并）、站点级分层采样死链监测、和多实体（站点/机构/企业）增强导航，在覆盖率、时效性和可追溯性上超越 Google Dataset Search 和 ChatPD。

---

### [Scaling Test-Time Robustness of Vision-Language Models via Self-Critical Inference Framework](self-critic-vlm.md)

🧩 多模态/VLM

提出 Self-Critical Inference（SCI）框架，通过多轮文本和视觉反事实推理统一解决 LVLM 的语言偏差和语言敏感性问题，同时提出模型自适应的 DRBench 动态鲁棒性评估基准，证明增加反事实推理轮数可持续提升鲁棒性。

---

### [SiamGM: Siamese Geometry-Aware and Motion-Guided Network for Real-Time Satellite Video Object Tracking](siamgm.md)

🎬 视频理解

提出 SiamGM，从空间几何和时间运动两个维度改进卫星视频跟踪——空间上用帧间图注意力（IFGA）建立细粒度拓扑对应 + 长宽比约束标签分配（LA），时间上用 nPSR 置信度驱动的在线运动模型修正（OMMR），在 SatSOT 上精度领先 4.5%，同时保持 130 FPS 实时速度。

---

### [TDM-R1: Reinforcing Few-Step Diffusion Models with Non-Differentiable Reward](tdm-r1.md)

🎨 图像生成

提出 TDM-R1，首个支持非可微奖励的少步扩散模型强化学习范式——利用 TDM 确定性轨迹为中间步骤提供无偏奖励估计，通过代理奖励学习 + 生成器优化的解耦机制，仅 4 NFE 即在 GenEval 上从 61% 提升至 92%，超越 GPT-4o（84%）。

---

### [VIVECaption: A Split Approach to Caption Quality Improvement](vivecaption.md)

🎨 图像生成

提出 VIVECaption，通过"两侧"策略改善 T2I/T2V 训练数据的图文对齐——Side A 用 CLIP 聚类+HDBSCAN 分层采样构建 310 张金标准数据集，Side B 用 SFT 微调 VLM 的角色检测能力，7B SFT 模型的角色 MacroF1 从 0.66 提升至 0.92。

---
