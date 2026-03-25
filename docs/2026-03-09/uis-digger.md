# UIS-Digger: Towards Comprehensive Research Agent Systems for Real-world Unindexed Information Seeking

**日期**: 2026-03-09  
**arXiv**: [2603.08117](https://arxiv.org/abs/2603.08117)  
**代码**: [HuggingFace Dataset](https://huggingface.co/datasets/UIS-Digger/UIS-QA)  
**领域**: LLM/NLP  
**关键词**: unindexed information seeking, research agent, multi-agent, dual-mode browsing, deep research

## 一句话总结
发现并形式化"未索引信息检索（UIS）"问题——搜索引擎无法直接索引的信息（动态页面/嵌入文件/深层链接），构建首个 UIS-QA benchmark（110 条专家标注 QA 对），并提出 UIS-Digger 四 agent 协作框架（双模浏览器+文件解析+SFT/RFT 两阶段训练），用 ~30B 参数模型达到 27.27% 超越 O3+GPT-4.1 驱动的系统。

## 研究背景与动机

1. **领域现状**: LLM 信息检索 agent 在 GAIA（Tongyi-DR 达 70.9%）和 BrowseComp-zh（46.7%）上表现优秀，这些 benchmark 评估的是基于搜索引擎索引知识的信息检索能力（Indexed Information Seeking, IIS）。

2. **现有痛点**: 现实世界中大量关键信息未被搜索引擎索引（Unindexed Information）——政府公告中需要多步点击才能到达的嵌入表格、需要日期选择器/筛选器等交互才能获取的动态页面内容、PDF/XLSX 等文件中的数据、被搜索引擎爬虫忽略的深层页面。现有 benchmark 完全没有评估这一能力。

3. **核心矛盾**: 两个因素限制了 UIS 能力——(a) action space 不足：搜索引擎型 agent 只能搜索+爬取，无法做深度网页交互（点击按钮/选日期/下载文件），使 UIS 问题"理论上不可解"；(b) 基座模型能力不足：即使扩展了 action space，模型也需要在庞大的行动空间中做出正确选择。

4. **本文要解决什么**: (a) 形式化 UIS 问题并构建评估 benchmark；(b) 设计覆盖搜索+深度浏览+文件解析的完整 action space；(c) 通过两阶段训练提升基座 LLM 的 UIS 决策能力。

5. **切入角度**: 将互联网页面集 $\mathcal{P}$ 分为搜索引擎可索引的 $\mathcal{II}$ 和不可索引的 $\mathcal{UI} = \mathcal{P} \setminus \mathcal{II}$，当回答问题需要的证据包含 $\mathcal{UI}$ 中的信息时即为 UIS 问题。

6. **核心 idea**: 扩展 agent action space（搜索+浏览+视觉感知+文件读取）+ 双模浏览（文本+截图共享记忆）+ SFT/RFT 两阶段微调底层 LLM。

## 方法详解

### 整体框架
用户查询 → **Planner**（任务分解+协调子 agent）→ **Web Searcher**（搜索引擎+爬虫获取索引信息，可委托 Web Surfer/File Reader）→ **Web Surfer**（从 URL 出发操作浏览器深度交互：点击/滚动/输入/选择/截图/下载）→ **File Reader**（PDF/XLSX/DOCX 分块解析）→ Planner 整合信息输出最终答案。四个 agent 通过请求-响应消息系统通信，每个 agent 配备独立工具集，遵循 ReAct 范式迭代推理。

### 关键设计

1. **UIS-QA Benchmark 构建**:
   - 做什么：首个专门评估 UIS 能力的 benchmark，110 条专家标注 QA 对
   - 核心思路：专家团队在权威/官方网站进行深度浏览（多轮点击、选项选择、筛选器设置、站内搜索、文件下载），到达深层信息源后基于内容编写事实性问答题
   - 质量保证五原则：客观性（确定唯一答案）、权威性（来源必须是官方/权威网站）、静态性（答案不随时间变化）、可验证性（数值/日期/专有名词格式）、可访问性（无需登录或 CAPTCHA）
   - UIS 过滤流水线：3 人独立用 Google 搜索验证 → z.ai 自动验证 → DeepSeek-R1 离线 LLM 过滤 → 最终保留 110 条确认需要未索引信息的样本
   - 数据分布：84 条中文 + 26 条英文，覆盖政府公告/产品文档/代码仓库/游戏/公司年报等领域

2. **双模浏览策略（Dual-Mode Browsing）**:
   - 做什么：Web Surfer 在文本模式和视觉模式间动态切换
   - 核心思路：文本模式读取 HTML 源码处理结构化内容（高效），视觉模式截图理解复杂布局/图表/交互控件（完整）；两种模式共享同一份内存和浏览器状态
   - 设计动机：纯文本 agent 无法理解视觉布局（如图表/日期选择器），纯视觉 agent 效率低；共享记忆消除了模式切换的同步开销，优先文本模式以加速推理，仅在必要时切换视觉模式

3. **训练数据构造（真实+模拟双轨）**:
   - 做什么：构造 UIS 训练数据用于微调基座 LLM
   - 真实轨道：收集 100+ 真实网站 → UIS-Digger 在网站内漫游提取深层信息 → 另一个 LLM 基于提取内容生成 QA 对 → LLM judge 过滤
   - 模拟轨道：针对早期薄弱环节（如日期选择器交互）开发 3 类虚拟网站（航班预订/统计数据查询），配有虚构 JSON 数据库，QA 对直接从数据库导出
   - 设计动机：真实数据保证泛化性，模拟数据强化特定交互能力短板

4. **SFT + RFT 两阶段微调**:
   - 做什么：将通用 LLM 训练为 UIS 专用决策模型
   - **SFT 阶段**：用强教师模型 $\mathcal{X}^*$ 在部分训练题上生成轨迹（temperature=0），reject sampling 保留正确且非平凡的轨迹，冷启动训练得到 $\mathcal{X}^s$
   - **RFT 阶段**：$\mathcal{X}^s$ 在剩余训练题上 temperature=0.4 采样 4 条轨迹/题，reject sampling 保留正确的，按难度重加权（难题轨迹更高权重），bootstrapping 得到最终 $\mathcal{X}^r$
   - 设计动机：SFT 提供能力基线，RFT 通过探索+难度加权进一步提升 UIS 决策能力

### 训练策略
- 仅对 LLM 生成的 token 做梯度更新，工具返回内容不参与训练
- 训练了两个版本：PanGu-38B 和 Qwen3-32B
- SFT 和 RFT 使用不相交的训练题集

## 实验关键数据

### 主实验（UIS-QA + GAIA + BrowseComp-zh）

| 方法 | 类型 | Backbone | UIS-QA | GAIA | BC-zh |
|------|------|----------|--------|------|-------|
| DeepSeek-V3.1 | 直接推理 | DeepSeek-V3.1 | 1.8% | — | — |
| GPT-5 | 直接推理 | GPT-5 | 0.9% | — | — |
| Gemini-2.5-pro | 商业系统 | Gemini-2.5-pro | 4.5% | — | — |
| WebSailor | ReAct | 32B+Qwen3-72B | 7.3% | 53.2 | 25.5 |
| Tongyi-DR | ReAct | 30B+GPT-4o | 23.6% | **70.9** | **46.7** |
| OWL | 多 agent | O3-mini+4o+Claude | 4.6% | 69.7 | — |
| Memento | 多 agent | O3+GPT-4.1 | 25.5% | 79.4 | — |
| **UIS-Digger (Pangu)** | 多 agent | PanGu-38B | **27.3%** | 50.5 | 32.5 |
| **UIS-Digger (Qwen)** | 多 agent | Qwen3-32B | **27.3%** | 47.6 | 32.5 |

### 消融实验（训练阶段消融，PanGu-38B backbone）

| 配置 | UIS-QA Acc | 提升 |
|------|-----------|------|
| 基座模型（无训练） | 9.1% | — |
| + SFT | 22.7% | +13.6 pp |
| + SFT + RFT（完整） | **27.3%** | +4.6 pp |

### 关键发现
- **所有 baseline 在 UIS-QA 上大幅暴跌**: Tongyi-DR 从 GAIA 70.9% 跌至 UIS-QA 23.6%（-47.3 pp），Memento 从 79.4% 跌至 25.5%（-53.9 pp），证明 UIS 是真实且严重的盲区
- **直接推理完全无效**: GPT-5 仅 0.9%，DeepSeek-V3.1 仅 1.8%，无工具调用几乎无法解决 UIS 问题
- **Action space 是必要条件但非充分条件**: OWL 有完整 action space 但仅 4.6%，说明基座模型能力才是瓶颈
- **两阶段训练收益显著**: SFT +13.6 pp，RFT 再 +4.6 pp，且 RFT 的难度加权策略有效
- **在 GAIA 上表现好的方法在 UIS-QA 上也相对好**（相关但非必然）——强基座模型对 UIS 任务仍然重要
- **~30B 专门训练的模型超越 O3+GPT-4.1 组合**: 说明 UIS 场景下模型微调比模型规模更重要

## 亮点与洞察
- **发现并形式化了一个重要的新问题**: UIS 将互联网信息明确分为"可索引"和"不可索引"两类——现有 agent 只擅长前者。形式化清晰（$\mathcal{II}$ vs $\mathcal{UI}$ 的集合论定义）为后续研究奠定了基础
- **UIS benchmark 的独特性**: 与 GAIA/BrowseComp 的关键区别是 Unindexed-Information Dependence——答案必须通过未索引信息才能获得，且用确定性短答案评估消除主观判断
- **双模浏览共享记忆**: 文本和视觉模式共享状态是比交替调用两个独立系统更高效的设计。优先文本模式、按需视觉模式的策略兼顾了效率和能力
- **模拟网站训练策略**: 针对交互控件薄弱环节构建虚拟网站的做法值得借鉴——可以精确控制训练目标

## 局限性 / 可改进方向
- 110 条测试样本偏少，统计显著性有限，且可能存在领域偏差
- 27.27% 的绝对准确率仍然很低，距离实用有很大差距
- 中英文比例不均衡（84 中文 + 26 英文），可能偏向中文互联网
- UIS 的形式化定义依赖特定搜索引擎（Google Serper），换引擎后 UIS/IIS 划分可能变化
- 训练数据构造依赖强教师模型（如 O3），冷启动成本高
- 未来可探索：更大规模 UIS benchmark、跨语言 UIS 评估、工具增强型 LLM 的通用 UIS 微调策略

## 相关工作与启发
- **vs GAIA / BrowseComp**: 同为信息检索 benchmark，但不区分 IIS/UIS——在这些 benchmark 上表现好的 agent 在 UIS-QA 上可能暴跌 50+ pp
- **vs WebArena / Mind2Web**: 计算机操作类 benchmark，聚焦浏览器交互操作能力，但在固定网站上评估，无需搜索策略
- **vs Memento**: 同为多 agent 框架且 UIS-QA 上表现接近（25.5% vs 27.3%），但 Memento 依赖 O3+GPT-4.1 等顶级商用模型，UIS-Digger 用 ~30B 开源模型实现超越
- **vs Tongyi DeepResearch**: ReAct 框架 + GPT-4o，GAIA 很强但缺少文件读取和浏览器操作能力，UIS 上仅 23.6%

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次定义 UIS 问题并构建专用 benchmark，揭示了 agent 评估的根本盲区
- 实验充分度: ⭐⭐⭐⭐ 15+ baseline 对比 + 训练阶段消融 + 详细失败分析 + 搜索/浏览行为可视化
- 写作质量: ⭐⭐⭐⭐ 问题形式化清晰（集合论定义），数据构造流水线详尽
- 价值: ⭐⭐⭐⭐⭐ 对 agent 研究方向有重要指引意义——从"搜索够用"转向"深度浏览必要"
