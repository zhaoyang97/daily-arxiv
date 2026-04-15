# LatSearch: Latent Reward-Guided Search for Faster Inference-Time Scaling in Video Diffusion

**日期**: 2026-03-15  
**arXiv**: [2603.14526](https://arxiv.org/abs/2603.14526)  
**代码**: [LatSearch](https://zengqunzhao.github.io/LatSearch)  
**领域**: 视频理解 / 图像生成  
**关键词**: inference-time scaling, video diffusion, latent reward model, search, Wan2.1

## 一句话总结
提出 LatSearch，在视频扩散推理过程中用 latent reward model 对中间去噪状态打分，配合 Reward-Guided Resampling and Pruning (RGRP) 策略进行搜索，在 VBench-2.0 上比 baseline 提升 3.35% 质量的同时仅需 2.13× 推理时间（相比 EvoSearch 的 10.15× 快近 5 倍）。

## 研究背景与动机

1. **领域现状**: LLM 的 inference-time scaling 成功经验正被迁移到视频扩散模型。已有工作发现存在"golden noise"——特定初始噪声能显著提升视频质量，由此催生了 Best-of-N、beam search、进化搜索等方法。

2. **现有痛点**: 现有 noise search 方法只能在完全解码后的视频上用 reward model 评估质量，导致三个问题：(a) 必须完整解码视频才能反馈，计算代价极高；(b) reward 信号严重延迟和稀疏；(c) 早期引入的错误在长去噪轨迹中不断累积。Noise optimization 方法虽成本低，但一旦轨迹开始就失去纠正能力。

3. **核心矛盾**: 更强的搜索算法能带来更好的质量/可控性，但现有 reward 评估方式让强搜索在计算上不可行。关键缺失是**对中间 latent 的可靠评估能力**。

4. **切入角度**: 能否不等到视频解码完成，直接在 latent space 对 partially denoised 状态打分？如果可以，就能实现 process-level supervision，早期剪枝坏候选，大幅降低搜索成本。

5. **核心 idea**: 训练一个 latent reward model 对任意时间步的去噪 latent 打分（视觉质量 VQ + 运动质量 MQ + 文本对齐 TA），然后用 RGRP 策略在去噪过程中概率性重采样+剪枝。

## 方法详解

### 整体框架

输入文本 prompt → Wan2.1 视频扩散模型 → 生成 N 个初始噪声候选 → 在去噪过程的指定时间步，用 latent reward model 给每个候选打分 → 按分数概率重采样（RGRP）→ 最终步按累计 reward 剪枝到 1 个 → 解码为视频。

### 关键设计

1. **Latent Reward Model**:
    - 做什么：对任意时间步 $t$ 的中间去噪 latent $\mathbf{z}_t$ 打分，输出 VQ/MQ/TA 三个维度分数
    - 核心思路：backbone 用 Qwen2-VL-3B，latent 经 3D 卷积 patchify 成 token，结合时间步 embedding 和 prompt token，通过 [VQ]/[MQ]/[TA] query token 回归分数。训练数据通过 cosine similarity credit assignment 构造——$\tilde{\mathbf{r}}_t = s_t \cdot \mathbf{r}$，其中 $s_t$ 是中间 latent 与最终 clean latent 的余弦相似度
    - 训练目标：regression loss（绝对值监督）+ preference loss（RLHF 风格的 pairwise 排序，确保相对序正确）
    - 设计动机：中间 latent 没有显式语义，直接标注不可行；通过相似度加权将视频级 reward 分配到每个时间步，是一种巧妙的弱监督策略

2. **Reward-Guided Resampling and Pruning (RGRP)**:
    - 做什么：在去噪轨迹中用 reward 信号引导候选筛选
    - 核心思路：在 scoring 时间步（如 t=10,15,20），将 reward 转为 softmax 权重 $\pi_i^{(t)} = \frac{\exp(\tau r_i^{(t)})}{\sum_k \exp(\tau r_k^{(t)})}$，按此概率多项式重采样 N 个，去重保留唯一 seed（避免计算浪费）。最终步按累计 reward 选最佳
    - 设计动机：相比 beam search 的贪心选择，概率采样更鲁棒——reward model 不完美，hard selection 容易 overfit reward 噪声；uniqueness pruning 保证多样性同时减少冗余计算
    - 与 beam search 的区别：beam search 纯按累计分数截断 → 过度依赖 reward → Table 4 显示 RGRP 平均比 beam search 高 0.42%

3. **Candidate Generation**:
    - 做什么：生成 N 个多样初始噪声
    - 核心思路：对基础噪声 $\mathbf{z}_T^{(0)}$ 加 $\eta$ 控制的扰动：$\mathbf{z}_T^{(i)} = \sqrt{1-\eta^2} \mathbf{z}_T^{(0)} + \eta \epsilon_i$
    - 设计动机：$\eta$ 控制候选多样性，太大失去原始噪声信息，太小候选太相似

### 训练策略
- Latent reward dataset：1000 prompts × 5 seeds = 5000 视频，存储各时间步 latent + similarity + video reward
- 两阶段学习率：1e-4 → 1e-5（第 10 epoch）
- Regression + preference 权重各 1.0

## 实验关键数据

### 主实验（VBench-2.0）

| 方法 | Average | Inference Time | 速度倍率 |
|------|---------|---------------|---------|
| Baseline (Wan2.1) | 51.90 | 77.21s | 1× |
| FreeInit | 49.82 (-2.08) | 308.87s | 4.00× |
| FreqPrior | 50.37 (-1.53) | 142.46s | 1.85× |
| VideoReward | 52.80 (+0.90) | 283.63s | 3.67× |
| EvoSearch | 55.01 (+3.11) | 783.76s | 10.15× |
| **LatSearch** | **55.25 (+3.35)** | 164.41s | **2.13×** |

### 消融实验

| 配置 | Average | 说明 |
|------|---------|------|
| Full (RGRP + PL) | 53.84 | 完整模型 |
| w/o Preference Loss | 53.42 (-0.42) | 去掉 PL 排序退步 |
| w/o RGRP (beam search) | 52.35 (-1.49) | 贪心搜索严重退步 |
| N=4 | 52.81 | 候选少但仍有效 |
| N=6 | 53.84 | 性价比最佳 |
| N=8 | 54.13 | 略好但边际递减 |
| Cosine similarity credit | 53.84 | 最佳 credit 策略 |
| Uniform credit | 52.31 | 均匀分配效果差 |

### 关键发现
- Noise optimization 方法（FreeInit、FreqPrior）反而比 baseline 差，说明不看中间状态盲目优化噪声不靠谱
- RGRP 的概率采样比 beam search 好 1.49%，验证了"不要过度信任不完美的 reward model"
- Cosine similarity credit assignment 显著优于 uniform/exponential，说明中间 latent 和最终结果的相似度是好的信号
- 从 Wan2.1-1.3B 到 14B backbone 都有效，方法是 model-agnostic 的

## 亮点与洞察
- **Latent-level reward model** 是核心创新：打破了"只能评估最终视频"的限制，让 process-level supervision 成为可能。可迁移到所有扩散模型的推理加速场景
- **Cosine similarity credit assignment** 巧妙：不需要人工标注中间 latent 的质量，利用几何距离作为代理指标，简单有效
- **概率重采样 + uniqueness pruning** 的组合很优雅：既避免 hard selection 的 reward hacking，又通过去重节省计算

## 局限性 / 可改进方向
- Reward model 基于 Qwen2-VL-3B，本身需要训练和推理开销，对更长/更高分辨率视频的扩展性待验证
- 只在 VBench-2.0 上评估，缺少用户偏好 (human evaluation) 的大规模验证
- Credit assignment 仍是启发式的——cosine similarity 假设中间 latent 与最终结果的几何距离和质量正相关，对某些问题可能不成立
- 搜索 schedule（哪些时间步打分）是手工设定的（t=10,15,20），自适应 schedule 可能更优

## 相关工作与启发
- **vs EvoSearch**: 进化搜索质量相当但慢 5 倍，因为需要反复解码完整视频做评估
- **vs VideoReward (Best-of-N)**: 只评估最终视频，+0.90 小于 LatSearch 的 +3.35
- **vs FreeInit/FreqPrior**: 这两个 noise optimization 方法不用中间监督，效果反而低于 baseline

## 评分
- 新颖性: ⭐⭐⭐⭐ latent-level reward model + RGRP 的组合有新意，但 SMC/importance sampling 在 LLM 推理中已有类似思路
- 实验充分度: ⭐⭐⭐⭐ VBench-2.0 全面评估 + 丰富消融，但缺少 human study
- 写作质量: ⭐⭐⭐⭐⭐ 公式清晰，motivation 逻辑链完整
- 价值: ⭐⭐⭐⭐ 推理时间缩减到 2× 的同时匹配 10× 方法的质量，实用价值高
