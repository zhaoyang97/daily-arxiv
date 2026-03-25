# SpatialMAGIC: A Hybrid Framework Integrating Graph Diffusion and Spatial Attention for Spatial Transcriptomics Imputation

**日期**: 2026-03-06  
**arXiv**: [2603.06780](https://arxiv.org/abs/2603.06780)  
**代码**: https://github.com/sayeemzzaman/SpatialMAGIC  
**领域**: 生物信息学 / 空间转录组学  
**关键词**: spatial transcriptomics, graph diffusion, spatial self-attention, imputation, clustering

## 一句话总结
提出 SpatialMAGIC，将 MAGIC 图扩散与 Transformer 空间自注意力融合，对空间转录组数据进行缺失值填补，在多平台上实现聚类精度和生物可解释性的双提升。

## 研究背景与动机
1. **领域现状**: 空间转录组学（ST）可在组织空间上下文中映射基因表达，但高分辨率数据（如 Stereo-seq）极度稀疏，超过 84% 的表达值为零。
2. **现有痛点**: 已有方法面临关键取舍——图神经网络/扩散模型计算开销大、扩展性差；单纯的图扩散方法（如 MAGIC）无法利用空间坐标信息；深度学习模型在全局扩散与局部结构保持之间难以平衡。
3. **核心矛盾**: 现有方法要么只用基因表达相似性（忽略空间位置），要么计算代价过高难以应用于大规模数据集（>50k spots）。
4. **切入角度**: 同时利用基因表达的图扩散（捕获长程依赖）和空间坐标的 Transformer 注意力（捕获局部空间结构），通过融合模块统一两种信息。
5. **核心idea一句话**: 用 MAGIC 图扩散做全局去噪 + Transformer 空间注意力做局部感知，再用自编码器融合两路信息完成最终填补。

## 方法详解
### 整体框架
输入基因表达矩阵 $\mathbf{X} \in \mathbb{R}^{n \times g}$ 和空间坐标 $\mathbf{S} \in \mathbb{R}^{n \times 2}$。流程分三步：(1) MAGIC 图扩散对表达矩阵去噪填补；(2) Transformer 编码空间坐标生成空间嵌入；(3) 融合两路信息通过编码器-解码器重建增强表达谱。

### 关键设计
1. **MAGIC 图扩散模块**: 
   - 对表达矩阵 PCA 降维后构建 kNN 图（$k=5$，最大邻居 $k_{max}=15$）
   - 用自适应高斯核计算亲和矩阵，对称化后行归一化得到转移矩阵 $\mathbf{P}$
   - 执行 $t$ 步随机游走扩散 $\mathbf{X}_{MAGIC} = \mathbf{P}^t \mathbf{X}_d$，实现长程信息传播
   - 核心思路：通过流形上的扩散过程平滑基因表达、恢复 dropout 值

2. **Spatial Transformer Attention 模块**:
   - 将 2D 空间坐标线性映射到 $d_s=32$ 维嵌入空间
   - 通过单层 Transformer 编码器（$h=2$ 头自注意力）学习全局空间依赖
   - 投影到基因维度后与 MAGIC 输出拼接：$\mathbf{X}_{fused} = [\mathbf{X}_{MAGIC} \| \mathbf{H}_{proj}]$
   - 设计动机：无需显式邻接矩阵或距离阈值，自适应学习空间关系

3. **融合精炼模块（Autoencoder）**:
   - 编码器：$2G \to 512 \to 256$ 的两层全连接 + ReLU + Dropout
   - 解码器：$256 \to 512 \to G$ 重建基因表达
   - 训练时对 MAGIC 填补结果随机遮蔽 20%，迫使模型利用空间信息恢复缺失值

### 损失函数 / 训练策略
- 损失函数：MSE 重建误差 $\mathcal{L} = \frac{1}{n}\sum_{i=1}^{n}\|\hat{\mathbf{x}}_i - \mathbf{x}_{MAGIC,i}\|_2^2$
- 训练策略：Adam 优化器，batch size $B=256$，20% 随机 masking 策略增强鲁棒性
- 选取 top $k=3000$ 高变异基因，PCA 降至 $d=100$ 维

## 实验关键数据
### 主实验

| 数据集 | Before | MAGIC | Attn PCA | Attn UMAP | **SpatialMAGIC** |
|--------|--------|-------|----------|-----------|-----------------|
| DX6_D2 (Stereo-seq) | 0.2661 | 0.2889 | 0.2818 | 0.2839 | **0.3254** |
| DT2_D0 (Stereo-seq) | 0.2847 | 0.3088 | 0.3194 | 0.3014 | **0.3301** |
| FB2_D1 (Stereo-seq) | 0.1679 | 0.2192 | 0.2580 | 0.2543 | **0.2993** |
| stickles (Slide-seq) | 0.1740 | 0.1764 | **0.2249** | 0.1736 | 0.2193 |
| diabetes T4 (Slide-seq) | 0.2657 | 0.2577 | 0.2336 | 0.2197 | **0.2688** |
| WT1_T3 (Slide-seq) | 0.2891 | 0.3049 | 0.2870 | 0.2287 | **0.3074** |
| GSE166692 (Sci-space) | 0.3095 | 0.4020 | 0.3717 | 0.3316 | **0.4216** |

*指标为 Adjusted Rand Index (ARI)，越高越好*

### 消融实验（运行时间对比）

| 数据集 | MAGIC (s) | SpatialMAGIC (s) | 倍数 |
|--------|-----------|------------------|------|
| DX6 | 191.50 | 291.56 | 1.52× |
| DT2 | 334.75 | 1451.36 | 4.3× |
| FB2 | 282.91 | 332.74 | 1.18× |

*实验环境：Kaggle GPU，双 NVIDIA Tesla T4 (15 GiB VRAM)，~30 GiB RAM*

### 关键发现
- SpatialMAGIC 在 7 个数据集中的 6 个上取得最佳 ARI，仅在 stickles 上略低于 Attention PCA
- Sci-space 数据集上提升最大：ARI 从 0.3095 → **0.4216**（+0.112）
- 差异表达基因分析显示填补后新检测到多个生物学相关基因（如 Mdm2、Plg、Ephx2）
- 通路富集分析验证了恢复基因参与代谢、转运和神经信号通路

## 亮点与洞察
- **双路互补设计**: 图扩散捕获全局基因表达模式，空间注意力保持局部组织结构，二者互补性强
- **masking 训练策略**: 20% 随机遮蔽训练让模型学会利用空间信息恢复缺失表达，类似 MAE 的思想
- **生物可解释性**: 不仅提升聚类指标，还通过 DEG 分析和通路富集验证了填补结果的生物学意义
- 跨平台泛化：在 Stereo-seq、Slide-seq、Sci-space 三种技术平台上均有效

## 局限性 / 可改进方向
- 计算开销较高，DT2 数据集上达 4.3× MAGIC 运行时间，大规模数据需优化
- Transformer 模块在超高分辨率数据集上可能是计算瓶颈，可引入稀疏注意力
- 缺乏与 DiffusionST、SpotDiff 等最新深度生成模型的直接对比
- 未在真实生物实验中验证填补结果的准确性
- 未来可融合多模态数据（组织学图像、蛋白组学）

## 相关工作与启发
- **MAGIC** (van Dijk et al., 2017): 基础图扩散方法，本文在其上扩展空间感知能力
- **ADEPT**: 图自编码器 + DEG 聚类，ARI 表现好但扩展性差
- **DiffusionST**: GCN + ZINB + 扩散模型，ARI 0.43-0.65 但计算昂贵（>50k spots 不适用）
- **Impeller**: 异构图 + 可学习路径算子，解决过平滑问题

## 评分
- ⭐⭐⭐ 新颖性：图扩散+空间注意力的组合思路直觉但有效，不算全新范式
- ⭐⭐⭐⭐ 有效性：7个数据集全面评估，大多数取得 SOTA，生物学验证充分
- ⭐⭐⭐ 效率：计算开销是主要瓶颈，部分数据集慢 4 倍以上
- ⭐⭐⭐ 写作：结构完整，实验详实，但公式符号略显冗余
