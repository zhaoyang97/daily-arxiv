# DepthArb: Training-Free Depth-Arbitrated Generation for Occlusion-Robust Image Synthesis

**日期**: 2026-03-25  
**arXiv**: [2603.23924](https://arxiv.org/abs/2603.23924)  
**代码**: 无  
**领域**: 图像生成 / 扩散模型 / 空间可控生成  
**关键词**: occlusion, depth ordering, attention arbitration, training-free, layout-guided generation

## 一句话总结
提出 DepthArb，一个无需训练的遮挡感知图像生成框架，通过注意力仲裁调制（AAM）抑制背景注意力泄漏 + 空间紧凑性控制（SCC）防止注意力发散，在扩散模型的交叉注意力层中显式解决深度排序冲突，在自建 OcclBench 和 OverLayBench 上显著超越现有方法。

## 研究背景与动机

1. **领域现状**：文本到图像扩散模型在多物体组合生成中，通常依赖 bounding box 或 mask 引导注意力实现空间控制。方法分两类：梯度优化型（BoxDiff 等）和区域融合型（Zero-Painter 等）。

2. **现有痛点**：这些方法只关心 2D 平面位置，对深度层级和遮挡关系毫无感知。当多个物体的 bounding box 重叠时，注意力图产生空间干扰——背景物体的注意力"泄漏"到前景区域（attention hijacking），导致三类典型问题：
    - **概念混合（concept mixing）**：重叠区域融合了多个物体的特征
    - **遮挡不合逻辑（illogical occlusion）**：本该被遮挡的物体反而显示在前面
    - **概念丢失（concept missing）**：某个物体完全消失

3. **核心矛盾**：现有方法对所有物体赋予相同显著性（uniform salience），无法在重叠区域做出像素级的归属判决。根本原因是缺乏深度感知的注意力仲裁机制。

4. **切入角度**：将遮挡问题重新定义为"注意力竞争的仲裁问题"——在特征空间中，让前景物体在重叠区域赢得注意力竞争，同时保持背景物体在非遮挡区域的语义完整性。

5. **核心 idea**：通过深度感知的注意力正交约束（AAM）强制前景/背景注意力在重叠区域解耦，通过空间二阶矩约束（SCC）防止注意力发散，全程训练自由，作为即插即用模块增强扩散模型的遮挡生成能力。

## 方法详解

### 整体框架
输入：文本 prompt + 每个物体的 bounding box $\mathbf{B}_i$ + 相对深度 $d_i \in [0,1]$  
输出：正确遮挡关系的合成图像  
Pipeline：在 SDXL 去噪过程的每步，计算三个损失并反向传播梯度更新 latent $\mathbf{z}_t$，分两阶段执行——Stage 1（结构阶段）全约束，Stage 2（纹理阶段）放松正交约束保留自然光影。

### 关键设计

1. **Layout Confinement (LC, 布局约束)**:
    - 做什么：确保每个物体的注意力集中在其 bounding box 内部
    - 核心思路：计算注意力的"对齐比率" $f_i = E_{in}^{(i)} / (E_{in}^{(i)} + E_{out}^{(i)} + \varepsilon)$，然后最小化 $\mathcal{L}_{align} = \sum_i d_i \cdot (1 - f_i)^2$
    - 设计动机：前景物体（$d_i$ 小=离相机近）占更大图像区域，注意力泄漏更显眼，所以用深度加权——越近的物体约束越严格

2. **Attention Arbitration Modulation (AAM, 注意力仲裁调制)**:
    - 做什么：在重叠区域抑制背景物体的注意力，确保前景物体占据支配地位
    - 核心思路：对每个前景-背景对 $(i,j)$，计算背景注意力在前景 mask 内的归一化响应 $\mathcal{I}_{i \leftarrow j}$，最小化深度加权的正交损失 $\mathcal{L}_{ortho} = \sum_{(i,j)} \lambda_{ij} \cdot \mathcal{I}_{i \leftarrow j}$，其中 $\lambda_{ij} = \lambda_0 \cdot \exp(\alpha \frac{d_j - d_i}{\tau})$
    - 设计动机：深度差越大（前景离相机越近、背景越远），正交约束越强。这确保了注意力在特征层面的空间正交性，从根本上消除了注意力泄漏

3. **Spatial Compactness Control (SCC, 空间紧凑性控制)**:
    - 做什么：防止注意力在 bounding box 内部过度扩散，保持物体边界清晰
    - 核心思路：将注意力图归一化为空间概率分布，计算空间二阶矩（方差）$\text{Var}_i = \sum_{x,y} \tilde{\mathbf{A}}_i(x,y) \|\mathbf{p}(x,y) - \boldsymbol{\mu}_i\|_2^2$，最小化 $\mathcal{L}_{compact} = \sum_i d_i \cdot \text{Var}_i$
    - 设计动机：AAM 解决了物体间干扰，但物体自身注意力可能在有效区域内弥散导致模糊。SCC 强制前景物体注意力紧凑集中，而允许背景物体适当松散（通过深度加权实现）

### 训练策略 / 两阶段推理
- **Stage 1（结构阶段）**：$\mathcal{L}_t = \mathcal{L}_{align} + \lambda_{ortho}\mathcal{L}_{ortho} + \lambda_{compact}\mathcal{L}_{compact}$，强制严格空间解耦 + 深度层级
- **Stage 2（纹理阶段）**：去掉 $\mathcal{L}_{ortho}$，只保留 $\mathcal{L}_{align} + \lambda_{compact}\mathcal{L}_{compact}$，允许自然光照交互（软阴影、光线包裹）
- 每步梯度更新：$\mathbf{z}_t \leftarrow \mathbf{z}_t - \eta_t \nabla_{\mathbf{z}_t} \mathcal{L}_t$

## 实验关键数据

### 主实验（OcclBench）

| 方法 | mIoU-all↑ | CLIP Score↑ | FOCR(%)↑ | BOR↑ | FBS↑ |
|------|-----------|-------------|----------|------|------|
| SDXL | 36.73 | 33.44 | 56.20 | 24.42 | 69.7 |
| Layout Guidance | 34.59 | 32.00 | 52.30 | 25.37 | 58.6 |
| R&B | 57.88 | 31.60 | 70.27 | 25.86 | 73.3 |
| LaRender | 41.22 | 31.47 | 61.97 | 25.31 | 74.5 |
| **DepthArb (full)** | **59.93** | **33.27** | **81.84** | **25.96** | **88.5** |

FOCR（前景遮挡覆盖率）从最佳 baseline R&B 的 70.27% 提升到 81.84%（+11.6pp），FBS（前景-背景可分离度）从 74.5 提升到 88.5（+14.0）。

### 消融实验

| 配置 | mIoU-all↑ | FOCR(%)↑ | FBS↑ |
|------|-----------|----------|------|
| **DepthArb (full)** | **59.93** | **81.84** | **88.5** |
| w/o LC | 39.13 | 69.18 | 71.2 |
| w/o AAM | 55.76 | 78.56 | 74.4 |
| w/o SCC | 56.12 | 75.40 | 77.0 |

### 关键发现
- **三个模块缺一不可**：去掉 LC 后 mIoU 暴跌（59.93→39.13），去掉 AAM 后 FBS 严重下降（88.5→74.4，说明概念混合加剧），去掉 SCC 后 FOCR 下降（81.84→75.40，注意力发散影响遮挡精度）
- **AAM 对遮挡质量贡献最大**：FBS 从 74.4（w/o AAM）到 88.5（full），提升 14.1 分，证明注意力正交约束是解决遮挡的关键
- **两阶段策略的必要性**：Stage 2 松弛正交约束允许自然光影生成，避免物体间过度隔离
- 在 OverLayBench 的复杂场景（Complex subset）中也保持 SOTA，证明方法在密集重叠下鲁棒

## 亮点与洞察
- **将遮挡建模为注意力仲裁问题**：这个视角非常精准——扩散模型中的空间关系确实由 cross-attention 决定，直接在注意力层面做深度排序比后处理更本质。这个思路可以迁移到视频生成中处理动态遮挡
- **深度加权的正交约束**：$\lambda_{ij}$ 的设计让遮挡约束自动适应深度差异，前景越近、背景越远时约束越强，深度接近时允许自然过渡，很优雅
- **OcclBench benchmark**：填补了遮挡评估的空白，FOCR/BOR/FBS 三个指标分别评估深度排序、被遮挡物完整性、前景-背景可分性，设计系统

## 局限性 / 可改进方向
- 仍基于 bounding box + 离散深度值输入，无法处理连续深度或非矩形遮挡
- 训练自由方法依赖逐步梯度更新，推理速度比不引导的生成慢
- 只在 SDXL 上验证，未测试 DiT 架构（如 SD3/FLUX），后者用 joint attention 替代了 cross-attention，AAM 能否直接适配是个问题
- 仅处理静态图像的遮挡，未扩展到视频生成中的时间一致性遮挡

## 相关工作与启发
- **vs LaRender**: LaRender 用 latent rendering 做遮挡，本质是刚性层分离，损失了全局光照一致性；DepthArb 在注意力层面做软约束，FBS 大幅领先（88.5 vs 74.5）
- **vs R&B**: R&B 做到了较好的空间对齐（mIoU 57.88），但遮挡能力不足（FOCR 70.27 vs 81.84），缺乏深度感知
- **vs adapter 方法（T2I-Adapter, ControlNet）**: 这些需要像素级深度图作为条件，灵活性差；DepthArb 只需要粗粒度的相对深度 $d_i$，对用户更友好

## 评分
- 新颖性: ⭐⭐⭐⭐ 把遮挡重构为注意力仲裁问题，AAM+SCC 设计有理论基础
- 实验充分度: ⭐⭐⭐⭐ OcclBench 自建 benchmark + OverLayBench + 完整消融
- 写作质量: ⭐⭐⭐⭐ 问题定义清晰，公式推导严谨，可视化丰富
- 价值: ⭐⭐⭐⭐ 即插即用、训练自由，解决了实际痛点，benchmark 有独立价值
