# Back to Point: Exploring Point-Language Models for Zero-Shot 3D Anomaly Detection

**日期**: 2026-03-23  
**arXiv**: [2603.21511](https://arxiv.org/abs/2603.21511)  
**代码**: [BTP-3DAD](https://github.com/wistful-8029/BTP-3DAD)  
**领域**: 3D视觉 / AI安全  
**关键词**: 零样本3D异常检测, Point-Language Model, 多粒度特征融合, 几何描述子, ULIP

## 一句话总结

首次将预训练 Point-Language Model (PLM) 应用于零样本 3D 异常检测，提出 BTP 框架，通过多粒度特征嵌入模块 (MGFEM) 和几何特征创建模块 (GFCM) 直接在点云空间实现细粒度异常定位，避免了传统 VLM 方法的 3D→2D 投影信息损失。

## 研究背景与动机

1. **领域现状**：零样本 3D 异常检测是工业质检的关键任务，现有方法多依赖 VLM（如 CLIP）将点云渲染为多视角 2D 图像后进行异常检测。
2. **现有痛点**：3D→2D 投影不可避免地丢失几何细节，且对局部异常敏感度有限；性能高度依赖渲染视角数量和角度选择，存在 view-selection bias。
3. **核心矛盾**：VLM-based 方法虽然能利用强大的视觉-语言对齐能力，但代价是牺牲了 3D 点云固有的结构与几何信息，而 3D 异常往往表现为微妙的结构形变和局部几何变化。
4. **本文要解决什么**：如何在不经过 3D-to-2D 转换的前提下，直接利用预训练 PLM 的点云-文本对齐能力进行零样本 3D 异常检测和定位。
5. **切入角度**：从 ULIP 等 PLM 出发，设计多粒度特征融合策略，同时引入可学习的几何描述子替代传统手工特征 FPFH，实现端到端的联合优化。
6. **核心 idea 一句话**：回归点云本身（Back To Point），通过多粒度语义-几何融合在 PLM 的文本对齐空间中实现零样本异常检测。

## 方法详解

### 整体框架

输入点云经 3D 编码器（Point-BERT based ULIP）提取多层 patch 特征、全局 CLS token 和 global embedding，同时由 GFCM 提取几何描述子。MGFEM 将这三类特征融合投影到文本对齐空间，与 learnable text prompt（正常/异常）的文本嵌入计算相似度，分别实现 object-level（全局嵌入 vs 文本）和 point-level（patch 嵌入 vs 文本）的异常检测。

### 关键设计

**Multi-Granularity Feature Embedding Module (MGFEM)**

- **做什么**：将多层中间语义特征、几何描述子、CLS token 融合为 patch 级别的结构感知表示
- **核心思路**：对各层语义特征做 softmax 加权聚合，与几何特征和 CLS token 拼接后通过融合层投影到文本嵌入维度 $\mathbf{Z} = \phi_f([\sum_l \alpha_l \mathbf{S}^{(l)} \| \mathbf{G} \| \mathbf{C}])$
- **设计动机**：仅使用最终层全局嵌入对局部异常不敏感，中间层包含不同抽象级别的几何和语义信息

**Geometric Feature Creation Module (GFCM)**

- **做什么**：基于 PointNet 的可学习几何描述子，替代传统不可学习的 FPFH
- **核心思路**：对每个 patch 的邻域点通过共享 MLP 提取点级特征，max-pooling 聚合后投影到文本嵌入维度 $\mathbf{f}_i = \phi(\max_j \text{MLP}(\mathbf{p}_{ij}))$
- **设计动机**：FPFH 虽然能编码局部几何，但无法端到端优化，表征能力受固定特征空间限制

**Hybrid Learnable Prompt**

- **做什么**：结合可学习 context token 与固定模板（"normal object" / "defective object"）生成文本提示
- **核心思路**：少量可学习 token 插入类别前后缀之间，由 ULIP 文本编码器生成正/负文本嵌入
- **设计动机**：保留自然语言语义先验的同时自适应对齐数据集分布

### 损失函数 / 训练策略

三级联合损失：$\mathcal{L} = \mathcal{L}_{\text{local}} + \lambda_1 \mathcal{L}_{\text{global}} + \lambda_2 \mathcal{L}_{\text{geo}}$

- **$\mathcal{L}_{\text{local}}$**：Focal Loss + Dice Loss，解决正常/异常点严重不平衡，同时优化区域覆盖
- **$\mathcal{L}_{\text{global}}$**：融合 point-level 和 patch-level 预测后的 BCE Loss，用于 object-level 判别
- **$\mathcal{L}_{\text{geo}}$**：将学习到的几何特征与 FPFH 描述子做对比学习对齐（cosine-based InfoNCE），$\lambda_1=0.5, \lambda_2=0.1$

训练使用 AdamW 优化器，10% linear warmup + cosine annealing，最小学习率 $1 \times 10^{-6}$，输入 2048 点（FPS 采样），单卡 RTX 4090，结果为 10 次独立运行平均。

## 实验关键数据

### 主实验

| 方法 | Real3D-AD O-AUROC | Real3D-AD P-AUROC | Anomaly-ShapeNet O-AUROC | Anomaly-ShapeNet P-AUROC |
|------|:-:|:-:|:-:|:-:|
| PointAD (ZS) | 74.8 | 73.5 | — | — |
| AnomalyCLIP (ZS) | 55.2 | 50.3 | — | — |
| CPMF | 58.6 | 75.9 | — | — |
| **BTP (Ours)** | **61.4** | **84.5** | **65.2** | **87.3** |

### 消融实验

| 配置 | Real3D O-AUROC/AP | Real3D P-AUROC/PRO | ShapeNet O-AUROC/AP | ShapeNet P-AUROC/PRO |
|------|:-:|:-:|:-:|:-:|
| Baseline | 51.5/54.5 | —/— | 53.9/60.7 | —/— |
| +MGFEM | 59.9/63.3 | 83.3/80.1 | 61.4/68.9 | 83.5/79.0 |
| +GFCM only | 52.5/57.4 | 55.0/55.0 | 53.8/61.1 | 52.0/51.2 |
| Full | 61.4/65.1 | 84.5/81.9 | 65.2/71.4 | 87.3/82.2 |
| w/o $\mathcal{L}_{\text{geo}}$ | 61.3/64.8 | 82.2/80.2 | 60.9/68.6 | 74.1/70.2 |
| w/o $\mathcal{L}_{\text{local}}$ | 60.3/64.1 | 68.8/66.2 | 61.1/68.8 | 62.4/55.7 |

### 关键发现

- BTP 在 point-level 定位上大幅领先：Real3D-AD P-AUROC 84.5% 超过第二名 CPMF 的 75.9%（+8.6%），12 个类别中 8 个排名第一
- Object-level 上 BTP (61.4%) 低于 PointAD (74.8%)，但在 ZS 方法中排第二，且 PointAD 依赖多视角渲染
- MGFEM 是核心：仅加 GFCM 几乎无提升，但 MGFEM+GFCM 组合效果最佳
- 去掉 $\mathcal{L}_{\text{local}}$ 导致 point-level 性能断崖式下降（84.5→68.8），证明局部监督对定位至关重要
- 输入 2048 点为最优平衡点（P-AUROC 84.5%，FPS 73.8）

## 亮点与洞察

- **范式转换**：首次将 PLM 引入 ZS 3D 异常检测，绕开了 VLM-based 方法的 3D→2D 投影瓶颈
- **可学习几何描述子**：GFCM 作为 FPFH 的端到端可学习替代方案，概念简洁但有效
- **多粒度融合的必要性**：单一全局嵌入无法捕捉局部异常，多层中间特征 + 几何 + CLS 的组合显著提升定位能力
- **跨类别泛化性强**：大多数训练类别的跨类测试均值 P-AUROC > 80%

## 局限性 / 可改进方向

- Object-level 检测落后于 PointAD（61.4 vs 74.8），全局判别能力有待加强
- 仅在 ULIP2 上验证，未探索其他 PLM（如 OpenShape、PointBind）的潜力
- 训练需要辅助点云数据和异常标注用于 joint representation learning，并非完全"零样本"
- 未考虑点云密度不均匀或大规模场景的情况
- 可学习 prompt 长度固定为 4，未探索动态 prompt 长度对性能的影响

## 相关工作与启发

- **vs PointAD**：PointAD 将点云渲染为多视角 2D 图像用 CLIP 检测，object-level 更强但 point-level 弱（73.5 vs 84.5）；BTP 直接在 3D 空间操作，保留几何细节
- **vs PLANE**：PLANE 也基于 PLM 但需要目标类别数据进行 category-specific 训练/适配，BTP 实现真正零样本
- **vs CPMF/M3DM**：传统 memory-bank 方法需要正常样本训练，BTP 无需任何目标类训练数据

## 评分

| 维度 | 分数 (1-10) | 说明 |
|------|:-:|------|
| 新颖性 | 8 | 首次将 PLM 用于 ZS 3D 异常检测，范式新颖 |
| 实验充分度 | 7 | 两个数据集 + 详细消融，但 object-level 结果不理想 |
| 写作质量 | 7 | 结构清晰，公式表述规范 |
| 价值 | 8 | 为 3D 异常检测开辟了 PLM-based 新方向 |
**领域**: 3D视觉 / 异常检测  
**关键词**: zero-shot, 3D anomaly detection, point-language model, ULIP, geometric descriptor

## 一句话总结
首次用预训练 Point-Language Model（ULIP2）做零样本 3D 异常检测——提出 BTP 框架，通过多粒度特征嵌入模块（MGFEM，融合多层 patch 语义+可学习几何描述子+全局 CLS token）与混合可学习文本提示对齐，配合三路联合损失，在 Real3D-AD 点级 AUROC 达 84.5%，大幅超越 PointAD 的 73.5%。

## 研究背景与动机

1. **领域现状**: 零样本 3D 异常检测的主流做法是将点云渲染为多视图 2D 图片，用 CLIP 等 VLM 对齐文本做检测（如 PointAD、MVP）。无监督方法（IMRNet、R3D-AD）依赖重建或记忆库，泛化能力有限。

2. **现有痛点**: 3D → 2D 渲染不可避免地丢失几何细节，对局部结构异常不敏感；性能严重依赖视角数量和选择；反投影计算开销大；且每换一个视角，检测结果可能不一致。

3. **核心矛盾**: 异常检测需要精细的几何感知（凹陷、裂纹、变形），但 VLM 只"看"到 2D 渲染图，几何信息在投影中丢失。PLM（如 ULIP）已能对齐点云和文本，但只用全局嵌入做分类，不能做细粒度定位。

4. **切入角度**: 扩展 ULIP 的使用方式——不只用最终全局嵌入，还提取中间层 patch 特征做点级定位；引入可学习几何描述子补充结构信息；三路联合损失同时优化全局判别、局部定位和几何感知。

5. **核心 idea**: 直接在点云空间做零样本异常检测，多粒度特征对齐文本 = 保留几何保真度 + 无需视角选择 + 点级精细定位。

## 方法详解

### 整体框架
输入点云（FPS 下采样至 2048 点）→ 双路特征提取：(1) ULIP2 编码器获取全局嵌入 + 中间层 patch 特征 + CLS token；(2) GFCM 几何特征创建模块从局部点集提取可学习几何描述子。两路经 MGFEM 融合后，与混合可学习文本提示的嵌入做相似度计算，输出物体级和点级异常分数。

### 关键设计

1. **Patch 级特征挖掘**:
    - 做什么：从 ULIP 编码器第 2/5/8/11 层提取中间层 patch 表示
    - 核心思路：不同层捕获不同抽象级别的几何和语义信息，多层融合增强局部变化敏感度
    - 设计动机：ULIP 原本只用最终全局嵌入，对点级异常不敏感

2. **几何特征创建模块（GFCM）**:
    - 做什么：用 PointNet 架构从每个 patch 的局部点集提取可学习几何描述子
    - 公式：$\mathbf{f}_i = \phi(\max_{j=1,...,M} \text{MLP}(\mathbf{p}_{ij}))$
    - 设计动机：替代不可学习的 FPFH，可端到端优化且表达能力更强
    - 额外监督：通过对比损失将 GFCM 输出与 FPFH 对齐

3. **多粒度特征嵌入模块（MGFEM）**:
    - 做什么：融合三类信息——多层语义特征、几何特征、CLS token
    - 核心思路：先投影到统一嵌入空间，再 concat + fusion 层得到 $\mathbf{Z} \in \mathbb{R}^{N \times D}$
    - 层间权重 $\alpha_l$ 通过 softmax 自适应学习

4. **混合可学习文本提示**: 4 个可学习 token 插入 "normal"/"defective" 模板之间

### 损失函数
$\mathcal{L} = \mathcal{L}_{local} + 0.5 \mathcal{L}_{global} + 0.1 \mathcal{L}_{geo}$
- $\mathcal{L}_{local}$：Focal + Dice loss
- $\mathcal{L}_{global}$：BCE loss（融合点级和 patch 级预测）
- $\mathcal{L}_{geo}$：对比损失（GFCM 与 FPFH 对齐）

## 实验关键数据

### Real3D-AD 主实验

| 方法 | 类型 | 点级 AUROC | 物体级 AUROC |
|------|------|-----------|-------------|
| CPMF | 监督 | 75.9 | 58.6 |
| PointAD | ZS (VLM) | 73.5 | 74.8 |
| AnomalyCLIP | ZS (VLM) | 50.3 | 55.2 |
| **BTP (Ours)** | **ZS (PLM)** | **84.5** | 61.4 |

### 消融实验

| 配置 | 点级 AUROC |
|------|-----------|
| 仅全局嵌入 | 基线 |
| + Patch 特征 | 显著提升 |
| + GFCM | 进一步提升 |
| + 联合三路损失 | **84.5** |

### 关键发现
- 点级定位是 BTP 强项：84.5% 大幅超越所有基线（含监督方法），因为直接在 3D 空间做 patch 级对齐保留完整几何
- 物体级检测较弱（61.4%），ULIP 全局嵌入的异常判别力不如 VLM 多视图聚合
- 中间层（5, 8 层）贡献最大，印证"中间层保留更多结构信息"假设
- 跨类别泛化：在一个类别训练，其他类别测试，平均 P-AUROC 仍保持可用

## 亮点与洞察
- **回归 3D 本源**: 首次证明 PLM 在零样本 3D 异常检测中可超越 VLM-based 方法的点级定位能力
- **可学习几何描述子（GFCM）**: 用 PointNet 替代 FPFH，既能端到端训练又保留手工特征先验
- **多粒度互补性**: 全局做判别、Patch 做定位、几何做结构增强，三位一体

## 局限性 / 可改进方向
- 物体级检测（61.4%）明显弱于 PointAD（74.8%），全局嵌入判别力有限
- 仅在 Real3D-AD 和 Anomaly-ShapeNet 验证，真实工业场景（遮挡、噪声）未测试
- ULIP2 预训练数据与工业缺陷数据的 domain gap 未探讨

## 相关工作与启发
- **vs PointAD**: 渲染多视图+CLIP 物体级更强但点级更弱；BTP 直接 3D 操作点级优势大
- **vs PLANE**: 也用 PLM 但需目标类别数据适配；BTP 真正零样本

## 评分
- 新颖性: ⭐⭐⭐⭐ 首次将 PLM 用于零样本 3D 异常检测
- 实验充分度: ⭐⭐⭐⭐ 两个基准 + 跨类别泛化 + 完整消融
- 写作质量: ⭐⭐⭐⭐ 结构清晰，公式规范
- 价值: ⭐⭐⭐⭐ 开辟 3D 异常检测新范式

