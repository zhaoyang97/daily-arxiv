# DualTSR: Unified Dual-Diffusion Transformer for Scene Text Image Super-Resolution

**日期**: 2026-03-15  
**arXiv**: [2603.14207](https://arxiv.org/abs/2603.14207)  
**代码**: 即将发布  
**领域**: 图像生成 / NLP生成  
**关键词**: scene text super-resolution, dual diffusion, flow matching, discrete diffusion, Chinese OCR

## 一句话总结
提出 DualTSR，用单一多模态 Transformer 同时建模图像超分（Conditional Flow Matching）和文字识别（Discrete Diffusion），去除对外部 OCR 的依赖，在中文场景文字超分上取得最优感知质量和文字保真度。

## 研究背景与动机

1. **领域现状**: 场景文字图像超分（STISR）要同时保证视觉质量和文字可读性。当前主流范式是 OCR-guided：用预训练 OCR 提取文字 prior 引导超分网络，DiffTSR 更进一步用双分支扩散分别建模图文。

2. **现有痛点**: (a) OCR-guided 方法的可靠性受限于外部 OCR 精度——错误预测传播到 SR 网络导致错误笔画/字形；(b) DiffTSR 等多模块架构将文字和图像分支独立建模，用 fusion module 连接，交互深度受限且系统复杂。

3. **核心矛盾**: 需要文字语义信息引导超分，但外部 OCR 不可靠；分支架构能力强但交互不够深。能否让模型自己学会文字理解？

4. **切入角度**: 如果把图像生成和文字识别放在同一个 Transformer 里联合训练，文字和图像 token 可以在每一层深度交互——模型不再需要外部 OCR，而是自己学会从低分辨率图像推断文字。

5. **核心 idea**: Dual diffusion = Flow Matching（连续，图像）+ Discrete Diffusion（离散，文字），共享一个多模态 Transformer backbone，实现端到端联合建模。

## 方法详解

### 整体框架

LR 图像 → VAE 编码到 latent → 同时初始化图像分支（高斯噪声）和文字分支（全 mask 序列）→ 共享 Transformer 迭代去噪（图像用 flow matching 更新，文字用 absorbing-state diffusion 更新）→ 图像 latent 解码为 HR 图像 + 文字序列输出。

### 关键设计

1. **Conditional Flow Matching（图像分支）**:
    - 做什么：从噪声 latent 生成高分辨率图像 latent
    - 核心思路：定义线性路径 $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$，学习速度场 $\mathbf{v}_\theta(\mathbf{x}_t, t, \mathbf{c})$，推理时用 Euler 步积分
    - 设计动机：Flow Matching 比标准 DDPM 更高效，path 更直，采样步数更少

2. **Discrete Diffusion（文字分支）**:
    - 做什么：从全 mask 序列恢复出原始文字
    - 核心思路：采用 absorbing-state CTMC——forward 过程将 token 替换为 mask token，reverse 过程预测 clean text。用 NELBO + log-linear schedule $\alpha_t = 1-t$
    - 设计动机：文字是离散数据，避免 continuous embedding 引入的映射误差

3. **Joint Attention (MM-DiT)**:
    - 做什么：图像和文字 token 深度融合
    - 核心思路：借鉴 SD3 的 MM-DiT 设计——图像和文字 token 各自独立做 projection，然后拼接进同一个 self-attention 层，attention 后再 split 回各自分支
    - 设计动机：比 DiffTSR 的外部 fusion module 深得多——每一层都做交叉注意力，文字信息可以即时反馈到图像生成（反之亦然）

4. **Model-Guided Training (MG-CFG)**:
    - 做什么：训练时引入 classifier-free guidance 风格的目标修正
    - 核心思路：用 EMA teacher 的条件/无条件预测差来修正 flow matching target: $\mathbf{u}'_t = \mathbf{u}_t + w \cdot (\text{sg}(\mathbf{v}^\text{ema}(\mathbf{x}_t,t,\mathbf{c})) - \mathbf{v}^\text{ema}(\mathbf{x}_t,t,\varnothing))$
    - 设计动机：直接在训练阶段就让模型学会 guidance 效果，推理时不需要额外的 CFG 开销

### 训练策略
- 三个 loss 联合优化：$\mathcal{L}_\text{IMG-MG} + \mathcal{L}_\text{TXT} + \mathcal{L}_\text{Joint-MG}$
- Joint loss 用相同时间步同时 corrupt 图文，训练模型同时去噪两个模态
- Text 分支用 K=8 antithetic sampling 近似连续时间目标
- 4×A100, 700k iterations, AdamW lr=1e-4 with cosine decay

## 实验关键数据

### 主实验（CTR-TSR ×4 超分）

| 方法 | PSNR↑ | LPIPS↓ | FID↓ | ACC↑ | NED↑ |
|------|-------|--------|------|------|------|
| ESRGAN | 22.18 | 0.3986 | 18.25 | 43.69% | 62.15% |
| SwinIR | 24.73 | 0.3957 | 50.89 | 50.09% | 68.93% |
| SRFormer | 25.05 | 0.3801 | 46.23 | 51.83% | 70.70% |
| DiffTSR | 20.62 | 0.3952 | 22.24 | 44.87% | 63.20% |
| **DualTSR** | 20.54 | **0.3292** | **16.42** | **57.65%** | **76.64%** |

### RealCE（真实场景 ×4）

| 方法 | LPIPS↓ | FID↓ | ACC↑ | NED↑ |
|------|--------|------|------|------|
| SwinIR | 0.3271 | 56.77 | 62.10% | 87.55% |
| DiffTSR | 0.3382 | 41.13 | 58.00% | 84.44% |
| **DualTSR** | **0.3277** | **40.78** | **62.20%** | **88.49%** |

### 关键发现
- DualTSR 的 PSNR 低于传统 SR 方法，但 FID/LPIPS/ACC/NED 全面领先——说明 pixel-wise 精度和感知质量/文字保真度存在 trade-off，DualTSR 优化的是后者
- 相比 DiffTSR（双分支 + fusion），DualTSR 的统一架构在 ACC 上高出 12.78%（CTR-TSR ×4），说明深度融合远好于浅层 fusion
- Joint loss 的贡献：联合 corrupt + 联合恢复迫使模型真正学会图文协同，而非各做各的
- MG-CFG 在 guidance scale w=1.0 时效果最好

## 亮点与洞察
- **统一双扩散**: 在同一个 Transformer 中同时做 flow matching（连续）和 discrete diffusion（离散），简洁优雅。可推广到任何需要同时生成连续和离散输出的场景
- **去除外部 OCR 依赖**: 让模型通过 joint training 自行学会 text prior，从根源解决 error propagation
- **Joint attention 的威力**: 每层都做图文交互 vs DiffTSR 的偶尔 fusion → ACC 提升 12.78%

## 局限性 / 可改进方向
- PSNR 偏低——扩散模型天然倾向生成多样性而非 pixel-exact，如果下游需要精确像素对齐可能是问题
- 只在中文文字 SR 上评估，英文/多语言泛化性未验证
- RealCE 只评估了 300 个 curated 样本子集，不是完整 benchmark
- 4-step ODE sampler 的推理效率 vs DiffTSR 的比较未详细报告

## 相关工作与启发
- **vs DiffTSR**: 同样用双扩散，但 DiffTSR 分离建模+fusion module → DualTSR 统一 backbone+joint attention，更深融合
- **vs MARCONet/MARCONet++**: 用 codebook/glyph mask 等结构 prior → DualTSR 不需要额外 prior，端到端更简洁
- **SD3 MM-DiT 的启发**: joint attention 设计直接来自 SD3，证明这种多模态融合方式在 SR 场景同样有效

## 评分
- 新颖性: ⭐⭐⭐⭐ 统一 flow matching + discrete diffusion 的思路有新意，但 MM-DiT 结构来自 SD3
- 实验充分度: ⭐⭐⭐ 只有中文 SR 评估，RealCE 是子集，缺少推理速度比较
- 写作质量: ⭐⭐⭐⭐ 结构清晰，公式自洽
- 价值: ⭐⭐⭐⭐ 端到端文字 SR 框架，去除 OCR 依赖有实际价值
