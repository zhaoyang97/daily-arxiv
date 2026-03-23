# ESG-Bench: Benchmarking Long-Context ESG Reports for Hallucination Mitigation

**日期**: 2026-03-13  
**arXiv**: [2603.13154](https://arxiv.org/abs/2603.13154)  
**代码**: 未公开  
**领域**: LLM推理 / NLP  
**关键词**: ESG reporting, hallucination mitigation, long-context QA, chain-of-thought, benchmark

## 一句话总结
构建 ESG-Bench——首个面向长上下文 ESG 报告的幻觉检测与缓解 benchmark（人工标注 QA 对+幻觉类型标签），设计任务特定 CoT 策略微调 LLM，显著减少 ESG 分析中的幻觉生成。

## 研究背景与动机

1. **领域现状**: ESG 报告已成为法律要求，但长达数百页，包含文本/表格/图形。LLM 自动化分析前景广阔但幻觉问题严重。

2. **现有痛点**: ESG 报告特殊挑战——"漂绿"风险、定性数据为主、多模态、超长文档。现有 QA benchmark 不针对 ESG 领域，无幻觉标签。

3. **核心 idea**: 构建带幻觉标注（添加型/遗漏型）的 ESG QA benchmark + 设计 CoT 策略引导 LLM 在源文档中定位证据再回答。

## 方法详解

### 数据集构建
- 94 份真实 ESG 报告（2020-2024），270 个 QA 对
- GPT-4o 生成初始回答 → 2 名博士级标注员独立评审 → 第三方仲裁
- 标签：正确(46.7%) / 不完整(34.8%) / 幻觉(15.6%) / 未找到答案(3.0%)
- Cohen's Kappa 68.9%-86.7%

### CoT 幻觉缓解
- 任务特定 CoT：引导模型先定位页码和段落，再推理回答
- CoT 标注的推理链用于微调

## 实验关键数据

| 方法 | ESG-Bench 幻觉率 ↓ |
|------|-------------------|
| Standard prompting | ~15.6% |
| Direct fine-tuning | ~10% |
| **CoT fine-tuning** | **~5%** |

### 关键发现
- CoT 策略大幅超越标准提示和直接微调——结构化推理有效减少幻觉
- 增益可迁移到非 ESG 领域的 QA benchmark

## 亮点与洞察
- 首个带幻觉标注的 ESG QA benchmark，填补合规性关键领域的评测空白
- 幻觉分类（添加型 vs 遗漏型）有助于精准评估

## 局限性 / 可改进方向
- 270 个 QA 对规模偏小
- 仅用 GPT-4o 作为初始回答生成器
- 多模态（表格/图形）处理不够深入

## 评分
- 新颖性: ⭐⭐⭐ 领域特定 benchmark 有价值，但方法层面（CoT微调）无新意
- 实验充分度: ⭐⭐⭐ 数据规模小，模型覆盖有限
- 价值: ⭐⭐⭐⭐ 对 ESG/金融 NLP 社区有实用价值
