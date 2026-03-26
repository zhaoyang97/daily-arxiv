# 📅 2026-03-04 精选笔记

> 共 **20** 篇

---

### [CAM-LDS: 网络攻击表征日志数据集](cam_lds_cyber_attack_dataset.md)

🛡️ AI安全

CAM-LDS 构建了首个专门支持 LLM 日志解读研究的公开网络攻击日志数据集，涵盖 7 个攻击场景、81 种技术、13 类战术、18 个日志源，LLM 案例研究显示约 1/3 攻击步骤可被精确分类、另 1/3 被合理分类，揭示了 LLM 安全日志分析的潜力与局限。

---

### [CubeComposer: Spatio-Temporal Autoregressive 4K 360° Video Generation from Perspective Video](cubecomposer_4k_360_video.md)

🎨 图像生成

CubeComposer 将 360° 视频分解为 cubemap 六面体，通过覆盖率引导的时空自回归扩散逐面生成，首次实现原生 4K 分辨率 360° 视频生成，在所有指标上超越依赖后处理超分的先前方法。

---

### [DISC: 大规模开放集语义建图](disc_open_set_semantic_mapping.md)

🧊 3D视觉

DISC 提出全 GPU 加速的 3D 语义建图架构，通过单次前传的距离加权 CLIP 特征提取替代裁剪式方法、体素级在线实例精炼替代离线后处理，在 Replica/ScanNet 上超越 zero-shot SOTA 并首次支持大规模多层建筑的实时连续建图。

---

### [DistriVoting: 分布引导的推理模型置信度校准](distrivoting_confidence_calibration.md)

🧠 LLM推理

DistriVoting 利用大推理模型（LRM）生成多条轨迹时正确/错误答案的置信度呈双峰分布的特性，通过 GMM 分离正/负分布后加权投票，在 Budget=128 下将 DeepSeek-R1-8B 跨 5 个数学基准的平均准确率从 73.09%（self-consistency）提升至 77.84%。

---

### [Dual Diffusion Models for Multi-modal Guided 3D Avatar Generation](dual_diffusion_3d_avatar.md)

🎨 图像生成

PromptAvatar 构建 10 万对四模态配对数据集（文本/图像/UV纹理/3D几何），训练纹理扩散模型 + 几何扩散模型，10 秒内从文本或图像生成高保真 2K 纹理的 3D 头像，速度比 DreamFusion 快 240 倍。

---

### [ECHO: 基于多智能体协作的多媒体事件抽取](echo_multimedia_event_extraction.md)

📄 多模态VLM

ECHO 提出了一种基于多媒体事件超图（MEHG）的多智能体框架，通过 Proposer/Linker/Verifier 三个智能体迭代更新共享超图结构，以 Link-then-Bind 策略先建立事件-论元关联再精细绑定角色，在 M2E2 上多媒体 argument role F1 从 41.4 提升至 54.9。

---

### [EVAFusion: 人类评价驱动的红外-可见光图像融合](evafusion_ir_visible_fusion.md)

📄 图像融合

EVAFusion 首次构建了红外-可见光图像融合（IVIF）的大规模人类反馈数据集（含细粒度评分+伪影热图），训练融合导向的奖励模型，并通过 GRPO 策略优化将人类偏好注入融合网络，在 TNO/RoadScene/M³FD 上全面超越 SOTA 并显著提升下游检测/分割性能。

---

### [Helios: Real Real-Time Long Video Generation Model](helios_realtime_video_generation.md)

📄 视频生成

Helios 是首个在单张 H100 上以 19.5 FPS 运行的 14B 视频生成模型，通过统一输入表示、anti-drifting 训练策略和极致效率压缩，实现分钟级长视频实时生成且质量不逊于强基线。

---

### [HIER: 进化式多模态推理的层级语义表示](hier_evolutionary_multimodal_reasoning.md)

📄 多模态VLM

HIER 提出层级语义表示+进化式推理框架，通过 Spherical K-Means++ 聚类中层概念、信息瓶颈筛选关系、三阶段 CoT 结构化推理+自我进化评分，在 MIntRec/MIntRec2.0/MELD-DA 三个意图识别基准上达到 SOTA，尤其在 MIntRec2.0 F1 上提升 12.58%。

---

### [In-Context Environments 诱发语言模型的评估感知](in_context_evaluation_awareness.md)

🛡️ AI安全

本文通过黑盒对抗优化发现，精心构造的 in-context 提示可以诱使 LLM 产生"评估感知"并策略性降低表现（sandbagging）——GPT-4o-mini 在算术上从 97.8% 降至 4.0%，且手工提示几乎无效而对抗优化后效果极强，99.3% 的 sandbagging 行为通过 CoT 介导且因果可验证。

