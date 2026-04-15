# OddGridBench: Exposing the Lack of Fine-Grained Visual Discrepancy Sensitivity in MLLMs

**日期**: 2026-03-10  
**arXiv**: [2603.09326](https://arxiv.org/abs/2603.09326)  
**代码**: [Project Page](https://wwwtttjjj.github.io/OddGridBench/)  
**领域**: 多模态评测 / 感知基准  
**关键词**: visual discrepancy, odd-one-out, low-level perception, GRPO, curriculum learning

## 一句话总结
提出 OddGridBench（1400+ 样本）系统评估 MLLM 的细粒度视觉差异感知能力，发现即使 GPT-5/Gemini 也明显低于人类；进一步提出 OddGrid-GRPO，把 Qwen3-VL-2B 从 17.1% 提升到 82.6%。

## 研究背景与动机

1. **现状**: MLLM 在高层语义任务（VQA、图表推理）表现很好，但“底层感知能力”很少被严格测试。
2. **关键缺口**: 人类视觉对细微差异（颜色、尺寸、旋转、位置）极敏感，这是高层推理基础；模型若在底层不可靠，高层能力也会受限。
3. **核心思路**: 用参数可控的 odd-one-out 任务隔离语义因素，只测视觉差异敏感度。

## 基准设计

### OddGridBench
- 任务：给定网格图，找出与其他元素不同的那个格子
- 单属性差异（4类）：
  - 颜色：$\Delta E\in[5,20]$
  - 大小：$\pm 5\%-15\%$
  - 旋转：$\pm 5^\circ-25^\circ$
  - 位置：偏移 $5\%-12\%$
- 复合差异（3类）：2-type/3-type/4-type
- 规模：测试 1400、验证 400、训练 30000
- 图标来源：IconFont + Material Design Icons（SVG，可控生成）

### 评价价值
- 可量化不同差异强度下模型性能曲线
- 可横向比较开源/闭源模型在低层感知上的真实差距

## OddGrid-GRPO：如何提升模型感知

### 1. 课程学习
按难度分阶段训练：Easy -> Easy+Medium -> Easy+Medium+Hard。难度由网格尺寸、差异类型和扰动幅度联合决定。

### 2. 距离感知奖励
标准 RL 的“对/错二值奖励”太粗糙，本文改为与预测位置距离相关的连续奖励：

$$
r_d=\max\left(\exp\left(-\frac{d^2}{2\sigma^2}\right)-\beta,0\right)
$$

即“猜得更近就给更多分”，更适合定位类任务。

## 实验关键数据

### MLLM 感知能力（准确率 %）

| 模型 | Color | Size | Rotation | Position | Total |
|------|-------|------|----------|----------|-------|
| GPT-5 | 56.5 | 9.5 | 21.0 | 5.0 | 28.9 |
| Gemini 2.5 Pro | 82.5 | 9.5 | 26.0 | 6.5 | 49.3 |
| Qwen3-VL-32B | 85.0 | 39.5 | 52.5 | 39.0 | 68.1 |
| **Human** | **91.3** | **69.3** | **82.7** | **78.0** | **87.5** |

### OddGrid-GRPO 训练效果（Qwen3-VL-2B）

| 方法 | Color | Size | Rotation | Position | Total |
|------|-------|------|----------|----------|-------|
| Baseline | 23.0 | 5.0 | 12.5 | 7.0 | 17.1 |
| GRPO | 88.5 | 44.0 | 67.5 | 41.5 | 70.9 |
| **OddGrid-GRPO** | **89.5** | **64.5** | **80.5** | **64.5** | **82.6** |

## 关键发现
- 当前最强 MLLM 仍远低于人类（68.1 vs 87.5）
- 最薄弱维度是 Size/Position（部分模型接近随机）
- 经针对性 RL 后，2B 模型可超过未经训练的大模型
- 说明问题主要在训练目标，不只是参数规模

## 局限性
- 合成图标场景与真实工业场景仍有 domain gap
- 目前仅覆盖 2D 网格，不含 3D/视频时序差异
- RL 训练成本与稳定性分析可再展开

## 评分
- 新颖性: ⭐⭐⭐⭐⭐（把“低层感知盲区”系统性量化）
- 实验充分度: ⭐⭐⭐⭐⭐（19 模型 + 人类对照 + 提升方案）
- 写作质量: ⭐⭐⭐⭐
- 价值: ⭐⭐⭐⭐⭐（对评测范式和训练目标都很有启发）
