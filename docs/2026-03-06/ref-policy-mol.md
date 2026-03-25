# Reference-guided Policy Optimization for Molecular Optimization via LLM Reasoning

**日期**: 2026-03-06  
**arXiv**: [2603.05900](https://arxiv.org/abs/2603.05900)  
**代码**: [GitHub](https://github.com/tmlr-group/RePO)  
**领域**: 模型压缩  
**关键词**: Molecular Optimization, LLM Reasoning, Reinforcement Learning, GRPO, Policy Optimization

## 一句话总结
提出 RePO（Reference-guided Policy Optimization），在 LLM 分子优化任务中结合 GRPO 风格的奖励驱动探索与答案级别的参考分子引导，解决了 SFT 抑制推理探索和 RLVR 奖励稀疏的问题，在 TOMG-Bench 上成功率×相似度提升最高 17.4%。

## 研究背景与动机
1. **领域现状**: LLM 通过 SFT 和 RLVR（如 GRPO）在推理任务上取得了显著进步，但在科学任务（如分子优化）上的应用尚未充分探索。
2. **现有痛点**: 指令式分子优化面临"监督不匹配"问题——每个数据点仅提供单个参考分子（无推理轨迹）；SFT 抑制多步推理，GRPO 在竞争目标下奖励稀疏导致学习缓慢。
3. **核心矛盾**: 分子优化需同时满足目标属性提升和结构相似度约束，这两个目标互相竞争——更大的结构修改可能改善属性但降低相似度。
4. **切入角度**: 在不需要推理轨迹标注的条件下，结合奖励驱动的探索和参考分子的答案级别引导。
5. **核心idea一句话**: RePO 用 GRPO 更新驱动化学空间探索，同时用参考分子作为答案锚点减轻奖励稀疏并稳定训练。

## 方法详解
### 整体框架
给定查询 $q = (x, m_0)$（指令 + 输入分子），模型输出 $o = [t; \hat{m}]$（推理 token + 优化后分子）。RePO 在每次更新时采样候选分子，用可验证奖励评分，然后同时做三件事：RL 更新（探索）、参考引导（锚定）、KL 正则化（稳定）。

### 关键设计
1. **三观察揭示监督不匹配**:
   - Observation 3.1: GRPO 在竞争目标下趋于保守编辑（相似度高但成功率低）
   - Observation 3.2: Answer-only SFT 坍缩为短回答（无推理过程），相似度控制差
   - Observation 3.3: GRPO (SFT-init) 继承 SFT 的短回答风格，无法恢复多步推理

2. **RePO 目标函数**:
   $$\mathcal{J}_{\mathrm{RePO}}(\pi_\theta) = \mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G}\left(\underbrace{\text{clipped PPO}}_{\text{Exploration}} + \beta \underbrace{\log \pi_\theta(m_{\mathrm{ref}} | q, t_i)}_{\text{Reference guidance}} - \gamma \underbrace{\mathbb{D}_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})}_{\text{KL regularization}}\right)\right]$$
   - **探索项**：对所有 token（推理 + 答案）应用 GRPO 式 clipped 更新
   - **参考引导项**：以模型采样的推理前缀 $t_i$ 为上下文，增加参考分子 $m_{\text{ref}}$ 在答案位置的似然
   - **KL 正则项**：稳定更新

3. **奖励设计**:
   - 结构相似度奖励：Tanimoto 相似度 $r_{\text{struct}} = \frac{|FP(m) \cap FP(m_0)|}{|FP(m) \cup FP(m_0)|}$
   - 属性奖励：二值判断属性是否改善 $r_{\text{prop}} \in \{0, 1\}$
   - 总奖励 $r = r_{\text{prop}} + r_{\text{struct}}$

4. **关键设计洞察**:
   - 参考引导不模仿推理 token，只在答案层面锚定
   - 不同于 SFT 的 token 级模仿，允许多种有效推理路径
   - 早期训练时参考引导减少奖励稀疏，加速有意义的 RL 更新

