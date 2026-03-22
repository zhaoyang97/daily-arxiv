# UniFusion: A Unified Image Fusion Framework with Robust Representation and Source-Aware Preservation

**日期**: 2026-03-15  
**arXiv**: [2603.14214](https://arxiv.org/abs/2603.14214)  
**代码**: [UniFusion](https://github.com/dusongcheng/UniFusion)  
**领域**: 多模态VLM / 图像生成  
**关键词**: image fusion, DINOv3, bilevel optimization, reconstruction alignment, cross-task generalization

## 一句话总结
提出 UniFusion，利用 DINOv3 语义先验 + reconstruction-alignment 机制 + bilevel optimization 策略，构建跨任务统一图像融合框架，在红外-可见光/医学/多曝光/多焦点四大融合任务上全面超越 TC-MoA 等 SOTA。

## 研究背景与动机

1. **领域现状**: 图像融合（多模态、多曝光、多焦点、医学）广泛应用于自动驾驶、医疗等场景。大多数方法针对特定任务设计，泛化能力差。TC-MoA 等通用融合方法尝试用 task-specific routing 统一多任务，但仍存在限制。

2. **现有痛点**: (a) 缺乏原则性的模态一致特征提取——异构信号难以在共享空间中鲁棒编码；(b) 深层传播中源图像关键信息退化（information degradation），导致融合质量下降。

3. **核心矛盾**: 要在一个模型中处理多种融合任务，需要既能提取模态一致特征（泛化性），又能保留每个源图像的独特信息（保真度）。

4. **切入角度**: DINOv3 是强大的自监督视觉模型，能提供模态一致的语义表示；用 reconstruction 约束确保编码特征能还原原图；用 bilevel optimization 平衡融合和重建。

5. **核心 idea**: DINOv3 冻结 backbone 做特征提取 → lightweight adapter 做模态适配 → cross-attention 做融合 → reconstruction 分支做信息保留约束 → bilevel optimization 同步优化。

## 方法详解

### 整体框架

双通道输入（源图像 A/B）→ 冻结的 DINOv3 backbone 提取多层语义特征 → lightweight adapter 进行模态特定适配 → cross-attention 模块融合 → 输出融合图像。同时，adapter 特征经 reconstruction 分支还原原图做自监督约束。

### 关键设计

1. **DINOv3 Semantic Prior Adaptation**:
   - 做什么：用预训练的 DINOv3 ViT 做通用特征提取
   - 核心思路：冻结 DINOv3 backbone，提取 4 个中间层的特征 $f^{(l_2)}, f^{(l_5)}, f^{(l_8)}, f^{(l_{11})}$，通过 hierarchical adapter 做渐进式特征校准和上采样
   - 设计动机：DINOv3 在大规模自然图像上预训练，具备 object-centric 和长程依赖建模能力，是理想的跨模态通用 backbone。adapter 弥补了预训练域和特定模态之间的 gap

2. **Reconstruction Alignment**:
   - 做什么：确保编码特征保留足够的源图像信息
   - 核心思路：每个 adapter 的输出 $\hat{\mathbf{F}}_m$ 经轻量 Transformer blocks + projection head 重建原图 $\bar{I}_m = R_m(\hat{\mathbf{F}}_m)$，用 L1 loss 监督
   - 设计动机：直接融合可能导致模态特有信息丢失（如红外的热辐射、可见光的纹理）。重建约束迫使编码保留完整信息，比 pixel-level 融合 loss 更能保持语义一致性

3. **Bilevel Optimization**:
   - 做什么：解耦并联合优化重建和融合目标
   - 核心思路：inner loop 快速更新 adapter+reconstruction 参数 $\phi$（学好特征表示）；outer loop 慢速更新 fusion 参数 $\theta$（学好融合策略）。学习率 $\eta_L > \eta_U$，加 EMA 稳定
   - 设计动机：重建和融合有耦合关系——如果 joint optimize 可能互相干扰。bilevel 让特征表示先稳定下来，再基于好的特征学融合策略

### 损失函数
- Inner level: $\mathcal{L}_\text{rec}$ (L1 reconstruction loss)
- Outer level: $\mathcal{L}_\text{fuse}$ (SwinFusion 的融合 loss)
- 交替优化，EMA momentum α 稳定 fusion 参数

## 实验关键数据

### 主实验（红外-可见光融合）

| 方法 | MI↑ | VIF↑ | Q_abf↑ | Q_y↑ |
|------|-----|------|--------|------|
| CDDFuse | 3.776 | 0.839 | 0.610 | 0.978 |
| TC-MoA | 3.466 | 0.870 | 0.636 | 0.983 |
| **UniFusion** | **4.268** | **0.899** | **0.637** | 0.982 |

### 消融实验

| 配置 | MI (M3FD) | VIF (M3FD) |
|------|-----------|-----------|
| w/o Adapter | 3.646 | 0.863 |
| w/o DINOv3 encoder | 3.681 | 0.879 |
| w/o Reconstruction | 3.846 | 0.870 |
| w/o Bilevel Optimization | 3.924 | 0.876 |
| **Full UniFusion** | **4.268** | **0.899** |

### 关键发现
- 每个组件都有明显贡献，其中 DINOv3 backbone 和 Adapter 的贡献最大（去掉后 MI 分别降 0.587 和 0.622）
- 在 MFIF（多焦点融合）上，即使没做任务特定微调也能排名前二，说明框架泛化性强
- Medical image fusion 对比可视化显示，UniFusion 在保留 MRI 解剖结构的同时准确整合 PET 功能信息

## 亮点与洞察
- **DINOv3 做图像融合 backbone**: 首次将自监督大视觉模型用于通用图像融合，提供了强大的模态一致语义先验
- **Bilevel optimization 解耦融合与重建**: 避免两个目标互相干扰，是一种通用的多任务训练策略
- **四大融合任务统一**: 一个模型处理 IVIF/MIF/MEF/MFF，且都达到 SOTA 或接近

## 局限性 / 可改进方向
- DINOv3 backbone 冻结不训练，可能无法充分适配极端模态（如 SAR、热成像等非自然图像）
- Bilevel optimization 的交替优化增加了训练复杂度和调参成本
- 只用了 10000 iterations 训练，对更大数据集和更复杂场景的 scalability 未验证
- 缺少推理速度对比——冻结的 DINOv3 ViT 可能推理较慢

## 相关工作与启发
- **vs TC-MoA**: task-specific routing → UniFusion 用统一 backbone + bilevel，更简洁
- **vs SwinFusion**: Swin Transformer 做融合 → UniFusion 用更强的 DINOv3 预训练特征
- **vs CDDFuse**: cross-domain Transformer → UniFusion 通过重建约束更好保留源信息

## 评分
- 新颖性: ⭐⭐⭐⭐ DINOv3 + bilevel optimization 的组合新颖，但各组件（adapter、reconstruction loss）较常规
- 实验充分度: ⭐⭐⭐⭐⭐ 覆盖四大融合任务 + 完整消融 + 下游任务验证
- 写作质量: ⭐⭐⭐⭐ 图表丰富，动机清晰
- 价值: ⭐⭐⭐⭐ 统一融合框架的实用价值高
