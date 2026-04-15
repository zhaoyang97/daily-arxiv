# GeoFusion-CAD: Structure-Aware Diffusion with Geometric State Space for Parametric 3D Design

**日期**: 2026-03-23  
**arXiv**: [2603.21978](https://arxiv.org/abs/2603.21978)  
**代码**: 即将发布 (GitHub)  
**领域**: 模型压缩 / CAD生成  
**关键词**: parametric CAD, diffusion model, state-space model, Mamba, long sequence generation

## 一句话总结
提出 GeoFusion-CAD，用层次化树结构编码 CAD 程序（联合捕获几何和拓扑信息），通过 G-Mamba 扩散编码器以线性时间复杂度 $O(Ld)$ 建模长程结构依赖，配合新构建的 DeepCAD-240 基准（序列长度 40-240），在长 CAD 序列生成上大幅超越 Transformer 方法，且保持高几何保真度和拓扑一致性。

## 研究背景与动机

1. **领域现状**: 参数化 CAD 生成主要分 Sketch-Extrusion（SE，过程化建模）和 B-Rep（边界表示）两种范式。Transformer 因自注意力的长程依赖建模能力占主导地位，代表方法有 DeepCAD、SkexGen、MultiCAD、BrepGen 等。

2. **现有痛点**: (i) Transformer 的 $O(L^2 d)$ 二次复杂度在 CAD 序列扩展到数百命令时开销爆炸；(ii) 为绕过长序列问题，现有方法只能分段训练（短片段）或在潜空间分阶段训练，破坏端到端优化导致特征对齐损失；(iii) 全局注意力平等对待所有 token，忽略 CAD 数据的层次化组织——sketch、face、edge、vertex 之间有严格的拓扑依赖关系，但统一注意力稀释了这些局部约束。

3. **核心矛盾**: CAD 程序是高度层次化和结构化的（根→sketch/extrusion→face→edge→vertex），但 Transformer 把所有 token 拍平处理，既丢失结构先验又在长序列上计算爆炸。Mamba（SSM）虽然线性复杂度，但刚性顺序扫描不适合层次化拓扑依赖建模。

4. **切入角度**: 设计 G-Mamba——将 Mamba 的选择性状态转移与几何层次感知融合，在线性时间内建模 CAD 的层次化长程依赖。配合扩散过程做端到端稳定训练。

5. **核心 idea**: 层次化树表示（保留 CAD 几何+拓扑结构）+ G-Mamba 扩散编码器（线性时间建模长程依赖）+ 端到端扩散训练 = 可扩展的结构感知 CAD 生成。

## 方法详解

### 整体框架
CAD 程序 → 层次化树表示（根=实体，三层：操作/面 → 边/拉伸 → 顶点）→ 两个嵌入层 + G-Mamba 扩散编码器 + CAD 解码器。父节点条件化子节点的逆扩散过程。

### 关键设计

1. **层次化树表示**:
    - 做什么：将 SE-CAD 程序编码为层次树——根节点 = 整体实体，子节点 = sketch/extrusion 操作
    - 三层结构：操作/面 → 边/拉伸深度 → 顶点
    - 终止符 $e_c, e_l, e_f, e_s$ 标记曲线/环/面/sketch 的边界
    - 关键优势：保持连接关系无重复节点——不同于 BrepGen 需要复制节点表示共享边
    - Sketch 表示：每条曲线由 2D 坐标 $(p_x, p_y)$ 的 token 序列编码
    - Extrusion 表示：方向角 $(\theta, \phi, \gamma)$、平移 $(\tau_x, \tau_y, \tau_z)$、缩放 $\sigma$、拉伸距离 $(d_+, d_-)$、类型 $\beta$

2. **G-Mamba 扩散编码器**:
    - 做什么：在线性时间 $O(Ld)$ 内建模长程结构依赖（vs Transformer 的 $O(L^2 d)$）
    - 核心思路：选择性状态转移（selective state transitions）——根据输入动态调整状态更新，而非 Mamba 的刚性顺序扫描
    - 几何感知：融合局部几何和全局拓扑到统一潜空间
    - 扩散训练：去噪扩散目标保证稳定优化和长序列泛化

3. **条件化生成**:
    - 父节点条件化子节点：在逆扩散过程中，每个父节点的表示作为条件引导其子节点的去噪
    - 实现结构化、连贯的层次生成

### DeepCAD-240 基准
- 基于原始 DeepCAD 数据集扩展，序列长度从原来的 ≤60 扩展到 40-240
- 保留 sketch-extrusion 语义的同时引入更复杂的层次依赖
- 从 ABC 数据集提取，保留原始 tokenization 协议
- 提供更具挑战性的长程依赖评测场景

## 实验关键数据

### 短序列（DeepCAD 原始，≤60 步）

| 方法 | 性能 | 说明 |
|------|------|------|
| DeepCAD | 基线 | Transformer autoregressive |
| SkexGen | 优于 DeepCAD | 分阶段 Transformer |
| BrepGen | 扩散但长程退化 | 多阶段训练 |
| **GeoFusion-CAD** | **SOTA** | 端到端扩散 + G-Mamba |

### 长序列（DeepCAD-240，100-240 步）

| 方法 | 表现 | 说明 |
|------|------|------|
| Transformer-based | **严重退化** | 二次复杂度 + 缺乏层次感知 |
| **GeoFusion-CAD** | **保持高保真** | 线性复杂度 + 结构感知 |

### 关键发现
- 短序列上 GeoFusion-CAD 已超越 Transformer 基线——G-Mamba 的层次感知即使在短序列也有优势
- 长序列上差距更加明显：Transformer 在 >100 步时几何保真度和拓扑一致性急剧退化，GeoFusion-CAD 保持稳定
- 线性复杂度带来的效率提升：在 240 步序列上内存和时间远低于 Transformer
- 层次化树表示的无重复节点设计保持了更紧凑的序列长度

## 亮点与洞察
- **Mamba 在 CAD 的首次成功应用**: G-Mamba 证明 SSM 可以被改造为支持层次化拓扑依赖的模型，而不仅是平坦序列
- **层次化树+扩散的结合**: 扩散保证训练稳定，树结构保证层次感知——两者互补解决端到端长序列生成问题
- **DeepCAD-240 新基准**: 为长序列 CAD 生成提供标准化评测，揭示现有方法的长度瓶颈
- **与语言模型的类比**: CAD as Language 范式的深化——用更高效的序列模型（SSM 替代 Transformer）处理"CAD 语言"

## 局限性 / 可改进方向
- 仅验证 Sketch-Extrusion 范式，B-Rep 生成未覆盖
- 条件生成（如从图像/文本生成 CAD）未探索
- 评测指标较传统（几何保真度、拓扑一致性），缺乏设计意图保留的评估
- G-Mamba 的选择性状态转移机制具体如何适配 CAD 层次结构需更详细的可视化分析

## 相关工作与启发
- **vs DeepCAD**: Transformer 自回归，二次复杂度限制序列长度
- **vs BrepGen**: 扩散 + B-Rep 表示，但多阶段训练限制端到端优化
- **vs Mamba (vanilla)**: 刚性顺序扫描不感知层次结构，G-Mamba 通过几何感知状态转移解决

## 评分
- 新颖性: ⭐⭐⭐⭐ SSM 在 CAD 生成中的新应用，层次化+扩散设计精巧
- 实验充分度: ⭐⭐⭐⭐ 短/长序列完整对比，新建 DeepCAD-240 基准
- 写作质量: ⭐⭐⭐⭐ 架构图清晰，层次表示直观
- 价值: ⭐⭐⭐⭐ 对可扩展 CAD 生成和 SSM 在结构化序列中的应用有重要意义

