# 📅 2026-03-22 精选笔记

> 共 **20** 篇

---

### [Amortized Variational Inference for Logistic Regression with Missing Covariates](amortized-vi.md)

🎨 图像生成

提出 AV-LR，用摊销变分推断直接在缺失协变量空间做推断（无需额外隐变量）——单个推断网络同时估计回归参数和缺失机制，在 60% MNAR 下 AUC=0.771 超越 SAEM 和 MICE，训练快 67×。

---

### [AutoKernel: Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search](autokernel.md)

🗣️ LLM/NLP

提出 AutoKernel，用 LLM Agent 自动化 GPU Kernel 优化——模拟专家工程师的"写→Profile→保留/回退"循环，结合 Amdahl 定律指导优化优先级和五阶段正确性验证，在 H100 上 RMSNorm 加速 5.29× vs PyTorch eager、3.44× softmax vs torch.compile。

---

### [Benchmarking Bengali Dialectal Bias: A Multi-Stage Framework Integrating RAG-Based Translation and Human-Augmented RLAIF](bengali-bias.md)

🗣️ LLM/NLP

首个系统量化孟加拉语方言偏差的框架——用 RAG 管道生成 9 种方言的 4000 问题变体，用 LLM-as-judge 替代完全失效的传统指标（BLEU CCC=0.065 vs LLM-judge CCC=0.506），对 19 个 LLM 进行 68,395 次 RLAIF 评估，发现偏差与方言语言学发散度高度系统相关（Chittagong 最差 5.44/10 vs Tangail 最优 7.68/10）。

---

### [Uncertainty-Aware Knowledge Distillation for Multimodal Large Language Models](beta-kd.md)

🧩 多模态/VLM

提出 Beta-KD，将知识蒸馏重新解释为带 Gibbs 先验的贝叶斯推断问题——用 Laplace 近似推导出闭式的不确定性自适应权重，自动平衡多目标蒸馏中的数据监督和教师引导，在 ScienceQA 上提升 ~4.7%。

---

### [Closed-form Conditional Diffusion Models for Data Assimilation](closed-form-diffusion.md)

🎨 图像生成

提出无需训练的扩散数据同化方法——用核密度估计(KDE)对状态-观测联合分布做闭式 score 函数推导，在反向扩散 ODE 中仅需 9-17 步就完成贝叶斯更新，在 Lorenz 系统上 Wasserstein-2 距离 5.74 vs EnKF 12.94 vs SIR 14.85，特别在小集合(N≤250)下优势显著。

---

### [A Generalised Exponentiated Gradient Approach to Enhance Fairness in Binary and Multi-class Classification](fairness-geg.md)

🛡️ AI安全

提出 Generalised Exponentiated Gradient (GEG) 算法，将经典 Exponentiated Gradient 公平学习框架从二分类推广到多分类——将公平约束建模为线性不等式、通过乘性权重迭代求解 min-max 博弈，在 10 个数据集（7 多分类 + 3 二分类）上公平性提升最高 92%（准确率代价 ≤14%）。

---

### [Aggregation Alignment for Federated Learning with Mixture-of-Experts under Data Heterogeneity](fedalign-moe.md)

🛡️ AI安全

提出 FedAlign-MoE，解决联邦学习中 MoE 模型的两大难题——通过一致性加权的路由分布对齐解决异构门控偏好 + 语义感知的专家聚合解决跨客户端专家语义漂移，在严重 Non-IID 下比 FedAvg 提升 8-10%。

---

### [KG-Hopper: Empowering Compact Open LLMs with Knowledge Graph Reasoning via Reinforcement Learning](kg-hopper.md)

🧠 LLM推理

提出 KG-Hopper，用强化学习训练 7B LLM 在单轮推理中完成多跳知识图谱问答——将整个 KG 遍历和推理过程嵌入模型的 "thinking" 阶段，在 8 个 KBQA benchmark 上超越 70B 多步方法并接近 GPT-4o-mini。

---

### [KHMP: Frequency-Domain Kalman Refinement for High-Fidelity Human Motion Prediction](khmp.md)

🎨 图像生成

提出 KHMP，在频率域（DCT）上用 Kalman 滤波抑制运动预测的高频抖动——训练时加入时序平滑和关节角度约束，推理时用 SNR 自适应 Kalman 滤波器精炼高频 DCT 系数，在保持运动多样性的同时显著改善物理合理性。

---

### [The Library Theorem: How External Organization Governs Agentic Reasoning Capacity](library-theorem.md)

🤖 机器人

