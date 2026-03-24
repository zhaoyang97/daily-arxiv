# ADaFuSE: Adaptive Diffusion-generated Image and Text Fusion for Interactive Text-to-Image Retrieval

**日期**: 2026-03-23  
**arXiv**: [2603.21886](https://arxiv.org/abs/2603.21886)  
**代码**: [GitHub](https://anonymous.4open.science/r/ADaFuSE-E149/README.md)  
**领域**: 信息检索 / 多模态融合  
**关键词**: interactive text-to-image retrieval, diffusion augmentation, adaptive gating, mixture-of-experts, multi-modal fusion

## 一句话总结

提出 ADaFuSE，用自适应门控 + 语义感知 MoE 双分支替代扩散增强交互式文本-图像检索 (I-TIR) 中的静态加法融合，动态校准文本与扩散生成图像的融合权重，在 4 个 I-TIR 基准上以仅 5.29% 的参数增量超越 DAR 最高 3.49% Hits@10，被 SIGIR 2026 录用。

## 研究背景与动机

1. **任务定义**: 交互式文本-图像检索 (I-TIR) 允许用户通过多轮自然语言对话迭代细化搜索意图，逐步逼近目标图像。与单次查询不同，需要系统整合多轮对话上下文。
2. **扩散增强范式**: DAR (Long et al., SIGIR 2025) 引入扩散模型从对话上下文条件生成合成图像，作为视觉代理桥接文本查询与图像语料库之间的模态鸿沟，在零样本场景下取得 SOTA。
3. **静态融合的致命缺陷**: DAR 使用固定权重加法融合文本和生成图像嵌入 ($z = z^T + \alpha \cdot z^D$)。但扩散模型本质上是随机的，生成图像质量因实例而异——作者在 VisDial 验证集实证发现，从第 2 轮开始超过 50% 的样本因引入扩散噪声反而性能下降（degradation rate > 55.62%），退化样本的平均排名下降约 7500 位。
4. **实例级差异被忽视**: 静态融合对所有样本一视同仁，无法根据当前生成图像与文本查询之间的语义一致性动态调整——高质量生成图像应被充分利用，低质量的应被抑制。
5. **与 CIR 的本质区别**: 组合图像检索 (CIR) 中参考图像是真实可靠的，文本是修改指令；但 I-TIR 中生成图像本身就含噪声，两种模态理论上语义等价但实际偏差大，需要专门的融合机制。
6. **核心洞察**: 问题不在于扩散增强本身无效，而在于融合策略太粗暴——需要「按质分配」的自适应融合来同时获得扩散增强的好处并规避其噪声。

## 方法详解

### 整体框架

ADaFuSE 是一个即插即用的轻量级融合模块，插入在现有 I-TIR 框架的编码器之后、检索之前，不需要修改 backbone 编码器。整体包含：投影层 → 双分支融合（自适应门控 + 语义感知 MoE）→ 残差聚合 → 归一化。

### 关键设计 1: 查询编码与非线性投影

文本查询 $T_{n,i}$ 和扩散生成图像 $I_{n,i}$ 分别经过预训练的文本/图像编码器 $\Phi_T, \Phi_I$ 得到 $d$ 维嵌入 $z^T, z^D$。由于预训练编码器倾向于压缩细粒度视觉细节，ADaFuSE 先用两个独立的投影头将嵌入映射到更高维的任务特定空间：

$$\mathbf{h}^T = \text{GELU}(\mathcal{P}_T(z^T)), \quad \mathbf{h}^D = \text{GELU}(\mathcal{P}_D(z^D))$$

其中 $\mathcal{P}: \mathbb{R}^d \to \mathbb{R}^{d'}$，拼接得到联合表示 $\mathbf{h}_u = [\mathbf{h}^T; \mathbf{h}^D] \in \mathbb{R}^{2d'}$，作为后续两个分支的共享输入。

### 关键设计 2: 自适应门控分支 (Adaptive Gating)

核心思想：从联合上下文 $\mathbf{h}_u$ 预测当前生成图像的可靠性，输出动态标量权重 $\lambda \in (0,1)$：

$$\lambda = \sigma(\mathbf{W}_2 \cdot \text{GELU}(\mathbf{W}_1 \mathbf{h}_u + \mathbf{b}_1) + \mathbf{b}_2)$$

门控值调制原始语义嵌入的融合：

$$\mathbf{z}^{base} = \lambda \cdot z^T + (1-\lambda) \cdot z^D$$

**关键行为**: 可视化分析显示，ADaFuSE 对生成图像权重 $(1-\lambda)$ 保守在 15%–25% 之间，远低于 DAR 的固定 45%。且随着文本-图像余弦相似度增加，系统自适应放大图像贡献——语义对齐度高时信任图像，对齐度低时回退到文本。

### 关键设计 3: 语义感知混合专家分支 (Semantic-aware MoE)

门控分支只能在两个模态嵌入之间线性插值，无法捕捉高阶跨模态交互。MoE 分支通过 $K$ 个语义专家提供补偿特征：

- 每个专家 $E_k: \mathbb{R}^{2d'} \to \mathbb{R}^{d_{hidden}}$ 是独立参数的轻量 FFN
- 路由网络基于 $\mathbf{h}_u$ 计算 softmax 路由概率 $p_k$
- 加权聚合专家输出：$\mathbf{h}_{res} = \sum_{k=1}^K p_k E_k(\mathbf{h}_u)$

最终通过投影矩阵 $\mathbf{W}_{out} \in \mathbb{R}^{d \times d_{hidden}}$ 映射回原始空间，以残差方式加到门控输出上：

$$\mathbf{z}^{final} = \text{Normalize}(\mathbf{z}^{base} + \mathbf{W}_{out} \mathbf{h}_{res})$$

**设计动机**: 扩散模型可能生成看似无关但实际对检索有用的元素（如"更短的袖子但相同轮廓"这类组合语义），需要非线性特征合成而非简单模态选择。残差连接保留 base query 防止过度修正。

### 训练策略

- 在 DA-VisDial 数据集上端到端训练
- 使用预训练 BLIP 权重初始化编码器
- 对称 InfoNCE 损失（symmetric contrastive loss）
- 评估指标：累积 Hits@10

## 实验关键数据

### 主实验：4 个基准上的整体表现

| 基准 | 方法 | Round 0 | Round 5 | Round 10 |
|------|------|---------|---------|----------|
| VisDial | ChatIR (text-only) | baseline | baseline | baseline |
| VisDial | DAR (static fusion) | — | — | — |
| VisDial | **ADaFuSE** | **+1.09%** | — | **+3.49%** |

- 在所有 4 个基准（VisDial, ChatGPT_BLIP2, Human_BLIP2, Flan-Alpaca-XXL_BLIP2）上每轮都超越 DAR
- 随对话轮次增加优势扩大：round 0 提升 1.09% → round 10 提升 3.49%（VisDial Hits@10）

### 退化率分析

| 指标 | DAR | ADaFuSE |
|------|-----|---------|
| 退化率 (Round 2+) | >50%, 峰值 55.62% | 持续更低且随轮次递减 |
| 退化样本平均排名下降 | ~7500 位 | ~20 位 |

- ADaFuSE 将退化样本的排名损失从 ~7500 降至 ~20，降幅超过 **99.7%**

### 消融与分析

- **参数效率**: 仅增加 5.29% 参数（轻量 MLP + 小规模 MoE）
- **门控权重可视化**: 图像权重 $(1-\lambda)$ 集中在 15%–25%（vs DAR 固定 45%），且与文本-图像余弦相似度正相关
- **长对话鲁棒性**: 在 Flan-Alpaca-XXL_BLIP2 等低质量文本/长对话场景中，ChatIR 早期饱和，DAR 部分缓解，ADaFuSE 在每轮都持续提升——说明自适应融合能补偿低质量文本反馈

### 关键发现

1. **后期轮次收益更大**: 归因于预训练编码器在 MSCOCO 短文本上训练，处理早期简短对话尚可，但长对话+冲突线索场景下退化严重，ADaFuSE 的滤噪能力此时更关键
2. **DAR 即为非自适应消融**: ADaFuSE 与 DAR 共享相同 backbone，性能差异直接证明收益来自自适应融合模块而非其他因素
3. **保守但智能的图像利用**: 平均仅用 15%–25% 的图像权重，远低于 DAR 的 45%，但通过 MoE 分支的补偿特征仍能充分利用有价值的视觉信息

## 亮点与洞察

- **问题诊断极为充分**: 用 degradation rate 和 average rank drop 两个指标量化了静态融合的危害（55.62% 样本退化、排名下降 7500 位），动机令人信服
- **双分支互补设计精巧**: 门控分支做粗粒度模态选择（trust or suppress），MoE 分支做细粒度语义合成（extract useful from noisy），残差连接确保稳定性
- **即插即用的工程价值**: 不修改 backbone 编码器，5.29% 参数增量，可直接插入任何扩散增强 I-TIR 框架
- **可视化分析有说服力**: 门控权重与语义对齐度的正相关回归曲线，直观展示了自适应机制的合理行为

## 局限性 / 可改进方向

1. **仅在 BLIP backbone 上验证**: 未测试更强的视觉-语言模型（如 BLIP-2, SigLIP），泛化性待验证
2. **MoE 专家数量 $K$ 的选择**: 论文未充分讨论专家数量对性能的影响和最优选择
3. **训练数据单一**: 仅在 DA-VisDial 上训练，在其他数据集上的表现依赖迁移能力
4. **缺少端到端与扩散模型联合优化**: 当前扩散模型和融合模块是分离的，联合训练可能进一步提升
5. **退化率分析仅限 VisDial**: 其他三个基准上的退化率分析缺失

## 相关工作与启发

- **DAR (Long et al., SIGIR 2025)**: 扩散增强 I-TIR 的开创性工作，用静态加法融合，是本文的直接改进对象
- **ChatIR (Levy et al., NeurIPS 2023)**: 基于对话的图像检索框架，纯文本查询基线
- **Gated Multimodal Units (Arevalo et al., ICLR 2017)**: 门控多模态融合的经典方法，启发了 ADaFuSE 的门控设计
- **FuseMoE (Han et al., NeurIPS 2024)**: 灵活模态融合的 MoE transformer，与 ADaFuSE 的 MoE 分支相关
- **Provable Dynamic Fusion (Zhang et al., ICML 2023)**: 低质量多模态数据的可证明动态融合，理论支持自适应权重的优越性
- **对 CIR 领域的启发**: 组合图像检索中也可以引入类似的自适应融合思路，尤其在参考图像不可靠的场景

## 评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 新颖性 | ⭐⭐⭐ | 门控融合和 MoE 都非新技术，但首次系统地应用于扩散增强 I-TIR 场景，问题诊断有深度 |
| 技术深度 | ⭐⭐⭐⭐ | 双分支互补设计合理，投影→门控→MoE→残差的 pipeline 各环节都有清晰动机 |
| 实验充分度 | ⭐⭐⭐⭐ | 4 个基准、退化率分析、门控权重可视化、跨轮次对比，分析全面 |
| 写作质量 | ⭐⭐⭐⭐ | 动机清晰、图表丰富、分析深入，SIGIR 2026 水准 |
| 实用价值 | ⭐⭐⭐⭐ | 即插即用、参数增量小、对多模态检索框架有直接实用意义 |
