# 📅 2026-03-03 精选笔记

> 共 **20** 篇

---

### [ACE-Merging: Data-Free Model Merging with Adaptive Covariance Estimation](ace-merging.md)

⚡ LLM效率

ACE-Merging 从理论上证明任务的输入协方差可以从微调权重变化中隐式估计，基于此推导出无数据模型合并的闭式解，并通过自适应归一化和谱精修保证鲁棒性，在 GPT-2 上比现有方法提升 4% 平均准确率。

---

### [Beyond Language Modeling: An Exploration of Multimodal Pretraining](beyond-language-modeling.md)

🧩 多模态/VLM

Meta FAIR 通过从头训练的受控实验系统研究了多模态预训练的设计空间，发现 RAE（表示自编码器）是最优统一视觉表示、视觉和语言数据协同而非竞争、世界建模能力从通用训练涌现、MoE 架构自然调和视觉和语言之间的缩放不对称性。

---

### [BrandFusion: A Multi-Agent Framework for Seamless Brand Integration in Text-to-Video Generation](brandfusion.md)

🎬 视频理解

BrandFusion 首次定义了 T2V 无缝品牌植入任务，提出离线品牌知识库构建 + 在线五智能体协作提示优化框架，在 18 个品牌 × 3 个 T2V 模型上显著超越基线，实现语义保持、品牌可见性和自然融合的三重平衡。

---

### [Chain of World: World Model Thinking in Latent Motion](chain-of-world.md)

🤖 机器人

CoWVLA 提出"Chain of World"范式，通过视频 VAE 将动态分解为结构和运动潜在表示，在预训练阶段学习推理潜在运动链+预测终帧，在微调阶段对齐离散动作，统一了世界模型的时序推理能力和潜在动作的紧凑性。

---

### [From "What" to "How": Constrained Reasoning for Autoregressive Image Generation](cor-painter.md)

🎨 图像生成

CoR-Painter 提出"How-to-What"范式——先推理空间约束和构图规则（How to draw），再生成详细描述（What to draw），配合双目标 GRPO 分别优化文本推理和视觉投影，在 T2I-CompBench 空间关系指标上提升 5.41%。

---

### [EduVQA: Benchmarking AI-Generated Video Quality Assessment for Education](eduvqa.md)

🗣️ LLM/NLP

EduVQA 构建了首个面向数学教育的 AI 生成视频质量基准 EduAIGV-1k（1130 个视频 ×5 维细粒度标注），并提出基于结构化 2D MoE 的双路径评估框架，在感知质量和提示对齐两个维度上全面超越现有 VQA 基线。

---

### [Graph-GRPO: Stabilizing Multi-Agent Topology Learning via Group Relative Policy Optimization](graph-grpo.md)

⚖️ LLM对齐

Graph-GRPO 将 Group Relative Policy Optimization 引入多智能体系统的通信拓扑优化，通过组内相对优势估计和边级别信用分配，解决了传统绝对奖励方法在简单任务上的虚假强化和信用分配模糊问题，在 6 个基准上达到 92.45% 平均准确率。

---

### [LoGeR: Long-Context Geometric Reconstruction with Hybrid Memory](loger.md)

🧊 3D视觉

LoGeR 提出混合记忆架构——参数化 TTT 锚定全局坐标系防止尺度漂移 + 非参数化滑动窗口注意力保持局部对齐精度，在 128 帧训练后可泛化到 19k 帧推理，在 KITTI 上 ATE 降低 74%（72.86→18.65）。

---

### [PhyPrompt: RL-based Prompt Refinement for Physically Plausible Text-to-Video Generation](phyprompt.md)

🎬 视频理解

PhyPrompt 用两阶段训练（物理 CoT 微调+动态奖励 GRPO）自动将用户提示重写为物理感知描述，7B 模型在 VideoPhy2 上达到 40.8% 联合成功率，超越 GPT-4o（+3.8%）和 DeepSeek-V3（+2.2%，100 倍参数），且零样本迁移到 4 种不同 T2V 架构。

---

### [QFlowNet: Fast, Diverse, and Efficient Unitary Synthesis with Generative Flow Networks](qflownet.md)

🎨 图像生成

QFlowNet 将量子电路的酉矩阵合成问题重构为通向恒等矩阵的路径查找，用 GFlowNet + Transformer 架构在稀疏奖励下学习多样化合成策略，3-qubit 基准上达 99.7% 成功率且推理效率远超扩散模型。

