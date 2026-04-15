# ACD-U: Asymmetric Co-teaching with Machine Unlearning for Robust Learning with Noisy Labels

**日期**: 2026-03-07  
**arXiv**: [2603.07166](https://arxiv.org/abs/2603.07166)  
**代码**: [GitHub](https://github.com/meruemon/ACD-U)  
**领域**: LLM/NLP  
**关键词**: noisy label learning, machine unlearning, co-teaching, vision Transformer, semi-supervised learning

## 一句话总结

提出 ACD-U 框架，将**机器遗忘（machine unlearning）**引入噪声标签学习领域，结合 CLIP 预训练 ViT 与 CNN 的**非对称协同教学**，实现对错误记忆样本的事后纠正，在多个合成与真实噪声基准上取得 SOTA。

## 研究背景与动机

1. **领域现状**: 噪声标签学习（Learning with Noisy Labels, LNL）是深度学习中的核心挑战。主流方法以 DivideMix 为代表，采用"样本选择 + 半监督学习"范式：通过 GMM 将训练样本分为干净/噪声集，再用 SSL 方法利用两类数据。
2. **现有痛点**: 一旦噪声样本在早期被错误判定为"干净"，后续训练中几乎无法纠正——错误标签被作为有监督信号持续使用，导致**确认偏差（confirmation bias）**不断累积。ProMix、RankMatch 等方法试图提升初始选择精度，但仍缺乏事后纠错机制。
3. **核心矛盾**: 现有方法只能**被动避免错误**（提高选择准确率），无法**主动纠正错误**（移除已记忆的噪声影响）。当两个网络同时将噪声样本错判为干净时，该错误会永久嵌入模型。
4. **切入角度**: (1) 从 machine unlearning 领域借鉴选择性遗忘技术，解决"已记忆错误不可逆"问题；(2) 利用预训练 ViT 与随机初始化 CNN 之间**异质的学习动态**（pretrained 模型早期精度高但可能过拟合，CNN 逐步提升但累积误差），设计非对称训练策略。
5. **核心 idea**: 构建一个"主动错误检测-遗忘-纠正"的反馈闭环——通过损失轨迹分析 + CLIP 一致性检查动态识别被错误记忆的样本，再用 KL 散度驱动的遗忘损失移除其影响，同时用非对称协同教学抑制噪声记忆。

## 方法详解

### 整体框架

ACD-U 由三个核心组件组成，按训练阶段逐步激活：

- **Warmup 阶段**（前 $E_{warmup}$ 个 epoch）：CNN（net A）做标准有监督训练，ViT（net V）做自监督学习（不使用标签，避免过早拟合噪声）
- **Preparation 阶段**（$E_{warmup}+1$ 到 $E_{start}$）：启动非对称协同教学（ACD），使用全部数据 $D$，ViT 编码器冻结至 $E_{encoder}$
- **Unlearning 阶段**（$E_{start}$ 之后）：完整 ACD-U 启动，每 $E_{UP}$ 个 epoch 周期性执行遗忘目标选择 + 遗忘操作

### 关键设计

1. **Unlearning Target Selection（遗忘目标选择）**: 通过三个条件的集成识别应被遗忘的样本：
    - **Condition 1 (Low-loss)**: 基于记忆效应，低损失样本更可能是已被记忆的噪声样本，用分位数阈值 $p_{low}$ 筛选
    - **Condition 2 (Loss-drop)**: 损失值在最近 $E_{UP}$ 个 epoch 内下降的样本，说明模型正在记忆它们，用分位数阈值 $p_{drop}$ 筛选
    - **Condition 3 (CLIP-consistent)**: 使用独立的 CLIP 模型做 zero-shot 预测——若 CLIP 预测与给定标签一致，则该样本很可能是干净的，从遗忘候选中排除
    - 最终遗忘集：$D_u^{(l)} = (D_{pl}^{(l)} \cup D_{\Delta l}^{(l)}) \setminus D_{CS}$

2. **Selective Forgetting（选择性遗忘）**: 采用基于 KL 散度的遗忘损失（受 SCRUB 启发）：$\mathcal{L}_{unl} = -T_{unl}^2 \cdot D_{KL}(p_{\theta_{ref}} \| p_{\theta_l})$。关键在于负号——将 KL 散度最小化转为最大化，使当前模型对遗忘目标的预测远离遗忘前保存的参考模型预测。遗忘前保存当前参数作为参考模型 $\theta_{ref}$，遗忘执行 $E_{UD}$ 个 epoch。

3. **Asymmetric Co-teaching with Different Architectures (ACD)**: 核心创新在于**非对称训练策略**：
    - **Net V（CLIP 预训练 ViT）**: 仅在高置信干净样本上训练（纯有监督），不使用未标注数据，避免性能退化
    - **Net A（随机初始化 CNN）**: 同时使用标注和未标注数据做 SSL 训练（含 consistency loss $\mathcal{L}_u$）
    - 样本选择采用交叉策略：net A 用 net V 的 GMM 概率选数据，反之亦然，缓解确认偏差
    - 训练数据 $D_t = D \setminus (D_u^{(A)} \cup D_u^{(V)})$，排除两个网络的遗忘目标

### 损失函数 / 训练策略

| 损失项 | 公式 | 适用网络 | 作用 |
|--------|------|----------|------|
| 标注样本交叉熵 $\mathcal{L}_x$ | $-\hat{\mathbf{y}}_{tx}^\top \log(p_{\theta_l}(\hat{\mathbf{x}}_{tx}))$ | Net A, Net V | 有监督学习 |
| 未标注一致性损失 $\mathcal{L}_u$ | $\|\hat{\mathbf{y}}_{tu} - p_{\theta_l}(\hat{\mathbf{x}}_{tu})\|^2$ | 仅 Net A | SSL 正则化 |
| 正则化 $\mathcal{L}_{reg}$ | DivideMix 正则化项 | Net A, Net V | 防过拟合 |
| 遗忘损失 $\mathcal{L}_{unl}$ | $-T_{unl}^2 \cdot D_{KL}(p_{\theta_{ref}} \| p_{\theta_l})$ | Net A, Net V | 移除噪声影响 |

- Net A 总损失：$\mathcal{L}^{(A)} = \mathcal{L}_x + \lambda_u \mathcal{L}_u + \mathcal{L}_{reg}$
- Net V 总损失：$\mathcal{L}^{(V)} = \mathcal{L}_x + \mathcal{L}_{reg}$（无 $\mathcal{L}_u$）
- Mixup 增强应用于所有训练样本，Net A 的 Mixup 从标注+未标注池中采样

## 实验关键数据

### 主实验

**CIFAR-100 合成噪声结果（Best accuracy %）**:

| 方法 | Sym.20% | Sym.50% | Sym.80% | Sym.90% |
|------|---------|---------|---------|---------|
| DivideMix | 77.3 | 74.6 | 60.2 | 31.5 |
| ProMix | 82.6 | 80.1 | 69.4 | 42.9 |
| RankMatch | 79.5 | 77.9 | 67.6 | 50.6 |
| NoiseBox+SS-KNN | 79.4* | 77.4* | 72.8* | 67.1* |
| CLIPCleaner | 78.2 | 75.2 | 69.7 | 63.1 |
| **ACD-U** | **83.3** | **81.6** | **74.4** | **66.5** |

*注：NoiseBox 报告的是 Last accuracy*

**真实世界噪声数据集结果**:

| 数据集/方法 | CIFAR-100N | WebVision Top1 | ImageNet Top1 | Clothing1M | Red Mini-IN 80% |
|-------------|-----------|----------------|---------------|------------|-----------------|
| DivideMix | 71.13 | 77.3 | 75.2 | 74.8 | 34.50 |
| Semi-RML++ | 73.68 | 83.0 | 78.7 | 75.4 | — |
| CLIPCleaner | — | 81.6 | 77.8 | 74.9 | 43.82 |
| **ACD-U** | **75.98** | **82.8** | **81.0** | **75.5** | **48.94** |

### 消融实验

**核心组件消融（CIFAR-100, Best accuracy %）**:

| 配置 | Sym.50% | Sym.80% |
|------|---------|---------|
| ACD-U (完整) | 81.6 | 74.4 |
| w/o unlearning | 81.6 (±0.0) | 72.7 (**-1.7**) |
| w/o ACD | 79.7 (**-1.9**) | 74.4 (±0.0) |

**遗忘目标选择条件消融（CIFAR-100 Sym.80%, Best）**:

| 配置 | Best | Δ |
|------|------|---|
| ACD-U (完整) | 74.4 | — |
| w/o Low-loss | 73.9 | -0.5 |
| w/o Loss-drop | 72.8 | -1.6 |
| w/o CLIP-consistent | 71.8 | **-2.6** |

### 关键发现

- **互补性**: Unlearning 在高噪声（80-90%）下关键（+1.7%），ACD 在中低噪声（50%）下关键（+1.9%），两者互补
- **样本选择精度提升**: ACD-U 在早期训练中将噪声样本误判为干净（HN）的数量降至 DivideMix 的 **1/6**（1127 vs 6444）
- **错误纠正能力**: DivideMix 中超过 40% 的初始误判永远无法纠正；ACD-U 通过 unlearning 在 epoch 90-150 间成功纠正这些错误
- **CLIP-consistent 条件最关键**: 移除后 Best 下降 2.6%、Last 下降 3.9%，说明外部噪声无关判据对遗忘安全性至关重要
- **跨数据集泛化**: 在 ImageNet 评估上超过 Semi-RML++ 2.3%（81.0 vs 78.7），说明学到的是鲁棒特征而非简单滤噪

## 亮点与洞察

1. **范式转换**: 从"被动避免错误"到"主动检测-遗忘-纠正错误"，这是噪声标签学习领域的重要思路突破
2. **Machine unlearning 的新应用**: 首次将原用于隐私保护的 unlearning 技术应用于 LNL，解决了 unlearning 中"遗忘目标未知"的核心挑战（传统 unlearning 假设要遗忘的数据是预先已知的）
3. **异构架构的互补利用**: 不像现有方法将预训练模型当静态工具，ACD-U 真正利用了 ViT（高初始精度、稳定预测）和 CNN（逐步适应）之间的学习动态差异
4. **三条件选择机制设计精巧**: Low-loss 捕捉已记忆样本，Loss-drop 捕捉正在被记忆的样本，CLIP-consistent 保护真正干净的样本——三者覆盖不同维度
5. **自监督 warmup 策略**: ViT 在 warmup 阶段不使用标签，避免早期过拟合噪声，这个设计在 Sym.90% 带来 3% 提升

## 局限性 / 可改进方向

1. **简单任务增益有限**: CIFAR-10 上仅比 ProMix 高 0.5-0.6%，现有方法已达 90%+ 时提升空间有限
2. **依赖 CLIP 预训练**: 在 CLIP 预训练数据未覆盖的专业领域（如医学图像）可能效果受限
3. **超参数敏感**: $T_{unl}$ 的最优范围很窄（0.05 为基线，≥0.1 即显著退化），不同数据集需要不同的 batch size（CIFAR: 512, Clothing1M: 128），调参成本较高
4. **计算开销**: 需要同时维护 ViT + CNN + 参考模型 + CLIP zero-shot 推理，资源消耗显著高于传统方法
5. **未来方向**: (a) 探索 ViT+CNN 之外的架构组合（Swin、DINOv2 等）；(b) 引入历史信息（memory bank）改进遗忘目标选择；(c) 探索 KL 散度之外的遗忘策略

## 相关工作与启发

- **DivideMix (ICLR 2020)**: ACD-U 的基础框架，GMM 样本选择 + SSL 的范式奠基者
- **SCRUB**: 提供了 KL 散度遗忘损失的灵感，原用于隐私保护
- **CLIPCleaner**: 同样使用 CLIP 但仅作为静态选择器，ACD-U 将 ViT 作为可训练组件
- **Co-teaching**: 双网络互相教学的经典范式，ACD-U 从对称扩展为非对称
- **启发**: "遗忘"作为一种主动学习策略的价值被低估——不仅可以用于隐私删除，还能用于模型质量改进；异构模型的学习动态差异是一种可被利用的资源而非需要消除的缺陷

## 评分

| 维度 | 分数 (1-10) | 说明 |
|------|-------------|------|
| 创新性 | 8 | 首次将 machine unlearning 引入 LNL，范式创新显著 |
| 技术深度 | 8 | 三组件集成设计精巧，消融分析充分证明互补性 |
| 实验充分性 | 9 | 6 个数据集、3 种噪声类型、详尽消融和超参分析 |
| 写作质量 | 8 | 结构清晰，RQ 导向的实验组织很好 |
| 实用价值 | 7 | 超参调优敏感且计算开销大，实际部署有门槛 |
| **综合** | **8.0** | 思路新颖、实验扎实的 solid work，unlearning for LNL 是一个有潜力的新方向 |
