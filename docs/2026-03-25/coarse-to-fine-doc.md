# PaddleOCR-VL: Boosting Document Parsing with Coarse-to-Fine Visual Processing

**日期**: 2026-03-25  
**arXiv**: [2603.24326](https://arxiv.org/abs/2603.24326)  
**代码**: https://github.com/PaddlePaddle/PaddleOCR  
**领域**: 多模态VLM / 文档解析  
**关键词**: document parsing, coarse-to-fine, visual token efficiency, OCR, layout detection

## 一句话总结

提出 PaddleOCR-VL，一个粗到细的文档解析框架：粗阶段用轻量级 VRFM（基于 RT-DETR + pointer network）检测有效区域并预测阅读顺序，细阶段用 0.9B 的 VLM 精细识别裁剪区域，仅用 2561 个 vision token 就在 OmniDocBench v1.5 上取得 92.62 分 SOTA，超越参数量 80 倍以上的大模型。

## 研究背景与动机

1. **领域现状**：文档解析需要从复杂文档中提取文字、公式、表格、图表等元素并确定阅读顺序。当前方法分三类：pipeline 方法（误差传播）、通用 VLM（幻觉严重）、专用 VLM（token 效率低）。

2. **现有痛点**：高分辨率输入对文档解析至关重要（小字、密集表格），但 vision token 数量随分辨率平方增长，计算成本爆炸。分析显示文档中 PPT 有效区域仅占 39%，即使信息密集的报纸也只占约 60%——大量计算浪费在背景上。

3. **核心矛盾**：现有 VLM 方法要么端到端处理全图（token 多、慢）、要么压缩全图 token（丢失布局精度），无法兼顾效率和精度。

4. **切入角度**：文档视觉信息分布极不均匀，利用这种稀疏性可以将计算集中在有效区域，跳过冗余背景。

5. **核心 idea**：将布局分析（轻量检测器完成）和元素识别（紧凑 VLM 完成）解耦为两个专精模块，每个模块独立优化，先定位后识别，避免对全图做 VLM 推理。

## 方法详解

### 整体框架
文档图像 → VRFM（粗阶段：检测有效区域 + 分类 + 阅读顺序预测）→ 裁剪有效区域 → PaddleOCR-VL-0.9B（细阶段：对每个裁剪区域做元素级识别）→ 按阅读顺序拼接 → 结构化文档输出。

### 关键设计

1. **Valid Region Focus Module (VRFM)**:
   - 做什么：轻量级检测文档中的有效区域（文本块、表格、公式、图表），同时预测阅读顺序
   - 核心思路：基于 RT-DETR 做布局检测和分类，在检测表示之上接 pointer network 建模区域间成对关系，预测 $N \times N$ 排序矩阵
   - 训练策略：两阶段——先训 RT-DETR 核心 100 epochs（用 PP-DocLayout_Plus-L 权重初始化），再冻结核心训 pointer network 200 epochs（用 Generalized CE Loss 处理噪声标注）
   - 设计动机：比 VLM-based 布局检测快得多且不会出现坐标飘移，同时 pointer network 优雅地解决了阅读顺序预测问题

2. **PaddleOCR-VL-0.9B（元素识别模型）**:
   - 做什么：对 VRFM 裁剪出的有效区域做精细识别（文字、表格、公式、图表等）
   - 架构：NaViT 风格视觉编码器（Keye-VL 初始化）+ 2 层 MLP 投影器（GELU 激活）+ ERNIE-4.5-0.3B 语言模型（+3D-RoPE）
   - 关键设计：**原生动态分辨率处理**——不做固定分辨率或 tiling，直接按原始分辨率处理，避免失真和幻觉
   - 训练：Stage 1 预对齐 29M 图文对 + Stage 2 指令微调 2.7M 样本（覆盖 OCR、表格 OTSL、公式 LaTeX、图表 Markdown）
   - 设计动机：因为输入是裁剪后的小区域而非全页，0.9B 小模型即可处理，token 数大幅减少

3. **高质量数据流水线（30M+ 样本）**:
   - 四来源：开源数据集（CASIA-HWDB、UniMER-1M 等）+ 合成数据（补充不平衡类别）+ 网络爬取（真实多样性）+ 自有数据
   - 自动标注：PP-StructureV3 生成伪标签 → ERNIE-4.5-VL / Qwen2.5-VL 精修 → 幻觉过滤
   - 难例挖掘：构建精标评估集 → 按子类别评估 → 针对弱项用 XeLaTeX/浏览器渲染合成新数据

### 训练策略
- VRFM：2 万+ 样本，RT-DETR 100 epochs + pointer network 200 epochs
- VLM Stage 1：29M 样本，max 1280 分辨率，LR 5e-5→5e-6，1 epoch
- VLM Stage 2：2.7M 样本，max 2048 分辨率，LR 5e-6→5e-7，2 epochs

## 实验关键数据

### 主实验（OmniDocBench v1.5 页面级解析）

| 方法 | 参数量 | Vision Tokens | Overall↑ | Text-Edit↓ | Formula-CDM↑ | Table-TEDS↑ |
|------|--------|--------------|----------|-----------|-------------|-------------|
| Qwen2.5-VL-72B | 72B | 5626 | 87.02 | 0.094 | 88.27 | 82.15 |
| Gemini-2.5 Pro | - | - | 88.03 | 0.075 | 85.82 | 85.71 |
| MonkeyOCR-pro-3B | 3.7B | 3962 | 88.85 | 0.075 | 87.25 | 86.78 |
| MinerU2.5 | 1.2B | 3256 | 90.67 | 0.047 | 88.46 | 88.22 |
| **PaddleOCR-VL-L** | **0.9B** | **2561** | **92.62** | **0.035** | **90.90** | **90.48** |

0.9B 模型以最少 token 和最小参数量取得全面 SOTA，Overall 比 MinerU2.5 高 2 分，比 72B 的 Qwen2.5-VL 高 5.6 分。

### S/M/L 配置对比

| 配置 | Vision Tokens | Overall | 适用分辨率范围 |
|------|-------------|---------|--------------|
| PaddleOCR-VL-S | 1898 | 91.55 | [3136, 235200] |
| PaddleOCR-VL-M | 2259 | 92.17 | [3136, 392000] |
| PaddleOCR-VL-L | 2561 | 92.62 | [3136, 627200] |

### 关键发现
- **粗到细解耦>端到端**：VRFM 过滤掉 40-60% 的冗余区域，让 0.9B 小模型专注有效内容即可超越 72B 大模型
- **原生动分辨率很重要**：NaViT 风格编码器避免了 tiling/resize 带来的失真，对小字体和密集表格尤为关键
- **数据是核心竞争力**：30M+ 高质量样本 + 自动标注 + 难例挖掘是达到 SOTA 的关键因素
- **阅读顺序**：pointer network 在读序预测上达 0.043 Edit Distance，超越所有对比方法
- **支持 109 种语言**，对手写和历史文档也有较强鲁棒性

## 亮点与洞察
- **解耦设计的工程智慧**：将布局检测（用成熟的目标检测方案）和元素识别（用轻量 VLM）分开，各自优化到最优，比端到端方案更实用。这种思路对任何"不同子任务难度不对称"的场景都有参考价值
- **pointer network 做阅读顺序**：巧妙地把阅读顺序建模为排列问题，比 VLM 自回归预测坐标更稳定
- **数据流水线本身的价值**：自动标注→VLM 精修→幻觉过滤→难例挖掘的闭环，是可复用的数据生产方案

## 局限性 / 可改进方向
- 两阶段流水线增加了工程复杂度和维护成本
- VRFM 检测失败（漏检有效区域）会导致不可恢复的信息丢失
- 对均匀密集的全页小字文档（如法律文件），冗余区域少，粗到细的效率优势减弱
- pointer network 的 $N \times N$ 阅读顺序矩阵在超长文档（数百个元素）时可能遇到规模瓶颈

## 相关工作与启发
- **vs MinerU2.5**: MinerU2.5 是前 SOTA（90.67），同为两阶段设计但 VLM 部分 1.2B + 3256 tokens；PaddleOCR-VL 用 0.9B + 2561 tokens 超 2 分，核心改进在 NaViT 动态分辨率和更大规模数据
- **vs DeepSeek-OCR**: DeepSeek-OCR 用 token 压缩减少成本但降低布局精度；PaddleOCR-VL 通过区域裁剪从根本上减少无关 token
- **vs dots.ocr**: dots.ocr 端到端 3B 模型达 88.41，但 token 多（5513）且推理慢；PaddleOCR-VL 更小更快且高 4 分

## 评分
- 新颖性: ⭐⭐⭐ 粗到细思路不新，但 VRFM+pointer network+NaViT 的具体组合有工程创新
- 实验充分度: ⭐⭐⭐⭐⭐ OmniDocBench + 元素级评测 + 多语言 + 效率分析，极其全面
- 写作质量: ⭐⭐⭐⭐ 结构清晰，数据详实
- 价值: ⭐⭐⭐⭐⭐ 百度开源，实用性极高，0.9B 超越 72B 的结果对工业部署有重大意义
