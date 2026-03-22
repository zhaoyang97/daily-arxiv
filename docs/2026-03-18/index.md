# 📅 2026-03-18 精选笔记

> 共 **20** 篇

---

### [CycleCap: Improving VLMs Captioning via Self-Supervised Cycle Consistency](cyclecap.md)

🎨 图像生成 / 多模态/VLM

将循环一致性（图→文→图重建相似度）作为 GRPO 奖励信号自监督微调 VLM，仅需原始图像无需标注数据，在 1B-7B 模型上一致提升 captioning 和减少幻觉。

---

### [Directing the Narrative: Controlling Coherence and Style in Story Generation](directing.md)

🎨 图像生成 / 视频理解

提出两阶段框架在 FLUX.1 上实现一致性故事生成：第一阶段用 Group-Shared Attention 在 batch 内共享高分辨率视觉 token 实现无损身份保持，第二阶段用 DPO 对齐人类审美，在 ViStoryBench 上 CIDS +10.0、CSD +18.7，6 项指标中 5 项 SOTA。

---

### [EvoGuard: An Extensible Agentic RL-based Framework for Practical AI-Generated Image Detection](evoguard.md)

🧩 多模态/VLM / AI安全

提出 EvoGuard，将异构 AIGI 检测器封装为可调用工具，用 MLLM Agent 通过能力感知的动态编排机制多轮调用和推理，仅需二值标签的 GRPO 训练，实现 SOTA 检测精度和无需重训练的即插即用可扩展性。

---

### [Fine-Grained Post-Training Quantization for LVLMs with Quantization-aware Integrated Gradients](fine-grained.md)

🧩 多模态/VLM / 模型压缩

借鉴可解释性中的公理化归因方法，提出量化感知积分梯度 (QIG) 将 LVLM 量化敏感度测量从模态级推进到 token 级，在 W3A16 下 LLaVA-onevision-7B 平均精度提升 1.60%，与全精度差距仅 1.33%。

---

### [FineViT: Progressively Unlocking Fine-Grained Perception with Dense Recaptions](finevit.md)

🧩 多模态/VLM

提出 FineViT，一个从零训练的三阶段渐进式视觉编码器（MIM初始化→高分辨率对比学习→LLM对齐），配合 4.5 亿区域级标注数据集 FineCap-450M，在零样本识别/检索和 MLLM 多模态理解上全面超越 SigLIP2 和 Qwen-ViT。

---

### [FloorPlan-VLN: Floor Plan Guided Vision-Language Navigation](floorplan-vln.md)

🤖 机器人

提出平面图引导的 VLN 新范式——用现成平面图替代冗长逐步指令作为全局空间先验，构建 10K+ episode 数据集（语义标注平面图 + Matterport3D 轨迹 + 简洁指令），提出 FP-Nav 通过双视角时空对齐视频 + 辅助推理任务实现平面图-视觉-指令对齐，导航成功率相对提升 60%+，在真实四足机器人上零样本部署验证。

---

### [Flow Matching Policy with Entropy Regularization (FMER)](flow.md)

🎮 强化学习

用 ODE 基的 Flow Matching 代替 SDE 基扩散作为在线 RL 策略，通过优势加权的 conditional FM loss + 可解析熵正则化实现原则性最大熵优化，在多峰/稀疏 FrankaKitchen 任务上超越 SOTA，训练速度比 QVPO 快 7×。

---

### [GeCO: Time Unconditional Flow Matching for Robotic Control](geco.md)

🤖 机器人 / 生成模型

将机器人动作生成从固定时间表积分转化为对时间无关的稳态速度场做迭代优化，自然实现自适应推理步数（简单动作早退、复杂动作多细化）和零训练 OOD 检测（场范数作为异常信号），可无缝插入 π₀ 等 VLA 模型作为 flow-matching head 替代。

---

### [Harm or Humor: A Multimodal, Multilingual Benchmark for Overt and Covert Harmful Humor](harm-or-humor.md)

🧩 多模态/VLM / AI安全

提出多模态多语言有害幽默检测基准（3000文本+6000图像+1200视频，英语/阿拉伯语），将有害幽默细分为显式和隐式两类，系统评估SOTA开源和闭源模型，发现闭源模型显著优于开源，隐式有害幽默是所有模型的最大盲区，阿拉伯语安全对齐严重滞后。

---

### [HRI-SA: Multimodal Dataset for Human Situational Awareness in Human-Robot Teaming](hri-sa.md)

🤖 机器人 / 人机交互

提出首个开放的人机协作情境感知 (SA) 检测数据集 HRI-SA，收集 30 人搜救任务中的眼动+生理+交互+机器人数据，系统定义感知型和理解型两种 SA 延迟并提供逐 5 秒连续标注，验证通用眼动特征可有效检测感知延迟（recall=88.91%），融合上下文信息后 F1 从 67.63% 提升到 80.38%。

---

