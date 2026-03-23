# CMHANet: A Cross-Modal Hybrid Attention Network for Point Cloud Registration

**日期**: 2026-03-13  
**arXiv**: [2603.12721](https://arxiv.org/abs/2603.12721)  
**代码**: [CMHANet](https://github.com/DongXu-Zhang/CMHANet)  
**领域**: 3D视觉 / 点云配准  
**关键词**: point cloud registration, cross-modal fusion, hybrid attention, 2D-3D, contrastive learning

## 一句话总结
提出 CMHANet，通过跨模态混合注意力机制融合 2D 图像纹理特征和 3D 点云几何特征，结合对比学习优化函数增强噪声和低重叠场景下的鲁棒性，在 3DMatch/3DLoMatch 上达到 SOTA 配准召回率。

## 研究背景与动机
- 点云配准是 3D 重建和 AR 的基础任务，但真实场景中的不完整数据、传感器噪声和低重叠区域导致现有方法退化
- 大多数方法仅用几何信息，忽略了 RGB 图像中丰富的纹理和语义上下文
- RGB-D 传感器天然提供互补的 2D+3D 数据流

## 方法详解
### 整体框架
平行编码器（KPConv-FPN 提取点云特征 + 图像编码器提取视觉特征）→ 三阶段跨模态注意力管线（建立几何-视觉联合特征空间）→ 混合注意力机制精炼匹配 → 密集对应优化 → 刚性变换估计

### 关键设计
1. **跨模态混合注意力**: 三种注意力机制建模 2D-3D 特征的复杂关系，超越简单拼接
2. **对比学习优化目标**: 联合促进几何一致性和语义连贯性
3. **超点-密集点两阶段匹配**: 先粗后精

## 实验关键数据
- 3DMatch: 最高配准召回率
- 3DLoMatch（低重叠挑战性场景）: 显著优于单模态方法
- TUM RGB-D 零样本迁移验证泛化能力

## 评分
- 新颖性: ⭐⭐⭐ 2D-3D 融合非新方向，但混合注意力设计有效
- 实验充分度: ⭐⭐⭐⭐ 3DMatch/3DLoMatch + 零样本迁移
- 价值: ⭐⭐⭐⭐ 利用日益普及的 RGB-D 数据的实用方案
