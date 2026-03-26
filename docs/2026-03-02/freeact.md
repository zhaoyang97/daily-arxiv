# FreeAct: Freeing Activations for LLM Quantization

**日期**: 2026-03-02  
**arXiv**: [2603.01776](https://arxiv.org/abs/2603.01776)  
**代码**: 即将开源  
**领域**: LLM效率 / 模型量化  
**关键词**: LLM quantization, W4A4, activation transformation, diffusion LLM, multimodal LLM

## 一句话总结

FreeAct 打破现有量化方法中变换矩阵的"一对一"刚性约束，利用激活值的秩亏缺性质为不同 token 类型（masked/unmasked、vision/text）分配不同的变换矩阵，同时保持权重端统一静态变换，在 dLLM 和 MLLM 的 W4A4 量化上最高提升 5.3%。

## 研究背景与动机

1. **领域现状**：LLM 量化是降低部署成本的关键手段。近期基于变换矩阵的方法（QuaRot、FlatQuant）通过正交矩阵 $\mathbf{P}$ 将激活值投影到更平滑的空间再量化，效果显著优于简单的 per-channel scaling（SmoothQuant）。
2. **现有痛点 — 一对一约束**：这些方法要求 $\mathbf{P} \times \mathbf{P}^{-1} = \mathbf{I}$，即激活端和权重端必须使用互逆的同一对矩阵。权重在推理时是静态的，但输入激活值的分布是动态变化的——dLLM 中 masked 和 unmasked token 的激活值分布差异巨大（范围相差数倍），MLLM 中 vision 和 text token 同样分布迥异。一个固定的变换矩阵无法同时处理两种分布。
3. **核心矛盾**：现有工作（如时间感知量化、模态感知量化）也意识到了这种动态差异，但受限于逆矩阵唯一性的硬约束，只能在激活端做 per-token scale 的调整，无法在变换矩阵层面引入灵活性。
4. **切入角度**：作者观察到 LLM 的激活值矩阵通常是**秩亏缺的**（rank-deficient），行空间不满秩。基于此，作者在理论上证明满足等价性的变换矩阵解空间远大于简单的逆矩阵集合（Proposition 1），从而可以为不同激活类型分配不同变换，同时共享一个权重端矩阵。
5. **核心 idea**：**打破"一对一"约束，走向"多对一"变换——不同 token 类型用不同的激活变换矩阵 $\{\mathbf{P}, \mathbf{P}'\}$，共享同一个权重变换矩阵 $\tilde{\mathbf{P}}$，通过秩亏缺保证等价性**。

## 方法详解

### 整体框架

输入一个线性层的激活 $\hat{\mathbf{X}}$，按 token 类型（dLLM: masked/unmasked; MLLM: vision/text）索引分为 $\mathbf{X}$ 和 $\mathbf{X}'$。分别用不同变换矩阵 $\mathbf{P}$ 和 $\mathbf{P}'$ 变换后量化，再与统一变换后的量化权重 $\mathcal{Q}(\tilde{\mathbf{P}} \mathbf{W}^\top)$ 相乘。输出与原始 FP16 计算等价。

### 关键设计

1. **理论基础 — 超越逆矩阵（Proposition 1）**
   - 做什么：证明 $\mathbf{X}\mathbf{P}\tilde{\mathbf{P}}\mathbf{W}^\top = \mathbf{X}\mathbf{W}^\top$ 的解空间不仅包含 $\mathbf{P}\tilde{\mathbf{P}}=\mathbf{I}$，还包含 $\{\mathbf{Z} - \mathbf{P}_X(\mathbf{Z}-\mathbf{I})\mathbf{P}_W\}$ 整个集合
   - 核心思路：利用 Penrose (1955) 的双边矩阵方程 $\mathbf{AXB}=\mathbf{C}$ 的通解公式，其中 $\mathbf{P}_X$ 和 $\mathbf{P}_W$ 是激活和权重的行空间正交投影。当激活秩亏缺时（$\mathbf{P}_X \neq \mathbf{I}$），解集严格大于单元素 $\{\mathbf{I}\}$
   - 设计动机：为"多对一"变换提供理论合法性——不同 $\mathbf{P}$ 可以配同一个 $\tilde{\mathbf{P}}$

2. **Token 索引与动态分配**
   - 做什么：按 token ID 将序列分为两组（dLLM: [MASK] vs 非 [MASK]；MLLM: [IMG] vs 文本），为每组分配不同变换矩阵
   - 核心思路：构造带共享和独占子空间的变换矩阵：$\mathbf{P} = [\mathbf{U}, \mathbf{U}_X, \mathbf{0}]$，$\mathbf{P}' = [\mathbf{U}, \mathbf{0}, \mathbf{U}_{X'}]$，权重端 $\tilde{\mathbf{P}} = [\mathbf{U}, \mathbf{U}_X, \mathbf{U}_{X'}]^\top$，其中 $r + r_1 + r_2 = d$
   - 设计动机：$\mathbf{U}$ 保留两种激活的共享行空间；$\mathbf{U}_X$/$\mathbf{U}_{X'}$ 分别处理各自独特的子空间；零填充防止不同子空间的信息纠缠。等价性由 Theorem 2（正交分解下的投影不变性）保证

3. **误差最小化训练**
   - 做什么：在校准数据上逐层优化变换矩阵和量化参数
   - 核心思路：损失函数分别计算两种激活类型的量化误差 $\mathcal{L}_q = \mathbb{E}[\|\mathbf{XW} - \mathcal{Q}(\mathbf{XP})\mathcal{Q}(\tilde{\mathbf{P}}\mathbf{W}^\top)\|_2^2 + \|\mathbf{X'W} - \mathcal{Q}(\mathbf{X'P'})\mathcal{Q}(\tilde{\mathbf{P}}\mathbf{W}^\top)\|_2^2]$
   - 实现细节：随机正交矩阵初始化，AdamW 优化 15 epochs；默认 $r_1 = r_2 = d/32$（即每种特有子空间只占 3.1% 维度）

### 附加增强

- **可学习裁剪阈值**：激活端动态设定裁剪阈值，自由度更高
- **Per-channel Scale**：通道级缩放与变换协同
- **Kronecker 分解**：$\mathbf{P} := \mathbf{P}_l \otimes \mathbf{P}_r$，减少大矩阵存储和计算

### 实现极简

只需在原有 FlatQuant 代码上加 3 行：变换后对不同 token 类型 zero-mask 对应的独占子空间维度。$\mathbf{P}$ 和 $\mathbf{P}'$ 由 $\tilde{\mathbf{P}}$ 切片得到，无额外存储。

## 实验关键数据

### 主实验（W4A4 量化）

| 方法 | LLaDA (dLLM) Avg. | Dream (dLLM) Avg. | Qwen2.5-VL (MLLM) Avg. | InternVL2.5 (MLLM) Avg. |
|------|-------------------|-------------------|------------------------|-------------------------|
| 16-bit Baseline | 53.03 | 55.49 | 67.40 | 68.90 |
| RTN (W4A4) | 00.05 | 00.18 | 09.02 | 07.92 |
| SmoothQuant | 00.00 | 00.05 | 08.67 | 08.47 |
| QuaRot | 39.56 | 40.46 | 57.47 | 53.36 |
| FlatQuant | 49.20 | 48.16 | 65.59 | 56.53 |
| **FreeAct** | **51.01** | **50.48** | **66.22** | **57.25** |

### 消融实验

| 配置 | 关键指标 | 说明 |
|------|---------|------|
| FreeAct w/o 可学习裁剪 | LLaDA: HumanEval 34.15 / Dream: HumanEval 34.14 | 变换矩阵仍是主要贡献 |
| FreeAct 完整 | LLaDA: HumanEval 34.60 / Dream: HumanEval 50.00 | Dream 上裁剪阈值贡献显著 |
| 低秩验证：去掉 d/32 维 | 接近全秩上界 | 证实秩亏缺假设 |
| 低秩验证：去掉 d/4 维 | 大幅掉点 | 过度压缩不可行 |
| FreeAct_full（所有层统一比例） | 部分模型略降 | 按层调整比例更优 |

### 关键发现
- W4A4 下 RTN 和 SmoothQuant 几乎完全崩溃（dLLM 接近 0%），说明动态激活分布的处理至关重要
- FreeAct 在 dLLM 上的提升幅度最大（vs FlatQuant: LLaDA +1.81%，Dream +2.32%），因为 masked/unmasked 分布差异更极端
- 秩亏缺实验验证：仅去除 d/32 或 d/64 的维度就能接近全秩性能，证实了理论假设
- 量化误差可视化显示两种 token 类型的误差范围确实不同（$\mathbf{X} > \mathbf{X}'$），动态处理合理

## 亮点与洞察
- **理论驱动的实用设计**：从秩亏缺的理论出发推导出解空间，再设计具体的子空间分配方案，思路清晰且有数学保证。不是经验性的 trick，而是有严格等价性证明的方法
- **极简实现**：核心修改只需 3 行代码（在变换后对特定维度 zero-mask），无额外存储开销，易于集成到现有框架
- **统一框架**：将 dLLM（masked token）和 MLLM（vision token）的异质激活问题统一为"多对一变换"，避免针对不同模型类型设计不同量化策略

## 局限性 / 可改进方向
- 目前仅支持 **2 种 token 类型**的区分，无法处理 3 种及以上模态（如音频+视觉+文本）
- 受限于资源，未在更大模型（70B+）上验证
- 使用 fake quantization 评估，未部署到硬件上测试真实加速比
- 每层的 $r_1/r_2$ 比例固定为 $d/32$，未逐层自适应调整——按层分析后针对性设置可能进一步提升

## 相关工作与启发
- **vs FlatQuant**: FlatQuant 将 Hadamard 变换推广到仿射变换，但仍然是一对一约束。FreeAct 在此基础上进一步放松为多对一，是变换方法的自然演进
- **vs QuaRot**: QuaRot 用随机 Hadamard 矩阵消除 outlier，更简单但灵活性最低。FreeAct 的提升主要来自对不同 token 类型的差异化处理
- **vs SmoothQuant**: 同属变换类方法，但 SmoothQuant 只做对角缩放，在 W4A4 下完全失效，说明仅靠 channel-wise 调整不够

## 评分
- 新颖性: ⭐⭐⭐⭐ 从秩亏缺推导出多对一变换的理论新颖，但子空间构造方案相对直觉
- 实验充分度: ⭐⭐⭐⭐ 4 个模型 × 6 个 benchmark + 消融 + 可视化，但缺少真实硬件延迟测试
- 写作质量: ⭐⭐⭐⭐⭐ 理论推导严谨，实验讲故事清晰，三个 RQ 组织合理
- 价值: ⭐⭐⭐⭐ 对 dLLM/MLLM 量化有实际意义，3 行代码改动极其工程友好
