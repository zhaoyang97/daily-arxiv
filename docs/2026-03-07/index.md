# 📅 2026-03-07 精选笔记

> 共 **20** 篇

---

### [ACD-U: Asymmetric Co-teaching with Machine Unlearning for Robust Learning with Noisy Labels](acd-u.md)

🗣️ LLM/NLP

提出 ACD-U 框架，将**机器遗忘（machine unlearning）**引入噪声标签学习领域，结合 CLIP 预训练 ViT 与 CNN 的**非对称协同教学**，实现对错误记忆样本的事后纠正，在多个合成与真实噪声基准上取得 SOTA。

---

### [AdaGen: Learning Adaptive Policy for Image Synthesis](adagen.md)

🎨 图像生成

提出 AdaGen 框架，将多步生成模型中的调度参数配置（如 noise level、mask ratio、guidance scale 等）建模为 MDP，通过强化学习训练轻量级策略网络实现逐样本自适应生成策略，并设计对抗式奖励模型防止奖励过拟合，在四种生成范式、五个数据集上取得显著的性能和效率提升。

---

### [Governance Architecture for Autonomous Agent Systems: Threats, Framework, and Engineering Practice](agent-governance.md)

📦 模型压缩

提出 Layered Governance Architecture (LGA)——一个四层纵深防御架构（执行沙箱 → 意图验证 → 零信任协议 → 不可变审计日志），针对 LLM Agent 的三类执行层威胁（prompt injection、RAG 投毒、恶意插件），在 1,081 条双语 benchmark 上验证：LLM judge 可拦截 93–98.5% 的恶意工具调用，级联方案将误报率压至 1.9–6.7%，端到端延迟仅 ~980 ms。

---

### [Agentic Planning with Reasoning for Image Styling via Offline RL](agentic-styling.md)

🎨 图像生成

提出基于工具的 agentic RL 后训练框架，将复杂图像风格化任务分解为可组合的原子工具调用序列，结合链式推理 (CoT) 与 offline RL（Reward-Weighted / Standardized Reward-Weighted）训练小型 VLM planner（Qwen3-VL 4B/8B），在图像质量和指令遵循上超越直接 prompt 编辑和 GPT-4o 零样本基线。

---

### [AgrI Challenge: A Data-Centric AI Competition for Cross-Team Validation in Agricultural Vision](agri-challenge.md)

🗣️ LLM/NLP

提出 AgrI Challenge 竞赛框架与 Cross-Team Validation (CTV) 评估范式，通过 12 支团队独立采集的 50,673 张树种图像，揭示单源训练存在高达 16.20% 的验证-测试泛化鸿沟，而协作多源训练可将该鸿沟压缩 82–84%。

---

### [Looking Back and Forth: Cross-Image Attention Calibration and Attentive Preference Learning for Multi-Image Hallucination Mitigation](cross-image-hallucination.md)

🧩 多模态/VLM

提出 CAPL 框架，通过选择性跨图像 token 双向注意力机制和基于注意力截断的偏好学习（DPO），系统性地解决多图像场景下 LVLM 因单向因果注意力导致的跨图像信息流不对称和幻觉问题。

---

### [DyACE: Dynamic Algorithm Co-evolution for Online Automated Heuristic Design with Large Language Model](dyace.md)

🗣️ LLM/NLP

将自动化启发式算法设计（AHD）从静态一次性搜索重新定义为非平稳双层控制问题，提出 DyACE 框架，通过 Receding Horizon Control 架构让 LLM 作为 meta-controller 持续感知搜索轨迹特征并在线合成时变算法，在 JSSP/TSP/CVRP 三个组合优化基准上显著超越静态 AHD 方法。

---

### [Facial Expression Generation Aligned with Human Preference for Natural Dyadic Interaction](facial-expression.md)

🧩 多模态/VLM

提出一种基于人类反馈强化学习（RLHF）的面部表情生成方法，通过将表情生成建模为身份无关空间中的动作学习过程，结合 VLA 模型与 DPO 算法，实现听者表情与说话者情感的社会性对齐。

---

### [Unlocking Data Value in Finance: A Study on Distillation and Difficulty-Aware Training](finance-distillation.md)

📦 模型压缩

以数据为中心的金融 LLM 训练研究——通过多阶段蒸馏+验证构建 ODA-Fin-SFT-318k（高质量 CoT 数据）和 ODA-Fin-RL-12k（难但可验证的样本），在 Qwen3-8B 上训练的 ODA-Fin-RL-8B 在 9 个金融基准上达到 74.6% 均分，逼近 4 倍大的 Qwen3-32B（74.7%）。

---

### [FinSheet-Bench: From Simple Lookups to Complex Reasoning, Where LLMs Break on Financial Spreadsheets](finsheet-bench.md)

📖 NLP理解

