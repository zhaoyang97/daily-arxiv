# Facial Expression Generation Aligned with Human Preference for Natural Dyadic Interaction

**日期**: 2026-03-07  
**arXiv**: [2603.07093](https://arxiv.org/abs/2603.07093)  
**代码**: 无  
**领域**: 多模态/VLM  
**关键词**: facial expression generation, human preference alignment, reinforcement learning, vision-language-action model, dyadic interaction

## 一句话总结

提出一种基于人类反馈强化学习（RLHF）的面部表情生成方法，通过将表情生成建模为身份无关空间中的动作学习过程，结合 VLA 模型与 DPO 算法，实现听者表情与说话者情感的社会性对齐。

## 研究背景与动机

**现状**：双人交互（dyadic interaction）中的听者表情生成已取得显著进展，基于扩散模型和 GAN 的方法可以生成视觉上逼真的表情。

**痛点**：现有方法将数据集中所有样本视为等价正确的模仿目标，未区分高质量社交互动与中性/注意力分散的状态。这导致生成的表情可能在几何重建上准确，但在社会规范和情感期望上不对齐——例如说话者表达厌恶时，听者却生成了开心的表情，造成交互失调。

**核心矛盾**：
1. **身份偏差问题**：生成的表情常与身份和外观纠缠，导致人类评估者混淆视觉真实感与表情质量，无法获得无偏的反馈信号
2. **开环生成问题**：大多数方法采用开环方式，生成后不随对话动态调整，无法实现持续对齐

**本文方案**：将表情生成建模为身份无关参数空间中的动作学习过程（action learning），使人类反馈聚焦于表情质量而非外观；建立闭环反馈机制，使听者表情能动态响应说话者的多模态线索。核心技术路线：SFT 预训练 VLA 模型 → 人类标注偏好 → DPO 强化学习对齐。

## 方法详解

### 整体框架

方法分为两阶段 pipeline：

1. **Stage 1（SFT 阶段）**：训练 Vision-Language-Action (VLA) 模型，以说话者的视觉帧和语言内容为输入，通过监督微调学习生成听者的 FLAME 3DMM 面部参数
2. **Stage 2（RL 阶段）**：利用 SFT 模型采样多个候选表情序列，由人类标注者评分排序，构建偏好数据集，通过 DPO 算法优化策略

### 关键设计

1. **身份无关的动作空间（Identity-Independent Action Space）**：
    - 核心思路：将表情生成定义为 FLAME 模型参数空间中的动作预测，而非直接生成图像/视频
    - 面部参数 $\mathbf{A}_t = [\mathbf{a}_t^{\text{exp}}; \mathbf{a}_t^{\text{pose}}]$ 由表情系数和头部姿态组成，通过固定身份参数 $\mathbf{a}^{\text{shape}}$ 的 FLAME 模型渲染 3D 面部网格
    - 设计动机：解耦身份与表情，使人类反馈仅评估表情的社交恰当性，避免外观偏差
    - 公式：$\mathcal{M}_t = \text{FLAME}(\mathbf{a}^{\text{shape}}, \mathbf{a}_t^{\text{exp}}, \mathbf{a}_t^{\text{pose}})$

2. **Vision-Language-Action (VLA) 模型**：
    - **双流视觉编码器**：每帧图像同时经过 DINO（捕捉姿态和细微表情细节）和 SigLIP（编码全局情感语义和社交线索）提取特征，拼接后通过 MLP 映射到 LLM 输入空间
    - **LLM 骨干**：采用 7B 参数的 LLaMA 2 作为核心推理引擎
    - **Action De-Tokenizer**：将连续面部动作离散化为 256 个 bin 的 token，先对训练集动作值排序并截取上下 1% 异常值，再在有效范围内均匀划分——集中建模能力于有效运动区间，提升微表情和头部姿态的精度
    - 设计动机：借鉴 RT-2 的思路，将连续控制问题转化为 LLM 可处理的离散 token 预测问题

3. **人类反馈强化学习（Human-Feedback RL）**：
    - **偏好数据收集**：对每个说话者输入，用 SFT 策略采样 $N=4$ 个候选听者动作序列，加上 ground-truth 共 5 个候选，渲染为交互视频供标注者评估
    - **评估维度**（四维加权打分）：
     - Empathy（共情）、Appropriateness（恰当性）、Engagement（参与度）、Naturalness（自然度）
     - 最终偏好分：$r(\tau^j) = \alpha_{\text{emp}} \cdot \text{Empathy} + \alpha_{\text{app}} \cdot \text{Appropriateness} + \alpha_{\text{eng}} \cdot \text{Engagement} + \alpha_{\text{nat}} \cdot \text{Naturalness}$
   - **偏好对构建**：每组候选中最高分为 preferred，最低分为 dispreferred，构成 DPO 训练对
   - 设计动机：对比式 DPO 目标优于单纯在正样本上做 SFT，能学习区分好坏行为

### 损失函数 / 训练策略

**SFT 阶段**：

- 预测损失：表情和姿态分别计算交叉熵损失并加权

$$\mathcal{L}_{\text{pre}} = \frac{\lambda_{\text{exp}}}{T}\sum_{t=1}^{T}\mathcal{L}_{\text{cross}}(\mathbf{a}_t^{\text{exp*}}, \mathbf{a}_t^{\text{exp}}) + \frac{\lambda_{\text{pose}}}{T}\sum_{t=1}^{T}\mathcal{L}_{\text{cross}}(\mathbf{a}_t^{\text{pose*}}, \mathbf{a}_t^{\text{pose}})$$

- 时序平滑正则化：约束相邻帧动作变化，保证时序连贯

$$\mathcal{L}_{\text{temp}} = \frac{1}{N}\sum_{i=1}^{N}\frac{1}{T-1}\sum_{t=1}^{T-1}(\|\mathbf{a}_{t+1}^{\text{exp}} - \mathbf{a}_t^{\text{exp}}\|_2^2 + \|\mathbf{a}_{t+1}^{\text{pose}} - \mathbf{a}_t^{\text{pose}}\|_2^2)$$

- 总损失：$\theta_{\text{SFT}}^* = \arg\min_\theta [\mathcal{L}_{\text{pre}} + \lambda_{\text{temp}} \mathcal{L}_{\text{temp}}]$

**RL 阶段**：

- DPO 损失（冻结 SFT 模型作为 reference policy $\pi_{\text{ref}}$）：

$$\mathcal{L}_{\text{policy}} = -\mathbb{E}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(\mathbf{A}_{1:T}^w|\mathbf{S}_{1:T})}{\pi_{\text{ref}}(\mathbf{A}_{1:T}^w|\mathbf{S}_{1:T})} - \beta\log\frac{\pi_\theta(\mathbf{A}_{1:T}^l|\mathbf{S}_{1:T})}{\pi_{\text{ref}}(\mathbf{A}_{1:T}^l|\mathbf{S}_{1:T})}\right)\right]$$

