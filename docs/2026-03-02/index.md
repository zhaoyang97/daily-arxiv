# 📅 2026-03-02 精选笔记

> 共 **20** 篇

---

### [According to Me: Long-Term Personalized Referential Memory QA](according-to-me.md)

📄 ai_safety

本文提出了 ATM-Bench，首个面向多模态、多来源个性化记忆问答的基准，包含约四年的真实隐私保护个人记忆数据和人工标注的 QA 对，并提出 Schema-Guided Memory (SGM) 结构化记忆表示方法，实验表明当前最先进的记忆系统在困难集上准确率不足 20%。

---

### [AgenticGEO: A Self-Evolving Agentic System for Generative Engine Optimization](agenticgeo.md)

📄 llm_agent

AgenticGEO 将生成式搜索引擎优化（GEO）形式化为内容条件化控制问题，通过 MAP-Elites 策略档案和协同进化的 Critic 代理实现自适应的多轮内容重写，在 3 个数据集上以平均 46.4% 的增益超越 14 个基线方法。

---

### [CRoCoDiL: Continuous and Robust Conditioned Diffusion for Language](crocodil.md)

⚡ LLM效率 / 扩散语言模型

CRoCoDiL 将 Masked Diffusion Model（MDM）的扩散过程从离散 token 空间迁移到连续句子级语义空间，通过联合训练 encoder-demasker 架构形成新型自编码器，并提出两种无条件文本生成算法（ConThenDisc 和 ConWithinDisc），在保持生成质量的同时实现超过 10× 的采样加速。

---

### [Deepfake Forensics Adapter: A Dual-Stream Network for Generalizable Deepfake Detection](deepfake-forensics-adapter.md)

🛡️ AI安全 / 深伪检测

DFA 提出双流框架将冻结的 CLIP 模型与专门的深伪取证分析融合：全局特征适配器识别图像整体伪造线索，局部异常流利用面部结构先验捕捉局部伪造痕迹，交互融合分类器深度融合两路特征。在 DFDC 挑战性 benchmark 上 video-level AUC 达到 0.836，较前方法提升 4.8%。

---

### [DUEL: Exact Likelihood for Masked Diffusion via Deterministic Unmasking](duel.md)

📄 image_generation (discrete diffusion / language modeling)

DUEL 框架证明了使用确定性解码策略的掩码扩散模型（MDM）可以精确计算似然，首次为 MDM 提供了"真正的困惑度"指标，将 MDM 与自回归模型的困惑度差距缩小了最高 82%（零样本），并发现 Oracle 搜索下 MDM 可远超自回归基线（AG News 上 36.47 vs 52.11）。

---

### [FACE: A Face-based Autoregressive Representation for High-Fidelity and Efficient Mesh Generation](face.md)

🧊 3D视觉 / 网格生成

FACE 提出"一面一token"的自回归网格生成范式，将三角面片（而非顶点坐标）作为基本生成单元，序列长度缩短 9 倍、压缩比达到 0.11（较 SOTA 减半），同时在重建质量和单图生成mesh上达到最优。

---

### [FireRed-OCR Technical Report](firered-ocr.md)

🧩 多模态/VLM / 文档解析

FireRed-OCR 提出三阶段渐进训练框架（多任务预对齐 → SFT → 格式约束 GRPO），将通用 VLM (Qwen3-VL-2B) 特化为像素级精确的结构化文档解析专家，在 OmniDocBench v1.5 上以 92.94% 总分大幅超越 DeepSeek-OCR 2 和 OCRVerse，仅 2B 参数即超越 235B 级别的通用 VLM。

---

### [FreeAct: Freeing Activations for LLM Quantization](freeact.md)

⚡ LLM效率 / 模型量化

FreeAct 打破现有量化方法中变换矩阵的"一对一"刚性约束，利用激活值的秩亏缺性质为不同 token 类型（masked/unmasked、vision/text）分配不同的变换矩阵，同时保持权重端统一静态变换，在 dLLM 和 MLLM 的 W4A4 量化上最高提升 5.3%。

---

### [GVCoT: Generative Visual Chain-of-Thought for Image Editing](gvcot.md)

🎨 图像生成 / 图像编辑

GVCoT 提出生成式视觉推理链框架：先生成空间定位线索（视觉 token）定位编辑区域，再执行编辑操作，两个阶段端到端联合优化。构建 1.8M 样本的 GVCoT-Edit-Instruct 数据集 + SREdit-Bench 挑战性 benchmark，在复杂场景细粒度编辑上持续超越 SOTA。

---

### [ICPO: Provable and Practical In-Context Policy Optimization for Self-Improvement](icpo.md)

🧠 LLM推理 / Test-time Scaling

ICPO 提出一套理论+实践框架：理论上证明经过 Fisher-weighted logit-matching 预训练的自注意力模型能在上下文中隐式执行策略优化；实践上提出 ME-ICPO（最小熵准则筛选自评估奖励），在数学推理任务上以低推理成本达到 top-tier 的 test-time scaling 效果。

---

### [KidGym: 2D Grid-Based Reasoning Benchmark for MLLMs](kidgym.md)

