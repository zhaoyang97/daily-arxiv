# Agentic Planning with Reasoning for Image Styling via Offline RL

**日期**: 2026-03-07  
**arXiv**: [2603.07148](https://arxiv.org/abs/2603.07148)  
**代码**: [HuggingFace](https://huggingface.co/datasets/subhojyoti1990/image-agent-styling)  
**领域**: 图像生成  
**关键词**: Offline RL, Image Styling, Tool-Based Planning, Chain-of-Thought Reasoning, Reward-Weighted Fine-tuning

## 一句话总结

提出基于工具的 agentic RL 后训练框架，将复杂图像风格化任务分解为可组合的原子工具调用序列，结合链式推理 (CoT) 与 offline RL（Reward-Weighted / Standardized Reward-Weighted）训练小型 VLM planner（Qwen3-VL 4B/8B），在图像质量和指令遵循上超越直接 prompt 编辑和 GPT-4o 零样本基线。

## 研究背景与动机

当前图像风格化主要依赖直接 prompt 编辑——用户用自然语言指令让基础模型生成/修改图像。然而该范式存在根本性局限：

1. **Prompt 模糊性**：自然语言 prompt 往往不精确，无法指定需要修改哪些视觉维度、修改顺序以及如何平衡竞争需求。例如"Transform to golden-hour winter wonderland with magical snowfall"实际上需要协调时间光照（golden-hour 暖色调）、季节变化（冬季美学）、天气效果（降雪）、氛围一致性和结构保持等多个维度。
2. **复合变换失败**：直接 prompt 编辑在多维度复合变换上表现差，产生颜色不一致、结构伪影和指令遵循度低的结果。
3. **缺乏结构化推理**：单次 prompt-to-image 的映射缺少显式的多步推理过程，模型无法像人类一样分步规划编辑策略。

核心直觉：利用**组合式图像编辑工具**而非直接 prompting，通过结构化的 agent 级规划和显式推理来分解复杂风格化任务，可以获得更好的结果。

## 方法详解

### 整体框架

提出四阶段结构化编辑流水线 (Four-Stage Structured Editing Pipeline)：

| 阶段 | 输入 | 输出 | 说明 |
|------|------|------|------|
| Stage 1: 提取结构化上下文 | 编辑目标 $e_i$, 原始图像 $I_i$ | 上下文 $c_i$ | 提取图像当前视觉状态的 10 维文本描述 |
| Stage 2: 带推理的规划 | $e_i$, $c_i$ | 推理链 $\{z_{i,j}\}$, 动作序列 $\{a_{i,j}\}$ | 生成 2-5 步工具调用及每步 CoT 推理 |
| Stage 3: 合成精确指令 | $e_i$, $c_i$, 推理链, 动作序列 | 精确编辑指令 $\hat{e}_i$ | 将模糊 prompt 转化为详细精确的编辑指令 |
| Stage 4: 渲染最终图像 | $\hat{e}_i$, $I_i$ | 编辑后图像 $\hat{I}_i$ | 使用冻结的 Qwen-Image-Edit 执行编辑 |

核心贡献在 Stage 1-3（规划与推理），Stage 4 使用冻结的黑盒编辑器，将规划问题与执行问题解耦。

### 关键设计

**1. 组合式工具库 (Compositional Tool Library)**

设计了包含 10 个正交维度的参数化工具库：

- `location_setting`：场景位置
- `architecture_style`：建筑风格
- `time_period`：时代
- `time_of_day`：时间/光照
- `season`：季节
- `weather`：天气
- `mood_lighting`：氛围光照
- `color_grading`：调色
- `artistic_medium`：艺术媒介
- `atmospheric_effects`：大气效果

每个维度控制一个视觉方面且相互干扰最小，从有限原语创造无限组合空间。

**2. 每步链式推理 (Per-Step Chain-of-Thought Reasoning)**

对计划中的每个工具调用，模型先生成推理解释为何选择该工具，例如：

> Tool: `time_of_day(sunset)` → Reasoning: "Setting golden-hour lighting creates warm sunset tones that enhance the winter atmosphere while providing natural illumination."

这种 reasoning-action 交替训练模型"先思考后行动"，提升动作质量和指令遵循。

**3. 合成数据生成流水线**

使用 teacher-student 范式：Qwen3-VL-8B-Instruct 作为 teacher 生成轨迹，训练小型 student（4B/8B）。生成三个大规模数据集：

| 数据集 | 轨迹数 | 步数 | 主题数 | 特点 |
|--------|--------|------|--------|------|
| Simple | 10,000 | 1-2 | - | 原子变换（如只改时间） |
| Regular | 10,000 | 3-5 | 10 | 组合变换（室内设计主题） |
| Complex | 10,000 | 3-5 | 83 | 高难度+保持约束+多样主题 |

每条轨迹包含结构化上下文、多步动作计划+CoT 推理、质量分数 $r_i \in [0,5]$。

**4. Offline RL 训练算法**

提出五种训练方法：

- **Standard (S)**：标准 SFT，忽略奖励信号
- **RL (R)**：奖励过滤，只保留 $r_i \geq 4.0$ 的轨迹（约 65%）
- **DPO (D)**：对比偏好学习，从 chosen/rejected 轨迹对中学习
- **Reward-Weighted (RW)**：按奖励分数加权每条轨迹的梯度贡献，$w(r_i) = \max\{r_i - 3.0, 0\}$
- **Standardized Reward-Weighted (SW)**：对奖励做 z-score 标准化后加权，$\tilde{r}_i = \frac{r_i - \bar{r}}{\sigma_r}$，权重可为负值，低于均值的轨迹被抑制

RW 和 SW 是核心算法贡献——保留所有数据的多样性，同时通过连续奖励加权强调高质量样本。

## 实验关键数据

评估设置：3 个数据集 × 2 种模型大小（4B/8B）× 2 种模态（Text-only/Vision）= 12 种配置，GPT-4o 作为评估器，200 个测试样本，6 个图像质量维度（0-100 分）。

### 主实验

| 配置 | 最佳方法 | Overall 分数 | 相比 Edit-Only 提升 | 相比 GPT-4o |
|------|----------|-------------|-------------------|-------------|
| Regular Text-4B | SW | 78.77 | +1.3~7.3 pts | 超越 |
| Regular Text-8B | SW | 77.86 | +1.3~7.3 pts | 超越 |
| Simple Vision-4B | RW | 79.33 | +1.3~7.3 pts | 超越 |
| Complex Vision-8B | DPO | 85.41 | +1.3~7.3 pts | 超越 |

关键结论：在 11 种配置中的 10 种，训练后的 4B/8B 模型在图像质量上超越 GPT-4o 零样本基线。

### 消融实验

| 因素 | 发现 | 最佳方法 | 说明 |
|------|------|----------|------|
| 任务复杂度 | 组合文本任务偏好 SW | SW (78.77/77.86) | 标准化加权支持组合推理 |
| 视觉模态 | 简单视觉任务偏好 RW | RW (79.33) | 视觉接地放大连续奖励加权效果 |
| 主题多样性 | 多样主题偏好 DPO | DPO (85.41) | 对比学习适合分布多样的场景 |
| Action Planning | Edit-Only 始终最差 | - | Overall 落后最佳方法 1.3-7.3 分 |
| CoT 推理 | 所有训练方法 >> Baseline | - | 显式推理痕迹显著改善规划指标 |
| 人类验证 | 77% 通过率 | - | 3,000 样本，3 名标注员独立评估 |

### 关键发现

1. **Offline RL 有效**：SW 在组合文本任务最优，RW 在简单视觉任务最优，DPO 在多样主题分布最优。
2. **Action Planning 不可或缺**：Edit-Only 在 Overall 分数上始终落后，表明直接 image-to-image 编辑缺乏指令遵循编辑所需的结构化推理。
3. **视觉接地放大连续奖励加权**：RW 在 Vision 模型上获得最强增益（Simple Vision-4B 达 79.33），在视觉接地指标上领先高达 1.24 分。
4. **标准化加权支持组合推理**：SW 在 Regular Text 配置上获最高 Overall（Semantic Accuracy 76.58/74.53，Instruction Following 77.55/77.00）。
5. **每步 CoT 提升规划质量**：所有训练方法在规划指标上大幅超越未微调的 Baseline。

## 亮点与洞察

- **规划与执行解耦**的设计理念非常优雅——冻结图像编辑器、专注训练 planner，使得小模型（4B）也能胜过 GPT-4o 这种大模型的零样本能力。
- **Standardized Reward-Weighted (SW)** 借鉴了策略梯度中经典的方差缩减技巧（REINFORCE baseline, GAE, PPO, GRPO），巧妙地将其迁移到 offline distillation 场景，均值以上正权重、以下负权重的设计使训练更稳定。
- **组合式工具库** 用 10 个正交维度构建可解释且可组合的编辑空间，既比端到端 prompt 编辑更可控，又避免了手工设计规则的脆弱性。
- 三个不同复杂度数据集的系统实验揭示了一个重要 insight：**没有单一最优 RL 方法**，最佳策略取决于任务复杂度、模态和主题多样性。
- 人类验证（77% 通过率 + GPT-4o 二次验证）为合成数据质量提供了可靠基线。

## 局限性 / 可改进方向

1. **工具库固定为 10 维**：当前正交维度是手工设计的，无法覆盖所有可能的视觉变换（如纹理细节、物体添加/删除等），扩展到更大工具库是重要方向。
2. **依赖冻结编辑器**：Stage 4 的 Qwen-Image-Edit 质量上限决定了最终效果天花板，planner 再好也无法弥补编辑器的能力不足。
3. **Offline RL 不适应改进策略**：offline 方法不会根据 improving policy 调整轨迹，online RL 或 iterative data generation 可能进一步提升性能。
4. **评估依赖 GPT-4o**：VLM-as-a-Judge 与人类判断仅中等相关（top-2 accuracy 76-83%），自动评估的可靠性存疑。
5. **仅限静态图像**：未扩展到视频编辑（需要时间一致性），论文提到这是未来方向。
6. **合成数据偏差**：teacher 模型（Qwen3-VL-8B）的生成偏差可能限制 student 的上限。

## 相关工作与启发

- 经典风格迁移（Gatys et al., 2016; CycleGAN）→ 直接 prompt 编辑（InstructPix2Pix, MagicBrush）→ 本文的**结构化规划编辑**，代表了图像风格化方法论的演进。
- **Reward-Weighted Regression** 有悠久历史：Peters & Schaal (2007) 最早提出，Peng et al. (2019) 提出 AWR，本文将其应用到 VLM planner 训练。
- **Plan-then-Execute** 范式与近期 LLM Agent 研究（ReAct, Toolformer）思路一致，但本文将其体系化地应用于图像编辑领域。
- 对 **offline RL 后训练** 的系统性实验（SFT → 过滤 → DPO → RW → SW）提供了一个实用的方法对比框架，可以迁移到其它 agent 任务。
- 启发：在需要多步组合推理的创意任务中，小模型 + 结构化规划 + reward-aware 训练 可能是比直接用大模型更高效的路径。

## 评分

| 维度 | 分数 (1-5) | 说明 |
|------|-----------|------|
| 新颖性 | 3.5 | 各组件（工具库、CoT、offline RL）并非全新，但组合方式和系统性框架有创新 |
| 技术深度 | 4.0 | 5 种训练算法的系统比较，理论动机清晰，SW 的设计有新意 |
| 实验充分性 | 4.0 | 12 种配置 + 30K 轨迹 + 人类验证，覆盖面广 |
| 实用价值 | 3.5 | 开源数据集+代码，4B 模型超越 GPT-4o 有实际意义 |
| 写作质量 | 3.5 | 结构清晰但篇幅冗长（附录非常多），核心贡献有时被细节淹没 |
| **综合** | **3.7** | 扎实的系统性工作，为创意域 agent 规划提供了实用框架 |