## 实验关键数据

### 主实验

**数据集**：L2L-trevor（单听者数据集）和 Realtalk（692 段对话视频，115 小时）

**评估指标**：L2（重建精度）、FD（分布相似度）、Variation/Diversity（动态丰富度）、P-FD（时序对齐运动质量）、L2 Affect（情感同步性）

| 方法 | L2 ↓ | FD ↓ | P-FD ↓ | L2 Affect(×10²) ↓ |
|------|------|------|--------|-------------------|
| **L2L-trevor 数据集** | | | | |
| LM-listener | 0.4345 | 17.6299 | 19.1583 | 6.3992 |
| MMLHG (SOTA) | 0.2910 | 10.0949 | 11.3908 | 2.6575 |
| Ours (SFT) | 0.3015 | **9.1473** | 11.2975 | 2.5724 |
| Ours (SFT+RL) | 0.3129 | 10.2385 | **10.8247** | **2.4842** |
| **Realtalk 数据集** | | | | |
| LM-listener | 0.2416 | 10.8423 | 10.5483 | 12.2730 |
| MMLHG (SOTA) | 0.1021 | 3.7914 | 3.8145 | 6.0427 |
| Ours (SFT) | **0.0824** | **3.2425** | 3.8036 | 4.5207 |
| Ours (SFT+RL) | 0.0973 | 3.5842 | **3.7914** | **4.3531** |

**用户研究（MOS，1-5 分）**：

| 方法 | Appropriateness | Empathy | Engagement | Naturalness |
|------|----------------|---------|------------|-------------|
| LM-listener | 2.7 | 3.1 | 3.4 | 2.9 |
| MMLHG | 3.0 | 3.3 | 3.5 | 3.1 |
| Ours (SFT) | 3.2 | 3.4 | 3.7 | 3.3 |
| Ours (SFT+RL) | **4.5** | **4.1** | **4.2** | **4.5** |

### 消融实验

| 方法 | L2 ↓ | FD ↓ | P-FD ↓ | L2 Affect(×10²) ↓ |
|------|------|------|--------|-------------------|
| Full (Ours) | 0.0973 | 3.5842 | **3.7914** | **4.3531** |
| Random-Prefer | 0.3142 | 12.3549 | 12.0354 | 15.2463 |
| SFT-Preferred | 0.1132 | 3.6791 | 3.9165 | 5.5190 |
| SFT-Only | **0.0824** | **3.2425** | 3.8036 | 4.5207 |

