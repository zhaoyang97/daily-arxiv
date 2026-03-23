# DocSage: An Information Structuring Agent for Multi-Doc Multi-Entity Question Answering

**日期**: 2026-03-12  
**arXiv**: [2603.11798](https://arxiv.org/abs/2603.11798)  
**代码**: 有  
**领域**: LLM Agent / 多文档QA  
**关键词**: multi-document QA, schema discovery, structured extraction, relational reasoning, agent

## 一句话总结
提出 DocSage，一个面向多文档多实体问答（MDMEQA）的端到端 Agent 框架——通过动态 Schema 发现（ASK 算法交互式推断查询特定的最小可连接模式）→ 逻辑感知的结构化抽取（CLEAR 机制跨记录逻辑一致性校验）→ Schema 引导的关系推理（SQL 驱动的精确事实定位和多跳推理），在两个 MDMEQA benchmark 上超越 SOTA 长上下文 LLM 和 RAG 系统 27%+。

## 研究背景与动机

1. **领域现状**: 多文档多实体问答要求模型追踪分散在多个文档中的隐式逻辑关系，是知识密集型 NLP 的核心任务。

2. **现有痛点**: (i) 标准 RAG 的向量相似度检索太粗粒度，遗漏关键事实；(ii) 图 RAG 难以高效整合复杂碎片化关系网络；(iii) 两者都缺乏 schema 感知——无法系统组织分散的实体和关系。

3. **核心 idea**: 将非结构化文档动态转化为 query 特定的结构化关系表，然后用 SQL 级精确推理替代 LLM 注意力在长文本中的稀释。

## 方法详解

### 整体框架
查询 + 文档集 → Module 1: Schema Discovery（ASK 算法）→ Module 2: Structured Extraction（CLEAR 校验）→ Module 3: Relational Reasoning（SQL 编译 + 证据回溯）→ 最终答案。

### 关键设计

1. **Interactive Schema Discovery（ASK 算法）**:
   - 做什么：动态推断查询特定的最小可连接 schema——表结构 + 实体 + 属性 + 关系
   - 核心思路：初始 schema 假设 → 一致性分析发现三类不确定性（实体对齐冲突/属性值异常/关系缺失）→ 生成澄清问题做针对性检索 → 迭代更新 schema 直到收敛
   - 设计动机：MDMEQA 中 schema 不预定义，需要从查询和文档中自动发现

2. **Logic-Aware Structured Extraction（CLEAR 机制）**:
   - 做什么：将非结构化文本填充到 schema 中生成关系表，同时保证抽取质量
   - 两级校验：Level A 单点置信度（LoRA 适配 + 保形预测阈值）；Level B 跨记录逻辑一致性（函数依赖/时间约束/数值范围/外键完整性）
   - 低置信或逻辑违反的元组触发纠正工作流（更强 LLM 重抽取或回溯检索）

3. **Schema-Guided Relational Reasoning**:
   - 做什么：将自然语言查询编译为优化的 SQL 查询，在构建好的关系数据库上执行
   - Schema 显式的连接键和关系定义使编译器能生成高效的 join 查询
   - 自动追溯每行结果到原始文档位置，保证答案可验证

## 实验关键数据

### 主实验（MEBench）

| 方法 | Comparison | Statistics | Relationship | Overall |
|------|-----------|-----------|-------------|---------|
| GPT-4o | 0.262 | 0.353 | 0.407 | 0.338 |
| GPT-4o + RAG | 0.696 | 0.579 | 0.593 | 0.620 |
| GraphRAG | 0.618 | 0.558 | 0.593 | 0.586 |
| StructRAG | 0.678 | 0.588 | 0.573 | 0.612 |
| **DocSage** | **0.934** | **0.908** | **0.812** | **0.892** |

### 关键发现
- DocSage 在所有类别上大幅领先——Overall 89.2% vs 下一最好 62.0%（+27.2%）
- 在 >100 文档场景（Set3）优势最大：87.9% vs 41.5%，说明结构化方法在长文本场景优势倍增
- SQL 驱动的推理完全消除了注意力稀释问题

## 亮点与洞察
- **从非结构化到结构化再到 SQL 推理**的 pipeline 设计非常优雅——将 MDMEQA 降维为数据库查询问题
- **ASK 算法的交互式 schema 发现**比静态预定义方案更灵活——能适应任意新领域
- **CLEAR 的跨记录逻辑一致性校验**是关键创新——不只检查单点抽取质量，还确保全局逻辑一致
- 在 >100 文档上的绝对优势说明结构化方法是长文档推理的正确方向

## 局限性 / 可改进方向
- 多模块 pipeline 依赖每个模块的质量——schema 发现错误会级联传播
- 依赖 GPT-4o 作为核心 LLM，成本较高
- SQL 表达能力有限——某些需要模糊匹配或推理的查询可能难以编译

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 动态 schema + 结构化抽取 + SQL 推理的完整 pipeline 是全新范式
- 实验充分度: ⭐⭐⭐⭐ 两个 benchmark + 不同文档规模分组对比
- 写作质量: ⭐⭐⭐⭐ 框架清晰，算法描述详尽
- 价值: ⭐⭐⭐⭐⭐ 对多文档 QA 有革命性的方法论意义
