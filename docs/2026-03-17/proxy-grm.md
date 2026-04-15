# Proxy-GRM: Learning Transferable Rubrics via Proxy-Guided Critique for VLM Reward Models

**日期**: 2026-03-17  
**arXiv**: [2603.16600](https://arxiv.org/abs/2603.16600)  
**代码**: [GitHub](https://github.com/Qwen-Applications/Proxy-GRM)  
**领域**: 多模态/VLM / LLM对齐  
**关键词**: 生成式奖励模型, 评估准则可迁移性, 代理验证, GRPO, VLM评估

## 一句话总结
提出 Proxy-GRM，通过训练独立的代理评估器验证生成式奖励模型（GRM）产生的评估准则（rubric）的可迁移性，将该验证信号作为 RL 奖励闭环优化 rubric 质量，仅用 ~50K 数据在三个 VLM 奖励基准上达到 SOTA。

## 研究背景与动机

1. **领域现状**: 生成式奖励模型（GRM）通过三阶段流水线评估 VLM 输出：生成评估准则（rubric）→ 逐条打分 → 最终判断。这比标量奖励模型更可解释。

2. **现有痛点**: 整个流水线的可靠性取决于第一步 rubric 的质量，但现有方法只优化最终答案——rubric 完全无监督。模型可能学会"先决定答案再编造理由"（post-hoc rationalization），产生的 rubric 无法迁移给其他评估者使用。

3. **核心矛盾**: 需要验证 rubric 质量，但 LLM-as-Judge 方式计算昂贵且不可微分，无法接入训练循环。

4. **切入角度**: 定义"rubric 可迁移性"——如果一个独立的评估者仅凭 rubric 就能做出正确的偏好判断，说明 rubric 编码了充分且无偏的信息。

5. **核心 idea**: 训练冻结的代理评估器（Proxy Agent），用其预测准确率作为 rubric 质量的奖励信号，闭环接入 GRPO 训练。

## 方法详解

### 整体框架

1. **数据蒸馏**: 合并多个 VLM 偏好数据集 → 过滤得到 ~60K 样本
2. **代理训练**: 训练 Proxy-SFT（从正确蒸馏样本 SFT）和 Proxy-RL（在 SFT 基础上再 RL）
3. **策略训练**: Cold-start SFT → GRPO with 三重奖励（准确性 + 代理验证 + 格式）
4. **推理**: 标准模式直接出答案 / 代理验证模式双重检查

### 关键设计

1. **Rubric 可迁移性的形式化**:
    - 做什么：定义什么是"好的 rubric"
    - 核心思路：$\text{Transferability}(\mathcal{R}) = \mathbf{1}[\phi(q, \mathcal{I}, r_1, r_2, \mathcal{R}) = \mathcal{A}^*]$，即独立代理 $\phi$ 仅凭 rubric 能否做出正确偏好判断
    - 设计动机：这是一个可计算的二元信号，可以直接作为 RL 奖励——解决了 LLM-as-Judge 不可微分的问题

2. **代理评估器训练（Proxy Agent）**:
    - 做什么：训练一个专门**消费** rubric（而非生成 rubric）的独立模型
    - 核心思路：Proxy-SFT 在 55K 正确样本上 SFT 训练，输入 $(q, \mathcal{I}, r_1, r_2, \mathcal{R})$，输出评估 + 判断。Proxy-RL 在 SFT 基础上用准确率 RL 继续训练
    - **关键发现**：Proxy-SFT 意外地比 Proxy-RL 表现更好。RL 训练的代理可能产生内部不一致的评估过程——用有缺陷的推理得到正确答案——这种不一致使其作为 rubric 验证器时给出噪声信号

3. **三重奖励 GRPO 训练**:
    - 做什么：闭环优化策略模型的 rubric 质量
    - 核心思路：$r = r_{\text{acc}} + r_{\text{proxy}} + 0.5 \cdot r_{\text{format}}$
     - $r_{\text{acc}}$: 最终判断是否正确 (±1)
     - $r_{\text{proxy}}$: 冻结代理能否用 rubric 做出正确判断 (±1)
     - $r_{\text{format}}$: 输出格式是否规范 (0/1)
   - 设计动机：$r_{\text{acc}}$ 保证最终答案正确，$r_{\text{proxy}}$ 保证 rubric 有真正的信息量而非 post-hoc rationalization。代理冻结防止共适应。

### 训练细节
- 基座模型：Qwen2.5-VL-7B-Instruct
- 教师模型：Qwen3-VL-235B-A22B（蒸馏用）
- SFT lr=1e-5, RL lr=5e-6, GRPO group size=7
- 总数据量 ~50K（比竞品少 4×）

## 实验关键数据

### 三基准主实验

| 方法 | 数据量 | VL-RewardBench | MM Reward Bench | MM-RLHF-RB |
|------|--------|---------------|-----------------|------------|
| **Proxy-GRM** | 50K | **75.22** | **85.62** | **82.94** |
| Unified-Reward-Think | 200K+ | 73.80 | 84.40 | 81.18 |
| R1-Reward | 200K+ | 71.92 | 82.20 | 80.59 |
| GPT-4o | - | 65.40 | 70.80 | 73.93 |
| Claude-3.7-Sonnet | - | 70.70 | 71.90 | 82.43 |

用 4× 少的数据超越所有开源和闭源方法。

### 代理选择消融

| 代理类型 | VL-RewardBench | 平均分 |
|----------|---------------|--------|
| Proxy-SFT | **75.22** | **81.26** |
| Proxy-RL | 73.38 | 79.97 |
| Unified-Reward-SFT | 74.98 | 81.18 |
| Unified-Reward-Think (RL) | 73.14 | 79.77 |
| Qwen2.5-VL-32B | 74.02 | 80.25 |
| Qwen2.5-VL-3B | 72.25 | 77.87 |

**SFT 代理全面优于 RL 代理**——包括外部模型（Unified-Reward-SFT > Think）也验证了这一规律。

### 关键发现
- **SFT > RL 作为代理**：RL 模型可能用错误推理得到正确答案（结果正确但过程不一致），作为验证器时产生噪声信号
- **数据效率极高**：50K 样本 > 200K+ 样本的竞品，proxy 信号比简单增加数据更有效
- **Rubric 可迁移**：生成的 rubric 传给未见过的评估者（如 Qwen2.5-VL-32B）仍能提升准确率

## 亮点与洞察

- **Rubric 可迁移性作为优化目标**：将模糊的"rubric 质量"转化为可计算的二元信号（代理能否用它做对判断），既有理论优雅又有实践价值。
- **SFT > RL 作为验证器的发现**：揭示了 outcome-only RL 的深层问题——结果对了但过程可能是乱来的。这对 reward model 训练有广泛启示：不是所有 RL trained 模型都适合做评估者。
- **4× 数据效率**：说明信号质量 > 数据数量。Proxy 奖励提供了比简单扩大数据更精准的学习信号。

## 局限性 / 可改进方向

- **代理和策略用同一基座**：Proxy-SFT 和 Proxy-GRM 都基于 Qwen2.5-VL-7B，能力上限一致，更大的代理是否更好？
- **Rubric 格式固定**：XML tag 格式的 rubric 是否是最优表示？自由文本 critique 可能更灵活
- **只管 rubric 不管 eval**：当前只优化 rubric 生成，eval 阶段同样可能存在 rationalization

## 相关工作与启发

- **vs R1-Reward**: R1-Reward 用 RL 训练但无 proxy 验证，rubric 质量不可控。Proxy-GRM 用 proxy 闭环验证，+3.3pp
- **vs Unified-Reward-Think**: 也用 RL 训练奖励模型，但数据量是 Proxy-GRM 的 4×。说明 proxy 信号 > 更多数据
- **启发**：这个"独立验证者"模式可以推广——任何 CoT 推理模型都可以用一个独立 agent 验证中间推理步骤的可迁移性

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ Rubric 可迁移性 + proxy 闭环验证是全新范式，SFT>RL 发现有深度
- 实验充分度: ⭐⭐⭐⭐⭐ 三基准 + 代理选择消融 + 奖励配置消融 + 可迁移性验证
- 写作质量: ⭐⭐⭐⭐ 结构清晰，形式化定义严谨
- 价值: ⭐⭐⭐⭐⭐ 对 reward model 和 RLHF 社区有重要启示，代码开源
