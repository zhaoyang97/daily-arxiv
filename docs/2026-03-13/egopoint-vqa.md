# Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering

**日期**: 2026-03-13  
**arXiv**: [2603.12533](https://arxiv.org/abs/2603.12533)  
**代码**: [EgoPointVQA](https://yuuraa.github.io/papers/choi2026egovqa)  
**领域**: 视频理解 / 第一人称视觉  
**关键词**: egocentric VQA, pointing gesture, hand intent tokens, deictic reasoning, MLLM

## 一句话总结
提出 EgoPointVQA 数据集（4000 合成+400 真实视频）和 HINT（Hand Intent Tokens）方法——将 3D 手部关键点编码为手势意图 token 并交织进 MLLM 输入，HINT-14B 在 6 类指示推理任务上以 68.1% 准确率超越 InternVL3-14B 6.6%。

## 研究背景与动机

1. **领域现状**: 第一人称 AI 助手（AR/VR、智能眼镜）需要理解用户注意力和指示手势。MLLM 在通用视觉上表现优异，但无法理解"这个是什么？"等需要手势才能解答的问题。

2. **现有痛点**: 即使 GPT-4o 和 Qwen3-VL-32B 也无法正确解析指示手势，因为训练数据缺乏手势丰富的视频，架构上也没有显式编码手部姿态的机制。

3. **核心 idea**: 用现成 3D 手部重建模型提取关键点 → 轻量适配器转为帧对齐的手势意图 token → 交织进视觉 token 序列中。

## 方法详解

### EgoPointVQA 数据集
- 4000 合成 + 400 真实第一人称视频，6 类任务：引用识别、计数、空间、时序、属性、功能反馈
- 672 个 QA 对用于评测

### HINT（Hand Intent Tokens）
- 3D 手部关键点 → MLP 编码器 → 36 个手势 token/帧 + 2D 正弦余弦位置编码
- 与对应帧的视觉 token 交织（非简单拼接在末尾）
- MLLM 自由交叉注意手势、视觉、文本 token

## 实验关键数据

| 模型 | 平均准确率 |
|------|-----------|
| InternVL3-14B | 61.5% |
| **HINT-14B** | **68.1%** (+6.6%) |
| 标准微调 | 61.6% |

### 关键发现
- 手势 token 比无 token 的标准微调高 6.5%——显式手势编码是必要的
- 3D 关键点比 2D 关键点更好——深度信息对指示方向判断很重要

## 亮点与洞察
- 填补了指示手势 + 第一人称 VQA 的空白——现有工作要么给定显式区域标注，要么不处理手势
- **隐式推断指示目标**比显式标注更符合真实场景

## 局限性 / 可改进方向
- 3D 手部重建依赖现成模型质量，复杂场景可能不准
- 仅支持指示手势，抓取/挥手等其他手势未涉及
- 合成数据可能存在域差距

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个指示手势第一人称 VQA benchmark + token 化手势方案
- 实验充分度: ⭐⭐⭐⭐ 多任务评测+消融+多规模模型
- 价值: ⭐⭐⭐⭐ 对 AR/VR 助手交互具有直接应用价值
