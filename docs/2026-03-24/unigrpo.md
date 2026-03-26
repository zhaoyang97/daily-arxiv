# UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation

**日期**: 2026-03-24  
**arXiv**: [2603.23500](https://arxiv.org/abs/2603.23500)  
**代码**: 无  
**领域**: 图像生成 / 强化学习 / 多模态统一模型  
**关键词**: GRPO, flow matching, reinforcement learning, interleaved generation, reasoning-driven T2I

## 一句话总结
提出 UniGRPO，将 "Prompt → 推理 → 生成图像" 的多模态交错生成建模为统一 MDP，用 GRPO 联合优化文本推理和 Flow Matching 图像生成策略，去掉 CFG + 用速度场 MSE 正则替代 latent KL，在 TA 和 GenEval 上取得 SOTA（0.8381 / 0.90）。

## 研究背景与动机

1. **领域现状**: 统一多模态模型（如 Bagel、Show-o、Transfusion）正在走向 "AR 建模文本 + Flow Matching 生成图像" 的架构范式，具备交错生成（interleaved generation）的潜力。

2. **现有痛点**: 现有工作要么只优化图像生成（FlowGRPO、ReFL），要么只优化推理文本（TextGRPO），缺少一个统一的 RL 框架来联合优化两个模态。分阶段训练（如先 ReFL 再 TextGRPO）也无法充分利用模态间的协同。

3. **核心矛盾**: 交错生成的关键优势在于利用 test-time compute 做迭代推理——先推理、再生图、再反思，但现有训练方案无法 end-to-end 地优化这个推理-生成链条。此外，CFG 在多轮多条件场景下的计算开销会指数膨胀，latent KL 正则在不同时间步的权重不一致容易被 reward hacking 利用。

4. **切入角度**: 从最小可行单元（单轮 Prompt→Thinking→Image）入手验证统一 RL 框架，而非直接跳到多轮交错生成。

5. **核心 idea**: 将多模态交错生成建模为单一 MDP，用 GRPO 同时优化文本 token 生成和 flow matching 去噪过程，共享 group-relative advantage。

## 方法详解

### 整体框架
输入一个生成 prompt $c$，模型先自回归生成推理链 $y$（文本 token），再用 flow matching 生成图像 $x_0$。整个过程被建模为一个 MDP：文本阶段每个 token 是一个 action，图像阶段每个去噪步是一个 action。只在图像完全生成后给一个稀疏终端奖励。对同一 prompt 采样 $G$ 个完整轨迹，计算 group-relative advantage，联合更新策略。

### 关键设计

1. **统一 MDP 建模**:
   - 做什么：将文本推理 + 图像生成统一为一个 MDP，状态空间在文本阶段是 $(c, y_{<k})$，图像阶段是 $(c, y, x_{t_k}, t_k)$
   - 核心思路：文本 action 是离散 token，图像 action 是连续去噪 latent，但共享同一个 advantage $\hat{A}_i$。总目标 $\mathcal{J} = \mathcal{J}_{\text{Text}} + \lambda \mathcal{J}_{\text{Flow}}$，$\lambda=1$
   - 设计动机：让推理文本直接被视觉奖励驱动优化——好的推理应该带来更好的图像

2. **去除 CFG（Classifier-Free Guidance）**:
   - 做什么：训练时完全不用 CFG，保持 rollout 是线性无分支的
   - 核心思路：标准 CFG 需要对每步做条件/无条件两次前向，多条件时更多。去掉 CFG 后通过 RL 奖励最大化把 prompt 对齐能力内化到策略权重里
   - 设计动机：多轮多条件生成时 CFG 计算开销会爆炸，且分支计算图让梯度估计变得复杂。实验证明去掉 CFG 训练、推理时再加 CFG 效果不降反升

3. **速度场 MSE 正则替代 latent KL**:
   - 做什么：用 $\|\mathbf{v}_\theta - \mathbf{v}_{\text{ref}}\|^2$ 替代标准的 latent KL penalty
   - 核心思路：标准 latent KL 等价于 $\frac{1}{\sigma_{t_k}^2}\|\Delta\mu\|^2$，在高噪声时间步惩罚极小、低噪声时间步惩罚极大，分布不均匀。直接用未加权的 MSE 在所有时间步均匀约束速度场
   - 设计动机：latent KL 的不均匀权重在某些时间步留下 "漏洞"，RL 优化器很容易利用这些漏洞做 reward hacking（表现为验证集 reward 先升后降、图像出现伪影）

4. **RatioNorm（来自 GRPO-Guard）**:
   - 做什么：标准化 importance ratio 的 log 分布，使其中心在 0 附近
   - 核心思路：diffusion/flow 模型中 importance ratio 天然左偏（均值 <1），标准 clipping 无法约束正方向的过大更新。RatioNorm 通过加入 mean drift 修正项来重新居中
   - 设计动机：防止过于自信的正更新导致 reward hacking

### 训练策略
- 基模型：Bagel（ByteDance），先做 SFT 再做 RL
- 奖励模型：基于 InternVL 微调的 text-image alignment 评分器（可微，以便与 ReFL 等 baseline 公平比较）
- FlowGRPO-Fast：只在连续时间窗口内用 SDE 采样并计算梯度，其余步走 ODE，大幅节省计算
- 分辨率 1024，$G$ 个 group 采样

## 实验关键数据

### 主实验

| 方法 | Thinking | TA Score | GenEval |
|------|----------|----------|---------|
| Bagel (原始) | ✗ | 0.6810 | 0.78 |
| SFT | ✗ | 0.7486 | 0.83 |
| SFT | ✓ | 0.7769 | 0.82 |
| ReFL | ✗ | 0.7786 | 0.85 |
| FlowGRPO | ✗ | 0.8112 | 0.88 |
| FlowGRPO | ✓ | 0.8208 | 0.86 |
| TextGRPO | ✓ | 0.8078 | 0.88 |
| **UniGRPO (Ours)** | **✓** | **0.8381** | **0.90** |

- UniGRPO 相比 FlowGRPO+Thinking 在 TA 上 +1.7%，GenEval +4%
- UniFPO（FPO 替代 FlowGRPO 的版本）训练崩溃，说明 GRPO 比 FPO 更稳定

### 消融实验

| 配置 | 效果 | 说明 |
|------|------|------|
| 有 CFG 训练 | 训练 reward 更高 | 但推理时加 CFG 后效果不优于无 CFG 训练 |
| 无 CFG 训练 | 验证效果相当或更好 | 计算量大幅减少，可扩展到多轮 |
| No KL | reward hacking | 验证 reward 先升后降，图像质量退化 |
| Latent KL | 训练不稳定 | 250 步出现网格伪影，被迫终止 |
| **Velocity MSE** | **最优** | 训练稳定、图像质量高 |

### 关键发现
- 联合优化 > 单模态优化 > 分阶段优化：UniGRPO > FlowGRPO ≈ TextGRPO > ReFL+TextGRPO
- 去掉 CFG 不会损害最终质量，反而让训练更高效、更容易扩展
- Velocity MSE 比 latent KL 稳定得多，latent KL 的时间步不均匀权重是 reward hacking 的根本原因
- Thinking 对 GenEval 的帮助不稳定（Bagel 的推理模块主要为知识推理训练），但 UniGRPO 能成功利用 thinking 链

## 亮点与洞察
- **统一 MDP 建模是关键抽象**：把文本推理和图像生成放进同一个 RL 循环，让推理过程直接被视觉奖励信号驱动，比分阶段训练效果好很多。这个框架可以直接推广到多轮交错生成
- **去 CFG 的洞察很实用**：CFG 在 RL 训练中不是必需的——RL 通过奖励最大化能内化 prompt alignment 能力。这对所有做 diffusion/flow RL 的工作都有参考价值
- **Velocity MSE vs Latent KL 的分析精到**：标准 KL 在 flow matching 中的时间步依赖权重 $1/\sigma^2$ 是不均匀正则的根源，直接用无权 MSE 更鲁棒。这个 trick 可迁移到所有 flow-based RL 工作

## 局限性 / 可改进方向
- 只验证了单轮生成（Prompt→Think→Image），多轮交错生成的效果未知
- 奖励模型是可微的 VLM 评分器，没有验证 GRPO 在黑盒/不可微奖励下的表现（虽然理论上兼容）
- 基模型 Bagel 的 thinking 能力有限，换一个推理更强的基模型可能有更大提升
- 稀疏终端奖励导致 credit assignment 困难——论文也提出了多模态 Process Reward Model 作为未来方向
- 缺少与其他统一模型（如 Emu3、VILA-U）的对比

## 相关工作与启发
- **vs FlowGRPO**: FlowGRPO 只优化图像生成，UniGRPO 把它扩展为联合优化文本+图像。关键改进是去 CFG + velocity MSE 替代 latent KL
- **vs ReFL**: ReFL 需要可微奖励 + 只优化图像生成单步，UniGRPO 用 GRPO 框架不需要可微奖励，且端到端优化推理+生成
- **vs DualGRPO/PromptRL（concurrent）**: 这些工作用分离的 LLM + diffusion 模型，不是真正的统一模型交错生成

## 评分
- 新颖性: ⭐⭐⭐⭐ 统一 MDP 建模 + 两个实用改进（去 CFG / velocity MSE），思路清晰但并非全新范式
- 实验充分度: ⭐⭐⭐⭐ 有主实验+两组消融，但只有两个 benchmark，缺少人类评估
- 写作质量: ⭐⭐⭐⭐⭐ 公式推导清晰，动机讲解到位，消融设计合理
- 价值: ⭐⭐⭐⭐ 为统一多模态模型的 RL post-training 建立了扎实的 baseline，去 CFG 和 velocity MSE trick 实用性强
