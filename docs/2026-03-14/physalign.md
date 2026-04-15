# PhysAlign: Physics-Coherent Image-to-Video Generation through Feature and 3D Representation Alignment

**日期**: 2026-03-14  
**arXiv**: [2603.13770](https://arxiv.org/abs/2603.13770)  
**代码**: [PhysAlign](https://physalign.github.io/PhysAlign)  
**领域**: 图像生成 / 视频生成  
**关键词**: physics-coherent, image-to-video, representation alignment, V-JEPA2, depth supervision, rigid-body

## 一句话总结
提出 PhysAlign，通过 Gram 矩阵时空关系对齐（从 V-JEPA2 提取运动学先验）+ 多层深度几何监督，仅用 3K 合成物理视频微调 Wan2.2-14B 的 LoRA adapter，即可显著提升生成视频的物理一致性（PIS 加速度指标从 0.52→0.63）而不损失视觉质量。

## 研究背景与动机

1. **领域现状**: Video Diffusion Models（VDMs）如 CogVideoX、HunyuanVideo、Wan2.2 能生成高质量视频，但常产生违反物理直觉的运动（物体穿透、不合理轨迹、违反重力等）。

2. **现有痛点**: 物理一致性定义为两个维度：(a) **一般物理定律**（重力加速度、碰撞动量守恒）和 (b) **3D 感知保真度**（正确遮挡、透视变化）。现有 VDM 仅从大规模视频数据隐式学习物理，缺乏显式物理标注。

3. **核心矛盾**: 真实视频数据集几乎没有物理标注（深度、力、质量等），直接监督不可行。需要合成数据 + 高效知识注入方式。

4. **核心 idea**: 用物理模拟器生成带稠密 3D 标注的合成视频，通过 Gram 矩阵关系对齐将 V-JEPA2 的运动学理解注入 VDM，同时用深度监督注入 3D 几何感知。

## 方法详解

### 整体框架
基于 Wan2.2-I2V-14B + LoRA。训练时用三个损失联合优化：flow matching loss + 物理关系对齐 loss + 3D 深度对齐 loss。推理时丢弃所有辅助分支，runtime 与标准 LoRA 相同。

### 关键设计

1. **合成数据 Pipeline**:
    - 基于 Blender 的刚体物理模拟器，3-7 个物体，随机质量/弹性/初速度/高度
    - 多模态渲染：RGB + 深度图 + 物理参数（力、质量、角度等写入 prompt）
    - 仅 3K 个合成视频即足够微调

2. **Physical Knowledge Injection（Gram 矩阵关系对齐）**:
    - 从 DiT 中间层提取 hidden states → MLP 投影到 V-JEPA2 特征空间
    - **不做 token 级绝对值对齐**（过于严格，会破坏生成先验），而是对齐**关系矩阵**
    - 计算时空 Gram 矩阵 $G_{i,j} = \cos(s_i, s_j)$，同时捕捉帧内空间几何和帧间因果关系
    - 用 margin-based L1 惩罚对齐学生和教师的关系矩阵：容许小偏差（margin m），仅惩罚结构性差异
    - 这样保留了生成多样性，同时注入了运动学约束

3. **3D Geometry Injection（深度监督）**:
    - 在 DiT 中间层附加轻量 3D 卷积头预测深度 latent
    - 四个互补深度损失：latent loss（全局结构）+ pixel SI loss（尺度不变的像素级）+ structure loss（空间梯度匹配，保留边缘）+ temporal loss（帧间深度变化一致性）
    - 推理时丢弃深度头，无额外开销

### 训练目标
$\mathcal{L} = \mathcal{L}_{FM} + \lambda_{Phys} \mathcal{L}_{Phys} + \lambda_{3D} \mathcal{L}_{3D}$

## 实验关键数据

### 主实验（Physical Invariance Score, PIS）

| 模型 | PIS-$a_x$↑ | PIS-$a_y$↑ | PIS-$v_x$↑ | PIS-$v_y$↑ |
|------|-----------|-----------|-----------|-----------|
| CogVideoX-5B | 0.350 | 0.385 | 0.494 | 0.467 |
| HunyuanI2V | 0.571 | 0.604 | 0.704 | 0.746 |
| Wan2.2 | 0.520 | 0.517 | 0.679 | 0.661 |
| **PhysAlign** | **0.632** | **0.648** | **0.746** | **0.798** |
| Reference | 0.701 | 0.715 | 0.790 | 0.827 |

### VBench-I2V 视觉质量

| 指标 | Wan2.2 | PhysAlign | 说明 |
|------|--------|-----------|------|
| motion_smooth | 0.991 | 0.997 | 运动更平滑 |
| dynamic_degree | 0.410 | 0.460 | 物体运动更充分 |
| i2v_subject | 0.856 | 0.871 | 主体一致性保持 |
| aesthetic | 0.517 | 0.526 | 美学质量不降反升 |

### 关键发现
- **仅 3K 合成视频**即可显著提升物理一致性，数据效率极高
- 物理一致性提升的同时**视觉质量不降反升**（VBench 各项指标持平或提升），说明物理先验与视觉先验互补
- 在 WISA 真实世界测试集上同样有效（$a_x$: 0.444→0.604），证明从合成到真实的泛化
- Gram 矩阵关系对齐比 token 级绝对对齐更有效 — 保留生成多样性

## 亮点与洞察
- **关系对齐 > 绝对对齐**是重要发现 — 对齐 token 间的关系结构而非绝对值，避免了过度约束生成模型。这个思路可迁移到其他需要 teacher-student 蒸馏的场景
- **合成-真实泛化**令人印象深刻 — 仅 3K 个 Blender 刚体模拟视频就能泛化到真实世界复杂场景，说明物理规律的可迁移性
- **推理零开销**的设计很实用 — 训练时的辅助分支（V-JEPA2、深度头）推理时全部丢弃

## 局限性 / 可改进方向
- 仅覆盖刚体物理（碰撞、抛射），流体、柔体等复杂物理未涉及
- PIS 指标本身有局限（基于 2D 投影的启发式评估）
- 3K 合成视频的场景多样性有限（抽象物体+简单几何），可能限制复杂场景泛化

## 相关工作与启发
- **vs PhysDiff/PhysCtrl**: 在 latent space 注入物理而非 input/output space，更灵活
- **vs REPA**: 引入时间维度的 Gram 矩阵关系对齐，而非 REPA 的空间 token 对齐
- 物理模拟器 + LoRA adapter 的范式可推广到其他需要物理一致性的生成任务

## 评分
- 新颖性: ⭐⭐⭐⭐ Gram 矩阵时空关系对齐 + 合成物理数据的组合是创新性的
- 实验充分度: ⭐⭐⭐⭐ PIS + VBench双指标评估，合成+真实泛化验证
- 写作质量: ⭐⭐⭐⭐ 方法动机清晰，公式推导完整
- 价值: ⭐⭐⭐⭐ 3K 合成数据就能提升物理一致性，开辟了高效的物理感知视频生成范式
