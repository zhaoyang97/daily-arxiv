# 📅 2026-03-16 精选笔记

> 共 **9** 篇

---

### [Mostly Text, Smart Visuals: Asymmetric Text-Visual Pruning for Large Vision-Language Models](atv-pruning.md)

👁️ 多模态/VLM / 模型压缩

通过解耦文本/视觉通路的剪枝敏感性，发现文本通路高度敏感（必须用文本 token 校准）而视觉通路极度冗余（60% 稀疏度仅掉 0.75%），提出 ATV-Pruning 用全部文本 token + 按层自适应采样少量显著视觉 token 构建校准池，在 9 个多模态基准上超越 SOTA 剪枝方法。

---

### [DAIT: Distillation from Vision-Language Models to Lightweight Classifiers with Adaptive Intermediate Teacher Transfer](dait.md)

👁️ 多模态/VLM / 模型压缩

提出两阶段蒸馏框架 DAIT——在 VLM 和轻量学生之间插入可训练的中间教师（甚至比学生更小），先用语义对齐+表示对齐+分类损失从冻结 VLM 中过滤出紧凑的任务相关知识，再用空间表示对齐蒸馏到轻量模型，在五个 FGVC 基准上全面超越 VL2Lite 等方法，Aircraft 上 ResNet-18 提升 11.57%、EfficientNet-B0 提升 18.81%。

---

### [Flash-Unified: A Training-Free and Task-Aware Acceleration Framework for Native Unified Models](flash-unified.md)

🎨 图像生成 / 多模态VLM / LLM效率

首次系统分析统一多模态模型的内部计算冗余，发现显著的参数特化现象（生成和理解任务使用不同神经元子集），提出无训练的任务感知加速框架 FlashU，在 Show-o2 上实现 1.78×-2.01× 推理加速同时保持 SOTA 性能。

---

### [HYDRA: Unifying Multi-modal Generation and Understanding via Representation-Harmonized Tokenization](hydra.md)

🎨 多模态/VLM / 图像生成

提出 HYDRA-TOK（表示协调 ViT），通过 Gen-ViT→GSB 瓶颈→Sem-ViT 的渐进式学习，在单一纯 ViT 架构中统一生成的结构细节和理解的语义抽象，rFID 0.08 刷新重建记录，理解基准平均超出现有统一模型 ~10 分。

---

### [MER-Bench: A Comprehensive Benchmark for Multimodal Meme Reappraisal](mer-bench.md)

🎨 多模态/VLM / 图像生成

定义 Meme Reappraisal 新任务（将负面 meme 转化为正面表达同时保持场景/实体/布局），构建 MER-Bench（3117 对 meme + 细粒度多模态标注）和基于 MLLM-as-a-Judge 的结构化评测框架（8 维指标 + RFS 综合分数），在 14 个 SOTA 图像编辑/多模态生成系统上揭示了结构保持+情感控制联合约束下的显著不足。

---

### [MMSpec: Benchmarking Speculative Decoding for Vision-Language Models](mmspec.md)

👁️ 多模态/VLM / LLM效率

构建首个 VLM 推测解码基准 MMSpec（600 样本×6 任务×10 种算法），揭示三个关键发现（文本方法在多模态退化、视觉感知在大 batch 更重要、吞吐量≠延迟），并提出即插即用的 ViSkip 方法达到 SOTA。

---

### [POLCA: Stochastic Generative Optimization with LLM](polca.md)

🧠 LLM Agent / LLM推理

将 LLM 优化复杂系统（prompt 设计、多轮 agent 等）形式化为随机生成式优化问题，提出 POLCA 框架（优先队列管理探索-利用 + Gemini embedding 驱动的 ε-Net 保持候选多样性 + LLM Summarizer 元学习），理论证明在随机性下收敛到近最优解，在 τ-bench/HotpotQA/VeriBench/KernelBench 四个基准上一致超越 GEPA 和 OpenEvolve。

---

### [SAMA: A Skill-augmented Agentic Framework and Benchmark for Multi-Video Understanding](sama-mvx.md)

🎬 视频理解 / LLM Agent

提出 MVX-Bench（将 11 个经典 CV 任务重构为多视频 QA，1,442 问题/4,255 视频）和 SAMA agent 框架（视觉工具执行底层分析 + 任务特定技能提供专业推理能力 + 冲突感知验证迭代修正矛盾信息），在跨视频推理上系统性超越 GPT 系列和开源基线，消融验证各组件有效性。

---

### [Video-CoE: Reinforcing Video Event Prediction via Chain of Events](video-coe.md)

🎬 多模态/VLM / 视频理解

提出 Chain of Events (CoE) 范式，通过构造时序事件链实现细粒度历史事件建模，用两阶段训练（CoE-SFT 建立逻辑推理 + CoE-GRPO 解锁时序定位），在 FutureBench 上 3B 模型超越 72B 基线和 GPT-5，7B 模型达到 75.0% 平均准确率。

---
