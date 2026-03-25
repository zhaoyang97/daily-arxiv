# 📅 2026-03-13 精选笔记

> 共 **20** 篇

---

### [Cheers: Decoupling Patch Details from Semantic Representations Enables Unified Multimodal Comprehension and Generation](cheers.md)

📄 多模态VLM / 统一理解与生成

提出 Cheers，通过将 patch 级细节从语义表示中解耦，构建统一视觉 tokenizer + 级联 flow matching 头（先语义再注入高频细节），实现单模型同时做视觉理解和图像生成，性能匹敌专用模型，训练成本仅 Tar-1.5B 的 20%。

---

### [CMHANet: A Cross-Modal Hybrid Attention Network for Point Cloud Registration](cmhanet.md)

🧊 3D视觉 / 点云配准

提出 CMHANet，通过三种跨模态混合注意力机制（自注意力 + 聚合注意力 + 交叉注意力）融合 2D 图像纹理和 3D 点云几何特征，结合跨模态对比损失，在 3DMatch 上达到 92.4% Registration Recall，3DLoMatch 上达到 75.5% RR，均为 SOTA。

---

### [daVinci-Env: Open SWE Environment Synthesis at Scale](davinci-env.md)

🦾 LLM Agent / 软件工程

发布 OpenSWE——最大规模全透明 SWE Agent 训练框架，包含 45320 个可执行 Docker 环境（12.8K 仓库），通过多 Agent 合成管线 + 质量-难度感知过滤，用约 $1.47M 构建约 13000 条高质量轨迹，训练出的 32B/72B 模型在 SWE-bench Verified 上达 62.4%/66.0% SOTA。

---

### [DiveUp: Learning Feature Upsampling from Diverse Vision Foundation Models](diveup.md)

🔄 自监督学习 / 密集预测

提出 DiveUp，首次利用多种 VFM 的结构共识来指导特征上采样——通过通用的局部质心（COM）场表示消除不同 VFM 特征空间的不对齐，结合尖峰感知选择策略过滤高范数伪影，在语义分割和深度估计上达到 SOTA。

---

### [Thinking in Dynamics: How MLLMs Perceive, Track, and Reason Dynamics in Physical 4D World](dyn-bench.md)

🎬 多模态VLM / 视频理解

提出 Dyn-Bench，首个大规模物理 4D 动态理解 benchmark（1K 视频、7K VQA、3K 动态目标 grounding），系统评测发现现有 MLLM 无法同时维持时空推理和动态 grounding 的强表现，CoT 等传统 prompting 改善有限，而 Mask-Guided Fusion 和 ST-TCM 结构化方法显著提升动态感知能力。

---

### [Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering](egopoint-vqa.md)

🎬 视频理解 / 第一人称视觉

提出 EgoPointVQA 数据集（4000 合成+400 真实视频，18745 QA 对）和 HINT（Hand Intent Tokens）方法——将 3D 手部关键点编码为手势意图 token 并交织进 MLLM 输入，HINT-14B 在 6 类指示推理任务上以 68.1% 准确率超越 InternVL3-14B 5.4%（+6.6% vs InternVL3-14B 的 62.7%）。

---

### [Reinforcement Learning for Diffusion LLMs with Entropy-Guided Step Selection and Stepwise Advantages](egspo.md)

🎨 图像生成 / LLM推理

针对扩散语言模型（DLM）提出 EGSPO/EGSPO-SA——将去噪轨迹建模为有限时域 MDP 并推导精确逐步策略梯度，通过熵引导选择信息量最大的去噪步 + 单步去噪奖励估计逐步优势，EGSPO-SA 在 Sudoku 上达 94.3%、Countdown 78.5%、MBPP 51.1%、HumanEval 44.5%，均为 DLM RL SOTA。（ICML 2026）

---

### [ESG-Bench: Benchmarking Long-Context ESG Reports for Hallucination Mitigation](esg-bench.md)

🧠 LLM推理 / NLP

构建 ESG-Bench——首个面向长上下文 ESG 报告的幻觉检测与缓解 benchmark（94 份真实报告、270 QA 对、博士级人工标注），设计四步 CoT 微调策略将 LLaMA-3.2-3B 的幻觉缓解准确率从 76.0% 提升到 96.0%。

---

### [Expert Pyramid Tuning: Efficient Parameter Fine-Tuning for Expertise-Driven Task Allocation](expert-pyramid-tuning.md)

⚡ LLM效率 / 参数高效微调

提出 EPT（Expert Pyramid Tuning），将 CV 中多尺度特征金字塔的思想引入 LoRA-MoE，通过共享元知识子空间 + 反卷积金字塔投影 + 对比学习路由，在多任务 PEFT 上超越 SOTA MoE-LoRA 变体，同时减少训练参数。

---

### [Feynman: Knowledge-Infused Diagramming Agent for Scalable Visual Designs](feynman.md)

🦾 LLM Agent / 多模态

提出 Feynman，一个知识驱动的图表生成 Agent，将知识提取和视觉生成解耦——LLM 枚举领域知识并规划，再翻译为声明式 Penrose 程序并迭代视觉精修，用不到 $400 生成 106K 张对齐的图表-标题对，同时构建了 Diagramma 视觉推理 benchmark。

