# FOCUS: Bridging Fine-Grained Recognition and Open-World Discovery across Domains

**日期**: 2026-03-15  
**arXiv**: [2603.14240](https://arxiv.org/abs/2603.14240)  
**领域**: 目标检测 / 域泛化  
**关键词**: generalized category discovery, domain generalization, fine-grained recognition, part discovery, uncertainty

## 一句话总结
首次定义 Fine-Grained Domain-Generalized GCD (FG-DG-GCD) 问题，提出 FoCUS 框架结合 Domain-Consistent Parts Discovery (DCPD) 和 Uncertainty-Aware Feature Augmentation (UFA)，在 CUB/Cars/Aircraft 跨域细粒度基准上超越 GCD/FG-GCD/DG-GCD 基线 3-10%，计算效率提升 ~3×。

## 研究背景与动机

1. **领域现状**: GCD (Generalized Category Discovery) 要求识别已知类同时发现新类。但现有 GCD 假设标注和未标注数据同分布；DG-GCD 面对域偏移；在细粒度场景下类间差异微小+类内变化大，使域泛化更难。

2. **现有痛点**: FG-GCD 忽略域偏移，DG-GCD 忽略细粒度挑战。没有统一框架同时处理细粒度+跨域+开放世界发现三重难题。

3. **核心 idea**: DCPD 通过几何稳定的 part reasoning 建立跨域一致的局部特征表示；UFA 通过不确定性引导的特征扰动实现正则化，增强模型对域变化的鲁棒性。

## 方法详解

### 整体框架
输入图像 → DCPD（发现域一致的部件区域）→ 部件级特征提取 → UFA（不确定性引导特征增强）→ 分类+聚类（已知类识别+新类发现）。单阶段框架，避免多阶段方法的冗余。

### 关键设计

1. **Domain-Consistent Parts Discovery (DCPD)**:
   - 做什么：在跨域场景中发现语义一致的物体部件区域（如鸟的头、翅膀、尾巴）
   - 核心思路：利用几何稳定性约束——同一物种的部件结构在不同域（真实照片 vs 油画 vs 素描）中保持一致
   - 设计动机：细粒度识别的关键在于局部部件差异（如鸟喙形状）而非全局外观（如背景颜色）
   - 用 diffusion-adapter 控制生成 painting/sketch 域变体，保证部件位置不变

2. **Uncertainty-Aware Feature Augmentation (UFA)**:
   - 做什么：通过置信度引导的特征扰动增强泛化能力
   - 核心思路：对高不确定性区域施加更大扰动，鼓励模型学习更鲁棒的决策边界
   - 设计动机：域偏移主要影响模型不确信的区域，针对性增强比全局增强更有效
   - 扰动强度与预测不确定性成正比，避免对已确信的特征造成不必要干扰

3. **FG-DG-GCD 基准构建**:
   - 做什么: 为 CUB-200-2011、Stanford Cars、FGVC-Aircraft 创建跨域变体
   - 方法: 用 diffusion-adapter 控制生成 painting 和 sketch 风格的同一物体图像
   - 保证身份一致性：同一只鸟在不同风格下仍可识别为同一品种

## 实验关键数据

### CUB/Cars/Aircraft 跨域细粒度基准

| 方法 | 设定 | 准确率提升 | 计算效率 |
|------|------|----------|----------|
| GCD baseline | 标准 GCD | 基线 | 1× |
| SimGCD | FG-GCD | 基线+ | 1× |
| PromptCAL | DG-GCD | 基线+ | ~2× |
| **FoCUS** | **FG-DG-GCD** | **+3.28% (GCD) / +9.68% (FG) / +2.07% (DG)** | **~3× 快** |

### 关键发现
- FG-GCD 设定下提升最大 (+9.68%)——说明 DCPD 的部件发现对细粒度识别贡献突出
- DG-GCD 设定提升 +2.07%——部件级特征对跨域泛化同样有效
- 计算效率提升 ~3×——单阶段框架避免了多阶段方法（先聚类再分类）的冗余
- 在新类发现任务上同样提升——部件级特征对未知类的判别同样有效
- 消融：去掉 DCPD 后 FG-GCD 提升从 9.68% 降到 ~3%，说明部件发现是核心贡献
- 消融：去掉 UFA 后 DG-GCD 提升从 2.07% 降到 ~1%，说明不确定性引导增强对跨域有效

## 亮点与洞察
- **三重挑战的统一框架**：首次将细粒度+域泛化+开放世界发现统一处理，问题定义本身有价值
- **部件级推理的域一致性**：利用物体结构的几何稳定性绕过域偏移——鸟的翅膀比例在照片和油画中基本一致
- **计算效率提升 3×**：单阶段框架避免了先聚类再分类的多阶段冗余
- **Diffusion-adapter 基准构建**：用可控生成创建跨域数据，保证身份一致性，方法论可复用

## 相关工作对比
- **vs 标准 GCD**: 假设同域同分布，域偏移下 clustering accuracy 下降 9.68%
- **vs DG-GCD**: 忽略细粒度挑战，FoCUS 在细粒度基准上提升 2.07% 且效率高 3x
- **vs FG-GCD**: 不考虑域偏移下掉点最严重（9.68%），域泛化在细粒度场景最关键
- **vs PartDiscover**: 通用部件发现无跨域一致性约束，DCPD 几何稳定性约束是核心改进


## 相关工作对比
- **vs 标准 GCD**: 假设同域同分布，域偏移下 clustering accuracy 下降 9.68%
- **vs DG-GCD**: 忽略细粒度挑战，FoCUS 在细粒度基准上提升 2.07% 且效率高 3x
- **vs FG-GCD**: 不考虑域偏移下掉点最严重（9.68%），域泛化在细粒度场景最关键
- **vs PartDiscover**: 通用部件发现无跨域一致性约束，DCPD 几何稳定性约束是核心改进


## 局限性 / 可改进方向
- 仅在 CUB/Cars/Aircraft 三个细粒度视觉基准验证，更多领域（如医学图像、工业质检）泛化待测
- 部件发现依赖于物体具有明确的可分解结构，对非刚体/抽象类别可能不适用
- 新类别发现的数量和粒度如何影响性能未深入分析——open-world setting 的类别数量先验敏感性未测
- 跨域变体由 diffusion-adapter 生成——生成图像与真实域偏移（如不同相机、不同地区）的差距可能影响结论
- UFA 的不确定性估计质量对增强效果有直接影响，校准不良时可能适得其反

## 相关工作与启发
- **vs SimGCD**: 标准 FG-GCD，不考虑域偏移——在跨域场景性能大幅下降
- **vs PromptCAL**: DG-GCD 方法，但不处理细粒度——在 fine-grained 设定下表现不佳
- **vs DINO-based part discovery**: 无监督部件发现，但没有域一致性约束

## 评分
- 新颖性: ⭐⭐⭐⭐ 首次定义 FG-DG-GCD 问题
- 实验充分度: ⭐⭐⭐⭐ 多基线多数据集对比
- 价值: ⭐⭐⭐⭐ 推动开放世界识别向真实部署场景前进

---
