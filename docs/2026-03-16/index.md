# 📅 2026-03-16 精选笔记

> 共 **20** 篇

---

### [Architecture-Agnostic Feature Synergy for Universal Defense Against Heterogeneous Generative Threats](atfs-defense.md)

🎨 图像生成 / AI安全

诊断了异构生成模型（扩散+GAN）在像素空间的梯度统计正交导致朴素集成防御失效的根本原因，提出 ATFS 框架通过引入目标引导图像将多模型防御统一为特征空间对齐任务，在 DM+GAN 和 DM+VAE 场景下全面超越专用防御方法和 PCGrad 梯度修正基线。

---

### [Mostly Text, Smart Visuals: Asymmetric Text-Visual Pruning for Large Vision-Language Models](atv-pruning.md)

🧩 多模态/VLM / 模型压缩

通过解耦文本/视觉通路的剪枝敏感性，发现文本通路高度敏感（必须用文本 token 校准）而视觉通路极度冗余（60% 稀疏度仅掉 0.75%），提出 ATV-Pruning 用全部文本 token + 按层自适应采样少量显著视觉 token 构建校准池，在 9 个多模态基准上超越 SOTA 剪枝方法。

---

### [DAIT: Distillation from Vision-Language Models to Lightweight Classifiers with Adaptive Intermediate Teacher Transfer](dait.md)

🧩 多模态/VLM / 模型压缩

提出两阶段蒸馏框架 DAIT——在 VLM 和轻量学生之间插入可训练的中间教师（甚至比学生更小），先用语义对齐+表示对齐+分类损失从冻结 VLM 中过滤出紧凑的任务相关知识，再用空间表示对齐蒸馏到轻量模型，在五个 FGVC 基准上全面超越 VL2Lite 等方法，Aircraft 上 ResNet-18 提升 11.57%、EfficientNet-B0 提升 18.81%。

---

### [Decision-Level Ordinal Modeling for Multimodal Essay Scoring with Large Language Models](dlom-essay-scoring.md)

📄 教育 NLP / 自动作文评分

提出 DLOM：把 LLM 作文评分从“生成文本再解析分数”改为“在分数 token 上直接做决策”，并进一步给出多模态门控融合（DLOM-GF）与距离感知正则（DLOM-DA），在 EssayJudge 与 ASAP/ASAP++ 上稳定优于生成式基线。

---

### [DOMINO: Towards Generalizable Robotic Manipulation in Dynamic Environments](domino-dynamic-manipulation.md)

🎬 机器人操作 / 视频理解 / VLA模型

引入 DOMINO 大规模动态操作数据集（35 任务/110K+ 轨迹）和 PUMA 动态感知 VLA 架构（场景级历史光流 + 物体级未来状态预测），在动态环境下比基线提升 6.3% 成功率，且动态数据训练可迁移增强静态任务表现。

---

### [Electrodermal Activity as a Unimodal Signal for Aerobic Exercise Detection in Wearable Sensors](eda-exercise.md)

📄 可穿戴传感 / 机器学习

系统评估仅基于皮肤电活动（EDA）信号区分静息状态与持续有氧运动的能力，在 30 名被试的 LOSO 验证下 EDA-only 分类器达到中等性能，相位时间动态特征和事件时序贡献最大，为 EDA 作为可穿戴活动推断的单模态输入建立了保守 baseline。

---

### [EditHF-1M: A Million-Scale Rich Human Preference Feedback for Image Editing](edithf-1m.md)

🎨 图像生成 / 多模态VLM

构建百万级图像编辑数据集 EditHF-1M（44.3K 源图×23 个编辑模型→101 万编辑图，29.1M 人类偏好对+148K MOS 评分，覆盖 43 类编辑任务×三维评估），基于此训练 MLLM 评估模型 EditHF 在三维度全面超越现有方法，并作为 reward model 通过 RL 显著提升 Qwen-Image-Edit 的编辑能力。

---

### [Flash-Unified: A Training-Free and Task-Aware Acceleration Framework for Native Unified Models](flash-unified.md)

🎨 图像生成 / 多模态VLM / LLM效率

首次系统分析统一多模态模型的内部计算冗余，发现显著的参数特化现象（生成和理解任务使用不同神经元子集），提出无训练的任务感知加速框架 FlashU，在 Show-o2 上实现 1.78×-2.01× 推理加速同时保持 SOTA 性能。

---

### [FSENet: Face-Guided Sentiment Boundary Enhancement for Weakly-Supervised Temporal Sentiment Localization](fsenet-sentiment.md)

🎬 多模态/VLM / 视频理解

提出 FSENet 框架利用面部特征引导时序情感定位——FSD 模块通过双分支建模（面部中心交互 + 全局情感感知）发现情感线索，PSSC 对比策略增强边界附近帧的情感语义区分，BSPG 将稀疏点标注平滑扩展为时序连续伪标签，在 TSL300 上 point-level 弱监督 mAP 达 21.45%，超越前 SOTA 5%+。

---

### [You've Got a Golden Ticket: Improving Generative Robot Policies With A Single Noise Vector](golden-ticket.md)

🎨 机器人 / 图像生成 / 扩散模型

提出 Golden Ticket 假说——固定一个精心选择的初始噪声向量代替每次从高斯分布采样，即可在完全冻结预训练扩散/流匹配策略的情况下提升下游任务性能，在 43 个任务中的 38 个提升成功率（模拟最高 +58%，真实硬件最高 +60%），无需训练额外网络。

