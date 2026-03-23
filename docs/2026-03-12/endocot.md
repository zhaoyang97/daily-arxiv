# EndoCoT: Scaling Endogenous Chain-of-Thought Reasoning in Diffusion Models

**日期**: 2026-03-12  
**arXiv**: [2603.12252](https://arxiv.org/abs/2603.12252)  
**代码**: [GitHub](https://github.com/InternLM/EndoCoT)  
**领域**: 图像生成 / 扩散模型推理  
**关键词**: chain-of-thought, diffusion model, visual reasoning, iterative refinement, latent reasoning

## 一句话总结
提出 EndoCoT，通过在 MLLM 中迭代精炼隐式思维状态并桥接到 DiT 去噪过程，实现扩散模型内生的链式思维推理，在 Maze/TSP/Sudoku/VSP 四个视觉推理 benchmark 上平均 92.1% 准确率，超越最强基线 DiffThinker 8.3 个百分点。

## 研究背景与动机

1. **领域现状**: 扩散模型已广泛集成 MLLM 作为文本编码器来处理复杂任务（如空间推理），但 MLLM 只被用作静态条件编码器——计算一次文本嵌入后就不再更新。

2. **现有痛点**: 两个关键瓶颈：(i) 单步推理不足——MLLM 的单次前向传播无法激活 CoT 过程，复杂约束无法在一次编码中完全捕获；(ii) 指导信号在解码过程中保持不变——静态嵌入无法让 DiT 逐步分解复杂指令。

3. **核心矛盾**: DiffThinker 等方法虽然尝试注入推理，但实际是"表面对齐"而非真正推理。实验发现这些模型在前几步去噪就锁定了最终方案，之后只是优化视觉质量。当推广到新领域时会灾难性失败。

4. **核心 idea**: 让扩散模型在生成过程中进行内生的 CoT 推理——通过迭代精炼 MLLM 的隐式思维状态，并动态桥接到 DiT 的去噪过程。

## 方法详解

### 整体框架
输入：文本提示 + 图像 → MLLM 编码为 prefix embeddings **P** → 迭代 $\mathcal{T}$ 步思维精炼 → 每步条件化 DiT 生成中间视觉输出 → 最终输出。核心是让推理过程和生成过程耦合。

### 关键设计

1. **Iterative Thought Guidance（迭代思维引导）**:
   - 做什么：在 MLLM 的隐空间中迭代更新思维状态 $\mathbf{h}_\tau$
   - 核心思路：第 $\tau$ 步将上一步的隐状态 $\mathbf{h}_{\tau-1}$ 拼接到 prefix 后面送入 MLLM，提取新位置的隐状态作为 $\mathbf{h}_\tau$：$\mathbf{h}_\tau = \mathbf{e}_{L+1}^\top f_\phi([\mathbf{P}; \mathbf{h}_{\tau-1}])$。关键是 $\mathbf{h}_{\tau-1}$ 直接作为高维输入送入 MLLM 第一层，绕过离散 embedding 查找表
   - 每一步推理产生的 $\mathbf{h}_\tau$ 条件化一次完整的 DiT 去噪轨迹（从噪声到图像），而非共享同一次去噪
   - 设计动机：模拟人类解题——不试图一次生成完整方案，而是逐步精炼

2. **Terminal Thought Grounding（终端思维锚定）**:
   - 做什么：将最终推理状态与文本监督对齐，防止推理轨迹漂移
   - 核心思路：用 ground-truth 推理步骤的文本编码得到参考状态 $\mathbf{h}_\text{ref}$，通过 L2 loss 对齐最终状态：$\mathcal{L}_\text{align} = \|\mathbf{h}_\mathcal{T} - \mathbf{h}_\text{ref}\|^2$
   - 只在最终步 $\tau=\mathcal{T}$ 激活对齐 loss，避免过早约束中间探索
   - 设计动机：纯视觉监督存在模态鸿沟，需要文本锚点防止累积漂移

3. **Progressive Training（渐进训练）**:
   - **Stage 1 (Reasoning Development)**: 监督所有推理步 $\tau=1,...,\mathcal{T}$ 的中间输出，学习逐步推理轨迹
   - **Stage 2 (Terminal Consolidation)**: 冻结中间步梯度，只优化最终输出，短周期微调以保留已学到的推理链

### 损失函数 / 训练策略
- Stage 1: $\mathcal{L}_\text{stage1} = \sum_\tau (\mathcal{L}_\text{FM}^\tau + \mathbb{I}_{\{\tau=\mathcal{T}\}} \lambda_\text{align} \mathcal{L}_\text{align})$
- Stage 2: $\mathcal{L}_\text{stage2} = \mathcal{L}_\text{FM}^\mathcal{T} + \lambda_\text{align} \mathcal{L}_\text{align}$
- 基于 Qwen-Image-Edit-2511，LoRA rank=32，lr=$1 \times 10^{-4}$，训练 55 epochs

## 实验关键数据

### 主实验

| 任务 | 难度 | EndoCoT | DiffThinker | 提升 |
|------|------|---------|-------------|------|
| Maze-8 | 低 | 100% | 100% | +0 |
| Maze-32 | 高 | **90%** | 65% | **+25%** |
| Sudoku-35 | 高 | **95%** | 55% | **+40%** |
| VSP-Super-32 | 高 | **85%** | 80% | +5% |
| **平均** (18项) | - | **92.1%** | 83.8% | **+8.3%** |

### 消融实验

| 配置 | Maze-8 ACC | Maze-32 ACC | 说明 |
|------|-----------|-------------|------|
| Full model | 100% | 90% | 完整模型 |
| w/o semantic loss | 39% | 14% | 去掉终端锚定 loss 后崩溃 |
| Explicit token | 34% | 0% | 用显式 token 替代隐式状态完全失败 |

### 关键发现
- **Terminal Thought Grounding 至关重要**：去掉后 Maze-32 从 90%→14%，说明纯视觉监督无法维持长程推理一致性
- **隐式 latent token 远优于显式 token**：显式 token 在 Maze-32 上直接 0%
- 推理步数 $\mathcal{T}$ 可在推理时灵活调节——天然支持 test-time scaling
- 统一训练（所有任务合练）仍保持竞争力，说明推理能力可跨任务迁移

## 亮点与洞察
- **首次在扩散模型中实现内生 CoT**：不是把推理结果注入扩散模型，而是让扩散模型自己在隐空间迭代推理。与 LLM 的 CoT 在理念上统一但在实现上创新
- **分析驱动的设计**：通过层级敏感性分析和注意力熵分析定位了问题本质（MLLM 是推理主力但单步不够、DiT 擅长空间定位但需动态条件），然后对症下药
- **渐进训练策略解耦了推理学习和输出质量**：先学推理路径，再固化输出质量，避免梯度冲突

## 局限性 / 可改进方向
- 每步推理需要完整的 DiT 去噪，计算开销随 $\mathcal{T}$ 线性增长
- 仅在结构化推理任务（迷宫、数独等）验证，自然图像编辑场景的泛化有待探索
- 中间推理步需要 ground-truth 分解作为监督，数据构造成本较高

## 相关工作与启发
- **vs DiffThinker**: DiffThinker 尝试在 MMDiT 内部注入推理，但本质是 pattern matching 而非真正推理；EndoCoT 通过迭代隐状态精炼实现了真正的逐步推理
- **vs Latent Sketchpad**: Latent Sketchpad 在自回归模型中用视觉 latent 交错推理；EndoCoT 将类似思想引入扩散框架

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 首次实现扩散模型内生 CoT，分析扎实
- 实验充分度: ⭐⭐⭐⭐ 四个 benchmark + 消融 + 统一训练
- 写作质量: ⭐⭐⭐⭐⭐ 分析驱动设计，逻辑清晰
- 价值: ⭐⭐⭐⭐ 为扩散模型推理开辟了新方向
