# Safety-Potential Pruning for Enhancing Safety Prompts Against VLM Jailbreaking Without Retraining

**日期**: 2026-03-15  
**arXiv**: [2603.14219](https://arxiv.org/abs/2603.14219)  
**代码**: [Safety-Potential-Pruning](https://github.com/AngelAlita/Safety-Potential-Pruning)  
**领域**: 多模态VLM / AI安全  
**关键词**: VLM safety, jailbreak defense, pruning, safety subnetwork, activation analysis

## 一句话总结
提出 Safety Subnetwork Hypothesis——VLM 内部存在稀疏的安全子网络，safety prompt 会选择性激活深层参数。据此提出 Safety-Potential Pruning，一次性剪枝对 safety prompt 不响应的权重，无需重训地将攻击成功率降低最多 22%。

## 研究背景与动机

1. **领域现状**: VLM 面临越狱攻击威胁。Safety prompt 是一种轻量防御，但效果受限于模型内部结构对安全刺激的响应性。
2. **现有痛点**: Fine-tuning 防御昂贵且可能降低通用性能；Safety prompt 单独使用效果有限（~60% DSR）。标准 magnitude pruning 会不成比例地破坏安全关键神经元。
3. **核心发现**: 对比有/无 safety prompt 的激活分布，发现深层有稀疏参数子集对 safety prompt 强响应。这些参数构成"安全潜力子网络"。

## 方法详解

### Safety Subnetwork Hypothesis
- 安全行为不是均匀分布的，而是集中在稀疏的 latent subnetwork 中
- Safety prompt 选择性激活深层参数，浅层几乎不变

### Safety-Potential Pruning
1. **Sensitivity 计算**: $S_j = \|A_j^S\|_2^2 - \|A_j^{NS}\|_2^2$（safety vs no-safety 激活差）
2. **Weight importance**: $\text{Score}_{ij} = |W_{ij}| \cdot \sqrt{\max(S_j, 0)}$
3. **One-shot 剪枝**: 移除低分权重，无需重训

### 关键设计动机
- 剪枝不是为了压缩，而是为了"暴露和放大"安全子网络
- $\sqrt{S}$ 调节极端 outlier，保持相对差异

## 实验关键数据

### 主实验（DSR%，50% 稀疏度）

| 模型 | Method | FigStep | MM-SafetyBench | JailbreakV |
|------|--------|---------|----------------|------------|
| Qwen2-VL-7B | Vanilla+SP | 91.6 | 86.6 | — |
| Qwen2-VL-7B | **Ours** | **100.0** | 86.5 | — |
| LLaVA-V1.6 | Vanilla+SP | 82.0 | 91.5 | 60.4 |
| LLaVA-V1.6 | **Ours** (50%) | **89.2** | **92.0** | **69.3** |

### 关键发现
- 50% 稀疏度下仍能提升安全性——说明大量参数是"安全无关"的
- t-SNE 可视化显示剪枝后 S/NS 嵌入分离更清晰
- 相比 Wanda、SparseGPT 等通用剪枝，safety-guided 剪枝安全性提升更大

## 亮点与洞察
- **Safety Subnetwork Hypothesis**: 将剪枝从"压缩工具"重新定义为"结构性安全干预"，概念有深度
- **One-shot、无需重训**: 实际部署门槛极低
- **剪枝 ≠ 破坏安全**: 反直觉地，正确的剪枝反而增强安全

## 局限性 / 可改进方向
- 校准样本只用 128 张 HOD 图片，样本选择对结果的敏感性未分析
- 只验证了 7B 规模模型，更大模型行为可能不同
- 安全子网络的位置是否跨模型一致？

## 实验关键数据

### 主实验（DSR%，Safety + 各种剪枝方法）

| 模型 | 方法 | FigStep | MM-SafetyBench | JailbreakV | Avg |
|------|------|---------|----------------|------------|-----|
| LLaVA-V1.6-7B | Vanilla+SP | 82.0 | 91.5 | 60.4 | 78.0 |
| LLaVA-V1.6-7B | Wanda (20%) | 89.0 | 90.6 | 60.0 | 79.9 |
| LLaVA-V1.6-7B | **Ours (20%)** | **99.0** | **91.4** | **61.4** | **83.9** |
| LLaVA-V1.6-7B | Wanda (50%) | 57.2 | 82.2 | 71.8 | 70.4 |
| LLaVA-V1.6-7B | **Ours (50%)** | **89.2** | **92.0** | **69.3** | **83.5** |
| Qwen2-VL-7B | Vanilla+SP | 91.6 | 86.6 | 93.6 | 90.6 |
| Qwen2-VL-7B | Wanda (50%) | 77.2 | 95.8 | 96.4 | 89.8 |
| Qwen2-VL-7B | **Ours (50%)** | **100.0** | **99.4** | **98.2** | **99.2** |

### 消融: 不同规模模型

| 模型 | 方法 | FigStep | MM-SafetyBench | JailbreakV | Avg |
|------|------|---------|----------------|------------|-----|
| Qwen2-VL-2B | Vanilla+SP | 69.4 | 95.9 | 83.2 | 82.8 |
| Qwen2-VL-2B | **Ours (20%)** | 69.0 | 95.9 | 85.4 | **83.4** |
| LLaVA-V1.6-13B | Vanilla+SP | 99.2 | 100.0 | 63.9 | 86.6 |
| LLaVA-V1.6-13B | **Ours (50%)** | **100.0** | **98.7** | **83.6** | **94.1** |

### Utility 保持
- 20% 稀疏度下，各模型在 TextVQA/RealWorldQA/ScienceQA 上几乎无退化
- 50% 稀疏度下，Qwen2-VL 和 LLaVA 的 utility 与 Wanda 相当，但安全性远超
- MMMU/MM-Vet/POPE 复杂任务：20% 下影响可忽略，50% 下有轻微退化但安全性大幅提升

### 关键发现
- **50% 稀疏仍能提升安全性**: Qwen2-VL-7B 从 90.6% 提升到 99.2%——大量参数是"安全无关"的
- **t-SNE 可视化**: 剪枝后 Safety/No-Safety embedding 分离更清晰，安全子网络被有效暴露
- **较大模型收益更大**: 13B 模型 50% 剪枝后 DSR 从 86.6% 到 94.1%，2B 提升较小
- **架构影响**: LLaVA 在 FigStep 50% 时有退化 (99.0→89.2)，Qwen2-VL 反而提升 (92.4→100.0)——安全子网络的剪枝容忍度因架构而异

## 亮点与洞察
- **Safety Subnetwork Hypothesis 有理论深度**: 将剪枝从"压缩工具"重定义为"结构性安全干预"，用激活分析给出了实验支撑
- **One-shot、零重训**: 部署门槛极低，只需 128 校准图片 + 一次前向传播
- **反直觉: 正确剪枝增强安全**: 移除对安全提示不响应的权重 = 放大安全子网络的信号
- **嵌入空间验证**: t-SNE 显示剪枝是在表示层面增强了安全/非安全的区分

## 局限性 / 可改进方向
- 校准样本只用 128 张 HOD 图片，样本选择对结果的敏感性未充分分析
- 只验证了 2B-13B 模型，30B+ 模型安全子网络位置是否一致未知
- Safety prompt 选择对 sensitivity 有影响，最优 prompt 选择策略未探索
- 仅考虑图像 jailbreak，纯文本和多轮对话攻击待研究

## 相关工作与启发
- **vs LVLM-LP**: logit 级检测+替换，不改内部表示
- **vs CoCA**: decoding logit 调整，需推理时额外计算
- **vs Wanda**: 通用剪枝，safety 提升不一致——说明 safety-aware metric 的必要性

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ Safety Subnetwork Hypothesis 和 pruning-for-safety 的视角非常新颖
- 实验充分度: ⭐⭐⭐⭐ 3 模型 × 3 benchmark × 2 稀疏度 + utility + t-SNE
- 写作质量: ⭐⭐⭐⭐ 假说→验证→方法的逻辑链完整
- 价值: ⭐⭐⭐⭐⭐ 零成本安全增强，部署价值极高
