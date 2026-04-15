# KG-Hopper: Empowering Compact Open LLMs with Knowledge Graph Reasoning via Reinforcement Learning

**日期**: 2026-03-22  
**arXiv**: [2603.21440](https://arxiv.org/abs/2603.21440)  
**代码**: [GitHub](https://github.com/Wangshuaiia/KG-Hopper)  
**领域**: LLM推理  
**关键词**: knowledge graph, KBQA, reinforcement learning, multi-hop reasoning, tool use

## 一句话总结
提出 KG-Hopper，用强化学习训练 7B LLM 在单轮推理中完成多跳知识图谱问答——将整个 KG 遍历和推理过程嵌入模型的 "thinking" 阶段，在 8 个 KBQA benchmark 上超越 70B 多步方法并接近 GPT-4o-mini。

## 研究背景与动机

1. **领域现状**: KBQA（基于知识图谱的问答）通常需要多跳推理——从主题实体出发在 KG 中逐跳遍历才能找到答案。现有方法大多采用"多步流水线"策略，每一步独立调用 LLM 做一次推理。

2. **现有痛点**: (a) 多步流水线灵活性差——遵循预定义路径，遇到 KG 不完整或走错路时难以回溯；(b) 错误级联——前一步选错实体会直接污染后续所有步骤；(c) 每步独立推理忽略了跨步骤依赖关系。

3. **核心矛盾**: 多步推理的"逐步独立"假设与多跳问答需要"全局一致"推理之间的矛盾。如果缺失某个中间实体（如 "Yellow Hibiscus"），多步 beam search 会误入歧途且无法纠正。

4. **切入角度**: Reasoning LLM（如 DeepSeek-R1）的 "thinking" 阶段允许模型在生成答案前进行自我修正——后面的 token 可以修正前面的推理。这种机制天然适配多跳 KBQA 的回溯需求。

5. **核心 idea**: 把整个多跳 KG 遍历过程压缩到单轮 LLM 推理的 thinking 阶段中，用 RL 训练模型自主调用 KG 检索工具、动态探索路径、支持回溯。

## 方法详解

### 整体框架
输入自然语言问题 + 主题实体 → LLM 在 `<think>` 阶段自主反复调用 KG 检索工具（`<search>entity</search>` → `<searched_triples>...`）→ 综合所有检索信息在 `<answer>` 中输出最终答案。全程单轮推理，无需多步编排。

### 关键设计

1. **KG 检索工具**:
    - 两阶段检索：先查实体的所有 predicate，再根据问题语义选择最相关的 predicate 获取尾实体
    - 模型通过生成 `<search>entity</search>` 特殊 token 自动触发工具调用
    - 检索结果以 `<searched_triples>` 标签注入上下文，模型可基于此继续推理

2. **Cold Start SFT**:
    - 用强 LLM few-shot 生成 500 条高质量 CoT 示例（含正确的工具调用格式和推理链）
    - 对基座 LLM 做 SFT 学习基本的工具调用模式和输出格式
    - 训练时 mask 掉 `<triples>` 内的检索内容，防止模型记忆 KG 事实而非学推理策略

3. **四分量复合奖励函数**:
    - $R_{search} = \min(0.5 \cdot n, 0.8)$：鼓励使用 KG 工具但设上限防止滥用
    - $R_{format}$：检查 `<think>/<search>/<answer>` 格式是否正确（0.5 or 0）
    - $R_{reason}$：用外部 LLM (Llama-3.3-70B) 评估推理过程质量，分数 ∈ (0,1)
    - $R_{answer}$：用 LLM 判断预测答案是否语义匹配 ground truth（0 or 1）
    - 总奖励 $R_{final} = R_{search} + R_{format} + R_{reason} + R_{answer}$

4. **GRPO 优化 + History Resampling**:
    - 用 Group Relative Policy Optimization 训练，每个问题采样 16 个 rollout
    - 从第 2 个 epoch 开始移除简单的单跳问题（课程学习），让模型专注多跳推理
    - Mask 检索三元组 token 在 loss 计算中的贡献

## 实验关键数据

### 主实验（Hits@1）

| 方法 | CWQ | WebQSP | WebQ | GrailQA |
|------|-----|--------|------|---------|
| GPT-4o (prompt only) | 41.2 | 51.1 | 36.1 | 36.9 |
| GPT-4o-mini + KG | 55.2 | 71.3 | 64.7 | 63.7 |
| ToG (LLaMA-70B) | 49.8 | 68.2 | — | — |
| **KG-Hopper (Qwen-7B)** | **57.8** | **73.5** | **67.2** | **74.8** |

### 消融实验

| 配置 | CWQ | WebQSP |
|------|-----|--------|
| Full KG-Hopper | 最优 | 最优 |
| w/o RL (仅 SFT) | 显著下降 | 下降 |
| w/o 检索奖励 | 下降（工具调用不足） | 下降 |
| w/o 推理奖励 | 下降（推理链质量差） | 下降 |
| w/o History Resampling | 下降（简单样本占主导） | 下降 |

### 关键发现
- 7B 模型通过 RL 训练后一致超越 70B 多步方法（ToG 等），证明"一轮全局推理"优于"多步局部推理"
- RL 比纯 SFT 带来 10-15% 的绝对提升，说明模仿学习不足以学会灵活的推理策略
- 推理奖励和检索奖励缺一不可——前者保证推理链质量，后者保证工具使用频率

## 亮点与洞察
- **单轮 vs 多步范式转换**: 把多跳推理从"多步编排"变成"单轮思考"，利用 Reasoning LLM 自带的自修正能力实现回溯，设计思路优雅
- **四分量奖励设计精细**: 检索、格式、推理、答案四个维度分别引导，避免 reward hacking
- **Mask 检索内容** 是个好 trick：防止模型在 RL 训练中走捷径记忆 KG 事实，迫使学习通用推理策略

## 局限性 / 可改进方向
- 需要 SPARQL 接口访问 KG，不适用于非结构化知识源
- 推理奖励依赖外部 70B LLM 评估，训练成本不低
- 仅在 Freebase + WikiData 上验证，对领域特定 KG（医学、金融）的泛化能力未知
- 单轮推理的上下文长度有上限，超长推理链可能受限

## 评分
- 新颖性: ⭐⭐⭐⭐ 将 RL + Reasoning LLM 应用到 KBQA 是自然但有效的组合
- 实验充分度: ⭐⭐⭐⭐⭐ 8 个 benchmark、多个基线对比、详细消融
- 价值: ⭐⭐⭐⭐ 7B 模型达到 GPT-4o-mini 水平有实用价值
