# Sky2Ground: A Benchmark for Site Modeling under Varying Altitude

**日期**: 2026-03-14  
**arXiv**: [2603.13740](https://arxiv.org/abs/2603.13740)  
**代码**: 即将开源  
**领域**: 3D视觉 / 跨视角定位  
**关键词**: cross-view localization, satellite-aerial-ground, 3D reconstruction, benchmark, site modeling

## 一句话总结
构建 Sky2Ground 跨高度场景建模 benchmark（51 个地理站点，覆盖卫星/航拍/地面三种视角），提出 SkyNet 双流架构（Masked-Satellite-Attention + 课程训练）进行跨视角定位，RRA@5 提升 9.6%。

## 研究背景与动机

1. **领域现状**: 跨视角定位（地面↔卫星/航拍）在自动驾驶和地理建模中重要，但现有数据集缺乏同时包含三种视角的统一数据。

2. **核心 idea**: 构建涵盖卫星-航拍-地面三视角的统一 benchmark，用航拍图像作为地面和卫星之间的"桥梁"。

## 方法详解

### 数据集
- 51 个地理站点，合成+真实图像混合
- 卫星（120 张）、航拍（1080 张）、地面（120 真实 + 50-250 合成）

### SkyNet 架构
- 双流结构 + Masked-Satellite-Attention（MSA）抑制卫星图像中的视角差异
- 课程训练：先学地面-航拍匹配，逐步引入卫星视角

## 实验关键数据

| 方法 | RRA@5↑ | RTA@5↑ |
|------|--------|--------|
| VGGT (ground/aerial) | 75.1 | 60.9 |
| Baseline | - | - |
| **SkyNet** | **+9.6%** | **+18.1%** |

### 关键发现
- 航拍图像确实是连接地面-卫星的有效中间媒介
- 加入真实图像反而降低渲染质量，合成-真实 domain gap 仍需解决

## 评分
- 新颖性: ⭐⭐⭐ Benchmark 构建有价值，方法创新性中等
- 实验充分度: ⭐⭐⭐⭐ 多方法对比 + 多视角组合评估
- 价值: ⭐⭐⭐⭐ 填补三视角统一 benchmark 空白
