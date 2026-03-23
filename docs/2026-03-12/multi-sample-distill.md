# Beyond Single-Sample: Reliable Multi-Sample Distillation for Video Understanding

**日期**: 2026-03-12  
**arXiv**: [2603.11423](https://arxiv.org/abs/2603.11423)  
**代码**: 无  
**领域**: 视频理解 / 知识蒸馏  
**关键词**: knowledge distillation, video LVLM, multi-sample, teacher variance, adversarial

## 一句话总结
提出 R-MSD（Reliable Multi-Sample Distillation），针对视频 LVLM 蒸馏中教师采样方差导致的监督噪声问题，通过多样本质量感知信号匹配（每输入 K 个教师响应 + 任务自适应质量评估）+ 在线 critic 对抗蒸馏，4B 学生模型在 VideoMME 上 +1.5%、Video-MMMU +3.2%、MathVerse +3.6%。

## 研究背景与动机

1. **领域现状**: 将大型视频 LVLM 蒸馏到小模型是实用化关键，但标准蒸馏假设教师输出确定，忽略了教师解码的随机性。

2. **核心矛盾**: 教师模型对同一输入多次采样会产生不同质量的响应（全局 σ=0.22，任务特定 σ=0.29），单样本蒸馏将高噪声监督直接传给学生。

3. **核心 idea**: 从教师的多次采样中选择质量最优的样本做监督，并用对抗机制进一步过滤噪声。

## 方法详解

### 关键设计

1. **Multi-Sample Quality-Aware Pairing**: 每个输入获取 K 个教师响应，按任务类型自适应评估质量（有 GT 的闭合题用 GT 匹配，开放题用均匀加权）
2. **Adversarial Distillation with Online Critic**: 在线训练一个 critic 模型评估师生响应，用对抗信号过滤低质量监督
3. **格式违反处理**: 识别并过滤教师输出的格式违反（全局 1%，任务特定 3.5%）

## 实验关键数据

| Benchmark | 基线 4B | R-MSD 4B | 提升 |
|-----------|---------|----------|------|
| VideoMME | 63.8 | **65.3** | +1.5% |
| Video-MMMU | 55.4 | **58.6** | +3.2% |
| MathVerse | 45.6 | **49.2** | +3.6% |

### 关键发现
- 教师采样方差是蒸馏性能的关键瓶颈
- 多样本 + 质量感知匹配比简单取最高概率更有效
- 对抗蒸馏进一步提升了鲁棒性

## 亮点与洞察
- 首次系统量化了教师解码方差对蒸馏质量的影响
- 质量感知的多样本匹配是简单但有效的改进

## 评分
- 新颖性: ⭐⭐⭐⭐ 多样本蒸馏视角新颖
- 实验充分度: ⭐⭐⭐⭐ 多 benchmark 验证
- 价值: ⭐⭐⭐⭐ 对 LVLM 蒸馏实践有直接指导
