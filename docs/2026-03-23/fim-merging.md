# FIM-Merging: Data-Free Layer-Adaptive Merging via Fisher Information for Long-to-Short Reasoning LLMs

**日期**: 2026-03-23  
**arXiv**: [2603.21705](https://arxiv.org/abs/2603.21705)  
**代码**: 无  
**领域**: LLM推理 / 模型合并  
**关键词**: model merging, Fisher information, layer-adaptive, Long-to-Short, reasoning LLM

## 一句话总结
提出 FIM-Merging，首次理论证明模型合并误差由 per-layer Hessian 范数约束，用 Fisher 信息矩阵作为无需校准数据的代理信号，实现层自适应合并系数分配。在 L2S（长推理→短推理）场景下，FIM-TIES 在 1.5B/7B 上均超越 ACM-TIES，MATH500 +6.2 点，同时输出长度缩短 92.6%。

## 研究背景与动机

1. **领域现状**: Long-to-Short (L2S) 通过参数空间合并将基座模型和长链推理模型结合，期望保留推理准确性的同时减少输出长度。Task Arithmetic ($\theta_{merged} = \theta_0 + \alpha \delta$) 是主流框架。

2. **现有痛点**: Task Arithmetic 假设模型行为在参数空间线性插值，但 L2S 场景下 task vector 范数比常规微调大一个数量级且层间差异巨大，线性假设系统性失效。ACM 等层自适应方法虽有效，但需要领域校准数据，且无理论依据。

3. **核心矛盾**: 层间合并敏感度差异巨大（FIM 最大/最小比 >1000x），统一系数 α 必然在某些层过激/过保守。但如何确定每层合并系数？缺乏理论指导，全靠启发式。

4. **切入角度**: 证明合并误差被 per-layer Hessian 范数约束（Proposition 1），再利用 Fisher-Hessian 等价性用对角 FIM 近似 Hessian，且发现用随机 token 输入算出的 FIM 与领域数据算出的高度一致。

5. **核心 idea**: 理论驱动的无数据层自适应合并——FIM × task vector 范数 = 合并误差上界的可计算代理 → 自适应层合并系数。

## 方法详解

### 整体框架
给定基座模型 $\theta_0$ 和长推理模型 $\theta_1$，计算 task vector $\delta = \theta_1 - \theta_0$。用 8 条随机 token 计算每层对角 FIM，乘以 $\|\delta^l\|^2$ 得到层重要性分数。通过 log 归一化 + sigmoid 映射转换为层合并系数 $\alpha^l$。高 FIM 层保守合并，低 FIM 层激进合并。

### 关键设计

1. **合并误差 Hessian 上界（Proposition 1）**:
   - 证明 $\mathcal{E}(\alpha) \leq \frac{\alpha(1-\alpha)}{2} \|\delta\|^2 \sup_t \|H_f\|_2$
   - Taylor 展开后一阶项对消，误差由二阶 Hessian 控制
   - 层 Hessian 范数大 → 合并误差大 → 应保守合并

2. **Fisher-Hessian 等价性**:
   - 在局部最优附近 $\mathcal{F}(\theta^*) = -\mathbb{E}[H_{\log p}(\theta^*)]$
   - 对角 FIM 是 Hessian 的低成本可计算代理
   - 只需 N=8 条随机输入即可估计，无需领域数据

3. **FIM-TIES 增强工程**:
   - TIES 剪枝阈值随模型规模调整：1.5B 保留 top-20%，7B 保留 top-40%
   - Gate 投影额外保护：$\alpha_{gate}^l = 0.7 \cdot \alpha^l$
   - 残差范数校准：合并后 norm 偏差 >5% 的层做重缩放

### 训练策略
完全 training-free、data-free。仅需 8 次前向+反向传播计算 FIM。

## 实验关键数据

### 1.5B 主实验

| 方法 | GSM8K | MATH500 | 平均 | 长度 |
|------|-------|---------|------|------|
| Base (Qwen2.5-Math) | 75.9 | 36.2 | - | 643 |
| DeepSeek-R1-1.5B | 76.6 | 69.6 | - | 5671 |
| ACM-TIES | 78.4 | 71.4 | 43.3 | 1489 |
| **FIM-TIES** | **81.6** | **74.9** | **47.3** | **411** |

### 7B 主实验

| 方法 | GSM8K | MATH500 | Olympiad | AIME24 |
|------|-------|---------|----------|--------|
| ACM-TIES | 92.2 | 84.0 | 46.4 | 33.3 |
| **FIM-TIES** | **92.2** | **90.2** | **47.9** | 26.7* |

*FIM-TIES + self-consistency (n=16) 在 AIME24 达 36.7%，超过 ACM-TIES 的 33.3%

### 关键发现
- FIM 层间辨识度极强：最大/最小比 >1700×（Layer 0: 4.43e-3, Layer 25: 2.61e-6）
- 单用权重范数做代理产生近均匀系数（α≈0.53），效果比 Task Arithmetic 还差
- FIM × ‖δ‖² 的组合比单用 FIM 在理论和实验上都更优
- 1.5B 输出长度仅 411 tokens（DeepSeek-R1 的 7.2%），推理效率极高

## 亮点与洞察
- **首个合并误差理论界**：从 Hessian 上界到 Fisher 代理，建立了模型合并的理论基础，不止是经验方法
- **无数据层自适应**：8 条随机输入即可获得和领域数据近似的层重要性排名，彻底消除对校准数据的依赖
- **长度压缩 92.6%**：从 5671 tokens 压到 411 tokens，同时准确率反而更高，体现了保守合并关键层的价值

## 局限性 / 可改进方向
- 对角 FIM 仅捕捉参数级别的独立重要性，忽略参数间交互
- 7B 规模下 AIME24 greedy 结果低于 ACM-TIES，需要 self-consistency 才能超越
- 只验证了 Qwen/DeepSeek 两个模型族的 L2S 合并

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次为层自适应合并提供理论基础，Fisher 代理优雅实用
- 实验充分度: ⭐⭐⭐⭐ 两个规模六个基准完整对比，消融充分
- 写作质量: ⭐⭐⭐⭐⭐ 理论推导清晰，实验设计严谨
- 价值: ⭐⭐⭐⭐⭐ 对模型合并领域有重要理论贡献
