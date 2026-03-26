# AgenticGEO: A Self-Evolving Agentic System for Generative Engine Optimization

**日期**: 2026-03-02  
**arXiv**: [2603.20213](https://arxiv.org/abs/2603.20213)  
**代码**: [https://github.com/AIcling/agentic_geo](https://github.com/AIcling/agentic_geo)  
**领域**: llm_agent  
**关键词**: Generative Engine Optimization, self-evolving agent, MAP-Elites, co-evolution, quality-diversity

## 一句话总结
AgenticGEO 将生成式搜索引擎优化（GEO）形式化为内容条件化控制问题，通过 MAP-Elites 策略档案和协同进化的 Critic 代理实现自适应的多轮内容重写，在 3 个数据集上以平均 46.4% 的增益超越 14 个基线方法。

## 研究背景与动机
生成式搜索引擎（如 Google AI Overviews、Perplexity AI）正从传统排名检索转向 LLM 合成摘要，这改变了内容优化的目标：不再争夺排名位置，而是争取被纳入生成答案中。**生成式引擎优化（GEO）** 旨在最大化源内容在生成答案中的可见度和引用。

现有方法的核心矛盾：
1. **静态启发式方法**（如添加引用、统计数据）对所有内容"一刀切"，忽略内容异质性
2. **学习型方法**（如 AutoGEO）蒸馏引擎偏好为固定规则，易于过拟合特定引擎行为
3. 作者通过策略敏感性分析（Figure 1）发现：**优化成功率因策略和内容差异极大，现有静态策略池无法优化近一半样本**

两大挑战：(i) 如何设计能灵活适应多样内容和动态引擎行为的进化方法；(ii) 如何在不依赖大量引擎反馈的情况下实现有效优化。

## 方法详解
### 整体框架
AgenticGEO 包含三个阶段：
1. **离线 Critic 对齐**: 用离线偏好数据预热轻量级代理 Critic
2. **在线策略-Critic 协同进化**: 通过进化循环联合训练 MAP-Elites 策略档案和 Critic
3. **推理时多轮重写**: Critic 引导的贪心搜索选择策略、执行多步内容优化

### 关键设计

**1. MAP-Elites 质量多样性策略档案**
- 不同于标准 top-k 列表，策略按行为维度（语调、格式、约束强度、推理步骤等 12 个离散维度）组织到多维网格中
- 策略准入需通过双门控：**价值门**（得分超过当前精英）和**新颖性门**（n-gram Jaccard 相似度 < 0.9）
- 每个策略的复合 PND 分数：S_PND(s) = r(s) + λ_pnd · (Nov(s) + Div(s))

**2. 离线 Critic 偏好对齐**
- Critic 架构：Qwen2.5-1.5B 骨干 + 两层 MLP 值头
- 混合目标函数：L_total = L_pair + λ · L_reg
  - 回归损失：Huber(C(x,s), r_sup(x,s)) 校准绝对值
  - 加权对比损失：强调 Top-5 策略的精细排序
- 分阶段训练：先冻结骨干预热值头，再联合微调

**3. 在线协同进化循环（4 阶段/轮）**
- **生成**: 从档案采样父代策略，Evolver (Qwen2.5-7B) 选择变异算子（字段级扰动、交叉）生成子代
- **筛选**: Critic 过滤，选 Top-K_top 开发 + K_rand 探索
- **评估**: 生成引擎评估选中候选，合并 Critic 分数更新档案
- **学习**: 用 Sibling-Aware AWR 更新 Evolver，用 GE 标注数据校准 Critic

**4. Sibling-Aware AWR 优势函数**
A_i = (r_i - r_parent) - α_sib · mean({Δ_j}_{siblings}) + I(Δ_i < 0) · S_PND(s_i)
- 同胞均值提供组内基线，消除内容固有难度的影响
- 负增益时添加探索奖励，保留新颖策略

### 损失函数 / 训练策略
- Evolver 损失：L_Evolver = -E[exp(A(x,s)/β) · log E(s|x)]（加权 SFT）
- Critic 在线校准：使用新收集的 GE 标注三元组 (x,s,r) 优化混合目标
- 理论保证：累积遗憾 O(√T)，平均性能差距渐近收敛至 0

## 实验关键数据
### 主实验

**In-Domain (GEO-Bench) 结果**:

| 方法 | Qwen2.5-32B (word/pos/overall) | Llama3.3-70B (word/pos/overall) |
|------|------|------|
| No optimization | 20.05/20.26/20.21 | 19.19/19.33/19.20 |
| Keyword Stuffing | 20.73/20.86/20.69 | 19.99/20.16/20.02 |
| AutoGEO | 23.51/23.70/23.71 | 22.77/22.65/22.78 |
| Quotation Addition-SFT | 24.10/24.28/23.92 | 22.31/22.45/22.20 |
| **AgenticGEO** | **25.42/25.85/25.48** | **24.38/24.59/24.52** |
| **增益** | **+26.78%** | **+27.71%** |

**Cross-Domain (MS MARCO) 结果**: AgenticGEO 在 Qwen 引擎上 Overall 34.10 vs AutoGEO 30.67（+11%+）

**Cross-Domain (E-Commerce) 结果**: AgenticGEO Overall 26.58 vs 最佳基线 21.83（+21.7%）

### 消融实验
- 移除进化策略档案(b)造成最大性能下降，确认长期策略积累是增益主要驱动力
- 离线 Critic 不足以替代在线协同进化(a)
- 随机规划替代 Critic 引导(c)导致性能下降
- 仅性能维护档案(d)降低泛化能力

**超参数敏感性**:
- 多轮重写：3 轮最优（overall 25.48），更多轮次增益有限
- 档案大小：25-35 策略最优，峰值在 35

**Critic 作为 GE 代理的效率**:
- 仅 700 次 GE 反馈（41.2% 监督量）即可达到 25.12 overall，保留 98.1% 的最佳性能（25.60）

### 关键发现
- 跨引擎鲁棒性强：从 Qwen2.5-32B 到 Llama3.3-70B 性能稳定
- 跨域转移能力显著：在未见过的 MS MARCO 和 E-Commerce 上仍大幅超越基线
- 语义一致性好：BERTScore-F1 维持较高水平，不依赖激进重写

## 亮点与洞察
1. **问题形式化精巧**: 将 GEO 形式化为内容条件化控制问题，而非简单的提示优化
2. **MAP-Elites 档案设计**: 通过质量-多样性平衡避免策略塌缩，每个行为单元格内独立竞争
3. **协同进化思想**: 策略档案和 Critic 互相促进——策略多样性提升 Critic 泛化，Critic 改善引导策略进化
4. **Sibling-Aware AWR**: 巧妙的组内基线消除内容难度差异，比全局优势更稳定
5. **理论分析**: 提供了 O(√T) 遗憾界的正式证明

## 局限性 / 可改进方向
1. Critic 基于 Qwen2.5-1.5B，对长文档和复杂查询的理解可能有限
2. 进化循环的计算成本较高（100 轮在线迭代），实际部署需考虑成本
3. 依赖 CLIP 相似度阈值等超参数的手工选择
4. 仅评估了两个生成引擎，对 GPT-based 搜索引擎的泛化性未知
5. 推理时 greedy 搜索可能陷入局部最优，未探索更强的规划算法（如 MCTS）

## 相关工作与启发
- **从 SEO 到 GEO 的范式转变**: 优化目标从排名位置变为合成答案中的可见度，是搜索生态系统的根本变化
- **自进化代理系统** (Self-Refine, Reflexion, EvoPrompt) 的延续，但引入了内容条件化和协同进化
- MAP-Elites 在游戏 AI、机器人等领域已有应用，本文首次将其用于内容优化策略空间
- Sibling-Aware 优势设计可迁移到其他异质化在线学习场景

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首创将 QD 进化算法与 LLM agent 结合解决 GEO 问题，问题形式化和方法设计均有创意
- 实验充分度: ⭐⭐⭐⭐⭐ 2引擎×3数据集×14基线，消融全面，含理论分析
- 写作质量: ⭐⭐⭐⭐ 方法描述详尽但公式密集，读起来较重
- 价值: ⭐⭐⭐⭐ 对 GEO 新兴方向有重要贡献，但应用场景较窄
