# Identity-Consistent Video Generation under Large Facial-Angle Variations

**日期**: 2026-03-22  
**arXiv**: [2603.21299](https://arxiv.org/abs/2603.21299)  
**代码**: 无  
**领域**: 视频理解  
**关键词**: video generation, identity consistency, multi-view conditioning, RoPE, region masking

## 一句话总结
提出 Mv²ID 框架，用多视角参考图引导视频生成——通过 Region Masking 防止"视角锁定"复制伪影 + Reference-Decoupled RoPE 区分时空编码，在大角度人脸变化下保持身份一致性并生成自然运动。

## 研究背景与动机

1. **领域现状**: 基于参考图的身份保持视频生成已有不少工作（IP-Adapter、InstantID 等），多用单张参考图 + 文本控制生成视频。

2. **现有痛点**: (a) 单视角参考图在大角度姿态变化时信息不足——侧面/背面无法从正面参考推断；(b) 使用多视角参考时出现"view-dependent copy-paste"伪影——人脸直接锁定到特定参考角度，运动不自然；(c) 获取 cross-paired 数据（同一人不同表情×不同角度）成本极高（<5%数据满足要求）。

3. **核心矛盾**: 多视角参考提供了更多信息，但也带来了直接复制而非融合生成的快捷路径。模型倾向于按角度匹配直接选择最近的参考视角粘贴。

4. **核心 idea**: 在 in-paired（同主体同场景多视角）数据上训练，用 Region Masking 迫使模型聚合互补信息而非复制单一视角，用 Decoupled RoPE 正确编码多参考图的时空关系。

## 方法详解

### 整体框架
多张参考图 token 拼接到视频 noisy token 序列上 → 共享 self-attention 实现跨参考交互 → Region Masking 随机遮挡 60% 参考区域 → RD-RoPE 为每张参考分配独立空间坐标 → 去噪生成视频。

### 关键设计

1. **Token-level 多视角注入**:
   - 将参考图编码为 clean tokens，与 noisy video tokens 沿序列维度拼接
   - 标准 self-attention 自然实现视频-参考和参考间的交互
   - 简单直接，不引入额外跨注意力模块

2. **Region Masking (RM)**:
   - MAE 启发：随机对每张参考图施加空间 binary mask，遮挡 60% 区域
   - 强制模型从多张不完整参考中聚合互补线索，学习视角不变表征
   - 防止模型走捷径直接按角度匹配复制参考图
   - 训练时 mask、推理时不 mask

3. **Reference-Decoupled RoPE (RD-RoPE)**:
   - 问题：标准 RoPE 会给多张参考图错误的时空位置编码
   - 解决：时间维度——所有参考图共享同一时间索引（"时间等价"），空间维度——每张参考图偏移不同的空间坐标（"空间区分"）
   - $h_i = h_v + i \cdot H, w_i = w_v + i \cdot W$，将参考图在空间上"铺开"

4. **大角度数据集构建**:
   - 三阶段 pipeline：粗过滤 → 分割追踪 → 3D 姿态估计挖掘角度
   - 产出 22K 视频，覆盖 30+ 身份，包含大角度人脸变化

## 实验关键数据

### 主实验

| 方法 | MvRC (ArcFace) | NaturalScore | AES | IQA |
|------|---------------|--------------|-----|-----|
| HuMo | 0.493 | 4.71 | 0.562 | 0.622 |
| MAGREF-MV | — | 4.43 | — | — |
| **Mv²ID** | **0.544** | **4.69** | **0.568** | **0.645** |

### 消融实验

| 配置 | MvRC | NaturalScore | 说明 |
|------|------|--------------|------|
| Base multi-view | good | baseline | 多视角已有基础优势 |
| + RM | +slight drop | +0.52 | 定量身份略降但运动更自然 |
| + RD-RoPE | — | +0.23 | 空间编码改善 |
| + RM + RD-RoPE | best | +0.82 | 组合效果最优 |

### 关键发现
- Region Masking + RD-RoPE 组合使运动自然度提升 0.82
- 面部轨迹分析显示方法产生平滑真实的旋转，而 baseline 出现轨迹坍缩/发散
- 用户研究 ANOVA F=81.70, p<1e-70，统计显著

## 亮点与洞察
- **MAE 理念迁移到视频生成**: Region Masking 在参考条件上做"数据增强"防止快捷学习，思路新颖
- **RD-RoPE 处理多参考时空编码**: 时间等价 + 空间区分的设计直觉合理
- **系统性研究大角度身份保持**: 首次专门针对大角度人脸变化的视频生成做系统分析

## 局限性 / 可改进方向
- Region Masking 定量上略降低身份一致性指标（虽然视觉上更自然）
- 主实验用 14B 参数模型，部署成本高
- 未分析超极端角度（>90°）的表现

## 评分
- 新颖性: ⭐⭐⭐⭐ Region Masking + RD-RoPE 组合设计有创意
- 实验充分度: ⭐⭐⭐⭐ 用户研究 + 轨迹分析 + 消融全面
- 价值: ⭐⭐⭐⭐ 大角度视频生成有实际应用需求