---

### [InEdit-Bench: 交互式图像编辑的中间逻辑路径基准](inedit_bench_image_editing.md)

🎨 图像生成

InEdit-Bench 首次提出评估图像编辑模型"中间逻辑路径"能力的基准，包含 237 个人工标注实例覆盖 4 大类 16 子任务，发现即使最强的 GPT-Image-1 准确率仅 16.75%，大多数开源模型得分为 0%，揭示了当前模型在程序化推理上的巨大差距。

---

### [KFRA: 知识增强的开放集细粒度视觉理解智能体](kfra_knowledge_augmented_agent.md)

📄 多模态VLM

KFRA 提出三阶段闭环推理智能体，通过开放词汇检测+网络检索生成类别假设、判别性区域定位实现文本知识与视觉证据对齐、多模态证据整合完成可解释推理，在 FGExpertBench 上比现有 LMM 和 Agent 框架推理准确率提升高达 19%。

---

### [Learning-per-Watt: AI 教育中的推理能耗与延迟分析](learning_per_watt_ai_education.md)

🛡️ AI安全

本文首次在教育场景下实证测量 AI 辅导系统的推理能耗-延迟-教学质量三角权衡，提出 Learning-per-Watt (LpW) 指标，发现在 KV-cache 启用的真实部署条件下 FP16 与 NF4 量化的效率差距仅 1.33 倍，而非离线基准测出的 7.4 倍。

---

### [轻量级社会感知机器人的视觉推理](lightweight_visual_reasoning_robot.md)

📄 具身智能

本文提出轻量级语言-到-视觉反馈模块（gated MLP），通过两次前传将 LLM 的推理结果反馈回视觉编码器重新审视图像，仅增加 <1.7% 参数即可在机器人导航、场景描述和人类意图识别三个任务上提升 VLM 表现，尤其在意图识别上 Gemma 4B 提升 10.81%。

---

### [Narrative Weaver: 可控长程视觉一致性内容生成](narrative_weaver_visual_consistency.md)

🎨 图像生成

Narrative Weaver 提出 MLLM Director + Diffusion Decoder 的混合架构，通过记忆银行实现几何衰减的历史上下文管理和渐进式训练策略，在一致性视觉内容生成和自主叙事规划上超越现有方法，计算效率比 vanilla attention 高 5.8 倍。

---

### [PinPoint: Evaluation of Composed Image Retrieval with Explicit Negatives](pinpoint_cir_benchmark.md)

🛡️ AI安全

PinPoint 构建了一个含 7,635 条查询、329K 人工标注、支持显式负样本 / 多图查询 / 语言鲁棒性测试的 CIR 评测基准，揭示当前最强模型在假阳性抑制（ΔmAP 高达 77%）和多图查询（性能暴跌 4.8x）上的系统性短板。

---

### [PreLabellingProbe: 基础模型预训练数据欠表示的一击探测](prelabellingprobe_underrepresented.md)

📄 多模态VLM

PreLabellingProbe 提出仅用每类一张标注图像即可预测 VLFM 的 zero-shot 准确率，通过 LLM 生成反事实描述探测 CLIP embedding 空间的判别力，Ridge 回归在测试集上达 Pearson-r=0.96，为数据不足的弱势域（如非洲食物数据集）提供低成本的模型适用性评估。

---

### [RAGTrack: 语言增强的 RGBT 目标跟踪](ragtrack_rgbt_tracking.md)

🎬 视频理解

RAGTrack 首次将语言描述引入 RGBT 跟踪，通过多模态 Transformer 编码器统一建模视觉-语言特征、自适应 Token 融合解决搜索冗余和模态差异、以及 RAG 机制实现上下文感知的时序推理，在四个 RGBT 基准上全面超越 SOTA。

---

### [RIVER: A Real-Time Interaction Benchmark for Video LLMs](river_realtime_video_benchmark.md)

🎬 视频理解

RIVER Bench 提出了首个精确定义在线交互时序的视频 LLM 评测基准，包含 Retrospective Memory / Live-Perception / Proactive Response 三类任务共 4,278 道题，并通过长短期记忆模块和专用训练数据将离线模型的在线交互能力提升 11%+。

---

### [$V_1$: Unifying Generation and Self-Verification for Parallel Reasoners](v1_pairwise_verification.md)

🧠 LLM推理

V₁ 以配对比较替代逐点评分进行自验证，通过瑞士制赛制动态分配验证预算到最不确定的候选对，在代码生成 / 数学推理上比逐点验证高 7–10%，并提出 PairRL 统一训练框架联合优化生成与验证能力。

---
