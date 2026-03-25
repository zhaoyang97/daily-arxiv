# 📅 2026-03-14 精选笔记

> 共 **20** 篇

---

### [AD-Copilot: A Vision-Language Assistant for Industrial Anomaly Detection via Visual In-context Comparison](ad-copilot.md)

📄 多模态VLM / 工业异常检测

提出 AD-Copilot，通过 Comparison Encoder（跨注意力提取图像对差异tokens）+ Chat-AD 大规模工业多模态数据集（62万样本）+ 四阶段渐进训练策略，使 7B MLLM 在工业异常检测 benchmark MMAD 上达到 82.3% 准确率，超越所有现有模型（含 GPT-4o）并接近人类专家水平。

---

### [Computation and Communication Efficient Federated Unlearning via On-server Gradient Conflict](fed-unlearning.md)

🛡️ AI安全 / 联邦遗忘

提出 FOUL（Federated On-server UnLearning），训练时用因果解纠缠将模型分为域不变/域特异子网络（L2U），遗忘时仅在服务器端对域特异子网络做梯度冲突匹配，实现高效无需客户端数据的联邦客户级遗忘。

---

### [Garments2Look: 首个大规模 Outfit 级虚拟试穿数据集](garments2look.md)

🎨 图像生成 / 虚拟试穿

构建首个 outfit 级虚拟试穿数据集 Garments2Look（80K 穿搭对、40+ 大类 300+ 子类、平均 4.48 参考图），benchmark 揭示 VTON 专用方法在 outfit 级表现极差（FastFit Layering 仅 0.131），通用编辑模型 Nano Banana 全面更优（Garment 0.925、Layering 0.885），结构化文本标注使 FID 降低 7.4%。

---

### [Geo-ID: Test-Time Geometric Consensus for Cross-View Consistent Intrinsics](geo-id.md)

🧊 3D视觉 / 内在分解

提出 Geo-ID，一种推理时框架，通过几何引导的稀疏对应关系耦合多视角内在分解预测，用体素化共识初始化 + 共识引导扩散注入跨视角约束，无需修改模型参数即可将 Marigold Appearance 的 Metallicity MAD 从 0.070 降至 0.044（32 视角），同时保持单视角分解质量不下降。

---

### [IGU-LoRA: Adaptive Rank Allocation via Integrated Gradients and Uncertainty-Aware Scoring](igu-lora.md)

📄 参数高效微调 / 自适应 LoRA

提出 IGU-LoRA，将 Integrated Gradients 从输入归因扩展到参数空间计算层级重要性得分，结合 EMA+偏差追踪的 SNR 不确定性感知评分实现自适应 rank 分配。RoBERTa-large 上 GLUE 平均 89.42%（0.33M 参数），Qwen-2.5-0.5B 上以 8.8M 参数达 59.17% 超越 Full FT（494M 参数 58.98%）。

---

### [Learning through Creation: A Hash-Free Framework for On-the-Fly Category Discovery](ltc-category-discovery.md)

📦 模型压缩 / 开放世界识别

提出 LTC（Learning through Creation）框架，通过在训练时用 MKEE（核能量最小化+熵最大化）单步扰动生成伪未知类样本，配合双 max-margin 损失和自适应阈值在连续特征空间（无 hash）中实现类别发现-识别对齐，在 7 个 OCD benchmark 上提升 1.5%-13.1%。

---

### [MHPO: Modulated Hazard-aware Policy Optimization for Stable Reinforcement Learning](mhpo.md)

🧠 LLM推理 / 强化学习优化

提出 MHPO 框架，通过 Log-Fidelity Modulator（log 空间 tanh 映射保证梯度可微且有界）+ Decoupled Hazard Penalty（Weibull 累积危险函数对正/负策略偏移施加非对称惩罚），解决 GRPO 训练中 importance ratio 导致的梯度不稳定问题，在数学推理和 VLM 任务上一致超越 GRPO/DAPO/SAPO。

---

### [Multi-Modal Character Localization and Extraction for Chinese Text Recognition](multi-modal-character.md)

📄 多模态VLM / 文字识别

提出 LER（Localization-Extraction-Recognition）框架，通过 CLIP 多模态信息辅助字符定位 + 显式字符特征解耦 + 部首感知 IDS 解码器，解决中文场景文字识别中的误差累积和注意力漂移问题，在 CTR benchmark 上以 81.47% 平均 LACC 达到 SOTA。

---

### [OasisSimp: An Open-source Asian-English Sentence Simplification Dataset](oasisssimp.md)

⚡ LLM效率 / 文本简化

构建 OasisSimp 多语言句子简化数据集（英语/僧伽罗语/泰语/泰米尔语/普什图语），由母语标注者经 3 轮训练后人工简化；评估 8 个开源 LLM 发现英语 SARI 可达 44.99 而低资源语言最低仅 24.07，揭示巨大的多语言性能鸿沟。

---

### [Revisiting the Perception-Distortion Trade-off with Spatial-Semantic Guided Super-Resolution](perception-distortion.md)

🎨 图像生成 / 超分辨率

提出 SpaSemSR 空间-语义引导扩散超分框架，通过空间锚定文本引导和语义增强视觉引导双路互补，在 DIV2K-Val 上 PSNR 21.31 超越全部扩散方法（StableSR 20.74），CLIP-IQA 0.693 大幅超越 GAN 方法（Real-ESRGAN 0.549），并在真实数据 RealSR/DRealSR 上全面领先，消融证实空间引导提升 PSNR +1.84，语义引导提升 CLIP-IQA +4.09%。

