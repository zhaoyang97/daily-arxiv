# RIVER: A Real-Time Interaction Benchmark for Video LLMs

**日期**: 2026-03-04  
**arXiv**: [2603.03985](https://arxiv.org/abs/2603.03985)  
**代码**: https://github.com/OpenGVLab/RIVER  
**领域**: 视频理解  
**关键词**: online video understanding, real-time interaction, benchmark, streaming video, Video LLM

## 一句话总结

RIVER Bench 提出了首个精确定义在线交互时序的视频 LLM 评测基准，包含 Retrospective Memory / Live-Perception / Proactive Response 三类任务共 4,278 道题，并通过长短期记忆模块和专用训练数据将离线模型的在线交互能力提升 11%+。

## 研究背景与动机

1. **领域现状**：GPT-4o、Gemini 等 MLLM 在离线设置下表现不错，但几乎都是"看完整段视频再回答"的离线范式，无法支持 AR 导航、机器人任务监督等实时交互场景。
2. **现有痛点**：现有在线视频基准（VStream-QA、OV-Bench、OVO-Bench）评测格式仍近似离线 benchmark——要么缺少精确的时间标注，要么只覆盖回忆/即时中的一两种能力，无法全面度量在线交互。
3. **核心矛盾**：在线交互要求模型同时具备三种时间感知能力——（1）长期记忆保持，（2）即时感知准确，（3）主动预判时机——但现有 benchmark 无法联合评测这三项，也缺少对"记忆衰减曲线"和"响应时效性"的定量刻画。
4. **本文要解决什么？** 设计精确定义 query time / cue time / response time 的在线交互基准；量化记忆随时间的衰退规律；提供通用方法让离线模型支持在线推理。
5. **切入角度**：从人机对话的时序关系出发，把在线交互递归定义为 $\mathcal{L} = -\log P_\theta(r_t | \mathbf{V}_{t':t}, q, h_{<t'}, r_{<t})$，然后按查询事件发生时间 $t_\mathbf{V}$ 与当前时间 $t$ 的关系划分三类任务。
6. **核心 idea 一句话**：用精确时间标注 + 三任务分类 + 长短期记忆模块，构建首个量化在线视频交互能力的 benchmark。

## 方法详解

### 整体框架

RIVER 由两部分组成：（1）**RIVER Bench** —— 1,067 个视频、4,278 道题的评测基准；（2）**通用在线推理方法** —— 滑动窗口 + 长短期记忆模块，让任意离线 MLLM 支持在线推理。

输入：流式视频帧 + 带时间戳的用户查询。输出：模型在正确时间点给出准确回答。

### 关键设计

1. **三类交互任务定义**：
   - **Retro-Memory**：事件发生在过去（$t_\mathbf{V} < t'$），查询涉及历史记忆。按时间间隔分 short/medium/long/very long 四档（15s~3600s）。
   - **Live-Perception**：事件发生在当前窗口（$t' \le t_\mathbf{V} \le t$），测试即时视觉理解。
   - **Pro-Response**：事件尚未发生（$t_\mathbf{V} > t$），模型需持续监控视频流，在条件满足时主动响应。又分 Instant（单次回答）和 Stream（持续描述）两种。
   - 设计动机：三类任务完整覆盖"过去/现在/未来"三个时间维度，且通过 $\Delta = \|t_\mathbf{V} - t\|$ 量化性能随时间间隔的变化。

2. **长短期记忆模块（使离线模型支持在线推理）**：
   - 短期记忆 = 当前滑动窗口（1fps 采样）的视频帧 token。
   - 长期记忆 = 固定 $M$ 个 slot，每个 slot 的 token 数与短期记忆相同。新帧输入时通过最近邻平均（nearest-neighbor averaging）合并最相似的 slot 对，保持 slot 数不增长。
   - 设计动机：模拟人类"将相邻时间事件整合为高级语义表征"的记忆机制，用可控内存处理超长视频（最长 120 分钟）。
   - 通过 system prompt 显式告知模型时间线信息："long memory of 0.0 to X seconds" + "short memory sampled from Y to Z seconds"。

3. **数据构建与质量控制**：
   - 数据来源：Vript-RR、LVBench、LongVideoBench、Ego4D、QVHighlights 五个公开数据集。
   - 多阶段过滤：rule-based 去掉过于简单/模糊的问题 → LLM 去掉不看视频也能答对的问题 → 语义相似度筛选独特事件作为锚点。
   - Pro-Response 训练数据使用随机时间戳（而非默认 0 秒）提升泛化性。

4. **评测指标设计**：
   - Retro-Memory & Live-Perception：MC 选择题准确率 + 开放式（OE）GPT 评分。
   - Pro-Response：Response Accuracy Metric —— 在容忍窗口 $w$ 内满分，早回答直接 0 分（惩罚误报），晚回答线性衰减。

### 训练策略

在线模型训练基于 VideoLLM-Online 架构（SigLIP-Large 编码器 + 2 层 MLP + LLaMA3-8B），使用 LoRA（r=128, α=256），4fps 采样，单 epoch 训练，lr=3e-5，DeepSpeed ZeRO-2。损失 = LM loss + streaming loss。

## 实验关键数据

### 主实验（核心在线能力评测）

| 模型类别 | 模型 | Retro-Memory MC | Live-Perception MC | Pro-Response Loc MC |
|----------|------|-----------------|-------------------|-------------------|
| 闭源 | GPT-4o | 59.56 | 61.05 | 1.63 |
| 闭源 | Gemini-1.5-pro | 36.35 | 52.19 | 1.51 |
| 离线开源 | InternVL2.5 (16F) | 42.68 | 43.65 | — |
| 离线开源 | LLaVA-Video (16F) | 49.52 | 50.88 | — |
| +在线适配 | VideoChat-Flash (1fps) | **52.90** | **54.45** | 3.92 |
| +在线适配 | LLaVA-Video (1fps) | 45.40 | **55.75** | 3.56 |
| 原生在线 | VideoLLM-Online | 28.61 | 29.83 | 3.63 |
| +RIVER训练 | VideoLLM-Online+RIVER | 28.44 | 30.10 | **14.91** |

### 记忆衰减分析（Retro-Memory 按时间间隔细分）

| 模型 | Short (15-30s) | Medium (30-60s) | Long (300-900s) | Very Long (1800-3600s) |
|------|---------------|-----------------|-----------------|----------------------|
| GPT-4o | 63.26 | 63.26 | 58.01 | 52.21 |
| VideoChat-Flash +在线 | 55.28 | 54.52 | 51.73 | 50.17 |
| Flash-VStream（原生在线） | 33.15 | 34.57 | 33.92 | 34.38 |

### 关键发现
- **离线 vs 在线差距巨大**：离线模型在单 QA 任务表现尚可，但置入严格实时场景后性能严重下降，尤其 Pro-Response 几乎为零。
- **长短期记忆有效**：加入记忆模块后，中长期记忆问题的衰减斜率降低约 12%，且在 1 小时内表现出比人类 Ebbinghaus 遗忘曲线更好的保持性。
- **训练数据关键**：仅用 RIVER 训练数据微调 VideoLLM-Online，Pro-Response 准确率从 3.63% 提升至 14.91%（+11.28%）。
- **视觉线索类型影响显著**：因果线索（Causal Cue）最难，所有模型在此类问题上表现最差，揭示视觉感知与事件归因推理的脱节。

## 亮点与洞察
- **时间维度的精确定义是核心贡献**：不同于之前 benchmark 只分"过去/现在/未来"，RIVER 精确标注了 query/cue/response 三个时间点，使得"记忆衰减曲线"和"响应时效性"首次可被定量分析。
- **长短期记忆融入 prompt 而非架构**：通过 system prompt 注入时间线信息，实现了与任意现有 MLLM 的即插即用兼容——这种"不改架构只改 prompt"的思路可迁移到其他时序任务。
- **Pro-Response 零分现象**：几乎所有离线模型在主动响应任务上得分近零，说明这是当前 Video LLM 的系统性盲区。

## 局限性 / 可改进方向
- 不包含音频模态——实际在线交互中声音是最易获得的实时信号。
- Pro-Response 的 Stream 类型（持续描述）评测较粗糙，缺少细粒度的语义对齐指标。
- 长期记忆的 nearest-neighbor averaging 策略较简单，可能丢失关键细节——可探索基于 attention 的选择性遗忘。
- 数据来源均为现有公开数据集的重组，缺少专门录制的在线交互数据。

## 相关工作与启发
- **vs OVO-Bench**：OVO-Bench 也分过去/现在/未来，但缺少精细时间分割；RIVER 精确到秒级标注，且增加了记忆衰减分析。
- **vs VideoLLM-Online**：VideoLLM-Online 关注流式推理但评测偏流畅度；RIVER 从准确性和时效性两个维度联合评测。
- **vs StreamForest**：StreamForest 关注记忆压缩效率；RIVER Bench 的 Retro-Memory 测试恰好可以评测这类方法在不同时间跨度下的表现。

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个精确定义在线交互时序的 Video LLM benchmark，三任务分类和记忆衰减曲线分析有新意
- 实验充分度: ⭐⭐⭐⭐ 覆盖闭源/开源/在线/离线四类模型，消融分析深入，但主动响应训练只用了一个架构
- 写作质量: ⭐⭐⭐⭐ 动机清晰，benchmark 设计描述详尽，附录完整
- 价值: ⭐⭐⭐⭐⭐ 填补了在线视频理解评测空白，短期内会成为该方向的标准 benchmark
