# 📅 2026-03-19 精选笔记

> 共 **22** 篇

---

### [AutoScreen-FW: An LLM-based Framework for Resume Screening](autoscreen-fw.md)

🛡️ AI安全

提出 AutoScreen-FW，一个本地部署的开源 LLM 简历筛选框架，通过三种代表性样本选择策略（多样性/相似性/聚类）+ 评价准则 + persona 描述进行 few-shot ICL，使 Qwen3-8B 在日本潜力型招聘场景下匹配甚至超越 GPT-5-mini，且每份简历筛选速度快 24-51%。

---

### [Balanced Thinking: Improving Chain of Thought Training in Vision Language Models](balanced-thinking.md)

👁️ 多模态/VLM / LLM推理

提出 SCALe-SFT（Scheduled Curriculum Adaptive Loss），通过在 SFT 阶段动态调整 think 和 answer 段的损失权重（从重推理逐渐转向重答案），解决推理数据中 token 不均衡问题，仅 SFT 即可匹配 SFT+GRPO 的效果且节省 ~6/7 训练时间。

---

### [Counting Circuits: Mechanistic Interpretability of Visual Reasoning in Large Vision-Language Models](counting-circuits.md)

👁️ 多模态/VLM

以计数任务为最小化探针，通过 Visual Activation Patching 和 HeadLens 两种新方法发现 LVLM 中结构化的"计数电路"（4类功能注意力头），仅用 8000 张简单合成图微调计数机制即可在 OOD 真实计数上提升 8.36% 且通用视觉推理提升 1.54%。

---

### [Cross-Modal Rationale Transfer for Explainable Humanitarian Classification](cross-modal.md)

👁️ 多模态/VLM

提出 VLTCrisis，一个可解释的多模态危机推文分类框架：先用 ViLT 编码器联合学习文本理据（有监督）和图像理据（通过跨模态对齐零样本迁移），再仅基于提取的理据进行分类，实现 interpretable-by-design。在 CrisisMMD 上 Macro-F1 比 baseline 高 2-35%，零样本泛化到新数据集达 80% 准确率。

---

### [CubiD: Cubic Discrete Diffusion — Discrete Visual Generation on High-Dimensional Representation Tokens](cubid.md)

🎨 图像生成

提出 Cubic Discrete Diffusion (CubiD)，首个在高维表示 token（768维）上进行离散生成的方法，通过在 h×w×d 三维张量上做细粒度逐元素掩码预测，在 ImageNet-256 上达到 1.88 FID，同时验证了离散化后的 token 同时保持理解和生成能力。

---

### [FLAC: Few-shot Acoustic Synthesis with Multimodal Flow Matching](flac.md)

🎨 图像生成 / 语音音频

提出 FLAC，首个将 Flow Matching 应用于少样本房间脉冲响应（RIR）合成的生成模型，仅用 1 条录音+深度图即可在新房间生成空间一致的 RIR，超越需要 8 条录音的 SOTA 方法，同时引入 AGREE 声学-几何联合嵌入用于场景一致性评估。

---

### [FlowMS: Flow Matching for De Novo Structure Elucidation from Mass Spectra](flowms.md)

🎨 图像生成 / 科学计算

提出 FlowMS，首个将离散 flow matching 用于质谱条件下从头分子结构生成的框架，通过线性插值噪声路径 + CTMC 去噪 + 化学式约束，在 NPLIB1 基准的 6 个指标中 5 个达到 SOTA：9.15% top-1 准确率（比 DiffMS 提升 9.7%）和 7.96 top-10 MCES（比 MS-BART 提升 4.2%）。

---

### [GenVideoLens: Where LVLMs Fall Short in AI-Generated Video Detection?](genvideolens.md)

👁️ 多模态/VLM / AI安全

提出 GenVideoLens，一个 15 维细粒度 AI 生成视频检测基准（400 高仿真合成+100 真实视频，6000+ 专家标注），揭示 LVLM 在光学一致性、物理交互和时序因果推理上的系统性弱点，且模型几乎不利用时序信息做真伪判断。

---

### [HiMu: Hierarchical Multimodal Frame Selection for Long Video Question Answering](himu.md)

🎬 视频理解 / 多模态/VLM

提出 HiMu，一个无训练帧选择框架：用单次 text-only LLM 调用将查询分解为层次逻辑树 → 叶节点路由到轻量多模态专家（CLIP/OVD/OCR/ASR/CLAP）→ 信号归一化+时序平滑 → 模糊逻辑算子自下而上组合成帧满意度曲线 → top-K 帧送入 LVLM。在 Video-MME 上以约 10× 更少 FLOPs 接近 Agent 方法性能，全面超越所有相似度选择器。

---

### [LVOmniBench: Pioneering Long Audio-Video Understanding Evaluation for Omnimodal LLMs](lvomnibench.md)

🎬 视频理解 / 多模态/VLM

提出 LVOmniBench，首个专门评估全模态 LLM 在长时音视频（10-90分钟，共140小时）上的跨模态理解能力的基准，包含 275 视频+1014 人工标注 QA 对，发现开源模型准确率 <35%，Gemini 3 Pro 峰值仅 ~65%。

---

### [MAPG: Multi-Agent Probabilistic Grounding for Vision-Language Navigation](mapg.md)

🧊 3D视觉 / 机器人

