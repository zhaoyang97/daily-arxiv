# ACE-Merging: Data-Free Model Merging with Adaptive Covariance Estimation

**日期**: 2026-03-03  
**arXiv**: [2603.02945](https://arxiv.org/abs/2603.02945)  
**代码**: 无  
**领域**: LLM效率  
**关键词**: 模型合并, 无数据, 协方差估计, 闭式解, 多任务学习

## 一句话总结

ACE-Merging 从理论上证明任务的输入协方差可以从微调权重变化中隐式估计，基于此推导出无数据模型合并的闭式解，并通过自适应归一化和谱精修保证鲁棒性，在 GPT-2 上比现有方法提升 4% 平均准确率。

## 研究背景与动机

1. **领域现状**：预训练+微调范式产生了大量专家模型。模型合并试图把多个专家合为一个多任务模型，避免昂贵的多任务重训练。
2. **现有痛点**：(1) 数据依赖方法（用 Fisher 信息）需要原始训练数据，隐私/可及性受限；(2) 测试时自适应方法引入推理开销，丧失"一次合并、到处部署"的效率；(3) 无数据方法（Task Arithmetic、TIES、DARE）是参数空间启发式，只处理干扰症状而非根因。
3. **核心矛盾**：最优合并需要知道每个任务的输入协方差矩阵 $\Sigma_t$——这正是数据依赖方法的核心变量。无数据方法的根本困难在于：缺少了优化目标中最关键的统计信号。
4. **切入角度**：理论证明 $\Sigma_t$ 与权重变化 $\Delta W_t$ 的协方差成正比（Theorem 1）——微调权重隐含了数据的统计结构。这提供了一座从参数空间回溯到数据空间的桥梁。
5. **核心 idea 一句话**：从微调权重变化估计输入协方差，推导出无数据合并的闭式解，用自适应归一化和谱精修保证鲁棒性。

## 方法详解

### 整体框架

三阶段逐层合并：(1) 自适应协方差归一化——平衡任务能量尺度；(2) 集体结构先验——各向异性正则化；(3) 谱精修——修正频谱失衡。最终产生闭式合并权重 $\bar{W}$。

### 关键设计

1. **理论基础：从权重到协方差**：
   - Theorem 1：$\Sigma_t \propto \text{Cov}_{\mathcal{D}_t}[\Delta W_t]$
   - 证明思路：微调更新 $\Delta W_t \approx -2\eta N_t \mathbb{E}[(W_0 x - y)x^\top]$，协方差自然出现
   - 实用估计器：把 $\Delta W_t$ 的行视为独立样本，计算经验协方差 $\hat{\Sigma}_t \propto (\Delta W_t - \mathbf{1}\mu_t^\top)^\top (\Delta W_t - \mathbf{1}\mu_t^\top)$
   - 统一框架：Weight Averaging 等价于 $\hat{\Sigma}_t = kI$，WUDI-Merging 等价于范数加权的外积估计

2. **自适应协方差归一化**：
   - 异质性指标 $\gamma = \text{Var}_t[\log\|\Delta W_t\|_F^2] / (\mathbb{E}_t[\log\|\Delta W_t\|_F^2])^2$
   - $\gamma > \tau$ 时触发归一化：$\hat{\Sigma}_{t,\text{scaled}} = \hat{\Sigma}_t / \text{Tr}(\hat{\Sigma}_t)$
   - Tikhonov 正则化：$\hat{\Sigma}_{t,\text{reg}} = \hat{\Sigma}_{t,\text{scaled}} + \frac{\epsilon}{\text{Tr}(\hat{\Sigma}_t)} I$
   - 设计动机：不同架构的异质性差异巨大（ViT-B/16 的 γ<0.25，RoBERTa 的 γ>0.3）

3. **集体结构先验（CSP）**：
   - $\mathbf{C}_{\text{agg}} = \mathbf{1}(\frac{1}{d_\text{in}} \mathbf{1}^\top \sum_t \hat{\Sigma}_{t,\text{scaled}})$
   - 从所有任务的聚合协方差中提取列均值能量分布
   - 各向异性正则化：选择性放大共享重要维度，比 $\epsilon I$ 更有信息量
   - 闭式解：$\bar{W}_\text{pre} = (\sum_t W_t \hat{\Sigma}_{t,\text{reg}})(\sum_t \hat{\Sigma}_{t,\text{reg}} + \mathbf{C}_\text{agg})^{-1}$

4. **谱精修**：
   - 问题：$\bar{W}_\text{pre}$ 频谱极度集中（top 5% 奇异值占 99%+ 能量），条件数 > $8.7 \times 10^5$
   - 但主方向正确（余弦相似度 ≈1）——问题在能量分布而非方向
   - 解决：计算结构残差 $\Delta_\text{res}$，SVD 分解后用均值奇异值替代 top-k：$\Delta W_\text{refine} = \sigma_\text{iso} \mathbf{U}_{:,1:k}\mathbf{V}_{:,1:k}^\top$

## 实验关键数据

### 视觉基准（ViT 三个骨干，8/14/20 任务）

| 方法 | ViT-B/32 8T | ViT-B/16 14T | ViT-L/14 20T |
|------|------------|-------------|-------------|
| Weight Avg | 66.3 | 69.5 | 71.6 |
| Task Arithmetic | 70.8 | 70.5 | 74.0 |
| CART | 84.7 | 84.1 | 87.9 |
| TSV-M | 85.9 | 84.6 | 87.7 |
| **ACE-Merging** | **87.9** | **86.1** | **89.5** |

### 语言基准（GPT-2, GLUE 7 任务）

| 方法 | CoLA | MNLI | MRPC | 平均 |
|------|------|------|------|------|
| Weight Avg | 55.0 | 55.1 | 51.0 | ~56 |
| WUDI-Merging | ~62 | ~68 | ~65 | ~66 |
| **ACE-Merging** | **~66** | **~72** | **~69** | **~70** |

### 关键发现
- 随任务数增加（8→14→20），ACE-Merging 的优势更大——说明协方差估计在高任务干扰下更重要
- 在 ViT-L/14 + 20 任务上，ACE-Merging 甚至超过部分数据依赖方法
- 自适应归一化是关键：RoBERTa（高异质性）需要归一化，ViT（低异质性）可以不需要
- 闭式解比 WUDI-Merging 的迭代优化更稳定且计算效率更高

## 亮点与洞察
- **"权重变化隐含数据协方差"**的理论洞察非常优雅：把无数据合并的根本不可能变成了可行，为后续工作提供了理论基础
- **统一框架的解释力**：Weight Averaging、WUDI-Merging 都是协方差估计的特例，这个视角帮助理解为什么某些方法在某些场景下有效/失效
- **谱精修的设计动机清晰**：先证明方向正确但能量分布失衡，再做谱校正——这种"诊断-治疗"的方法论值得学习

## 局限性 / 可改进方向
- 线性近似 $f(W,x) \approx Wx$ 在深层网络中可能不够准确
- 只在相对小的模型上验证（GPT-2、ViT），大模型（7B+）的效果待验证
- 谱精修的 rank fraction $k_\text{frac}$ 需要调优
- 协方差估计把权重矩阵的行视为独立样本，这个假设在 attention 层中可能不成立

## 相关工作与启发
- **vs Task Arithmetic**：Task Arithmetic 等价于假设 $\Sigma_t = kI$（最粗糙的估计），ACE-Merging 估计完整协方差
- **vs WUDI-Merging**：WUDI-Merging 隐式用了外积估计但需迭代优化，ACE-Merging 有闭式解更稳定
- **vs RegMean**：RegMean 需要实际数据计算协方差，ACE-Merging 从权重估计，完全无数据

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 权重→协方差的理论洞察是开创性的
- 实验充分度: ⭐⭐⭐⭐⭐ 视觉+语言双基准、多骨干、多任务规模
- 写作质量: ⭐⭐⭐⭐⭐ 理论推导清晰，统一框架有解释力
- 价值: ⭐⭐⭐⭐⭐ 为无数据模型合并提供了理论基础和实用方案
