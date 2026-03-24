# Do World Action Models Generalize Better than VLAs? A Robustness Study

**日期**: 2026-03-23  
**arXiv**: [2603.22078](https://arxiv.org/abs/2603.22078)  
**代码**: 无  
**领域**: 机器人 / 世界模型  
**关键词**: world action model, VLA, robustness, visual perturbation, robot manipulation

## 一句话总结
系统对比 SOTA VLA 策略（π0.5、OpenVLA 等）和新兴的世界动作模型 WAM（Cosmos-Policy、LingBot-VA 等）在视觉/语言扰动下的鲁棒性，发现 WAM 凭借视频预训练获得的时空先验在噪声/光照/布局扰动下表现更好（LingBot-VA 74.2%、Cosmos-Policy 82.2%），但推理延迟高于 VLA 4.8 倍以上。

## 研究背景与动机

1. **领域现状**: VLA（Vision-Language-Action）模型通过将视觉-语言大模型适配到机器人动作生成，在多种任务上表现出色。WAM（World Action Models）则基于视频生成模型的潜表示解码动作，是新兴替代方案。

2. **现有痛点**: VLA 性能受训练数据范围限制，对未见场景泛化差，对视觉/语言扰动脆弱。WAM 声称视频预训练带来的时空先验使其泛化更好，但缺乏系统对比验证。

3. **核心矛盾**: VLM backbone 可能已隐式建模世界动力学，WAM 显式的动态预测是否真有必要？视频先验的优势在哪些扰动类型下体现？

4. **切入角度**: 在两个增强操作基准（LIBERO-Plus 单臂 + RoboTwin 2.0-Plus 双臂）上，系统评测多种视觉和语言扰动下的策略鲁棒性。

5. **核心 idea**: 通过受控扰动实验系统揭示 WAM vs VLA 的鲁棒性差异及其根源。

## 方法详解

### 评测框架
- **LIBERO-Plus**: 7 种扰动类型的单臂操作任务
- **RoboTwin 2.0-Plus**: 类似扰动协议的双臂 Aloha-Agilex 设置
- 扰动类型：噪声、光照变化、布局更改、背景干扰、语言改述等

### 评测模型

**VLA 系列**: π0.5、OpenVLA-OFT、X-VLA、SimpleVLA-RL
**WAM 系列**: VPP (SVD-based)、Genie-Act (LTX-Video)、Cosmos-Policy (Cosmos-Predict2)、LingBot-VA (Wan2.2-5B)、DreamZero (Wan2.1-14B)
**混合方法**: MOTUS、VLA-JEPA（部分集成视频动态学习）

### WAM 架构特征
- 基于视频扩散/flow matching 模型 backbone
- 轻量级动作头从潜表示解码 robot actions
- 支持自回归生成（LingBot-VA、DreamZero）或联合去噪（Cosmos-Policy）
- 参数量 1.5B-14B

## 实验关键数据

### 鲁棒性对比

| 模型 | 类型 | RoboTwin 2.0-Plus | LIBERO-Plus |
|------|------|-------------------|-------------|
| LingBot-VA | WAM | **74.2%** | - |
| Cosmos-Policy | WAM | - | **82.2%** |
| π0.5 | VLA | 可比但需更多数据 | 可比 |
| MOTUS | 混合 | 中等 | 中等 |

### 推理效率

| 模型 | 推理速度对比 |
|------|-------------|
| WAM 最快 | ≥4.8× 慢于 π0.5 |
| π0.5 (VLA) | baseline |

### 关键发现
- WAM 在噪声、光照、布局扰动下普遍更鲁棒——时空先验从视频预训练继承
- π0.5 等 VLA 可达到可比鲁棒性，但需要精心策划的多样化数据集和多种学习目标
- WAM 的优势在于 policy 训练阶段简单（无需大规模多任务 robot 数据预训练）
- WAM 的劣势：推理开销大（≥4.8× 慢），限制实际部署
- 混合方法（部分集成视频先验）鲁棒性介于两者之间——视频先验的集成方式很重要
- 模型更大不一定更鲁棒，"thinking"模式不一定更安全

## 亮点与洞察
- **首个 WAM vs VLA 系统鲁棒性对比**: 填补了两类范式在受控扰动下的对比空白
- **视频先验的价值明确化**: WAM 的鲁棒性增益主要来自视频预训练的时空先验，而非架构本身
- **训练简单 vs 推理高效的 trade-off**: WAM 训练简单但推理贵，VLA 训练数据需求大但推理快

## 局限性 / 可改进方向
- 仅在模拟环境测试，真实世界扰动（机械噪声、传感器退化）未覆盖
- WAM 推理延迟问题未提出解决方案
- 扰动类型有限，未测试对抗性扰动
- 混合方法的最优集成策略尚不明确

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个系统对比研究，及时且有洞察
- 实验充分度: ⭐⭐⭐⭐ 两个基准多种扰动，覆盖 VLA/WAM/混合
- 写作质量: ⭐⭐⭐⭐ 分类清晰，相关工作全面
- 价值: ⭐⭐⭐⭐ 对 embodied AI 方向选择有重要参考
