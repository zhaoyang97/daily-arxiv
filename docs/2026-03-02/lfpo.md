# LFPO: Likelihood-Free Policy Optimization for Masked Diffusion Models

**日期**: 2026-03-02  
**arXiv**: [2603.01563](https://arxiv.org/abs/2603.01563)  
**代码**: 无  
**领域**: LLM推理 / 扩散语言模型  
**关键词**: diffusion LLM, RLVR, likelihood-free, flow matching, masked diffusion

## 一句话总结

LFPO 提出面向 Masked Diffusion 语言模型（dLLM）的原生对齐框架：将 flow matching 的向量场概念映射到离散 token 空间，绕过不可解的似然计算，通过对比更新直接优化去噪 logits，在代码和推理任务上超越 SOTA，同时通过中间步一致性约束将推理加速约 20%。

## 研究背景与动机

1. **领域现状**：Diffusion LLM（如 LLaDA、Dream）作为自回归的替代方案快速崛起，通过并行去噪实现高效生成。RLVR（Reinforcement Learning with Verifiable Rewards）已在自回归 LLM 上大获成功（数学推理、代码生成的准确性显著提升）。
2. **现有痛点 — 似然不可解**：RLVR 的核心是 policy gradient，需要计算模型的似然 $\log p_\theta(y|x)$。对自回归模型这很简单（token 概率连乘），但对 dLLM，精确似然需要 Evidence Lower Bound（ELBO），涉及所有扩散步和所有位置的边缘化，计算上不可行。现有方法（如 dDPO）不得不用高方差近似，效果不稳定。
3. **核心矛盾**：dLLM 的对齐需要奖励信号指导优化，但经典 RL 方法都依赖似然，而 dLLM 的似然天然不可解
4. **切入角度**：不执着于估计似然，而是直接在 logit 空间做优化。借鉴连续扩散中 flow matching 的"速度场矫正"概念，设计无似然的策略更新规则
5. **核心 idea**：**绕过似然计算，将对齐问题重新formulate为"几何速度矫正"——对好/坏样本的去噪 logits 做对比更新，直接拉直概率流（straighten probability flow），同时实现质量提升和加速推理**

## 方法详解

### 整体框架

给定 dLLM（如 LLaDA），从 masked input 去噪生成回答 → 用 verifiable reward 评估正确性 → LFPO 对比正确/错误样本的去噪 logits，更新模型参数使去噪方向偏向正确答案。同时约束中间步预测与最终答案的一致性（straighten flow）。

### 关键设计

1. **离散速度场映射（Discrete Flow Matching）**
   - 做什么：将连续扩散中的向量场概念映射到离散 token 空间
   - 核心思路：在连续空间中，flow matching 学习将噪声映射到数据的速度场 $v_\theta(x_t, t)$。在离散空间中，"速度"变成了去噪 logits：每个位置在每个时间步的预测分布。LFPO 定义离散版本的速度场为 $f_\theta(x_t, t) = \text{logits}$ 指示预测方向
   - 设计动机：将连续世界的几何直觉（速度、流、拉直）引入离散世界，绕过似然瓶颈

2. **对比 Logit 更新（Contrastive Velocity Rectification）**
   - 做什么：通过对比正确/错误样本直接优化去噪 logits
   - 核心思路：采样多个回答，用 verifiable reward 区分正确（$y^+$）和错误（$y^-$）。损失函数形如 $\mathcal{L} = -\log \sigma(f_\theta(y^+) - f_\theta(y^-))$，直接拉大好/坏样本在 logit 空间的距离
   - 设计动机：对比学习不需要显式的似然计算，只需要相对偏好——完美匹配 verifiable reward 的二元信号

3. **流拉直约束（Probability Flow Straightening）**
   - 做什么：约束中间扩散步的预测与最终答案一致
   - 核心思路：从中间步 $x_t$ 直接预测最终 $x_0$，鼓励预测轨迹"一步到位"而非绕弯。$\mathcal{L}_{\text{straight}} = \|f_\theta(x_t) - x_0\|$ 约束中间步预测直指终点
   - 设计动机：拉直后的流可以用更少的步数达到同样质量，实现推理加速（~20% 步数减少）

### 训练策略
- 从预训练 dLLM 开始，交替：(1) 采样回答 → 计算奖励 → 对比更新；(2) 构造中间步 → 流拉直约束
- 奖励可以是数学答案的正确性验证或代码的测试通过率

## 实验关键数据

### 主实验

| 方法 | 代码 (HumanEval) | 数学 (GSM8K/Math) | 推理速度 |
|------|-----------------|-------------------|---------|
| LLaDA-8B (base) | 基准 | 基准 | 基准 |
| dDPO (似然近似) | +小幅 | +小幅 | 不变 |
| dRLHF (ELBO 近似) | +中等 | +中等 | 不变 |
| **LFPO** | **最优** | **最优** | **~20% 加速** |

### 消融实验

| 配置 | 效果 | 说明 |
|------|------|------|
| LFPO 无流拉直 | 质量好但速度无提升 | 拉直是加速的关键 |
| LFPO 无对比（只做拉直）| 速度快但质量差 | 对比更新是准确率的关键 |
| 用似然近似代替对比 | 降低 2-5% | 似然近似方差大，不如对比稳定 |
| 完整 LFPO | 最优 | 对比+拉直互补 |

### 关键发现
- 似然近似方法（dDPO、dRLHF）在 dLLM 上效果不稳定，因为 ELBO 近似的方差随序列长度增加
- LFPO 的对比更新完全避免了似然估计，梯度更精确，训练更稳定
- 流拉直直接带来推理加速——减少 20% 扩散步数而不损失质量
- 两个组件互补：对比更新提升质量，流拉直提升速度

## 亮点与洞察
- **绕过"不可能"的技术路径**：不是更好地近似似然，而是重新定义优化目标，直接在 logit 空间做优化——思路非常优雅
- **质量+速度双收**：通常 alignment 会增加推理成本，但 LFPO 通过流拉直同时加速推理，一石二鸟
- **连续到离散的概念迁移**：将 flow matching 的几何直觉（速度场、流拉直）系统地迁移到离散 token 空间

## 局限性 / 可改进方向
- 只在 dLLM 上验证（LLaDA/Dream），是否适用于其他非自回归模型待探索
- 流拉直假设存在最优的"直线路径"，对于多模答案分布可能不成立
- 训练仍需采样大量正负样本对，计算成本不低
- 20% 的加速虽好，但 dLLM 本身的推理成本仍高于自回归

## 相关工作与启发
- **vs dDPO/dRLHF**: 这些方法直接搬运自回归 RL 的框架到 dLLM，被似然不可解卡住。LFPO 从根本上回避了这个问题
- **vs Flow Matching**: LFPO 是 flow matching 在离散空间的创新应用，将连续领域的理论工具适配到 dLLM
- **vs GRPO（自回归RL）**: GRPO 用组相对奖励优化自回归模型，LFPO 是 dLLM 的对应方案

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 离散flow matching + 无似然策略优化是全新的formulation
- 实验充分度: ⭐⭐⭐⭐ 代码+数学两大任务 + 消融 + 加速验证
- 写作质量: ⭐⭐⭐⭐ 连续→离散的类比讲得清楚
- 价值: ⭐⭐⭐⭐⭐ 为 dLLM 的对齐提供了实用且理论扎实的方案，解决了核心瓶颈