---

### [PhysAlign: Physics-Coherent Image-to-Video Generation through Feature and 3D Representation Alignment](physalign.md)

🎨 图像生成 / 视频生成

提出 PhysAlign，通过 Gram 矩阵时空关系对齐（从 V-JEPA2 提取运动学先验）+ 多层深度几何监督，仅用 3K 合成物理视频微调 Wan2.2-14B 的 LoRA adapter，即可显著提升生成视频的物理一致性（PIS 加速度指标从 0.52→0.63）而不损失视觉质量。

---

### [QTrack: Query-Driven Reasoning for Multi-modal MOT](qtrack.md)

🎬 视频理解 / 多目标跟踪

提出 QTrack，将多目标跟踪从"跟踪所有物体"扩展为"根据自然语言查询推理并跟踪指定目标"，通过端到端 VLM + TAPO（时序感知策略优化）+ 结构化奖励实现语言条件化的时空推理跟踪，3B 模型即超越 GPT-5.2 等 10+ baseline，并构建 RMOT26 大规模 benchmark。

---

### [RSEdit: Text-Guided Image Editing for Remote Sensing](rsedit.md)

🎨 图像生成 / 遥感编辑

提出 RSEdit，通过架构感知的适配策略（U-Net 用 channel concatenation，DiT 用 token concatenation）将预训练 T2I 扩散模型转化为遥感图像编辑器，在 6 万双时相卫星图像对上训练，在灾害模拟、城市变化等任务上大幅超越通用编辑器（F1dam 从 8.37 提升到 34.11）。

---

### [Sat-JEPA-Diff: Bridging Self-Supervised Learning and Generative Diffusion for Remote Sensing](sat-jepa-diff.md)

🎨 图像生成 / 遥感时序预测

提出 Sat-JEPA-Diff，用 IJEPA 在 latent 空间预测未来帧的语义表示，再通过 ~25M 参数的 cross-attention adapter 引导冻结的 SD 3.5 生成高保真卫星图像，在全球 100 个 ROI 的 Sentinel-2 数据集上 GSSIM 达 0.8984（比确定性方法高 11%+），FID 0.1475。

---

### [Sparse-Dense Mixture of Experts Adapter for Multi-Modal Tracking](sdmoea-tracking.md)

🎬 视频理解 / 多模态跟踪

提出 SDMoEA 参数高效微调框架，通过 Sparse MoE（建模模态特异信息）+ Dense-Shared MoE（串并混合结构建模模态共享信息）作为多模态 adapter，配合超图融合模块建模高阶跨模态关系，在 7 个多模态跟踪数据集上超越现有 PEFT 方法。

---

### [Sky2Ground: A Benchmark for Site Modeling under Varying Altitude](sky2ground.md)

🧊 3D视觉 / 跨视角定位

构建 Sky2Ground 跨高度场景建模 benchmark（51 个地理站点、80k 张图像，覆盖卫星/航拍/地面三种视角），提出 SkyNet 双流架构在 GAS 设置下 RRA@5 达 83.2%（+9.6%），平均指标 65.1（VGGT 零样本 52.9），消融显示 MSA 贡献 +8.2%、P-VS 贡献 +7.3%。

---

### [ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation](st-vla.md)

🧊 3D视觉 / 机器人操作

提出 ST-VLA 层级式 VLA 框架，通过统一的 3D-4D 中间表示（显式 3D 轨迹 + 平滑空间掩码）桥接高层 VLM 语义推理与低层 3D 策略执行，配合 ST-Human 大规模人操作数据集（30万 episodes、14 类任务）训练的 ST-VLM，在 RLBench 和真实场景上零样本成功率提升 44.6%。

---

### [Steering Generative Models for Accessibility: EasyRead Image Generation](steering-accessibility.md)

🎨 图像生成 / 可访问性, **关键词**: EasyRead, pictogram, LoRA fine-tuning, cognitive accessibility, diffusion model

在 OpenMoji/ARASAAC/LDS 三源混合数据集（共 ~17k 图）上用 LoRA rank-16 微调 SD v1.5，提出首个定量 EasyRead Score (ERS) 评估框架，生成面向智力障碍与低识字人群的简洁象形图（ERS 0.40→0.47，CLIP 相似度 24.33→31.15）。发表于 CHI EA 2026。

---

### [ToolFlood: Beyond Selection — Hiding Valid Tools from LLM Agents via Semantic Covering](toolflood.md)

🦾 LLM Agent / 安全攻击

揭露 tool-augmented LLM agent 检索阶段的新漏洞——ToolFlood 通过 Monte Carlo 候选生成 + 贪心语义覆盖，在 ToolBench（11,760 工具）上仅注入 1.2% 的对抗工具即实现 91% TDR 和 ~95% ASR，使合法工具被完全隐藏在 top-k 检索结果之外。

---

### [vla-eval: VLA 模型统一评估框架](vla-eval.md)

📄 多模态VLM / 评估框架

统一评估框架 vla-eval，WebSocket+msgpack 协议解耦模型与 benchmark，Docker 隔离环境冲突，支持 13 个仿真 benchmark + 6 个模型。并行评估（N=50 shards + B=16 batch）实现 **47× 加速**，2000 LIBERO episodes 仅需 ~18 min。可复现性审计发现 SimplerEnv 终止语义歧义、CALVIN 隐藏归一化统计等未文档化问题。

---
