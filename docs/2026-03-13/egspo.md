# Reinforcement Learning for Diffusion LLMs with Entropy-Guided Step Selection and Stepwise Advantages

**日期**: 2026-03-13  
**arXiv**: [2603.12554](https://arxiv.org/abs/2603.12554)  
**代码**: [EGSPO](https://github.com/vishnuteja/egspo)  
**领域**: 图像生成 / LLM推理  
**关键词**: diffusion language model, reinforcement learning, GRPO, entropy-guided, stepwise advantage

## 一句话总结
针对扩散语言模型（DLM）提出 EGSPO/EGSPO-SA，将去噪轨迹建模为有限时域 MDP，推导出精确的逐步策略梯度——通过熵引导选择信息量最大的去噪步 + 单步去噪奖励估计逐步优势，在编码和逻辑推理上达到 DLM RL 后训练的 SOTA。

## 研究背景与动机

1. **领域现状**: DLM（masked discrete diffusion）通过迭代去噪生成文本，支持双向上下文和多 token 并行，是 AR-LM 的有力替代。RL 后训练在 AR-LM 上效果显著（GRPO/PPO），但 DLM 缺乏高效 RL 方法。

2. **现有痛点**: 将 AR-LM 的 RL 方法直接搬到 DLM 失败——DLM 没有因果 token 分解，序列级似然不可解。现有方法（d1/wd1/SPG/d2 等）依赖代理似然或启发式近似，引入偏差，忽略去噪过程的序列结构。

3. **核心矛盾**: DLM 的决策发生在去噪步而非 token 位置——标准 GRPO 把同一个序列级优势广播给所有步，无法做精细的信用分配。

4. **切入角度**: 从第一原理出发——什么是 DLM 正确的 MDP 形式化？精确策略梯度是什么？如何利用扩散结构做步级优势估计和计算分配？

5. **核心 idea**: 将去噪过程建模为有限时域 MDP → 推导精确逐步策略梯度 → 用熵选择信息量最大的步进行更新 + 一步去噪完成估计逐步优势。

## 方法详解

### 整体框架
masked diffusion 生成 = 从全 mask 逐步 unmask → 建模为 MDP（状态=部分 mask 序列，动作=unmask 哪些 token 填什么值）→ 推导精确策略梯度 → EGSPO（熵引导步选择）→ EGSPO-SA（+逐步优势估计）。

### 关键设计

1. **有限时域 MDP 形式化**: 状态 $\mathbf{x}_t$（部分 mask 序列），动作 = 去噪策略 $\pi_\theta^{t|t+1}$，奖励只在最终序列 $\mathbf{x}_0$ 上给

2. **熵引导步选择（EGSPO）**: 不是每一步都更新——计算每步的去噪策略分布熵 $H_t$，选择熵最大的 K 步（信息量最大/最不确定）做策略梯度更新。其他步跳过→节省计算

3. **逐步优势估计（EGSPO-SA）**: 从中间状态 $\mathbf{x}_{t+1}$ 做一步贪心去噪完成 → 得到近似序列 → 计算奖励作为基线 → $A_t = r(\mathbf{x}_0) - r(\hat{\mathbf{x}}_{0|t+1})$ 衡量第 t 步的增量贡献。不需要额外 value 网络或多步 rollout

### 训练策略
- 基于 GRPO 框架，替换为逐步损失
- 精确策略梯度不需要显式序列似然计算

## 实验关键数据

### 编码和推理 Benchmark

| 方法 | LiveCodeBench | MBPP+ | LogiQA |
|------|-------------|-------|--------|
| d1 (GRPO for DLM) | ~30% | ~55% | ~40% |
| wd1 | ~32% | ~56% | ~42% |
| **EGSPO-SA** | **~38%** | **~62%** | **~48%** |

### 关键发现
- 熵引导步选择和逐步优势都有独立贡献，两者结合效果最佳
- 高熵步确实是最值得优化的——在这些步做策略更新效率最高
- 一步去噪完成作为优势基线在去噪后期越来越准确

## 亮点与洞察
- **从第一原理推导**的方法论值得称赞——不是 patch 现有方法，而是重新形式化正确的 MDP 并推导精确梯度
- **熵引导计算分配**充分利用了 DLM 独有的属性——AR-LM 无此结构
- 逐步优势的估计方式巧妙利用了 DLM 天然的"全 unmask 预测"能力

## 局限性 / 可改进方向
- 只在相对小规模的 DLM 上评测，大规模 DLM（>7B）的效果和效率未知
- 数学推理上只是"competitive"未取得 SOTA——可能需要结合其他技巧
- 熵阈值 K 的选择是超参数，自适应 K 未探索
- 仅支持 masked diffusion，连续扩散 LM 的适用性未讨论

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次为 DLM 推导精确逐步策略梯度+熵引导计算分配
- 实验充分度: ⭐⭐⭐⭐ 编码+逻辑+数学多 benchmark，有消融
- 写作质量: ⭐⭐⭐⭐⭐ 理论推导严谨，表述清晰
- 价值: ⭐⭐⭐⭐ 为 DLM 的 RL 后训练建立了理论基础
