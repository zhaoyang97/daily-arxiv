# PolyGLU: State-Conditional Activation Routing in Transformer Feed-Forward Networks

**日期**: 2026-03-07  
**arXiv**: [2603.13347](https://arxiv.org/abs/2603.13347)  
**代码**: [GitHub](https://github.com/danielxmed/PolyGLU)  
**领域**: LLM/NLP  
**关键词**: activation function, feed-forward network, Gumbel-Softmax routing, emergent specialization, SwiGLU

## 一句话总结

提出 PolyGLU，将 Transformer FFN 中固定的单一激活函数替换为可学习的多激活函数动态路由机制（K=4），通过 Gumbel-Softmax 端到端训练，发现无需任何显式正则化即可涌现出近确定性的路由选择和深度依赖的激活函数特化模式（浅层偏好 GELU、深层偏好 Tanh）。

## 研究背景与动机

生物神经系统使用多种神经递质（谷氨酸、GABA、多巴胺、乙酰胆碱）在共享的神经回路中实现不同的信号处理模态。然而现代 Transformer 在所有 FFN 神经元上统一使用单一固定激活函数。从 ReLU → GELU → SwiGLU 的演进虽然提升了性能，但"一个激活函数适用于所有神经元"的基本假设从未被挑战。

作者受生物神经多样性启发，提出核心问题：**不同层、不同神经元是否需要不同的非线性变换？** 如果给予模型选择激活函数的自由度，它会如何自组织？

此外，MoE 模型在 token 级别做路由，但需要显式的 load-balancing loss 防止路由坍缩。PolyGLU 在更细粒度（神经元级别）进行路由，且无需任何辅助损失。

## 方法详解

### 整体框架

PolyGLU 是 SwiGLU 的 drop-in 替换。标准 SwiGLU 计算为：

$$\text{SwiGLU}(\mathbf{x}) = [\text{SiLU}(\mathbf{x}W_{\text{gate}})] \odot (\mathbf{x}W_{\text{up}})$$

PolyGLU 将固定的 SiLU 替换为 K=4 个候选激活函数的加权混合：

$$\text{PolyGLU}(\mathbf{x}) = \left[\sum_{k=1}^{K} g_k \cdot \sigma_k(\mathbf{x}W_{\text{gate}})\right] \odot (\mathbf{x}W_{\text{up}})$$

四种候选激活函数的选择有明确的设计意图：

| 编号 | 函数 | 性质 | 生物类比 |
|------|------|------|----------|
| 0 | ReLU | 硬阈值 | 谷氨酸（兴奋性） |
| 1 | Tanh | 对称压缩 | GABA（抑制性） |
| 2 | SiLU | 自门控 | 多巴胺（调制性） |
| 3 | GELU | 概率门控 | 乙酰胆碱（注意力） |

### 关键设计

**路由机制** 由静态偏好和动态门控两部分组成：

1. **静态偏好（Static Preferences）**：每个神经元 $j$ 维护一个可学习偏好向量 $\boldsymbol{\alpha}_j \in \mathbb{R}^K$，初始化为零（均匀先验），编码神经元的固有激活亲和力。

2. **动态门控（Dynamic Gating）**：一个轻量 MLP 处理 mean-pooled 的隐藏状态 $\bar{\mathbf{h}}$，生成上下文相关的路由调制信号：
   $$f(\bar{\mathbf{h}}) = W_2 \cdot \text{ReLU}(W_1 \bar{\mathbf{h}} + b_1) + b_2$$
   其中 $W_1 \in \mathbb{R}^{32 \times d_{\text{model}}}$，$W_2 \in \mathbb{R}^{K \times 32}$。

3. **组合路由**：最终 logits 为 $\ell_k = \alpha_k + \beta_k \cdot f(\bar{\mathbf{h}})_k$，通过 Gumbel-Softmax 得到路由权重 $g_k$。

**Gumbel-Softmax 温度退火**：

$$\tau(t) = \max(0.1, 1.0 - 0.9 \cdot t / t_{\text{total}})$$

τ=1.0（训练开始）时路由接近均匀→探索；τ=0.1（训练结束）时路由近确定性→承诺。

**参数开销极低**：每层约 49,320 个路由参数（$\alpha$ 16,384 + $\beta$ 4 + 门控网络 32,932），28层总计约 1.4M，仅占 597M 总参数的 **0.23%**。

### 损失函数 / 训练策略

- **无任何辅助损失**：不使用稀疏性损失、熵惩罚或 load-balancing 正则化，路由行为完全由语言建模交叉熵目标驱动
- 优化器：AdamW（β₁=0.9, β₂=0.95, weight decay=0.1，$\alpha$ 和 $\beta$ 豁免 weight decay）
- 学习率：cosine decay，2000 步 warmup，峰值 1e-4
- 有效 batch size：524,288 tokens（16 序列 × 4096 tokens × 8 梯度累积）
- 总训练：19,531 步，约 10.24B tokens
- **数据混合**：Math 70% / STEM 25% / Code(Python) 5%，训练最后 20% 退火为 85/10/5
- SFT 阶段冻结 τ=0.1，学习率 2e-5，训练 13,067 步

**Weight Decay Bug 事件**：训练约 10,000 步时发现 $\alpha$（2D 张量）被误分入 weight decay 组，导致静态偏好被持续抑制。通过 optimizer state transplant 修复，无 loss spike。这一 bug 反而揭示了重要发现：仅靠动态门控网络就能达到近确定性路由。

## 实验关键数据

### 主实验

模型架构 PolychromaticLM：597M 参数，28 层，hidden dim 1024，FFN dim 4096，GQA（16/8 heads），RoPE，Qwen3 tokenizer。

| Benchmark | Metric | Base | SFT | Δ | Qwen3-0.6B |
|-----------|--------|------|-----|---|------------|
| HellaSwag | acc_norm | 28.51 | 27.84 | -0.67 | 41.10 |
| ARC-Easy | acc_norm | 41.04 | 36.11 | -4.93 | 65.60 |
| ARC-Challenge | acc_norm | 22.27 | 24.15 | +1.88 | 33.90 |
| PIQA | acc_norm | 58.87 | 54.52 | -4.35 | 70.00 |
| WinoGrande | acc | 52.17 | 52.72 | +0.55 | 58.50 |
| BoolQ | acc | 61.13 | 55.63 | -5.50 | 69.70 |
| MMLU-STEM | acc (5-shot) | 25.28 | 28.42 | +3.14 | — |
| LAMBADA | acc | 15.35 | 7.01 | -8.34 | — |
| OpenBookQA | acc_norm | 29.00 | 26.80 | -2.20 | — |
| SciQ | acc_norm | 61.20 | 52.70 | -8.50 | — |
| **Mean** | | **39.48** | **36.59** | **-2.89** | — |

关键结论：在 6 个有 Qwen3-0.6B-Base 对比数据的 benchmark 上，PolychromaticLM 达到 Qwen3 **62-89%** 的性能，但仅用了 **3600 分之一** 的训练数据。

### 消融实验

论文没有标准消融实验（缺少 SwiGLU baseline 是作者自述的最大局限），但提供了丰富的路由行为分析和领域困惑度数据作为替代：

| 分析维度 | 关键数值 | 含义 |
|----------|----------|------|
| 平均动态路由熵 | 4.1×10⁻⁴（最大值的 0.030%） | 路由几乎完全确定性 |
| Layer 17 路由熵 | 9.6×10⁻³ | 全网最高，主动维持激活多样性 |
| 静态偏好被抑制时动态熵 | 最大值的 0.58% | 动态门控本身足以做出确定路由 |
| SFT 路由熵变化 | 恒定 ln(4)≈1.386 | 微调完全不影响路由结构 |
| Math 困惑度 | 3.56 | 主训练域效果最好 |
| Code 困惑度 | 7.08 | 仅 5% 数据但优于 STEM |
| STEM 困惑度 | 31.93 | 25% 数据但困惑度最高 |

### 关键发现

1. **自发路由收敛**：无需任何正则化，路由机制自发收敛到近确定性选择。作者假设语言建模损失本身提供了足够的路由特化信号——特定激活函数产生更干净一致的梯度，Gumbel-Softmax 温度退火形成正反馈循环。

2. **深度依赖特化**：28 层呈现清晰的激活函数梯度：
   - 浅层（0-2）：GELU 主导（35-40%），Tanh 和 SiLU 次之
   - 中间层（3-14）：渐变过渡，GELU 仍占多数，SiLU 增长至 15-25%
   - 深层（15-27）：Tanh 激增至 50-65%，成为绝对主导

3. **三个"弹性层"**：Layer 9、16、17 维持较高路由熵，尤其 Layer 17 在训练后期熵反而增加，暗示这些层主动从激活多样性中获益。

4. **微调鲁棒性**：13,067 步 SFT 期间路由熵恒定，说明 PolyGLU 干净地分离了"如何计算"与"计算什么"，微调不会导致路由坍缩。

5. **Code vs STEM 困惑度反转**：Code 仅用 5% 训练数据却远低于 25% 的 STEM 困惑度，归因于 Python 代码更低的固有熵和数学训练的迁移效应。

## 亮点与洞察

- **核心创新不在机制本身，而在涌现行为**：PolyGLU 的机制相对简单，但无监督涌现出的路由模式（近确定性收敛、深度特化、弹性层）极具启发性。
- **"一个激活函数适用所有层"的假设被挑战**：深层偏好 Tanh 的有界对称输出，浅层偏好 GELU 的概率门控，这一发现可直接指导未来架构设计。
- **实用性极强的参数效率**：0.23% 的参数开销实现了全新的计算范式，且收敛后的路由模式可以"蒸馏"为静态固定激活，零推理成本。
- **独立研究者的示范**：单张 A100、346 美元总预算、12.5 天训练，证明了架构创新研究可以在大型工业实验室之外完成。
- **Weight Decay Bug 的意外收获**：训练中的 bug 反而帮助验证了动态门控单独就能完成路由的关键结论。

## 局限性 / 可改进方向

1. **缺少 SwiGLU baseline**：最关键的缺陷——没有完全相同配置的 vanilla SwiGLU 对照实验，无法归因于 PolyGLU 还是训练设置
2. **缺少 GSM8K 评估**：因推理效率问题未完成 generation-based 评估
3. **规模受限**：仅在约 600M / 10B tokens 尺度验证，大规模下路由模式是否持续未知
4. **激活函数 palette 选择**：K=4 且组合是启发式选择，未探索 Mish、squared ReLU 等候选或 K 的最优值
5. **推理开销**：推理时需计算所有 K 个激活函数再选择，但可通过冻结路由消除
6. **SFT 后普遍性能下降**：mean -2.89pp，数学微调导致通用能力遗忘较明显

## 相关工作与启发

- **GLU 系列** (Dauphin et al. 2017 → Shazeer 2020 SwiGLU)：PolyGLU 是 SwiGLU 的自然推广，从固定激活到可选激活
- **MoE** (Shazeer et al. 2017, Switch Transformer)：MoE 在 token→expert 级别路由，PolyGLU 在 neuron→activation 级别路由，粒度更细且无需 load-balancing
- **Gumbel-Softmax** (Jang et al. 2017)：成熟的离散选择可微化技术，温度退火是关键的训练策略
- **自适应计算** (Graves 2016)：PolyGLU 是 per-neuron per-layer 的自适应，结合了静态偏好和动态输入条件

**对后续研究的启发**：
- 可训练 PolyGLU 后观察路由模式再"蒸馏"为异构固定激活（zero-cost at inference）
- 路由模式可作为 data-driven 的激活函数搜索方法
- Tanh 在深层偏好暗示有界对称激活可能提供隐式正则化，值得深入研究

## 评分

| 维度 | 分数 (1-10) | 评语 |
|------|-------------|------|
| 新颖性 | 7 | 激活函数路由的想法有新意，但机制本身（Gumbel-Softmax+MLP 门控）较标准 |
| 技术深度 | 7 | 路由行为分析非常细致，但缺少 ablation 和 SwiGLU baseline 是硬伤 |
| 实验充分度 | 5 | 单一模型规模、无对照 baseline、缺少 generation 评估 |
| 写作清晰度 | 9 | 论文写得极好，Weight Decay Bug 的坦诚报告和分析是加分项 |
| 实用价值 | 7 | 0.23% overhead 的 drop-in 替换有实用前景，但需大规模验证 |
| **综合** | **7** | 涌现行为分析是核心亮点，但实验规模和 baseline 缺失制约了结论强度 |
