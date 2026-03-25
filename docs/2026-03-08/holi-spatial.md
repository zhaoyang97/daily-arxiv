# Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence

**日期**: 2026-03-08  
**arXiv**: [2603.07660](https://arxiv.org/abs/2603.07660)  
**代码**: [GitHub](https://github.com/Visionary-Laboratory/Holi-Spatial)  
**领域**: 3D视觉  
**关键词**: spatial intelligence, 3D dataset, 3DGS, video annotation, VLM fine-tuning

## 一句话总结
提出 Holi-Spatial，首个全自动从原始视频生成大规模 3D 空间标注的 pipeline——三阶段流程（几何优化→图像级感知→场景级精炼）构建 Holi-Spatial-4M 数据集（12K 场景、320K 3D 框、1.2M 空间 QA），用于微调 VLM 提升空间推理能力，在 ScanNet++ 上 3D grounding AP50 提升 15%。

## 研究背景与动机

1. **领域现状**: 空间智能要求大模型从 2D 视觉理解扩展到 3D 空间感知。现有方法依赖少量人工标注的 3D 数据集（如 ScanNet ~1500 场景）构造 QA 对。

2. **现有痛点**: (a) 人工 3D 标注成本极高，数据量远不及 2D（LAION 10 亿 vs ScanNet 千级别）；(b) 小规模数据集导致严重的领域偏差；(c) 点云方法依赖 3D 传感器，feed-forward 方法精度不足。

3. **核心 idea**: 利用 AI 工具链（Depth-Anything-V3 + 3DGS + SAM3 + Gemini3-Pro）组成全自动 pipeline，从网络视频生成高质量 3D 空间标注，标注质量甚至超越人工标注。

## 方法详解

### 整体框架
原始视频 → SfM 相机恢复 → 3DGS 几何优化 → 关键帧采样 → VLM 分类 + SAM3 分割 → 深度投影到 3D → 跨视图合并 → VLM 过滤和描述 → 生成 3D 框/grounding/QA 对。

### 关键设计

1. **几何优化阶段**:
   - Depth-Anything-V3 初始化单目深度 → 3DGS 逐场景优化
   - 几何正则化确保多视图深度一致性
   - 消除 floater 噪声，获得与物理表面对齐的干净场景表示

2. **图像级感知**:
   - 均匀采样关键帧 → Gemini3-Pro 生成开放词汇类别
   - 维护动态类别标签记忆 $\mathcal{M}_t$ 确保语义一致性
   - SAM3 按类别引导生成高质量 2D 实例分割

3. **场景级 Lift 和精炼**:
   - 2D 掩码 → 深度投影 → 3D 点云 → 初始 3D OBB
   - 4 步去噪策略：掩码腐蚀 + mesh 深度指导过滤 + 跨视图 IoU 合并 + VLM 置信度过滤
   - 合并后的实例生成 caption + grounding + 空间 QA 对

4. **Holi-Spatial-4M 数据集**:
   - 来源：ScanNet + ScanNet++ + DL3DV-10K
   - 12K 优化 3DGS 场景，1.3M 2D 掩码，320K 3D 框，1.2M 空间 QA
   - 标注质量超越 ScanNet 官方标注（更准确的分割边界 + 更全的类别覆盖）

## 实验关键数据

### 主实验

| 任务 | 基线 | 微调后 | 提升 |
|------|------|--------|------|
| ScanNet++ 3D Grounding AP50 | 前方法 | Qwen3-VL + Holi-Spatial | **+15%** |
| MMSI-Bench 空间推理 | 前方法 | Qwen3-VL + Holi-Spatial | **+7.9%** |
| ScanNet 多视图深度 F1 | 前方法 | Holi-Spatial pipeline | **+0.5** |
| ScanNet 3D Detection AP50 | 前方法 | Holi-Spatial pipeline | **+64%** |

### 消融实验

| 配置 | 效果 |
|------|------|
| w/o 3DGS 几何优化 | 深度噪声大，3D 框质量差 |
| w/o 掩码腐蚀 + 深度过滤 | 边界不准，误检增多 |
| w/o VLM 过滤 | 低置信度实例引入噪声 |
| 手动标注 vs Holi-Spatial | Holi-Spatial 边界更清晰 |

### 关键发现
- Holi-Spatial 的自动标注在 ScanNet 上甚至超越官方人工标注（mask 边界更清晰、类别覆盖更广）
- 3DGS 几何优化 vs feed-forward 深度：前者大幅降低 floater，对 3D 框精度至关重要
- 数据规模效应显著——1.2M QA 对的训练量对 VLM 空间推理能力提升显著

## 亮点与洞察
- **AI 工具链自动化标注超越人类**: 组合多个 SOTA 工具（VLM + SAM3 + 3DGS）实现 pipeline，标注质量超人工
- **数据飞轮范式**: 不再依赖昂贵人工标注，而是从网络视频自动生成——可持续扩展
- **统一多任务框架**: 一个 pipeline 同时输出深度/分割/检测/grounding/QA，避免多任务割裂

## 局限性 / 可改进方向
- 依赖 SfM 相机恢复 → 纹理缺乏或运动模糊的视频可能失败
- 3DGS 逐场景优化耗时，大规模时成为瓶颈
- 开放词汇类别由 VLM 决定，可能遗漏罕见物体

## 相关工作与启发
- **vs SpatialLM/LLaVA-3D**: 需要点云输入，依赖 3D 传感器；Holi-Spatial 仅需视频
- **vs M3-Spatial**: 类似的 3DGS + 语言特征方案，但 M3-Spatial 是逐场景训练；Holi-Spatial 是可扩展 pipeline
- **vs SenseNova-SI-800K**: 标注量更大但来源场景少（几千个 ScanNet 场景）；Holi-Spatial 场景更多样

## 评分
- 新颖性: ⭐⭐⭐⭐ 全自动 3D 标注 pipeline 的系统集成创新
- 实验充分度: ⭐⭐⭐⭐⭐ 多 benchmark + 标注质量对比 + VLM 下游验证
- 写作质量: ⭐⭐⭐⭐ 系统性强，pipeline 图清晰
- 价值: ⭐⭐⭐⭐⭐ 空间智能数据瓶颈的重要解法