### 损失函数 / 训练策略
- 基于 Qwen-2.5-3B Instruct 作为基础模型
- GRPO 采样 $G$ 个候选分子并计算组内相对优势
- 参考分子 $m_{\text{ref}}$ 经 RDKit 有效性检查
- 梯度仅在答案 token 上施加参考引导，推理 token 由 RL 更新

## 实验关键数据
### 主实验（TOMG-Bench 单目标优化）

| 任务 | 指标 | Base | SFT | GRPO | GRPO(SFT) | **RePO** |
|---|---|---|---|---|---|---|
| AddComponent | SR×Sim | 0.066 | 0.147 | 0.005 | 0.156 | **0.239** |
| SubComponent | SR×Sim | 0.046 | 0.264 | 0.052 | 0.299 | **0.344** |
| QED | SR×Sim | 0.130 | 0.207 | 0.123 | 0.192 | **0.236** |
| LogP | SR×Sim | 0.168 | 0.206 | **0.305** | 0.183 | 0.297 |
| MR | SR×Sim | 0.173 | 0.238 | 0.188 | 0.225 | **0.294** |

### 跨模型验证（Llama-3.1-8B Instruct）

| 任务 | Base SR×Sim | SFT SR×Sim | GRPO SR×Sim | **RePO SR×Sim** |
|---|---|---|---|---|
| LogP | 0.164 | 0.219 | 0.151 | **0.269** |
| QED | 0.115 | 0.150 | 0.093 | **0.190** |
| MR | 0.129 | 0.186 | 0.117 | **0.231** |

### 多目标优化（MuMOInstruct）

| 设定 | 任务 | SFT SR×Sim | GRPO SR×Sim | RePO SR×Sim |
|---|---|---|---|---|
| Seen instruction | BDP | 0.101 | **0.118** | 0.117 |
| Unseen instruction | BDP | 0.081 | 0.108 | **0.113** |
| Unseen instruction | BPQ | 0.104 | 0.107 | **0.144** |

### 关键发现
- RePO 在 6 个单目标任务中 4 个取得最优 SR×Sim
- GRPO 不加 SFT 初始化在结构任务上几乎完全失败（SR 低至 0.5%），暴露纯 RL 在化学空间中的探索困难
- RePO 在未见过的指令格式上也保持优势，泛化能力强
- 跨模型（Qwen-2.5-3B → Llama-3.1-8B）一致提升，方法通用性好

## 亮点与洞察
- **深入的诊断分析**（三个 Observation）清晰揭示了 SFT 和 GRPO 在科学任务上的根本局限
- 参考引导的设计精巧：保留推理过程作为上下文，仅在答案层面提供锚定信号
- 奖励设计简洁有效：结构相似度（连续）+ 属性改善（二值）
- 梯度分离策略（探索项作用于全部 token，引导项仅作用于答案 token）避免了推理过程被参考分子"绑架"

## 局限性 / 可改进方向
- 每个数据点仅一个参考分子，质量不一（论文在附录中讨论了参考分子有效性）
- 属性奖励是二值的（改善/未改善），没有度量改善幅度
- 当前仅在单轮优化中评估，MOLLEO 等多轮进化方法在某些指标上可能更优
- 化学空间的探索仍受限于 LLM 的分子表示能力（SMILES 格式）

## 相关工作与启发
- 与 GRPO（DeepSeek）的直接对比表明，RLVR 在科学推理中需要额外引导
- MOLLEO 使用 LLM 进化搜索，与 RePO 的单轮 RL 形成互补
- 可将 RePO 的参考引导思路推广到其他"仅有单一参考答案、无推理轨迹"的科学任务

## 评分
- ⭐⭐⭐⭐ 创新性：参考引导策略优化结合 GRPO 是新颖的训练范式，诊断分析深入
- ⭐⭐⭐⭐ 实验充分性：两个 benchmark + 跨模型 + 多目标 + 消融 + 机制分析
- ⭐⭐⭐ 实用性：目前限于分子优化这一较窄的应用场景
- ⭐⭐⭐⭐ 写作质量：三个 Observation 的诊断分析是论文的核心亮点，说服力强
