# LongVidSearch: An Agentic Benchmark for Multi-hop Evidence Retrieval Planning in Long Videos

**日期**: 2026-03-15  
**arXiv**: [2603.14468](https://arxiv.org/abs/2603.14468)  
**代码**: [LongVidSearch](https://github.com/yrywill/LongVidSearch)  
**领域**: 视频理解 / LLM Agent  
**关键词**: long video QA, multi-hop retrieval, agentic benchmark, tool use, retrieval planning

## 一句话总结
提出 LongVidSearch benchmark（3000 QA / 447 长视频 / 平均 26 分钟），通过 N-1 adversarial ablation 严格保证 multi-hop 检索的必要性，用统一 tool 接口评估 agent 的检索规划能力，GPT-5 最高准确率仅 42.43%，揭示 multi-hop retrieval planning 是当前最大瓶颈。

## 研究背景与动机

1. **领域现状**: 长视频 QA 越来越依赖 agent + tool use 架构来检索跨时间的证据片段。LVBench、MLVU 等 benchmark 扩展了视频长度和任务多样性，但仍采用静态一次性评估。

2. **现有痛点**: (a) **Necessity Gap**: 很多标注为"multi-hop"的问题实际上用单帧线索或语言先验就能回答（shortcut learning）；(b) **Interaction Gap**: 一次性协议无法评估 agent 的迭代搜索、子目标分解、自适应查询能力。

3. **核心矛盾**: 现有 benchmark 不区分"检索规划失败"和"答案生成失败"——如果给 gold evidence，模型都能回答正确，说明瓶颈在检索规划而非理解。

4. **切入角度**: 借鉴文本 QA 的 multi-hop 检索范式（HotpotQA、MuSiQue），在视频领域严格定义 Hop-k = 需要恰好 k 个不可缺少的证据片段。

5. **核心 idea**: (1) N-1 adversarial ablation check 保证每条 evidence 都必要；(2) 统一 tool 接口固定检索后端，隔离 agent 的规划能力。

## 方法详解

### 整体框架

数据构建：LoVR 长视频 → GPT-5.2 生成候选 QA → 语义泄漏审计 → 时间不连续性检查 → N-1 adversarial ablation → 视觉一致性验证 → 人工审计。评估：统一 tool 接口 + 三 judge 多数投票。

### 关键设计

1. **N-1 Adversarial Ablation Check**:
   - 做什么：严格保证 multi-hop question 中每条 evidence 都不可或缺
   - 核心思路：对 k-hop 问题，系统性遮掩每条证据（k 次），让 Verifier Agent 尝试回答。只有当所有 k 次遮掩都导致 agent 回答"INSUFFICIENT"时才保留该问题
   - 设计动机：45% 的逻辑上合法的候选被此步过滤掉，说明"伪 multi-hop"问题非常普遍。这是区别于现有 benchmark 的核心创新

2. **四类推理任务分类**:
   - Visual Tracking（实体+聚合）：跨时间追踪同一实体
   - State Mutation（实体+转变）：检测同一实体的状态变化
   - Causal Inference（叙事+转变）：因果链推理
   - Global Summary（叙事+聚合）：全局信息综合
   - 设计动机：从语义粒度（细粒度/粗粒度）× 推理范式（聚合/转变）两个维度正交划分

3. **统一 Tool 接口**:
   - `Search_Clips_In_Video(video_id, query, top_k)`: 文本查询检索片段
   - `Get_Clip_Detail(clip_id)`: 获取片段详细描述
   - `FINAL_ANSWER(answer, evidence_ids)`: 提交答案
   - 设计动机：固定检索后端，差异只来自 agent 的查询生成和规划能力

### 数据统计
- 3000 QA / 447 视频 / 平均 26 分钟
- 2-hop 61.3% / 3-hop 23.9% / 4-hop 14.8%
- 从 11,612 条原始生成经漏斗式过滤到 3000 条（~26% 通过率）

## 实验关键数据

### 主实验（General Accuracy）

| Agent Backbone | All | 2-hop | 3-hop | 4-hop |
|---------------|-----|-------|-------|-------|
| GPT-5 | **42.43** | — | — | — |
| Gemini 3 Pro | 30.97 | — | — | — |
| GPT-4o | 19.20 | — | — | — |
| Qwen3-VL-32B | 29.59 | — | — | — |
| Qwen2.5-VL-72B | 25.30 | — | — | — |

### Oracle 实验

| 条件 | Accuracy |
|------|----------|
| Agent retrieval | 42.43 (GPT-5) |
| Gold evidence clips | ~100% |

### 关键发现
- 最强模型 GPT-5 也只有 42.43% 准确率，远低于 50%——multi-hop retrieval planning 极难
- Gold evidence 实验几乎完美→ **瓶颈在检索规划而非答案生成**
- Hop 数增加 accuracy 显著下降：GPT-5 的 2-hop ~45% → 4-hop ~30%
- Causal Inference 最难（需要建立事件间因果桥梁），Visual Tracking 最容易（直接实体匹配）
- GPT-5 tool call 最多（9.62 per question），但也最准——更多检索尝试确实有帮助

## 亮点与洞察
- **N-1 Adversarial Ablation** 是金标准：过滤 45% 伪 multi-hop，确保 benchmark 质量远超现有
- **统一 tool 接口** 的实验设计巧妙：控制变量只在 agent planning 能力，消除了检索后端差异的干扰
- **Gold evidence oracle** 实验一锤定音：问题不在理解能力，而在检索规划
- **对 agentic AI 的评估启发**: 现有 agent 在多步规划上还很弱，即使最强的 GPT-5 也不到一半

## 局限性 / 可改进方向
- 评估依赖 LLM-as-judge（GPT-5/Gemini 3 Pro/GPT-4o），存在评估偏差
- 检索后端固定为文本查询→片段字幕匹配，未探索视觉检索（frame-level retrieval）
- 目前只评估了 VideoAgent-style 架构，缺少端到端 Video-LLM 的对比
- 数据源依赖 LoVR 的人工字幕质量

## 相关工作与启发
- **vs LVBench/MLVU**: 静态一次性评估 → LongVidSearch 要求迭代检索
- **vs HotpotQA**: 文本 multi-hop → LongVidSearch 将此范式迁移到视频
- **vs VideoAgent**: 评估框架而非 agent 设计，提供 controlled testbed

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ multi-hop necessity 验证 + 统一 tool 接口评估是 benchmark 设计的重要创新
- 实验充分度: ⭐⭐⭐⭐ 10 个模型 + oracle + cost 分析，但缺少非 agent 的端到端对比
- 写作质量: ⭐⭐⭐⭐⭐ 问题定义清晰，构建流程严谨
- 价值: ⭐⭐⭐⭐⭐ 填补了 agentic long video QA 评估的空白，对社区价值很高
