# Infinity-RoPE: Action-Controllable Infinite Video Generation Emerges From Autoregressive Self-Rollout

**日期**: 2026-03-20  
**arXiv**: [2511.20649](https://arxiv.org/abs/2511.20649)  
**代码**: 无  
**领域**: 视频理解 / 图像生成  
**关键词**: infinite video generation, RoPE reparameterization, KV cache, action control, scene transitions

## 一句话总结
提出 Infinity-RoPE，通过 Block-Relativistic RoPE（移动参考系时序编码）+ KV Flush（仅保留 2 token 实现即时 prompt 响应）+ RoPE Cut（受控时序断裂实现场景转换），在 Wan2.1-T2V 上实现训练无关的无限长视频生成——60 秒视频 VBench Overall 0.8298（SOTA），12× 超训练长度且动态度保持 0.52（vs baseline 0.32-0.36）。

## 研究背景与动机

1. **领域现状**: 自回归视频扩散模型（如 Self-Forcing on Wan2.1）在短片（5 秒）生成上表现出色，但受 3D-RoPE 固定时域（1024 帧）限制，无法生成更长视频。

2. **现有痛点**: (a) 超出训练长度后 RoPE 编码越界导致质量崩溃；(b) KV cache 累积造成语义滞后——prompt 变化后模型反应迟钝；(c) 无法在连续生成流中实现干净的场景切换（电影式剪辑）。

3. **核心 idea**: 纯推理时的 RoPE 重参数化——三种操作（Block-Relativistic/Flush/Cut）解决三个问题（长度外推/即时响应/场景转换），无需重新训练。

## 方法详解

### 关键设计

1. **Block-Relativistic RoPE**:
   - 做什么：将时序编码从绝对坐标转为移动参考系
   - 核心思路：每个新生成的 block 相对模型最大视域做旋转，旧 block 向后退——像火车上看风景，永远在"当前窗口"内
   - 两种 cache 模式：Fixed cache（稳定质量）/ Unbounded cache（远帧自动"语义化"，{1,2,3}→{1,1,1}）
   - 结果：突破 1024 帧限制，支持分钟级生成

2. **KV Flush**:
   - 做什么：清空 KV cache 只保留 2 个 token（全局 sink + 最后帧）
   - 效果：prompt 变化后即时响应，无语义滞后
   - 恒定内存占用

3. **RoPE Cut**:
   - 做什么：在时序 RoPE 中插入坐标偏移 Δ，制造受控断裂
   - 效果：干净的场景切换，零时序上下文泄漏
   - 实现电影式多剪辑场景

## 实验关键数据

### 60 秒视频生成（12× 训练长度）

| 方法 | Overall | Dynamic Degree | Background Consist. |
|------|---------|---------------|-------------------|
| Self-Forcing | 0.7715 | 0.32 | ~0.92 |
| Rolling-Forcing | 0.8146 | 0.36 | 0.9447 |
| SkyReels | 0.7768 | - | - |
| **Infinity-RoPE** | **0.8298** | **0.52** | **0.9490** |

### 5 秒视频（训练长度内）

| 方法 | Overall | Temporal Flicker | Subject Consist. |
|------|---------|-----------------|-----------------|
| Self-Forcing | 0.8398 | 0.9823 | 0.9757 |
| **Infinity-RoPE** | **0.8377** | **0.9845** | **0.9787** |

120 秒和 240 秒生成也保持第一或第二。吞吐量 17.01 FPS，与 baseline 持平。

### 关键发现
- **Dynamic Degree 0.52 vs 0.32-0.36** 是最大亮点——长视频生成中运动丰富度大幅领先
- 注意力可视化确认了对角带+sink列模式在超长视域中保持完好——机制完整性
- KV Flush 实现了流畅的 prompt 过渡：站立→跳跃→坐下→唱歌
- 训练无关：直接适用于现有 Self-Forcing 模型

## 亮点与洞察
- **训练无关**是最大价值：纯推理时 RoPE 重参数化，任何基于 RoPE 的视频扩散模型都可直接使用
- **移动参考系**的物理类比非常直观：把"绝对时间坐标"变成"相对运动坐标"，自然解决了长度外推
- **三个操作三个问题**的对称设计很优雅——Block-Relativistic（长度）/Flush（响应）/Cut（场景）

## 局限性 / 可改进方向
- 依赖 Self-Forcing 蒸馏模型的基础质量——base model 弱则无法弥补
- Unbounded cache 的"语义化"可能导致远距离视觉细节丢失
- RoPE Cut 的断裂点位置和偏移量 Δ 需要手动设定
- 仅在 Wan2.1-1.3B 上验证，更大模型的效果待测

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 训练无关的 RoPE 重参数化实现无限视频生成，思路极其优雅
- 实验充分度: ⭐⭐⭐⭐ 5s/60s/120s/240s 全面测试 + 注意力可视化
- 价值: ⭐⭐⭐⭐⭐ 直接可用于现有模型的即插即用方案，工程价值极高
