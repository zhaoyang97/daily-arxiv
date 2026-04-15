# When Models Judge Themselves: Unsupervised Self-Evolution for Multimodal Reasoning

**日期**: 2026-03-22  
**arXiv**: [2603.21289](https://arxiv.org/abs/2603.21289)  
**代码**: [项目主页](https://dingwu1021.github.io/SelfJudge/)  
**领域**: 多模态/VLM  
**关键词**: self-evolution, MLLM, unsupervised, GRPO, self-consistency

## 一句话总结
提出 Actor-Judge 自进化框架——同一个 MLLM 既做推理(Actor)又做质量评估(Judge), 用 Self-Consistency 探索 + Judge 调制 + 能量归一化 GRPO 训练, 无需人工标注在数学视觉推理上提升 5.9%, 达到监督方法的同等水平。

## 研究背景与动机

1. **领域现状**: 多模态推理数据标注昂贵且稀缺。Self-play/Self-evolve 方法可以利用模型自身生成训练信号，但现有方法多依赖多数投票。

2. **现有痛点**: (a) 多数投票放大早期主导模式、抑制探索，导致模式坍缩；(b) 响应长度退化——训练过程中回答越来越短，质量下降；(c) 纯自洽性信号无法区分"一致但错误"的高频答案。

3. **核心 idea**: 用 Self-Consistency 保持探索多样性 + 用冻结的 Judge（自身副本）评估推理质量做调制 → 通过能量归一化避免绝对奖励不稳定 → 实现持续自我改进。

## 方法详解

### 整体框架
Actor 对每个输入采样 n 条推理轨迹 → Self-Consistency 计算频率奖励 $r_i^{SC} = \hat{p}(a_i)$ → 冻结 Judge 对每条轨迹评分 (答案正确性 + 推理质量 + 视觉 grounding) → 有界校准函数调制 SC 奖励 → GRPO 更新策略（能量归一化基线）。

### 关键设计

1. **Self-Consistency 频率奖励**:
    - 保留回答频率分布（而非二值化为对/错）
    - 高频答案获得更高初始奖励，但不是绝对——Judge 可以降权
    - 维持输出多样性，防止过早模式坍缩

2. **Judge 有界校准调制**:
    - 冻结的模型副本从三个维度评估: 答案正确性、推理质量、视觉 grounding
    - 有界校准函数 $g(s) = 1 + \lambda_+ \sigma((s-t_h)/\tau_h) - \lambda_- \sigma((t_l-s)/\tau_l)$
    - 上下界约束防止极端放大——保持训练稳定

3. **能量归一化 GRPO**:
    - 不用组内减均值归一化，而用 log-sum-exp 基线: $b(x) = \log \sum \exp(\tilde{r}_j)$
    - 隐式等价于对 reward-induced distribution 做 KL 散度匹配
    - 避免组内方差主导更新方向

## 实验关键数据

### 主实验

| 方法 | MathVision | 5-benchmark 均值 |
|------|-----------|-----------------|
| Baseline (Qwen2.5-VL) | 25.0% | 34.6% |
| MM-UPT (多数投票) | 27.5% | ~36% |
| Vision-R1 (监督) | 29.4% | — |
| **SelfJudge** | **30.9%** | **37.9%** |

### 消融实验

| 配置 | MathVision | 说明 |
|------|-----------|------|
| SC only | 25.2% | 几乎无改善 |
| Judge only | 27.3% | 不稳定, 长度坍缩 |
| SC + Judge (full) | **30.9%** | 两者互补 |

### 关键发现
- 无标注方法达到监督方法 (Vision-R1) 水平
- SC 和 Judge 缺一不可——SC 保证探索、Judge 保证质量
- 训练动态更健康: 熵轨迹平稳、长度坍缩减轻
- 跨模型规模有效 (2B-32B)

## 亮点与洞察
- **Self-Consistency × Self-Judge 互补设计**精巧: SC 防止收敛太快、Judge 防止收敛到错误方向
- **能量归一化**是重要技术贡献: 比标准 GRPO 归一化更稳定
- **无标注 ≈ 有监督**: 说明模型自身的推理评估能力已足够指导训练

## 局限性 / 可改进方向
- Judge 冻结不更新——随着 Actor 进步，Judge 的评估标准不会同步提高
- Pass@10 指标略有下降 (0.57→0.54)——可能存在轻微分布坍缩
- 仅在数学/逻辑推理上验证

## 相关工作与启发
- **vs MM-UPT (多数投票)**: MV +1.8% vs SelfJudge +4.9%——多数投票放大早期错误模式
- **vs Vision-R1 (监督)**: 36.0→38.4 (supervised) vs 34.6→37.9 (unsupervised)——差距仅 0.5%
- **vs EvoLMM**: SelfJudge 更高效 (1.4× cost vs 2.2×)，组 distributional modeling 更稳定

## 评分
- 新颖性: ⭐⭐⭐⭐ Actor-Judge 自判 + 能量归一化 GRPO 双创新
- 实验充分度: ⭐⭐⭐⭐ 5 benchmark + 7 模型 + 训练动态分析
- 写作质量: ⭐⭐⭐⭐ 理论推导（KL 散度等价证明）与实验验证结合
- 价值: ⭐⭐⭐⭐ 无标注自进化方向有持续价值，可推广到非数学领域
