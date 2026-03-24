# Mamba Learns in Context: Structure-Aware Domain Generalization for Multi-Task Point Cloud Understanding

**日期**: 2026-03-21  
**arXiv**: [2603.20739](https://arxiv.org/abs/2603.20739)  
**代码**: [GitHub](https://github.com/Jinec98/SADG)  
**领域**: 3D视觉  
**关键词**: Mamba, point cloud, domain generalization, structure-aware serialization, in-context learning

## 一句话总结
提出 SADG，首个基于 Mamba 的多任务点云域泛化框架，通过质心距离谱(CDS)和测地线曲率谱(GCS)实现变换不变的结构感知序列化，配合层级域感知建模和谱图对齐，在重建/去噪/配准三任务上全面超越 SOTA（含引入新数据集 MP3DObject）。

## 研究背景与动机

1. **领域现状**: 3D 点云理解的 Transformer 方法（PointBERT 等）具备全局推理能力但复杂度 $O(n^2)$；Mamba 提供线性时间序列建模但依赖坐标驱动序列化。

2. **现有痛点**: (a) 现有方法主要面向单任务单域，直接应用到多任务域泛化时性能下降；(b) Mamba 的坐标序列化（轴扫描、Hilbert 曲线）对视角变化和缺失区域敏感，破坏层级结构；(c) DG-PIC 用 Transformer 做多任务域泛化但计算昂贵且缺乏显式序列。

3. **核心 idea**: 用内在几何性质（质心拓扑 + 测地线曲率）替代坐标驱动序列化，使 Mamba 的循环状态传播反映物体的层级结构而非坐标位置，实现变换不变的稳定建模。

## 方法详解

### 整体框架
输入点云 → FPS+KNN 分 patch → 结构感知序列化（CDS+GCS 双谱双向） → 层级域感知建模（域内结构 + 域间融合） → 测试时谱图对齐。三个任务（重建、去噪、配准）统一在 ICL 框架下。

### 关键设计

1. **质心距离谱（CDS）序列化**:
   - 构建 token 图，亲和力 $w(i,j) = \exp(-\|u_i-u_j\|^2/\sigma^2)$
   - 从最近质心的 token 开始 BFS 遍历，按亲和力排序邻居
   - 平衡全局覆盖和局部连续性——比单纯按距离排序多了空间平滑约束
   - 变换不变：基于内在距离而非绝对坐标

2. **测地线曲率谱（GCS）序列化**:
   - 计算测地线距离（KNN 图上的最短路径），构建 Laplace-Beltrami 算子
   - 热核扩散 $K_\tau(i,i)$ 隐式编码局部曲率——高曲率区域热耗散快
   - 多尺度曲率描述子 $h_i = [K_{\tau_1}(i,i), ..., K_{\tau_S}(i,i)]$
   - 从最低曲率 token 开始按曲率升序遍历，保持几何平滑性
   - 避免显式法向量估计在噪声/缺失下的脆弱性

3. **层级域感知建模（HDM）**:
   - **域内结构建模（ISM）**: prompt 域和 query 域各自独立过 Mamba，保持域内结构一致性
   - **域间关系融合（IRF）**: 按共享结构序交错排列两域 token $[z^p_1, z^q_1, z^p_2, z^q_2, ...]$，共享 Mamba 联合建模
   - 交错排列比直接拼接更好——通过循环传播隐式交换特征

4. **谱图对齐（SGA，测试时）**:
   - 将序列化目标特征视为图信号，在谱域对齐到源域原型
   - 无需更新模型参数，轻量级测试时自适应

### 统一序列
双谱双向拼接：$X_{seq} = [X_{\pi_{CDS}}; X_{rev}; X_{\pi_{GCS}}; X_{rev}]$，Mamba 线性效率不变。

## 实验关键数据

### 主实验（Chamfer Distance ×10⁻³，越低越好）

五域 leave-one-out：ModelNet, ShapeNet, ScanNet, ScanObjectNN, MP3DObject

| 方法 | ModelNet Rec. | ShapeNet Den. | ScanObjectNN Reg. | MP3DObject Avg |
|------|--------------|---------------|-------------------|----------------|
| DG-PIC (Transformer) | — | — | — | 基线 |
| SADG (Mamba) | 显著优于所有方法 | — | — | SOTA |

### 消融实验

| 配置 | 重建 CD | 去噪 CD | 配准 CD |
|------|---------|---------|---------|
| 坐标排序 | 较差 | 较差 | 较差 |
| CDS only | 改善 | 改善 | 改善 |
| CDS + GCS | 最优 | 最优 | 最优 |
| w/o HDM | 下降 | 下降 | 下降 |
| w/o SGA | 下降 | — | 下降 |

### 关键发现
- 结构感知序列化对 Mamba 的域泛化至关重要——坐标排序在域偏移下不稳定
- CDS 贡献全局拓扑，GCS 贡献局部几何，两者互补
- 交错域间融合优于直接拼接——避免了序列边界的不连续性

## 亮点与洞察
- **内在几何序列化**思路优雅：用热扩散隐式编码曲率避免了显式法向量的噪声敏感问题
- **Mamba + ICL 的首次结合**在点云域泛化中实现，证明线性复杂度模型可替代 Transformer
- 谱图对齐作为免训练测试时自适应方法值得借鉴

## 局限性 / 可改进方向
- BFS 遍历和热核计算引入额外预处理开销，具体延时未报告
- 仅验证三个任务（重建/去噪/配准），分类和分割等语义任务未覆盖
- MP3DObject 数据集规模和难度有待社区验证

## 评分
- 新颖性: ⭐⭐⭐⭐⭐ 结构感知序列化 + Mamba ICL 的融合是首创
- 实验充分度: ⭐⭐⭐⭐ 五域三任务全面评估，消融充分
- 价值: ⭐⭐⭐⭐ 为 Mamba 在 3D 域泛化开辟新方向
