# CangjieBench: Benchmarking LLMs on a Low-Resource General-Purpose Programming Language

**日期**: 2026-03-15  
**arXiv**: [2603.14501](https://arxiv.org/abs/2603.14501)  
**领域**: NLP生成 / LLM推理  
**关键词**: CangjieLang, code benchmark, low-resource programming, RAG, agent

## 一句话总结
为新兴仓颉编程语言创建首个零污染 benchmark（248 个手工翻译样本），覆盖函数级和类级任务，评估四种生成范式（直接/语法约束/RAG/Agent），发现 Code-to-Code 翻译存在负迁移、语法约束最佳性价比、Agent 最高准确但 token 消耗大。

## 研究背景与动机

1. **领域现状**: LLM 代码生成在 Python/Java 等高资源语言上表现优异，但对训练数据中几乎不存在的新语言（如仓颉——HarmonyOS 的核心语言）完全失效。

2. **现有痛点**: 无零污染的低资源语言评估基准；不清楚哪种适配范式（直接生成/翻译/RAG/Agent）最适合低资源语言。

3. **核心 idea**: 手工将 HumanEval (164题) + ClassEval (84题) 翻译为仓颉语言，构建 248 个零污染样本，用 Docker 沙箱安全执行评估，系统比较四种生成范式。

## 方法详解

### 基准构建
- **数据源**: HumanEval（函数级）+ ClassEval（类级）手工逐题翻译为仓颉
- **零污染保证**: 仓颉语言不在任何公开 LLM 训练集中
- **安全执行**: Docker 沙箱隔离运行测试用例

### 四种生成范式

1. **Direct Generation**: 直接提示 LLM 生成仓颉代码
2. **Syntax-Constrained Generation**: 在提示中加入仓颉语法规范片段
3. **RAG (Retrieval-Augmented Generation)**: 检索仓颉文档/示例代码
4. **Agent**: 多轮交互 + 错误反馈迭代修正

### 评估维度
- Text-to-Code：从自然语言描述生成仓颉代码
- Code-to-Code：从 Python 代码翻译为仓颉代码

## 实验关键数据

### 主实验: Text-to-Code (HumanEval 子集, Pass@1%)

| 范式 | DeepSeek-V3 | ERNIE-4.5 | Kimi-K2 | Qwen3 | GPT-5 |
|------|------------|-----------|---------|-------|-------|
| Direct | 3.0 | 4.3 | **23.8** | 4.3 | 7.3 |
| Syntax-Constrained | **47.6** | 39.0 | — | — | — |

- Direct Generation 时，大多 LLM 准确率不到 5%——零资源语言的知识完全为空
- Kimi-K2 异常高 (23.8%)——可能见过少量仓颉资料
- Syntax-Constrained 下 DeepSeek-V3 从 3.0% 跃升到 47.6%——语法规范的 ICL 效果惊人

### Code-to-Code vs Text-to-Code 对比

| 范式 | T2C Pass@1 | C2C Pass@1 | 结论 |
|------|-----------|-----------|------|
| Direct | 3.0 | ≤3.0 | 两者都极低 |
| Syntax-Constrained | 47.6 | <47.6 | **C2C 出现负迁移** |
| Agent | 最高 | 低于 T2C | **C2C 负迁移持续存在** |

### Compilation Rate
- Direct Generation 编译率仅 ~5%——几乎全部语法错误
- Syntax-Constrained 编译率跃升到 35-45%——语法规范让模型能写出可编译代码

### 关键发现
- **Code-to-Code 负迁移**: Python→仓颉翻译反而不如 Text-to-Code，模型翻译时保留 Python 的 list comprehension、动态类型等语法，而这些在仓颉中不存在
- **语法约束是最佳性价比**: 简洁语法片段让 DeepSeek-V3 提升 14.8×，成本仅增加少量 prompt token
- **Agent 准确率最高但 token 消耗最大**: 多轮交互+编译反馈迭代修正能达到最高准确率
- **ClassEval 远难于 HumanEval**: 类级别任务需要多方法协调，Pass@1 远低于函数级

## 亮点与洞察
- **负迁移的首次量化**: Code-to-Code 翻译中源语言语法偏见被在编程语言层面首次严格测量——与跨语言 NMT 的 negative transfer 类似
- **方法论可推广**: 评估框架（手工翻译+Docker 沙箱+四范式评估）可复用于 Mojo、Carbon 等新语言
- **零污染评估**: 仓颉 2025 年 7 月发布，完全排除预训练数据泄露
- **Syntax-Constrained 的实用价值**: 对企业采用新语言时的 LLM 辅助开发有直接指导

## 局限性 / 可改进方向
- 仓颉语言社区较小，benchmark 直接受众有限
- 248 样本规模有限，更大规模可更好评估难题通过率
- 仅评估代码生成，调试/修复/代码理解等任务未涉及
- 未评估 fine-tuning——用少量仓颉代码微调 Code LLM 可能更直接

## 相关工作与启发
- **vs VerilogEval / SolEval**: DSL benchmark，领域知识和语法混在一起
- **vs MultiPL-E**: Lua/R 等"低资源语言"在预训练集中大量存在，不是真正零资源

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个低资源通用语言零污染 benchmark + 负迁移发现
- 实验充分度: ⭐⭐⭐⭐ 6 个模型 × 四种范式 × 两类任务
- 写作质量: ⭐⭐⭐⭐ 动机和评估逻辑清晰
- 价值: ⭐⭐⭐ 仓颉受众有限，但方法论和发现可推广
