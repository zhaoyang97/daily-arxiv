# 📅 2026-03-25 精选笔记

> 共 **19** 篇

---

### [A³: Towards Advertising Aesthetic Assessment](a3-advertising.md)

🧩 多模态/VLM / 图像美学评估 / 广告

提出 A³ 广告美学评估框架，包含理论驱动的三阶段评估范式 A³-Law（感知注意→形式兴趣→欲望影响）+ 30K 图像 120K 标注的 A³-Dataset + 经 SFT+GRPO 训练的 A³-Align 模型 + A³-Bench 基准，在广告美学评估上超越现有 MLLM。

---

### [Leave No Stone Unturned: Audio-Visual Deepfake Detection](av-deepfake-detect.md)

🛡️ AI安全 / 深伪检测

提出整体性音视频深伪检测方法：不仅检测单模态伪造痕迹和音视频不一致，还联合利用两种信号源——单模态固有特征和跨模态内在一致性——实现对未见生成器的鲁棒泛化，显著超越仅依赖单一信号源的现有方法。

---

### [PaddleOCR-VL: Boosting Document Parsing with Coarse-to-Fine Visual Processing](coarse-to-fine-doc.md)

📄 多模态VLM / 文档解析

提出 PaddleOCR-VL，一个粗到细的文档解析框架：粗阶段用轻量级 VRFM（基于 RT-DETR + pointer network）检测有效区域并预测阅读顺序，细阶段用 0.9B 的 VLM 精细识别裁剪区域，仅用 2561 个 vision token 就在 OmniDocBench v1.5 上取得 92.62 分 SOTA，超越参数量 80 倍以上的大模型。

---

### [DepthArb: Training-Free Depth-Arbitrated Generation for Occlusion-Robust Image Synthesis](deptharb.md)

🎨 图像生成 / 扩散模型 / 空间可控生成

提出 DepthArb，一个无需训练的遮挡感知图像生成框架，通过注意力仲裁调制（AAM）抑制背景注意力泄漏 + 空间紧凑性控制（SCC）防止注意力发散，在扩散模型的交叉注意力层中显式解决深度排序冲突，在自建 OcclBench 和 OverLayBench 上显著超越现有方法。

---

### [EMoT: Enhanced Mycelium of Thought — Bio-Inspired Hierarchical Reasoning](emot.md)

🧠 LLM推理 / Prompting

EMoT 受菌丝网络启发，提出四层认知处理架构替代线性/树状推理（CoT/ToT）：引入持久化记忆、策略性休眠（暂停低回报探索分支）和跨领域合成能力，让 LLM 在复杂多步推理中维持全局一致性和资源效率。

---

### [HGGT: Robust and Flexible 3D Hand Mesh Reconstruction from Uncalibrated Images](hggt.md)

🧊 3D视觉 / 手部重建 / 多视角几何

首次提出无需标定的前馈式多视角 3D 手部网格重建框架 HGGT：基于 VGGT backbone 提取多视角特征，通过可学习 hand/camera token 的交叉注意力联合推断手部 MANO 参数和相机位姿，结合单目+真实多视角+合成多视角的混合训练数据，在标准基准上超越 SOTA。

---

### [Language-Assisted Image Clustering Guided by Discriminative Relational Signals and Adaptive Semantic Centers](laic.md)

🧩 多模态/VLM / 图像聚类 / 提示学习

提出新的语言辅助图像聚类（LAIC）框架：通过跨模态关系矩阵（ridge regression 重建图像-文本表示）挖掘更具判别力的自监督信号 + 通过提示学习在 CLIP 语义空间中学习连续类别语义中心来产生最终聚类分配，在 8 个基准上平均超越 SOTA 2.6%。

---

### [Marchuk: Efficient Global Weather Forecasting from Mid-Range to Sub-Seasonal Scales via Flow Matching](marchuk.md)

🎨 图像生成 / 天气预报 / Flow Matching

提出 Marchuk，一个仅 276M 参数的隐空间 flow matching DiT 天气预报模型，在 ERA5 数据上可预测长达 30 天的全球天气，性能匹敌 1.6B 参数的 LaDCast 且推理速度快 6 倍（30 天 50 成员集合预报仅需 7.5 分钟/H100）。

---

### [Invisible Threats from Model Context Protocol: Generating Stealthy Injection Payload via Tree-based Adaptive Search](mcp-tip.md)

🦾 AI安全 / LLM Agent / Prompt Injection

提出 TIP（Tree-structured Injection for Payloads），针对 MCP 工具增强 Agent 的黑盒 prompt 注入攻击框架：将 payload 生成建模为树搜索问题，通过粗到细优化 + 路径感知反馈机制生成语义自然的注入 payload，在无防御下 ASR>95%、有防御下>50%，且查询量比现有自适应攻击低一个数量级。

---

### [EPOS-VLM: Memory-Augmented Vision-Language Agents for Persistent and Semantically Consistent Object Captioning](memory-vl-agent.md)

📄 多模态VLM / 具身智能