---

### [SERP: Agentic Self-Evolutionary Replanning for Embodied Navigation](serp-replanning.md)

🤖 机器人

SERP 提出自进化重规划框架，通过局部 ILAD（上下文学习 + 自动微分）实时优化动作模型参数 + 全局 GCOT（图链式思维）压缩场景图做高效语义重规划，实现从"冻结模型"到"进化模型"的范式转变。

---

### [SFDE: Spatial and Frequency Domain Enhancement for Cross-View Geo-Localization](sfde-crossview.md)

📦 模型压缩

SFDE 提出空间-频率域协同增强网络，通过全局语义一致性、局部几何敏感性和频率稳定性对齐三个互补分支的并行学习，在 UAV-卫星跨视角地理定位中以轻量化设计取得竞争力甚至超越 SOTA 的性能。

---

### [TagaVLM: Topology-Aware Global Action Reasoning for Vision-Language Navigation](tagavlm.md)

🤖 机器人

TagaVLM 将拓扑图结构显式注入 VLM 骨干网络，通过交错导航提示（INP）和空间拓扑感知残差注意力（STAR-Att）实现端到端的全局动作推理，0.5B 模型即超越大部分大模型方法，7B 版本在 R2R unseen 上达到 SR 51.09%、SPL 47.18，大幅领先 MapGPT。

---

### [TC-Padé: Trajectory-Consistent Padé Approximation for Diffusion Acceleration](tc-pade.md)

🎨 图像生成

TC-Padé 提出基于 Padé 有理函数逼近的残差预测框架，通过自适应系数调制和分阶段预测策略，在低步数（20-30步）扩散采样中实现轨迹一致性加速，在 FLUX.1-dev 上实现 2.88× 加速且质量损失极小。

---

### [Think-as-You-See: Streaming Chain-of-Thought Reasoning for Large Vision-Language Models](think-as-you-see.md)

🎬 视频理解

TaYS 提出流式视频 CoT 推理范式，通过流式注意力掩码、解耦位置编码和并行双 KV 缓存机制，使 LVLM 在接收视频帧的同时进行增量推理，将首 token 延迟从 10.6 秒降至近零，推理-事件偏差减少 55%。

---

### [TRACE: Task-Adaptive Reasoning and Representation Learning for Universal Multimodal Retrieval](trace.md)

🧩 多模态/VLM

TRACE 将生成式 CoT 推理与判别式嵌入学习统一，先生成推理链解析查询意图再压缩为紧凑嵌入，模型自动学会对简单查询跳过推理、对复杂查询激活推理，在 M-BEIR 基准上达到新 SOTA。

---

### [Tucano 2 Cool: Better Open Source LLMs for Portuguese](tucano2.md)

🧠 LLM推理

Tucano 2 是一套完全开源的葡萄牙语 LLM（0.5B-3.7B），基于 320B token 高质量语料 GigaVerbo-v2 + 9.3B 合成数据训练，在多个葡萄牙语基准上达到 SOTA，并开放全部数据集、训练配方和评估代码。

---

### [ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation](ultra-humanoid.md)

🤖 机器人

ULTRA 提出一套完整的人形机器人全身运动操作框架：从物理驱动的神经重定向生成高质量训练数据，到统一的多模态控制器支持密集参考跟踪和稀疏目标执行，在 Unitree G1 上实现了从自我中心感知到自主操作的闭环控制。

---

### [UniG2U-Bench: Do Unified Models Advance Multimodal Understanding?](unig2u-bench.md)

🧩 多模态/VLM

UniG2U-Bench 是目前最大的统一多模态模型评测基准（3000 样本、30 子任务、30+ 模型），系统验证了"生成是否帮助理解"——结论是统一模型通常不如基础 VLM，但在空间智能、视觉错觉和多轮推理等特定任务上生成能力带来一致的提升。

---

### [VB: Visibility Benchmark for Visibility and Perspective Reasoning in Images](vb-visibility-benchmark.md)

🧩 多模态/VLM

VB 提出了一个专门测试 VLM 能否判断照片中什么可见/不可见、并在无法确定时选择弃权的基准，通过 2×2 最小编辑设计（图像翻转×文本翻转）在 100 个家族/300 个评测项上评估 9 个模型，GPT-4o 和 Gemini 3.1 Pro 并列最佳（0.728 综合分）。

---
