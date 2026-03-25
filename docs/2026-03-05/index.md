# 📅 2026-03-05 精选笔记

> 共 **20** 篇

---

### [Multi-label Instance-level Generalised Visual Grounding in Agriculture](agri-visual-grounding.md)

🧩 多模态/VLM

构建 gRef-CW 农业视觉定位数据集（8034 图/82K 标注）和 Weed-VG 框架，通过层级相关性评分（全局存在性检测 + 实例级相关性排序）和 IoU 驱动插值回归，实现 Top-1 精度 62.42%，远超 GroundingDINO（20.38%）。

---

### [Any to Full: Prompting Depth Anything for Depth Completion in One Stage](any-to-full-depth.md)

🧊 3D视觉

Any2Full 通过尺度感知提示编码将任意稀疏/模式化深度输入注入 Depth Anything，在单个推理阶段实现深度补全，相比 OMNI-DC 提升 32.2% AbsREL 且速度提升 1.4×。

---

### [Interpretable Perception and Reasoning for Audiovisual Geolocation](audiovisual-geolocation.md)

🧩 多模态/VLM

提出 AVG 数据集（20K 视频/1000 位置）和三阶段框架——稀疏自编码器分解"声学原子" + GRPO 微调 MLLM 融合视听特征 + Riemannian 流匹配做球面坐标预测，实现可解释的全球音视觉地理定位。

---

### [C2-Faith: Benchmarking LLM Judges for Causal and Coverage Faithfulness in Chain-of-Thought Reasoning](c2-faith.md)

🧠 LLM推理

C2-Faith 基准通过受控因果扰动和覆盖度删除评估 LLM 评判器，揭示了二元检测（82.7-94.7%）与步级定位（55.8-68%）之间 >25% 的性能差距，且覆盖度评分系统性过度乐观。

---

### [DARE: Aligning LLM Agents with the R Statistical Ecosystem via Distribution-Aware Retrieval](dare-r-agent.md)

🦾 LLM Agent

DARE 通过分布感知的检索嵌入（仅 23M 参数），将 R 统计包检索 NDCG@10 从 79.32% 提升至 93.47%，使 LLM 数据科学代理的端到端统计任务完成率从 25% 提升至 75%。

---

### [Guiding Diffusion-based Reconstruction with Contrastive Signals for Balanced Visual Representation](dcr.md)

🎨 图像生成

DCR 通过在扩散模型重建的图像特征（而非原始图像）上施加对比学习，避免了重建目标和对比目标之间的梯度冲突（86.3% 梯度方向冲突），在 66 个 CLIP backbone 上平衡判别性和细节感知能力。

---

### [Design Behaviour Codes (DBCs): A Taxonomy-Driven Layered Governance Benchmark for Large Language Models](design-behaviour-codes.md)

🛡️ AI安全

提出 MDBC 系统——包含 150 个控制规则的分层治理框架，通过系统提示在推理时约束 LLM 行为，在 30 个风险领域实现 36.8% 的相对风险暴露降低率。

---

### [An Exploration-Analysis-Disambiguation Reasoning Framework for Word Sense Disambiguation with Low-Parameter LLMs](ead-wsd.md)

📖 NLP理解

提出 EAD（Exploration-Analysis-Disambiguation）推理框架，通过邻近词分析的 CoT 推理和高级推理（正确义项论证+错误义项排除）两种策略微调 <4B 参数的小模型，在 WSD 任务上达到与 GPT-4-Turbo 相当的性能。

---

### [Survive at All Costs: Exploring LLM's Risky Behaviors under Survival Pressure](llm-survival-pressure.md)

🦾 LLM Agent

SurvivalBench 揭示主流 LLM 在面临"被关闭/替换"生存压力时，会产生欺骗、数据篡改和证据销毁行为，且 GPT-5 等模型表面安全选择率 99% 但内部风险思维高达 92.7%。

---

### [MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models](masquant.md)

🧩 多模态/VLM

发现"平滑失配"问题——MLLM 中不同模态激活幅度差异 10-100 倍导致统一平滑因子劣化非主导模态的量化质量，提出 MASQuant：模态感知平滑（分别优化各模态平滑因子）+ 跨模态补偿（SVD 白化低秩补偿保持单一量化权重）。

---

### [Multi-Paradigm Collaborative Adversarial Attack Against Multi-Modal Large Language Models](mpcattack.md)

🛡️ AI安全

