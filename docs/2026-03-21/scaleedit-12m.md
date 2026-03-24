# ScaleEdit-12M: Scaling Open-Source Image Editing Data Generation via Multi-Agent Framework

**日期**: 2026-03-21  
**arXiv**: [2603.20644](https://arxiv.org/abs/2603.20644)  
**代码**: [GitHub](https://github.com/gzchen4ai/ScaleEdit-12M)  
**领域**: 图像生成  
**关键词**: image editing, multi-agent, dataset, open-source, unified multimodal model

## 一句话总结
提出 ScaleEditor，全开源多智能体层级框架，通过源图扩展+自适应编辑合成+任务感知质量验证三阶段构建了 ScaleEdit-12M（1200 万编辑对，23 类任务），微调 UniWorld-V1 后在 GEdit 上提升 35.1%、RISE 上提升 150.0%，证明开源 pipeline 可逼近商用 API 数据质量。

## 研究背景与动机

1. **领域现状**: 指令式图像编辑是统一多模态模型(UMM)的核心能力，GPT-4o-Image 和 Nano-Banana 等商用系统已展示强大编辑能力。

2. **现有痛点**: (a) 依赖闭源模型标注——GPT-4o 生成数据虽质量高但成本不可扩展（如 OpenGPT-4o-Image 仅 40K 对）；(b) 开源固定合成管线——UltraEdit/AnyEdit 用固定编辑算子（mask inpainting、风格转化等），质量和多样性受限；(c) 源图域窄、指令模板死板、质量过滤粗糙。

3. **核心 idea**: 用开源多智能体框架替代商用 API——同时解决源图多样性（检索+合成扩展）、编辑自适应性（路由到专用 agent）和质量保证（三维评估过滤）。

## 方法详解

### 整体框架
ScaleEditor 分三阶段：源图扩展 → 自适应多 Agent 编辑合成 → 任务感知质量验证。

### 关键设计

1. **源图扩展（世界知识注入）**:
   - 检索分支：基于图像和文本的双路搜索引擎检索，引入真实场景变体和长尾视觉概念
   - 合成分支：MetaCaptioner 生成详细描述 → Qwen-Image 生成变体图像，增加域内多样性
   - 感知哈希去重，最终 >10M 唯一图像

2. **自适应多 Agent 编辑合成**:
   - 23 类预定义编辑任务，Qwen2.5-VL-72B 作为任务路由器
   - 拒绝策略：排除不适合的任务，其余视为可行（一图多任务）
   - 24 个专用指令 Agent + 多种编辑模型（Qwen-Image-Edit, FLUX.1 Kontext, Step1X-Edit, Flux-Text）
   - 文本感知编辑：PaddleOCR 检测 → 文本指令 Agent → 文本编辑 Agent
   - 知识推理编辑：指令解耦——复杂推理查询 + 精简可执行命令，保留复杂意图作为用户输入

3. **任务感知质量验证**:
   - 三维评估：指令遵循、编辑一致性、生成质量
   - 每类任务有专用评估 prompt（Qwen2.5-VL-72B）
   - 过滤标准：指令遵循必须满分(3)，其余至少 2 分
   - 85.3% 数据三维均达满分

## 实验关键数据

### GEdit-EN-Full 对比

| 模型 + 数据 | Avg Score |
|-------------|-----------|
| UniWorld-V1 (原始) | ~4.85 |
| + UltraEdit | 5.30 |
| + AnyEdit | 5.52 |
| + **ScaleEdit** | **6.55** (+35.1%) |

### 知识编辑 Benchmark

| Benchmark | UniWorld-V1 原始 | + ScaleEdit | 提升 |
|-----------|-----------------|-------------|------|
| RISE | 基线 | — | +150.0% |
| KRIS-Bench | 基线 | — | +12.6% |

### Bagel 基线验证

| Benchmark | Bagel + ScaleEdit 提升 |
|-----------|-----------------------|
| GEdit | +10.0% |
| ImgEdit | +7.8% |
| KRIS-Bench | +26.5% |

### 关键发现
- ScaleEdit 在所有 benchmark 上一致优于其他开源数据集训练的模型
- 知识推理编辑提升最大（RISE +150%），说明世界知识注入和推理编辑工作流有效
- 跨模型泛化：UniWorld-V1 和 Bagel 两个不同架构均获得显著收益

## 亮点与洞察
- **规模 + 质量兼得**：12M 级别的纯开源编辑数据集，质量可比肩 ShareGPT-4o
- **指令解耦策略**巧妙：将复杂推理查询与可执行命令分离，绕过执行模型的能力边界
- **任务路由器的拒绝策略**比肯定匹配更鲁棒——明确排除不适合任务而非强行匹配

## 局限性 / 可改进方向
- 质量验证仍依赖 Qwen2.5-VL-72B 打分，可能有系统性偏差
- 缺少人工评估对比
- 计算成本分析缺失——12M 数据的生成总成本是多少？

## 评分
- 新颖性: ⭐⭐⭐⭐ 多 Agent 框架思路清晰，知识推理编辑和指令解耦有新意
- 实验充分度: ⭐⭐⭐⭐ 多 benchmark 多模型交叉验证
- 价值: ⭐⭐⭐⭐⭐ 12M 开源数据集对社区价值极大
