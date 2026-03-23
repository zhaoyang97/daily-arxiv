# vla-eval: A Unified Evaluation Harness for Vision-Language-Action Models

**日期**: 2026-03-14  
**arXiv**: [2603.13966](https://arxiv.org/abs/2603.13966)  
**代码**: [vla-eval](https://github.com/allenai/vla-evaluation-harness)  
**领域**: 多模态VLM / 评估框架  
**关键词**: VLA evaluation, benchmark harness, reproducibility, robot learning, simulation

## 一句话总结
提出 vla-eval 统一评估框架，通过 WebSocket+msgpack 协议解耦模型推理与 benchmark 执行，用 Docker 容器化隔离环境，支持 13 个仿真 benchmark + 6 个模型服务器，并行评估实现 47× 吞吐提升，发现多个现有方法存在不可复现问题。

## 研究背景与动机

1. **领域现状**: VLA 模型评估使用各 benchmark 独立维护的脚本，导致代码重复、依赖冲突、协议不明确，严重阻碍可复现性研究。

2. **核心矛盾**: 评估计算成本极高（单次 LIBERO 评估需 ~14 小时），使得消融实验不切实际。不同论文使用不同评估脚本导致结果不可比。

3. **核心 idea**: 用标准化接口解耦模型和 benchmark，Docker 隔离环境，并行 episode 分片 + batch 推理降低成本。

## 方法详解

### 关键设计

1. **协议层**: WebSocket+msgpack，模型只需实现 `predict()` 方法，benchmark 只需 4 个接口方法
2. **环境隔离**: Docker 容器化每个 benchmark，消除依赖冲突
3. **并行评估**: Episode sharding（N=50 容器）+ batch 推理（B=16）→ 47× 吞吐提升
4. **VLA Leaderboard**: 汇聚 2685 篇论文的 657 个评估结果

## 实验关键数据

| 指标 | 数值 |
|------|------|
| 支持 benchmark 数 | 13 |
| 支持模型数 | 6 |
| 2000 LIBERO episodes | ~18 分钟（vs 14 小时） |
| 吞吐提升 | 47× |
| 可复现偏差 | ±1.4% |

### 关键发现
- DB-CogACT 的 LIBERO 结果可在 ±1.4% 内复现
- SimplerEnv 的终止语义和 CALVIN 的归一化统计是未文档化的隐藏要求
- 标准化评估揭示了多个方法的实际性能与报告值有差异

## 亮点与洞察
- **基础设施级贡献** — 解决了 VLA 社区的评估碎片化问题
- **47× 加速**使得大规模消融研究变得可行

## 评分
- 新颖性: ⭐⭐⭐ 工程贡献为主
- 实验充分度: ⭐⭐⭐⭐ 可复现性审计和性能分析充分
- 价值: ⭐⭐⭐⭐⭐ 对 VLA 社区有极高实用价值
