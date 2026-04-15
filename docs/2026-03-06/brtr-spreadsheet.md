# Beyond Rows to Reasoning: Agentic Retrieval for Multimodal Spreadsheet Understanding

**日期**: 2026-03-06  
**arXiv**: [2603.06503](https://arxiv.org/abs/2603.06503)  
**代码**: 无  
**领域**: 多模态/VLM  
**关键词**: spreadsheet understanding, agentic RAG, tool-calling, multimodal retrieval, enterprise QA

## 一句话总结
提出 BRTR，一个多模态 agentic RAG 框架，用迭代工具调用循环替代单次检索，结合 planner-executor 架构，在企业级电子表格理解任务上比单次检索方法提升 25 个百分点（FRTR-Bench 达 99% 准确率）。

## 研究背景与动机

1. **领域现状**：企业级电子表格包含数百万单元格、跨 sheet 依赖和嵌入的可视化。现有方法分两类：压缩方法（SpreadsheetLLM）将 worksheet 压缩到 LLM 上下文窗口内；检索方法（FRTR）对内容分块做语义检索。两者都是单次检索。

2. **现有痛点**：(a) 单次检索可能遗漏关键上下文——真实分析师会跨 sheet 交叉引用、跟踪单元格依赖、逐步收集证据；(b) 压缩方法丢失数据精度；(c) 全量注入超出上下文窗口。

3. **核心矛盾**：电子表格分析是一个天然需要多步推理的过程（先查列名→找到数据→跨表对比→计算），但现有系统只能"一锤子买卖"式检索。

4. **切入角度**：参照 ReAct 范式，让 LLM 像真实分析师一样迭代查询、检查结果、精炼搜索。

5. **核心 idea**：用 agentic tool-calling loop 替代单次检索，配合 planner-executor 架构处理复杂多步企业工作流。

## 方法详解

### 整体框架
电子表格 → 多模态索引（行/列/窗口/图像 chunk + NVIDIA NeMo 1B 嵌入）→ 混合检索（dense + BM25 + RRF 融合）→ Agentic Loop（LLM 调用 5 种搜索工具，最多 50 轮迭代）→ Planner 分解为 DAG 子任务 → 6 种 Executor（Excel/IO/Web/Validation/OCR/Search）并行执行 → 综合输出。

### 关键设计

1. **多模态索引与混合检索**:
    - 做什么：将电子表格分为行/列/矩形窗口/嵌入图像四种 chunk，混合语义+词汇检索
    - 核心思路：RRF 融合 $\text{score}(c,q) = \sum_{r} \frac{1}{k + \text{rank}_r(c,q)}$，$k=60$，top-10 chunks 作为初始上下文
    - 设计动机：电子表格中精确数值和单元格引用需要词汇匹配（BM25），而语义查询需要 dense retrieval，两者互补

2. **Agentic 迭代工具调用**:
    - 做什么：LLM 通过 5 种搜索工具（search_rows/columns/windows/images/all）迭代获取证据
    - 核心思路：初始检索后 LLM 判断证据是否充分→不充分则精炼查询/换检索类型/加坐标过滤→最多 50 轮迭代（实际平均 3-6 轮）
    - 设计动机：模拟真实分析师的工作流——先看总表，发现需要看明细，再查特定行列。上下文管理用 always-prune 策略避免 token 溢出

3. **Planner-Executor 架构**:
    - 做什么：将复杂工作流分解为依赖图，并行调度独立子任务
    - 核心思路：Planner 生成子任务 DAG → 独立分支并发执行 → 完成结果注入下游依赖 → 最终综合
    - 设计动机：长 horizon 的组合任务（计算+格式化+可视化+跨文件验证）在单线程 agent 中会累积误差

### 嵌入模型评估
系统比较了 5 种多模态嵌入模型，NVIDIA NeMo Retriever 1B 在 Recall@10 (0.60) 和 nDCG@10 (0.42) 均最优。

## 实验关键数据

### 主实验（FRTR-Bench, 159 queries）

| 模型 | BRTR | FRTR (单次) | SpreadsheetLLM | 提升 |
|------|:---:|:---:|:---:|------|
| GPT-5 | **0.99** | 0.73 | 0.18 | +26pp |
| Gemini 3 Pro | **0.99** | 0.68 | 0.29 | +31pp |
| Claude Opus 4.6 | **0.98** | 0.74 | 0.34 | +24pp |
| GPT-5.2 | **0.98** | 0.72 | 0.32 | +26pp |

### 消融实验

| 配置 | 关键指标 | 说明 |
|------|---------|------|
| BRTR 完整 | 99% | 迭代检索+规划 |
| 无 Planner | - | 复杂多步任务退化 |
| 无迭代（单次检索） | 73% | FRTR baseline |
| 无搜索工具 | - | 仅靠上下文 |

### 关键发现
- BRTR 在 FRTR-Bench 上达到 99%，超过单次检索 25pp，超过 SpreadsheetLLM 81pp
- 平均只需 3-6 次工具调用即可收敛，远低于 50 次上限
- GPT-5.2 在效率-准确率 trade-off 上最优（20K tokens, 91s, 98% accuracy）
- Claude Opus 4.6 token 消耗最高（462K），说明模型检索策略差异巨大
- FINCH benchmark 上超过已有方法 32pp

## 亮点与洞察
- **迭代检索的收益远超预期**：从 73% 到 99%，证明"多次查找"对电子表格理解是变革性的（类比人类分析师不可能一次扫完百万单元格）
- **always-prune 的上下文管理策略**：丢弃旧图像但保留文字描述——简单有效地控制 token 增长，保留推理记忆
- **NVIDIA NeMo 1B 在混合表格+视觉数据上优于其他嵌入模型**：对实际 RAG 系统选型有直接参考价值

## 局限性 / 可改进方向
- 强依赖 frontier LLM 的 function-calling 能力，小模型（GPT-4o: 67%）效果大幅下降
- 只评估了英文电子表格，多语言/多格式泛化未验证
- 迭代检索增加延迟（GPT-5: 166s/query），对实时场景不友好
- 200+ 小时人工评估成本高昂，可复现性受限

## 相关工作与启发
- **vs FRTR**: BRTR 在 FRTR 的分块检索基础上加入 agentic loop，从 73% → 99%
- **vs SpreadsheetLLM**: 压缩方法在复杂查询上效果极差（18-34%），说明信息丢失是致命的
- **vs SheetAgent/TableMind**: 代码执行型 agent 容易陷入死循环，BRTR 用结构化搜索工具避免此问题

## 评分
- 新颖性: ⭐⭐⭐⭐ agentic RAG 思路不新但在电子表格领域是首次系统实践
- 实验充分度: ⭐⭐⭐⭐⭐ 3 个 benchmark + 9 个 LLM + 5 个嵌入模型 + 200h 人工评估
- 写作质量: ⭐⭐⭐⭐ 结构清晰，系统全面
- 价值: ⭐⭐⭐⭐⭐ 对企业级文档 QA 系统有直接工程参考价值
