# IGU-LoRA: Adaptive Rank Allocation via Integrated Gradients and Uncertainty-Aware Scoring

**日期**: 2026-03-14  
**arXiv**: [2603.13792](https://arxiv.org/abs/2603.13792)  
**代码**: [IGU-LoRA](https://github.com/withyou12/igulora.git)  
**领域**: 视频理解 / 参数高效微调  
**关键词**: LoRA, adaptive rank, integrated gradients, uncertainty scoring, parameter-efficient

## 一句话总结
提出 IGU-LoRA，将 Integrated Gradients 扩展到参数空间计算层内参数重要性得分，结合不确定性感知评分（EMA+偏差追踪）抑制噪声更新，用随机求积近似降低计算成本，实现自适应 LoRA rank 分配，在 GLUE 上以 0.33M 参数达到 89.42% 平均精度。

## 研究背景与动机

1. **领域现状**: LoRA 是 LLM 参数高效微调的主流方法，但在所有层使用统一 rank 忽略了层间重要性差异。AdaLoRA 等方法尝试自适应分配但依赖局部梯度信息。

2. **现有痛点**: 局部梯度只反映当前点的敏感度，无法捕捉参数从零到当前值的全路径贡献。rank 选择过程中梯度噪声大导致分配不稳定。

3. **核心 idea**: 用 Integrated Gradients（路径积分梯度）替代局部梯度评估参数重要性，用 EMA + 偏差追踪的不确定性评分稳定 rank 分配决策。

## 方法详解

### 关键设计

1. **Integrated Gradients 在参数空间的扩展**: 计算参数从零到当前值路径的积分梯度 $\text{IG}(w) = w \cdot \int_0^1 \nabla_w L(\alpha w) d\alpha$，捕捉非局部路径敏感性。用随机求积近似将 O(N) 前向-后向 pass 降低到 batch-linear 开销。

2. **不确定性感知评分**: 对重要性分数用 EMA 追踪均值和偏差（$\mu_t = \beta \mu_{t-1} + (1-\beta) s_t$），当偏差超过阈值时抑制该参数的 rank 贡献，避免噪声梯度导致的不稳定分配。

3. **自适应 Rank 分配**: 基于层级重要性得分分配不同 rank，总参数预算约束下优化。

## 实验关键数据

| 方法 | Params | GLUE Avg | CoLA | RTE |
|------|--------|---------|------|-----|
| LoRA | 0.33M | 87.86 | 68.83 | 85.56 |
| AdaLoRA | 0.33M | 88.45 | 70.32 | 86.64 |
| AutoLoRA | 0.33M | 88.76 | - | - |
| **IGU-LoRA** | **0.33M** | **89.42** | **71.93** | **88.46** |

### 关键发现
- 在 RoBERTa-large 上 GLUE 平均 89.42%，比 AutoLoRA +0.66%
- 在 Llama-2-7B、Llama-3-8B、DeepSeek-R1 等多种backbone上有效
- 随机求积的理论误差界 $O(N^{-2}) + O(M^{-1/2})$ 保证了计算效率

## 亮点与洞察
- Integrated Gradients 从输入归因扩展到参数重要性评估是跨领域迁移创新
- 不确定性感知的"信号 vs 噪声"区分机制比纯梯度阈值更鲁棒

## 局限性 / 可改进方向
- 随机求积仍有额外计算开销
- 缺少生成任务（翻译、摘要等）上的验证

## 评分
- 新颖性: ⭐⭐⭐⭐ IG 在参数空间的首次应用
- 实验充分度: ⭐⭐⭐⭐ 多 backbone + 多任务
- 写作质量: ⭐⭐⭐⭐ 理论推导完整
- 价值: ⭐⭐⭐ 增量提升，但为自适应 rank 提供新工具