### [Learning Transferable Temporal Primitives for Video Reasoning via Synthetic Videos](learning.md)

🎬 视频理解

通过代码生成的合成几何视频构造 7.7K CoT + 7K RL 样本，教授模型方向/速度/状态追踪等基础时序理解原语，仅用 7.7K 合成数据就在 15 个视频推理基准上超越 Video-R1 的 165K 真实样本（**数据效率 21 倍**）。

---

### [LED: A Benchmark for Evaluating Layout Error Detection in Document Analysis](led.md)

📄 多模态/文档理解

首次定义文档布局分析中 8 种结构错误类型（缺失、幻觉、大小错误、分割、合并、重叠、重复、误分类），通过可控合成错误注入构建 LED 基准（5K 文档、70K 元素），用三层递进任务评估多模态模型，揭示即使 GPT-4V 在元素级诊断上也极弱（F1<0.35），填补文档评估十年空白。

---

### [LoST: Level of Semantics Tokenization for 3D Shapes](lost.md)

🧊 3D视觉/生成模型

按语义显著性（而非几何细节）排序 3D token 序列，使早期前缀即可解码为完整可信形状，后续 token 逐步精细化——仅需 0.1%-10% 的 token 即超越现有自回归模型，通过新颖的 RIDA 损失在无 3D DINO 的条件下实现 3D 语义对齐。

---

### [MCoT-MVS: Multi-level Vision Selection by Multi-modal Chain-of-Thought Reasoning for Composed Image Retrieval](mcot-mvs.md)

🧩 多模态/VLM

提出 MCoT-MVS，利用 MLLM 的链式思维推理将组合图像检索（CIR）中的用户意图分解为"保留/删除/目标"三部分文本，指导 patch 级和实例级双层视觉选择，在 CIRR 和 FashionIQ 上达到新 SOTA。

---

### [Motion-MLLM: Egomotion-Aware Video Representation for Efficient 3D Scene Understanding](motion-mllm.md)

🧊 3D视觉

将低成本 IMU 自运动数据作为新模态注入 MLLM，通过级联运动-视觉关键帧筛选和非对称跨模态融合，以 ~4B 参数在 VSI-Bench 上超越 78B 模型，成本效率比 2D/3D 方法分别高 1.40×/1.63×。

---

### [NEO: A Unified Language Model for Large-Scale Search, Recommendation, and Reasoning](neo.md)

📋 推荐系统/LLM

NEO 让 decoder-only LLM 学习交织自然语言与语义标识符（SID），在单个端到端模型中支持对 1000 万级异质目录的推荐/搜索/用户理解三统一，无需工具调用，通过三阶段递进式适配实现跨任务正迁移，在真实流媒体平台验证性能超越多年优化的专用系统。

---

### [ProbeFlow: Training-Free Adaptive Flow Matching for Vision-Language-Action Models](probeflow.md)

🎨 机器人 / 图像生成

提出 ProbeFlow，一种无需训练的自适应 Flow Matching 推理框架，通过前瞻线性度探测（余弦相似度）动态分配 ODE 积分步数，在 MetaWorld 上将动作解码加速 14.8×（50步→2.6步），端到端延迟降低 2.8×，成功率保持不变。

---

### [SegFly: A 2D-3D-2D Paradigm for Aerial RGB-Thermal Semantic Segmentation](segfly.md)

🧊 3D视觉/遥感

SegFly 提出 **2D-3D-2D** 范式——从手动标注的 <3% 高分辨率航拍 RGB 图像提升到 3D 语义点云，再投影到全部 RGB 和热图像，实现 91% RGB 自动标注精度 + 88% 热成像精度，通过 3D 点云作为中介实现无硬件同步的 RGB-热配准（87% 像素精度），构建首个大规模航拍 RGB-T 多模态分割基准（20K+ RGB / 15K+ RGB-T）。

---

### [UniSAFE: A Comprehensive Benchmark for Safety Evaluation of Unified Multimodal Models](unisafe.md)

🧩 多模态/VLM / AI安全

提出 UniSAFE，首个系统级 UMM 安全基准，覆盖 7 种 I/O 模态组合（包括首次评估多图组合和图像输出安全），通过"共享目标"设计控制跨任务对比，评估 15 个 SOTA UMM 发现图像输出任务比文本输出显著更脆弱、多图组合和多轮场景安全违规率最高。

---

### [VCoT-Bench: Can LLMs Reason Like Automated Theorem Provers for Rust Verification?](vcot-bench.md)

🧠 LLM推理/形式验证

通过 VCoT-Lift 框架将 Z3 求解器的低层推理提升为高层 Verus 验证步骤，构造 1,988 道涵盖缺失度/类型/位置三维度的 VCoT 完成任务，评估 10 个 SOTA LLM 发现即使最强模型在 10% 缺失率下仅 ~77% 准确率，100% 缺失接近崩溃（~17%）。

---
