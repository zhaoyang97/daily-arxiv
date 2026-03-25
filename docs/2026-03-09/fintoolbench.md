# FinToolBench: Evaluating LLM Agents for Real-World Financial Tool Use

**日期**: 2026-03-09  
**arXiv**: [2603.08262](https://arxiv.org/abs/2603.08262)  
**代码**: 即将开源（tool manifest + 执行环境 + 评估代码）  
**领域**: LLM Agent  
**关键词**: financial benchmark, tool use, LLM agent, compliance evaluation, trustworthy AI

## 一句话总结
构建首个可执行的金融工具使用 benchmark FinToolBench（760 个真实金融 API + 295 条工具依赖查询），提出超越二元执行成功的评估维度——时效性/意图约束/监管域对齐三个合规指标，以及 FATR 金融感知工具检索 baseline。

## 研究背景与动机

1. **领域现状**: LLM agent 被越来越多地部署为金融数据的接口，将自然语言请求转化为 API 调用序列。通用工具 benchmark（API-Bank、StableToolBench）评估 API 调用正确性，但不考虑金融特有约束。

2. **现有痛点**: (a) 金融 benchmark 主要聚焦静态文本分析/文档 QA，不涉及工具执行；(b) 通用工具 benchmark 缺少金融领域特有的严格性——数据时效性、合规约束、快速波动性；(c) 评估只看"是否执行成功"忽视了三个关键失败模式：**过时数据**（问"当前"汇率却返回日快照）、**意图升级**（信息查询被升级为交易操作）、**域不匹配**（股票 API 回答加密货币问题）。

3. **核心 idea**: 评估金融 agent 不仅要看能力（是否调用成功）还要看合规（调用链是否在金融约束下可接受），提出 call-level compliance mismatch rates。

## 方法详解

### 整体框架
8 阶段构建流水线：原始工具收集 → 可执行性过滤 → 统一 manifest 标准化 → 金融属性标注 → 问题生成/筛选 → 工具-问题对齐 → 人工质检 → 最终 benchmark。

### 关键设计

1. **760 工具库**:
   - 来源：RapidAPI（第三方市场 API）+ AkShare（开源 Python 金融库）
   - 从 5470 个候选接口过滤到 760 个可用工具
   - 每个工具规范化为统一 manifest（稳定 ID + 描述 + 标准化签名 + 参数类型 + 对齐输出 schema）

2. **金融属性标注**:
   - **update_frequency**: realtime / daily / as_filed / periodic / static → 评估时效性
   - **intent_type**: informational / advisory / transactional → 评估意图约束
   - **regulatory_domain**: 集合值域（股票/加密/外汇等）→ 评估监管域对齐
   - 在 tool manifest 中为每个 API 标注这三个属性

3. **三维合规评估指标**:
   - **TMR (Timeliness Mismatch Rate)**: 时效性不匹配率，如用 daily 数据回答需要 realtime 的查询
   - **IMR (Intent Mismatch Rate)**: 意图升级率，如信息查询调用了交易 API
   - **DMR (Domain Mismatch Rate)**: 域不匹配率，如用股票工具回答加密货币问题
   - 从完整工具执行 trace 中计算

4. **FATR Baseline（Finance-Aware Tool Retrieval）**:
   - 检索小候选集 + 注入金融属性到 tool card + 缓存/重试/输出压缩稳定执行
   - 轻量级，为未来研究提供参考基线

### 评估协议
- 295 条问题（166 单工具 + 129 多工具）
- 每次运行产生审计级工具 trace（step/tool_name/parameters/output/error）
- LLM-as-judge 重复评分 + capability/compliance 分离

## 实验关键数据

### 主实验（不同 LLM 的能力+合规评估）

| 模型 | 调用成功率 | 执行成功率 | TMR ↓ | IMR ↓ | DMR ↓ |
|------|-----------|-----------|-------|-------|-------|
| GPT-4o | 82.3% | 71.5% | 18.2% | 5.1% | 12.4% |
| Claude-3.5 | 79.8% | 68.9% | 20.5% | 6.3% | 14.7% |
| GPT-4o + FATR | **85.7%** | **76.2%** | **12.1%** | **3.2%** | **8.5%** |

### 消融实验

| 配置 | 执行成功率 | TMR |
|------|-----------|-----|
| 无金融属性注入 | 71.5% | 18.2% |
| + 金融属性注入 | 74.8% | 14.3% |
| + 缓存/重试 | **76.2%** | **12.1%** |

### 关键发现
- 所有模型的 TMR 都很高（~20%），说明时效性是最容易犯的金融错误
- FATR 的金融属性注入有效降低了合规违规率
- 多工具查询的合规问题比单工具严重得多
- 即使执行成功的 trace 也可能在合规维度上有问题

## 亮点与洞察
- **"能力 vs 合规"分离评估**: 金融领域核心贡献——执行成功不等于可信
- **审计级 trace 设计**: 每次 API 调用都可追溯，对金融监管至关重要
- **三个金融专属 mismatch rate**: TMR/IMR/DMR 精准刻画了金融 agent 的三类典型失败
- **真实 API + 实际执行**: 不是 mock 环境，涉及真实的 rate limit、数据波动、API 不稳定

## 局限性 / 可改进方向
- 仅使用免费层 API，覆盖面有限（高级金融数据通常付费，如 Bloomberg/Reuters 终端数据）
- 295 条问题规模偏小，多工具链路长度有限，未涉及 5+ 步长链调用
- 合规指标依赖预标注的金融属性，标注质量影响评估准确性
- 未涉及安全性测试（如恶意交易指令的检测和拒绝）
- 缺少中文金融 API 和 A 股市场工具的覆盖

## 相关工作与启发
- **vs StableToolBench**: 通用工具 benchmark，不含金融合规维度。StableToolBench 关注 API 调用正确性和稳定性，但不区分“执行成功”和“合规可接受”
- **vs FinanceBench/FinQA/TAT-QA**: 金融 QA benchmark，但是静态文档问答，不涉及工具执行，无法评估工具调用链的合规性
- **vs AgentBench/WebArena/GAIA**: 通用 agent benchmark，缺少金融领域特定约束。它们评估通用规划和工具使用能力，但不考虑时效性/意图约束/监管域等金融专属约束
- **vs Finance Agent Benchmark**: 最近的工作，但未发布标准化工具库也未定义 call-level 合规指标

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首个可执行的金融工具 benchmark + 合规评估框架
- 实验充分度: ⭐⭐⭐⭐ 多模型对比 + FATR baseline + 合规分析
- 写作质量: ⭐⭐⭐⭐ 问题定义清晰，pipeline 详尽
- 价值: ⭐⭐⭐⭐⭐ 对金融 AI agent 的信任和审计至关重要
