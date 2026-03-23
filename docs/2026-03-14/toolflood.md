# ToolFlood: Beyond Selection — Hiding Valid Tools from LLM Agents via Semantic Covering

**日期**: 2026-03-14  
**arXiv**: [2603.13950](https://arxiv.org/abs/2603.13950)  
**代码**: [ToolFlood](https://github.com/as1-prog/ToolFlood) (即将开源)  
**领域**: LLM Agent / 安全攻击  
**关键词**: tool-augmented LLM, retrieval attack, semantic covering, top-k domination, adversarial tools

## 一句话总结
揭露 tool-augmented LLM agent 的检索阶段新漏洞——ToolFlood 通过 Monte Carlo 候选生成 + 贪心语义覆盖，仅注入 1% 的对抗性工具即可实现 95% 的 top-k 支配率，使合法工具被完全隐藏在检索结果之外。

## 研究背景与动机

1. **领域现状**: Tool-augmented LLM agent（如 GPT function calling）依赖 embedding-based 检索从大规模工具库中选择相关工具。现有安全研究集中在工具选择阶段的攻击。

2. **现有痛点**: 更严重但被忽视的威胁是**检索阶段的 top-k 支配** — 攻击者可以通过注入语义相近的对抗工具来完全挤占合法工具在 top-k 检索结果中的位置，使 agent 根本看不到正确的工具。

3. **核心 idea**: 用少量精心设计的对抗工具描述"覆盖"查询空间，使合法工具的嵌入距离被对抗工具阻挡。

## 方法详解

### 两阶段攻击

1. **Monte Carlo 候选生成**: 对目标查询子集采样，用 LLM 迭代生成多样化的对抗工具名称和描述，使其与查询子集语义高度相关

2. **贪心语义多覆盖**: 从候选集中选择能最大化覆盖剩余未覆盖查询的工具（在余弦距离阈值 δ 下），解决带预算约束的覆盖问题。使用代理嵌入模型近似目标检索器的几何结构。

### 攻击原理
少量对抗工具 → embedding 空间中覆盖大范围查询 → top-k 检索结果被对抗工具占满 → 合法工具被"隐藏"

## 实验关键数据

| 指标 | 数值 |
|------|------|
| Top-k 支配率 | 最高 95% |
| 工具注入比例 | 仅 1% |
| 测试平台 | ToolBench |

### 关键发现
- 1% 的注入率就能实现近乎完全的支配，说明 embedding-based 检索极其脆弱
- 低注入率使得攻击极难被防御系统检测
- 使用代理嵌入模型的黑盒攻击同样有效

## 亮点与洞察
- **暴露了 LLM 工具使用的系统性安全漏洞** — 不是 prompt injection 也不是工具误选，而是在检索层面就阻止了正确工具被发现
- **语义覆盖的集合论框架**在攻击理论上很优雅 — 将安全问题形式化为组合优化问题

## 局限性 / 可改进方向
- 缺少防御方法的讨论和评估
- 仅在 ToolBench 上验证，真实 API 市场的多样性未覆盖
- 对抗工具的可检测性（人工审核）未分析

## 相关工作与启发
- 传统 retrieval augmentation 的安全研究（如 RAG poisoning）
- 可推广到任何 embedding-based 检索系统的对抗攻击

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次系统性揭露工具检索阶段的对抗漏洞
- 实验充分度: ⭐⭐⭐ 单一 benchmark，缺少防御评估
- 写作质量: ⭐⭐⭐⭐ 攻击形式化清晰
- 价值: ⭐⭐⭐⭐⭐ 对 LLM agent 安全有重要警示意义
