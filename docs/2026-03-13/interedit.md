# InterEdit: Navigating Text-Guided Multi-Human 3D Motion Editing

**日期**: 2026-03-13  
**arXiv**: [2603.13082](https://arxiv.org/abs/2603.13082)  
**代码**: [InterEdit](https://github.com/YNG916/InterEdit)  
**领域**: 图像生成 / 3D动作  
**关键词**: multi-person motion editing, diffusion model, interaction-aware, frequency alignment, TMME

## 一句话总结
提出多人 3D 动作编辑任务（TMME）、InterEdit3D 数据集（5161 个源-目标-指令三元组）和 InterEdit 模型——通过语义感知计划 token 对齐 + 交互感知频率 token 对齐（DCT 能量池化），实现精确的文本指导双人动作编辑，在 TMME 上达到 SOTA。

## 研究背景与动机
- 单人文本引导动作编辑已有进展，但多人交互编辑未被探索
- 挑战：交互语义源自相对时序和配置（同步、角色切换、接触时机），微小修改可能破坏协调性
- 缺乏配对的多人动作编辑数据和 benchmark

## 方法详解

### InterEdit3D 数据集
- 基于 InterHuman 构建，半自动检索+标注管线
- 5161 个源-目标-文本三元组，强调空间/时间/协调层面的编辑

### InterEdit 模型
1. **语义感知计划 Token 对齐**: 可学习计划 token 对齐到预训练运动教师嵌入，捕获高层交互线索
2. **交互感知频率 Token 对齐**: 对平均/差分交互信号做 DCT → 频带能量描述子 → 频率控制 token，监督回归目标频带能量 → 保持交互节奏和同步
3. **无分类器条件扩散**: 同步去噪双人动作

## 关键发现
- 双 token 对齐策略比单独使用语义或频率对齐都更好
- 频率对齐对保持交互同步性至关重要

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个多人动作编辑任务+数据集+方法
- 实验充分度: ⭐⭐⭐⭐ 多基线对比（单人编辑+多人生成方法改造）
- 价值: ⭐⭐⭐⭐ 对游戏/动画/社交机器人等应用有直接价值
