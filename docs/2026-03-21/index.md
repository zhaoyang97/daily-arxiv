# 📅 2026-03-21 精选笔记

> 共 **20** 篇

---

### [AC4A: Access Control for Agents](ac4a.md)

🗣️ LLM/NLP / AI安全

提出 AC4A，首个统一的 LLM Agent 访问控制框架，支持 API 和浏览器两类 Agent，通过层级资源类型树 + 资源值规范 + 动作的权限三元组实现细粒度权限控制（如只允许查看本周日历而非整个 API 权限），灵感来自 Unix 文件系统权限模型。

---

### [AEGIS: From Clues to Verdicts -- Graph-Guided Deep Vulnerability Reasoning via Dialectics and Meta-Auditing](aegis.md)

🧠 LLM推理 / AI安全 / 软件工程

识别 LLM 漏洞检测的根本问题——agent 辩论和 RAG 均在"无根据的推理空间"中运作（缺乏假设特定的证据基础），提出 AEGIS 多 agent 框架：先从代码异常中发现线索(Clues)，再通过仓库级 Code Property Graph 按需切片重建每变量依赖链，Verifier Agent 在封闭证据边界内构建正反辩证论证，独立 Audit Agent 拥有一票否决权防止幻觉裁决。PrimeVul 上首次突破 100 Pairwise Correct（达 122），FPR 降低 54.4%，成本仅 $0.09/样本，无需训练。

---

### [Attention in Space: Functional Roles of VLM Heads for Spatial Reasoning](attention-in-space.md)

🧩 多模态/VLM

通过机制可解释性分析发现 VLM 中空间推理头极其稀缺（<9% 超过 0.001 重要性），提出 CogVSR 数据集和探测框架识别认知头，并通过 Spatial Head Activation (SHA) 激活潜在空间头，InternVL3-2B 提升 >10%。

---

### [BenchBench: Benchmarking Automated Benchmark Generation](benchbench.md)

🎬 视频理解 / LLM评估

提出 BenchBench，评估 LLM 自动生成 benchmark 能力的三阶段流水线——从种子 benchmark 提取领域卡 → LLM 设计者生成配额控制的题目套件 → 多模型答题面板验证——发现 benchmark 设计能力与答题能力仅弱相关（Spearman ρ≈0.37），生成 16.7K 题目覆盖 CS/数学/医学/ToM 四个领域。

---

### [Code-MIE: A Code-style Model for Multimodal Information Extraction with Scene Graph and Entity Attribute Knowledge Enhancement](code-mie.md)

🧩 多模态/VLM

提出 Code-MIE，首个将代码风格模板扩展到多模态信息抽取的框架，通过将场景图和实体属性整合到统一的 Python 函数模板中，在 M3D、Twitter-15/17、MNRE 四个数据集上全面超越六个基线（F1 提升最高 6.94%）。

---

### [CTCal: Rethinking Text-to-Image Diffusion Models via Cross-Timestep Self-Calibration](ctcal.md)

🎨 图像生成

提出 CTCal，利用扩散模型在小时间步（低噪声）建立的可靠文本-图像对齐（cross-attention map）来校准大时间步（高噪声）的学习，为文本-图像对应提供显式监督，在 SD 2.1 和 SD 3 上均显著提升组合生成能力（T2I-CompBench++ 和 GenEval）。

---

### [Democratizing AI: A Comparative Study in Deep Learning Efficiency and Future Trends in Computational Processing](democratizing-ai.md)

📦 模型压缩 / 系统 / 深度学习基准测试

在 CIFAR-10 和 Horse2Zebra 数据集上系统基准测试 Conv6/VGG16/ResNet18/CycleGAN 四种模型在 TensorFlow/PyTorch 两个框架下的 CPU vs GPU 性能差异：GPU 加速比从轻量模型 Conv6 的 246× 到生成模型 CycleGAN 的 11× 不等，TensorFlow 推理延迟比 PyTorch 低约 15%，并用多项式回归预测 GPU 显存增长趋势。

---

### [DiscoUQ: Structured Disagreement Analysis for Uncertainty Quantification in LLM Agent Ensembles](discouq.md)

🦾 LLM Agent

提出 DiscoUQ，分析多 Agent LLM 系统分歧的结构（语言特征：证据重叠/论证强度/分歧深度 + 嵌入几何：聚类距离/离散度/凝聚度）来产生校准后的置信度估计，在 4 个 benchmark 上以 AUROC 0.802 和 ECE 0.036 超越简单投票和 LLM 聚合基线，特别在"弱分歧"区间提升最大。

---

### [Memory-Efficient Fine-Tuning Diffusion Transformers via Dynamic Patch Sampling and Block Skipping](dit-blockskip.md)

🎨 图像生成 / 扩散模型 / 高效微调

提出 DiT-BlockSkip：(1) 时间步感知的动态 patch 采样——高时间步大 patch 学全局结构、低时间步小 patch 学细节，统一 resize 到低分辨率；(2) 基于 cross-attention masking 识别关键 block 后跳过非关键 block 并预计算残差特征。在 FLUX/SANA 上，30% 跳过率+256 分辨率训练即可达到 LoRA@512 水平（DINO 0.7194 vs 0.7324），内存减少约 71%。

---

### [E-SocialNav: Efficient Socially Compliant Navigation with Language Models](e-socialnav.md)

🤖 机器人 / 社会导航 / 小语言模型

