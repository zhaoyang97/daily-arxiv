# Multi-label Instance-level Generalised Visual Grounding in Agriculture

**日期**: 2026-03-05  
**arXiv**: [2603.06699](https://arxiv.org/abs/2603.06699)  
**代码**: 无（暂未公开）  
**领域**: 多模态/VLM  
**关键词**: precision agriculture, visual grounding, crop-weed detection, multi-label, hierarchical relevance

## 一句话总结

构建 gRef-CW 农业视觉定位数据集（8034 图/82K 标注）和 Weed-VG 框架，通过层级相关性评分（全局存在性检测 + 实例级相关性排序）和 IoU 驱动插值回归，实现 Top-1 精度 62.42%，远超 GroundingDINO（20.38%）。

## 研究背景与动机

1. **领域现状**：精准农业需要从田间图像中检测和区分作物/杂草实例，现有方法多采用检测框架但缺乏自然语言理解能力。
2. **现有痛点**：(1) 缺乏农业场景的视觉定位数据集；(2) 通用视觉定位模型对密集小目标和领域术语表现差，GroundingDINO 的负例准确率仅 7.52%；(3) 农业场景目标尺度极端变化（占图像面积 0.01%-0.97%），通用模型无法处理。
3. **核心矛盾**：需要多标签实例级精细定位（区分不同植物种类+判断是否存在），同时处理高密度场景（>30 实例/图）和极端尺度差异。
4. **切入角度**：构建专门的 gRef-CW 数据集 + Weed-VG 框架，用层级化评分分解"是否存在"和"哪个实例"两个子问题。

## 方法详解

### 整体框架

Weed-VG 基于 GroundingDINO 扩展，分为三阶段：(1) 提案生成——Swin Transformer + BERT 生成候选区域；(2) 层级相关性评分——L0 判断目标是否存在 + L1 对实例做相关性排序；(3) IoU 驱动插值回归——解决极端尺度变化下的定位精度。

### 关键设计

1. **层级相关性评分（HRS）**：
   - **L0 全局存在性检测**：先判断查询描述的目标是否在图像中存在。池化所有提案分数 $s_{\text{pool}}(k) = \max_j s(v_j, t_k)$，softmax 归一化后做二分类
   - **L1 实例相关性排序**：结合句子级和词级相似度做对比评分 $S_{\text{ref}} = w_s \cdot S_{\text{sent}} + (1-w_s) \cdot \text{MaxPool}(S_{\text{word}})$
   - **层级约束**：$L_{\text{lvl1}}^{\text{constrained}} = \max(L_{\text{lvl1}}, L_{\text{lvl0}})$
   - 设计动机：通用模型对不相关查询几乎不拒绝（Neg-Acc 7.52%），两级分解让模型先学会"说不"

2. **IoU 驱动插值回归（InterpIoU）**：
   - 构建插值框 $B_{\text{int}} = (1-\alpha)B_{\text{pred}} + \alpha B_{\text{gt}}$，$\alpha=0.99$
   - 联合损失 $L_{\text{InterpIoU}} = L_{\text{IoU}}(B_{\text{pred}}, B_{\text{gt}}) + L_{\text{IoU}}(B_{\text{int}}, B_{\text{gt}})$
   - 对微小目标，标准 IoU 损失梯度极小难以优化；插值框提供了更陡峭的梯度信号

3. **距离和尺度感知匹配**：
   - 匹配代价 $C_{ij} = (1-\text{IoU}) + \lambda_\text{centre}\|\mathbf{c}(P)-\mathbf{c}(G)\|^2 + \lambda_\text{size}(\frac{|w_P-w_G|}{w_G}+\frac{|h_P-h_G|}{h_G})$

### 损失函数 / 训练策略

两阶段训练：Stage 1（100 epoch）微调最后解码层+框回归头用 InterpIoU；Stage 2（60 epoch）训练投影/注意力层和 HRS。AdamW + cosine annealing，lr=2e-4，batch=4。A100 GPU。

## 实验关键数据

### 主实验（gRef-CW 测试集）

| 方法 | Top-1↑ | R@0.5↑ | mIoU↑ | Neg-Acc↑ |
|------|--------|--------|-------|---------|
| MDETR | 10.16 | 7.78 | 54.19 | 3.32 |
| GroundingDINO-L | 20.38 | 28.73 | 23.68 | 7.52 |
| SAM3 | 34.88 | 46.65 | 32.76 | 25.53 |
| **Weed-VG** | **62.42** | **55.44** | **57.25** | **78.35** |

### 消融实验

| 配置 | Top-1 | mIoU | Neg-Acc |
|------|-------|------|---------|
| Full Weed-VG | 62.42 | 57.25 | 78.35 |
| w/o 查询投影 | 33.20 | — | — |
| w/o InterpIoU | 49.15 | 47.72 | — |
| 仅句子级 | 49.29 | 49.35 | — |
| w/o 层级约束 | 59.87 | — | 41.60 |

### 关键发现
- Weed-VG 比 GroundingDINO 高 3 倍精度（62.42% vs 20.38%），Neg-Acc 差 10 倍
- 尺度鲁棒性：tiny→large 差距仅 17 点（SAM3 为 58 点）
- 查询投影去除后 Top-1 暴跌 29 点，是最关键组件
- 层级约束对 Neg-Acc 贡献最大（去除后 -36.75 点）

## 亮点与洞察
- **层级分解的负例拒绝**：两级评分使 Neg-Acc 从 7.52% 跃升到 78.35%——"学会说不"比"学会说是"更难更重要
- **InterpIoU 回归**：用插值框为微小目标提供有效梯度，可迁移到其他小目标检测任务

## 局限性 / 可改进方向
- gRef-CW 数据集地理和气候多样性有限
- 实时性评估缺失（田间部署需要低延迟）
- 仅覆盖特定作物类型

## 评分
- 新颖性: ⭐⭐⭐⭐ 层级评分和 InterpIoU 设计有创新
- 实验充分度: ⭐⭐⭐⭐⭐ 多尺度、密度分析、详尽消融
- 写作质量: ⭐⭐⭐⭐ 结构清晰
- 价值: ⭐⭐⭐⭐ 对精准农业有直接应用价值