📄 多模态VLM / Benchmark

KidGym 受韦氏儿童智力量表启发，设计了 12 个 2D 网格交互任务（涵盖执行、感知推理、学习、记忆、规划五大能力），首次系统评估 MLLM 在动态交互场景中的认知能力。实验揭示：即使 o3/GPT-5 在简单任务接近满分，但在抽象推理、数量感知和复合能力任务上仍远落后于人类。

---

### [Kiwi-Edit: Versatile Video Editing via Instruction and Reference Guidance](kiwi-edit.md)

📄 image_generation

Kiwi-Edit 提出了一个可扩展的数据生成流水线来构建 477K 高质量的指令-参考图像-视频编辑四元组数据集 RefVIE，并设计了统一的 MLLM-DiT 架构通过 Query Connector 和 Latent Connector 双路径机制实现指令+参考图像引导的视频编辑，在 OpenVE-Bench 上以 3.02 的 Overall 分数超越所有开源基线。

---

### [Legal RAG Bench: An End-to-End Benchmark for Legal RAG](legal-rag-bench.md)

🧠 LLM推理 / 信息检索

提出 Legal RAG Bench——首个端到端法律 RAG 基准，包含 4,876 段落 + 100 个专家手工问题，通过全因子实验设计和层级错误分解框架，定量证明**检索质量（而非 LLM 能力）是法律 RAG 系统性能的天花板**，许多被归因于"幻觉"的错误实际上是检索失败所致。

---

### [LFPO: Likelihood-Free Policy Optimization for Masked Diffusion Models](lfpo.md)

🧠 LLM推理 / 扩散语言模型

LFPO 提出面向 Masked Diffusion 语言模型（dLLM）的原生对齐框架：将 flow matching 的向量场概念映射到离散 token 空间，绕过不可解的似然计算，通过对比更新直接优化去噪 logits，在代码和推理任务上超越 SOTA，同时通过中间步一致性约束将推理加速约 20%。

---

### [MIST-RL: Mutation-based Incremental Suite Testing via Reinforcement Learning](mist-rl.md)

🧠 LLM推理 / 代码生成

MIST-RL 将 LLM 测试用例生成从"堆数量"转变为"提质量"，通过 GRPO 强化学习+增量变异奖励+动态惩罚，在 mutation score 提升 28.5% 的同时减少 19.3% 的测试用例数量，并显著提升下游代码重排序准确率。

---

### [Nano-EmoX: Unifying Multimodal Emotional Intelligence from Perception to Empathy](nano-emox.md)

🧩 多模态/VLM / 情感计算

提出 Nano-EmoX（2.2B），一个紧凑型多任务多模态情感语言模型，通过三层认知层级框架（感知→理解→交互）和 P2E 课程训练策略，首次在单模型中统一六项核心情感任务（MSA/MER/OV-MER/ERI/MIR/ERG），以 73% 参数缩减达到或超越 7-9B 级别的 SOTA。

---

### [PhotoBench: Beyond Visual Matching Towards Personalized Intent-Driven Photo Retrieval](photobench.md)

🧩 多模态/VLM / 信息检索

提出 PhotoBench——首个基于真实个人相册构建的个性化照片检索基准，通过"多源画像框架"（视觉语义 + 时空元数据 + 社交身份 + 时间事件）合成复杂意图驱动查询，揭示统一嵌入模型在非视觉约束上的"模态鸿沟"和 Agent 系统的"源融合悖论"两大关键缺陷。

---

### [StepVAR: Structure-Texture Guided Pruning for Visual Autoregressive Models](stepvar.md)

🎨 图像生成 / 模型效率

StepVAR 提出一种无训练的 token 剪枝框架，通过高通滤波器（捕捉纹理细节）和 PCA（保留全局结构信息）双重准则联合决定保留哪些 token，配合最近邻特征传播重建完整特征图，在 text-to-image 和 text-to-video VAR 模型上实现显著加速且保持生成质量。

---

### [Video TokenCom: Textual Intent-guided Multi-Rate Video Token Communications with UEP-based Adaptive Source–Channel Coding](video-tokencom.md)

📄 multimodal_vlm

Video TokenCom 提出了文本意图引导的多速率视频 Token 通信框架，通过 CLIP 热力图+光流传播识别用户意图区域、为意图/非意图 token 分配不同比特精度的多速率编码、以及 UEP 自适应信源-信道联合编码，在超低 BPP 下以 0.013 BPP 在 PSNR（26.36 vs 23.28）和 FVD（1289 vs 4010）上全面超越 H.265。

---

### [WorldStereo: Bridging Camera-Guided Video Generation and Scene Reconstruction via 3D Geometric Memories](worldstereo.md)

📄 3d_vision

WorldStereo 提出了一个基于几何记忆的多轨迹视频生成框架，通过全局几何记忆（GGM）和空间立体记忆（SSM）两个模块，实现了精确相机控制下的多视角一致视频生成，并可用于高质量 3D 场景重建，同时通过 DMD 蒸馏实现 20× 加速。

---
