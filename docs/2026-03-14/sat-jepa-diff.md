# Sat-JEPA-Diff: Bridging Self-Supervised Learning and Generative Diffusion for Remote Sensing

**日期**: 2026-03-14  
**arXiv**: [2603.13943](https://arxiv.org/abs/2603.13943)  
**代码**: 有（GitHub）  
**领域**: 图像生成 / 遥感时序预测  
**关键词**: satellite forecasting, IJEPA, latent diffusion, self-supervised learning, Sentinel-2

## 一句话总结
提出 Sat-JEPA-Diff，用 IJEPA 在 latent 空间预测未来帧的语义表示，再通过 ~25M 参数的 cross-attention adapter 引导冻结的 SD 3.5 生成高保真卫星图像，在全球 100 个 ROI 的 Sentinel-2 数据集上 GSSIM 达 0.8984（比确定性方法高 11%+），FID 0.1475。

## 研究背景与动机

1. **领域现状**: 卫星时序预测（$t \to t+1$）是遥感监测的关键"虚拟传感器"，可弥补云覆盖导致的观测缺失，但现有方法在结构准确性和纹理逼真度之间存在根本性矛盾。
2. **确定性方法的瓶颈**: PredRNN / SimVP 优化像素级 MSE，导致"均值回归"——PSNR 高但输出模糊，掩盖伊斯坦布尔城市密度、模糊亚马逊农业用地边界，GSSIM 仅约 0.78，FID 高达 9.97–18.72。
3. **生成方法的缺陷**: DDPM / LDM 可生成逼真纹理，但缺乏语义约束时容易"幻觉"出不存在的道路拓扑、建筑等结构。MCVD 的 FID 0.196 但 GSSIM 仅 0.7665，结构保持能力不足。
4. **核心 idea**: 将预测解耦为"语义预测 + 条件生成"两阶段——IJEPA 在抽象 latent 空间做结构级预测（天然抗传感器噪声和大气变化），预测结果引导冻结 LDM 做纹理合成。与 MAE/SatMAE 等重建式方法不同，IJEPA 不在像素空间操作因此不会过拟合噪声。

## 方法详解

### 整体框架
两阶段管线：

- **阶段一：IJEPA 时序预测** — ViT 编码器（patch size 8, 输入 128×128）将当前帧编码为 $z_t \in \mathbb{R}^{256 \times 768}$，6 层 transformer 预测器 $P_\phi$ 预测 $\hat{z}_{t+1}$，线性投影层将 768 维映射到 Alpha Earth 64 维嵌入空间。EMA 目标编码器 $E_\xi$ 提供稳定的训练目标。
- **阶段二：条件扩散生成** — 预测嵌入 $\hat{z}_{t+1}$ + 32×32 粗分辨率 RGB 经 conditioning adapter 转换为 cross-attention 条件信号，注入冻结 SD 3.5 Medium 的 attention 层，结合 LoRA 微调生成 $\hat{I}_{t+1}$。

### 关键设计

1. **IJEPA 混合损失**: $\mathcal{L}_{\text{IJEPA}} = 20 \cdot L_1 + 2 \cdot (1 - \cos) + 2 \cdot \mathcal{L}_{\text{spatial}} + 0.5 \cdot \text{InfoNCE}$。空间方差项 $\mathcal{L}_{\text{spatial}}$ 防止表示坍塌（ablation 显示缺少该项方差趋近于零）。EMA 目标编码器动量从 0.999 cosine 增至 1.0。
2. **Conditioning Adapter（~25M 参数）**: 三层 MLP 将 IJEPA token 投影到 4096 维 cross-attention 空间；粗 RGB 分块为 64 个 token 经同样投影；全局 pooled 向量投影到 2048 维。可学习 sigmoid 融合门 $\alpha$（训练收敛至 ~0.5）平衡语义与结构信号。训练时以 $p=0.15$ 概率丢弃粗 RGB，迫使模型依赖语义预测。
3. **Flow Matching + LoRA**: 冻结 SD 3.5 核心 transformer，仅训练 LoRA（rank=8, alpha=16）和 adapter。AdamW 优化器，lr $10^{-4}$ cosine 衰减至 $10^{-6}$，100 epoch，单卡 RTX 5090，推理 20 步 Euler 采样。

## 实验关键数据

数据集覆盖全球 100 个 ROI，时间跨度 2017–2024，Sentinel-2 10m GSD RGB 三波段，80/20 训练/验证划分。

| 模型 | L1↓ | PSNR↑ | SSIM↑ | GSSIM↑ | LPIPS↓ | FID↓ |
|------|-----|-------|-------|--------|--------|------|
| Default baseline | 0.0131 | 37.52 | 0.9361 | 0.7858 | 0.0708 | 0.696 |
| PredRNN | 0.0117 | 38.38 | 0.9476 | 0.7836 | 0.0726 | 9.972 |
| SimVP v2 | 0.0131 | 37.63 | 0.9391 | 0.7719 | 0.0928 | 18.72 |
| MCVD | 0.0314 | 31.28 | 0.8637 | 0.7665 | 0.1890 | 0.196 |
| SD 3.5 (uncond.) | 0.0175 | 32.98 | 0.8398 | 0.8711 | 0.4528 | 0.153 |
| Ours (Panopticon enc.) | 0.0179 | 32.89 | 0.8398 | 0.8750 | 0.4475 | 0.148 |
| **Sat-JEPA-Diff** | **0.0158** | **33.81** | **0.8672** | **0.8984** | **0.4449** | **0.1475** |

消融与分析：

| 消融 / 分析 | 结论 |
|-------------|------|
| 去掉空间方差项 | 嵌入方差趋零，发生表示坍塌 |
| 去掉 InfoNCE | 早期训练不稳定，cosine 对齐速度明显变慢 |
| 换 Panopticon 编码器 | GSSIM 0.8750 / FID 0.1475，性能接近，方法对编码器不敏感 |
| 自回归 rollout (2018→2024) | 确定性方法 2–3 步后快速模糊；Sat-JEPA-Diff 保持 7 年跨度的锐利纹理 |

### 关键发现
- GSSIM 0.8984 比最佳确定性 baseline（0.7858）高 14.3%，比最佳生成 baseline SD 3.5（0.8711）高 3.1%，证明语义引导有效保持边缘与地理空间结构
- 确定性方法 PSNR 高（38.38）但 FID 极差（9.97–18.72），生成方法 FID 低（<0.2）但 PSNR 较低，验证了经典的感知-失真 trade-off
- LPIPS 0.4449 与 SD 3.5（0.4528）接近，但 L1 从 0.0175 降至 0.0158、MSE 从 0.0005 降至 0.0004，说明语义引导在保持感知质量的同时改善了像素保真度
- 消融显示去掉空间方差项后嵌入方差趋零导致表示坍塌，去掉 InfoNCE 后早期 cosine 对齐速度显著变慢
- 长程自回归 rollout（2018→2024，里约海岸）中确定性方法 2–3 步后坍塌为光谱模糊，Sat-JEPA-Diff 保持 7 年跨度的锐利纹理和高对比度

## 亮点与洞察
- **IJEPA 做时序预测**而非像素重建——在抽象语义空间预测天然抗传感器噪声和大气干扰，比 MAE/SatMAE 等重建式方法更鲁棒，且避免了对高频噪声的过拟合
- **冻结 SD + 轻量 adapter + LoRA** 的范式保留预训练生成先验，仅 ~25M adapter + LoRA 可训练参数即可适配遥感域，单卡 RTX 5090 即可完成 100 epoch 训练
- 融合门 $\alpha$ 自动收敛至 ~0.5，表明语义与结构信号同等重要；$p=0.15$ 的 reference dropout 进一步增强泛化能力
- 未来方向：用视觉-语言场景描述替代学习到的嵌入作为可预测的条件信号，有望引入更丰富的语义信息

## 局限性
- PSNR/SSIM 低于确定性方法（33.81 vs 38.38），LPIPS 0.4449 较高，像素保真度有牺牲——这是感知-失真 trade-off 的固有代价
- 仅在 Sentinel-2 RGB 三波段、100 ROI 单一数据集上验证，缺乏多光谱（如 13 波段）/ 多传感器（SAR）/ 多分辨率实验
- 无下游任务评估（变化检测、语义分割、土地利用分类等），定量指标以感知质量为主
- 消融仅做了 20 epoch 早期轨迹分析，作者也承认 full-scale 100 epoch 消融是 future work
- 自回归 rollout 仅有定性展示，缺少长程定量指标（如逐步 GSSIM 衰减曲线）

## 相关工作与启发
- Alpha Earth Foundation Model 提供 64 维像素级语义嵌入作为 IJEPA 监督目标——此类地理基础模型嵌入可作为通用语义锚点迁移到其他遥感时序任务
- Panopticon / TerraMind 等替代编码器的兼容性证明框架的通用性，不依赖特定基础模型
- "语义预测 + 条件生成"的两阶段范式可推广到视频预测、气象预报等场景；冻结大模型 + 轻量 adapter 的训练策略在资源受限场景下尤其有价值

## 评分
- 新颖性: ⭐⭐⭐⭐ IJEPA + 冻结 LDM 桥接自监督语义预测和条件纹理生成，组合方式新颖且动机清晰
- 实验充分度: ⭐⭐⭐ 单数据集 + 有限消融，但包含长程 rollout 定性分析和双编码器对比实验
- 写作质量: ⭐⭐⭐ 短论文格式简洁清晰，附录提供了完整的架构参数和训练配置
- 价值: ⭐⭐⭐⭐ 为遥感时序预测提供了结构-纹理解耦的新范式，adapter 设计和冻结大模型策略具有广泛的迁移价值
