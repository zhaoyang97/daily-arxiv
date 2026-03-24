# AutoKernel: Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search

**日期**: 2026-03-22  
**arXiv**: [2603.21331](https://arxiv.org/abs/2603.21331)  
**代码**: [GitHub](https://github.com/RightNow-AI/autokernel)  
**领域**: LLM/NLP  
**关键词**: GPU kernel optimization, LLM agent, Triton, CUDA, automated performance tuning

## 一句话总结
提出 AutoKernel，用 LLM Agent 自动化 GPU Kernel 优化——模拟专家工程师的"写→Profile→保留/回退"循环，结合 Amdahl 定律指导优化优先级和五阶段正确性验证，在 H100 上 RMSNorm 加速 5.29× vs PyTorch eager、3.44× softmax vs torch.compile。

## 研究背景与动机

1. **领域现状**: 高性能 GPU kernel 开发是 AI infra 的核心瓶颈——专家级工程师需要数周调优一个 kernel（block tiling、shared memory、tensor core 等）。

2. **现有痛点**: (a) LLM 单独生成 kernel 成功率 <20%——缺乏编译反馈和性能分析；(b) 现有自动化方法不做模型级 profiling，无法判断哪个 kernel 优化收益最大；(c) 不支持 Triton + CUDA 双后端。

3. **核心 idea**: 机械化专家内核工程师的工作流——LLM Agent 在 keep/revert 循环中迭代优化，用模型级 profiler + Amdahl 定律分配优化预算，五阶段正确性保证。

## 方法详解

### 整体框架
PyTorch 模型 → torch.profiler 逐 kernel 分析 GPU 时间 → Amdahl 定律排序 → 对每个 kernel: LLM 编辑代码 → 五阶段验证 → benchark → 超过 1% 提升则保留、否则回退 → 重复直到收敛。

### 关键设计

1. **模型级 Profiler + Amdahl 排序**:
   - torch.profiler 捕获每个 kernel 的 GPU 时间占比
   - 按 $S = 1/((1-f) + f/s)$ 排序优先级——60% 占比的 kernel 1.5× 加速 → 整体 1.25×，5% 的 kernel 同样加速只有 1.03×
   - 自动分配优化预算到高收益 kernel

2. **五阶段正确性验证**:
   - Smoke test（编译通过）→ Shape sweep（8-10 配置 × 3 dtype）→ 数值稳定性（对抗输入）→ 确定性验证（bitwise 一致）→ 边界情况（非 power-of-2）
   - 每个阶段捕获不同类别的 bug，缺一不可
   - dtype 特定容差: FP16 atol=1e-2, BF16 2e-2, FP32 1e-4

3. **双后端支持**:
   - **Triton**: 快速迭代（1-5s 编译），9 种 kernel 类型，调 block_size/num_warps/num_stages
   - **CUDA C++**: 显式控制 tensor core/warp shuffle/shared memory layout
   - 每次迭代 ~90s（30s 正确性 + 30s 性能 + 30s 推理）

4. **Agent 指令工程**:
   - 909 行 program.md 编码 6 层优化 Playbook: block sizing → 内存访问 → 计算 → 高级 → 架构特定 → kernel 特定
   - 单文件不变量: Agent 只编辑一个 kernel 文件，保持 diff 小、回退干净
   - 收敛条件: 连续 5 次回退 / 达到 GPU 峰值 90% / 超 2 小时 / 2× 加速

## 实验关键数据

### 主实验（NVIDIA H100，μs 越小越好）

| Kernel | 尺寸 | Eager (μs) | torch.compile (μs) | 本文 (μs) | vs Eager | vs Compiled |
|--------|------|-----------|-------------------|----------|----------|------------|
| **RMSNorm** | 8192² | 509.6 | 272.1 | **96.3** | **5.29×** | **2.83×** |
| **Softmax** | 8192² | 270.4 | 330.0 | **95.9** | **2.82×** | **3.44×** |
| **Cross-Ent** | 8192×32k | 559.7 | 745.1 | **253.3** | **2.21×** | **2.94×** |
| **Reduce** | 16384×4096 | 50.4 | 185.9 | 52.8 | 0.95× | **3.52×** |
| Matmul | 4096³ | 182.8 | 257.8 | 494.2 | 0.37× | 0.52× |

RMSNorm 达到 **2,788 GB/s（H100 峰值的 83%）**。

### 社区 Benchmark
- **VectorSum B200 排行榜第一**: 44.086μs 领先第二名 44.249μs
- **FP4 MatMul vs CUTLASS**: Triton 实现超 CUTLASS 1.63-2.15×（128→2048 batch）

### 优化轨迹（RMSNorm 代表性曲线）

| 阶段 | 迭代数 | 吞吐量 | 说明 |
|------|--------|--------|------|
| Tier 1 (block size) | 1-5 | 207→2400 GB/s | **10.6× 提升** |
| Tier 2 (memory coalescing) | 6-20 | 2400→2650 GB/s | +10% |
| Tier 3 (epilogue fusion) | 21-35 | 2650→2788 GB/s | +5%, 接近峰值 |

### 关键发现
- **Memory-bound kernel 收益最大**: RMSNorm/softmax/cross-entropy (5.29×/2.82×/2.21×)，单 pass fusion 减少 HBM round-trips 是关键
- **Matmul 是困难场景**: cuBLAS 已极度优化 →仅 0.37×；agent 需更多实验空间
- **迭代效率**: ~40 实验/小时，300-400 次/10小时；~90s/迭代（30s 验证+30s 性能+30s 推理）
- **All 34 configs 通过正确性**: 零 silent corruption——五阶段 harness 必不可少

## 亮点与洞察
- **系统工程胜于复杂架构**: 简单的写→测→保留/回退循环 + 完善的正确性保证 > 花哨的 multi-agent
- **Amdahl 指导优化预算**: 把教科书优化理论和 LLM Agent 结合，避免在低收益 kernel 上浪费时间
- **五阶段验证设计可复用**: 这套 kernel 正确性验证框架本身就有独立价值

## 局限性 / 可改进方向
- 仅支持 9 种 kernel 类型，不能自动发现全新算法
- 依赖 PyTorch 框架
- Shape/dtype 参数不能自动发现
- 不包含 kernel 架构层面的创新（只在已知模式内优化）

## 相关工作与启发
- **vs KernelBench**: 仅 benchmark 基础设施；AutoKernel 是端到端优化 pipeline
- **vs CUDA Agent, GEAK**: RL-based / multi-agent；AutoKernel 简单 keep/revert 循环 + roofline 更实用
- **独特优势**: 唯一同时具备 (1) 模型 profiling (2) Amdahl 编排 (3) 双后端 (4) 五阶段验证的系统

## 评分
- 新颖性: ⭐⭐⭐ 更偏系统工程，核心思路直觉
- 实验充分度: ⭐⭐⭐⭐⭐ 多 GPU、多 kernel 类型、社区排行榜实战验证
- 写作质量: ⭐⭐⭐⭐ 工程细节描述充分
- 价值: ⭐⭐⭐⭐⭐ 实用价值极高，代码开源，FP4 MatMul 打败 CUTLASS
