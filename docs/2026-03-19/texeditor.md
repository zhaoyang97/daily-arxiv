# TexEditor: Structure-Preserving Text-Driven Texture Editing

**日期**: 2026-03-19  
**arXiv**: [2603.18488](https://arxiv.org/abs/2603.18488)  
**代码**: [GitHub](https://github.com/KlingAIResearch/TexEditor)  
**领域**: 图像生成 / 图像编辑  
**关键词**: 纹理编辑, 结构保持, Blender合成数据, 强化学习, TexBench

## 一句话总结
提出 TexEditor，通过 Blender 合成的 TexBlender 数据集做 SFT 冷启动 + StructureNFT 强化学习（结合指令遵循和结构保持奖励）两阶段训练，在文本驱动纹理编辑中一致超越 Nano Banana Pro 等 SOTA 编辑模型，同时提出 TexBench（真实世界基准）和 TexEval（结合结构一致性的评估指标）。

## 研究背景与动机

1. **领域现状**: 文本驱动图像编辑快速发展（Stable Diffusion、Qwen-Image-Edit 等），但纹理编辑（只改外观不改几何）是未被充分解决的子问题。

2. **现有痛点**: 即使 SOTA 编辑模型（如 Nano Banana Pro），在纹理编辑时也经常不保持物体几何结构——本该只改"皮肤"却连"骨头"一起改了。原因：缺乏明确的结构保持训练信号，且无合适的纹理编辑评估基准。

3. **核心矛盾**: 纹理编辑需要精确解耦外观和几何——修改纹理属性（粗糙度、材质）同时保持物体形状、空间布局和语义身份不变。

4. **切入角度**: 从数据和训练两方面入手——用 Blender 合成几何不变的配对数据做冷启动，再用 RL + 结构保持 loss 泛化到真实场景。

## 方法详解

### 整体框架
基于 Qwen-Image-Edit-2509 的两阶段训练：
1. **SFT 阶段**：在 TexBlender 合成数据上微调，学习纹理编辑 + 结构保持
2. **RL 阶段**：在 COCO 真实图像上用 StructureNFT 强化学习，泛化到真实场景

### 关键设计

1. **TexBlender 合成数据集**:
   - 做什么：提供配对的（编辑前, 编辑后）图像，几何完全相同仅纹理变化
   - 核心思路：用 3D-Front 室内场景 + Blender 渲染，两种编辑模式：(a) 属性调整（粗糙度/金属度/透明度）通过 Principled BSDF shader；(b) 全局纹理替换（用 MatSynth 纹理）
   - 关键区别：不是单物体而是场景级，对物体组编辑（不同粒度），加入复杂背景和遮挡
   - 指令生成：记录纹理修改元数据 → Qwen3-VL 生成自然语言指令 → SAM3 视觉引导精化

2. **StructureNFT（结构感知 RL）**:
   - 做什么：在真实图像上通过 RL 平衡指令遵循和结构保持
   - 奖励函数：$Reward = Score_{ins} + Score_{struct}$
   - 指令奖励：$Score_{ins} = MLLM(I_e, I, P, P_{sys})$，用 Gemini 3 Flash 评分
   - 结构奖励：比较三种方案后选 SSIM on SAUGE wireframe
     - SAM3 mask IoU：太粗粒度
     - Wireframe IoU：对像素扰动过敏
     - **Wireframe SSIM**（最终选择）：$s = SSIM(SAUGE(I_e), SAUGE(I))$，对小位移鲁棒
   - 经验归一化：原始 SSIM 值范围窄，为纹理替换和属性编辑分别设 $\tau_{min}, \tau_{max}$ 做分段线性映射

3. **TexEval 评估指标**:
   - 做什么：联合评估指令遵循和结构保持
   - $TexEval = \alpha \cdot Score_{Ins} + (1-\alpha) \cdot Score_{struct}$
   - 500 对样本的人类偏好研究验证其与人类判断对齐度最高

## 实验关键数据

### TexBench 主实验

| 方法 | Texture TexEval↑ | Attribute TexEval↑ |
|------|-----------------|-------------------|
| Qwen-2509 (base) | 0.717 | 0.514 |
| Alchemist | 0.741 | 0.583 |
| Nano Banana Pro | **0.794** | 0.597 |
| **TexEditor** | 0.767 | **0.620** |
| **TexEditor-Pro** | **0.796** | **0.630** |

### 消融实验

| 配置 | TexEval |
|------|---------|
| Base (Qwen-2509) | 0.717 |
| + SFT (TexBlender) | 0.750 |
| + RL (指令 only) | 0.758 |
| + RL (指令 + 结构) | **0.767** |

### 关键发现
- SFT 冷启动提供了显著的结构保持先验（+0.033 TexEval）
- RL 阶段结构 loss 的加入进一步提升性能——仅用指令奖励的 RL 会忽视结构退化
- 在 ImgEdit 通用编辑基准的纹理子任务上，TexEditor 超越其基座模型 Qwen-2509

## 亮点与洞察
- **数据+训练双管齐下**：Blender 提供干净的结构保持监督信号 → SFT 学会"什么不该改"；RL 泛化到真实场景 → 学会"在复杂背景下也不改"
- **SAUGE wireframe + SSIM 做结构度量**：比语义级 SAM mask 更细粒度，比像素级 wireframe IoU 更鲁棒——这个组合可复用到其他结构保持任务
- **TexBench 填补空白**：首个基于真实图像的场景级纹理编辑基准，825 条样本覆盖属性编辑和纹理替换

## 局限性 / 可改进方向
- 合成数据与真实图像的 domain gap 仍存在——RL 阶段部分弥补但不完全
- 结构评估依赖 SAUGE 线框提取质量，某些纹理变化可能改变线框
- TexBench 规模有限（825 条），评测覆盖有限
- 归一化阈值基于经验设定，不是最优的

## 相关工作与启发
- **vs Alchemist**: 仅在 Blender 单物体场景上训练；TexEditor 扩展到场景级 + 真实场景 RL
- **vs Nano Banana Pro**: 商业 SOTA，在纹理替换上强但属性编辑上结构退化严重
- **vs DiffusionNFT**: TexEditor 基于此低成本 RL 框架，加入结构保持项

## 评分
- 新颖性: ⭐⭐⭐⭐ TexBlender + StructureNFT 的数据-训练联合方案设计巧妙
- 实验充分度: ⭐⭐⭐⭐ 消融全面，有泛化实验，但基准规模有限
- 写作质量: ⭐⭐⭐⭐ 问题定义清晰，训练流程图直观
- 价值: ⭐⭐⭐⭐ 对纹理编辑和结构保持领域有直接贡献