提出 EPOS-VLM，一个统一的记忆增强 Vision-Language-Action 模型，将数据关联、物体描述和导航策略整合到单一自回归框架中，通过物体级 episodic memory 的文本序列化使 VLM 能跨视角推理，在 HM3D 上实现标准 captioning 指标 +11.86% 和跨视角描述一致性 +7.39% 的提升。

---

### [MMTIT-Bench: Multilingual Multi-Scenario Text-Image Machine Translation](mmtit-bench.md)

📄 多模态VLM / NLP

MMTIT-Bench 是首个人工验证的端到端文本-图像机器翻译 benchmark，覆盖多语言和多视觉场景，通过认知-感知-推理三层评估体系系统测试 VLLM 在图像内文字翻译中的能力，揭示现有模型在低资源语言和复杂视觉场景下的重大不足。

---

### [OmniWeaving: Towards Unified Video Generation with Free-form Composition and Reasoning](omniweaving.md)

📄 视频生成 / 多模态

OmniWeaving 提出开源统一视频生成框架，将文生视频、图生视频、视频编辑、视频推理等多种任务整合到单一模型中，支持自由组合式输入（图文混合 prompt），弥补了开源社区与 Seedance-2.0 等商业系统在全能视频生成上的巨大差距。

---

### [PP-OCRv5: A Specialized 5M-Parameter Model Rivaling Billion-Parameter Vision-Language Models on OCR Tasks](pp-ocrv5.md)

🧩 多模态/VLM / OCR / 数据中心AI

PP-OCRv5 是仅 5M 参数的轻量级两阶段 OCR 系统，通过系统化的数据中心方法论（从数据难度、准确性、多样性三个维度优化 22.6M 训练集），在标准 OCR 基准上达到与 billion 参数级 VLM 可比的识别精度，同时具备更精确的定位、更少的幻觉和极高的部署效率。

---

### [QuadFM: Foundational Text-Driven Quadruped Motion Dataset for Generation and Control](quadfm.md)

🤖 机器人 / 四足运动生成 / 数据集

发布首个大规模四足机器人文本-动作数据集 QuadFM（11784 个动作片段+三层文本标注共 35352 条描述），覆盖运动、交互和情感表达行为，配套 Gen2Control RL 框架联合训练动作生成器和通用运动控制器，在 Unitree Go2 上实现 <500ms 实时文本驱动动作合成。

---

### [SafeFlow: Real-Time Text-Driven Humanoid Whole-Body Control via Physics-Guided Rectified Flow and Selective Safety Gating](safeflow.md)

🤖 机器人 / 人形机器人控制 / 运动生成

提出 SafeFlow，一个面向真实人形机器人的实时文本驱动全身控制框架：高层用物理引导的 rectified flow 在 VAE 隐空间生成可执行运动轨迹 + reflow 蒸馏实现 NFE=1 实时推理 + 三阶段安全门控（语义 OOD 检测→生成稳定性过滤→运动学硬约束）选择性执行，在 Unitree G1 上实现 98.5% 成功率和严格安全保障。

---

### [ScrollScape: Unlocking 32K Image Generation With Video Diffusion Priors](scrollscape.md)

🎨 图像生成 / 超高分辨率 / 视频扩散先验

将极端宽高比（EAR）图像生成重构为视频扫描任务，提出 ScrollScape 框架：ScanPE 将空间坐标映射到时序帧实现"移动相机"效果 + ScrollSR 利用视频超分先验逐帧提升分辨率到 32K，在 3K 张训练图上微调 Wan2.1 即可生成全局连贯、无重复的超宽画幅图像。

---

### [SOMA: Strategic Orchestration and Memory-Augmented System for VLA Robustness](soma.md)

🦾 具身智能 / LLM Agent

SOMA 为 Vision-Language-Action (VLA) 模型增加长期记忆、因果故障归因和动态干预能力，使机器人控制器在分布外（OOD）感知噪声和环境变化下保持鲁棒，通过 in-context 适应实现无需重新训练的策略修正。

---

### [Thinking with Tables (TWT): Enhancing Multi-Modal Tabular Understanding via Neuro-Symbolic Reasoning](thinking-with-tables.md)

🧩 多模态/VLM / 表格理解 / 神经符号推理

提出 TWT，一个面向表格-视觉多模态理解（TVMU）的程序辅助神经符号推理框架：通过代码交互式推理与沙盒环境交互实现信息提取和特征建模，采用两阶段训练（SFT + 自适应损失缩放 RL），在 8 个基准上平均超越 baseline 10%，性能匹敌或超越商业 SOTA LLM。

---

### [ViHOI: Human-Object Interaction Synthesis with Visual Priors](vihoi.md)

🎨 图像生成 / 人体动作生成 / 人物-物体交互

提出 ViHOI，利用 VLM（Qwen2.5-VL）从 2D 参考图像中提取视觉先验和文本先验，通过 Q-Former 压缩为紧凑 token 后注入扩散模型，实现即插即用地提升多种 HOI 运动生成模型的质量和泛化性，在 FullBodyManipulation 和 BEHAVE 两个数据集上达到 SOTA。

---
