# Scaling Test-Time Robustness of Vision-Language Models via Self-Critical Inference Framework

**日期**: 2026-03-08  
**arXiv**: [2603.07659](https://arxiv.org/abs/2603.07659)  
**代码**: [GitHub](https://github.com/KaihuaTang/Self-Critical-Inference-Framework)  
**领域**: 多模态/VLM  
**关键词**: LVLM robustness, counterfactual inference, language bias, language sensitivity, test-time scaling

## 一句话总结
提出 Self-Critical Inference（SCI）框架，通过多轮文本和视觉反事实推理统一解决 LVLM 的语言偏差和语言敏感性问题，同时提出模型自适应的 DRBench 动态鲁棒性评估基准，证明增加反事实推理轮数可持续提升鲁棒性。

## 研究背景与动机

1. **领域现状**: LVLM 将视觉编码器与预训练 LLM 结合，在 VQA 等任务上表现优秀，但继承了 LLM 的语言偏差（幻觉）和语言敏感性（prompt 微变导致输出改变）问题。

2. **现有痛点**: (a) VCD 等方法仅针对视觉幻觉（语言偏差），忽略了语言敏感性；(b) 固定鲁棒性 benchmark 不能捕捉不同模型的真实脆弱样本——不同 LVLM 的非鲁棒样本仅有 ~7% 重叠；(c) VCD 使用单次反事实推理，改进空间有限。

3. **核心 idea**: 将 VCD 解构为 TIE logit 的重加权，在此基础上扩展为文本+视觉双通道多轮反事实推理，建立测试时鲁棒性的 scaling law。

## 方法详解

### 整体框架
SCI = 文本反事实（TC）+ 视觉反事实（VC），通过 $p_{SCI}(y) \propto \exp(TC/\tau_1) \cdot \exp(VC/\tau_2)$ 融合为统一的解码分布。

### 关键设计

1. **VCD 的因果解读**:
    - 揭示 VCD 本质是 TIE logit 重加权：$p(y) \propto \exp(Z(v,q)) \cdot \exp(TIE/\tau)$
    - $\alpha = 1/\tau$ 是温度参数，不是简单的权重
    - 这一洞察统一了 VCD 和 CF-VQA 的框架

2. **文本反事实（TC）**:
    - 对原始 prompt 生成 N 个语义等价但词汇不同的变体
    - $TC_k = \max_i(Z_k(v^0, q^i))$，取所有变体中 logit 的逐元素最大值
    - 确保一致性：对不同 prompt 给出相同答案

3. **视觉反事实（VC）**:
    - 生成 M 个去除内容的假图像的视觉 token
    - $VC = Z(v^0, q^0) - \mathbb{E}[Z(v^j, q^0)]$
    - 多个 dummy 图像取平均提供更稳定的偏差估计

4. **DRBench 动态基准**:
    - Bias Subset：原始和 dummy 图像都给错误答案的样本（依赖语言先验）
    - Sensitivity Subset：prompt 微变后答案改变的样本
    - 模型自适应构建，避免固定 benchmark 的过拟合问题

### 配置
SCI3 (M=N=1), SCI5 (M=N=2), SCI7 (M=N=3)，轮数增加 → 鲁棒性持续提升。

## 实验关键数据

### 主实验（DRBench BS Subset）

| 方法 | LLaVA-NeXT Overall | Qwen2-VL Overall |
|------|-------------------|-----------------|
| Baseline | 18.75% | — |
| TIE | 27.31% | — |
| VCD | 27.89% | — |
| SCI3 | 优于 VCD | — |
| SCI5 | 进一步提升 | — |
| SCI7 | **最优** | — |

### 消融实验

| 配置 | 效果 |
|------|------|
| 仅 TC | 改善敏感性但不改善偏差 |
| 仅 VC (=VCD) | 改善偏差但不改善敏感性 |
| TC + VC (SCI) | 同时改善两者 |
| 增加轮数 SCI3→5→7 | 鲁棒性持续提升 |

### 关键发现
- 不同 LVLM 的非鲁棒样本重叠极少（24.68% 中仅 7.34% 共享）→ 固定 benchmark 不可靠
- Qwen2-VL 比 LLaVA-NeXT 整体更鲁棒，但偏差问题更严重
- SCI 在标准 benchmark 上也有改善，不仅限于鲁棒性子集
- 测试时鲁棒性可以通过增加推理轮数 scale

## 亮点与洞察
- **VCD 的因果理论统一**: 将 VCD、TIE、CF-VQA 纳入统一框架，理论贡献清晰
- **测试时鲁棒性 scaling 是新方向**: 不同于增加 CoT 长度的 scaling，增加反事实轮数是正交维度
- **DRBench 设计理念**: 模型自适应 benchmark 防止过拟合，可应用于任何 LVLM 评估

## 局限性 / 可改进方向
- 推理成本随轮数线性增长（SCI7 = 7 倍推理时间）
- 反事实 prompt 生成依赖模板，质量有限
- 仅在 7B/8B 模型上验证，更大模型的鲁棒性 scaling 效果未知

## 相关工作与启发
- **vs VCD**: SCI 是 VCD 的严格泛化——VCD = SCI 的 M=1, N=0 特例
- **vs M3ID**: 同样基于 VCD 思路但 M3ID 用位置相关的 τ，SCI 用多轮推理
- **vs test-time scaling**: 传统 scaling 增加 token 长度，SCI 增加推理轮数

## 评分
- 新颖性: ⭐⭐⭐⭐ 因果理论统一 + 鲁棒性 scaling 新方向
- 实验充分度: ⭐⭐⭐⭐ 多模型 + 6 个 benchmark + 详细消融
- 写作质量: ⭐⭐⭐⭐ 理论推导严谨，动机清晰
- 价值: ⭐⭐⭐⭐ 对 LVLM 鲁棒部署有实际意义
