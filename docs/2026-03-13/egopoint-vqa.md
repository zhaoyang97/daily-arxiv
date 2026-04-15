# Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering

**日期**: 2026-03-13  
**arXiv**: [2603.12533](https://arxiv.org/abs/2603.12533)  
**代码**: [EgoPointVQA](https://yuuraa.github.io/papers/choi2026egovqa)  
**领域**: 视频理解 / 第一人称视觉  
**关键词**: egocentric VQA, pointing gesture, hand intent tokens, deictic reasoning, MLLM

## 一句话总结
提出 EgoPointVQA 数据集（4000 合成+400 真实视频，18745 QA 对）和 HINT（Hand Intent Tokens）方法——将 3D 手部关键点编码为手势意图 token 并交织进 MLLM 输入，HINT-14B 在 6 类指示推理任务上以 68.1% 准确率超越 InternVL3-14B 5.4%（+6.6% vs InternVL3-14B 的 62.7%）。

## 研究背景与动机
1. **交互需求**: 第一人称 AI 助手（AR/VR、智能眼镜如 Meta Ray-Ban）需要理解用户指示手势和指示表达（如"这个是什么？"）
2. **MLLM 的盲区**: GPT-4o 和 Qwen3-VL-32B 都无法正确解析指示手势——训练数据缺乏手势视频，架构缺乏手部姿态编码
3. **显式标注 vs 隐式推断**: 现有区域级 VQA 需要显式给定 bounding box/mask，但真实场景中用户的指向意图需要从手势隐式推断
4. **核心 idea**: 用现成 3D 手部重建模型提取关键点 → 轻量适配器转为手势意图 token → 交织进视觉 token 序列

## 方法详解

### EgoPointVQA 数据集
- **合成数据**: 4000 视频，AI2-THOR 模拟器（184 室内场景），MIXAMO 动画 + 逆运动学对齐指向
- **真实数据**: 400 视频，20 名参与者用 Meta Ray-Ban 智能眼镜录制（360 室内 + 40 户外）
- **6 类任务**: 引用识别(Reference)、计数(Counting)、空间(Spatial)、时序(Temporal)、属性(Attribute)、功能反馈(Feedback)
- **评测集**: 300 真实视频，672 QA 对，人工验证正确性和指示歧义性

### HINT（Hand Intent Tokens）
1. **3D 手部姿态提取**: WiLoR 模型输出每帧 21 个 3D 关键点 $K_t \in \mathbb{R}^{21 \times 3}$，3D 比 2D 好在提供深度信息用于判断指向方向
2. **Keypoint Adapter**: $K_t$ → flatten（63维）→ LayerNorm → MLP ($W_1 \in \mathbb{R}^{d_h \times 63}$, GeLU, $W_2 \in \mathbb{R}^{d \times d_h}$) → 手势意图 token $H_t$
3. **帧-关键点交织**: 每帧视觉 token $V_t$ 后接对应手势 token $H_t$（检测置信度 $c_t \geq 0.5$ 时才插入）
4. **联合推理**: $p(X_a|V,X_q,H) = \prod_i p(x_i|V,X_{q,<i},X_{a,<i},H_{<i})$，MLLM 通过自注意力同时处理视觉、手势、文本 token

## 实验关键数据

| 模型 | 参数 | Reference | Temporal | Spatial | Count | Attr. | Feed. | 平均 |
|------|------|-----------|----------|---------|-------|-------|-------|------|
| GPT-5 | — | 75.6 | 53.6 | 62.3 | 50.0 | 56.1 | 77.8 | 62.6 |
| InternVL3-78B | 78B | 71.4 | 71.4 | 62.3 | 45.8 | 68.3 | 80.1 | 66.6 |
| InternVL3-14B | 14B | 63.1 | 66.1 | 61.4 | 50.0 | 58.5 | 77.2 | 62.7 |
| **HINT-14B** | 14B | **73.8** | **69.6** | **64.9** | **54.2** | **63.4** | **82.5** | **68.1** |

| 消融 | 平均准确率 |
|------|-----------|
| InternVL3-8B baseline | 58.0% |
| InternVL3-8B + 标准微调 | ~58.0% |
| **HINT-8B** | **63.7%** (+5.7%) |
| **HINT-14B** | **68.1%** (+5.4% vs baseline) |

### 关键发现
- HINT 比无手势 token 的标准微调高 5-6%——显式手势编码是必要的，单纯微调不够
- 3D 关键点编码优于 2D——深度信息对指示方向判断关键
- 所有模型在 Counting 任务上最差（<55%），追踪多次指向仍是难点
- GPT-5 在 Reference 上 75.6% 最高，但 Temporal 骤降到 53.6%——多时序手势理解是根本瓶颈
- 交织式插入 vs 末尾拼接：交织式保持时序对齐，MLLM 能自然关联每帧的手势和视觉内容
- 即使是 78B InternVL3 也仅 66.6%，说明问题难度不只是规模能解决的

## 亮点与洞察
- 填补指示手势 + 第一人称 VQA 的空白——现有工作要么给定显式区域标注，要么不处理手势
- 交织式 token 插入使 MLLM 保持时序对齐，比末尾拼接更自然
- 轻量 Keypoint Adapter（两层 MLP + LayerNorm）设计表明：不需要复杂架构，关键是提供正确的信号

## 局限性 / 可改进方向
- 3D 手部重建依赖 WiLoR 质量，复杂遮挡和快速运动场景可能不准
- 仅支持指示手势，抓取/挥手/比划等其他手势类型未涉及
- 合成-真实域差距可能影响泛化——合成数据用 AI2-THOR 的室内场景，真实数据更多样
- Counting 和 Temporal 任务准确率仍低（<55%），需要更强的时序推理能力
- 评测集仅 672 QA 对，统计显著性可能有限

## 相关工作与启发
- **vs Artemis/Elysium（区域级视频 VQA）**: 这些工作假设区域已显式给定（bbox/mask），EgoPointVQA 需从手势隐式推断
- **vs EgoGPT**: EgoGPT 聚焦通用第一人称理解，单任务 Reference 67.3% 但平均仅 55.9%——HINT 的手势编码带来全面提升
- **vs Visual Prompting（SoM/alphanumeric tags）**: 人工视觉提示 vs 自然手势——HINT 不需要额外标注，更贴近真实交互场景

## 评分
- 新颖性: ⭐⭐⭐⭐ 首个指示手势第一人称 VQA benchmark + token 化手势方案
- 实验充分度: ⭐⭐⭐⭐ 15 个 baseline（含 GPT-5）+ 3 个 backbone 消融 + 6 类任务
- 价值: ⭐⭐⭐⭐ 对 AR/VR 助手交互具有直接应用价值
- 写作质量: ⭐⭐⭐⭐ 任务定义清晰，数据集构建流程规范

## 补充说明
- 数据集构建经过三阶段自动生成 + 人工质检，确保评测质量
- 合成数据使用 AI2-THOR（184 场景）+ MIXAMO 动画 + 逆运动学，质量较高
- 真实数据由 20 名参与者用 Meta Ray-Ban 智能眼镜录制，覆盖室内外多种场景
- HINT 对 LLaVA-OneVision 也有效（54.4% vs 49.9%），说明方法不限于特定 backbone
- 训练策略：LoRA 微调视觉编码器+LLM + Keypoint Adapter 从头训练，AdamW+cosine schedule，1 epoch
- QA 对生成使用 InternVL3-78B 作为标注 MLLM，GPT-4o 做最终的指示代词替换