提出 FinSheet-Bench，基于真实私募基金结构生成的合成金融电子表格基准——评估 10 种模型配置在复杂表格问答中的表现，最好的 Gemini 3.1 Pro 仅达 82.4%（约每 6 题错 1 题），揭示 LLM 在复杂金融表格上远未达到专业应用标准。

---

### [Hit-RAG: Learning to Reason with Long Contexts via Preference Alignment](hit-rag.md)

🧩 多模态/VLM

提出 Hit-RAG，三阶段偏好对齐框架（SFT 建立上下文感知 → DPO 抵御噪声干扰 → GRPO 防止推理崩溃），使小模型（Qwen3-4B/8B）在 8 个 RAG 基准上超越大模型甚至商业系统，PopQA 从 54.9% 提升到 63.1%。

---

### [Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts](llm-cuda.md)

🗣️ LLM/NLP

提出 MSKernelBench（多场景 CUDA 算子优化基准）和 CUDAMaster（多 agent + 硬件 profiling 过滤的自动优化框架），在密集/稀疏/LLM/科学计算等多类算子上实现显著加速，部分算子超越 cuBLAS 等闭源库性能。

---

### [MURE: Hierarchical Multi-Resolution Encoding via Vision-Language Models for Visual Document Retrieval](mure.md)

🧩 多模态/VLM

提出 MURE，通过多分辨率采样 + Resolution-level Matryoshka 表示学习 + 语义感知层次聚类压缩，实现视觉文档检索中粗细粒度特征的统一编码——仅用 ColPali 50% 的视觉 token 就超越其性能，在 ViDoRe V1/V2 上达到 PaliGemma 系列 SOTA。

---

### [PolyGLU: State-Conditional Activation Routing in Transformer Feed-Forward Networks](polyglu.md)

🗣️ LLM/NLP

提出 PolyGLU，将 Transformer FFN 中固定的单一激活函数替换为可学习的多激活函数动态路由机制（K=4），通过 Gumbel-Softmax 端到端训练，发现无需任何显式正则化即可涌现出近确定性的路由选择和深度依赖的激活函数特化模式（浅层偏好 GELU、深层偏好 Tanh）。

---

### [Retrieval-Augmented Generation for Predicting Cellular Responses to Gene Perturbation](rag-cellular.md)

🗣️ LLM/NLP

提出 PT-RAG，首个将 RAG 范式引入单细胞基因扰动响应预测的框架，通过两阶段可微检索（语义检索 + Gumbel-Softmax 细胞类型感知选择）来为生成器提供相关扰动上下文，显著优于无检索和朴素 RAG 基线。

---

### [SRLM: Self-Reflective Program Search for Long Context](recursive-lm-search.md)

🦾 LLM Agent

提出 SRLM，用不确定性感知的自反省（self-consistency + 口头置信度 + 推理链长度三信号联合）来指导长上下文交互程序的选择——在相同时间预算下比 RLM 提升最多 22%，且揭示递归本身并非 RLM 性能的主要驱动因素。

---

### [RoTri-Diff: A Spatial Robot-Object Triadic Interaction-Guided Diffusion Model for Bimanual Manipulation](rotri-diff.md)

🎨 图像生成

提出 RoTri-Diff，通过显式建模双臂与物体之间的三元空间交互关系（RoTri），并将其融入层次化扩散模型，实现稳定、精确的双臂协调操作，在 RLBench2 的 11 个任务上平均成功率超越 SOTA 10.2%。

---

### [Optimizing Multi-Modal Models for Image-Based Shape Retrieval: The Role of Pre-Alignment and Hard Contrastive Learning](shape-retrieval.md)

🧊 3D视觉

提出利用预对齐的多模态编码器（ULIP/OpenShape）将图像和点云嵌入共享空间，并设计多模态 Hard Contrastive Loss (HCL) 强化实例级区分，在多个 IBSR 基准上实现 SOTA，$Acc_{Top10}$ 接近 100%。

---

### [VirtueBench: Evaluating Trustworthiness under Uncertainty in Long Video Understanding](virtuebench.md)

🎬 视频理解

提出 VirtueBench，首个显式评估 VLM 在长视频理解中"不确定性下可信度"的基准——通过为每个视频构建多帧采样级别并区分可回答/不可回答案例，揭示大多数模型不善于诚实拒绝（拒绝准确率 0%~70%+），促使社区从"猜对就行"转向"可信回答"。

---

### [Foundational World Models Accurately Detect Bimanual Manipulator Failures](world-model-failure.md)

🤖 机器人

提出基于预训练视频基础模型（Cosmos Tokenizer）压缩潜空间中训练的概率世界模型，用 VAE 不确定性作为 conformal prediction 的非一致性分数进行运行时故障检测——仅用 ~600K 参数就在双臂机器人电缆操作数据集上达到 92.0% 加权分类精度，超越参数量 20 倍的学习方法 3.8%。

---
