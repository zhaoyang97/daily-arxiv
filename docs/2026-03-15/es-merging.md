# ES-Merging: Biological MLLM Merging via Embedding Space Signals

**日期**: 2026-03-15  
**arXiv**: [2603.14405](https://arxiv.org/abs/2603.14405)  
**代码**: 无  
**领域**: 多模态VLM / 模型压缩  
**关键词**: model merging, MLLM, embedding space, biological, cross-modal

## 一句话总结
提出 ES-Merging，用 embedding space 信号（而非 parameter space 启发式）估计 merging 系数，在 layer-wise 粗粒度和 element-wise 细粒度两个层面融合生物领域的分子/蛋白质/细胞三个 MLLM，在跨模态交互预测任务上超越所有现有 merging 方法甚至超过 task-specific fine-tuned 模型。

## 研究背景与动机

1. **领域现状**: 生物领域已有针对分子（Mol-LLaMA）、蛋白质（Prot2Text-V2）、细胞（Cell-o1）的专用 MLLM，但它们各自只理解单一模态。许多科学问题（如药物-蛋白互作、药物-细胞效应）本质上是跨模态的。

2. **现有痛点**: 联合训练跨模态模型需要昂贵的跨模态数据集构建。Model merging 是一种高效替代，但现有方法（TIES-Merging、EMR-Merging 等）都基于 parameter space 信号（权重大小、符号、方向）启发式分配系数——这些信号是 input-agnostic 的，无法捕捉模态特化的真实语义。

3. **核心矛盾**: Parameter space 信号只是间接代理，不知道每个参数对特定模态的贡献有多大；而理想的 merging 系数应该反映每个参数在处理特定模态输入时的重要性。

4. **切入角度**: 作者观察到，当不同模态 token 通过 base LLM 和 specialized MLLM 时，embedding 分布有显著差异，且差异大小和模态是否匹配高度相关（Fig.2）。这说明 embedding space 包含了模态特化的信息。

5. **核心 idea**: 从 embedding space 的分布变化估计 merging 系数——哪个 MLLM 在哪一层对哪种模态的 embedding 改变最大，就给它更高的权重。

## 方法详解

### 整体框架

设计 probe input（包含各模态 token）→ 分别过 base LLM 和各 MLLM 获取逐层 embedding → 从粗粒度（layer-wise SWD 距离变化）和细粒度（element-wise 梯度）两个层面估计 merging 系数 → 组合为最终系数 → 加权合并 LoRA 参数。

### 关键设计

1. **Probe Input 设计**:
    - 做什么：构造一个包含所有模态 token 的探测输入
    - 核心思路：收集每种模态的样本，用各自 encoder 映射到 embedding space，拼接为 `[text_m1; H_m1; text_m2; H_m2; ...]`
    - 设计动机：要比较 base 和 specialized 模型的 embedding 差异，需要一个统一输入——probe input 让所有模型处理相同的多模态输入，从而公平比较

2. **Layer-wise Global Merging Coefficient**:
    - 做什么：估计每层整体上哪个模型更重要
    - 核心思路：将各模态 token 的 embedding 做 mean pooling 得到粗粒度表示，用 Sliced Wasserstein Distance (SWD) 衡量 base 和 specialized 模型在每层的分布距离。计算**层间增量** $d^l = \text{SWD}^l - \text{SWD}^{l-1}$（哪些层新引入了更多模态特化），Z-score 归一化后 softmax 得到 $\alpha_{m_j}^l$
    - 设计动机：SWD 直接度量分布距离，增量形式捕捉"在哪一层发生了关键特化"，比绝对值更有信息量

3. **Element-wise Local Merging Coefficient**:
    - 做什么：在每层内部，估计每个参数元素的重要性
    - 核心思路：计算 embedding 距离 $r = \|H_\text{base} - H_\text{specialized}\|_F$ 对每个 LoRA 参数的梯度绝对值，累加所有模态和 probe 样本的梯度，归一化后 softmax 得到 $\beta_{m_j}^{l,n}$
    - 设计动机：同一层内不同参数对模态特化的贡献差异很大，fine-grained 系数捕捉这种差异

4. **系数组合**:
    - $\lambda_{m_i}^{l,n} = \frac{\alpha_{m_i}^l \cdot \beta_{m_i}^{l,n}}{\sum_m \alpha_m^l \cdot \beta_m^{l,n}}$
    - 乘积 + 归一化，结合两个粒度的信息

### 训练策略
- 无需额外训练！系数估计是基于 forward pass + gradient 计算的，不需要迭代优化
- 只需少量 probe samples（论文用 K 个）即可估计

## 实验关键数据

### 主实验（跨模态交互预测）

| 方法 | Molecule-Protein Avg Acc | Molecule-Cell Avg Acc |
|------|--------------------------|----------------------|
| Base LLM | 57.5 | 79.3 |
| Best single MLLM | 61.2 | 81.1 |
| Avg Merging | 64.2 | 78.9 |
| TIES-Merging | 60.7 | 80.3 |
| EMR-Merging | 63.8 | 69.3 |
| PCB-Merging | 58.0 | 81.7 |
| Avg Merging + FT | 57.8 | 87.5 |
| **ES-Merging** | **65.7** | **87.4** |

### 消融实验

| 配置 | Avg Acc | 说明 |
|------|---------|------|
| Layer-wise only | 65.0 | 只用粗粒度 |
| Element-wise only | 64.8 | 只用细粒度 |
| Layer + Element (ES-Merging) | 65.7 | 组合最优 |

### 关键发现
- ES-Merging 在 molecule-protein 交互上不仅超越所有 merging 方法，还超越了 Avg Merging + FT（task-specific fine-tuned），说明 embedding-aware 系数比暴力 fine-tune 更准
- 单模态 MLLM 在非本模态任务上常常大幅退步（如 Prot2Text 在 molecule-protein 的 Human 子集只有 47.2%），而 merging 后统一模型全面提升
- Layer-wise 和 element-wise 缺一不可，组合比单独使用各高 0.7-0.9%

## 亮点与洞察
- **Paradigm shift**: 把 model merging 从 parameter space 拉到 embedding space，利用 input-aware 的信号估计系数，思路干净且有理论支撑
- **无训练**: 不需要额外优化过程，只需 forward + backward 即可估计系数，非常高效
- **超越 fine-tuned 模型**: 在某些任务上 merging 甚至比专门 fine-tune 好，说明好的 merging 策略能保留更多互补知识

## 局限性 / 可改进方向
- 只在 LLaMA-3.1-8B + LoRA 设置下验证，对 full fine-tune 或不同规模模型的泛化性未知
- 生物领域的实验设置较为 niche，在更广泛的视觉/语言多任务 merging 上是否同样有效需要验证
- SWD 和梯度计算需要对每个 probe sample 做完整 forward + backward，probe sample 数量对结果的敏感性未充分分析
- 温度参数 $\tau$ 在 softmax 中的影响未讨论

## 相关工作与启发
- **vs TIES-Merging**: sign-based 启发式，input-agnostic → ES-Merging 用 embedding 信号，input-aware
- **vs AdaMerging**: 用 test data 自适应调系数，但仍在 parameter space → 效果反而最差
- **vs PCB-Merging**: magnitude-based，在 cell 任务上不错但 protein 任务差 → 说明 parameter 信号的不稳定性

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 从 parameter space 到 embedding space 的范式转变，是 model merging 领域的新方向
- 实验充分度: ⭐⭐⭐⭐ 生物跨模态任务覆盖全面，但缺少 NLP/CV 通用场景验证
- 写作质量: ⭐⭐⭐⭐ 动机 figure 清晰，公式规范
- 价值: ⭐⭐⭐⭐ 对 model merging 社区有启发，embedding-aware 思路可广泛应用
