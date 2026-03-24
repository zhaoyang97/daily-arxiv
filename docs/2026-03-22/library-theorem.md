# The Library Theorem: How External Organization Governs Agentic Reasoning Capacity

**日期**: 2026-03-22  
**arXiv**: [2603.21272](https://arxiv.org/abs/2603.21272)  
**代码**: [GitHub](https://github.com/zmainen/library-theorem)  
**领域**: 机器人  
**关键词**: agentic reasoning, B-tree, context window, indexed retrieval, computational complexity

## 一句话总结
提出 Library Theorem，将 Transformer 上下文窗口形式化为 I/O 页面，证明顺序扫描 vs B-tree 索引检索存在指数级效率差异——M=500 条目下索引仅需 1 次页读取 vs 顺序需 21 次，M=2000 时 token 成本差 153.6×。

## 研究背景与动机

1. **领域现状**: LLM Agent 将对话历史作为顺序存储维护在上下文窗口中。检索信息需要线性扫描整个历史。

2. **现有痛点**: 随着交互变长，顺序检索的累积成本 $\Theta(T^2)$ 不可持续。每次推理步都需要重新扫描前面的所有内容，这是对计算资源的极大浪费。

3. **核心 idea**: 引入经典 B-tree 索引理论——将上下文窗口类比为磁盘 I/O 页面，证明索引化外部记忆将检索从 $O(T^2)$ 降到 $O(T \log T)$，即从二次复杂度降到近线性。

## 方法详解

### 整体框架
形式化: 上下文窗口容量 C tokens → 三种实验条件: FLAT（随机页），FLAT-SORTED（排序无索引），INDEXED（B-tree 目录）→ Agent 用 tool calls (read_page, get_index) 检索目标键值 → 测量页读取次数和 token 成本。

### 关键设计

1. **I/O 页面模型**:
   - 将 Transformer 上下文窗口形式化为容量 C 的 I/O 页面
   - 顺序访问: 读任意页 i 无结构信息, 最坏 $\Omega(N)$ 次
   - 这个类比让经典外存算法理论直接适用

2. **B-tree 索引检索**:
   - 内部节点包含键范围，分支因子 $b = \lfloor C/(\eta + \kappa + \delta) \rfloor$
   - 检索成本 $\lceil \log_b N \rceil + 1$ 次页读取
   - 累积 T 步成本 $O(T \log_b T)$ vs 顺序 $\Theta(T^2)$

3. **三种内容类型控制实验**:
   - **Hash 内容**: 随机字符串，纯检索能力测试
   - **Numeric 内容**: 数字键值，可测试 Agent 是否自发做二分搜索
   - **Encyclopedia 内容**: 真实知识条目，测试参数记忆竞争

4. **参数记忆竞争现象**:
   - 在 Encyclopedia 条件下，模型倾向于直接用参数知识回答而非遵循检索协议
   - 这是一种新的失败模式: 语义理解绕过了工具使用
   - INDEXED-CORRUPTED: 打乱索引后性能崩溃到 FLAT 以下，证明模型确实在使用索引

## 实验关键数据

### 主实验（Hash, M=500）

| 条件 | 中位页读取 | 分离比 |
|------|-----------|--------|
| FLAT | 21.0 | — |
| INDEXED | 1.0 | 21× |
| 理论预测 | M/20≈25 | ✓匹配 |

### Token 成本（M=2000）

| 条件 | 总 Token |
|------|---------|
| FLAT | 913,983 |
| INDEXED | 5,950 |
| 比值 | **153.6×** |

### 关键发现
- 分离比随 M 线性增长: M∈{50,100,200,500} 对应 3×,6×,9×,21×，精确匹配理论
- GPT-5.4 在排序页上可做近最优二分搜索 (5.0 reads vs log₂(50)≈5.6)，但仍比索引慢 5×
- 打乱索引后性能崩溃（11.0 vs 9.0 reads, 58% vs 94% accuracy），证因果使用

## 亮点与洞察
- **经典 CS 理论直接适用**: B-tree/外存算法理论完美映射到 LLM Agent 场景，理论优雅
- **参数记忆竞争**是新现象: 当 Agent 已"知道"答案时会跳过工具使用——对 RAG/tool-use 设计有重要启示
- **实际影响巨大**: 153× token 节省意味着 Agent 的长期交互成本可以大幅降低

## 局限性 / 可改进方向
- 仅在键值查找任务上验证——更复杂的推理任务如何？
- 仅两个模型 (GPT-4o-mini, GPT-5.4) 参与实验
- B-tree 假设键全序——关系型或图结构知识需要更丰富的索引

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 将经典复杂度理论引入 Agent 系统设计
- 实验充分度: ⭐⭐⭐⭐ 精心设计的控制实验、因果验证
- 价值: ⭐⭐⭐⭐⭐ 对长期 Agent 交互的外部记忆设计有根本性指导
