# PA³: Policy-Aware Agent Alignment through Chain-of-Thought

**日期**: 2026-03-15  
**arXiv**: [2603.14602](https://arxiv.org/abs/2603.14602)  
**领域**: LLM推理 / LLM Agent  
**关键词**: policy alignment, chain-of-thought, GRPO, business rules, conversational agent

## 一句话总结
提出 PA³ 多阶段对齐方法训练 LLM agent 在 CoT 推理中自行回忆和应用业务策略（无需全部策略放入上下文），引入 PolicyRecall reward (Jaccard score) 和 Hallucination Penalty 用于 GRPO 训练，比基线提升 16 分，比同规模方法高 3 分且少用 40% token。

## 研究背景与动机

1. **领域现状**: LLM agent 在工具调用上表现出色但难以遵守复杂业务规则。现有方案是将所有策略放入上下文。

2. **现有痛点**: 将全部策略放入上下文导致延迟高、needle-in-haystack 问题降低性能。对话中不同阶段需要不同策略子集，全量推送造成干扰。

3. **核心 idea**: 不在上下文中提供全部策略，而是训练模型在 CoT 推理时自行"回忆"相关策略并正确应用——类似人类客服内化业务知识后无需查手册。

## 方法详解

### 整体框架
多阶段训练：(1) SFT 习得策略回忆+应用的基本模式 → (2) GRPO 强化学习用 PolicyRecall + Hallucination Penalty 优化回忆准确性和减少幻觉。

### 关键设计

1. **PolicyRecall Reward**:
   - 做什么：评估模型是否在 CoT 中回忆了正确的策略规则
   - 核心思路：用 Jaccard similarity 衡量模型 CoT 中提及的策略集合与 ground truth 之间的重叠
   - 设计动机：直接奖励策略回忆而非仅奖励最终回答正确

2. **Hallucination Penalty**:
   - 做什么：惩罚模型在 CoT 中编造不存在的策略
   - 核心思路：检测 CoT 中引用的策略是否在策略库中存在
   - 设计动机：防止模型为了获得高 recall 而胡编策略

3. **多阶段训练**:
   - SFT 阶段：用标注的策略回忆 + 应用 CoT 样本训练基本模式
   - GRPO 阶段：用 PolicyRecall + Hallucination Penalty 的组合奖励做在线强化学习

## 实验关键数据

### 主实验

| 方法 | 得分 | Token 消耗 | 说明 |
|------|------|-----------|------|
| 基线 (无策略) | 基线 | 1× | 模型无策略知识 |
| In-context (全量策略) | +13 | **1.4×** | 所有策略放入上下文 |
| **PA³ (SFT + GRPO)** | **+16** | **1×** | 策略内化，无需上下文 |

### 消融实验

| 配置 | 得分变化 | 说明 |
|------|---------|------|
| SFT only | +12 | 习得回忆模式但不精确 |
| + PolicyRecall reward | +14 | Jaccard 奖励提升回忆准确性 |
| + Hallucination Penalty | **+16** | 抑制编造不存在的策略 |
| w/o CoT (直接回答) | +8 | CoT 推理是关键 |

### 关键发现
- PA³ 比 in-context 高 **3 分**且少用 **40% token**——策略内化同时提升质量和效率
- PolicyRecall (Jaccard score) 比纯 outcome reward 额外 +2 分——直接奖励中间推理有效
- Hallucination Penalty 额外 +2 分——LLM 在 GRPO 中倾向编造策略获高 recall
- CoT 是核心: 去掉 CoT 只有 +8 分——必须在推理链中显式回忆策略

## 亮点与洞察
- **从外部检索到内在回忆的范式转变**: 模型"内化"策略而非每次检索，类似人类客服内化业务知识
- **PolicyRecall reward 直接优化 CoT 质量**: 解决了策略遵循中的 credit assignment 问题
- **Hallucination Penalty 针对 GRPO 的 reward hacking**: 编造策略是 policy alignment 特有 failure mode
- **40% token 节省**: 大规模客服系统中 = 显著成本和延迟降低

## 局限性 / 可改进方向
- 策略库规模有限时效果好，数千条策略的规模效应待测
- PolicyRecall ground truth 需人工标注，标注成本高
- 仅在客服场景验证，法律/医疗等策略密集场景待测
- 策略更新后需重训，增量学习策略值得探索

## 相关工作与启发
- **vs RAG-based policy retrieval**: 受限于上下文长度和检索准确性
- **vs 直接 SFT**: SFT 只教模式不教质量，无 RL 阶段优化

## 评分
- 新颖性: ⭐⭐⭐⭐ PolicyRecall reward + Hallucination Penalty 有新意
- 实验充分度: ⭐⭐⭐⭐ 主实验 + 消融 + 真实企业场景验证
- 写作质量: ⭐⭐⭐⭐ 动机和方法逻辑清晰
- 价值: ⭐⭐⭐⭐ 企业级 agent 对齐需求明确，有商业价值
