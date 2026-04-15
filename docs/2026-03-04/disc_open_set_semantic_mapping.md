# DISC: 大规模开放集语义建图

**日期**: 2026-03-04  
**arXiv**: [2603.03935](https://arxiv.org/abs/2603.03935)  
**代码**: https://github.com/DFKI-NI/DISC  
**领域**: 3D视觉  
**关键词**: open-set semantic mapping, CLIP, single-pass feature extraction, GPU-accelerated, voxel-based refinement

## 一句话总结

DISC 提出全 GPU 加速的 3D 语义建图架构，通过单次前传的距离加权 CLIP 特征提取替代裁剪式方法、体素级在线实例精炼替代离线后处理，在 Replica/ScanNet 上超越 zero-shot SOTA 并首次支持大规模多层建筑的实时连续建图。

## 研究背景与动机

1. **领域现状**：开放集语义建图通过 CLIP 等视觉-语言基础模型将自然语言查询锚定到 3D 场景中。ConceptGraphs、BBQ、Core-3D 等实例级方法构建 3D 语义场景图（3DSSG），支持复杂查询。
2. **现有痛点**：(a) 现有方法依赖裁剪图像再过 CLIP 的流程——裁剪导致全局上下文丢失、domain shift 劣化 zero-shot 能力、且每个实例需独立推理，计算量与实例数成正比；(b) 数据关联靠粗粒度 AABB overlap，需要周期性离线精炼来修复过分割，不适合在线部署。
3. **核心矛盾**：高精度语义特征需要完整图像上下文（CLIP 的训练分布），但实例级特征又需要空间隔离避免"特征 bleeding"——裁剪和不裁剪各有弊端。
4. **本文要解决什么？** (1) 不裁剪就获得高保真实例级 CLIP 特征；(2) 取消离线精炼，实现在线逐帧实例融合；(3) 支持大规模多层建筑的连续建图。
5. **切入角度**：受 MaskCLIP 启发，从 CLIP ViT 中间层直接提取 dense patch-level 特征，用空间显著性图加权而非简单平均；数据关联从 AABB 升级为精确体素交集。
6. **核心 idea 一句话**：单次 CLIP 前传提取密集 patch 特征 + 全 GPU 体素级在线精炼，实现大规模实时开放集语义建图。

## 方法详解

### 整体框架

每帧 RGB-D 输入：FastSAM 分割 → DINOv2 + CLIP 并行特征提取 → 3D 体素化 → BVH 碰撞检测找候选 → 体素交集精确匹配 → 实例融合/创建 → CLIP 特征质量更新。全流程 GPU 常驻。

### 关键设计

1. **单次前传密集 CLIP 特征提取**:
    - 做什么：从 CLIP ViT 倒数第二层直接提取 dense patch-level 特征，无需裁剪
    - 核心思路：计算空间显著性图 $D_{i,j} = \|f_{i,j} - \bar{f}\|_2 / (\frac{1}{HW}\sum_{i,j}\|f_{i,j}-\bar{f}\|_2 + \epsilon)$，对纹理丰富的 patch 赋予更高权重，抑制均匀背景
    - 设计动机：ViT 的 intermediate tokens 保持较强的语义-文本对齐（与 CNN 不同），直接用它们做 mask-aligned 聚合可兼顾全局上下文和实例隔离
    - 与裁剪方法的区别：裁剪造成 domain shift + 特征 bleeding（邻近实例污染），DISC 完全避免

2. **增量视角质量融合**:
    - 做什么：跨帧更新实例的 CLIP 特征时，选择最佳观测而非平均
    - 质量评分：$Q = S_{geo} \cdot S_{sem} \cdot S_{dist}$
     - $S_{geo} = S_{size} \cdot S_{angle}$：物理观测质量（面积占比 + 法线朝向）
     - $S_{sem}$：语义门控（局部-全局特征余弦相似度，滤除语义不一致的片段）
     - $S_{dist} = 0.5 + 0.5 \cdot \bar{D}_{mask}$：空间显著性置信度
   - 当两个实例融合时，保留 $Q$ 更高的特征，避免质量稀释

3. **全 GPU 体素级在线精炼**:
    - 做什么：取消离线精炼步骤，每帧实时合并过分割实例
    - 核心思路：用 BVH（Bounding Volume Hierarchy）快速碰撞检测找 active 候选集 → 精确计算体素交集 → 满足几何重叠 + DINO 视觉相似度阈值时合并
    - 设计动机：AABB heuristic 粗糙且需要定期离线修复；体素交集精确度高且 GPU 实现后开销可控
    - 最终仅需轻量级后处理：合并残余碎片 + 过滤小于阈值的噪声实例

### 损失函数 / 训练策略

无训练、zero-shot 方法。使用 OpenCLIP ViT-L/14 (LAION-2B) + DINOv2-ViTS14-reg。

## 实验关键数据

### 主实验

3D 开放集语义分割（Replica / ScanNet）：

| 方法 | Replica mAcc | Replica fmIoU | ScanNet mAcc | ScanNet fmIoU |
|------|-------------|---------------|-------------|---------------|
| ConceptGraphs | 0.36 | 0.15 | 0.52 | 0.29 |
| BBQ | 0.38 | 0.48 | 0.56 | 0.36 |
| CORE-3D | 0.38 | 0.56 | 0.61 | 0.46 |
| **DISC** | **0.47** | 0.54 | **0.71** | **0.49** |
| OpenFusion (有监督) | 0.41 | 0.58 | 0.67 | 0.64 |

HM3DSEM 目标级检索（$AUC_{top-k}$）：DISC 在 Acc@5 (+3.79%) 和 Acc@10 (+13.63%) 上显著超越 HOV-SG。

### 消融实验

不同 CLIP backbone 对比（HM3DSEM val split）：

| 方法 | Backbone | fmIoU | Acc@5 | Acc@10 |
|------|----------|-------|-------|--------|
| Patch 特征 | ViT-L/14 | **0.45** | 21.96 | **33.87** |
| Crop 特征 | ViT-L/14 | 0.39 | 16.84 | 25.15 |
| Patch 特征 | ConvNeXt-L | 0.17 | 13.06 | 18.93 |
| Crop 特征 | EVA02-L/14 | 0.46 | 20.25 | 29.37 |

### 关键发现

- **Patch > Crop 对 ViT 架构**：ViT-L/14 的 patch 提取在 fmIoU 上从 0.39 提升到 0.45，证明避免裁剪确实有效
- **CNN 架构不适合 patch 提取**：ConvNeXt-L 的 patch 提取 fmIoU 仅 0.17（vs crop 0.40），因为 CNN 中间特征未对齐文本空间
- **大规模建图性能稳定**：在 HM3DSEM 全数据集（181 个场景）上 $AUC_{top-k}$ 保持 0.84，FPS 随实例数增长保持近似恒定

## 亮点与洞察

- **"不裁剪"的 patch 特征提取**：利用 ViT 中间层 token 本身对齐文本空间的特性，一次前传得到所有实例的特征——速度快且保留全局上下文。这一思路可推广到任何需要区域级 CLIP 特征的场景（如 referring segmentation、visual grounding）
- **体素级在线精炼**：用精确几何代替粗糙 heuristic，且 GPU 实现后不增加显著开销——证明"精确方法可以比近似方法更快"

## 局限性 / 可改进方向

- **依赖 2D 分割质量**：FastSAM 的欠分割或遮挡漏检会直接传播到 3D 建图
- **ViT patch 尺寸限制**：14×14 像素的 patch 粒度对极小/极细物体（电缆、细杆）建模不足
- **静态场景假设**：当前体素整合机制假设环境基本静态

## 相关工作与启发

- **vs ConceptGraphs**: ConceptGraphs 也做实例级建图但靠裁剪+离线精炼，DISC 实现了实时在线
- **vs BBQ**: BBQ 用 DINOv2 做实例追踪+离线 CLIP 提取，DISC 统一在线完成
- **vs MaskCLIP**: MaskCLIP 启发了 dense patch 特征思路，DISC 在此基础上加入显著性加权和视角质量融合

## 评分

- 新颖性: ⭐⭐⭐⭐ 单次前传 patch 特征 + 全 GPU 体素精炼的组合新颖且实用
- 实验充分度: ⭐⭐⭐⭐⭐ Replica/ScanNet 标准基准 + 自建大规模 HM3DSEM 基准 + backbone 消融
- 写作质量: ⭐⭐⭐⭐ 系统描述清楚，公式完整
- 价值: ⭐⭐⭐⭐ 对机器人实时语义建图和具身智能有直接应用价值
