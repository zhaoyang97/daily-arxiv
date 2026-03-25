# 📅 2026-03-06 精选笔记

> 共 **20** 篇

---

### [Multimodal Behavior Tree Generation: A Small Vision-Language Model for Robot Task Planning](behavior-tree-vlm.md)

🤖 机器人

提出首个用紧凑型开源 VLM（500M-4B）从 RGB 图像和自然语言指令直接生成可执行行为树的方法，通过大模型教师管线构建多模态行为树数据集，微调后的 4B 模型在仿真评估中达到 87% 成功率，接近 GPT-5 表现。

---

### [Beyond Rows to Reasoning: Agentic Retrieval for Multimodal Spreadsheet Understanding](brtr-spreadsheet.md)

🧩 多模态/VLM

提出 BRTR，一个多模态 agentic RAG 框架，用迭代工具调用循环替代单次检索，结合 planner-executor 架构，在企业级电子表格理解任务上比单次检索方法提升 25 个百分点（FRTR-Bench 达 99% 准确率）。

---

### [Reforming the Mechanism: Editing Reasoning Patterns in LLMs with Circuit Reshaping](circuit-reshaping.md)

🔄 自监督学习

提出 Reasoning Editing 范式和 REdit 框架，通过发现 Circuit-Interference Law（电路重叠度与编辑干扰成正比），主动重塑 LLM 内部神经电路来解码/注入推理模式，在通用性和局部性之间取得优越平衡，Generality 提升最高 16.1%，Locality 提升最高 12.2%。

---

### [Spatial Colour Mixing Illusions as a Perception Stress Test for Vision-Language Models](color-mixing-vlm.md)

🧩 多模态/VLM

提出空间颜色混合错觉作为 VLM 感知压力测试，发现 9 个 VLM 在 8 种颜色畸变下精度急剧下降，且扩大语言模型规模无法可靠缓解，而人类在相同条件下远优于模型。

---

### [DC-Merge: Improving Model Merging with Directional Consistency](dc-merge.md)

🧩 多模态/VLM

提出 DC-Merge，通过平衡 task vector 的奇异值能量分布 + 投影到共享正交子空间对齐方向几何，解决模型合并时知识丢失问题——在 vision 和 VLM benchmark 上全面 SOTA（CVPR 2026）。

---

### [DreamToNav: Generalizable Navigation for Robots via Generative Video Planning](dreamtonav.md)

🎬 视频理解 / 机器人导航

提出 DreamToNav，利用生成式视频模型（NVIDIA Cosmos 2.5）作为规划引擎，机器人先"想象"执行过程的视频，再从生成视频中提取可执行轨迹，实现自然语言驱动的无需任务特定工程的导航。

---

### [GenHOI: Towards Object-Consistent Hand-Object Interaction with Temporally Balanced and Spatially Selective Object Injection](genhoi.md)

🎬 视频理解

提出 GenHOI，一个基于预训练视频生成模型的轻量扩展模块，通过 Head-Sliding RoPE 实现时间均衡的参考物体信息注入和空间注意力门控实现空间选择性注入，在野外场景中显著提升手-物交互视频的物体一致性和交互真实感。

---

### [HERO: Hierarchical Embedding-Refinement for Open-Vocabulary Temporal Sentence Grounding](hero-ov-tsgv.md)

🎬 视频理解

首次定义 Open-Vocabulary TSGV 任务并构建 Charades-OV/ActivityNet-OV benchmark，提出 HERO 框架通过层次语义嵌入 + 语义引导视觉过滤 + 对比掩码文本精炼三个模块，在开放词汇场景下大幅提升时序句子定位的泛化能力。

---

### [Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration](igar-vla-grounding.md)

🤖 机器人

揭示 VLA 模型的"语言盲视"现象——机器人在矛盾指令下仍执行视觉上合理的动作而忽略语言语义，提出 ICBench 诊断基准和 IGAR 无训练注意力重校准方法，显著提升语言指令对动作生成的影响力。

---

### [LIT-RAGBench: Benchmarking Generator Capabilities of Large Language Models in RAG](lit-ragbench.md)

🧠 LLM推理

提出 LIT-RAGBench，一个系统评估 RAG 中 Generator 五大能力（Integration/Reasoning/Logic/Table/Abstention）的 benchmark——通过虚构实体防止知识泄漏、支持跨类别组合评估，实验发现即使 GPT-5 也无法超过 90% 总体准确率。

