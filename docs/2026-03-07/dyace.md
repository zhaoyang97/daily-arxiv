# DyACE: Dynamic Algorithm Co-evolution for Online Automated Heuristic Design with Large Language Model

**日期**: 2026-03-07  
**arXiv**: [2603.13344](https://arxiv.org/abs/2603.13344)  
**代码**: 无  
**领域**: LLM/NLP  
**关键词**: Automated Heuristic Design, Large Language Model, Receding Horizon Control, Combinatorial Optimization, Dynamic Algorithm Evolution

## 一句话总结

将自动化启发式算法设计（AHD）从静态一次性搜索重新定义为非平稳双层控制问题，提出 DyACE 框架，通过 Receding Horizon Control 架构让 LLM 作为 meta-controller 持续感知搜索轨迹特征并在线合成时变算法，在 JSSP/TSP/CVRP 三个组合优化基准上显著超越静态 AHD 方法。

## 研究背景与动机

1. **领域现状**: 自动化启发式设计（AHD）利用 LLM 的代码生成能力来自动发现组合优化算法，代表性工作如 FunSearch、EoH、ReEvo 已展现出强大的算法发现潜力。
2. **现有痛点**: 当前 LLM 驱动的 AHD 方法遵循"静态算法范式"——先离线搜索出一个最优算法，然后冻结部署。这种固定算法假设单一算子能有效处理整个搜索过程的所有阶段。
3. **核心矛盾**: 扰动式启发搜索本质上是非平稳的动态过程：早期需要高探索以覆盖解空间，后期需要精细开发以收敛。静态算法无法感知这些阶段转换，导致固定逻辑与变化需求之间的错配，尤其在高维复杂问题上出现"可扩展性墙"。
4. **切入角度**: 从控制论视角出发，将 AHD 重新定义为非平稳双层控制问题（Non-stationary Bi-level Control Problem），引入 Receding Horizon Control（滚动时域控制）架构，使算法设计从开环任务变为闭环反馈控制。
5. **核心 idea**: 建立"前瞻性搜索感知 → 解耦元推理 → 自适应执行"的在线闭环系统，让 LLM 作为有根据的 meta-controller，根据搜索轨迹的实时状态持续合成时变算法，使算法逻辑与解群体的演化保持动态对齐。

## 方法详解

### 整体框架

DyACE 采用 Receding Horizon Control 架构，将算法设计从一次性合成变为持续闭环反馈过程。系统维护一条自适应算法轨迹 $\tau_S$（动态算子序列 $\{h_t\}$），通过三个模块的循环交互实现：

1. **Look-Ahead Rollout Search**（感知层）：从当前种群 $\mathcal{P}_t$ 出发执行短期前瞻性rollout，提取搜索轨迹特征
2. **Decoupled Meta-Reasoning**（控制层）：LLM 解读状态特征，合成上下文特定的启发式算子 $h_t = \pi(\mathcal{S}_t)$
3. **Receding Horizon Evolution**（执行层）：在有限时域 $H$ 内应用合成算子驱动状态转移 $\mathcal{P}_t \to \mathcal{P}_{t+H}$

核心数学建模：将上层问题从静态的时不变优化 $c^* = \arg\min_{c \in \mathcal{C}} \mathbb{E}[J(\text{Rollout}(\mathcal{P}_0, \Psi(c)))]$（约束 $h_t \equiv \Psi(c), \forall t$），松弛为学习动态策略 $\pi: \mathcal{S} \to \Omega$，使得 $h_t = \pi(s_t)$ 可随时间变化。

### 关键设计

1. **Look-Ahead Rollout Search（前瞻搜索感知）**: 在每个决策步创建并行影子环境，从当前种群 $\mathcal{P}_t$ 出发执行短期 rollout（30代 vs 静态方法的150代完整rollout），信息分为两个并行流：
   - **Landscape Feature Extraction**：提取景观运动学特征（fitness轨迹的速度/加速度衡量优化动量，多样性损失率判断探索/开发状态）和算子遥测特征（Operator Precision = 后代严格优于父代的比例，Operator Impact = 成功更新的平均fitness增益）
   - **Iso-State Rollout Evaluation**：对每个算法 $h_k$ 从相同 $\mathcal{P}_t$ 出发运行 $M$ 次独立 Monte Carlo rollout，计算平均最优性gap $J(h_k) = \frac{1}{M}\sum_{m=1}^{M} g(\mathcal{P}_{t+\tau}^{(m)} | h_k)$

2. **Decoupled Meta-Reasoning（解耦元推理）**: 采用"Think-then-Code"的两阶段诊断-处方架构：
   - **Phase I - Diagnosis Agent**：仅分析搜索轨迹特征，禁止写代码，将景观动态翻译为自然语言"Verbal Gradients"（如"单块交叉限制了混合，需重构为两点交叉以交换不相邻段提升结构多样性"）
   - **Phase II - Coding Agent**：基于 Verbal Gradients 合成新算法，算法定义为三元组 $S = \langle \mathcal{D}, \mathcal{C}, \Theta \rangle$（语义描述、可执行代码、演化超参数），允许同时调整逻辑和参数

3. **Three Reasoning Modes（三种推理模式）**:
   - **Combine**：通过 Structure-Aware Sampling 选择一对父代（主选适应度最高、副选按 AST Tree-Edit Distance 最远），LLM 融合两者逻辑创建连贯的混合算法
   - **Mutate**：对单一父代进行局部优化，重构代码或微调参数，不改变基本算法结构
   - **Explore**：使用高温采样诱导最大逻辑发散，创建与父代显著不同的算法结构，扩展搜索范围

### 损失函数 / 训练策略

- **统一评估预算**：所有方法严格限制 $B=300$ 次算法评估，解群体大小 $N=100$
- **在线协同演化协议**：每一代算法演化，解群体前进5代；算法群体大小 $M=5$，演化30代，与解层150代同步（$30 \times 5 = 150$）
- **短视野rollout**：DyACE 的 Look-Ahead 使用30代短视野rollout（而非完整150代），每次评估时间限制2分钟（静态方法为5分钟）
- **重评估机制**：由于解景观的非平稳性，每个决策步需对父代算法重新评估以反映当前拓扑上的性能

## 实验关键数据

### 主实验

在三个 NP-hard 组合优化问题上进行评估，LLM backbone 统一为 GPT-4o-mini。

**Table 1: JSSP Taillard Benchmark 性能对比（Optimality Gap %, 越低越好）**

| 实例 | 规模 | GP | GEP | FunSearch | EoH | ReEvo | **DyACE** |
|------|------|------|------|-----------|-----|-------|-----------|
| TA01 | 15×15 | 25.67 | 25.67 | 35.17 | 13.81 | 10.85 | **6.66** |
| TA21 | 20×20 | 27.28 | 27.22 | 34.35 | 20.95 | 19.98 | **15.23** |
| TA51 | 50×15 | 30.54 | 32.90 | 36.52 | 25.91 | 26.85 | **16.96** |
| TA71 | 100×20 | 15.39 | 14.90 | 22.71 | 26.39 | 19.42 | **11.13** |
| TA72 | 100×20 | 11.48 | 8.57 | 22.58 | 26.98 | 17.47 | **8.43** |
| **Avg** | – | 28.32 | 26.54 | 33.45 | 24.25 | 19.38 | **14.73** |

**Table 2: TSP（TSPLIB）和 CVRP（CMT）性能对比（Optimality Gap %）**

| 方法 | eli51 | st70 | rd100 | bier127 | kroB200 | CMT1 | CMT2 | CMT5 |
|------|-------|------|-------|---------|---------|------|------|------|
| FunSearch | 2.35 | 9.93 | 50.83 | 61.98 | 218.22 | 25.58 | 47.33 | 166.82 |
| EoH | 0.47 | 3.70 | 13.65 | 5.25 | 19.90 | 17.04 | 33.49 | 168.84 |
| ReEvo | 0.00 | 0.00 | 0.61 | 1.71 | 16.19 | 12.57 | 41.27 | 12.96 |
| **DyACE** | **0.00** | **0.00** | **0.00** | **0.00** | **6.38** | **3.17** | **28.44** | **12.01** |

### 消融实验

**Table 3: JSSP 消融实验（Optimality Gap %）**

| 方法 | ta21 (20×20) | ta51 (50×15) | ta71 (100×20) |
|------|-------------|-------------|--------------|
| DyACE-w/o-both | 20.95 | 26.41 | 20.20 |
| DyACE-Blind（去掉特征提取） | 17.36 | 21.45 | 19.60 |
| DyACE-Static（去掉在线适应） | 16.63 | 19.17 | 17.94 |
| **DyACE (Full)** | **15.23** | **16.96** | **11.13** |

三个消融变体：
- **DyACE-Static**：移除 Receding Horizon Control 循环，冻结算法逻辑
- **DyACE-Blind**：保留在线适应但移除特征提取，Meta-Controller 在无搜索轨迹特征下运作
- **DyACE-w/o-Both**：同时移除两个机制

### 关键发现

1. **可扩展性优势显著**：DyACE 在 JSSP 所有16个实例上均取得最优，平均 gap 14.73% vs ReEvo 19.38%（相对提升约24%）。问题规模越大优势越明显——TA71 上 DyACE 11.13% vs 静态最强 ReEvo 19.42%
2. **TSP 上达到全局最优**：在仅用 Crossover+Mutation（无 local search）的严格约束下，DyACE 在 eli51 到 bier127（51-127节点）上均收敛到已知最优解（0.00% gap），ReEvo 从 rd100 开始出现退化
3. **"盲目适应"比静态更差**：消融中最关键的发现——DyACE-Blind 在 ta71 上（19.60%）不仅差于完整模型，甚至**差于静态基线**（17.94%）。这证明没有 grounded perception 的动态适应实质上退化为算子空间的随机游走，反而破坏优化动量
4. **阶梯式收敛 vs 平台式停滞**：进化过程分析显示，静态方法在约5-15代后在算法空间收敛到局部最优并停止改进，而 DyACE 全程持续降低算法最优性gap，解的收敛曲线呈阶梯状下降模式

## 亮点与洞察

- **视角转换极具启发性**：将 AHD 从静态优化重新定义为非平稳控制问题，这一理论框架化为整个领域提供了新思路。类比于经典控制论中的开环与闭环控制，论文清晰指出静态 AHD 是开环的，因此在动态环境中必然失败
- **"Verbal Gradients"作为因果桥梁**：通过 Diagnosis Agent 将量化的搜索轨迹特征翻译为自然语言"梯度"，巧妙地利用了 LLM 在自然语言推理上的优势，避免了直接从特征到代码的映射错误
- **消融设计精妙**：DyACE-Blind 的失败不仅验证了特征提取的必要性，更揭示了一个深层原理——**无信息基础的适应反而有害**，这与控制论中"盲反馈引入不稳定性"的原理一致
- **Case Study 可读性强**：附录 D 中对 ta51 演化轨迹的分析展示了算法如何从通用 OX 逐步演化到 Compatibility-aware Heuristic Crossover，体现了 domain-awareness 的自动涌现

## 局限性 / 可改进方向

1. **推理延迟**：Meta-Controller 的两阶段 LLM 推理（诊断+编码）是主要瓶颈，限制了在实时调度场景的应用。作者建议未来采用分层结构，小模型负责频繁微调、大模型处理战略性变化
2. **缺乏跨领域迁移**：目前每个实例从零开始，未利用跨问题的知识迁移。Verbal Gradients 的自然语言表示为跨域迁移提供了天然接口，但尚未被开发
3. **Instance-specific 评估**：受扰动式启发搜索的Monte Carlo评估成本限制，仅能做 instance-specific 的演化，未验证跨实例泛化能力
4. **LLM 选择单一**：所有实验仅用 GPT-4o-mini，未探索不同 LLM backbone 对性能的影响
5. **计算成本分析不够详细**：虽然论文声称总评估预算统一为300次，但 DyACE 的在线重评估和双阶段 LLM 调用的实际 wall-clock time 对比数据缺失

## 相关工作与启发

- **FunSearch** (Romera-Paredes et al., Nature 2023): LLM 驱动的函数搜索，多岛演化模型，是 LLM-AHD 的开创性工作
- **EoH** (Liu et al., 2024): 启发式演化框架，结合代码与自然语言描述的双层表示
- **ReEvo** (Ye et al., NeurIPS 2024): 引入反思性演化，通过 verbal reflection 指导算法生成，是 DyACE 最直接的对比对象
- **启发**: DyACE 的闭环控制思想可推广到更广泛的 LLM-as-optimizer 范式——任何需要 LLM 迭代生成策略的场景（如 prompt 优化、reward design）都可能从"感知-推理-执行"的在线闭环中获益

## 评分

| 维度 | 分数 (1-10) | 说明 |
|------|------------|------|
| 新颖性 | 8 | 将 AHD 重新定义为非平稳控制问题的视角新颖且有理论深度 |
| 技术质量 | 8 | 框架设计系统性强，消融实验设计精妙，尤其 Blind 消融揭示了深层原理 |
| 实验充分性 | 7 | 三个基准问题覆盖面好，但缺少 wall-clock time 对比和跨实例泛化验证 |
| 写作质量 | 8 | 问题定义和数学建模清晰，从静态到动态的逻辑推导流畅 |
| 实用价值 | 7 | 推理延迟限制了实时应用，但为 LLM-AHD 领域指明了动态化方向 |
| **总分** | **7.6** | 理论贡献扎实，实验有力，是 LLM-based AHD 领域的高质量工作 |
