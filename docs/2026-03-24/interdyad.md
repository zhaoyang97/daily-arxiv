# InterDyad: Interactive Dyadic Speech-to-Video Generation by Querying Intermediate Visual Guidance

**日期**: 2026-03-24  
**arXiv**: [2603.23132](https://arxiv.org/abs/2603.23132)  
**代码**: [项目页面](https://interdyad.github.io/)  
**领域**: 视频理解 / 数字人 / 多人对话生成  
**关键词**: dyadic interaction, speech-to-video, MetaQuery, modality alignment, Gaussian guidance

## 一句话总结
提出 InterDyad，一个双人对话视频生成框架：通过 Interactivity Injector 注入参考视频的运动先验，MetaQuery 模态对齐机制将对话语音映射到交互模式空间，RoDG 解决极端头部姿态下的唇同步问题，在视觉质量、唇同步和新提出的交互指标上全面超越 MultiTalk/InfiniteTalk/LongCat。

## 研究背景与动机

1. **领域现状**: 单人 Speech-to-Video 生成已取得巨大进展（基于 DiT 的端到端生成），多人场景的工作也在增加（MultiTalk 用 L-RoPE 绑定身份和音频，InfiniteTalk 做长视频配音）。

2. **现有痛点**: 当前多人方法主要关注音频-个体运动的同步和身份绑定，忽略了跨个体的交互动态——听者应该根据说话者的语音内容做出相应的非语言反馈（点头、姿态调整等），现有方法生成的"听者"基本是静态或随机运动。

3. **核心矛盾**: (1) 文本 prompt 缺乏时间精度，无法描述"在某个强调词后点头"这种细粒度交互；(2) 说话者音频和听者反应之间存在跨模态鸿沟，直接从音频预测交互很难；(3) 自然对话中频繁的转头和对视导致极端侧脸视角，唇同步严重退化。

4. **切入角度**: 构建一个"语音 → 运动先验"的中间桥梁——先从参考视频提取身份无关的运动模式，再用 MLLM 学习从对话音频映射到这个运动空间。

5. **核心 idea**: 两阶段解耦——Stage 1 学视频重演（motion prior 注入），Stage 2 学音频到运动的跨模态对齐（MetaQuery），推理时可以纯从音频驱动双人交互。

## 方法详解

### 整体框架
基于 Wan2.1-I2V-14B 构建，输入一帧双人参考图 + 双轨音频 + 文本 prompt，输出自然的双人对话视频。支持两种模式：(1) 从参考视频复制交互模式（黄色结果） (2) 纯从音频推断交互（蓝色结果）。

### 关键设计

1. **Interactivity Injector（交互注入器）**:
   - 做什么：从参考视频中提取身份无关的交互运动 latent $\mathbf{m}_k$，注入到扩散生成过程
   - 核心思路：用预训练 motion encoder 提取运动先验，关键trick——**Lips-Masking Strategy**：编码前遮住嘴部区域，确保提取的动态只包含非语言行为（头部运动、姿态），不干扰音频驱动的唇同步。通过 **Spatial-Masking Cross-Attention** 将 Speaker 和 Listener 的运动先验分别注入各自的空间区域
   - 设计动机：将"交互"建模为显式可控的模态，而非隐式 latent

2. **MetaQuery 模态对齐**:
   - 做什么：将对话音频映射到 Stage 1 优化好的运动先验空间
   - 核心思路：用冻结的 Qwen3-Omni 作为多模态编码器，输入双轨音频、参考图和文本描述。引入时间对齐的可学习 **MetaQuery** 序列 $\mathcal{Q} \in \mathbb{R}^{N \times D}$（每个 query 严格对应一个音频帧），经过 1D Conv + Transformer Encoder + Linear 组成的 Temporal Connector 网络，输出预测的交互模式 $\hat{\mathbf{m}}$
   - 损失函数：$\mathcal{L}_{\text{align}} = \|\mathbf{m} - \hat{\mathbf{m}}\|_2^2 + \|\Delta\mathbf{m} - \Delta\hat{\mathbf{m}}\|_2^2$（MSE + 时间差分平滑）
   - 设计动机：MLLM 能理解语音中的语义意图和韵律强调，MetaQuery 作为可学习接口桥接高层语义和细粒度运动

3. **Role-aware Dyadic Gaussian Guidance (RoDG)**:
   - 做什么：推理时自适应增强说话者嘴部区域的音频 CFG 引导
   - 核心思路：用 VAD 确定每帧的说话者/听者角色，在说话者嘴部位置构建 2D 高斯图 $\mathbf{G}_k$，将音频 CFG 强度空间调制为 $w_a(\mathbf{x},t) = w_{\text{base}} + \alpha_t \cdot \mathbb{I}(k=S_t) \cdot \mathbf{G}_k$，听者嘴部区域不加音频引导
   - 设计动机：避免音频引导"泄漏"到非说话者的嘴上，同时在说话者的嘴部区域加强引导以抵抗极端姿态带来的唇同步退化

### 训练策略
- 训练数据：从海量视频中过滤出 70 万条高质量双人对话视频（720P+, 25fps, 3-10秒）
- Stage 1 (模态对齐): 6000 iterations, 12 小时
- Stage 2 (端到端 DiT 微调): 10000 iterations, 2 天

## 实验关键数据

### 主实验

| 方法 | FID↓ | FVD↓ | ID-Cons↑ | Sync-C↑ | DI-Sync↑ | DI-Sali↑ |
|------|------|------|----------|---------|----------|----------|
| MultiTalk | 49.60 | 477.62 | 0.5275 | 3.2253 | 0.2333 | 0.8889 |
| InfiniteTalk | 46.38 | 440.67 | **0.6418** | 3.0446 | 0.2371 | 0.8560 |
| LongCat-VA | 45.47 | 548.83 | 0.6059 | 3.1985 | 0.2417 | 1.1145 |
| **Ours** | **44.07** | **390.58** | 0.6260 | **3.5618** | **0.2744** | **1.2879** |

- DI-Sync (交互时间同步) +13.5% vs 次优，DI-Sali (交互活跃度) +15.5%
- ID-Cons 略低于 InfiniteTalk 是因为更丰富的交互动作带来更多极端侧脸

### 消融实验

| 配置 | FID | Sync-C | DI-Sync | DI-Sali |
|------|-----|--------|---------|---------|
| w/o Interactivity Injector | 44.81 | 3.42 | 0.2416 | 1.0234 |
| w/o MetaQuery Alignment | 43.25 | 3.53 | 0.2501 | 1.1576 |
| w/o RoDG | 44.52 | 3.18 | 0.2712 | 1.2645 |
| **Full model** | **44.07** | **3.56** | **0.2744** | **1.2879** |

### 关键发现
- Interactivity Injector 对交互质量贡献最大（DI-Sali 从 1.02 到 1.29）
- RoDG 主要提升唇同步（Sync-C 3.18→3.56），对交互性几乎无影响
- MetaQuery 对齐使纯音频驱动的交互成为可能，不再需要参考视频

## 亮点与洞察
- **"交互作为模态"的设计哲学**：把双人交互动态显式解耦为可提取、可映射、可注入的模态，而非让模型隐式学习。这个思路可以推广到多人场景和更复杂的社交动态建模
- **Lips-Masking 是小而关键的 trick**：避免参考视频的嘴部运动干扰音频驱动的唇同步，简单但有效
- **DI-Sync 和 DI-Sali 指标**：首次定量衡量双人对话中的交互质量，DI-Sync 用 MLLM 提取韵律强调和反应行为的时间段做 TIoU，比人工评估更可复现

## 局限性 / 可改进方向
- 只处理双人场景，多人（>2）的交互建模未涉及
- MetaQuery 的时间对齐是严格一对一的，对于更长时间跨度的交互响应可能不够灵活
- 交互模式的多样性受限于训练数据中的交互类型
- 对极端遮挡（如一人完全遮住另一人）的处理未讨论

## 相关工作与启发
- **vs InfiniteTalk**: InfiniteTalk 专注于长视频的身份一致性，但不建模交互；InterDyad 通过 Interactivity Injector 显式注入交互动态
- **vs INFP/DiTaiListener**: 这些听者反应生成方法通常只做分屏或正面场景，不处理共享画布中的空间关系
- **vs MultiTalk**: MultiTalk 用 L-RoPE 做身份绑定，InterDyad 在此基础上增加了交互维度

## 评分
- 新颖性: ⭐⭐⭐⭐ 将交互作为显式模态、MetaQuery 桥接音频和运动空间的思路新颖
- 实验充分度: ⭐⭐⭐⭐ 定量对比+消融+新指标设计，但 baseline 偏少
- 写作质量: ⭐⭐⭐⭐ 模块化描述清晰，但公式较多稍显冗长
- 价值: ⭐⭐⭐⭐ 双人对话场景在数字人/虚拟会议等应用中需求大，首次系统解决交互问题
