# Beyond Heuristic Prompting: A Concept-Guided Bayesian Framework for Zero-Shot Image Recognition

**日期**: 2026-03-09  
**arXiv**: [2603.07911](https://arxiv.org/abs/2603.07911)  
**代码**: [GitHub](https://github.com/less-and-less-bugs/CGBC)  
**领域**: 多模态/VLM  
**关键词**: zero-shot recognition, Bayesian inference, concept discovery, CLIP, prompt engineering

## 一句话总结
将 VLM 的零样本图像识别重新建模为概念空间上的贝叶斯边际化推断——用 LLM 驱动的四阶段流水线生成判别性、组合性、多样性的概念集合，再用自适应 soft-trim likelihood 下调离群概念权重，在 11 个数据集上一致超过 SOTA 零样本方法。

## 研究背景与动机

1. **领域现状**: CLIP 等 VLM 通过 "A photo of {class}" 模板实现零样本分类。为提升效果，一些方法用 LLM 生成更多类别描述（如 CuPL）或做测试时增强（如 TPT/MTA）。

2. **现有痛点**: (a) prompt 增强方法依赖启发式设计，缺乏理论依据；(b) 细粒度分类时难以定义有意义的子类（如具体车型）；(c) 多个 prompt 的相似度分布常呈长尾/偏斜分布，离群 prompt 会降低准确率；(d) 简单平均所有 prompt 分数忽略了概念质量差异。

3. **核心矛盾**: 需要丰富的概念集合来覆盖类别语义空间，但概念越多离群概念越多，简单聚合反而有害。

4. **切入角度**: 将概念视为隐变量，从贝叶斯推断角度重新审视零样本分类——分类 = 概念空间上的边际化，每个概念由先验和似然加权。

5. **核心 idea**: $p(Y_i|X) = \sum_{C_{i,j}} p(Y_i|X,C_{i,j}) \cdot p(X|C_{i,j})$，关键在于构建好的概念提议分布和鲁棒的似然估计。

## 方法详解

### 整体框架
输入图像 + 类别集合 → LLM 四阶段概念合成（得到每个类的概念集合 $\mathcal{C}_i$）→ CLIP 计算图像与概念增强 prompt 的相似度 → 自适应 soft-trim 下调离群概念 → 加权求和得到 $p(Y_i|X)$ → 分类。

### 关键设计

1. **LLM 驱动的四阶段概念合成流水线**:
   - **Step 1 — 硬负例邻域构建**: 用 CLIP 文本编码器计算类间余弦相似度，为每个类找 $H$ 个最相似的混淆类
   - **Step 2 — 对比式原子概念生成**: 将目标类和硬负例类一起喂给 LLM，要求生成能区分它们的判别性原子概念（如区分锤头鲨和其他鲨鱼的 "T形扁平头部"）
   - **Step 3 — 组合概念构造**: 从原子概念池中随机采样组合（如 "X or Y or Z"），产生复合概念，增强语义覆盖
   - **Step 4 — DPP 多样性选择**: 用 Determinantal Point Process 从候选复合概念中选出语义冗余最小的子集
   - 设计动机：三个性质（判别性→硬负例对比、组合性→原子组合、多样性→DPP）是经典概念发现理论的现代实例化

2. **自适应 Soft-Trim Likelihood**:
   - 做什么：对每个类的相似度集合 $\mathcal{S}_i$ 估计离群率并下调离群概念权重
   - 核心思路：先算中位数 $m_i$ 和 MAD，估计污染率 $\hat{\rho}_i$（偏离中位数 $\lambda \cdot \text{MAD}$ 的比例），再用 sigmoid 函数给每个概念计算可靠性权重 $w_{i,j}$
   - 公式：$w_{i,j} = \sigma\left(-\log\frac{1-\hat{\rho}_i}{\hat{\rho}_i} \cdot \frac{|S_{i,j} - m_i| \cdot k}{\text{MAD}_i}\right)$
   - 设计动机：相当于 Huber 污染模型下的鲁棒均值估计，有理论保证

3. **理论保证**:
   - Robust Guarantee：估计误差 $|\hat{\mu}_i - \mu_i|$ 随污染率 $\rho_i$ 线性增长，随概念数 $M_i$ 减小
   - 多分类超额风险界：excess risk 由最大污染率、最大方差和最小概念集大小控制

### 训练策略
- 完全 training-free：概念离线生成+编码一次，推理时只需一次前向传播
- 无需 test-time augmentation，消除了 TPT/MTA 的推理计算开销

## 实验关键数据

### 主实验（11 个数据集平均准确率，ViT-B/16）

| 方法 | 平均 Acc | ImageNet | Cars | SUN397 | 额外开销 |
|------|---------|----------|------|--------|---------|
| CLIP | 63.5 | 66.7 | 65.5 | 62.3 | (1 view, 1 prompt) |
| CuPL | 65.2 | 67.6 | 66.0 | 65.3 | (1, 多 prompt) |
| TPT | 66.1 | 68.9 | 66.3 | 65.4 | (64 views, 优化) |
| MTA | 67.4 | 69.7 | 67.2 | 66.8 | (64 views, 优化) |
| **CGBC (M=50)** | **68.9** | **70.4** | **68.5** | **67.6** | (1, 50 prompts) |

### 消融实验

| 配置 | 平均 Acc | 说明 |
|------|---------|------|
| CGBC Full | **68.9** | 完整方法 |
| CGBC Prior（无 likelihood） | 66.8 | 简单平均，不做 soft-trim |
| 随机概念（无 4 阶段流水线） | 65.1 | 概念质量差 |
| 无 DPP（Step 4 替换为随机选） | 67.3 | 冗余概念降低效率 |
| 无组合（仅原子概念） | 67.8 | 组合提升 +1.1% |

### 关键发现
- Soft-trim likelihood 贡献最大（+2.1%），离群概念问题确实严重
- 硬负例对比生成的概念比普通 LLM 生成更判别
- 概念数从 16 增到 50 有稳定提升，但边际递减
- 在细粒度数据集（Cars/Aircraft）上的优势比粗粒度更明显

## 亮点与洞察
- **贝叶斯视角统一了 prompt 增强**: 以前的方法（CuPL等）本质上都是在做概念空间上的粗糙边际化，本文给出了理论框架
- **Soft-trim likelihood 的优雅**: 用 Huber 污染模型 + sigmoid 权重做鲁棒估计，有闭式形式+理论保证
- **四阶段流水线可复用**: 判别性+组合性+多样性三原则适用于任何需要概念集合的任务
- **Training-free**: 不需要任何训练或 test-time optimization，部署友好

## 局限性 / 可改进方向
- LLM 概念生成质量依赖 GPT-4.1 Turbo，模型成本较高
- 离线概念生成+编码的存储开销随类别数线性增长
- 贝叶斯框架假设概念独立且服从简单分布，实际概念间有复杂相关性
- 仅在图像分类上验证，未扩展到检索/VQA 等其他零样本场景

## 相关工作与启发
- **vs CuPL**: CuPL 启发式地用多 prompt 平均分数，CGBC 从贝叶斯角度推导出需要似然加权而非简单平均
- **vs TPT/MTA**: 这些方法通过 test-time augmentation + 优化提升，计算开销大；CGBC 用概念多样性替代了数据增强
- **vs ZERO**: 层次化 prompt 设计，但缺少鲁棒估计和理论保证

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 贝叶斯视角 + DPP 选择 + robust likelihood 三位一体
- 实验充分度: ⭐⭐⭐⭐⭐ 11 个数据集 + 多个消融 + 理论分析
- 写作质量: ⭐⭐⭐⭐⭐ 理论推导严谨，行文清晰
- 价值: ⭐⭐⭐⭐ 零样本分类的新范式，实用且有理论深度
