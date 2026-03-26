# RAGTrack: 语言增强的 RGBT 目标跟踪

**日期**: 2026-03-04  
**arXiv**: [2603.03617](https://arxiv.org/abs/2603.03617)  
**代码**: https://github.com/IdolLab/RAGTrack  
**领域**: 视频理解  
**关键词**: RGBT tracking, retrieval-augmented generation, multi-modal tracking, language-aware, adaptive token fusion

## 一句话总结

RAGTrack 首次将语言描述引入 RGBT 跟踪，通过多模态 Transformer 编码器统一建模视觉-语言特征、自适应 Token 融合解决搜索冗余和模态差异、以及 RAG 机制实现上下文感知的时序推理，在四个 RGBT 基准上全面超越 SOTA。

## 研究背景与动机

1. **领域现状**：RGBT 跟踪利用可见光和热红外互补信息进行全天候目标定位，已有 ViPT、BAT、SUTrack 等多种融合策略。
2. **现有痛点**：(a) 现有 RGBT 跟踪器仅用初始帧视觉信息建模目标，无法应对剧烈外观变化导致 drift；(b) 搜索区域存在大量冗余背景 token，降低跟踪精度；(c) RGB 和 TIR 模态间的异质 gap 阻碍有效跨模态对应建立。
3. **核心矛盾**：视觉模板信息有限且歧义——同一区域可能包含扫帚、簸箕或行人下半身，纯视觉线索不足以区分；缺乏高层语义引导。
4. **本文要解决什么？** (1) 引入语言为 RGBT 跟踪提供高层语义表示；(2) 解决搜索冗余和模态 gap；(3) 实现跨帧的时序推理能力。
5. **切入角度**：语言提供比图像更抽象的目标理解，包括类别、外观属性和运动状态，能有效区分目标与背景。利用 MLLM 自动生成文本标注，无需人工。
6. **核心 idea 一句话**：用 RAG 机制维护动态知识库实现时序语言推理 + 自适应 token 融合解决搜索冗余和模态 gap。

## 方法详解

### 整体框架

输入：RGB/TIR 搜索图 $\mathbf{X}_m^t$、模板图 $\mathbf{Z}_m^t$、语言描述 $\mathbf{L}^t$。三个核心模块串联：MTE（特征编码）→ ATF（token 融合）→ CRM（时序推理）→ 预测头输出 bounding box。参数共享处理 RGB 和 TIR 两个分支。

### 关键设计

1. **多模态 Transformer 编码器 (MTE)**:
   - 做什么：统一建模视觉和语言 token
   - 核心思路：文本通过 CLIP 编码器得到语义特征 $\hat{\mathbf{H}}^t = \mathcal{T}(\mathbf{H}^t)$；引入可学习序列前缀 "A sequence of a [*] object:" 增强时序感知；将推理 token $\mathbf{R}_m^t$、文本 token、模板 token、搜索 token 拼接后通过多头自注意力统一建模
   - 设计动机：文本特征与视觉特征在同一空间交互，使语义信息直接增强特征判别力

2. **自适应 Token 融合 (ATF)**:
   - 做什么：动态选择目标相关 token + 自适应通道交换
   - **Token 选择**：利用自注意力分数作为 token 重要性指标，聚合搜索 token 与推理/文本/模板/搜索之间的注意力分数 $\mathbf{A}_{total}^m$，按保留率 $\gamma=85\%$ 筛选高分 token——无参数、无额外计算
   - **通道交换**：计算 RGB 与 TIR 特征在通道维度的跨模态相关性 $\mathbf{S} = ((\mathbf{F}_B^l)^T \mathbf{W}_B^l)((\mathbf{F}_R^l)^T \mathbf{W}_R^l)^T$，选择相关性最高的通道进行交换（交换率 $\sigma=50\%$）
   - 设计动机：token 选择减少冗余背景干扰，通道交换弥合模态 gap；在第 6/12/18/24 层插入实现渐进融合

3. **上下文感知推理模块 (CRM)**:
   - 做什么：通过 RAG 机制维护动态知识库 + MLLM 生成自适应目标描述
   - **Construction**：维护 $n=4$ 个历史文本特征嵌入 $\mathbf{D}^m$，新特征仅在与现有条目最大余弦相似度 < 阈值 $\lambda=1.0$ 时加入
   - **Retrieval**：用当前查询从知识库检索 top-$k=2$ 个相关特征 $\mathbf{V}^m$
   - **Augmentation**：推理 token 通过 MLP 融合推理/文本/模板的 pooled 特征，传播到下一帧
   - **Generation**：每帧用 QWen2.5-VL-3B 根据跟踪结果生成新的目标描述，动态更新语言输入

### 损失函数 / 训练策略

$$\mathcal{L} = L_{cls} + \lambda_{iou} L_{iou} + \lambda_{L_1} L_1$$

- $L_{cls}$: focal loss，$\lambda_{iou}=2$，$\lambda_{L_1}=5$
- HiViT-B 骨干（从 SOT 初始化），CLIP 文本编码器，AdamW $lr=10^{-4}$，4× V100，batch=16
- 在 LasHeR 训练集上训练，模板 $128\times128$，搜索 $256\times256$

## 实验关键数据

### 主实验

在四个 RGBT 基准上的SOTA对比：

| 方法 | GTOT MPR/MSR | RGBT210 PR/SR | RGBT234 MPR/MSR | LasHeR PR/NPR/SR |
|------|-------------|---------------|-----------------|-----------------|
| SUTrack | - | - | 92.1/69.2 | 75.8/-/60.9 |
| STTrack | - | - | 89.8/66.7 | 76.0/-/60.3 |
| AINet | - | 87.5/64.8 | 89.2/67.3 | 74.2/70.1/59.1 |
| **RAGTrack** | **95.1/79.3** | **93.2/67.1** | **93.8/69.5** | **76.8/73.0/61.1** |

### 消融实验

| 配置 | RGBT234 MPR | RGBT234 MSR | 说明 |
|------|------------|------------|------|
| Baseline | 87.9 | 64.5 | 骨干+卷积融合 |
| + CRM* (无文本) | 89.1 | 65.0 | 仅时序推理 |
| + MTE + CRM* | 91.1 | 66.7 | 加入文本统一建模 |
| + MTE + CRM | 91.8 | 67.4 | 完整 CRM（含语言生成）|
| + MTE + CRM + ATF | **93.8** | **69.5** | 完整 RAGTrack |

### 关键发现

- **ATF 贡献最大**：在已有 MTE+CRM 的基础上再加 ATF，MPR +2.0%，MSR +2.1%，且参数量最少（101.8M vs TBSI 145.9M）
- **语言信息关键**：CRM* (无文本) → CRM（有文本）提升 0.7% MPR，验证语言引导的价值
- **对缺失文本鲁棒**：即使 100% 文本缺失，RAGTrack 仍达 92.9% MPR / 68.8% MSR（超过 AINet），因为 RAG 机制能通过检索历史推理补偿

## 亮点与洞察

- **首次在 RGBT 跟踪中引入语言**：通过 MLLM 自动标注避免人工成本，且 RAG 机制使语言信息随时间动态更新
- **ATF 的"免费午餐"**：直接复用自注意力分数做 token 选择，零额外参数，却效果最好——说明搜索冗余是被严重忽视的性能瓶颈
- **通道交换弥合模态 gap**：比 TBSI 的 template-bridged interaction 更参数高效并且效果更好

## 局限性 / 可改进方向

- **MLLM 推理开销**：每帧调用 QWen2.5-VL-3B 生成描述，影响实际部署速度（24.3 FPS 已含此开销）
- **语言标注质量依赖 MLLM**：可能引入幻觉，虽经人工校审但大规模部署时难以保证
- **仅在 RGBT 验证**：框架理论上可推广到 RGB-D、RGB-Event 等多模态跟踪，但尚未验证

## 相关工作与启发

- **vs ViPT/BAT/SDSTrack**: 它们用 visual prompt 增强多模态跟踪，但缺少语言引导和时序推理
- **vs ChatTracker/DTLLM-VLT**: 它们也引入 LLM，但局限于 RGB-Language 跟踪，且缺乏 ATF 式的 token 选择
- **vs CKD**: CKD 用知识蒸馏弥合模态 gap，RAGTrack 用通道交换更直接

## 评分

- 新颖性: ⭐⭐⭐⭐ 首次将语言+RAG 引入 RGBT 跟踪，ATF 设计巧妙
- 实验充分度: ⭐⭐⭐⭐⭐ 四个基准、详尽消融、属性分析、鲁棒性实验齐全
- 写作质量: ⭐⭐⭐⭐ 结构清晰，图示丰富
- 价值: ⭐⭐⭐⭐ 为多模态跟踪开辟语言增强新范式，代码开源
