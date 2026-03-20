# Parallel In-context Learning for Large Vision Language Models

**日期**: 2026-03-17  
**arXiv**: [2603.16092](https://arxiv.org/abs/2603.16092)  
**领域**: 多模态/VLM  
**关键词**: 并行ICL, Product-of-Experts, 推理加速, 多模态示例, 即插即用

## 一句话总结
提出 Parallel-ICL，将长示例上下文分割为并行处理的小块，通过加权 Product-of-Experts 融合，在保持完整上下文ICL性能的同时大幅降低推理延迟。

## 亮点
- **即插即用**：不改模型架构，任何VLM都可用
- **打破ICL的序列瓶颈**：将O(n)示例处理变为O(n/k)并行——对长示例上下文尤其有效
- PoE融合比简单平均更优——不同块贡献不同权重

## 评分
- 新颖性: ⭐⭐⭐⭐ | 实验: ⭐⭐⭐ | 价值: ⭐⭐⭐⭐