---

### [GUI-CEval: A Hierarchical and Comprehensive Chinese Benchmark for Mobile GUI Agents](gui-ceval.md)

🧩 多模态/VLM / LLM Agent

构建首个中文移动端 GUI Agent 综合基准 GUI-CEval（201 款 App×4 设备类型，4,194 QA + 4,028 Agent 任务），采用感知/规划/反思/执行/评估五维层级结构，20 个模型评估揭示反思决策和自我评估是当前系统最大短板，最强模型在线成功率仅 33%。

---

### [HYDRA: Unifying Multi-modal Generation and Understanding via Representation-Harmonized Tokenization](hydra.md)

🎨 多模态/VLM / 图像生成

提出 HYDRA-TOK（表示协调 ViT），通过 Gen-ViT→GSB 瓶颈→Sem-ViT 的渐进式学习，在单一纯 ViT 架构中统一生成的结构细节和理解的语义抽象，rFID 0.08 刷新重建记录，理解基准平均超出现有统一模型 ~10 分。

---

### [LLMind: Bio-inspired Training-free Adaptive Visual Representations for Vision-Language Models](llmind-bio-vision.md)

🧩 多模态/VLM / LLM效率

受人类视觉系统的中央凹编码和皮层放大启发，提出无训练框架 LLMind——用 Möbius 变换实现非均匀自适应采样(BASS)，结合闭环语义反馈(CSF)在测试时优化采样参数，仅用 1%/3%/5% 像素即可保留 82%/92%/97% 全分辨率性能，VQAv2 平均提升 +20%、Seed-Bench +38%、A-OKVQA +37%。

---

### [MER-Bench: A Comprehensive Benchmark for Multimodal Meme Reappraisal](mer-bench.md)

🎨 多模态/VLM / 图像生成

定义 Meme Reappraisal 新任务（将负面 meme 转化为正面表达同时保持场景/实体/布局），构建 MER-Bench（3117 对 meme + 细粒度多模态标注）和基于 MLLM-as-a-Judge 的结构化评测框架（8 维指标 + RFS 综合分数），在 14 个 SOTA 图像编辑/多模态生成系统上揭示了结构保持+情感控制联合约束下的显著不足。

---

### [MMSpec: Benchmarking Speculative Decoding for Vision-Language Models](mmspec.md)

🧩 多模态/VLM / LLM效率

构建首个 VLM 推测解码基准 MMSpec（600 样本×6 任务×10 种算法），揭示三个关键发现（文本方法在多模态退化、视觉感知在大 batch 更重要、吞吐量≠延迟），并提出即插即用的 ViSkip 方法达到 SOTA。

---

### [Multi-Turn Physics-Informed Vision-Language Model for Physics-Grounded Anomaly Detection](physics-vlm-anomaly.md)

🧩 多模态/VLM / 异常检测

针对 VLM 在基于物理规律的异常检测上的根本缺陷（缺乏动力学因果理解），提出物理先验指令微调框架——将物体属性、运动范式、动态约束编码为结构化先验并通过多轮对话逐步注入 VLM，在 Phys-AD 基准上将 AUROC 从 66.9% 提升至 96.7%，因果解释质量 LLM score 达 0.777。

---

### [POLCA: Stochastic Generative Optimization with LLM](polca.md)

🧠 LLM Agent / LLM推理

将 LLM 优化复杂系统（prompt 设计、多轮 agent 等）形式化为随机生成式优化问题，提出 POLCA 框架（优先队列管理探索-利用 + Gemini embedding 驱动的 ε-Net 保持候选多样性 + LLM Summarizer 元学习），理论证明在随机性下收敛到近最优解，在 τ-bench/HotpotQA/VeriBench/KernelBench 四个基准上一致超越 GEPA 和 OpenEvolve。

---

### [SAMA: A Skill-augmented Agentic Framework and Benchmark for Multi-Video Understanding](sama-mvx.md)

🎬 视频理解 / LLM Agent

提出 MVX-Bench（将 11 个经典 CV 任务重构为多视频 QA，1,442 问题/4,255 视频）和 SAMA agent 框架（视觉工具执行底层分析 + 任务特定技能提供专业推理能力 + 冲突感知验证迭代修正矛盾信息），在跨视频推理上系统性超越 GPT 系列和开源基线，消融验证各组件有效性。

---

### [VAREX: A Benchmark for Multi-Modal Structured Extraction from Documents](varex.md)

🧩 多模态/VLM / 文档理解

提出 Reverse Annotation 流水线——从可填充 PDF 模板出发注入合成值生成确定性 ground truth，构建 1,777 篇文档×1,771 个独立 schema×四种输入模态的文档结构化抽取基准 VAREX，在 20 个模型上揭示 <4B 模型的主要瓶颈是结构化输出合规性（schema echo 导致 45-65pp 精度损失）而非视觉能力，且 2B 微调即可弥补。

---

### [Video-CoE: Reinforcing Video Event Prediction via Chain of Events](video-coe.md)

🎬 多模态/VLM / 视频理解

提出 Chain of Events (CoE) 范式，通过构造时序事件链实现细粒度历史事件建模，用两阶段训练（CoE-SFT 建立逻辑推理 + CoE-GRPO 解锁时序定位），在 FutureBench 上 3B 模型超越 72B 基线和 GPT-5，7B 模型达到 75.0% 平均准确率。

---
