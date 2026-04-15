# SOT-GLP: Local-Global Prompt Learning via Sparse Optimal Transport

**日期**: 2026-03-09  
**arXiv**: [2603.08347](https://arxiv.org/abs/2603.08347)  
**代码**: [GitHub](https://github.com/Deniz2304988/SOT-GLP)  
**领域**: 多模态/VLM  
**关键词**: prompt learning, optimal transport, CLIP, few-shot classification, OOD detection

## 一句话总结
提出 SOT-GLP——用稀疏最优传输将显著 patch 均衡分配给各类别专属 local prompt，结合全局 prompt 保持整体对齐，在 11 个 benchmark 16-shot 上达到 85.1% 平均精度，并发现无投影版本在 OOD 检测上达 94.2% AUC 的 SOTA。

## 研究背景与动机

1. **领域现状**: CLIP 的 prompt learning（CoOp/CoCoOp/MaPLe 等）通过学习文本 prompt 做少样本适应，主流做法将全局 [CLS] embedding 与文本匹配，丢失了细粒度局部特征。

2. **现有痛点**: (a) 全局匹配平均了所有空间区域，对纹理/部件等细粒度线索不敏感；(b) 引入局部匹配的方法（PLOT/GalLoP）对每个 prompt 独立做 top-K patch 选择，导致多个 prompt 关注重叠区域，prompt 冗余和塌缩。

3. **核心矛盾**: 需要多个 prompt 专注不同视觉证据，但独立选择会导致重叠。

4. **切入角度**: 共享一个显著 patch 集合，用最优传输的均衡约束强制不同 prompt 分配到不同 patch——"soft partition"而非独立选择。

## 方法详解

### 整体框架
双分支架构：**全局分支**（标准 CLIP Q-K attention [CLS] token + 全局 prompt → 交叉熵损失）+ **局部分支**（V-V attention patch token → saliency 筛选 top-K → 稀疏 OT 分配到类别专属 local prompt → OT 加权相似度损失）。最终分类 = 全局 + $\lambda \cdot$ 局部。

### 关键设计

1. **双流视觉编码器**:
    - 原始 CLIP 流（Q-K attention）产生全局 [CLS] embedding $Z_{\text{global}}$
    - 并行 V-V attention 流产生局部 patch features $Z_{\text{local}}$
    - V-V attention：$A^{vv} = \text{softmax}(VV^\top / \sqrt{d})$，直接关联 value 表示，增强 patch-to-patch 交互
    - 设计动机：V-V attention 已在 CLIP Surgery 中被证明能增强局部判别性

2. **Saliency-Guided Sparsification**:
    - 对每个类 $c$，计算每个 patch 与该类所有 local prompt 的平均相似度作为显著性分数
    - 取 top-K 个显著 patch 构成共享稀疏支撑集 $\mathcal{S}_c^{(i)}$
    - 设计动机：过滤背景噪声，确保后续 OT 只在前景区域上操作

3. **Balanced Entropic Optimal Transport**:
    - 在稀疏 patch 集合和 local prompt 之间建立 OT 问题
    - 代价矩阵 $C_{uv} = 1 - s_u^\top t_v$，均匀边际约束 $\mathbf{a} = \frac{1}{K}\mathbf{1}_K$，$\mathbf{b} = \frac{1}{N_\ell}\mathbf{1}_{N_\ell}$
    - 用 Sinkhorn 迭代可微求解，得到传输矩阵 $\mathbf{T}$
    - 设计动机：均衡边际约束防止 prompt 塌缩——每个 prompt 收到可比的分配质量，不同 prompt 自然专注不同 patch

4. **Accuracy-Robustness Trade-off 发现**:
    - 带可学习投影的版本：few-shot 精度最高（+0.9%），但改变了 CLIP 原始特征流形
    - 无投影版本：保持 CLIP 原生几何结构，OOD 检测性能 SOTA（23.8 FPR95 / 94.2 AUC）
    - 这是一个有趣且实用的 trade-off 发现

### 训练策略
- 冻结 CLIP 视觉和文本编码器，只训练 prompt 参数
- $\mathcal{L} = \mathcal{L}_{\text{global}} + \lambda \mathcal{L}_{\text{local}}$
- 全局 prompt dropout 防止冗余
- SGD，lr=0.05，cosine annealing 50 epochs

## 实验关键数据

### 主实验（11 个数据集，16-shot，ViT-B/16）

| 方法 | 平均 Acc | ImageNet | Cars | DTD |
|------|---------|----------|------|-----|
| CoOp | 82.7 | 75.6 | 73.1 | 72.4 |
| MaPLe | 83.5 | 76.1 | 75.2 | 73.8 |
| GalLoP | 84.3 | 76.8 | 76.1 | 74.5 |
| **SOT-GLP** | **85.1** | **77.3** | **77.5** | **75.9** |

### OOD 检测

| 方法 | FPR95 ↓ | AUC ↑ |
|------|---------|-------|
| GL-MCM | 28.5 | 92.1 |
| GalLoP | 26.2 | 93.0 |
| **SOT-GLP (无投影)** | **23.8** | **94.2** |

### 消融实验

| 配置 | 平均 Acc |
|------|---------|
| 仅全局分支 | 82.9 |
| + 独立 top-K（无 OT） | 83.8 |
| + OT（无 sparsification） | 84.2 |
| + Sparse OT（完整） | **85.1** |

### 关键发现
- OT 分配比独立 top-K 提升 +1.3%，验证了均衡分配防止 prompt 重叠的有效性
- Sparsification 贡献 +0.9%，过滤背景确实改善了 OT 质量
- 无投影版本在 OOD 检测上大幅领先，揭示了 accuracy-robustness trade-off

## 亮点与洞察
- **OT 做 patch-prompt 分配**: 优雅地解决了多 prompt 重叠问题，均衡约束是核心
- **V-V attention 作为专用局部特征流**: 首次将 CLIP Surgery 的 V-V attention 用于 prompt learning
- **Accuracy-Robustness trade-off**: 实用发现——需要 OOD 鲁棒性时去掉投影层

## 局限性 / 可改进方向
- Sinkhorn 迭代增加了训练计算开销
- Top-K 值固定为 10，可能对不同分辨率/数据集不够自适应
- 仅在 ViT-B/16 上实验，更大 backbone 效果未知
- OT 的正则化系数 $\epsilon$ 对性能有影响但未深入分析

## 相关工作与启发
- **vs GalLoP**: 独立 top-K 导致重叠，SOT-GLP 用共享 top-K + OT 显式分区
- **vs PLOT**: PLOT 做 dense OT（全部 patch），计算昂贵且背景干扰大；SOT-GLP 先 sparsify 再 OT
- **vs CoOp/CoCoOp**: 仅全局匹配，缺少局部精细对齐

## 评分
- 新颖性: ⭐⭐⭐⭐ 稀疏 OT + V-V attention 的组合设计有创新
- 实验充分度: ⭐⭐⭐⭐ 11 个数据集 + OOD 检测 + 消融
- 写作质量: ⭐⭐⭐⭐ 公式推导清晰，动机阐述到位
- 价值: ⭐⭐⭐⭐ Prompt learning 领域的有效改进
