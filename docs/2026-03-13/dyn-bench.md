# Thinking in Dynamics: How MLLMs Perceive, Track, and Reason Dynamics in Physical 4D World

**日期**: 2026-03-13  
**arXiv**: [2603.12746](https://arxiv.org/abs/2603.12746)  
**代码**: 已开源  
**领域**: 多模态VLM / 视频理解  
**关键词**: 4D dynamics, spatio-temporal reasoning, benchmark, object grounding, MLLM

## 一句话总结
提出 Dyn-Bench，首个大规模物理 4D 动态理解 benchmark（1K 视频、7K VQA、3K 动态目标 grounding），发现现有 MLLM 无法同时维持时空推理和动态目标定位的强表现，提出 Mask-Guided Fusion 和 ST-TCM 结构化集成方法显著提升动态感知能力。

## 研究背景与动机
- 人类生活在几何结构和语义内容随时间演变的物理 4D 世界，但 MLLM 主要擅长静态视觉理解
- 缺乏系统评估 MLLM 时空推理 + 动态目标定位能力的 benchmark

## 方法详解
- 从大量 2D 和 4D 数据源多阶段筛选构建高质量动态场景集
- 探测通用/空间/区域级 MLLM 的语言和视觉动态思考能力
- 传统 prompting（CoT、caption hints）改善有限，结构化方法（Mask-Guided Fusion、ST-TCM）显著有效

## 关键发现
- 现有模型在时空推理和动态 grounding 上存在不一致的运动/交互解释
- 结构化空间-时间整合方法远优于简单 prompting 策略

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个 4D 动态理解 benchmark
- 实验充分度: ⭐⭐⭐⭐ 多类 MLLM 系统评测
- 价值: ⭐⭐⭐⭐ 揭示 MLLM 在动态理解上的系统性不足
