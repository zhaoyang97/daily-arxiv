# 📅 2026-03-19 精选笔记

> 共 **22** 篇

---

### [AutoScreen-FW: An LLM-based Framework for Resume Screening](autoscreen-fw.md)

🛡️ AI安全

用开源 LLM + ICL 实现隐私保护的简历自动筛选，性能匹配/超越商业 LLM 且速度更快。

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

通过跨模态理据迁移实现可解释的社交媒体危机分类，提升2-35%且零样本准确率达80%。

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

首个用离散 Flow Matching 从质谱预测分子结构的框架，在6个指标中5个达到SOTA，通过迭代优化+化学式约束生成合理分子候选。

---

### [GenVideoLens: Where LVLMs Fall Short in AI-Generated Video Detection?](genvideolens.md)

👁️ 多模态/VLM / AI安全

提出 GenVideoLens，一个 15 维细粒度 AI 生成视频检测基准（400 高仿真合成+100 真实视频，6000+ 专家标注），揭示 LVLM 在光学一致性、物理交互和时序因果推理上的系统性弱点，且模型几乎不利用时序信息做真伪判断。

---

### [HiMu: Hierarchical Multimodal Frame Selection for Long Video Question Answering](himu.md)

🎬 视频理解 / 多模态/VLM

提出 HiMu，用单次 LLM 调用将查询分解为层次逻辑树，叶节点路由到轻量多模态专家（CLIP/OCR/ASR/CLAP），通过模糊逻辑算子自下而上组合产生帧满意度曲线——在 Qwen3-VL 8B + 16 帧配置下超越所有帧选择器，在 GPT-4o 下以 10× 更少 FLOPs 超越 Agent 方法。

---

### [LVOmniBench: Pioneering Long Audio-Video Understanding Evaluation for Omnimodal LLMs](lvomnibench.md)

🎬 视频理解 / 多模态/VLM

提出 LVOmniBench，首个专门评估全模态 LLM 在长时音视频（10-90分钟，共140小时）上的跨模态理解能力的基准，包含 275 视频+1014 人工标注 QA 对，发现开源模型准确率 <35%，Gemini 3 Pro 峰值仅 ~65%。

---

### [MAPG: Multi-Agent Probabilistic Grounding for Vision-Language Navigation](mapg.md)

🧊 3D视觉 / 机器人

将度量-语义语言查询分解为多个组件，由VLM智能体分别接地并概率组合用于机器人导航，包含 MAPG-Bench 基准和真实机器人部署。

---

### [Matryoshka Gaussian Splatting](matryoshka-gaussian-splatting.md)

🧊 3D视觉

将 Matryoshka 嵌套表示思想应用于 3D Gaussian Splatting，通过按重要性排序高斯基元并用随机预算训练，使单个模型的任意前缀子集都能产生连贯渲染，实现连续 LoD 控制且不牺牲全容量质量。

---

### [MemMA: Coordinating the Memory Cycle through Multi-Agent Reasoning and In-Situ Self-Evolution](memma.md)

🦾 LLM Agent

提出 MemMA，一个即插即用的多智能体框架，通过前向路径（Meta-Thinker 指导记忆构建和迭代检索）和后向路径（原位自演化记忆修复）协调记忆循环的三个阶段（构建-检索-利用），在 LoCoMo 上一致超越现有记忆增强基线。

---

### [MonoArt: Progressive Structural Reasoning for Monocular Articulated 3D Reconstruction](monoart.md)

🧊 3D视觉

提出 MonoArt，一个端到端的单目铰接3D物体重建框架，通过渐进式结构推理（几何→零件→运动→运动学树），在 PartNet-Mobility 上实现 SOTA 重建精度和推理速度，无需多视图、视频生成或检索库。

---

### [PowerFlow: Unlocking the Dual Nature of LLMs via Principled Distribution Matching](powerflow.md)

🧠 LLM推理

提出 PowerFlow，将无监督 LLM 微调形式化为 α-幂分布匹配问题——α>1 锐化分布增强推理、α<1 平化分布释放创造力——通过长度感知的 Trajectory-Balance 目标解决自回归长度偏差，在无外部监督下匹配甚至超越有监督的 GRPO。

---

### [Revisiting Autoregressive Models for Generative Image Classification](revisiting.md)

🎨 图像生成

证明自回归模型通过跨多种token顺序的序边际化预测可超越扩散分类器，效率提升25×同时达到与判别式自监督模型竞争的分类性能。

---

### [SEAR: Simple and Efficient Adaptation of Visual Geometric Transformers for RGB+Thermal 3D Reconstruction](sear.md)

🧊 3D视觉

提出 SEAR，用 LoRA 适配器+模态专用 camera token+混合批处理策略，以不到 5% 参数量将 VGGT 几何基础模型适配到 RGB-热成像联合 3D 重建，仅需 ~15K 配对图像训练即在 AUC@30 上超越 SOTA 29%+。

---

### [Seeking Universal Shot Language Understanding Solutions](seeking.md)

👁️ 多模态/VLM

提出 SLU-SUITE（490K标注QA×33种电影任务）和 UniShot/AgentShots 模型，在电影镜头语言理解上超越任务专用集成和商业VLM 22%。

---

### [T-QPM: Enabling Temporal Out-Of-Distribution Detection and Domain Generalization for VLMs](t-qpm.md)

👁️ 多模态/VLM

提出 T-QPM，将 CLIP 的 OOD 检测从静态双模式匹配扩展到时序四模式匹配（图像×文本 × ID×OOD），通过时间步特定的视觉原型+轻量融合权重+ATC正则化，在时序变化环境下显著超越静态基线。

---

### [TexEditor: Structure-Preserving Text-Driven Texture Editing](texeditor.md)

🎨 LLM效率 / 图像生成

通过 TexBlender 合成数据和 TexBench 真实基准实现文本驱动的结构保持纹理编辑，在物体外观修改上一致超越基线。

---

### [VEGA-3D: Generation Models Know Space — Unleashing Implicit 3D Priors for Scene Understanding](vega-3d.md)

🧊 3D视觉 / 多模态VLM

将预训练视频生成模型（如 Wan2.1）作为"潜在世界模拟器"，通过噪声注入激活其隐式3D先验，并用 token 级自适应门控融合机制将几何特征与语义特征结合，无需显式3D标注即可大幅提升 MLLM 的3D场景理解和空间推理能力。

---

### [Not All Features Are Created Equal: A Mechanistic Study of Vision-Language-Action Models](vla-mechanistic-study.md)

🤖 机器人 / 多模态VLM

对 6 种 VLA 模型（80M-7B）进行大规模机械可解释性研究（39.4万+ rollout），发现视觉通路主导动作生成、语言敏感性取决于任务结构而非模型设计、多通路架构呈现 expert 编码运动程序 / VLM 编码目标语义的一致性分工。

---
