# 📅 2026-03-18 精选笔记

> 共 **20** 篇

---

### [CycleCap: Improving VLMs Captioning via Self-Supervised Cycle Consistency](cyclecap.md)

🎨 图像生成 / 多模态/VLM

用循环一致性（图→文→图重建）作为自监督训练信号改善 VLM 描述质量，无需人工标注数据，在 1B-7B 参数模型上一致提升。

---

### [Directing the Narrative: Controlling Coherence and Style in Story Generation](directing.md)

⚖️ LLM对齐

结合 Group-Shared Attention 和 DPO 实现连续叙事中角色身份（+10.0 CIDS）和视觉风格（+18.7 CSD）的一致性控制。

---

### [EvoGuard: An Extensible Agentic RL-based Framework for Practical AI-Generated Image Detection](evoguard.md)

👁️ 多模态/VLM / AI安全

提出 EvoGuard，将异构 AIGI 检测器封装为可调用工具，用 MLLM Agent 通过能力感知的动态编排机制多轮调用和推理，仅需二值标签的 GRPO 训练，实现 SOTA 检测精度和无需重训练的即插即用可扩展性。

---

### [Fine-Grained Post-Training Quantization for LVLMs with Quantization-aware Integrated Gradients](fine-grained.md)

👁️ 多模态/VLM / 模型压缩

用量化感知积分梯度在 token 级别测量量化敏感度（而非模态级别），在 3-bit 权重量化下提升 LLaVA-onevision-7B 1.60%，与全精度差距仅 1.33%。

---

### [FineViT: Progressively Unlocking Fine-Grained Perception with Dense Recaptions](finevit.md)

👁️ 多模态/VLM

提出 FineViT，一个从零训练的三阶段渐进式视觉编码器（MIM初始化→高分辨率对比学习→LLM对齐），配合 4.5 亿区域级标注数据集 FineCap-450M，在零样本识别/检索和 MLLM 多模态理解上全面超越 SigLIP2 和 Qwen-ViT。

---

### [FloorPlan-VLN: Floor Plan Guided Vision-Language Navigation](floorplan-vln.md)

🤖 机器人

构建 10K+ 集+100+ 标注平面图的导航数据集，实现平面图引导的 VLN 导航，成功率相对提升 60%+，对平面图畸变鲁棒。

---

### [Flow Matching Policy with Entropy Regularization (FMER)](flow.md)

🎨 图像生成 / 强化学习

基于 ODE 的 RL 框架，将 Flow Matching 与可解析的熵正则化结合增强探索，训练速度比 QVPO 快 7×，比高效扩散变体快 10-15%。

---

### [GeCO: Time Unconditional Flow Matching for Robotic Control](geco.md)

🎨 图像生成 / 机器人

将动作生成从固定积分转变为自适应迭代优化（使用静止速度场），提供无训练的 OOD 检测和基于任务复杂度的计算预算分配。

---

### [Harm or Humor: A Multimodal, Multilingual Benchmark for Overt and Covert Harmful Humor](harm-or-humor.md)

👁️ 多模态/VLM / AI安全

提出多模态多语言有害幽默检测基准（3000文本+6000图像+1200视频，英语/阿拉伯语），将有害幽默细分为显式和隐式两类，发现闭源模型显著优于开源，阿拉伯语表现远差于英语，凸显文化感知安全对齐的迫切需求。

---

### [HRI-SA: Multimodal Dataset for Human Situational Awareness in Human-Robot Teaming](hri-sa.md)

🎬 视频理解 / 机器人

收集 30 名参与者在搜救任务中的连续眼动+生理信号+机器人数据，眼动特征达 88.91% 召回率（融合后 91.51%），用于在线人类态势感知评估。

---

### [Learning Transferable Temporal Primitives for Video Reasoning via Synthetic Videos](learning.md)

🎬 视频理解

用合成几何视频构造 7.7K CoT + 7K RL 样本教授方向/速度/状态追踪等时序原语，7.7K 合成样本在 15 个时序推理基准上超越 165K 真实样本。

---

### [LED: A Benchmark for Evaluating Layout Error Detection in Document Analysis](led.md)

👁️ 多模态/VLM

提出 LED 基准系统性诊断文档布局预测中的 8 种结构错误类型，实现对 LLM 和多模态模型结构理解能力的细粒度评估。

---

### [LoST: Level of Semantics Tokenization for 3D Shapes](lost.md)

🧊 3D视觉

按语义显著性排序 3D 形状 token，使得早期前缀即可解码为完整可信的形状、后续 token 精细化——仅用 0.1%-10% 的 token 即超越现有自回归模型的重建指标。

---

### [MCoT-MVS: Multi-level Vision Selection by Multi-modal Chain-of-Thought Reasoning for Composed Image Retrieval](mcot-mvs.md)

👁️ 多模态/VLM

提出 MCoT-MVS，利用 MLLM 的链式思维推理将组合图像检索（CIR）中的用户意图分解为"保留/删除/目标"三部分文本，指导 patch 级和实例级双层视觉选择，在 CIRR 和 FashionIQ 上达到新 SOTA。

---

### [Motion-MLLM: Egomotion-Aware Video Representation for Efficient 3D Scene Understanding](motion-mllm.md)

🧊 3D视觉

融合 IMU 自运动数据与视频实现空间推理，将视觉内容锚定在物理轨迹中，以 1.40×/1.63× 更好的成本效率达到或超越 SOTA 精度。

---

### [NEO: A Unified Language Model for Large-Scale Search, Recommendation, and Reasoning](neo.md)

🎨 图像生成 / 推荐系统

让 LLM 交织自然语言和语义标识符（SID）实现对 1000 万级目录的搜索/推荐/推理统一，单模型支持多媒体类型且跨任务正迁移。

---

### [ProbeFlow: Training-Free Adaptive Flow Matching for Vision-Language-Action Models](probeflow.md)

🎨 机器人 / 图像生成

提出 ProbeFlow，一种无需训练的自适应 Flow Matching 推理框架，通过前瞻线性度探测（余弦相似度）动态分配 ODE 积分步数，在 MetaWorld 上将动作解码加速 14.8×（50步→2.6步），端到端延迟降低 2.8×，成功率保持不变。

---

### [SegFly: A 2D-3D-2D Paradigm for Aerial RGB-Thermal Semantic Segmentation](segfly.md)

🧊 3D视觉

用多视图几何从 <3% 手动标注的 RGB 图像自动传播标签到 RGB+热成像，构建 20K+ RGB + 15K+ RGB-T 对的基准，标注准确率达 91%/88%。

---

### [UniSAFE: A Comprehensive Benchmark for Safety Evaluation of Unified Multimodal Models](unisafe.md)

👁️ 多模态/VLM / AI安全

提出 UniSAFE，首个系统级 UMM 安全基准，覆盖 7 种 I/O 模态组合（包括首次评估多图组合和图像输出安全），通过"共享目标"设计控制跨任务对比，评估 15 个 SOTA UMM 发现图像输出任务比文本输出显著更脆弱、多图组合和多轮场景安全违规率最高。

---

### [VCoT-Bench: Can LLMs Reason Like Automated Theorem Provers for Rust Verification?](vcot-bench.md)

🧠 LLM推理

提出 VCoT-Bench（1988 道验证思维链任务），将求解器级推理暴露为显式步骤，评估 10 个 SOTA LLM 发现当前模型远达不到自动定理证明器的推理水平。

---
