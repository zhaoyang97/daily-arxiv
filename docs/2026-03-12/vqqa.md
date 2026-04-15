# VQQA: An Agentic Approach for Video Evaluation and Quality Improvement

**日期**: 2026-03-12  
**arXiv**: [2603.12310](https://arxiv.org/abs/2603.12310)  
**代码**: 无  
**领域**: 视频理解 / 视频生成评估  
**关键词**: video evaluation, agentic, prompt refinement, VLM, closed-loop

## 一句话总结
提出 VQQA，一个多 Agent 视频评估与质量改进框架——通过三个 Agent（问题生成→视频问答→提示优化）构建闭环，将 VLM 的评估反馈作为"语义梯度"驱动 prompt 迭代优化，无需模型微调，在 T2V-CompBench 上对 CogVideoX-5B 提升 +11.57%（41.89%→53.46%），VBench2 上 +8.43%（41.98%→50.41%）。

## 研究背景与动机

1. **评估与生成脱节**: 现有视频生成评估（FVD、VQAScore 等）都是被动打分，评估结果无法回馈到生成过程中改进质量。
2. **测试时优化受限**: 已有方法要么计算开销巨大（VISTA 的 pairwise tournament），要么需要白盒模型内部访问（Video-TTT 的梯度更新）。
3. **核心思路**: 将评估从被动 benchmark 转化为主动闭环反馈——评估→定位缺陷→优化 prompt→重新生成，全程通过黑盒自然语言接口完成。

## 方法详解

### 三 Agent 协作架构

整个框架将视频评估形式化为离散文本优化问题：将 prompt 视为优化变量，VLM 反馈视为语义梯度。

1. **Question Generation (QG) Agent**: 分析视频 v、prompt p 和条件 C，沿三个维度动态生成视觉问题集 Q：
    - Video-Prompt Alignment：视频是否忠实表达了 prompt 的语义？
    - Visual Quality：是否存在视觉伪影、时序不一致？
    - Condition Fidelity：是否保持参考图像的身份和语义细节？（I2V 时激活）
2. **Question Answering (QA) Agent**: 用 VLM 对每个问题评分，低分问题精确指向具体缺陷（如物体数量错误、空间关系混乱、动作不连贯等）。
3. **Prompt Refinement Agent**: 将低分 QA 对中的批评信息作为"语义梯度"（借鉴 TextGrad 思想），针对性修改 prompt 措辞以修复已识别的缺陷，而非重写整个 prompt。

### 关键机制

- **Global Selection**: 用 VLM 将每轮候选视频与**初始 prompt**（非优化后的 prompt）做整体对齐评分，防止局部优化导致语义漂移。消融实验证实去掉 Global Selection 后平均分下降 1.02%；用 QA 平均分替代则下降 1.86%。
- **Dynamic Stopping**: 当全局最高分在耐心窗口 k 步内改进低于阈值 ε 时自动停止。k=3 时平均 3.80–4.22 步收敛，4 步即捕获绝大部分收益。
- **任务无关**: 同一架构无需修改即可处理 T2V 和 I2V 任务，Agent 根据输入条件集自动适配。

## 实验关键数据

### T2V-CompBench（CogVideoX-5B，7 个类别，1400 prompts）

| 方法 | Consist-attr | Spatial | Numeracy | AVG |
|------|-------------|---------|----------|-----|
| Vanilla CogVideoX-5B | 61.64 | 51.72 | 37.06 | 41.89 |
| VPO (prompt optimizer) | 76.43 | 54.18 | 45.72 | 48.55 |
| BoN + VQAScore | 80.83 | 56.62 | 44.48 | 48.70 |
| **VQQA (Gemini-3-Pro)** | **84.58** | **66.03** | **50.91** | **53.46** |

最大提升类别：consistent-attribute +22.94%，spatial +14.31%，numeracy +13.85%。

### VBench2（CogVideoX-5B，5 维度）

| 方法 | Creativity | Physics | Total |
|------|-----------|---------|-------|
| Vanilla CogVideoX-5B | 42.99 | 38.57 | 41.98 |
| BoN + VQAScore | 51.51 | 42.49 | 46.95 |
| **VQQA (Gemini-3-Pro)** | **54.85** | **54.26** | **50.41** |

Physics 维度提升最显著：38.57%→54.26%（+15.69%），说明闭环反馈对物理真实感修复效果突出。

### VBench-I2V（CogVideoX-5B-I2V）

- VQQA (Gemini-3-Pro) 平均 97.86%，比 vanilla 97.62% 提升 +1.24%。
- 平均仅需 1.6 步迭代即满足停止条件，效率极高。

### 问题生成质量验证

在 VideoFeedback2 测试集上：VQQA 的 End-to-End Recall 为 82.08%，比 VLM 直接分析的 70.18% 高出 11.9%，Precision 均 >99%。

### Veo 3.1（商用模型泛化）

在已有内部 prompt 优化的 Veo 3.1 上，VQQA 仍能从 55.93% 提升到 61.81%（+5.88%），验证了模型无关性。

## 亮点与局限

- "评估反馈作为语义梯度"将评估和改进统一到闭环中，概念新颖且实用
- 完全不需要模型权重访问，只通过自然语言接口优化 prompt——对商用 API 友好
- 4 步迭代已能捕获大部分收益，计算效率可控
- 多 Agent 分工清晰：QG 聚焦覆盖面、QA 聚焦定位精度、PR 聚焦修复
- **局限**: I2V 任务上提升有限（+1.24%），可能因该任务已接近饱和或 prompt 空间优化余地较小
- **局限**: 每轮迭代需调用 VLM + 视频生成模型，绝对计算量仍取决于底层模型推理成本

## 评分
- 新颖性: ⭐⭐⭐⭐ 闭环评估-改进范式新颖，语义梯度概念精巧
- 实验充分度: ⭐⭐⭐⭐⭐ 三大 benchmark + 消融 + 商用模型验证
- 价值: ⭐⭐⭐⭐ 实用的黑盒视频生成质量改进方案
