# Kiwi-Edit: Versatile Video Editing via Instruction and Reference Guidance

**日期**: 2026-03-02  
**arXiv**: [2603.02175](https://arxiv.org/abs/2603.02175)  
**代码**: [https://github.com/showlab/Kiwi-Edit](https://github.com/showlab/Kiwi-Edit)  
**领域**: image_generation  
**关键词**: video editing, reference-guided editing, diffusion transformer, MLLM, dataset curation

## 一句话总结
Kiwi-Edit 提出了一个可扩展的数据生成流水线来构建 477K 高质量的指令-参考图像-视频编辑四元组数据集 RefVIE，并设计了统一的 MLLM-DiT 架构通过 Query Connector 和 Latent Connector 双路径机制实现指令+参考图像引导的视频编辑，在 OpenVE-Bench 上以 3.02 的 Overall 分数超越所有开源基线。

## 研究背景与动机
当前基于指令的视频编辑方法取得了显著进展，但存在一个核心矛盾：**自然语言在描述精细视觉细节（如特定纹理、物体身份、风格特征）时存在固有的模糊性**。用户往往希望通过视觉示例来传达编辑意图（如"把车替换成这辆跑车"），但纯文本模型无法完成此类任务。

参考图像引导的视频编辑是自然的解决方案，但其发展受到**数据稀缺**的严重制约。训练此类模型需要高质量的四元组数据（源视频、编辑指令、参考图像、目标视频），而现有数据集（InsViE、Señorita、Ditto、ReCo、OpenVE）均不提供参考图像。仅有的少数探索（InstructX、Kling-Omni）依赖于闭源私有数据。

Kiwi-Edit 的核心洞察是：**强大的预训练图像生成模型可以作为高保真参考图像合成器**，从而实现可扩展的数据构建。

## 方法详解
### 整体框架
系统包含两个主要组件：(1) 冻结的多模态大语言模型（MLLM，Qwen2.5-VL-3B）用于语义理解；(2) 扩散 Transformer（DiT，Wan2.2-TI2V-5B）用于视频生成。MLLM 编码多模态输入（源视频、指令、参考图像）为条件信号，引导 DiT 生成编辑后的视频。

### 关键设计

**1. 可扩展数据生成流水线（RefVIE 构建）**
- **Stage 1 - 源聚合与过滤**: 从 Ditto-1M、ReCo、OpenVE-3M 聚合 3.7M 样本，使用 EditScore > 6 过滤文本引导样本，EditScore > 8 过滤参考引导样本
- **Stage 2 - 定位与分割**: 用 Qwen3-VL-32B 定位编辑区域，SAM3 精细分割
- **Stage 3 - 参考图像合成**: 用 Qwen-Image-Edit 合成参考图像——背景任务移除前景后修复，局部编辑任务提取目标物体
- **Stage 4 - 质量控制**: MLLM 验证语义一致性，CLIP 特征去重
- 最终从 3.7M 样本中精炼出 477K 高质量四元组

**2. 双连接器机制（Dual-Connector）**
- **Query Connector**: 使用可学习查询 token（图像 256、视频 512、参考任务 768 个）通过 MLP 投影，提炼编辑意图的高层语义
- **Latent Connector**: 提取参考图像对应的视觉 token 并通过独立 MLP 投影，注入密集视觉先验
- 两者输出拼接为统一的 Context Tokens，作为 DiT 交叉注意力的 key/value

**3. 混合潜空间注入策略（Hybrid Injection）**
- **源视频控制（逐元素加法）**: 源帧通过 VAE 编码后经零初始化 PatchEmbed 处理，以可学习的时间步依赖标量 γ(t) 调制后与噪声潜变量逐元素相加：z_t' = PatchEmbed(z_t) + γ(t) · PatchEmbed_src(VAE(x_src))
- **参考图像控制（序列拼接）**: 参考图像 patch-embed 后拼接到 DiT 输入序列，扩展注意力窗口以直接"复制"纹理细节

### 损失函数 / 训练策略
采用 Flow Matching 训练目标，最小化预测速度场与真实漂移的 MSE：L_flow = E[||v_θ(z_t, t, c) - (z_1 - z_0)||²]

**三阶段渐进训练课程**:
- **Stage 1 (MLLM-DiT 对齐)**: 冻结 MLLM 和 DiT，仅训练 LoRA、连接器和查询 token，使用图像编辑三元组数据（GPT-Image-Edit、NHR-Edit）
- **Stage 2 (指令微调)**: 解冻 DiT 联合优化，使用大规模图像+视频编辑数据，从 480p 渐进到 720p
- **Stage 3 (参考引导微调)**: 引入 RefVIE 数据，图像:指令视频:参考视频 = 2:1:1 混合训练

## 实验关键数据
### 主实验

**OpenVE-Bench 指令编辑结果 (Gemini-2.5-Pro 评估)**:

| 方法 | 参数 | Overall | Global Style | Background | Local Change | Local Remove | Local Add |
|------|------|---------|-------------|------------|-------------|-------------|----------|
| Runway Aleph (闭源) | - | 3.49 | 3.72 | 2.62 | 4.18 | 4.16 | 2.78 |
| OpenVE-Edit | 5B | 2.50 | 3.16 | 2.36 | 2.98 | 1.85 | 2.15 |
| DITTO | 14B | 2.13 | 4.01 | 1.68 | 2.03 | 1.53 | 1.41 |
| **Kiwi-Edit (Stage3)** | **5B** | **3.02** | **3.64** | **3.84** | **2.63** | **2.36** | - |

**RefVIE-Bench 参考引导编辑结果**:

| 模型 | Identity Consist. | Temporal Consist. | Physical Consist. | Reference Sim. | Matting Quality | Video Quality | Overall |
|------|----------|----------|----------|----------|----------|----------|---------|
| Runway Aleph | 3.79 | 3.65 | 3.58 | 3.33 | 2.81 | 2.58 | 3.29 |
| Kling-O1 | 4.75 | 4.66 | 4.60 | 3.95 | 3.21 | 2.75 | 3.99 |
| **Kiwi-Edit** | **3.98** | **3.40** | **3.34** | **3.72** | **2.90** | **2.51** | **3.31** |

### 消融实验
- **Channel Concat vs Add**: 通道拼接（2.08 Remove）远差于逐元素加法（2.63），共享 PatchEmbed 降至 1.01
- **时间步缩放**: 移除 γ(t) 后 Remove 从 2.63 降至 2.58
- **对齐阶段**: 跳过 Stage 1 导致灾难性性能下降（1.47）
- **图像协训练**: 去掉图像编辑数据后 Remove 从 2.84 降至 2.58
- **参考条件**: 仅用查询 3.20，加入 Latent Connector 提升至 3.30

### 关键发现
- Background Change 得分 3.84 超越闭源 Runway Aleph 的 2.62
- 5B 参数量的开源模型首次在参考引导编辑上接近商业闭源模型
- Stage 3 提升局部编辑但降低背景性能，归因于数据集偏向局部变化

## 亮点与洞察
1. **Data-centric 方法论**: 核心贡献不仅是模型而是数据——证明从已有编辑对中合成参考图像是可行的大规模方案
2. **双连接器设计精妙**: Query 捕获高层编辑意图，Latent 捕获精细视觉细节，两者互补
3. **混合注入策略合理**: 源视频需要精细的结构保持（逐元素加法+时间步缩放），参考图像需要全局注意力（序列拼接），不同条件采用不同注入方式
4. **渐进训练稳定**: 三阶段从对齐→指令→参考，避免了多条件联合训练的优化困难

## 局限性 / 可改进方向
1. 参考图像合成依赖现有图像编辑模型的质量，错误会级联传播
2. 数据集重度偏向局部编辑，全局风格迁移等任务覆盖不足
3. Identity Consistency (3.98) 和 Kling-O1 (4.75) 的差距仍然显著，特别是物理一致性
4. 最大采样帧数限制为 81 帧，对长视频编辑的泛化性未知
5. 与 Kling-O1 等闭源模型的差距可能来自模型规模和训练数据量

## 相关工作与启发
- 与 InstructX、Kling-Omni 相比，关键优势在于**开源**和**可扩展的数据构建流水线**
- 从 InsV2V 到 Señorita-2M、Ditto 的数据规模扩展，到本文添加参考图像维度，呈现出视频编辑数据集的演进路径
- Query+Latent 双路径设计可迁移到其他多模态条件生成任务

## 评分
- 新颖性: ⭐⭐⭐⭐ 数据生成流水线有创意，但架构层面的创新有限
- 实验充分度: ⭐⭐⭐⭐ 覆盖指令编辑和参考引导编辑，消融实验详细
- 写作质量: ⭐⭐⭐⭐ 结构清晰，流水线描述详尽
- 价值: ⭐⭐⭐⭐⭐ 首个大规模开源参考引导视频编辑数据集+模型，对社区价值极高
