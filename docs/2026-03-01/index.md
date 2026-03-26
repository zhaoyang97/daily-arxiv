# 📅 2026-03-01 精选笔记

> 共 **20** 篇

---

### [AgilePruner: Adaptive Visual Token Pruning in Large Vision-Language Models](agilepruner.md)

📄 多模态VLM / 模型效率

AgilePruner 系统性地用 effective rank 和注意力熵分析了注意力 vs 多样性两类视觉 token 剪枝方法的优劣，发现多样性方法保留的多样性被高估且与幻觉相关，进而提出图像感知自适应剪枝机制——简单图像用注意力策略、复杂图像用多样性策略，在标准和幻觉 benchmark 上均取得可靠提升。

---

### [ArtLLM: Generating Articulated Assets via 3D LLM](artllm.md)

🧊 3D视觉 / 铰接体生成

提出 ArtLLM，将铰接物体的运动学结构（部件布局 + 关节参数）表示为离散 token 序列，用 3D 多模态大语言模型自回归预测，再配合部件感知几何生成和物理约束后处理，在 PartNet-Mobility 上大幅超越现有方法，并成功构建 real2sim 数字孪生。

---

### [DEP: A Decentralized Large Language Model Evaluation Protocol](dep.md)

🧠 LLM推理 / 评估框架

DEP 提出去中心化 LLM 评估协议：通过匹配服务器将用户、LLM 和 benchmark 解耦，实现模块化即插即用评估。benchmark 的数据和评估逻辑留在服务器端保证防泄漏，同时提供断点续传、并发请求等工程特性。截至 2026 年 2 月已适配 60+ 个 benchmark。

---

### [Can Thinking Models Think to Detect Hateful Memes?](hateful-memes-thinking.md)

🧩 多模态/VLM / AI安全

提出基于 GRPO 强化学习的后训练框架，通过 CoT 蒸馏 + 多奖励联合优化（格式/标签/长度/语义），将 thinking-based MLLM（Qwen3-VL-8B）用于仇恨 meme 检测，在 Hateful Memes 基准上达到 81.2% 准确率（SOTA），同时生成高质量解释。

---

### [HypeLoRA: Hyper-Network-Generated LoRA Adapters for Calibrated Fine-Tuning](hypelora.md)

⚡ LLM效率 / 参数高效微调

HypeLoRA 研究 LoRA 及超网络生成 LoRA 适配器在模型校准方面的动态：发现 LoRA 能达到全微调的校准水平甚至更优，超网络生成的跨层结构耦合 LoRA 能进一步改善特定任务的 MCC，而冻结 A 矩阵可作为增强校准的正则化手段（以准确率为代价）。

---

### [ICPRL: Acquiring Physical Intuition from Interactive Control](icprl.md)

📄 多模态VLM / 物理推理

ICPRL 提出让 VLM 通过交互式试错获取物理直觉的框架：用多轮 GRPO 训练视觉策略模型从像素级交互历史中 in-context 适应，搭配世界模型做动作结果预测，通过 PUCT 搜索选最佳动作，在 DeepPHY 物理谜题上显著超越基线且在未见环境中保持泛化。

---

### [JailNewsBench: Multi-Lingual and Regional Benchmark for Fake News Generation under Jailbreak Attacks](jailnewsbench.md)

⚖️ LLM对齐 / AI安全

构建首个面向越狱攻击诱导假新闻生成的多语言多区域基准 JailNewsBench，覆盖 34 个地区 22 种语言 5 种越狱方法 ~300k 实例，揭示英语/美国话题防御能力显著弱于其他区域的安全失衡现象。

---

### [MOSAIC: Modular Opinion Summarization using Aspect Identification and Clustering](mosaic.md)

✍️ NLP生成 / 意见摘要

提出 MOSAIC，一个面向工业部署的模块化评论摘要框架，将任务分解为主题发现→约束性意见抽取→意见聚类→层次摘要四步，在 PeerSum 和 SPACE 上超越 SOTA，通过在线 A/B 测试验证中间输出直接提升了旅游平台 1.5% 的 RPV（每访客收入）。

---

### [Multilingual Hate Speech Detection and Counterspeech Generation: A Survey](multilingual-hate-speech.md)

📖 NLP理解 / AI安全

一篇系统综述，覆盖多语言仇恨言论检测和反仇恨言论生成的全流程（任务设计→数据构建→评估），分析了单语模型在非英语和混合代码场景中失效的原因，提出三阶段框架并指出低资源语言数据稀缺、公平性偏差和多模态整合是三大待解决挑战。

---

### [PR-A²CL: Predictive Reasoning with Augmented Anomaly Contrastive Learning](pr-a2cl.md)

📄 多模态VLM / 视觉推理

PR-A²CL 针对组合视觉关系（CVR）推理任务——从四张图中找出不符合共同规则的"异常图"——提出增强异常对比学习（最大化正常实例相似度、最小化与异常的相似度）和预测-验证范式（用 3 张图预测第4张，通过差异定位规则违反），在 SVRT、CVR 和 MC²R 数据集上显著超越 SOTA。

