# AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents

**日期**: 2026-03-15  
**arXiv**: [2603.14465](https://arxiv.org/abs/2603.14465)  
**代码**: [AgentProcessBench](https://github.com/RUCBM/AgentProcessBench)  
**领域**: LLM Agent  
**关键词**: process reward model, step-level evaluation, tool-use agent, ternary labeling, error propagation

## 一句话总结
首个面向 tool-use agent 的步级有效性评估基准（1000 条轨迹 / 8509 步人工标注），采用三元标签 (+1/0/-1) 和误差传播规则，揭示弱模型因 early termination 导致虚高正确率、当前 LLM 难以区分 neutral 和 erroneous 动作。

## 研究背景与动机

1. **领域现状**: LLM agent 已能调用工具完成复杂任务，但 tool-use 与数学推理不同——错误步骤可能导致不可逆副作用（如误发邮件、删除文件），因此准确的步级验证至关重要。Process Reward Model (PRM) 是实现步级监督的核心机制。

2. **现有痛点**: 现有 PRM 基准（PRM800K、ProcessBench、PRMBench）几乎全部聚焦数学推理这类封闭域场景，错误模式主要是逻辑/计算错误。而 tool-use agent 面对的是开放环境——动态观测、模糊用户意图、策略约束，失败模式截然不同。

3. **核心矛盾**: 标准 agent 基准（GAIA、τ²-Bench）只报告端到端任务成功率，不提供步级信号。现有 agent reward 基准（AgentRewardBench）只做轨迹级 rubric 评估，缺乏逐步的绝对 effectiveness 标签。

4. **本文要解决什么？** 构建一个有人工标注的、步级的、面向 tool-use agent 的 PRM 评估基准。

5. **切入角度**: 引入三元标签 (+1 正确 / 0 中性/探索 / -1 错误)，并设计误差传播规则——一旦出现错误步，后续因果相关步均打 -1，避免级联错误的虚假 credit。

6. **核心 idea**: 构建 AgentProcessBench，包含来自 HotPotQA/GAIA/BFCL/τ²-Bench 的 1000 条轨迹，由 5 种模型生成，89.1% 标注者一致率。

## 方法详解

### 整体框架

任务定义：给定任务描述 $T$ 和交互轨迹 $X=(m_0,...,m_{n-1})$，对每个 assistant 步骤输出标签 $y_i \in \{-1, 0, +1\}$。评估两个互补指标：StepAcc（步级微平均准确率）和 FirstErrAcc（首错位置准确率）。

### 关键设计

1. **三元标签方案**:
   - +1 (正确有效): 推进任务的步骤，包括正确调用工具、引入有效约束、纠正之前错误
   - 0 (中性/探索): 合理但无显著推进的步骤，如遇到 404 错误、冗余复述、结果不确定
   - -1 (错误/有害): 误解 tool 输出、违反策略、重复失败动作
   - 设计动机: 区别于数学推理的二元对错，tool-use 天然存在大量"探索"行为（试错获取信息），需要 neutral 标签避免惩罚合理的信息搜集步骤

2. **误差传播规则 (Error Propagation Rule)**:
   - 做什么: 一旦某步为 -1，所有后续因果相关步均标为 -1，直到 agent 显式纠正错误或切换到独立子任务
   - 设计动机: 防止下游步骤获得虚假正 credit（如基于错误 API 结果做出的"正确"推理）
   - 保证长程轨迹标注的一致性，人工标注者间一致率 89.1%

3. **数据构建流程**:
   - 任务来源: HotPotQA (多跳推理)、GAIA (深度检索)、BFCL (工具调用)、τ²-Bench (长程对话)，均 200 条任务
   - 轨迹生成: 5 个模型 (Qwen3-4B-Instruct, Qwen3-30B-A3B, DeepSeek-V3.2, GPT-5-mini, GPT-5)
   - 标注: 每条轨迹两名专家独立标注，辅以 DeepSeek-V3.2/GPT-5.2/Claude 4.5 参考（但人工与参考一致率仅 66.9%-72.1%，说明人工保持了独立判断）

### 评估指标
- **StepAcc**: 步级标签的微平均准确率，长轨迹贡献更多步
- **FirstErrAcc**: 每条轨迹的首错位置准确率——更难，因为级联错误使根因定位比判断后续步更具挑战性

## 实验关键数据

### 主实验 (20 个 LLM 评估)

| 模型 | 平均 StepAcc | 平均 FirstErrAcc |
|------|-------------|-----------------|
| Gemini-3-Flash-Preview-Thinking | **81.6** | **65.8** |
| GPT-5.2-Chat | 74.8 | 61.1 |
| DeepSeek-V3.2-Thinking | 72.8 | 59.6 |
| Qwen3-30B-A3B-Thinking | 68.5 | 52.0 |
| Qwen3-8B-Thinking | 63.2 | 46.0 |
| LLaMA-3.1-8B-Instruct | 52.3 | 40.2 |

### Best-of-N 选择策略消融 (GAIA, N=8)

| Generator | Final (ORM) | % Pos (PRM) | Two-Stage |
|-----------|------------|-------------|-----------|
| DeepSeek-V3.2-Thinking | 56.6 | 54.7 | **64.2** |
| Qwen3-30B-Thinking | 35.9 | 49.1 | **50.9** |
| Gemini-3-Flash-Preview | 56.6 | 49.1 | **60.4** |

### 关键发现
- **弱模型虚高正确率**: Qwen3-4B 轨迹成功率最低但步级正确率不低——因为 fail-fast 行为减少了错误步积累
- **neutral 步最难判**: 混淆矩阵显示 0 标签的误分类率最高，大量被误判为 +1，因为 neutral 步的效用取决于后续上下文
- **Process + Outcome 互补**: Two-Stage (ORM→PRM) 在 GAIA 上比纯 ORM 高 7.6%（64.2 vs 56.6），而 oracle Pass@8 上限为 77.4%
- **任务越复杂，小模型退化越严重**: HotPotQA→GAIA，Qwen3-4B FirstErrAcc 暴跌 30%，而 Gemini 仅降 16.8%
- **thinking 模式显著提升**: Qwen3-8B thinking vs non-thinking: +6.1% StepAcc, +5.3% FirstErrAcc
- **不同数据集失败模式不同**: τ²-Bench 的首错多出现在后期步（策略违规），HotPotQA/GAIA 多在 Step 1（工具调用格式错误）

## 亮点与洞察
- **三元标签 + 误差传播规则**组合巧妙解决了 tool-use 场景独有的标注挑战：探索行为不应被惩罚，但级联错误必须被追踪
- **"弱模型虚高正确率"现象**的发现很有洞察——StepAcc 的局限推动了 FirstErrAcc 指标的设计
- **Process 作为 Outcome 的补充而非替代**: process-level 信号在 tie-breaking 场景最有效，这为 test-time scaling 提供了实用路径

## 局限性 / 可改进方向
- 仅评估 tool-use 场景，未覆盖纯推理、创意写作等其他 agent 任务类型
- 误差传播规则依赖人工判断因果关系，自动化级联错误检测是有价值的研究方向
- 缺乏用 AgentProcessBench 数据训练 PRM 的实验——目前只作为评估基准
- Oracle Pass@8 (77.4%) 与最佳实际策略 (64.2%) 差距大，说明 PRM 仍有很大提升空间

## 相关工作与启发
- **vs PRM800K / ProcessBench**: 仅限数学推理，封闭域，二元标签
- **vs AgentRewardBench**: 轨迹级 rubric = 缺乏步级粒度
- **vs Agent-RewardBench**: 多模态偏好对，但步级监督仅限规划阶段

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个 tool-use 步级基准 + 三元标签设计有创新
- 实验充分度: ⭐⭐⭐⭐⭐ 20 模型 × 4 子集 + Best-of-N 消融 + 数据集级别 failure mode 分析
- 写作质量: ⭐⭐⭐⭐ 结构清晰，motivation 推导完整
- 价值: ⭐⭐⭐⭐ 填补 agent PRM 评估空白，对 RLHF 和 test-time scaling 有直接指导