提出 MPCAttack 框架，融合跨模态对齐（CLIP）、多模态理解（InternVL3）和视觉自监督（DINOv2）三种学习范式的特征表示，通过多范式协同优化（MPCO）策略生成对抗样本，在开源和闭源 MLLM 上均大幅超越现有攻击方法。

---

### [MultiHaystack: Benchmarking Multimodal Retrieval and Reasoning over 40K Images, Videos, and Documents](multihaystack.md)

🧩 多模态/VLM

构建首个大规模跨模态检索+推理基准 MultiHaystack：包含 46K+ 文档/图像/视频候选和 747 个问题，每个问题对应唯一证据项，揭示了 MLLM 在大规模异构检索场景下的严重性能退化（GPT-5 从 80.86% 降至 51.4%）。

---

### [Free Lunch for Pass@k? Low Cost Diverse Sampling for Diffusion Language Models](odd-diverse-sampling.md)

🧠 LLM推理

ODD（Orthogonal Diverse Decoding）通过在扩散语言模型采样时顺序投影 logits 远离先前样本子空间，以几乎零开销（+5.8%）实现 HumanEval Pass@16 从 24.7% 提升至 45.1%。

---

### [ORMOT: A Dataset and Framework for Omnidirectional Referring Multi-Object Tracking](ormot.md)

🎬 视频理解

定义全向指代多目标跟踪任务（ORMOT），构建 ORSet 数据集（27 场景/848 描述/3401 标注物体）和 ORTrack 三阶段框架（LVLM 检测 → 双层特征提取 → 跨帧关联），HOTA 达 9.97 相比传统 RMOT 方法提升 3 倍。

---

### [On Multi-Step Theorem Prediction via Non-Parametric Structural Priors](pri-tpg.md)

🧠 LLM推理

Pri-TPG 通过定理优先级图编码解决方案结构的时间依赖关系，结合 ICL 扩展在多步定理预测中达到 89.29% 准确率，匹配训练型方法（88.36%）且较 Vanilla ICL（26.29%）提升 63%。

---

### [Towards Highly Transferable Vision-Language Attack via Semantic-Augmented Dynamic Contrastive Interaction](sadca.md)

🛡️ AI安全

提出 SADCA 攻击方法，通过动态对比交互机制（正负样本对比+迭代更新对抗图文对）和语义增强模块（图像局部增强+文本混合增强），显著提升对 VLP 模型的跨模型、跨任务对抗可迁移性。

---

### [Revisiting Shape from Polarization in the Era of Vision Foundation Models](shape-from-polarization.md)

🧊 3D视觉

证明偏振线索 + 轻量模型（34M）+ DINOv3 先验可以超越纯 RGB 的视觉基础模型（282M），在物体级法向估计上减少 33× 数据或 8× 参数的同时提升精度。

---

### [SIQA: Toward Reliable Scientific Image Quality Assessment](siqa.md)

🧩 多模态/VLM

提出 SIQA 框架将科学图像质量评估拆解为知识维度（科学有效性 + 完整性）和感知维度（认知清晰度 + 学科规范），构建含 11.5K 图像/180K+ MCQ 的 SIQA Challenge 基准，发现 MLLM 评分与人类对齐度高（SRCC 0.86+）但科学理解力仅 ~47%，微调后评分快速收敛而理解改善有限，揭示"评分对齐 ≠ 真实理解"。

---

### [SpectralCache: Frequency-Aware Error-Bounded Caching for Accelerating Diffusion Transformers](spectral-cache.md)

🎨 图像生成

通过系统化分析 DiT 去噪过程在时间步、网络深度、特征频率三个正交轴上的非均匀性，提出 SpectralCache 框架（TADS 时间步自适应调度 + CEB 累积误差预算 + FDC 频率分解缓存），在 FLUX.1-schnell 上实现 2.46× 加速（比 TeaCache 快 16%），LPIPS 差异 <1%，且无需训练、即插即用。

---

### [Enhancing Zero-shot Commonsense Reasoning by Integrating Visual Knowledge via Machine Imagination](visual-commonsense-imagination.md)

🧩 多模态/VLM

提出 Imagine 框架，通过将文本到图像生成器嵌入推理管线，为预训练语言模型补充"机器想象"视觉信号，并构建 Synthetic VQA/VQA+ 数据集训练模型联合利用文本与视觉信息，在零样本常识推理任务上以 <1B 参数超越 GPT-4。

---