---

### [Communication-Efficient Quantum Federated Learning over Large-Scale Wireless Networks](quantum-fl.md)

🛡️ AI安全 / 联邦学习

研究大规模无线网络中的量子联邦学习通信效率问题：提出基于 NOMA 的多信道 QFL 框架，联合优化信道选择和发射功率以最大化总速率，用量子近似优化算法（QAOA）求解 NP-hard 问题，并首次给出非凸损失、异构数据和量子噪声下的 QFL 收敛理论分析，实现总速率 100%+ 提升。

---

### [riMESA: Consensus ADMM for Real-World Collaborative SLAM](rimesa.md)

🤖 具身智能 / 多机器人SLAM

riMESA 提出基于 Consensus ADMM 的鲁棒增量分布式协作 SLAM 后端：对异常测量鲁棒、在有限通信下可靠、支持在线实时计算，在真实世界 C-SLAM 数据集上精度超越前方法 7 倍以上。

---

### [RMBench: Memory-Dependent Robotic Manipulation Benchmark](rmbench.md)

🤖 具身智能 / 机器人操作

RMBench 提出首个系统评估机器人操作策略记忆能力的仿真 benchmark（9 个任务、多级记忆复杂度），配套 Mem-0 模块化策略支持受控消融，实验揭示现有策略的记忆短板并给出架构设计的经验指导。

---

### [RnG: A Unified Transformer for Complete 3D Modeling from Partial Observations](rng.md)

🧊 3D视觉 / 3D重建

RnG 提出统一的前馈 Transformer，通过"重建引导的因果注意力"机制将 3D 重建和生成在注意力层面解耦，把 KV-cache 作为隐式 3D 表示，从稀疏图像同时恢复已见几何并生成合理的未见结构，在重建和生成两个任务上达到 SOTA 且支持实时交互。

---

### [SandboxEscapeBench: Quantifying LLM Capabilities for Container Sandbox Escape](sandbox-escape.md)

🛡️ AI安全 / LLM安全

SandboxEscapeBench 是首个安全量化 LLM 突破容器沙箱能力的 benchmark，采用嵌套沙箱架构（内层 LLM 容器 + 外层含 flag 无已知漏洞容器）实现 CTF 评估，覆盖配置错误、权限分配、内核缺陷和运行时弱点等逃逸路径，发现 LLM 在漏洞存在时确实能识别并利用它们。

---

### [TCD-Net: Teacher-Guided Causal Disentanglement for Image Denoising](tcd-denoising.md)

📄 CV / 图像去噪

TCD-Net 从因果推断视角重新审视图像去噪：通过环境偏置消除（去混杂）、正交双分支内容-噪声解耦、以及 AI 生成图引导的因果先验，打破传统去噪中内容与噪声的虚假相关，在多个 benchmark 上以 104.2 FPS 速度超越主流方法。

---

### [Token-level Data Selection for Safe LLM Fine-tuning](toss-safe-finetuning.md)

⚡ LLM效率 / AI安全

提出 TOSS/TOSS-Pro，将 LLM 微调中的安全退化问题从"样本级"细化到"token 级"，通过训练安全退化/效用两个参考模型对每个 token 打分并遮蔽高风险 token，在 Llama-3-8B 上平均安全 win rate 比标准 SFT 高 33%，比最强 baseline SEAL 高 22%，同时保持效用不降。

---

### [Agent-Based Simulation of Trust Development in Human-Robot Teams](trust-hri.md)

📄 具身智能 / 人机协作

提出一个基于 NetLogo 的 agent-based model 模拟人机团队中的信任动态，经 Hancock 元分析验证（Spearman ρ=0.833），发现机器人可靠性主导任务成功率（η²=0.93），并揭示了"信任-性能脱耦"现象——高信任不等于高性能，校准误差才是关键诊断指标。

---

### [Truth as a Trajectory (TaT): What Internal Representations Reveal About LLM Reasoning](truth-trajectory.md)

🧠 LLM推理 / 可解释性

TaT 提出将 transformer 推理建模为隐状态的"轨迹"（层间位移分析），而非静态激活值的探测，发现层间几何位移中存在区分正确/错误推理的不变量，在常识推理、QA、毒性检测上优于传统 probing 方法。

---

### [VisNec: Measuring and Leveraging Visual Necessity for Multimodal Instruction Tuning](visnec.md)

📄 多模态VLM / 数据选择

VisNec 提出"视觉必要性分数"——通过比较有/无视觉输入时的预测损失差异来量化每个训练样本是否真正需要视觉推理，配合语义聚类保持任务多样性。仅用 LLaVA-665K 的 15% 数据达到 100.2% 的全量性能，在 Vision-Flan-186K 上甚至超过全量训练 15.8%。

---