提出 MAPG（Multi-Agent Probabilistic Grounding），将自然语言度量-语义查询（如"冰箱右边 2 米"）分解为锚点+空间关系+度量约束，由多个 VLM Agent 分别接地并通过概率核组合生成规划器可用的 3D 目标分布。在新提出的 MAPG-Bench 上将目标定位误差从 5.82m 降至 0.07m（98.8% 降幅）。

---

### [Matryoshka Gaussian Splatting](matryoshka-gaussian-splatting.md)

🧊 3D视觉

将 Matryoshka 嵌套表示思想应用于 3D Gaussian Splatting，通过按重要性排序高斯基元并用随机预算训练，使单个模型的任意前缀子集都能产生连贯渲染，实现连续 LoD 控制且不牺牲全容量质量。

---

### [MemMA: Coordinating the Memory Cycle through Multi-Agent Reasoning and In-Situ Self-Evolution](memma.md)

🦾 LLM Agent

提出 MemMA，一个即插即用的多智能体框架，通过前向路径（Meta-Thinker 指导 Memory Manager 构建 + Query Reasoner 迭代检索）和后向路径（原位自演化记忆修复：合成探测 QA→验证→失败转修复）协调记忆循环的三个阶段，在 LoCoMo 上整体 ACC 从 75.66% 提升至 81.58%。

---

### [MonoArt: Progressive Structural Reasoning for Monocular Articulated 3D Reconstruction](monoart.md)

🧊 3D视觉

提出 MonoArt，一个端到端的单目铰接3D物体重建框架，通过渐进式结构推理（几何→零件→运动→运动学树），在 PartNet-Mobility 上实现 SOTA 重建精度和推理速度，无需多视图、视频生成或检索库。

---

### [PowerFlow: Unlocking the Dual Nature of LLMs via Principled Distribution Matching](powerflow.md)

🧠 LLM推理

提出 PowerFlow，将无监督 LLM 微调形式化为 α-幂分布匹配问题——α>1 锐化分布增强推理、α<1 平化分布释放创造力——通过长度感知的 Trajectory-Balance (LA-TB) 目标解决自回归长度偏差。在推理任务上无监督匹配甚至超越 GRPO（有监督），在创造力任务上突破质量-多样性 Pareto 边界。

---

### [Revisiting Autoregressive Models for Generative Image Classification](revisiting.md)

🎨 图像生成

揭示固定 token 顺序是 AR 生成式分类器的关键瓶颈，利用 any-order AR 模型（RandAR）通过对多种排列取序边际化（order-marginalized）估计类条件 log-likelihood，在 ImageNet 及 OOD 基准上全面超越扩散分类器，效率提升 25×，并首次与 DINOv2 等 SOTA 自监督方法竞争。

---

### [SEAR: Simple and Efficient Adaptation of Visual Geometric Transformers for RGB+Thermal 3D Reconstruction](sear.md)

🧊 3D视觉

提出 SEAR，用 LoRA 适配器+模态专用 camera token+混合批处理策略，以不到 5% 参数量将 VGGT 几何基础模型适配到 RGB-热成像联合 3D 重建，仅需 ~15K 配对图像训练即在 AUC@30 上超越 SOTA 29%+。

---

### [Seeking Universal Shot Language Understanding Solutions](seeking.md)

👁️ 多模态/VLM

提出 SLU-SUITE（490K 人工标注 QA × 33 个电影任务 × 6 维度）和两套方案：UniShot（单模型均衡泛化，动态平衡数据混合）和 AgentShots（专家路由集群，零样本超越 Gemini-3.0-Pro 22%），揭示 VLM 用于镜头语言理解的瓶颈是语义对齐而非视觉感知。

---

### [T-QPM: Enabling Temporal Out-Of-Distribution Detection and Domain Generalization for VLMs](t-qpm.md)

👁️ 多模态/VLM

提出 T-QPM，将 CLIP 的 OOD 检测从静态双模式匹配扩展到时序四模式匹配（图像×文本 × ID×OOD），通过时间步特定的视觉原型+轻量融合权重+ATC正则化，在时序变化环境下显著超越静态基线。

---

### [TexEditor: Structure-Preserving Text-Driven Texture Editing](texeditor.md)

🎨 图像生成 / 图像编辑

提出 TexEditor，通过 Blender 合成的 TexBlender 数据集做 SFT 冷启动 + StructureNFT 强化学习（结合指令遵循和结构保持奖励）两阶段训练，在文本驱动纹理编辑中一致超越 Nano Banana Pro 等 SOTA 编辑模型，同时提出 TexBench（真实世界基准）和 TexEval（结合结构一致性的评估指标）。

---

### [VEGA-3D: Generation Models Know Space — Unleashing Implicit 3D Priors for Scene Understanding](vega-3d.md)

🧊 3D视觉 / 多模态VLM

将预训练视频生成模型（如 Wan2.1）作为"潜在世界模拟器"，通过噪声注入激活其隐式3D先验，并用 token 级自适应门控融合机制将几何特征与语义特征结合，无需显式3D标注即可大幅提升 MLLM 的3D场景理解和空间推理能力。

---

### [Not All Features Are Created Equal: A Mechanistic Study of Vision-Language-Action Models](vla-mechanistic-study.md)

🤖 机器人 / 多模态VLM

对 6 种 VLA 模型（80M-7B）进行大规模机械可解释性研究（39.4万+ rollout），发现视觉通路主导动作生成、语言敏感性取决于任务结构而非模型设计、多通路架构呈现 expert 编码运动程序 / VLM 编码目标语义的一致性分工。

---