---

### [Cut to the Chase: Training-free Multimodal Summarization via Chain-of-Events](multimodal-summary.md)

🧩 多模态/VLM

提出 CoE（Chain-of-Events），一个无需训练的多模态摘要框架，通过构建层次化事件图（HEG）实现结构化跨模态推理，在 8 个数据集上平均超越 SOTA 视频 CoT 方法 +3.04 ROUGE、+9.51 CIDEr、+1.88 BERTScore。

---

### [Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion](omni-diffusion.md)

🎨 图像生成

首个基于 mask-based 离散扩散模型的 any-to-any 多模态语言模型——Omni-Diffusion 通过统一的 mask token 预测直接建模文本/图像/语音的联合分布，配合三阶段渐进训练和专用推理策略，在多模态理解和生成任务上达到可比甚至超越自回归方法的性能。

---

### [Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders](penguin-vl.md)

🧩 多模态/VLM

Penguin-VL 提出用文本 LLM（Qwen3-0.6B）直接初始化视觉编码器，配合重建蒸馏预训练、时序冗余感知压缩（TRA）和两阶段 SFT，在 2B/8B 参数量级实现与 Qwen3-VL 可比甚至超越的多模态性能——证明视觉表征质量而非模型规模才是高效 VLM 的关键瓶颈。

---

### [Physical Simulator In-the-Loop Video Generation](physics-video-gen.md)

🎨 图像生成

提出 PSIVG 框架，将物理模拟器嵌入视频扩散生成循环中，通过感知管线重建 4D 场景并在物理模拟器中生成物理一致的轨迹来引导视频生成，同时设计测试时纹理一致性优化（TTCO）提升运动物体的纹理稳定性，用户偏好率达 82.3%。

---

### [Pinterest Canvas: Large-Scale Image Generation at Pinterest](pinterest-canvas.md)

🎨 图像生成

Pinterest 提出 Canvas 系统，先训练一个通用的多模态扩散基础模型，再快速微调出面向不同产品场景（背景生成、宽高比扩展、场景合成、图生视频）的专用变体，在线 A/B 实验显示广告互动率提升 18%。

---

### [Place-it-R1: Unlocking Environment-aware Reasoning for Video Object Insertion](place-it-r1.md)

🎨 图像生成

提出 Place-it-R1，首个 Think-then-Place 视频物体插入框架——利用 MLLM 的 CoT 推理理解物理场景约束并自动规划插入轨迹，通过 Spatial DPO 和闭环协同精炼实现物理合理的视频编辑，在多个 benchmark 上超越商业模型 Kling/Pika。

---

### [Reference-guided Policy Optimization for Molecular Optimization via LLM Reasoning](ref-policy-mol.md)

📦 模型压缩

提出 RePO（Reference-guided Policy Optimization），在 LLM 分子优化任务中结合 GRPO 风格的奖励驱动探索与答案级别的参考分子引导，解决了 SFT 抑制推理探索和 RLVR 奖励稀疏的问题，在 TOMG-Bench 上成功率×相似度提升最高 17.4%。

---

### [Reflective Flow Sampling Enhancement](reflective-flow.md)

🎨 图像生成

提出 RF-Sampling，一个面向 Flow Matching 模型（尤其是 CFG-distilled 变体如 FLUX）的无训练推理增强框架，理论证明其隐式执行文本-图像对齐分数的梯度上升，在多个 benchmark 上提升生成质量并首次在 FLUX 上展示 test-time scaling 能力。

---

### [SpatialMAGIC: A Hybrid Framework Integrating Graph Diffusion and Spatial Attention for Spatial Transcriptomics Imputation](spatialmagic.md)

📄 生物信息学 / 空间转录组学

提出 SpatialMAGIC，将 MAGIC 图扩散与 Transformer 空间自注意力融合，对空间转录组数据进行缺失值填补，在多平台上实现聚类精度和生物可解释性的双提升。

---

### [History-Conditioned Spatio-Temporal Visual Token Pruning for Efficient VLN](vln-token-pruning.md)

🤖 机器人

提出面向视觉语言导航（VLN）的无训练时空 token 剪枝框架——通过 Adaptive MMR 对当前帧做空间 token 选择、Query-Guided Re-weighting 对历史帧做时空压缩，在 90% 剪枝率下仍保持优于所有基线的导航性能，并在真实四足机器人上部署验证。

---
