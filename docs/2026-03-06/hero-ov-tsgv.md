# HERO: Hierarchical Embedding-Refinement for Open-Vocabulary Temporal Sentence Grounding

**日期**: 2026-03-06  
**arXiv**: [2603.06732](https://arxiv.org/abs/2603.06732)  
**代码**: https://github.com/TTingHan-HDU/HERO  
**领域**: 视频理解  
**关键词**: temporal grounding, open-vocabulary, hierarchical embedding, contrastive learning, video-language alignment

## 一句话总结
首次定义 Open-Vocabulary TSGV 任务并构建 Charades-OV/ActivityNet-OV benchmark，提出 HERO 框架通过层次语义嵌入 + 语义引导视觉过滤 + 对比掩码文本精炼三个模块，在开放词汇场景下大幅提升时序句子定位的泛化能力。

## 研究背景与动机

1. **领域现状**：时序句子定位（TSGV）旨在根据自然语言查询定位视频中对应片段。现有方法（proposal-based 和 proposal-free）在闭合词汇设置下取得了不错结果，但训练和测试使用相同词汇分布。

2. **现有痛点**：(a) 现有模型严重过拟合训练集的词汇分布——将 query 中的 "person" 替换为语义等价的 "human"，定位性能就显著下降；(b) 既有的去偏 benchmark（Charades-CD、ActivityNet-CD）虽然考虑了分布偏移，但 96% 的测试句子仍然只包含训练集中出现过的词汇，本质上还是闭合词汇。

3. **核心矛盾**：实际应用中用户使用的语言表达多样且不受约束，但 TSGV 模型对词汇变化极为脆弱——根本原因是模型学到的是特定词汇到视觉特征的映射，而非语义级别的跨模态对齐。

4. **切入角度**：如果模型能在多个语义抽象层次（从词汇到概念）上理解 query，就能更鲁棒地处理同义替换和改述。同时，通过掩码文本的对比学习，可以迫使模型不依赖特定词汇。

5. **核心 idea**：层次语义编码（低级词汇→高级语义）+ 对比掩码训练实现开放词汇时序定位。

## 方法详解

### 整体框架
输入视频（I3D 特征）+ 文本 query（GloVe 嵌入）→ Hierarchical Embedding Module (HEM) 提取 4 层语义表示 → 4 个并行 CFRE 分支分别做语义引导视觉过滤(SGVF) + 对比掩码文本精炼(CMTR) → 时序定位模块预测每层的时间边界和相关性分数 → 可学习加权聚合得到最终预测 $(s, e)$。

### 关键设计

1. **Hierarchical Embedding Module (HEM)**:
   - 做什么：将 query 编码为 4 层不同语义抽象级别的表示
   - 核心思路：6 层 Transformer Encoder，分别取第 0（原始嵌入）、2、4、6 层输出作为 $Q_0, Q_1, Q_2, Q_3$。低层保留词汇细节，高层捕获语义概念
   - 设计动机：开放词汇的关键挑战是同义词/改述难以在单一表示层级处理——"boy grabs skateboard" 和 "kid picks up object" 在词汇层完全不同，但在高层语义相近。多层次编码允许模型在合适的抽象层找到匹配

2. **Semantic-Guided Visual Filter (SGVF)**:
   - 做什么：用文本语义引导过滤无关视觉内容
   - 核心思路：cross-attention 以视频 $V$ 为 query、文本 $Q_i$ 为 key/value，得到注意力后经 sigmoid 生成软相关系数 $\hat{V}_i = V \odot \sigma(V_i^{attn})$
   - 设计动机：视频中大量帧与 query 无关（背景噪声），直接融合会稀释有效信号。SGVF 在特征层面抑制无关帧，提升跨模态对齐精度

3. **Contrastive Masked Text Refiner (CMTR)**:
   - 做什么：通过随机掩码 query token + 对比学习提升文本鲁棒性
   - 核心思路：随机掩码 $Q_i$ 生成 $Q_i^m$，分别与视频特征融合后计算相关性分数 $RS$ 和 $RS^m$，最小化 KL 散度 $\mathcal{L}_{CL} = D_{KL}(RS \| RS^m)$
   - 设计动机：掩码训练迫使模型不依赖单个特定词汇进行定位——即使 query 中部分词被遮住，模型仍需给出一致的相关性判断。这直接增强了对词汇变化和缺失的鲁棒性

### 损失函数
总损失：$\mathcal{L} = \mathcal{L}_{TSGV} + \lambda_1 \mathcal{L}_{RS} + \lambda_2 \mathcal{L}_{CL}$
- $\mathcal{L}_{TSGV}$：时序定位主损失（继承自 EMB baseline）
- $\mathcal{L}_{RS}$：帧级相关性 BCE loss（对原始和掩码 query 各算一次取平均）
- $\mathcal{L}_{CL}$：对比掩码文本一致性 KL loss
- $\lambda_1 = \lambda_2 = 0.1$

## 实验关键数据

### 主实验（Open-Vocabulary TSGV）

| 方法 | Charades-OV R1@0.5 | Charades-OV R1@0.7 | ActivityNet-OV R1@0.5 | ActivityNet-OV R1@0.7 |
|------|:---:|:---:|:---:|:---:|
| EMB | 43.88 | 25.99 | 21.70 | 10.78 |
| TR-DETR | 45.36 | 21.87 | 19.41 | 9.00 |
| **HERO** | **45.51** | **27.20** | **25.23** | **12.18** |

### 标准 Benchmark（Charades-STA）

| 方法 | R1@0.5 | R1@0.7 |
|------|:---:|:---:|
| FlashVTG | 60.11 | 38.01 |
| $R^2$-tuning | 59.78 | 37.02 |
| EMB (baseline) | 58.33 | 39.25 |
| **HERO** | - | **>39.25** |

### 关键发现
- 在 Open-Vocabulary 设置下所有现有方法性能大幅下降（对比标准 benchmark），验证了词汇脆弱性问题真实存在
- HERO 在 ActivityNet-OV 上 R1@0.5 比 EMB 提升 +3.53 个点（25.23 vs 21.70），在开放词汇场景提升最为显著
- Charades-CD 96% 测试句子不含新词 → Charades-OV 100% 测试句子含至少一个新词，benchmark 的词汇新颖度质变
- 层次嵌入的贡献：高层语义抽象对词汇替换（如 person→human）的鲁棒性至关重要

## 亮点与洞察
- **OV-TSGV 任务定义的价值超过方法本身**：首次揭示了 TSGV 领域的词汇脆弱性——现有 benchmark 看似测泛化，实际 96% 测试不含新词。这个问题的暴露比解法更重要
- **CMTR 的掩码对比策略可直接迁移**：这种"让模型在信息缺失时保持一致输出"的训练策略，可以用在任何需要鲁棒跨模态对齐的场景（如 VQA、图文检索）
- **插件式设计实用性强**：HERO 的 HEM+CFRE 作为即插即用模块可接入任何 TSGV backbone，不需要修改原有架构

## 局限性 / 可改进方向
- 使用 I3D + GloVe 作为特征提取器，未探索更强的预训练特征（如 CLIP visual + BERT text），泛化能力可能被特征表示限制
- 只测试了作为 EMB 的插件，没有在更强的 DETR-style backbone 上验证效果
- OV benchmark 的构造依赖 LLM 改写 + 人工验证，改写质量和覆盖度受限于改写策略
- 层次嵌入固定为 4 层，没有消融不同层数的影响

## 相关工作与启发
- **vs EMB**: HERO 的 baseline，proposal-free 方法。HERO 在其基础上增加 HEM+CFRE，在 OV 设置下特别有效
- **vs TR-DETR/QD-DETR**: DETR-style 方法在标准 benchmark 上强，但 OV 设置下同样脆弱
- **vs 开放词汇目标检测**: TSGV 的"类别"不是预定义标签而是自由形式 query 中的词汇，问题定义更复杂

## 评分
- 新颖性: ⭐⭐⭐⭐ 任务定义有价值，benchmark 构建合理，但方法（层次嵌入+对比学习）相对标准
- 实验充分度: ⭐⭐⭐⭐ 覆盖标准和 OV benchmark，对比多种 baseline
- 写作质量: ⭐⭐⭐⭐ 问题定义清晰，benchmark 分析有说服力
- 价值: ⭐⭐⭐⭐ 开辟 OV-TSGV 研究方向，benchmark 对社区有持续影响
