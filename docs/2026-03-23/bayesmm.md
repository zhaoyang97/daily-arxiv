# BayesMM: Adapting Point Cloud Analysis via Multimodal Bayesian Distribution Learning

**日期**: 2026-03-23  
**arXiv**: [2603.22070](https://arxiv.org/abs/2603.22070)  
**代码**: 无  
**领域**: 3D视觉 / 点云分析  
**关键词**: test-time adaptation, point cloud, Bayesian fusion, multimodal, distribution learning

## 一句话总结

提出 BayesMM，用高斯分布建模文本先验和流式视觉特征，通过贝叶斯模型平均自动调节两模态权重，实现 training-free 的测试时点云分析适配，在多个点云基准上平均提升 4%+ 鲁棒性。

## 研究背景与动机

1. **领域现状**: 大规模多模态 3D 模型（ULIP、ULIP-2、OpenShape、Uni3D）通过点云-图像-文本对比预训练实现零样本泛化，但面对域偏移（corruptions、sim-to-real gap）时性能显著下降。
2. **Cache-based TTA 的局限**: 现有 cache-based 方法（如 Point-Cache）仅存储有限数量的高置信度样本，随测试流演化信息逐步丢失；cache 替换策略导致长期分布统计信息被丢弃，容易出现灾难性遗忘。
3. **启发式融合的不稳定性**: cache logits 与 zero-shot logits 的融合依赖手调超参 $\lambda, \gamma$，缺乏理论原则，跨域泛化不稳定。
4. **核心矛盾**: 离散样本缓存 vs. 连续分布建模——前者信息损失大，后者能完整保留类别统计量。
5. **切入角度**: 用高斯分布参数化刻画每个类的特征分布——文本端从 LLM 生成的语义 prompt 变体推导先验，视觉端从流式测试样本在线递归更新。
6. **核心 idea**: 高斯分布建模 + 在线参数递归更新 + 贝叶斯模型平均融合 = 原则性的 training-free 多模态 TTA，无需任何超参手调即可自动平衡模态贡献。

## 方法详解

### 整体框架

冻结点云编码器 $\Phi$ + 冻结文本编码器 $\Psi$，投射到共享 $\mathbb{R}^d$ 特征空间。为每个类 $c$ 建立：

- **文本高斯** $\mathcal{N}(\boldsymbol{\nu}^c_{\mathsf{MAP}}, \mathbf{S}^c)$：从 prompt 变体推导
- **几何高斯** $\mathcal{N}(\boldsymbol{\mu}_t^c, \boldsymbol{\Sigma}_t^c)$：从测试流在线递归更新

预测时通过贝叶斯模型平均（Bayesian Model Averaging）融合两模态后验，自动调节权重。

### 关键设计

#### 1. 文本先验分布学习（Textual Distribution Learning）

对每个类 $c$，用 LLM 将基础 prompt "a 3D object of {class}" 扩展为 $M$ 个语义描述变体，得到嵌入集合 $\{\mathbf{z}^{c,1}, \dots, \mathbf{z}^{c,M}\}$。计算经验均值和协方差：

$$\bar{\mathbf{z}}^c = \frac{1}{M}\sum_{i=1}^M \mathbf{z}^{c,i}, \quad \mathbf{S}^c = \sum_{i=1}^M (\mathbf{z}^{c,i} - \bar{\mathbf{z}}^c)(\mathbf{z}^{c,i} - \bar{\mathbf{z}}^c)^\top$$

对文本原型 $\boldsymbol{\nu}^c$ 施加高斯先验 $p(\boldsymbol{\nu}^c) = \mathcal{N}(\boldsymbol{\nu}^c \mid \bar{\mathbf{z}}^c, \beta^2 \mathbf{I})$，结合似然 $p(\mathbf{x}_t \mid \boldsymbol{\nu}^c, \mathbf{S}^c)$ 做 MAP 估计：

$$\boldsymbol{\nu}^c_{\mathsf{MAP}} = (\beta^{-2}\mathbf{I} + M(\mathbf{S}^c)^{-1})^{-1} (\mathbf{S}^c)^{-1} \bar{\mathbf{z}}^c$$

实践中所有类共享协方差 $\mathbf{S}$，等价于 Dirac 先验 $p(\mathbf{S}^c) = \delta(\mathbf{S}^c - \mathbf{S})$。

#### 2. 几何分布在线学习（Geometric Distribution Learning）

每个类维护在线高斯参数 $\boldsymbol{\Theta}_t^c = \{\boldsymbol{\mu}_t^c, \boldsymbol{\Sigma}_t^c\}$。初始时刻以文本原型为锚点：

$$p(\boldsymbol{\mu}_0^c) = \mathcal{N}(\boldsymbol{\mu}_0^c \mid \bar{\mathbf{z}}^c, \alpha^2 \mathbf{I}), \quad \boldsymbol{\Sigma}_0^c = \mathbf{S}^c$$

新样本 $\mathbf{x}_t$ 到达后，贝叶斯递归更新（closed-form）：

$$\boldsymbol{\mu}_t^c = \boldsymbol{\Sigma}_t^c \big((\boldsymbol{\Sigma}^c)^{-1}\mathbf{x}_t + (\boldsymbol{\Sigma}_{t-1}^c)^{-1}\boldsymbol{\mu}_{t-1}^c\big)$$
$$\boldsymbol{\Sigma}_t^c = \big((\boldsymbol{\Sigma}_{t-1}^c)^{-1} + (\boldsymbol{\Sigma}^c)^{-1}\big)^{-1}$$

每个新样本到达只需一次矩阵运算，无需存储历史样本。

#### 3. 贝叶斯模型平均（Bayesian Model Averaging）

融合两模态后验得到最终预测：

$$p(c \mid \mathbf{x}_t) = \underbrace{p(c \mid \mathbf{x}_t, \boldsymbol{\Omega}^c)\,p(\boldsymbol{\Omega}^c \mid \mathbf{x}_t)}_{\text{文本后验预测}} + \underbrace{p(c \mid \mathbf{x}_t, \boldsymbol{\Theta}_t^c)\,p(\boldsymbol{\Theta}_t^c \mid \mathbf{x}_t)}_{\text{几何后验预测}}$$

其中 $p(\boldsymbol{\Omega}^c \mid \mathbf{x}_t)$ 和 $p(\boldsymbol{\Theta}_t^c \mid \mathbf{x}_t)$ 为贝叶斯证据权重，自动调节模态贡献——无需手调超参。每个模态内部用高斯判别分析（GDA）计算归一化后验。

### 损失函数 / 训练策略

**完全 training-free**，无需任何损失函数或梯度更新：

- 编码器参数全程冻结，不引入额外可学习参数
- 文本分布在推理前一次性计算完成（预处理阶段）
- 几何分布通过贝叶斯递归在线更新，无需反向传播
- 超参 $\alpha^2, \beta^2$ 对性能不敏感，无需精细调参

## 实验关键数据

### 主实验：ModelNet-C 鲁棒性（Table 1）

| 方法 | Clean | Add Global | Add Local | Drop Global | Drop Local | Rotate | Scale | Jitter | **Avg.** |
|------|-------|-----------|-----------|------------|-----------|--------|-------|--------|---------|
| ULIP | 56.16 | 33.55 | 43.92 | 54.70 | 50.89 | 55.27 | 50.20 | 44.08 | 48.60 |
| + Point-Cache (H) | 64.22 | 46.15 | 47.85 | 59.16 | 56.00 | 61.47 | 55.35 | 49.92 | 55.02 |
| **+ BayesMM** | **66.04** | **54.82** | **53.93** | **63.09** | **60.13** | **63.82** | **60.49** | **53.04** | **59.42** |
| Uni3D | 81.81 | 72.45 | 56.36 | 68.15 | 67.18 | 79.94 | 75.36 | 56.24 | 69.69 |
| + Point-Cache (H) | 83.87 | 77.51 | 71.15 | 72.16 | 70.75 | 81.77 | 77.31 | 62.52 | 74.63 |
| **+ BayesMM** | **85.17** | **77.59** | **73.30** | **74.96** | **71.88** | **83.75** | **79.98** | **65.84** | **76.56** |

BayesMM 在 ULIP 上平均提升 **+10.82%**，在 Uni3D 上提升 **+6.87%**。

### 主实验：跨数据集泛化（Table 2）

| 方法 | ModelNet40 | S-PB_RS_T50 | O-LVIS | Omni3D (1k/4k/16k) | **Avg.** |
|------|-----------|------------|--------|-------------------|---------|
| Uni3D | 88.41 | 65.19 | 55.42 | 31.52 / 41.98 / 41.86 | 54.09 |
| + Point-Cache (H) | 89.18 | 68.24 | 55.19 | 35.82 / 45.60 / 45.89 | 56.65 |
| **+ BayesMM** | **90.48** | **73.04** | 53.63 | **36.54 / 45.97 / 46.68** | **57.72** |

跨 4 个 backbone 平均改进 **+3.6%~+4.2%**。

### 消融实验（Table 4, ULIP-2）

| 几何分布 | 文本分布 | 贝叶斯融合 | S-OBJ | Omni3D |
|---------|---------|-----------|-------|--------|
| ✗ | ✗ | ✗ | 42.00 | 26.58 |
| ✔ | ✗ | ✗ | 46.47 | 26.63 |
| ✗ | ✔ | ✗ | 52.50 | 30.79 |
| **✔** | **✔** | **✔** | **53.02** | **31.12** |

- 文本分布贡献最大（+10.5 / +4.2），提供稳定语义先验
- 几何分布提供在线适应性（+4.5 / +0.05）
- 贝叶斯融合在两者基础上进一步提升（+0.5 / +0.3）

### 关键发现

- **分布一致性持续改善**: KL 散度从 17.2 降至 12.6，MMD 从 0.91 降至 0.71（t1→t4，500→2000 样本），表明贝叶斯融合持续优化跨模态对齐
- **文本模态主导**: 权重分析显示文本模态始终获得更高权重（clean 和 corrupted 场景均如此），反映其更强的语义稳定性
- **超参不敏感**: $\alpha^2$ 和 $\beta^2$ 在较大范围内变化时精度波动 <0.5%，ULIP 稳定在 ~59.4%，ULIP-2 稳定在 ~65.2%
- **内存高效**: 从 40 类扩展到 1156 类时，Point-Cache 增加 ~18MB，BayesMM 仅增加 ~4MB（共享协方差结构）
- **吞吐量保持**: 推理速度保持 zero-shot 的 97%+ (如 ULIP: 10.99 vs 11.35 samples/s)

## 亮点与洞察

1. **分布 vs. 缓存的范式转变**: 用连续高斯分布替代离散样本缓存，从根本上解决了 cache 容量有限导致的信息衰减问题；分布参数天然聚合了历史信息
2. **贝叶斯原则性融合**: 模态权重由后验证据自动决定，避免了 cache-based 方法中 $\lambda, \gamma$ 等超参的人工调节，理论上更优雅
3. **文本先验的巧妙利用**: 用 LLM 生成 prompt 变体来估计文本分布的协方差，将语言模型的多样性转化为不确定性度量
4. **Training-free 的实用性**: 无需任何梯度/训练，直接在冻结模型上做推理时适配，部署友好

## 局限性 / 可改进方向

1. **高斯假设的局限**: 特征分布未必是高斯的，特别是在大类别数（O-LVIS 1156 类）场景下可能出现多模态分布，需要混合高斯或非参数方法
2. **O-LVIS 上偶有下降**: Table 2 中 OpenShape 和 Uni3D 在 O-LVIS 上 BayesMM 略低于 Point-Cache（43.93 vs 45.63，53.63 vs 55.19），说明大规模细粒度场景下分布估计可能不够准确
3. **共享协方差的简化**: 所有类共享 $\mathbf{S}$，丢失了类间差异信息，对形状差异极大的类别（如 1156 类场景）可能不够
4. **缺少与更多 TTA 方法对比**: 只比较了 Point-Cache 系列，未与 TENT、MEMO 等通用 TTA 方法对比
5. **Sim-to-Real 提升不均匀**: 在 Uni3D 上 Sim-to-Real 提升仅 +1.87%，远低于 ULIP 的 +4.35%，对强 backbone 边际收益递减

## 相关工作与启发

- **Point-Cache [ECCV 2024]**: 本文的直接对比基线，用离散缓存做 TTA，BayesMM 从分布视角统一了其思想
- **DOTA [2024]**: 在 2D VLM 上做高斯参数在线估计的 TTA，BayesMM 将其扩展到 3D 多模态场景
- **GDA 经典方法**: 高斯判别分析为本文提供了理论框架，BayesMM 本质上是在线版本的多模态 GDA
- **启发**: 分布学习的思路可以迁移到其他 TTA 场景（如 2D 图像、视频理解），贝叶斯模型平均是融合多模态/多源信息的通用工具

## 评分

- **新颖性**: ⭐⭐⭐⭐ 贝叶斯分布学习替代离散缓存的思路在 3D TTA 中是新的，理论推导完整
- **实验充分度**: ⭐⭐⭐⭐ 4 个 backbone × 多个基准 × 消融 + 超参敏感性 + 内存/吞吐分析，较全面
- **写作质量**: ⭐⭐⭐⭐ 公式推导清晰，图表直观，故事线连贯
- **实用价值**: ⭐⭐⭐⭐ training-free + 低内存开销 + 高吞吐量，适合实际部署
- **综合评分**: ⭐⭐⭐⭐ 3D 点云 TTA 领域扎实的工作，方法优雅但高斯假设存在理论天花板
