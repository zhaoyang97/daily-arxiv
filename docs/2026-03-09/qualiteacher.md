# QualiTeacher: Quality-Conditioned Pseudo-Labeling for Real-World Image Restoration

**日期**: 2026-03-09  
**arXiv**: [2603.08030](https://arxiv.org/abs/2603.08030)  
**代码**: 即将开源  
**领域**: 图像生成  
**关键词**: image restoration, pseudo-label, mean-teacher, NR-IQA, preference optimization

## 一句话总结
将伪标签质量从需要过滤的噪声转化为条件监督信号——将 NR-IQA 分数注入学生网络使其学习质量分级的修复流形，结合基于 DPO 的偏好优化确保分数-质量单调映射，使学生网络能外推到超越教师的修复质量。

## 研究背景与动机

1. **领域现状**: 真实世界图像修复（RWIR）缺少干净的 ground-truth，Mean-Teacher 框架用教师网络生成伪标签（PL）监督学生是主流做法。

2. **现有痛点**: 伪标签质量参差不齐——无条件信任低质量 PL 会让学生学到伪影（unconditional trust），但丢弃低质量 PL 又限制数据多样性（aggressive filtering）。更糟的是，过度平滑的输出可能骗过 IQA 获得高分而通过过滤。

3. **核心矛盾**: "全有或全无"的 PL 处理方式——要么学噪声，要么缺数据。

4. **核心 idea**: 不过滤低质量 PL，而是将质量分数作为条件注入学生网络——让学生理解不同质量级别意味着什么，从而（1）不盲目模仿低质量 PL 的伪影，（2）学会质量改善的"方向"，从而外推到更高质量。

## 方法详解

### 整体框架
Teacher（EMA）生成多增强 PL → 多 IQA 模型打分 + 双重过滤 → 分数注入学生网络（正弦编码+MLP→特征加法）→ 分块加权损失 + 基于分数的偏好优化 + 裁剪一致性损失。

### 关键设计

1. **Quality-Conditioned Score Injection**:
    - 将 NR-IQA 集成分数 $S$ 通过正弦位置编码 $\gamma(S)$ + MLP 映射到特征维度 $\mathbf{e}_S$
    - 在网络中间层（如 U-Net bottleneck）通过加法注入：$\mathbf{F}' = \mathbf{F} + \mathbf{e}_S$
    - 推理时注入高分数条件，引导学生输出超越教师的质量

2. **Multi-Augmentation + Multi-IQA 评估**:
    - 3 种几何增强（水平翻转/垂直翻转/90°旋转）产生多样化 PL
    - 3 个互补 IQA 模型（MUSIQ-KonIQ/BRISQUE/CLIP-IQA）覆盖低级失真+语义级评估
    - 双重过滤（cross-IQA 一致性 + cross-augmentation 稳定性）+ 记忆库保留 Top-3

3. **Score-Based Preference Optimization**:
    - 类比 DPO：高 IQA 分数输出为 preferred，低分数输出为 rejected
    - $\mathcal{L}_1$ 强制高/低分数输出间有最小质量差（inter-space separation）
    - $\mathcal{L}_2$ 锚定高分数输出必须超越教师最差 PL（upward anchor）
    - $\mathcal{L}_{reg}$ 限制注入层权重变化防止干扰修复能力

4. **Cropped Consistency Loss**:
    - 防止 reward hacking：比较"先修复再裁剪评分"vs"先裁剪再修复评分"
    - 如果模型用局部统计捷径膨胀分数，两种顺序的 IQA 分数会不一致
    - $\mathcal{L}_{cropped} = \|S_1 - S_2\|_1$

### 训练策略
- EMA 教师（α=0.998）
- 联合损失：$\mathcal{L} = \mathcal{L}_{rec} + \mathcal{L}_{per} + \mathcal{L}_{pref} + \mathcal{L}_{cropped}$
- AdamW，lr=5e-5，仅 10K 迭代
- 分数 >7 合并为统一高质量空间

## 实验关键数据

### 主实验（多任务 NR-IQA 评估）

| 方法 | 去雪 CLIP-IQA ↑ | 去雨 MUSIQ ↑ | 去雾 HyperIQA ↑ |
|------|----------------|-------------|-----------------|
| SemiDDM | baseline | baseline | baseline |
| + QualiTeacher | **+提升** | **+提升** | **+提升** |

### 消融实验

| 配置 | 效果 |
|------|------|
| 无 score injection | 回退到标准 MT，质量上限受限于教师 |
| 无偏好优化 | 不同分数条件的输出质量区分不明显 |
| 无 cropped consistency | reward hacking 风险增加 |
| 无 multi-augmentation | PL 质量谱窄，学习多样性不足 |

### 关键发现
- Score-conditioned 学生在推理时用高分数条件确实能输出超越教师质量的修复结果
- DPO 偏好优化显著提升了分数-质量的单调映射质量
- 作为 plug-and-play 策略可提升多个现有框架

## 亮点与洞察
- **将 PL 质量从"负债"变为"资产"**: 全新范式——不过滤而是条件化
- **DPO 首次引入图像修复**: 巧妙绕过了确定性模型无概率输出的理论障碍
- **Cropped consistency 防 reward hacking**: 实用的防御设计
- **学生超越教师**: 通过学习质量梯度方向实现外推

## 局限性 / 可改进方向
- NR-IQA 模型本身的偏差会影响质量评估准确性——如果 IQA 模型对某类伪影不敏感，条件化就失效
- 分块加权固定为 2×2，对不同尺度退化可能不够灵活，自适应分块策略值得探索
- 仅在修复任务验证，超分辨率/去模糊/去压缩等任务未测试
- Score injection 的位置选择（bottleneck）可能不是最优的，多层注入可能更好
- IQA 集成分数的权重（0.4/0.4/0.2）为手动设定，自动权重学习可能更鲁棒

## 相关工作与启发
- **vs Real-ESRGAN / StableSR**: 这些方法用合成退化模型构造训练对，但合成-真实 domain gap 大；QualiTeacher 直接在真实退化上工作，更接近实际
- **vs SemiDDM / SnowMaster**: 同为 Mean-Teacher 框架，但它们无条件信任或二元过滤 PL，QualiTeacher 用质量分数条件化替代过滤
- **vs DPO 在生成模型中的应用**: DPO 在 LLM/扩散模型中广泛使用，但未在确定性图像修复模型中应用，本文巧妙绕过了无概率输出的理论障碍
- **vs Kendall 不确定性加权**: 类似思路但针对多任务学习，QualiTeacher 针对单任务的伪标签质量变化

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 质量条件化 + DPO 偏好优化的全新范式
- 实验充分度: ⭐⭐⭐⭐ 多任务（去雪/雨/雾/暗光/水下）+ 详细消融
- 写作质量: ⭐⭐⭐⭐⭐ 动机清晰、方法严谨、公式完整
- 价值: ⭐⭐⭐⭐⭐ 为有噪声监督学习提供了新范式
