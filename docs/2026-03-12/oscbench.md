# OSCBench: Benchmarking Object State Change in Text-to-Video Generation

**日期**: 2026-03-12  
**arXiv**: [2603.11698](https://arxiv.org/abs/2603.11698)  
**代码**: 无  
**领域**: 视频理解 / T2V Benchmark  
**关键词**: text-to-video, object state change, benchmark, evaluation, video generation

## 一句话总结
提出 OSCBench，首个专门评估文本到视频生成中物体状态变化（如水结冰、蜡烛燃烧）的 benchmark，包含 1,120 个提示覆盖 140 个场景，通过 CoT 四维评估策略（语义/状态变化准确性+一致性/场景对齐/感知质量）揭示当前 SOTA T2V 模型在物体状态变化上的关键瓶颈。

## 研究背景与动机

1. **领域现状**: T2V 模型在视觉质量和语义对齐上取得巨大进步，但物体状态变化（Object State Change, OSC）——物理世界中物体随时间改变状态的动态过程——仍是核心难题。

2. **核心矛盾**: 现有 benchmark 不专门评估 OSC，导致模型在"冰块融化""纸张燃烧"等需要物理理解的场景上表现差但不被发现。

3. **核心 idea**: 构建系统性的 OSC benchmark + CoT 评估协议。

## 方法详解

### Benchmark 构建
- **1,120 个提示**，覆盖 140 个物体-状态场景
  - 108 个常规场景 + 20 个新颖场景 + 12 个组合场景
- 评估 6 个 SOTA 模型：Open-Sora-2.0, HunyuanVideo, Wan-2.2, Kling-2.5-Turbo, Veo-3.1-Fast

### 评估协议（CoT 四维度）
1. **Semantic Adherence**: 语义一致性
2. **Object State Change**: 准确性 + 时间一致性
3. **Scene Alignment**: 场景匹配度
4. **Perceptual Quality**: 感知质量

## 实验关键数据

| 模型 | OSC 准确性 | OSC 一致性 | 
|------|-----------|-----------|
| Veo-3.1-Fast | 0.786 | 0.748 |
| Kling-2.5-Turbo | 0.726 | 0.726 |
| HunyuanVideo-1.5 | ~0.6 | ~0.6 |
| Open-Sora-2.0 | 0.380 | 0.428 |

### 关键发现
- 即使最强模型（Veo-3.1-Fast）在 OSC 准确性上也只有 78.6%，远非完美
- 开源模型（Open-Sora）在 OSC 上表现极差（38%），说明开源 T2V 对物理过程建模不足
- OSC 是 T2V 发展的关键瓶颈——语义对齐好不等于物理过程理解好

## 亮点与洞察
- 首次系统性暴露了 T2V 模型在物理状态变化上的不足
- CoT 评估策略比简单打分更有诊断价值
- 新颖/组合场景的加入测试了泛化能力

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个 OSC 专用 benchmark
- 实验充分度: ⭐⭐⭐⭐ 6 个 SOTA 模型对比
- 价值: ⭐⭐⭐⭐ 对 T2V 发展方向有重要指引
