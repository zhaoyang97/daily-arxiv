# VQQA: An Agentic Approach for Video Evaluation and Quality Improvement

**日期**: 2026-03-12  
**arXiv**: [2603.12310](https://arxiv.org/abs/2603.12310)  
**代码**: 无  
**领域**: 视频理解 / 视频生成评估  
**关键词**: video evaluation, agentic, prompt refinement, VLM, closed-loop

## 一句话总结
提出 VQQA，一个多 Agent 视频评估与质量改进框架——通过三个 Agent（问题生成→视频问答→提示优化）构建闭环，将 VLM 的评估反馈作为"语义梯度"驱动 prompt 迭代优化，无需模型微调，在 T2V-CompBench 上对 CogVideoX-5B 提升 11.57%，VBench2 上 +8.43%。

## 研究背景与动机

1. **领域现状**: 视频生成评估主要是被动打分，评估结果无法回馈到生成过程中改进质量。

2. **核心 idea**: 将视频评估从被动 benchmark 转化为主动的闭环反馈——评估→找缺陷→优化 prompt→重新生成。

## 方法详解

### 三 Agent 协作

1. **Question Generation Agent**: 针对生成视频制定视觉查询
2. **Question Answering Agent**: 评估视频回答查询，隔离具体缺陷
3. **Prompt Refinement Agent**: 将评估批评作为语义梯度优化 prompt

- **Global VLM Selection**: 防止语义漂移
- **Dynamic Stopping**: 动态停止准则管理计算开销

## 实验关键数据

| Benchmark | 模型 | 改进幅度 |
|-----------|------|---------|
| T2V-CompBench | CogVideoX-5B | **+11.57%** |
| VBench2 | - | **+8.43%** |

### 关键发现
- 几步迭代即可获得显著改进——计算效率高
- 无需模型权重访问，通过黑盒 VLM 接口即可工作
- 对 T2V 和 I2V 任务都适用

## 亮点与洞察
- "评估反馈作为语义梯度"的概念很精妙——将评估和改进统一到一个闭环中
- 完全不需要微调生成模型，只优化 prompt——通用性极强
- 多 Agent 架构自然地分工协作

## 评分
- 新颖性: ⭐⭐⭐⭐ 闭环评估-改进范式新颖
- 实验充分度: ⭐⭐⭐⭐ 多 benchmark + T2V/I2V
- 价值: ⭐⭐⭐⭐ 实用的视频生成质量改进方案
