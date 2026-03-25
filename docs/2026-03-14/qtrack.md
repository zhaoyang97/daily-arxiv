# QTrack: Query-Driven Reasoning for Multi-modal MOT

**日期**: 2026-03-14  
**arXiv**: [2603.13759](https://arxiv.org/abs/2603.13759)  
**代码**: [QTrack](https://github.com/gaash-lab/QTrack)  
**领域**: 视频理解 / 多目标跟踪  
**关键词**: query-driven tracking, MOT, VLM reasoning, reinforcement learning, GRPO

## 一句话总结
提出 QTrack，将多目标跟踪从"跟踪所有物体"扩展为"根据自然语言查询推理并跟踪指定目标"，通过端到端 VLM + TAPO（时序感知策略优化）+ 结构化奖励实现语言条件化的时空推理跟踪，3B 模型即超越 GPT-5.2 等 10+ baseline，并构建 RMOT26 大规模 benchmark。

## 研究背景与动机

1. **领域现状**: 传统 MOT 关注"所有物体在哪"（trajectory estimation），按类别检测并关联。VLM 在多模态 grounding 上展现强能力，但跟踪和推理仍是松耦合——先 VLM 识别再交给 tracker，缺乏统一优化。

2. **现有痛点**: (a) 传统 MOT 不支持用户意图，无法根据语义指令选择性跟踪；(b) 现有 referring tracking 只做静态描述到目标的 grounding，不显式建模身份持续性和运动推理；(c) 缺乏同时评估推理能力和跟踪质量的 benchmark。

3. **核心 idea**: 将跟踪重新定义为语言条件化的时空推理问题——VLM 先推理"跟踪哪个目标"，再端到端预测目标轨迹，用 RL 优化序列级目标而非帧级损失。

## 方法详解

### 整体框架
输入视频帧序列 + 参考帧（含目标 bounding box）+ 自然语言查询 → VLM 生成 chain-of-thought 推理 + 结构化目标边界框轨迹。整体用 GRPO + TAPO 强化学习优化。

### 关键设计

1. **任务分解三层级**: 空间 grounding（单帧定位）、时序跟踪（跨帧身份关联）、关系推理（基于行为/交互的多目标推理，如"跟踪捡起红色背包后上出租车的人"）

2. **TAPO（Temporal Perception-Aware Policy Optimization）**: 构造时序损坏序列——将所有帧冻结为第一帧静态副本，计算原始输入 vs 损坏输入下策略输出的非对称 KL 散度，显式惩罚对时序信息不敏感的策略，迫使模型依赖运动线索而非仅静态外观

3. **结构化奖励**: (a) 格式奖励：检查推理/答案标签完整性；(b) IoU 奖励：Hungarian 匹配后 IoU>0.5 为正；(c) MCP 运动一致性奖励：$\text{MCP} = \frac{1}{T-1}\sum_{t=2}^{T} A_t \cdot S_t$，其中 $A_t$ 为方向余弦相似度、$S_t$ 为速度 Gaussian 惩罚

4. **RMOT26 Benchmark**: 从 DanceTrack / MOT16/17/20 / SportsMOT 等 7 个 MOT 数据集策划，查询由 Qwen-2.5-VL 生成以保证语言多样性，含单目标/多目标/遮挡感知三类查询，序列级划分防止身份泄漏

### 训练目标
$J_{\text{TAPO}} = J_{\text{GRPO}} + \gamma \cdot D_{\text{KL}}(\pi_{\theta}(\cdot|x) \| \pi_{\theta}(\cdot|\tilde{x}))$

其中 $\tilde{x}$ 为时序损坏输入，$\gamma$ 控制时序感知正则化强度。

## 实验关键数据

### RMOT26 主要结果（Table 2）

| 模型 | 参数 | MCP↑ | MOTP↑ | CLE(px)↓ | NDE↓ |
|------|------|------|-------|----------|------|
| Qwen2.5-VL-Instruct | 7B | 0.24 | 0.48 | 289.2 | 2.07 |
| Qwen3-VL-Instruct | 8B | 0.25 | 0.64 | 96.0 | 0.97 |
| Gemma 3 | 27B | 0.24 | 0.56 | 58.4 | 0.88 |
| Llama 3.2 Vision | 11B | 0.19 | 0.15 | 552.1 | 2.67 |
| InternVL | 8B | 0.21 | 0.66 | 117.4 | 0.64 |
| GPT-5.2 | - | 0.25 | 0.61 | 94.2 | 0.55 |
| **QTrack (Ours)** | **3B** | **0.30** | **0.75** | **44.61** | **0.39** |

QTrack 仅 3B 参数即全面超越所有开源/闭源模型：MCP 0.30（+20% vs Qwen3-VL）、CLE 降至 44.61px（GPT-5.2 为 94.2px）。

### 消融实验（3B 模型）

| 配置 | MCP↑ | MOTP↑ | NDE↓ |
|------|------|-------|------|
| VisionReasoner baseline | 0.21 | 0.44 | 2.32 |
| + GRPO | 0.22 | 0.65 | 0.96 |
| + MCP Reward | 0.25 | 0.61 | 1.06 |
| + TAPO | 0.24 | 0.72 | 0.82 |
| **QTrack (全部)** | **0.30** | **0.75** | **0.39** |

### 传统 MOT 对比
- **MOT17**: QTrack MOTP 0.87、HOTA 0.69，超越 MOTR (0.81/0.22) 和 BoostTrack++ (0.76/0.38)
- **DanceTrack**: QTrack MOTA 0.63、HOTA 0.66，超越 MOTRv2 (0.49/0.37)

### 关键发现
- 参数规模不决定时序推理能力：Gemma 27B (MCP 0.24) 不如 Qwen3 8B (0.25)，说明运动一致性需显式监督
- GRPO 显著提升空间对齐（MOTP 0.44→0.65）但 MCP 几乎不变（0.21→0.22），确认帧级优化不足以学习时序推理
- MCP 奖励和 TAPO 提供互补增益：前者监督运动一致性，后者正则化时序敏感性，缺一不可

## 亮点与洞察
- **范式转换**: 将 MOT 从"跟踪所有物体"重新定义为"推理后选择性跟踪"，统一了 where + which 两个维度
- **TAPO 时序损坏策略**简洁有效——冻结所有帧为首帧来移除运动信息，用 KL 散度惩罚不利用时间线索的策略
- **小模型大效果**: 3B QTrack 超越 GPT-5.2，说明任务特定的 RL 优化比纯粹 scaling 更高效

## 局限性
- 评估限于 query-specific 短片段而非完整视频，与传统 MOT 的全序列评估不完全可比
- 查询类型相对有限，复杂多步推理（如因果链）场景尚未覆盖
- VLM 处理长视频序列的效率是实际部署瓶颈

## 评分
- 新颖性: ⭐⭐⭐⭐ Query-driven tracking + TAPO 是 MOT 方向的新范式
- 实验充分度: ⭐⭐⭐⭐ 12 个 VLM baseline + 传统 MOT 对比 + 完整消融
- 写作质量: ⭐⭐⭐⭐ 问题定义清晰，实验分析有深度
- 价值: ⭐⭐⭐⭐ 推动 MOT 从感知向推理进化，3B 模型超闭源大模型有说服力