评估 GPT-4o/Claude 在社会导航中的零样本能力（效果很差），提出 E-SocialNav：基于 Phi-2-2.7B + SigLIP 的小语言模型，通过两阶段训练（SFT on 多轮对话 + DPO on 单轮偏好对）在小数据（265 张图）下超越零样本大模型，最佳配置 SFT(projector)+DPO(lora) 达到 SMS 0.846、FPS 2.354、AA 0.550。

---

### [IBCapsNet: Information Bottleneck Capsule Network for Noise-Robust Representation Learning](ibcapsnet.md)

📦 模型压缩

提出 IBCapsNet，用信息瓶颈原理替代胶囊网络的迭代动态路由——将主胶囊压缩为全局上下文后通过类别特定 VAE 推断正则化潜在胶囊——在 MNIST/SVHN 上匹配 CapsNet 准确率，噪声下平均提升 17.1%（钳位加性噪声），同时训练快 2.54×、推理快 3.64×。

---

### [ME-IQA: Memory-Enhanced Image Quality Assessment via Re-Ranking](me-iqa.md)

🧩 多模态/VLM

提出 ME-IQA，一个即插即用的测试时记忆增强重排序框架，通过混合记忆库检索 + VLM 作为概率比较器 + Thurstone Case V 融合，缓解推理型 VLM 在 IQA 任务中的离散坍缩问题。

---

### [Reasoning Topology Matters: Network-of-Thought for Complex Reasoning Tasks](network-of-thought.md)

🧠 LLM推理

提出 Network-of-Thought (NoT)，将 LLM 推理建模为带类型节点和边的有向图（而非链/树），配合启发式控制器策略和自生成权重机制，在 HotpotQA 多跳推理上达 91.0%（Judge），超越 ToT 的 88.0%，同时揭示评估方法（string-match vs LLM-as-Judge）可导致最高 18 个百分点的排名偏差。

---

### [ROI-Driven Foveated Attention for Unified Egocentric Representations in Vision-Language-Action Systems](roi-foveated-attention.md)

🤖 机器人

提出基于 FK 投影的 ROI 驱动工程流水线，从单个外部相机生成末端执行器中心的高分辨率裁剪区域，替代腕部相机，为 VLA 系统提供统一的自我中心表征。

---

### [Mamba Learns in Context: Structure-Aware Domain Generalization for Multi-Task Point Cloud Understanding](sadg.md)

🧊 3D视觉

提出 SADG，首个基于 Mamba 的多任务点云域泛化框架，通过质心距离谱(CDS)和测地线曲率谱(GCS)实现变换不变的结构感知序列化，配合层级域感知建模和谱图对齐，在重建/去噪/配准三任务上全面超越 SOTA（含引入新数据集 MP3DObject）。

---

### [Satellite-to-Street: Synthesizing Post-Disaster Views from Satellite Imagery via Generative Vision Models](satellite-to-street.md)

🎨 3D视觉 / 图像生成

系统比较四种生成方法（Pix2Pix、ControlNet、VLM-guided、Disaster-MoE）从卫星图合成灾后街景，提出三层评估框架（像素级/语义一致性/VLM-as-Judge），揭示"真实感-保真度"权衡。

---

### [ScaleEdit-12M: Scaling Open-Source Image Editing Data Generation via Multi-Agent Framework](scaleedit-12m.md)

🎨 图像生成

提出 ScaleEditor，全开源多智能体层级框架，通过源图扩展+自适应编辑合成+任务感知质量验证三阶段构建了 ScaleEdit-12M（1200 万编辑对，23 类任务），微调 UniWorld-V1 后在 GEdit 上提升 35.1%、RISE 上提升 150.0%，证明开源 pipeline 可逼近商用 API 数据质量。

---

### [Seed1.8 Model Card: Towards Generalized Real-World Agency](seed1-8.md)

🧩 多模态/VLM / LLM Agent

字节跳动发布 Seed1.8 模型卡，一个面向通用真实世界代理的大模型，在保持 LLM/VLM 基础能力（推理、知识、指令遵循）的同时，统一支持搜索、代码执行和 GUI 交互的多步骤 Agent 工作流，提供四级思考模式平衡延迟与质量，在 AIME-25（94.3）、HMMT-25（89.7）等多个 benchmark 上达到或接近 GPT-5/Gemini-3-pro 水平。

---

### [Improving Diffusion Generalization with Weak-to-Strong Segmented Guidance](sgg.md)

🎨 图像生成 / 扩散模型

从 Weak-to-Strong 原则统一分析条件依赖引导(CFG)和条件无关引导(AG)的有效操作域——CFG 擅长高噪声时的类间分离，AG 擅长低噪声时的类内精化——提出 SGG 分段引导（先 CFG 后 AG）并将其迁移到训练目标中，在 SD3/SD3.5 推理和 SiT 训练上均超越所有现有引导变体。

---

### [StageCraft: Execution Aware Mitigation of Distractor and Obstruction Failures in VLA Models](stagecraft.md)

🤖 机器人

提出 StageCraft，免训练的 VLA 策略改进模块——通过分析少量策略 rollout 的成功/失败与初始场景中物体集合的关系，利用 VLM 推理识别导致策略失败的干扰物并在执行前最小化地移除它们，在三个真实任务中将 Pi0.5 和 SmolVLA 的成功率绝对提升 40%。

---
