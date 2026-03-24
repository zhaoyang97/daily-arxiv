# A Generalised Exponentiated Gradient Approach to Enhance Fairness in Binary and Multi-class Classification

**日期**: 2026-03-22  
**arXiv**: [2603.21393](https://arxiv.org/abs/2603.21393)  
**代码**: 无  
**领域**: AI安全  
**关键词**: fairness, multi-class classification, exponentiated gradient, bias mitigation, multi-objective optimization

## 一句话总结
提出 Generalised Exponentiated Gradient (GEG) 算法，将经典 Exponentiated Gradient 公平学习框架从二分类推广到多分类——将公平约束建模为线性不等式、通过乘性权重迭代求解 min-max 博弈，在 10 个数据集（7 多分类 + 3 二分类）上公平性提升最高 92%（准确率代价 ≤14%）。

## 研究背景与动机

1. **领域现状**: 机器学习公平性研究过去几年发展迅速，但绝大多数方法专注于二分类（如信用评估的"通过/拒绝"、招聘的"录用/淘汰"）。Agarwal et al. (2018) 的 Exponentiated Gradient (EG) 方法通过将公平约束转化为 cost-sensitive classification 的 reduction，成为二分类公平学习的标准方法之一。

2. **现有痛点**: (a) 原始 EG 算法的约束公式化仅适用于二分类——多分类下公平约束数量组合爆炸（k 个类别 × g 个敏感群体 × 多种公平定义）；(b) 多分类的公平定义本身不够成熟——demographic parity 和 equalized odds 如何自然推广到 k-way 分类？约束数从 $O(g)$ 增长到 $O(kg)$ 甚至 $O(k^2g)$；(c) 现有将二分类方法简单套用（如 one-vs-rest 拆分后分别做公平约束）的策略忽略了类间关联，导致全局公平性无法保证。

3. **核心矛盾**: 多分类公平约束空间的维度远大于二分类，但 Lagrangian 框架的收敛性和计算效率需要约束结构的良好性质。如何在约束数目爆炸的同时保持算法高效可解？

4. **本文要解决什么**: (a) 给出多分类下多种公平定义（demographic parity / equalized odds / predictive parity 等）的线性约束标准化表达；(b) 设计可高效求解的 in-processing 算法，适用于任意 base learner。

5. **切入角度**: 将多分类公平学习形式化为多目标优化中的约束博弈——effectiveness（预测正确性）作为主目标，多个线性公平约束作为约束集合——然后用推广的指数梯度方法迭代求解对偶问题。

6. **核心 idea 一句话**: 将 Agarwal et al. 的 EG reduction 从二分类推广到多分类，统一处理多种公平定义下的约束优化。

## 方法详解

### 整体框架
输入：任意 base learner $h$、训练数据 $(X, Y, A)$（$A$ 为敏感属性）、公平约束集合 $\mathcal{C}$ → GEG 将公平学习转化为 min-max 博弈: $\min_h \max_\lambda \mathcal{L}(h) + \sum_j \lambda_j c_j(h)$ → 内循环: 给定 $\lambda$ 训练 base learner 最小化加权目标；外循环: 指数梯度更新 $\lambda$ → 迭代直到收敛或达到公平-准确率均衡。

### 关键设计

1. **多分类公平约束的线性化**:
   - 做什么：将 demographic parity / equalized odds / predictive parity 等公平定义统一表达为关于分类器预测分布的线性不等式
   - 核心思路：对 k 类问题，demographic parity 要求 $P(\hat{Y}=c | A=a) \approx P(\hat{Y}=c | A=a')$ 对所有类别 $c$ 和群体 $a, a'$ 成立。这可以写成线性约束 $|\mathbb{E}[\mathbf{1}[\hat{Y}=c | A=a]] - \mathbb{E}[\mathbf{1}[\hat{Y}=c | A=a']]| \leq \epsilon$。Equalized odds 类似但条件在 $Y=y$ 上
   - 设计动机：线性约束是 EG 框架高效求解的前提——非线性约束需要更复杂的优化技术。通过将各种公平定义统一到线性框架，GEG 可以用同一套算法处理

2. **Generalised Exponentiated Gradient 迭代**:
   - 做什么：在对偶空间迭代更新 Lagrange 乘子 $\lambda$，指导 base learner 在公平-准确率之间权衡
   - 核心思路：经典 EG 的乘性更新 $\lambda_j^{(t+1)} = \lambda_j^{(t)} \cdot \exp(\eta \cdot c_j(h^{(t)}))$——约束违反越严重（$c_j > 0$），对应 $\lambda_j$ 增长越快，下一轮 base learner 会更重视该约束
   - 与原始 EG 的区别：(a) 约束数量从 $O(g)$ 扩展到 $O(kg)$，需要处理高维 $\lambda$ 的稳定性；(b) 支持同时施加多种公平定义（如同时满足 demographic parity 和 equalized odds）；(c) 步长 $\eta$ 需要适配多分类约束的规模

3. **多目标均衡机制**:
   - 做什么：在 effectiveness 和 fairness 之间寻找合理的 trade-off 点
   - 核心思路：GEG 作为 in-processing 方法，在训练过程中直接将公平约束嵌入优化目标，而非事前（重采样/重加权）或事后（阈值调整）处理。迭代过程自然产生 Pareto 前沿上的解
   - 设计动机：Pre-processing 方法（如重采样）改变数据分布可能损失信息；Post-processing（如校准阈值）与模型训练脱耦，无法利用训练信号。In-processing 直接在优化目标中编码公平性，理论上可达到更优的 Pareto 前沿

### 损失函数 / 训练策略
- 主目标: base learner 的标准分类损失（如交叉熵）
- 约束项: 多个线性公平约束的加权和，权重由 EG 迭代动态调整
- 可搭配任意 base learner（逻辑回归、决策树、神经网络等）——GEG 本身是 meta-algorithm

## 实验关键数据

### 主实验（7 多分类 + 3 二分类数据集）

| 评估维度 | 配置 | GEG 表现 |
|---------|------|---------|
| 数据集 | 7 多分类 + 3 二分类 | 10 个数据集全面覆盖 |
| Baseline | 6 种公平方法 | 一致超越 |
| 效果指标 | 4 种 (Accuracy/Precision/Recall/F1) | 准确率下降 ≤14% |
| 公平指标 | 3 种公平定义 | **公平提升最高 92%** |

### 消融/对比表

| 对比维度 | GEG 优势 | 说明 |
|---------|---------|------|
| vs Pre-processing 方法 | 更优 Pareto 前沿 | 不改变数据分布 |
| vs Post-processing 方法 | 更细粒度的控制 | 训练时端到端优化 |
| vs 二分类 EG 直接套用 | 多分类下更稳健 | 避免 one-vs-rest 拆分的信息损失 |
| 多分类 vs 二分类场景 | 多分类优势更明显 | 现有方法在多分类上退化严重 |

### 关键发现
- **多分类场景是关键差异化**: 现有公平方法在多分类上退化严重（约束空间膨胀），而 GEG 专门为此设计，优势最为明显
- **公平提升 92% 的上界场景**: 可能对应某些 baseline 在多分类+严格公平定义下几乎完全失效的情况，GEG 通过系统化约束处理大幅改善
- **14% 准确率下降是上界**: 在多数数据集/公平定义组合上代价更小，说明公平-准确率 trade-off 并非线性——小幅准确率让步可换取大幅公平改善
- **三种公平定义的难度不同**: 不同公平定义的约束结构差异导致优化难度不同，GEG 统一处理的优势在此体现

## 亮点与洞察
- **填补多分类公平性空白**: 从二分类到多分类不是简单的"推广"，约束空间的组合爆炸是本质挑战。GEG 通过线性化 + 高效 EG 迭代优雅解决
- **In-processing 的理论优势**: 与 pre/post-processing 相比，训练时内嵌公平约束可以达到更优的 Pareto 前沿——这不仅是实验观察，也有理论支持（凸优化对偶理论）
- **Base learner 无关性**: GEG 作为 meta-algorithm 适用于任意分类器，从逻辑回归到深度学习都可以即插即用。这种模块化设计让实际部署更灵活
- **统一多种公平定义**: 不需要为每种公平定义设计不同算法，线性化框架统一处理

## 局限性 / 可改进方向
- **准确率代价上限 14% 在高风险场景难以接受**: 医疗/司法等领域可能需要更精细的 Pareto 控制，让用户指定可接受的准确率下降范围
- **HTML 版本不可用（仅 abs fallback）**: 具体的约束公式化细节、收敛分析和逐数据集结果无法从摘要中获取
- **公平约束的交互效应未讨论**: 同时施加多种公平定义时，约束之间可能冲突（如 demographic parity 与 equalized odds 不always兼容），如何处理冲突未知
- **可扩展性**: 多分类约束数 $O(kg)$ 随类别数线性增长，对于 k>>10 的细粒度分类（如 ImageNet 1000 类）是否仍可行？
- **与深度学习的结合**: 摘要未提及 base learner 包含神经网络的实验，当前实验可能以传统 ML 方法为主

## 相关工作与启发
- **vs Agarwal et al. (2018) EG**: 原始 EG 只处理二分类，本文的核心贡献是推广到多分类。关键区别在于约束空间的扩展和 EG 迭代的稳定性处理
- **vs FairLearn**: 微软的 FairLearn 库实现了 EG 方法，但同样限于二分类。GEG 若能集成到 FairLearn 将有很大实际价值
- **vs Adversarial Debiasing**: 对抗去偏通过 min-max 游戏隐式优化公平性，但更难控制具体的公平定义。GEG 的显式约束方式更透明可控

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个系统化将 EG 推广到多分类公平约束的工作，方向明确
- 实验充分度: ⭐⭐⭐⭐ 10 数据集 × 6 baseline × 4 效果指标 × 3 公平定义，组合全面
- 写作质量: ⭐⭐⭐ 仅有摘要可评估，无法判断方法章节的清晰度
- 价值: ⭐⭐⭐⭐ 多分类公平性是实际应用中的真实需求，填补了方法论空白