### 关键发现

- **SFT 模型在几何重建指标（L2、FD）上最优**，因为它直接模仿 ground truth；但 **SFT+RL 模型在情感对齐指标（L2 Affect、P-FD）上最优**，说明 RL 将优化重心从几何重建转向社会/情感对齐
- **Random-Prefer 显著退化**（L2 Affect 从 4.35 飙升到 15.25），验证了准确人类反馈的必要性，随机偏好标签甚至比不用 RL 更差
- **DPO 优于 SFT-Preferred**（L2 Affect 4.35 vs 5.52）：对比式目标函数学习区分好坏行为，比仅在正样本上做 SFT 更有效
- 用户研究中 SFT+RL 的 Appropriateness 从 SFT 的 3.2 跃升至 4.5（+1.3），Naturalness 从 3.3 到 4.5（+1.2），增幅巨大
- 定性分析显示 MMLHG 存在"幻觉正面情绪"问题（如说话者讨论严肃话题时生成不恰当的微笑），本方法能正确理解上下文语境

## 亮点与洞察

- **身份解耦的动作空间设计**是最大亮点：在 FLAME 参数空间而非像素空间做生成和评估，从根本上解决了人类反馈中身份/外观偏差的问题，这一思路可迁移到其他需要无偏反馈的生成任务
- **VLA 框架的创新应用**：将原本用于机器人控制的 Vision-Language-Action 范式迁移到面部表情生成，用 LLM 作为多模态推理核心，256-bin 离散化策略巧妙桥接了连续动作与离散 token
- **双流视觉编码**（DINO + SigLIP）兼顾细粒度面部动态和全局情感语义，设计合理
- **实验揭示的 trade-off 很有洞察**：RL 对齐后几何指标略降但情感指标显著提升，说明"看起来像 GT"和"社会性恰当"是两个不同的优化目标，未来工作应同时优化两者
- **闭环交互策略**：将表情生成建模为序列决策问题，听者动态响应说话者变化，比一次性生成更贴合真实交互

## 局限性 / 可改进方向

- **标注成本高**：每个样本需采样 4 个候选 + GT 共 5 个序列，渲染为视频后由人工打分，扩展性受限
- **仅使用 FLAME 参数**：无法建模眨眼、眼球运动等精细面部动作，表达力有上限
- **数据集规模有限**：L2L-trevor 是单人数据集，Realtalk 虽有 115 小时但场景多样性不足
- **RL 阶段的几何指标退化**：SFT+RL 的 L2/FD 略差于 SFT-Only，说明 DPO 可能过度偏向情感对齐而牺牲了重建精度，需要更精细的多目标平衡
- **缺少实时推理性能分析**：7B LLaMA 骨干的推理速度可能无法满足实时交互需求
- **可尝试 AI 标注替代人工**：用 VLM（如 GPT-4V）做偏好标注来降低成本，但需验证与人类偏好的一致性

## 相关工作与启发

- **vs Avatar Forcing**：同样引入偏好对齐到 3D talking head，但 Avatar Forcing 依赖合成代理数据而非真实人类反馈，无法捕捉微妙社会规范；本文的闭环人类反馈框架更可靠
- **vs MMLHG**：当前 SOTA，融合对话内容与 FLAME 参数生成听者反应，但将所有训练样本视为等价正确，无法区分高/低质量交互
- **vs RLHF in NLP**：将 NLP 领域成熟的 RLHF 范式（SFT → RM → PPO/DPO）首次系统性迁移到面部表情生成，关键创新在于身份无关空间解决了反馈偏差问题
- **vs RT-2**：借鉴其将连续机器人动作离散化为 LLM token 的思路，应用于面部动作参数

## 评分

- 新颖性: ⭐⭐⭐⭐ 首次将 RLHF 系统性引入面部表情生成，身份无关动作空间设计巧妙，但整体框架是 SFT+DPO 的标准范式
- 实验充分度: ⭐⭐⭐⭐ 两个数据集 + 用户研究 + 消融实验覆盖较全，但缺少推理速度分析和更多数据集验证
- 写作质量: ⭐⭐⭐⭐ 动机阐述清晰，方法描述有条理，但部分公式符号不够统一（如消融表中 P-ID 和 P-FD 混用）
- 价值: ⭐⭐⭐⭐ 为面部表情生成引入人类偏好对齐开辟了新方向，用户研究的大幅提升很有说服力，但标注成本限制了实际应用
