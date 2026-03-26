# PEPO: Rethinking Token-Level Policy Optimization for Multimodal Chain-of-Thought

**日期**: 2026-03-24  
**arXiv**: [2603.22847](https://arxiv.org/abs/2603.22847)  
**代码**: 无  
**领域**: 多模态/VLM / LLM推理 / 强化学习  
**关键词**: multimodal CoT, token-level optimization, visual grounding, GRPO, perception prior

## 一句话总结
提出 PEPO（Perception-Exploration Policy Optimization），通过 token 级视觉感知先验（隐状态与视觉 token 的余弦相似度）和熵引导探索信号的自适应融合，重新加权 GRPO 策略梯度，在几何/视觉推理/视觉定位等任务上比标准 GRPO 提升 +3.67%，首次揭示多模态 CoT 中视觉锚定和推理探索的互补角色。

## 研究背景与动机

1. **领域现状**: RLVR（Reinforcement Learning from Verifiable Rewards）方法如 GRPO 在 LLM 推理上很成功，但应用于多模态 CoT 时，序列级均匀监督忽略了不同 token 在视觉锚定程度上的差异。

2. **现有痛点**: 对于多模态任务，某些 token 强依赖视觉输入（感知 token），某些则涉及逻辑推理和自我纠错（探索 token），均匀加权导致优化失衡。

3. **核心 idea**: 从隐状态相似度中提取免标注的视觉锚定度先验，与 token 级熵融合构建 token 级 advantage 权重。

## 方法详解

### 整体框架
在 GRPO/DAPO 的序列级 advantage 基础上引入 token 级权重调制：对每个 response token 计算视觉相似度（感知先验）和熵（探索信号），通过自适应门控融合为 token 级 advantage 权重。线性逼近计划从序列级均匀权重平滑过渡到 token 级差异化权重。

### 关键设计

1. **视觉相似度（感知先验）**:
   - $\text{VS}_t=\frac{1}{L}\sum_{l=1}^{L}\frac{1}{N}\sum_{n=1}^{N}\frac{\langle h_{l,t}, v_{l,n}\rangle}{\|h_{l,t}\|\|v_{l,n}\|}$
   - 跨所有层、所有 vision token 的余弦相似度均值
   - 高 VS token 是"看图说话"型——移除图像后隐状态偏移 2-3 倍大
   - 无需标注，直接从模型隐状态中提取

2. **熵引导探索信号**:
   - $H_t=-\sum_{x\in\mathcal{V}} p_\theta(x|s_t)\log p_\theta(x|s_t)$
   - 高熵 token 通常是推理转折点（"但是""因此""检查"等）
   - 仅用熵做 RL 在视觉定位任务上崩溃，说明感知先验是必要的

3. **感知-探索融合门控**:
   - 均值中心化得分：$g_t=\hat{\text{VS}}_t+\hat{H}_t-\text{mean}_t(\hat{\text{VS}}+\hat{H})$
   - 权重：$w_t=T\cdot\text{Softmax}((1+\alpha\tanh(g_t))\cdot\text{VS}_t)$
   - 门控乘以 VS 保持感知主导（α=0.05 最优）
   - Token 级 advantage：$A_t^{(i)}=[(1-\lambda)+\lambda w_t^{(i)}]A^{(i)}$
   - λ 从 0→1 线性 schedule，避免早期训练不稳定

4. **即插即用**: 无缝集成到 GRPO（PEPOG 变体）和 DAPO（PEPOD 变体），计算开销 <1%

## 实验关键数据

### 几何推理 (Qwen2.5-VL-3B)

| 方法 | Geo3K val | Geo3K test | MathVista | MathVerse | 平均 |
|------|----------|-----------|-----------|-----------|------|
| GRPO | - | - | - | - | 32.64 |
| **PEPOG** | 21.91 | 27.27 | **54.45** | **45.42** | **36.70** |

InternVL3-2B 上 PEPOD vs DAPO: 37.66 vs 32.51（+5.15）

### 视觉定位 (RefCOCO, IoU@50)

| 方法 | val | testA | testB | 跨域均值 |
|------|-----|-------|-------|---------|
| GRPO | - | - | - | 62.42 |
| **PEPOG** | **90.44** | **92.40** | **85.75** | **65.26** |

### 细粒度分类 (FGVC Aircraft)

| 方法 | 1-shot | 4-shot | 平均 |
|------|--------|--------|------|
| GRPO | - | - | 56.09 |
| **PEPOG** | 51.13 | **75.79** | **61.41** |

### 消融实验

| 组件 | Geo3K val | 说明 |
|------|----------|------|
| GRPO baseline | 19.00 | 基准 |
| 仅探索（熵） | 20.18 | +1.18 |
| 仅感知（VS, α=0） | 21.07 | +2.07 |
| **完整 PEPO** | **22.80** | **+3.80** |

- 去 schedule（λ=1 固定）: 19.80，说明渐进加权重要
- 加法融合（无门控）: 20.99，门控比加法好 1.8 分
- 浅层 (1-10) vs 全层: 18.92 vs 22.80，所有层都有贡献

## 亮点与洞察
- **首次量化多模态推理中视觉锚定和探索的互补角色**——感知和探索编码不同模式，联合优于任一单独使用
- **免标注感知先验**通过隐状态相似度获得，优雅且通用
- 可直接应用到任何 GRPO/DAPO pipeline，开销极小（<1%），工程实用性强
- SuperClevr Counting 上 +14.94 的最大增益显示 PEPO 对高度视觉依赖的任务帮助最大
- 仅熵优化在视觉定位上崩溃——确认了多模态 RL 中视觉锚定不可或缺

## 局限性 / 可改进方向
- 仅在 2B-3B 模型验证，7B+ 效果未知（GPU/显存限制）
- 感知参数（α, λ schedule）需要验证集调优，非完全自适应
- 未在视频理解、工具增强推理等更广泛任务上测试
- 高熵 baseline 不稳定使得纯探索对比受限

## 评分
- 新颖性: ⭐⭐⭐⭐ 首次在 token 级分析多模态 RL 的感知-探索互补
- 实验充分度: ⭐⭐⭐⭐ 多任务多模型 + token 级分析 + 系统消融
- 写作质量: ⭐⭐⭐⭐ 分析深入，可视化有说服力
- 价值: ⭐⭐⭐⭐ 对多模态 RL 训练有实用指导意义
