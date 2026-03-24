# Seed1.8 Model Card: Towards Generalized Real-World Agency

**日期**: 2026-03-21  
**arXiv**: [2603.20633](https://arxiv.org/abs/2603.20633)  
**代码**: 无  
**领域**: 多模态/VLM / LLM Agent  
**关键词**: foundation model, agentic AI, GUI agent, multi-step reasoning, thinking modes

## 一句话总结
字节跳动发布 Seed1.8 模型卡，一个面向通用真实世界代理的大模型，在保持 LLM/VLM 基础能力（推理、知识、指令遵循）的同时，统一支持搜索、代码执行和 GUI 交互的多步骤 Agent 工作流，提供四级思考模式平衡延迟与质量，在 AIME-25（94.3）、HMMT-25（89.7）等多个 benchmark 上达到或接近 GPT-5/Gemini-3-pro 水平。

## 研究背景与动机

1. **领域现状**: 前沿模型（GPT-5, Claude-Sonnet-4.5, Gemini-3-pro）在推理、代码和多模态理解上能力强大，但从单轮预测到交互式多步任务执行仍有差距。

2. **设计目标**: (a) 保持强基础能力（推理/知识/指令遵循）；(b) 统一 Agent 交互——搜索+代码执行+GUI 操作在单一模型中完成；(c) 延迟和成本感知——四级思考模式（no_think/低/中/高）可配置；(d) 实际应用对齐的评估。

## 方法详解

### 四级思考模式
- **no_think**: 无额外推理，最低延迟
- **think-low/medium/high**: 递增的推理深度，更高计算成本但更高质量
- 允许用户根据任务复杂度灵活配置

### 统一 Agent 能力
- **搜索**: 信息收集和证据综合
- **代码执行**: 程序修改和工具编排
- **GUI 交互**: 直接操作视觉界面（截图/文档/图表/视频）——当 API 不可用时的 fallback

### 优化的视觉编码
- 减少图像/视频输入的 token 消耗，降低多模态和长上下文场景的推理成本

## 实验关键数据

### 数学推理

| Benchmark | GPT-5 High | Gemini-3-pro | Seed1.8 |
|-----------|-----------|-------------|---------|
| AIME-25 | **94.6** | 95.0 | 94.3 |
| HMMT-25 | 88.3 | **97.5** | 89.7 |
| BeyondAIME | 74.0 | **83.0** | 77.0 |

### 代码推理

| Benchmark | GPT-5 High | Gemini-3-pro | Seed1.8 |
|-----------|-----------|-------------|---------|
| AetherCode | 43.3 | **56.7** | 38.2 |
| LiveCodeBench v6 | 87.0 | **90.7** | 79.5 |

### 指令遵循

| Benchmark | GPT-5 High | Gemini-3-pro | Seed1.8 |
|-----------|-----------|-------------|---------|
| Inverse IFEval | 78.9 | **80.6** | 80.3 |
| MultiChallenge | **69.6** | 67.4 | 66.7 |

### 关键发现
- Seed1.8 在数学推理上紧随 GPT-5 和 Gemini-3-pro，多数 benchmark 排名第二
- 代码能力相对较弱（AetherCode 38.2 vs GPT-5 43.3/Gemini-3 56.7）
- 指令遵循能力突出（Inverse IFEval 80.3 仅次于 Gemini-3 的 80.6）
- 多模态和 Agent 能力通过统一接口提供，减少了任务特定管线的需求

## 亮点与洞察
- **四级思考模式**是务实的工程设计——不同任务不需要同等推理深度
- 统一 Agent 框架（搜索+代码+GUI）比管线式组装更简洁
- 作为 model card 发布，透明度值得肯定

## 局限性 / 可改进方向
- 代码能力相比竞品有明显差距
- Agent 能力的评估细节相对模糊，缺少具体 Agent benchmark 结果
- 缺少开源计划

## 评分
- 新颖性: ⭐⭐⭐ 主要是工程集成而非方法创新
- 实验充分度: ⭐⭐⭐⭐ Benchmark 覆盖全面，对比模型有代表性
- 价值: ⭐⭐⭐⭐ 展示了统一 Agent 模型的可行性
