# History-Conditioned Spatio-Temporal Visual Token Pruning for Efficient VLN

**日期**: 2026-03-06  
**arXiv**: [2603.06480](https://arxiv.org/abs/2603.06480)  
**代码**: 无  
**领域**: 机器人  
**关键词**: vision-language navigation, token pruning, VLA efficiency, spatio-temporal compression, training-free

## 一句话总结
提出面向视觉语言导航（VLN）的无训练时空 token 剪枝框架——通过 Adaptive MMR 对当前帧做空间 token 选择、Query-Guided Re-weighting 对历史帧做时空压缩，在 90% 剪枝率下仍保持优于所有基线的导航性能，并在真实四足机器人上部署验证。

## 研究背景与动机

1. **领域现状**：VLA 模型（如 StreamVLN、NaVILA）在视觉语言导航中表现优异，但 transformer-based 架构计算量大，视觉 token 主导输入长度和计算成本，导致实时部署困难。

2. **现有痛点**：(a) 现有 token 剪枝方法（SparseVLM、DivPrune、VisPruner）基于单帧设计，未考虑 VLN 特有的时空结构；(b) VLN 需要历史观测来做长 horizon 决策，但历史帧中存在大量与当前无关的冗余信息；(c) 高压缩比下性能急剧下降。

3. **核心矛盾**：VLN 需要利用历史记忆做长程推理，但历史帧的 token 量随时间线性增长带来计算瓶颈。简单剪枝丢弃了对导航有价值的信息。

4. **切入角度**：当前帧和历史帧应该区别对待——当前帧保持空间覆盖，历史帧只保留与当前相关的信息。

5. **核心 idea**：对当前帧用 Adaptive MMR 平衡 saliency 和 diversity 选 token，对历史帧用当前帧 query 做 relevance reweighting 后再做 A-MMR 压缩。

## 方法详解

### 整体框架
所有帧（历史+当前）→ Vision encoder 提取 token 特征 → [CLS] token 与 patch token 的余弦相似度作为 $I_{base}$ → 当前帧 A-MMR 选择 → 选中 token 作为 Query → 历史帧 Query-Guided Re-weighting + A-MMR → 合并 token → Projector + LLM → 导航动作预测。

### 关键设计

1. **Adaptive Maximal Marginal Relevance (A-MMR)**:
    - 做什么：迭代选择兼顾重要性和多样性的 token 子集
    - 核心思路：$i^* = \arg\max_{i \in \mathcal{U}} \big(I_{base}^{(i)} \cdot (1 - \max_{j \in \mathcal{S}} \text{sim}(\mathbf{f}_i, \mathbf{f}_j))\big)$
    - 设计动机：纯 importance-based 选择会保留很多相似 token（冗余）；纯 diversity-based 选择可能保留不重要的 token。A-MMR 通过乘法组合自动平衡——先选高 attention 目标物体，再逐步扩展到语义不同的背景区域

2. **Query-Guided Re-weighting**:
    - 做什么：用当前帧选中的 token 作为 query，重新评估历史 token 的重要性
    - 核心思路：时空相关性 $R^{(i)} = \max_{k \in \mathcal{Q}} \text{sim}(\mathbf{f}_{hist}^{(i)}, \mathbf{f}_{curr}^{(k)})$，最终重要性 $I_{final}^{(i)} = I_{base}^{(i)} \cdot (\alpha + (1-\alpha) \cdot R^{(i)})$，α=0.5
    - 设计动机：历史帧中与当前视野相关的信息更重要（如导航目标在历史帧中出现过）。不相关的历史信息可以安全丢弃

### 训练策略
完全无训练——即插即用应用于预训练 VLA 模型，不修改参数避免分布偏移。

## 实验关键数据

### 主实验（VLN benchmark，90% 剪枝）

| 方法 | R2R SR↑ | R2R SPL↑ | RxR SR↑ | RxR SPL↑ |
|------|:---:|:---:|:---:|:---:|
| 无剪枝 | 55.74 | 49.66 | 56.53 | 47.26 |
| SparseVLM | 34.91 | 31.08 | 23.17 | 20.87 |
| DivPrune | 27.57 | 18.55 | 23.22 | 14.56 |
| VisPruner | 41.16 | 29.27 | 37.34 | 25.34 |
| **Ours** | **47.63** | **36.36** | **45.71** | **32.91** |

### 消融实验

| 配置 | R2R SPL (90%) |
|------|:---:|
| 纯 importance (无 diversity) | 较低 |
| 纯 diversity (无 importance) | 较低 |
| A-MMR (当前帧) | 提升 |
| + Query-Guided (历史帧) | **36.36** |

### 关键发现
- 90% 剪枝率下，本方法 R2R SPL 36.36 vs VisPruner 29.27（+7.09），RxR SPL 32.91 vs VisPruner 25.34（+7.57）
- 即使在 70% 剪枝率下，本方法也是唯一接近无剪枝性能的方法（SPL 47.28 vs 49.66）
- 延迟从 231.34ms 降至 213.40ms（90% 剪枝），比其他方法更快
- 真实世界 Unitree Go2 四足机器人部署验证了实际可行性

## 亮点与洞察
- **当前帧与历史帧的差异化处理思路值得推广**：VLN 不是唯一需要历史记忆的任务——视频理解、对话式 VQA 等都面临类似的时空冗余问题
- **A-MMR 的 importance × distinctness 乘法公式简洁有效**：比硬编码分割（VisPruner）和纯多样性优化（DivPrune）都更灵活
- **无训练即插即用**：保持了预训练模型的泛化能力，对实际机器人部署非常友好

## 局限性 / 可改进方向
- 仅在 StreamVLN 一个 VLA 模型上验证，泛化到其他 VLA 未知
- 延迟减少不大（231→213ms），90% 的 token 剪枝只带来 ~8% 的延迟减少——瓶颈可能不只在 token 数量
- α=0.5 固定不变，可能需要根据环境复杂度自适应调整
- RxR 多语言场景下只报告了英语结果

## 相关工作与启发
- **vs SparseVLM**: 纯 text-guided 重要性，高压缩率下冗余严重（同类 token 过多）
- **vs VisPruner**: 硬编码分割策略缺乏灵活性，A-MMR 的统一公式更优雅
- **vs DivPrune**: 纯多样性优化忽略了重要性，导致保留不重要但多样的 token

## 评分
- 新颖性: ⭐⭐⭐⭐ 首次将时空压缩概念引入 VLN token 剪枝，A-MMR 设计合理
- 实验充分度: ⭐⭐⭐⭐ 两个 benchmark + 三种剪枝率 + 真实机器人部署
- 写作质量: ⭐⭐⭐⭐ 框架清晰，公式推导简洁
- 价值: ⭐⭐⭐⭐ 对 VLA 实时部署有直接工程价值
