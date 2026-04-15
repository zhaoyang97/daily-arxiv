# MHPO: Modulated Hazard-aware Policy Optimization for Stable Reinforcement Learning

**日期**: 2026-03-14  
**arXiv**: [2603.16929](https://arxiv.org/abs/2603.16929)  
**代码**: 无  
**领域**: LLM推理 / 强化学习优化  
**关键词**: GRPO, importance ratio, training stability, Weibull hazard, policy optimization

## 一句话总结
提出 MHPO 框架，通过 Log-Fidelity Modulator（log 空间 tanh 映射保证梯度可微且有界）+ Decoupled Hazard Penalty（Weibull 累积危险函数对正/负策略偏移施加非对称惩罚），解决 GRPO 训练中 importance ratio 导致的梯度不稳定问题，在数学推理和 VLM 任务上一致超越 GRPO/DAPO/SAPO。

## 研究背景与动机

1. **领域现状**: GRPO（Group Relative Policy Optimization）是 LLM 后训练（RL）的主流方法之一，通过 group 内 rollout 计算相对优势替代 critic，成功解锁了 CoT 推理能力。

2. **现有痛点**: GRPO 依赖 importance ratio $r_t = \pi_\theta / \pi_{\theta_{old}}$ 来补偿策略差异，但在长序列 CoT 生成中 token 级别的 ratio 方差极大，**outlier token 导致梯度尖峰**，严重影响训练稳定性。PPO/GRPO 的硬裁剪 $[1-\epsilon, 1+\epsilon]$ 引入不可微边界和梯度消失区域，SAPO 的 sigmoid soft gating 虽恢复可微性但无法区分正/负策略偏移的不同风险。

3. **核心矛盾**: 正向偏移（概率增大）过度 → 模式坍塌；负向偏移（概率降低）过度 → 策略侵蚀（不可逆地抑制正常语言模式）。这两种风险天然不对称，但现有方法对称处理。

4. **切入角度**: 从可靠性工程/生存分析中借鉴 Weibull 累积危险函数，对正/负偏移施加不同的惩罚曲线，结合 log 空间的 tanh 有界映射保证全局梯度稳定。

5. **核心 idea**: 在梯度乘子层级做 fidelity + damping 的联合控制 — LFM 做有界映射保证可微，DHP 做方向解耦惩罚防止不对称风险。

## 方法详解

### 整体框架
MHPO 替换 GRPO 目标函数中的硬裁剪操作，用两个模块处理 importance ratio：先经 LFM 映射到有界可微空间，再经 DHP 施加方向性惩罚。最终目标函数为 $\mathcal{L} = -\mathbb{E}[\exp(\psi(r) - \zeta(r)) \hat{A}]$，其中 $\psi$ 是 LFM，$\zeta$ 是 DHP。

### 关键设计

1. **Log-Fidelity Modulator (LFM)**:
    - 做什么：将无界的 importance ratio 映射到有界可微流形
    - 核心思路：$\psi(r) = c \tanh(\log(r)/c)$，先取 log 将乘法空间变为加法空间（$r=1$ 成为原点），再用 scaled tanh 饱和到 $[-c, c]$
    - 三个关键性质：(1) 近原点时 $\psi \approx \log r$（高保真局部映射）；(2) 远离原点时梯度通过 $\mathrm{sech}^2$ 平滑衰减（不硬截断）；(3) $C^\infty$ 可微，不像硬裁剪那样破坏 Adam 的动量缓冲
    - 梯度乘子有理论上界：$|\mathcal{M}(r)| \leq e^c$（与 ratio 大小无关），保证了梯度二阶矩有界

2. **Decoupled Hazard Penalty (DHP)**:
    - 做什么：对正向（$r>1$）和负向（$r<1$）策略偏移施加不同强度的惩罚
    - 核心思路：$\zeta(r) = (s(\psi)/\lambda_+)^{k_+} + (s(-\psi)/\lambda_-)^{k_-}$，其中 $s(\cdot) = \log(1+e^x)$ 是 softplus，用于解耦正/负方向。Weibull 累积危险函数 $H(x) = (x/\lambda)^k$ 控制惩罚曲线形状
    - 设计动机：$\lambda$ 控制安全区域大小（小偏移惩罚可忽略），$k>1$ 保证超过阈值后惩罚加速增长。默认配置 $(k_+, \lambda_+) = (1.5, 1.0)$（正向宽松探索），$(k_-, \lambda_-) = (2.0, 0.8)$（负向严格抑制），反映"防止策略侵蚀比防止模式坍塌更重要"的不对称先验

3. **Semi-gradient 优化**:
    - DHP 中对 $\psi$ 应用 stop-gradient，使 $\zeta$ 仅作为幅值调制器而不改变策略梯度方向
    - 这是关键的实现细节 — 如果允许 DHP 梯度回传可能导致梯度反转

### 损失函数 / 训练策略
- 目标函数：$\mathcal{L}_{\text{MHPO}} = -\mathbb{E}[\frac{1}{K}\sum_i \frac{1}{T_i}\sum_t \exp(\psi(r_t) - \zeta(r_t)) \hat{A}_t]$
- 超参数选择：$c=1.5$，正向 $(k_+, \lambda_+)=(1.5, 1.0)$，负向 $(k_-, \lambda_-)=(2.0, 0.8)$
- 最大输出长度：Qwen2.5 系列 2048 tokens，Qwen3-4B 4096 tokens

## 实验关键数据

### 主实验（Qwen2.5-7B-Instruct, Avg@32）

| 方法 | MATH500 | HMMT25 | AMC23 | AIME25 | AIME24 | 平均 |
|------|---------|--------|-------|--------|--------|------|
| Baseline | 70.0 | 5.6 | 52.4 | 3.5 | 16.4 | 29.6 |
| GRPO | 79.2 | 7.8 | 68.3 | 8.6 | 27.4 | 38.3 |
| DAPO | 81.2 | 9.1 | 71.3 | 11.4 | 28.0 | 40.2 |
| SAPO | 80.4 | 8.0 | 69.2 | 10.1 | 27.1 | 39.0 |
| **MHPO** | **82.1** | **13.8** | **74.6** | **16.7** | **31.5** | **43.7** |

### 消融实验（LFM + DHP 贡献）

| 配置 | 平均 Avg@32 | 说明 |
|------|-----------|------|
| GRPO (baseline) | 38.3 | 原始硬裁剪 |
| + LFM only | ~41 | 可微映射带来稳定性提升 |
| + DHP only | ~40 | 危险惩罚提升 |
| LFM + DHP (MHPO) | 43.7 | 两者互补，最优 |
| c=0.5 | 降低 | c 太小压缩信号过度 |
| c=2.0 | 略降 | c 太大衰减不足 |
| 对称 DHP ($k_+=k_-$) | 降低 | 证实不对称设计必要 |

### 关键发现
- **挑战越大收益越大**: 在竞赛级难题（AIME25、HMMT25）上 MHPO 优势最明显（比 DAPO +6 pts），说明稳定优化在困难推理中更关键
- **Base 模型获益最大**: 在 Qwen3-4B-Base 上 MHPO 平均 52.9%（比 GSPO +5.7 pts），因为 base 模型策略漂移更剧烈
- **梯度稳定性可视化**: MHPO 训练过程中梯度 norm 始终低且平稳，而 GRPO/DAPO 出现频繁尖峰
- **VLM 同样有效**: 在 Qwen2.5-VL-7B 上达到 53.0% 平均（比 DAPO +0.7），证实多模态场景也适用

## 亮点与洞察
- **从可靠性工程借鉴 Weibull 危险函数**做策略惩罚非常巧妙 — 累积危险函数天然具有"小偏移安全，大偏移急剧惩罚"的形状，完美匹配信任域的需求
- **stop-gradient 的使用**是被低估的关键设计 — 如果 DHP 也参与梯度回传会导致惩罚项自身被优化掉，这种 semi-gradient 技巧值得在其他带惩罚项的 RL 方法中推广
- **理论保证** $|\mathcal{M}(r)| \leq e^c$ 意味着只需调一个超参 $c$ 就能控制梯度稳定性的上界，比 PPO/DAPO 的裁剪阈值直觉上更有计算理论保障

## 局限性 / 可改进方向
- 超参数较多（$c, k_+, k_-, \lambda_+, \lambda_-$），虽然默认配置在多个模型上有效，但最优配置可能随任务变化
- 仅在数学推理任务上验证，缺少代码生成、通用对话等任务的实验
- 与 DAPO 的差距在 VLM 上较小（+0.7），说明多模态场景的优势有限
- 没有与最新的 KL-based 方法（如 Dr. GRPO）做对比

## 相关工作与启发
- **vs GRPO/PPO**: 硬裁剪导致梯度不连续 + 消失区域，MHPO 用 tanh 做平滑饱和彻底解决
- **vs DAPO**: DAPO 只是不对称裁剪边界，仍是硬裁剪；MHPO 在梯度乘子层级做连续的不对称控制
- **vs SAPO**: SAPO 用 sigmoid soft gate 恢复可微但不区分正/负偏移方向；MHPO 的 DHP 显式解耦
- 这种"梯度乘子层级的信号处理"思路有潜力推广到其他 RL 场景（机器人控制、RLHF 等）

## 评分
- 新颖性: ⭐⭐⭐⭐ 从生存分析借鉴 Weibull 函数做策略优化是独到的跨领域创新
- 实验充分度: ⭐⭐⭐⭐ 覆盖 4 种模型架构 + 8 个 benchmark，但缺少非数学任务验证
- 写作质量: ⭐⭐⭐⭐ 公式推导严谨，理论分析完整，但符号较多读起来吃力
- 价值: ⭐⭐⭐⭐ 对 GRPO 训练稳定性的系统性改进，具有即插即用的实用价值
