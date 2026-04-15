# GenState-AI: State-Aware Dataset for Text-to-Video Retrieval on AI-Generated Videos

**日期**: 2026-03-15  
**arXiv**: [2603.14426](https://arxiv.org/abs/2603.14426)  
**领域**: 视频理解 / 多模态VLM  
**关键词**: text-to-video retrieval, state transition, hard negative, AI-generated, benchmark

## 一句话总结
提出 GenState-AI benchmark，用 Wan2.2 生成 AI 视频，每个 query 配 temporal hard negative（改终态）和 semantic hard negative（换物体），三元组设计暴露现有 MLLM 检索模型在终态判断上的系统性失败。

## 研究背景与动机

1. **领域现状**: 文本-视频检索基准以真实视频为主（MSR-VTT、DiDeMo），多数语义可从单帧推断，temporal reasoning 被低估。

2. **现有痛点**: (a) 负样本与正样本在多个维度不同，无法精确诊断失败原因；(b) 没有区分"temporal confusion"和"semantic confusion"的机制；(c) 真实视频难以精确控制状态变化。

3. **核心 idea**: 用 AI 生成器精确控制状态转变——三元组设计让失败模式可解释：主视频 vs temporal HN（动作相同但终态不同）vs semantic HN（物体替换但时序相同）。

## 方法详解

### 数据集设计
- **规模**: 195 条 query × 3 个视频（main + temporal HN + semantic HN）= 956 视频
- **场景**: Home(127), Toy(21), Cartoon(24), Manipulation(23)
- **视频规格**: 720p / 24fps / 5s，Wan2.2-TI2V-5B 生成 + 人工质量过滤
- **关键控制**: temporal HN 仅改变终态（如"杯子倒了"→"杯子没倒"），semantic HN 保持时序但换物体

### 三元组评估范式

1. **Main vs Temporal HN**:
    - 测什么：模型是否关注终态证据
    - 难度：高——两个视频前 80% 完全相同

2. **Main vs Semantic HN**:
    - 测什么：模型是否区分核心物体
    - 难度：相对低——物体差异在视觉上明显

## 实验关键数据

### 数据集统计

| 类别 | 查询数 | 视频数 | 平均 query 长度 | 数据量 |
|------|--------|--------|----------------|--------|
| Home | 127 | 368 | 20.1 tokens | 2.53 GB |
| Toy | 21 | 221 | 26.8 tokens | 1.01 GB |
| Cartoon | 24 | 150 | 30.7 tokens | 522 MB |
| Manipulation | 23 | 217 | 14.7 tokens | — |
| **总计** | **195** | **956** | **21.5** | — |

视频规格：1280×704 (720p), 24 FPS, ~5s (121 frames/clip)

### 基线评估结果

| 子集 | 基线 | R@1 | R@5 | Acc_temp | Acc_sem | Acc_tri |
|------|------|-----|-----|---------|---------|---------|
| Toy | VCF-Lik | 0.381 | 0.714 | 0.619 | 0.810 | 0.524 |
| Toy | Qwen3-VL | **0.667** | **0.952** | 0.524 | **0.857** | 0.524 |
| Cartoon | Qwen3-VL | **0.708** | **0.958** | **0.750** | **0.917** | **0.750** |
| Home | VCF-Lik | 0.386 | 0.512 | **0.772** | **0.921** | **0.724** |
| Home | Qwen3-VL | **0.520** | **0.827** | 0.811 | 0.835 | 0.685 |
| Manipulation | VCF-Lik | **0.478** | **0.870** | **0.957** | 0.826 | **0.826** |
| Manipulation | Qwen3-VL | 0.391 | 0.739 | 0.391 | 0.652 | 0.304 |
| **All** | VCF-Lik | 0.374 | 0.564 | **0.744** | **0.887** | **0.677** |
| **All** | Qwen3-VL | **0.572** | **0.869** | 0.619 | 0.815 | 0.566 |

### 关键发现
- **两类基线都在 temporal HN 上系统性失败**: Acc_temp < Acc_sem 是普遍模式——模型依赖外观匹配，不验证终态
- **Qwen3-VL R@1 更高但 triplet 准确率更低**: 说明全局嵌入强但精细状态判断弱
- **VCF-Lik 在 Manipulation 类中反超**: 因为物体操作的 likelihood scoring 更稳定
- **Qwen3-VL 在 Manipulation 类崩溃**: Acc_tri 仅 0.304——数量变化的状态推理对 embedding 模型极难
- **Semantic HN 错误主要出现在视觉相似物体替换场景**（如红杯→粉杯），而非语义差异大的场景

## 亮点与洞察
- **AI 生成 + 三元组设计的巧妙**：完全控制变量，精确诊断失败原因——这是用真实视频无法做到的
- **暴露了检索模型的状态感知盲区**：模型依赖外观匹配而非理解状态转变
- **方法论可推广**：三元组 hard negative 设计可用于其他视频理解任务的诊断

## 相关工作对比
- **vs MSR-VTT/DiDeMo**: 正负样本多维度不同，模型靠外观匹配即可。GenState-AI 控制变量迫使状态推理
- **vs SSv2**: 也强调时序但有相机运动/背景混淆因素，GenState-AI 通过 AI 生成消除干扰
- **vs BLiM**: bidirectional likelihood 在真实基准上好，但在 GenState-AI 上同样频繁 temporal confusion
- **vs WebVid-2M/HowTo100M**: 大规模但以全局外观为主，无法测试状态转变理解


## 相关工作对比
- **vs MSR-VTT/DiDeMo**: 正负样本多维度不同，模型靠外观匹配即可。GenState-AI 控制变量迫使状态推理
- **vs SSv2**: 也强调时序但有相机运动/背景混淆因素，GenState-AI 通过 AI 生成消除干扰
- **vs BLiM**: bidirectional likelihood 在真实基准上好，但在 GenState-AI 上同样频繁 temporal confusion
- **vs WebVid-2M/HowTo100M**: 大规模但以全局外观为主，无法测试状态转变理解


## 局限性 / 可改进方向
- 195 条 query 规模较小，更大规模可更好验证发现
- AI 生成视频的视觉质量和真实性可能影响结论的普适性
- 仅评估了检索任务，状态感知在 VQA/描述生成中的表现未涉及

## 评分
- 新颖性: ⭐⭐⭐⭐ AI 生成三元组 benchmark 设计新颖
- 实验充分度: ⭐⭐⭐ 规模有限（195 queries）
- 价值: ⭐⭐⭐⭐ 暴露了检索模型的状态感知盲区