提出 Library Theorem，将 Transformer 上下文窗口形式化为 I/O 页面，证明顺序扫描 vs B-tree 索引检索存在指数级效率差异——M=500 条目下索引仅需 1 次页读取 vs 顺序需 21 次，M=2000 时 token 成本差 153.6×。

---

### [More Than Sum of Its Parts: Deciphering Intent Shifts in Multimodal Hate Speech Detection](more-than-sum.md)

🧩 多模态/VLM

提出 H-VLI benchmark 和 ARCADE 框架——用"法庭辩论"式多代理对抗推理来检测隐式多模态仇恨言论，其中文本和图像单独看无害但组合后产生仇恨语义，在隐式案例上显著超越现有方法。

---

### [Identity-Consistent Video Generation under Large Facial-Angle Variations](mv2id.md)

🎬 视频理解

提出 Mv²ID 框架，用多视角参考图引导视频生成——通过 Region Masking 防止"视角锁定"复制伪影 + Reference-Decoupled RoPE 区分时空编码，在大角度人脸变化下保持身份一致性并生成自然运动。

---

### [PAS3R: Pose-Adaptive Streaming 3D Reconstruction for Long Video Sequences](pas3r.md)

🧊 3D视觉

提出 PAS3R，根据帧间相机运动幅度和图像频率丰富度动态调节状态更新强度——平衡稳定性和适应性，配合轨迹一致性 loss 和时空稳定化滤波，在长视频(1000帧)流式三维重建上保持亚线性误差增长。

---

### [PLR: Plackett-Luce for Reordering In-Context Learning Examples](plr-icl.md)

🧠 LLM推理

提出 PLR，用 Plackett-Luce 分布模型替代离散排列搜索来优化 ICL 示例顺序——通过 Gumbel perturb-and-sort 高效采样排列并迭代集中概率到高性能序列上，在分类和数学推理任务上比 baseline 提升 9-15%。

---

### [Enhancing Reasoning Accuracy in Large Language Models during Inference Time](reasoning-accuracy.md)

🧠 LLM推理

系统比较三种推理时增强策略——Self-Consistency（控温采样+LLM 语义投票, 64.9% vs 贪心 56.2%）、双模型交叉验证（精度优先, 适合高风险场景）和自反思（+3.4pp, 小模型收益有限），为不同风险等级场景提供策略选择指南。

---

### [Relax Forcing: Relaxed KV-Memory for Consistent Long Video Generation](relax-forcing.md)

🎬 视频理解

提出 Relax Forcing，用结构化稀疏 KV-Memory 替代稠密时序缓存来生成一致的长视频——将历史帧分解为 Sink（全局锚点）/History（动态选择的中程运动）/Tail（近程连续性）三个功能角色，在 60 秒视频生成上比 Deep Forcing 提升 1.24%，动态度提升 66.8%。

---

### [When Models Judge Themselves: Unsupervised Self-Evolution for Multimodal Reasoning](self-judge.md)

🧩 多模态/VLM

提出 Actor-Judge 自进化框架——同一个 MLLM 既做推理(Actor)又做质量评估(Judge), 用 Self-Consistency 探索 + Judge 调制 + 能量归一化 GRPO 训练, 无需人工标注在数学视觉推理上提升 5.9%, 达到监督方法的同等水平。

---

### [Silent Commitment Failure in Instruction-Tuned Language Models: Evidence of Governability Divergence Across Architectures](silent-commitment.md)

🗣️ LLM/NLP

揭示"静默承诺失败"现象——指令调优 LLM 在犯错时输出自信流畅且无任何预警信号，提出"可治理性"框架量化错误可检测/可纠正程度，发现可治理性由架构预训练决定（52×差异）而非指令调优（±0.32×）。

---

### [Text-Image Conditioned 3D Generation (TIGON)](tigon.md)

🧊 3D视觉

提出 TIGON，首个研究文本+图像混合条件的原生 3D 生成方法——双分支 DiT（图像分支提供外观细节、文本分支提供语义引导）通过零初始化 cross-modal bridge 做早期融合 + 速度场平均做晚期融合，在低信息视角下显著优于单模态方法。

---

### [Test-Time Adaptation via Cache Personalization for Facial Expression Recognition in Videos](tta-cap.md)

🧩 多模态/VLM

提出 TTA-CaP，一种无梯度的缓存式测试时自适应方法——结合离线个性化源域原型和动态目标域正/负缓存，通过三重门控机制可靠更新缓存，在视频表情识别上超越需要梯度更新的昂贵 prompt-tuning 方法。

---
