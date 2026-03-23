# Geo-ID: Test-Time Geometric Consensus for Cross-View Consistent Intrinsics

**日期**: 2026-03-14  
**arXiv**: [2603.13859](https://arxiv.org/abs/2603.13859)  
**代码**: 有  
**领域**: 3D视觉 / 内在分解  
**关键词**: intrinsic decomposition, multi-view consistency, geometric consensus, test-time, diffusion

## 一句话总结
提出 Geo-ID，一种推理时框架，通过几何引导的稀疏对应关系耦合多视角内在分解预测，用体素化共识初始化 + 共识引导扩散注入跨视角约束，无需修改模型参数即可实现多视角一致的 albedo/metallicity 估计。

## 研究背景与动机

1. **领域现状**: 单视角内在分解模型（RGB→albedo/shading/metallicity）已较成熟，但不同视角的预测不一致，限制了在神经场景编辑中的应用。

2. **核心矛盾**: 单视角模型独立处理每张图，无法保证同一 3D 点在不同视角下的属性一致。现有多视角方法需要密集有序序列或大量逐场景优化。

3. **核心 idea**: 在推理时通过几何对应关系建立跨视角共识，注入扩散去噪过程，无需重训模型。

## 方法详解

### 三阶段流程
1. **几何引导对应估计**: 用 VGGT 预测相机参数和 3D 点图
2. **体素化共识初始化**: 对跨视角对应点的预测做加权中值聚合
3. **共识引导扩散**: 将稀疏跨视角约束注入去噪过程

## 实验关键数据

| 场景 | 指标 | 无 Geo-ID | 有 Geo-ID |
|------|------|----------|----------|
| MipNeRF-360 (32views) | Albedo MAD | 0.091 | 0.076 |
| Outdoor | Metallicity MAD | 0.070 | 0.044 |

### 关键发现
- 一致性随视角数量单调提升
- 模型无关设计，兼容 RGB↔X 和 Marigold IID
- 单视角分解质量基本保持

## 评分
- 新颖性: ⭐⭐⭐⭐ 推理时几何共识注入扩散是新颖设计
- 实验充分度: ⭐⭐⭐ 评估场景有限
- 价值: ⭐⭐⭐⭐ 对可编辑神经场景有直接实用价值
