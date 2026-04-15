# LIT-RAGBench: Benchmarking Generator Capabilities of Large Language Models in RAG

**日期**: 2026-03-06  
**arXiv**: [2603.06198](https://arxiv.org/abs/2603.06198)  
**代码**: https://github.com/Koki-Itai/LIT-RAGBench  
**领域**: LLM推理  
**关键词**: RAG, benchmark, LLM evaluation, generator capabilities, abstention

## 一句话总结
提出 LIT-RAGBench，一个系统评估 RAG 中 Generator 五大能力（Integration/Reasoning/Logic/Table/Abstention）的 benchmark——通过虚构实体防止知识泄漏、支持跨类别组合评估，实验发现即使 GPT-5 也无法超过 90% 总体准确率。

## 研究背景与动机

1. **领域现状**：RAG 已成为缓解 LLM 幻觉、知识过时等问题的主流框架。现有 RAG benchmark（FRAMES、RAGBench、RGB 等）主要评估 Retriever 或孤立地测试 Generator 的某个能力维度。

2. **现有痛点**：(a) 现有 benchmark 覆盖面有限——FRAMES 关注端到端评估但不分离 Generator 能力；RGB 测试了噪声鲁棒性和信息整合但缺少表格理解；RAGTruth 专注幻觉检测但不测推理能力；(b) 实际 RAG 场景中 Generator 需要同时具备多种能力（如：从多文档表格中做数值推理），但没有 benchmark 系统评估这种能力组合。

3. **核心矛盾**：实际 RAG 应用要求 Generator 同时处理多种复杂场景（多源整合 + 表格解析 + 数值推理 + 适时拒答），但现有评估只测单一维度，导致模型选型缺乏可靠依据。

4. **切入角度**：将 Generator 需要的能力系统化为 5 大类别 × 14 个细分方面，构建支持跨类别组合的评估数据集，用虚构实体确保模型无法靠预训练知识作弊。

5. **核心 idea**：构建一个"组合式"RAG Generator benchmark，每个问题可同时涉及 1-2 个类别的能力，实现对 Generator 多维能力的联合评估。

## 方法详解

### 整体框架
LIT-RAGBench 定义了 5 个评估类别（Integration、Reasoning、Logic、Table、Abstention），每个类别下有 2-4 个评估方面。数据集包含 114 个人工构造的日语问题 + 对应英语翻译版本。每个问题配有相关文档集 $C^+$ 和无关文档集 $C^-$（$|C^+ \cup C^-| \geq 8$），评估时随机打乱文档顺序消除位置偏差。

### 关键设计

1. **五大评估类别**:
    - **Integration**: 多源信息整合（$|C^+| \geq 2$），需从分散在多个文档中的证据提取并整合信息
    - **Reasoning**: 包含 multi-hop reasoning（跨文档推理得出未明确陈述的结论）和 numerical calculation（需要常识运算如利润率、增长率）
    - **Logic**: 处理 query 与文档之间的语义/逻辑偏差——同义词解读（"1万元" vs "10,000元"）、数值包含判断（35岁是否满足"20以上40以下"）、概念包含解读（"降噪耳机"是否属于"电子设备"）
    - **Table**: 表格理解——HTML 表格、带合并单元格的 HTML、Markdown 表格、CSV 数据
    - **Abstention**: 适时拒答——证据不足（$C^+$ 为空）、矛盾证据、不完整 chunk
    - 设计动机：前四个为"主能力"（Main），Abstention 为独立的"异常处理"能力

2. **跨类别组合评估**:
    - 做什么：每个问题可关联 1-2 个类别的评估方面（如同时测试 Reasoning + Table）
    - 核心思路：形式化为 $\Psi(q) \subseteq \Phi$，约束 $1 \leq |\Psi(q)| \leq 2$ 且同一类别不重复
    - 设计动机：实际 RAG 场景中能力是组合出现的——比如需要从 HTML 表格中做数值计算。只测单一能力无法反映真实难度

3. **虚构实体防知识泄漏**:
    - 做什么：所有 QA 场景使用虚构的公司名、产品名、人名
    - 设计动机：防止 LLM 利用预训练知识直接回答，确保必须依赖提供的外部文档

### 评估方法
- 使用 LLM-as-a-Judge（GPT-4.1）做二元判断：生成答案是否与参考答案语义一致
- 按类别计算准确率 $\text{Accuracy}(\theta)$，总体准确率取各类别平均 $\overline{\text{Accuracy}}$

## 实验关键数据

### 主实验（日语/英语总体准确率）

| 模型 | 日语 Acc | 英语 Acc | 类型 |
|------|:---:|:---:|------|
| GPT-5 | **0.872** | **0.872** | API reasoning |
| o3 | 0.857 | 0.844 | API reasoning |
| o4-mini | 0.852 | 0.864 | API reasoning |
| Gemini-2.5-Flash | 0.823 | 0.878 | API |
| Qwen3-235B-A22B | 0.865 | 0.806 | Open |
| Claude-Sonnet-4 | 0.821 | 0.791 | API |
| Llama-3.1-8B | 0.396 | 0.582 | Open |

### 类别级分析（日语）

| 模型 | Integration | Reasoning | Logic | Table | Abstention |
|------|:---:|:---:|:---:|:---:|:---:|
| GPT-5 | 0.833 | **0.870** | 0.867 | 0.839 | **0.900** |
| o3 | 0.833 | **0.957** | **0.900** | 0.839 | 0.817 |
| o4-mini | **0.917** | 0.913 | **0.900** | **0.871** | 0.783 |
| Claude-Sonnet-4 | 0.750 | 0.783 | 0.700 | 0.677 | **0.950** |

### 关键发现
- **没有模型超过 90%**：即使 GPT-5 总体也只有 0.872，说明 RAG Generator 能力仍有显著提升空间
- **Reasoning 类别区分度最大**：最强的 o3 达 0.957，最弱的 Llama-3.1-8B 仅 0.130（日语），差距 83 个点
- **Claude-Sonnet-4 在 Abstention 上最强**（0.950）但 Main 类最弱——说明"知道自己不知道"和"知道答案"是不同维度的能力
- **日语 vs 英语差异显著**：多数模型英语表现更好（尤其开源模型），但 GPT-5 在两种语言上持平

## 亮点与洞察
- **组合评估的设计思路值得借鉴**：通过跨类别组合，一个 114 题的小数据集就能有效评估多种复杂场景，数据效率很高
- **虚构实体策略简单有效**：避免知识泄漏问题，比 counterfactual 修改真实事实更自然，可迁移到其他 benchmark 构建
- **Claude 的"拒答能力强但主能力弱"现象很有意思**：提示 alignment 过度可能导致模型过于保守，在需要做答的场景也倾向拒答

## 局限性 / 可改进方向
- 数据集规模偏小（114 题），统计置信度有限
- 只覆盖日语和英语两种语言，缺少多语言泛化验证
- Abstention 中"矛盾证据"和"不完整 chunk"各只有 3 题，样本量不足以得出可靠结论
- LLM-as-a-Judge 的评估可靠性依赖 GPT-4.1，可能引入系统性偏差
- 没有评估模型在不同 chunk 数量和文档长度下的性能变化

## 相关工作与启发
- **vs RGB**: RGB 也评估了 noise robustness、negative rejection 和 integration，但缺少 Table 和 Logic 类别，且不支持跨类别组合
- **vs FRAMES**: FRAMES 更关注端到端评估，不分离 Retriever 和 Generator 的效果；LIT-RAGBench 用人工构造的 $C^+/C^-$ 完全隔离 Retriever 变量
- **vs RAGBench/TRACe**: TRACe 从 utilization/adherence/completeness 角度评估，更关注信息使用质量而非推理能力

## 评分
- 新颖性: ⭐⭐⭐ 评估框架设计合理但 benchmark 构建本身创新有限
- 实验充分度: ⭐⭐⭐⭐ 覆盖 15 个模型（API + 开源），双语评估
- 写作质量: ⭐⭐⭐⭐ 形式化定义清晰，分类体系完整
- 价值: ⭐⭐⭐⭐ 对 RAG 系统中 Generator 选型有实际指导意义
