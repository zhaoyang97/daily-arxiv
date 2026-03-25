# One-Step Flow Policy: Self-Distillation for Fast Visuomotor Policies

**日期**: 2026-03-12  
**arXiv**: [2603.12480](https://arxiv.org/abs/2603.12480)  
**代码**: 无  
**领域**: 图像生成 / 机器人策略  
**关键词**: flow matching, self-distillation, one-step, visuomotor policy, consistency

## 一句话总结
提出 One-Step Flow Policy (OFP)，通过从零开始的自蒸馏框架（自一致性 loss + 自引导正则化 + warm-start），无需预训练教师即可实现单步动作生成——在 56 个仿真操作任务上 1-NFE 平均成功率 71.6%，超越 100 步 DP3 基线（66.4%），推理仅需 17.58 ms（加速 183×）。

## 研究背景与动机

1. **领域现状**: 基于 flow/diffusion 的机器人策略（如 Diffusion Policy、FM Policy）能有效建模多模态动作分布，但采样需要 10-100 步 ODE 求解，每次动作生成需要数秒。
2. **现有加速方案的不足**:
   - Consistency Policy (CP): 依赖预训练 teacher 做蒸馏，且 mode-covering 特性导致单步预测过于平滑，精度不足
   - OneDP: 使用 score distillation，mode-seeking 产生尖锐但多样性不足的动作，且只支持单步推理无法灵活调整
   - MeanFlow (MP1): 训练中引入 Jacobian-vector products (JVPs)，内存开销大且优化不稳定
3. **核心动机**: 能否设计一个无需预训练教师、从零训练的自蒸馏框架，同时兼顾单步精度和多步灵活性？

## 方法详解

### 1. Self-Consistency Loss（自一致性损失）
- 对 flow ODE 轨迹上不同时间步的点，强制模型预测映射到同一终点
- 类似 Consistency Model 的思想，但不需要教师——模型自身在不同时间区间的预测作为一致性约束
- 主要作用：保证 few-step 推理的可靠性

### 2. Self-Guided Regularization（自引导正则化）
- 借鉴 Classifier-Free Guidance 思想：模型同时学习条件/无条件速度场
- 两者的差异（score 差）作为分布级别的修正信号，将预测推向高密度专家模式
- 主要作用：驱动单步推理的性能提升，避免 mode-averaging

### 3. Warm-Start Mechanism（热启动，无需训练）
- 利用机器人动作的时间连续性：相邻时间步的动作高度相关
- 推理时用前一步动作预测初始化当前步的噪声起点，缩短 flow 传输距离
- 训练无关（training-free），在任意 NFE 下都能提升性能

### 设计优势
- 不需要预训练教师模型，端到端从零训练
- 不引入 JVP 计算，训练稳定且内存友好
- 支持灵活 NFE：单步低延迟 or 多步高精度

## 实验关键数据

### 2D 图像条件操控（7 个任务，Adroit + DexArt）

| 方法 | NFE | 平均成功率 |
|------|-----|-----------|
| DP (Diffusion Policy) | 100 | 64.2% |
| FM Policy | 100 | 67.2% |
| CP | 1 | 59.7% |
| OneDP | 1 | 63.3% |
| MP1 | 1 | 60.5% |
| **OFP (Ours)** | **1** | **68.3%** |

### 3D 点云条件操控（56 个任务，Adroit + DexArt + MetaWorld）

| 方法 | NFE | Adroit (3) | MetaWorld Easy (28) | MetaWorld Hard (5) | 平均 |
|------|-----|-----------|-------------------|-------------------|------|
| DP3 | 100 | 79.0% | 82.8% | 38.3% | 66.4% |
| FM Policy | 100 | 83.3% | 68.9% | 43.6% | 59.8% |
| OneDP | 1 | 77.3% | 77.7% | 38.7% | 62.4% |
| **OFP** | **1** | **85.0%** | **87.9%** | **43.3%** | **71.6%** |

### 推理速度
- OFP: **17.58 ms**/action chunk vs DP3 (NFE=100): 3225.67 ms → **183× 加速**
- vs FM Policy (NFE=100): 1865.72 ms → **106× 加速**

### VLA 集成（π₀.₅ + RoboTwin 2.0，4 个任务）
- OFP (NFE=1) 平均成功率 **94.7%**，超越原始 π₀.₅ (NFE=10) 基线
- 对比其他加速方法（CFM、Shortcut Models、iMF）均取得最高平均成功率

### 灵活 NFE 与数据效率
- OFP NFE=1 → 4 时性能从 64.5% 提升到 66.2%，支持延迟-精度灵活权衡
- 数据稀缺场景（20 demos）下 OFP 维持 32.7% 成功率，MP1 急剧退化

### 消融实验
- 自一致性损失：保证 few-step 推理的可靠性
- 自引导正则化：驱动单步性能提升
- Warm-start：训练无关的推理先验，在任意 NFE 下一致提升

## 亮点与洞察
- 三种机制互补优雅：一致性保证多步、引导保证单步精度、热启动利用领域先验
- 单步生成反而超越 100 步基线，体现了自蒸馏的正则化效果
- 在大规模 VLA（π₀.₅）上依然有效，证明方法不局限于小模型
- 与同期 OneDP 形成对比：OFP 不需要教师且支持灵活 NFE

## 评分
- 新颖性: ⭐⭐⭐⭐ 自蒸馏三机制组合新颖，warm-start 利用领域特性
- 实验充分度: ⭐⭐⭐⭐⭐ 56 任务 + π₀.₅ 集成 + 消融 + 数据效率分析
- 价值: ⭐⭐⭐⭐ 实用的策略加速方案，183× 加速且性能不降反升
