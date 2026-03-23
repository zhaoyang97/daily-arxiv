# Sat-JEPA-Diff: Bridging Self-Supervised Learning and Generative Diffusion for Remote Sensing

**日期**: 2026-03-14  
**arXiv**: [2603.13943](https://arxiv.org/abs/2603.13943)  
**代码**: 有（GitHub）  
**领域**: 图像生成 / 遥感时序预测  
**关键词**: satellite forecasting, IJEPA, latent diffusion, self-supervised learning, Sentinel-2

## 一句话总结
提出 Sat-JEPA-Diff，用 IJEPA 在 latent 空间预测未来帧的语义表示，再通过轻量 cross-attention adapter 引导冻结的 Stable Diffusion 3.5 生成高保真卫星图像，在 GSSIM（边缘保持）上比确定性方法提升 11%+，FID 达 0.1475。

## 研究背景与动机

1. **领域现状**: 卫星时序预测（t→t+1）是遥感监测的关键任务。确定性方法（PredRNN、SimVP）优化像素级 MSE 但产生模糊输出（均值回归）；生成模型（DDPM/LDM）纹理逼真但缺乏语义引导会"幻觉"出错误结构。

2. **现有痛点**: 确定性方法高 PSNR/SSIM 但边缘模糊（低 GSSIM）；纯生成方法可能生成不存在的道路/建筑。需要兼顾结构准确性和纹理真实性。

3. **核心 idea**: 用 IJEPA 在 latent 空间做语义级预测（结构准确），用预测的语义表示引导冻结的 LDM 做纹理生成（细节逼真），实现结构-纹理的桥接。

## 方法详解

### 整体框架
两阶段：(1) IJEPA 时序预测器：编码当前帧 $I_t$ 为语义嵌入 $z_t$，预测器 $P_\phi$ 预测 $\hat{z}_{t+1}$；(2) 条件扩散生成器：预测的语义嵌入 + 低分辨率空间结构（32×32 降采样）通过 cross-attention adapter 引导冻结的 SD 3.5 生成 $\hat{I}_{t+1}$。

### 关键设计

1. **IJEPA 时序预测**: ViT 编码器提取 patch 嵌入，transformer 预测器预测未来帧嵌入。用 EMA 目标编码器提供稳定目标。损失函数结合 L1 + cosine + 空间方差匹配（防空间坍塌）+ InfoNCE 对比损失。

2. **Conditioning Adapter**: 轻量模块将 IJEPA 嵌入转换为 cross-attention 条件信号（token 级 h + 全局 p），通过可学习融合门 α 平衡语义信号和粗空间结构信号。

3. **Flow Matching + LoRA**: 冻结 SD 3.5 核心，只训练 adapter 和 LoRA。用 rectified flow 的速度预测公式训练。

## 实验关键数据

| 模型 | PSNR↑ | SSIM↑ | GSSIM↑ | FID↓ |
|------|-------|-------|--------|------|
| PredRNN | 38.38 | 0.9476 | 0.7836 | 9.972 |
| SimVP | 37.63 | 0.9391 | 0.7719 | 18.72 |
| SD 3.5 | 32.98 | 0.8398 | 0.8711 | 0.153 |
| **Sat-JEPA-Diff** | **33.81** | **0.8672** | **0.8984** | **0.1475** |

### 关键发现
- GSSIM 0.8984（边缘+结构保持），比最佳 baseline 高 11%+，说明语义引导有效防止模糊
- 确定性方法 PSNR/SSIM 高但 FID 极差（>9），说明像素级指标无法反映生成质量
- 换用 Panopticon 编码器结果相近，证明方法对编码器选择不敏感

## 亮点与洞察
- **IJEPA 做时序预测**而非像素重建是关键设计 — 在抽象语义空间预测比像素空间更鲁棒，天然回避了传感器噪声和大气干扰
- **冻结 SD + 轻量 adapter** 的范式保留了预训练生成先验，训练成本极低

## 局限性 / 可改进方向
- PSNR/SSIM 低于确定性方法（33.81 vs 38.38），存在感知-失真 trade-off
- 仅做 t→t+1 单步预测，长horizon自回归稳定性受限
- 缺少下游任务（变化检测、分类等）的评估

## 评分
- 新颖性: ⭐⭐⭐⭐ IJEPA+LDM 桥接自监督预测和生成是新颖组合
- 实验充分度: ⭐⭐⭐ 单数据集实验，定量指标较简单
- 写作质量: ⭐⭐⭐ 短论文格式，简洁但缺少细节
- 价值: ⭐⭐⭐ 为遥感时序预测提供了新范式
