# Reinforcement Learning for Diffusion LLMs with Entropy-Guided Step Selection and Stepwise Advantages

**日期**: 2026-03-13  
**arXiv**: [2603.12554](https://arxiv.org/abs/2603.12554)  
**代码**: [EGSPO](https://github.com/vishnuteja/egspo)  
**领域**: 图像生成 / LLM推理  
**关键词**: diffusion language model, reinforcement learning, GRPO, entropy-guided, stepwise advantage

## 一句话总结
针对扩散语言模型（DLM）提出 EGSPO/EGSPO-SA——将去噪轨迹建模为有限时域 MDP 并推导精确逐步策略梯度，通过熵引导选择信息量最大的去噪步 + 单步去噪奖励估计逐步优势，EGSPO-SA 在 Sudoku 上达 94.3%、Countdown 78.5%、MBPP 51.1%、HumanEval 44.5%，均为 DLM RL SOTA。（ICML 2026）

## 研究背景与动机
1. **DLM 的崛起**: 扩散语言模型通过 masked discrete diffusion 迭代去噪生成文本，支持双向上下文和多 token 并行，是 AR-LM 的有力替代
2. **RL 移植困难**: AR-LM 的 RL（GRPO/PPO）依赖因果 token 分解，DLM 打破此结构——序列级似然不可解，importance ratio 无法直接计算
3. **现有近似的偏差**: d1/wd1/SPG/d2 等方法依赖代理似然或启发式近似，忽略去噪过程的序列结构，无法做精细信用分配
4. **核心问题**: DLM 的决策发生在去噪步而非 token 位置——标准 GRPO 广播同一序列级优势给所有步，无法区分哪些步真正重要

## 方法详解
### 整体框架
masked diffusion 生成 = 从全 mask 逐步 unmask → 建模为有限时域 MDP（状态 $\mathbf{x}_t$=部分 mask 序列，动作=unmask 决策）→ 推导精确策略梯度定理 → EGSPO（熵引导步选择）→ EGSPO-SA（+逐步优势估计）

### 关键设计
1. **有限时域 MDP**: 状态 $\mathbf{s}_t = (\mathbf{x}_{T-t}, \mathbf{q})$，动作 $\mathbf{a}_t = \mathbf{x}_{T-t-1}$，奖励仅在最终 $\mathbf{x}_0$ 给出 → 推导策略梯度：$\nabla J(\theta) = \sum_{t} \mathbb{E}[A_t^{\pi_\theta} \nabla \log \pi_\theta(\mathbf{x}_t | \mathbf{x}_{t+1})]$
2. **熵引导步选择（EGSPO）**: 计算每步去噪熵 $H(\pi_\theta^{t|t+1})$，选择 top-$K$ 高熵步更新（信息量最大/最不确定），其他跳过 → 节省计算。理论上界：$\Delta_S \leq B \sum_{t \notin S} H(\pi_\theta^{t|t+1})$
3. **逐步优势估计（EGSPO-SA）**: 从中间 $\mathbf{x}_{t+1}$ 做一步贪心 unmask → $\hat{\mathbf{x}}_{0|t+1}$ → $\hat{A}_t = (1+\lambda_t) r(\mathbf{x}_0) - \lambda_t r(\hat{\mathbf{x}}_{0|t+1})$，不需额外 value 网络
4. **逐步 GRPO 损失**: $L_t = -\min(\rho_t A_t, \text{clip}(\rho_t) A_t) + \beta D_{KL}(\pi_\theta \| \pi_{ref})$，$\rho_t = \pi_\theta(\mathbf{x}_t|\mathbf{x}_{t+1}) / \pi_{\theta_{old}}(\mathbf{x}_t|\mathbf{x}_{t+1})$

## 实验关键数据

| 方法 | Sudoku (Best) | Countdown (Best) | GSM8K (Best) | MATH500 (Best) |
|------|-------------|-----------------|-------------|----------------|
| LLaDA-8B-Instruct | 11.7 | 20.7 | 78.2 | 36.2 |
| d1 (GRPO for DLM) | 22.1 | 42.2 | 82.1 | 40.2 |
| wd1 | 76.4 | 51.2 | 82.3 | 39.0 |
| SPG | 94.0† | 71.5 | 86.1 | 41.8 |
| EGSPO | 93.6 | 75.8 | 85.7 | 39.0 |
| **EGSPO-SA** | **94.3** | **78.5** | **85.03** | **39.6** |

| 方法 | HumanEval (Best) | MBPP (Best) |
|------|-----------------|-------------|
| LLaDA-8B-Instruct | 37.8 | 41.2 |
| d1 | 37.8 | 44.7 |
| EGSPO | 40.2 | 50.6 |
| **EGSPO-SA** | **44.5** | **51.1** |

### 关键发现
- 逻辑推理（Sudoku/Countdown）上 EGSPO-SA 全面优于所有 baseline——全局约束任务最需逐步信用分配
- 编码任务（HumanEval/MBPP）提升巨大：EGSPO-SA 比 d1 高 6.7%/6.4%
- 数学推理上"competitive"但未取得 SOTA——可能因数学任务对去噪步结构的依赖不如逻辑和编码
- 高熵步确实是最值得优化的步——在这些步做策略更新效率最高
- EGSPO（无逐步优势）vs EGSPO-SA：SA 在 Countdown 上额外提升 2.7%（78.5 vs 75.8），在 HumanEval 上额外提升 4.3%（44.5 vs 40.2）
- 生成长度影响显著：多数任务在 256 或 512 token 时最优，说明 DLM 需要足够的去噪步数

## 亮点与洞察
- **从第一原理推导**：不是 patch 现有方法，而是重新形式化正确的 MDP 并推导精确梯度
- 熵引导计算分配充分利用 DLM 独有属性——AR-LM 的每个 token 都有因果依赖，无法选择性跳过
- 一步贪心完成作为优势基线巧妙利用了 DLM 天然的"全 unmask 预测"能力——不需额外 value 网络
- 理论上界 $\Delta_S \leq B \sum_{t \notin S} H(\pi_\theta^{t|t+1})$ 为步选择提供了原理性保证

## 局限性 / 可改进方向
- 仅在 LLaDA-8B 上评测，大规模 DLM（>7B）效果和效率未知
- 数学推理（MATH500 39.6%）未取得 SOTA——可能因数学推理更依赖 token 级精度而非步级结构
- 熵阈值 $K$ 的选择是超参数，自适应 $K$ 的探索留待未来
- 一步贪心完成在去噪早期（$t$ 大时）偏差较大，$\lambda_t$ 的设置缺乏自适应机制
- 仅支持 masked diffusion，连续扩散 LM（如 CDLM）的适用性未讨论

## 相关工作与启发
- **vs d1 (GRPO for DLM)**: d1 用均场似然近似广播序列级优势，Sudoku 上 22.1% vs EGSPO-SA 94.3%——精确梯度+逐步优势差距巨大
- **vs SPG**: SPG 优化 pessimistic/optimistic 界，Sudoku 需 3-shot 才达 94.0%†；EGSPO-SA 0-shot 达 94.3%
- **vs d2**: d2 是 trajectory-level 形式化但用 step-merging 估计器引入偏差；EGSPO 推导精确逐步梯度
- **vs AR-LM GRPO (DeepSeek-R1)**: AR 的 token-level 信用分配 vs DLM 的 step-level 信用分配——不同生成结构需要不同的 MDP 形式化

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次为 DLM 推导精确逐步策略梯度 + 熵引导计算分配
- 实验充分度: ⭐⭐⭐⭐ 编码+逻辑+数学 6 个 benchmark，有多长度评测
- 价值: ⭐⭐⭐⭐ 为 DLM 的 RL 后训练建立了理论基础（ICML 2026）
- 写作质量: ⭐⭐⭐⭐⭐ 理论推导严谨，从 MDP 形式化到实用算法一气呵成

## 补充说明
- 基于 LLaDA-8B-Instruct（masked diffusion LM），无需 SFT 直接 RL 微调
- 代码开源（GitHub），实验结果可复现
- 与 AR-LM 的 RL（如 DeepSeek-R1 的 GRPO）形成互补——EGSPO 是 DLM 领域的对应物
- 去噪步数 $T$ 通常为 $10^2$-$10^3$，熵引导步选择将计算减少到 $K$ 次前向传播
- 逐步优势的偏差控制：$\lambda_t$ 在去噪后期增大，利用一步完成越来越准确的特性
- 所有 baseline 结果引用自原论文（d1/wd1/SPG/d2），编码任务仅 d1 有公开结果
