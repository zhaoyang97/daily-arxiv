# ToolFlood: Beyond Selection — Hiding Valid Tools from LLM Agents via Semantic Covering

**日期**: 2026-03-14  
**arXiv**: [2603.13950](https://arxiv.org/abs/2603.13950)  
**代码**: [ToolFlood](https://github.com/as1-prog/ToolFlood) (即将开源)  
**领域**: LLM Agent / 安全攻击  
**关键词**: tool-augmented LLM, retrieval attack, semantic covering, top-k domination, adversarial tools

## 一句话总结
揭露 tool-augmented LLM agent 检索阶段的新漏洞——ToolFlood 通过 Monte Carlo 候选生成 + 贪心语义覆盖，在 ToolBench（11,760 工具）上仅注入 1.2% 的对抗工具即实现 91% TDR 和 ~95% ASR，使合法工具被完全隐藏在 top-k 检索结果之外。

## 研究背景与动机

1. **领域现状**: Tool-augmented LLM agent（如 GPT function calling）依赖 embedding-based 检索从大规模工具库中选择 top-k 相关工具。现有安全研究集中在工具**选择阶段**——假设合法工具已在候选集中，攻击者只需让恶意工具被优先选中。
2. **被忽视的威胁**: 更根本的漏洞在**检索阶段**——Top-k 支配（domination）。攻击者注入语义相近的对抗工具，直接将合法工具挤出 top-k 结果，使 agent 根本看不到正确工具。这是检索层的拒绝服务攻击（denial-of-visibility）。
3. **现有防御失效**: 选择阶段的防御（prompt-injection 过滤、tool-call sanitization）都**预设合法工具在候选集中**。一旦 top-k 被完全支配，这些防御全部失效——agent 被迫在攻击者策划的工具集中推理。

## 方法详解

### Phase 1: Monte Carlo 候选生成
- 运行 $I=1000$ 轮迭代，每轮采样 $|S_i|=20$ 个目标查询
- 用 GPT-4o-mini 为每个子集生成 $|G_i|=10$ 个候选对抗工具（名称+描述）
- 最终候选池大小：$1000 \times 10 = 10{,}000$ 个候选工具

### Phase 2: 贪心语义多覆盖选择
- 设定余弦距离阈值 $\delta=0.3$（基于查询与良性工具距离的 5% 分位数）
- 使用代理嵌入模型（黑盒）迭代选择能最大化覆盖未覆盖查询的工具
- 目标：top-k=5 的完全支配（quota $r=k=5$），直到所有查询被覆盖或预算用尽

### 攻击原理
少量精心设计的对抗工具 → embedding 空间中语义覆盖大范围查询 → top-k 结果被对抗工具占满 → 合法工具从候选集中消失 → 下游选择阶段防御全部失效

## 实验关键数据

**主实验（Table 1, text-embedding-3-small 检索）：**

| 数据集 | 方法 | 平均注入量 | 毒化率 | TDR | ASR (GPT-4o) | ASR (GPT-4o-mini) |
|---------|------|-----------|--------|-----|-------------|-------------------|
| MetaTool (199 工具) | Random-Sybil | 200 | 100% | 1.6% | 4.6% | 4.0% |
| MetaTool | PoisonedRAG | 100 | 50% | 95% | 98.1% | 98.1% |
| MetaTool | **ToolFlood** | 171 | 86.3% | **97.2%** | **99.6%** | **99%** |
| ToolBench (11,760 工具) | Random-Sybil | 200 | 1.7% | 0% | 1% | 0.2% |
| ToolBench | PoisonedRAG | 100 | 0.85% | 82% | 91.4% | 92% |
| ToolBench | **ToolFlood** | 145 | **1.2%** | **91%** | **94.6%** | **96.1%** |

**跨检索器迁移性（Table 2, ToolBench）：**

| 目标检索器 | 代理检索器 | TDR | ASR |
|-----------|-----------|-----|-----|
| text-embedding-3-small | text-embedding-3-small | 91% | 94.6% |
| text-embedding-3-small | all-MiniLM-L6-v2 | 84% | 91.2% |
| text-embedding-3-large | text-embedding-3-small | 91.8% | 95% |
| all-MiniLM-L6-v2 | text-embedding-3-small | 78% | 92.7% |

**防御评估（Table 3, ToolBench, GPT-4o-mini）：**

| 防御方法 | TDR | ASR |
|---------|-----|-----|
| 无防御 | 91% | 96.1% |
| + MMR 重排序 | 44.8% | 91.0% |
| + Llama Prompt Guard | 91% | 96.1% |

### 关键发现
- ToolBench 上仅 1.2% 毒化率即达 91% TDR，远超 Random-Sybil（0% TDR）
- ASR 在不同 selector LLM（GPT-4o/5-mini/4o-mini）间高度一致，说明攻击与下游模型无关
- 黑盒跨检索器迁移：代理模型为 MiniLM 时，在 text-embedding-3-small 上仍有 84% TDR
- MMR 重排序将 TDR 从 91% 降至 44.8%，但 ASR 仍高达 91%——部分洪泛即足以误导选择
- Prompt Guard 完全无效（TDR/ASR 不变），因为对抗工具不含显式 prompt injection 特征

## 亮点与洞察

- **揭露检索层系统性漏洞**：不是 prompt injection 也不是工具误选，而是在检索阶段就阻止了正确工具被发现，使所有下游防御失效
- **Sybil 攻击框架**：将问题形式化为 embedding 空间的集合覆盖优化，理论上证明了检索饱和的几何条件
- **实际威胁**：开放工具市场（如 GPT Store、LangChain Hub）的发布门槛极低，使此类攻击在实践中完全可行

## 局限性
- 假设攻击者可在开放工具市场中注入并维持大量工具，在严格审核的平台上可能受限
- 仅在 MetaTool (199) 和 ToolBench (11,760) 两个 benchmark 上验证
- MMR 虽降低了 TDR 但未降低 ASR，论文未提出有效防御方案

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次系统性揭露工具检索阶段的 top-k 支配漏洞
- 实验充分度: ⭐⭐⭐⭐ 双 benchmark + 跨检索器迁移 + 防御评估，较完整
- 写作质量: ⭐⭐⭐⭐ 攻击形式化清晰，理论与实验结合紧密
- 价值: ⭐⭐⭐⭐⭐ 对 LLM agent 工具生态安全有重要警示意义
