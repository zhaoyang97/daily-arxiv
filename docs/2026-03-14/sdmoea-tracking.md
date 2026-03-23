# Sparse-Dense Mixture of Experts Adapter for Multi-Modal Tracking

**日期**: 2026-03-14  
**arXiv**: [2603.13719](https://arxiv.org/abs/2603.13719)  
**代码**: 无  
**领域**: 视频理解 / 多模态跟踪  
**关键词**: multi-modal tracking, mixture of experts, parameter-efficient fine-tuning, hypergraph fusion, adapter

## 一句话总结
提出 SDMoEA 参数高效微调框架，通过 Sparse MoE（建模模态特异信息）+ Dense-Shared MoE（串并混合结构建模模态共享信息）作为多模态 adapter，配合超图融合模块建模高阶跨模态关系，在 7 个多模态跟踪数据集上超越现有 PEFT 方法。

## 研究背景与动机

1. **领域现状**: 多模态跟踪（RGB-T/RGB-E/RGB-D）通过融合多种模态应对复杂场景。参数高效微调（PEFT）方法如 ViPT、SDSTrack 通过 adapter/prompt 适配预训练 RGB 模型到多模态数据。

2. **现有痛点**: (a) 现有 PEFT 方法虽实现统一框架但未共享参数，需为每对模态单独训练模型。(b) 引入 MoE 的 XTrack 虽然共享参数，但**模态共享信息挖掘不足** — 多个并行共享专家计算量大，单个共享专家又无法充分利用跨模态共性。(c) 现有方法在多层级多模态特征融合中**缺乏高阶关系建模**。

3. **核心矛盾**: 多模态数据的异质性使得在共享参数框架中难以同时建模模态特异性和共性，且跨模态特征融合缺乏高阶语义对齐。

4. **切入角度**: 设计串并混合的 Dense-Shared MoE 结构平衡计算效率与共享信息建模能力，用超图捕捉多模态高阶关系。

5. **核心 idea**: Sparse MoE 建模特异性 + 串并结构 Dense-Shared MoE 建模共性 + 超图融合建模高阶跨模态关系。

## 方法详解

### 整体框架
基于 ODTrack（ViT 结构），冻结主干网络，在每个 Transformer block 的 MLP 后嵌入 SDMoE adapter。特征提取后，用 GSAHF 模块融合多级多模态特征，最后通过 box head 预测目标框。

### 关键设计

1. **Sparse MoE（模态特异建模）**:
   - 做什么：含 N=4 个特异专家，每个 token 通过 router 只选 K=1 个专家参与计算
   - 核心思路：每个专家由 down-projection（维度压缩 12 倍）→ gate + SiLU 激活 → up-projection 组成。只有被选中的专家参与前向传播，大幅扩展模型容量而计算量几乎不增
   - 使用 expert balance loss 防止路由坍塌

2. **Dense-Shared MoE（模态共享建模，串并结构）**:
   - 做什么：建模不同模态间的共享信息
   - 核心思路：**串并结构**（区别于 DeepSeek-MoE 的并串结构）— 所有专家共享串行的 down-projection 和 up-projection 层，中间有 M=4 个并行子网络（各只含 1 个全连接层）。下投影后特征维度很低，并行子网络计算量极小
   - 设计动机：并串结构中多个并行共享专家太贵，单专家不够；串并结构将共享的维度变换（最贵的部分）提取为公共层，并行部分只做低维特征处理，同时拥有多专家的表达力和低计算量

3. **GSAHF（Gram 语义对齐超图融合）**:
   - 做什么：融合来自 ViT 不同层级的多模态特征，建模高阶关系
   - 核心思路：先用 Gram 矩阵计算跨模态特征的语义相似度做对齐，然后基于距离度量构建超图（每条超边连接多个节点），通过超图卷积提取高阶关系
   - 设计动机：普通图只能建模二元关系，超图可建模多元高阶关系；在跨模态场景中，先做 Gram 对齐确保超图结构准确反映跨模态语义相似性

### 损失函数 / 训练策略
- 跟踪损失 + expert balance loss
- 基于 ODTrack，端到端统一训练

## 实验关键数据

### 主实验（LasHeR RGB-T 跟踪，PEFT 方法对比）

| 方法 | 类型 | PR | AUC |
|------|------|-----|-----|
| ViPT | PEFT | 65.1 | 52.5 |
| SDSTrack | PEFT | 66.5 | 53.1 |
| XTrack-L | PEFT | 73.1 | 58.7 |
| SeqTrackv2-L | PEFT | 76.7 | 61.0 |
| **SDMoEA-L** | **PEFT** | **77.7** | **60.9** |
| SUTrack-L | FFT | 76.9 | 61.9 |

### 消融实验

| 配置 | LasHeR PR/AUC | 说明 |
|------|--------------|------|
| Baseline (无 adapter) | ~65/~52 | 冻结 ViT |
| + Sparse MoE only | 提升 | 模态特异建模有效 |
| + Dense-Shared MoE | 进一步提升 | 共享信息补充 |
| + GSAHF | 最佳 | 高阶融合有贡献 |
| 并串结构 vs 串并结构 | 串并更优 | 串并结构效率更高 |

### 关键发现
- PEFT 方法（SDMoEA-L）PR 达 77.7%，接近全量微调 SOTA（SUTrack-L 76.9% PR），而参数量远少
- 串并结构比 XTrack 的并串 MoE结构性能更好且更高效
- 在 RGB-E（VisEvent、COESOT）和 RGB-D（DepthTrack、VOT-RGBD2022）上同样表现优秀，证实跨模态泛化能力
- 超图融合相对贡献不算很大，但在多层级特征融合场景下有一致提升

## 亮点与洞察
- **串并结构**是对 DeepSeek-MoE 共享专家设计的有效演进 — 将计算密集的维度变换共享化，并行部分轻量化，在参数-计算-性能之间取得更好平衡
- **Gram 矩阵**做跨模态语义对齐是简洁有效的设计 — 不需要额外的对齐网络，直接用内积矩阵衡量特征相关性

## 局限性 / 可改进方向
- 超图构建基于距离度量，可能对特征表示质量敏感
- 仅在 dual-modal 跟踪上实验，三模态及以上场景未验证
- 与全量微调的 SUTrack 在 AUC 上仍有差距（60.9 vs 61.9）

## 相关工作与启发
- **vs XTrack**: 同样用 MoE 做多模态跟踪，但 XTrack 的并串结构共享专家效率低；SDMoEA 的串并结构更优
- **vs ViPT/SDSTrack**: 早期 PEFT 方法需要为每对模态训练单独模型，SDMoEA 真正实现统一参数
- 串并 MoE 结构可推广到其他多任务/多域 PEFT 场景

## 评分
- 新颖性: ⭐⭐⭐ 串并 MoE + 超图融合的组合有新意但各模块单独看并非全新
- 实验充分度: ⭐⭐⭐⭐ 7 个数据集覆盖 3 种模态对，对比全面
- 写作质量: ⭐⭐⭐ 结构清晰但部分描述冗余
- 价值: ⭐⭐⭐⭐ 对多模态跟踪的 PEFT 方案有实用推进