---

### [Geo-ADAPT: Locatability-Guided Adaptive Reasoning for Image Geo-Localization](geo-adapt.md)

📄 多模态VLM / 视觉推理

提出 Geo-ADAPT——可定位性引导的自适应推理框架，通过优化可定位性分数 $L_{opt}$ 量化深度推理适宜性，策划 Geo-ADAPT-51K 数据集 + 两阶段 GRPO 课程训练，Geo-ADAPT-8B 在 IM2GPS3K 上 Region-200km 达 62.6%（+3.6%）、Country-750km 达 77.9%（+1.7%），国家命名准确率 89.2% 超越 Gemini 2.5 Flash。

---

### [GeoChemAD: Benchmarking Unsupervised Geochemical Anomaly Detection for Mineral Exploration](geochemad.md)

📄 AI for Science / 异常检测

发布 GeoChemAD，首个开源多区域多元素地球化学异常检测 benchmark（8 个子集），并提出 GeoChemFormer——基于自监督预训练的 Transformer 框架，学习目标元素感知的地球化学表征，在所有子集上 consistently 优于现有无监督方法。

---

### [HiFICL: High-Fidelity In-Context Learning for Multimodal Tasks](hificl.md)

📄 多模态VLM / ICL

通过数学推导精确分解注意力公式：$\text{Attn}_{out} = \alpha \cdot \text{SA}(q,K,V) + \beta \cdot V_D$，揭示 ICL 效应的精确形式，据此提出 HiFICL 用低秩虚拟 key-value 对直接参数化 ICL 源头，在 Idefics2 上 VQAv2 达 72.08%（比 MimIC 高 2.79%），仅用 ~2.2M 参数。（CVPR 2026）

---

### [InterEdit: Navigating Text-Guided Multi-Human 3D Motion Editing](interedit.md)

🎨 图像生成 / 3D动作

提出多人 3D 动作编辑任务（TMME）、InterEdit3D 数据集（5161 个源-目标-指令三元组）和 InterEdit 模型——通过语义感知计划 token 对齐 + 交互感知频率 token 对齐（DCT 能量池化），在 g2t R@1 上达 30.82%（比 TIMotion 高 +5.85%），FID 0.37（低 17%）。

---

### [LibraGen: Playing a Balance Game in Subject-Driven Video Generation](libragen.md)

📄 视频生成 / 主体驱动

提出 LibraGen，将 S2V（主体驱动视频生成）建模为"平衡博弈"——用万级高质量数据 + in-pair/cross-pair LoRA 合并 + Consis-DPO/Real-Fake DPO 双管线合并 + 动态 CFG，在运动质量、视觉美学、文本对齐、主体一致性上全面超越开源和商业 S2V 模型。

---

### [Multimodal OCR: Parse Anything from Documents](multimodal-ocr.md)

📄 多模态VLM / 文档解析

提出 MOCR 文档解析范式和 dots.mocr 系统（3B 参数），把文档中的图表、图标、UI 等图形元素也当作一等解析目标转为 SVG 代码，在文档解析上仅次于 Gemini 3 Pro（olmOCR-Bench SOTA 83.9），在图形重建上多项指标超越 Gemini 3 Pro。

---

### [Beyond Binary Success: Sample-Efficient and Statistically Rigorous Robot Policy Comparison](n-score.md)

🤖 机器人 / 评估方法论

提出 N-SCORE，基于安全随时有效推断（SAVI）的机器人策略对比框架，支持从二值成功率到连续奖励的通用指标，通过序贯检验在统计严格性不降的前提下比批处理方法减少最多 70% 评估负担（仿真）和 50%（硬件），在 4500+ 硬件 rollout 上验证。

---

### [PISmith: Reinforcement Learning-based Red Teaming for Prompt Injection Defenses](pismith.md)

🛡️ AI安全 / LLM安全

提出 PISmith，一个基于 RL 的提示注入红队框架，通过自适应熵正则化和动态优势加权解决极端奖励稀疏问题，在黑盒设定下对 13 个 benchmark 上的 SOTA 防御（含 GPT-4o-mini/GPT-5-nano）实现高攻击成功率，揭示现有防御在自适应攻击下普遍脆弱。

---

### [Purify Once, Edit Freely: Breaking Image Protections under Model Mismatch](purify-once-edit-freely.md)

🛡️ AI安全 / 图像保护

揭示对抗性图像保护方法的严重缺陷——提出 VAE-Trans 和 EditorClean 两种净化器，利用模型架构不匹配（U-Net vs DiT）和 VAE 潜空间分布偏移，在 6 种保护方法 × 2100 个编辑任务上将 PSNR 提升 3-6 dB、FID 降低 50-70%，证明"净化一次，自由编辑"的攻击模式。

---

### [TacVLA: Contact-Aware Tactile Fusion for Robust Vision-Language-Action Manipulation](tacvla.md)

🤖 机器人 / 触觉感知

提出 TacVLA，将紧凑触觉阵列集成到 Transformer VLA 框架中，通过接触感知门控机制（仅在检测到物理接触时激活触觉 token），在约束锁扣拆卸和箱内抓取任务上平均提升 20-60% 成功率，遮挡场景下提升 2.1 倍。

---
