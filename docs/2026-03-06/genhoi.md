# GenHOI: Towards Object-Consistent Hand-Object Interaction with Temporally Balanced and Spatially Selective Object Injection

**日期**: 2026-03-06  
**arXiv**: [2603.06048](https://arxiv.org/abs/2603.06048)  
**代码**: [项目主页](https://xuanhuang0.github.io/GenHOI/)  
**领域**: 视频理解  
**关键词**: Hand-Object Interaction, Video Generation, RoPE, Attention Gate, Object Consistency

## 一句话总结
提出 GenHOI，一个基于预训练视频生成模型的轻量扩展模块，通过 Head-Sliding RoPE 实现时间均衡的参考物体信息注入和空间注意力门控实现空间选择性注入，在野外场景中显著提升手-物交互视频的物体一致性和交互真实感。

## 研究背景与动机
1. **领域现状**: 手-物交互（HOI）是数字人内容创作的核心挑战，在在线教育和电商领域尤为重要。近期 HOI 重演方法取得了进展，但泛化能力有限。
2. **现有痛点**: HOI 重演方法（如 HOI-Swap、Re-HOLD）在域内数据上表现好但难以泛化到野外场景；通用视频编辑模型（如 VACE）泛化性强但无法保持物体在帧间的一致性。
3. **核心矛盾**: 泛化能力（利用大规模预训练）与 HOI 特有需求（物体一致性 + 自然交互）之间存在冲突。
4. **切入角度**: 在预训练视频生成模型上增加轻量模块，专门解决参考物体信息的时间均衡和空间选择性注入。
5. **核心idea一句话**: 用 Head-Sliding RoPE 消除 3D RoPE 的时间衰减、用空间注意力门控将物体信息精准注入 HOI 区域，两者协同实现高质量 HOI 视频。

## 方法详解

### 整体框架
GenHOI 基于预训练 Wan-14B-I2V 视频生成模型，增加三个轻量组件：HOI Condition Unit（条件输入）、Head-Sliding RoPE（时间均衡注入）、Spatial Attention Gate（空间选择性注入）。训练以自监督重建方式进行。

### 关键设计
1. **HOI Condition Unit (HCU)**:
    - 将视频 inpainting 与物体参考注入统一为条件输入
    - 构造参考视频 $\mathbf{V}_r$：第 0 帧保留原始，后续帧用二值掩码标记 HOI 区域（掩码区域填充常数 $\lambda=127$）
    - 所有输入在 VAE 潜空间中通道拼接：$\mathbf{L_v} = \text{Concat}(\mathbf{X_t}, \mathcal{E}(\mathbf{V}_r), \psi(\mathbf{V}_{mask}))$
    - 不引入额外网络分支或参数

2. **Head-Sliding RoPE**:
    - **问题**：标准 3D RoPE 给条件 token 分配固定帧索引（如 -1），导致注意力响应随时间距离衰减——早期帧物体清晰，后期帧退化
    - **解决**：让不同注意力头分配不同的帧索引给参考 token：$\lceil \frac{N_f}{N_{head}} n_{head} \rceil$
    - 效果：参考 token 的注意力响应在视频全时间跨度上被均匀平均
    - 空间坐标保持不变，仅修改时间维度的 RoPE

3. **Spatial Attention Gate（两级空间门控）**:
    - **Hard Mask Gate (HMG)**：二值掩码控制信息流向
     - 允许 HOI 区域 query 关注参考 key
     - 阻止背景 query 关注参考 key（避免背景污染）
     - 阻止参考 query 反向关注视频 key（避免自回归泄漏）
     - $T_{out} = \text{softmax}\left(\frac{M \odot QK^\intercal}{\sqrt{d_k}}\right) V$
   - **Soft Flow Gate (SFG)**：逐 token 门控系数
     - $G_v = \sigma(\mathcal{F}(\mathcal{LN}(T'_v)))$，$\tilde{T}_v = G_v \odot T'_v$
     - 自适应放大有信息区域、抑制冗余响应

### 损失函数 / 训练策略
- 在约 19,000 个视频上训练，16 × NVIDIA H100 (80GB) 训练 3 天
- 学习率 $1 \times 10^{-5}$
- 仅增加 157M 可学习参数（占原 16.5B 模型的 0.95%）
- 推理时参考物体图像由用户提供，首帧通过图像编辑方法生成

## 实验关键数据

### 主实验（AnchorCrafter_HOI 数据集）

**短视频生成（81 帧）**:

| 方法 | PSNR ↑ | SSIM ↑ | LPIPS ↓ | FID ↓ | FVD ↓ | OC ↑ | VQ (用户) | RF (用户) |
|---|---|---|---|---|---|---|---|---|
| VACE | 28.60 | 0.937 | 0.056 | 34.83 | 211.2 | 0.880 | 3.94 | 2.80 |
| HOI-Swap | 24.29 | 0.843 | 0.173 | 50.67 | 352.1 | 0.787 | 1.48 | 1.20 |
| MimicMotion | 20.13 | 0.685 | 0.206 | 48.89 | 395.1 | 0.777 | 2.82 | 2.09 |
| **GenHOI** | **31.71** | **0.952** | **0.036** | **11.53** | **67.95** | **0.937** | **4.49** | **4.64** |

**长视频生成（401 帧）**:

| 方法 | PSNR ↑ | FVD ↓ | OC ↑ | VQ (用户) | RF (用户) |
|---|---|---|---|---|---|
| VACE | 26.32 | 195.9 | 0.882 | 3.14 | 2.29 |
| **GenHOI** | **30.69** | **42.17** | **0.932** | **4.46** | **4.53** |

### 消融实验

| 方法 | PSNR ↑ | FID ↓ | FVD ↓ | OC ↑ |
|---|---|---|---|---|
| HCU (baseline) | 28.25 | 22.89 | 248.6 | 0.907 |
| + separate RoPE | 29.73 | 22.66 | 223.8 | 0.908 |
| + ref-in-bbox | 30.34 | 18.23 | 101.9 | 0.919 |
| + HS RoPE | 30.88 | 17.92 | 103.9 | 0.915 |
| + HS RoPE + SAG | 31.21 | 16.79 | 98.09 | 0.920 |
| + HS RoPE + SAG + FLF (full) | **31.71** | **11.53** | **67.95** | **0.937** |

### 关键发现
- Head-Sliding RoPE 比 separate RoPE 提升 1.15 dB PSNR，比 ref-in-bbox 提升 0.54 dB
- 长视频场景下优势更大：与 VACE 的 PSNR 差距从 3.11 扩大到 4.37
- 用户研究中参考保真度评分（RF）4.64 vs. VACE 的 2.80，差距巨大
- 模型对可变形物体、动态物理效果、遮挡和旋转均表现鲁棒

## 亮点与洞察
- **Head-Sliding RoPE** 是优雅的位置编码创新：不同注意力头看到参考 token 在不同"时间点"，自然实现时间均衡
- 两级空间门控（硬掩码 + 软门控）的分工清晰：硬掩码控制"哪里"，软门控控制"多强"
- 仅 0.95% 的额外参数即可显著提升 HOI 质量，体现了轻量级设计的价值
- 支持跨物体重演（如包包→口红、奶茶杯、魔法棒），电商场景实用性极强

## 局限性 / 可改进方向
- 依赖预训练的 Wan-14B 模型，自身不独立
- 训练数据仅约 19K 视频
- 评估主要基于 AnchorCrafter 数据集（50+50 视频），规模偏小
- 首帧需要通过外部图像编辑方法提供，增加了端到端使用的复杂度

## 相关工作与启发
- 与 VACE（通用视频编辑）形成互补：VACE 泛化性强但 HOI 一致性差，GenHOI 专注 HOI 一致性
- HOI-Swap 的帧间 warping 方案在野外场景的泛化性不足
- Head-Sliding RoPE 的思路可推广到其他需要条件 token 长程影响的任务

## 评分
- ⭐⭐⭐⭐⭐ 创新性：Head-Sliding RoPE 和空间注意力门控是新颖且有效的架构设计
- ⭐⭐⭐⭐ 实验充分性：全面的定量对比 + 消融 + 30 人用户研究 + 丰富的定性结果
- ⭐⭐⭐⭐ 实用价值：0.95% 额外参数，电商/数字人场景直接落地
- ⭐⭐⭐⭐ 写作质量：方法描述清晰，图示丰富，动机-方法-实验逻辑链完整
