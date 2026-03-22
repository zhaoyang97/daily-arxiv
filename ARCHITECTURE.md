# Daily arXiv 架构设计

## 项目简介

Daily arXiv 是一个自动追踪 arXiv 上每日新发布的 AI/LLM/NLP/CV 论文的工具。它每天从 arXiv 获取 400+ 篇新论文，自动分类到 28 个研究领域，通过打分筛选出最值得关注的 60 篇（A 档 20 篇深度笔记 + B 档 40 篇轻量笔记），并生成可浏览的 mkdocs 站点。计划作为独立 repo 开源。

## 系统概览

```
daily_arxiv/                          # 独立子项目（计划开源为独立 repo）
├── src/                              # 核心脚本
│   ├── fetch_daily.py                # 从 arXiv API 获取每日论文
│   ├── filter_daily.py               # 打分筛选 A/B 两档
│   ├── classify.py                   # 28 领域自动分类规则
│   ├── gen_daily_page.py             # 生成 mkdocs 页面
│   ├── gen_todo.py                   # 生成 TODO.md
│   └── download_daily.py             # 下载论文全文到缓存
├── docs/                             # mkdocs 源文件（自动生成）
│   ├── index.md                      # 首页：历史日期列表
│   └── YYYY-MM-DD/
│       ├── index.md                  # 每日速览页：领域分布 + 论文表格
│       └── notes/                    # 深度笔记（手动触发）
│           └── paper-slug.md
├── logs/                             # 原始数据
│   ├── daily_YYYY-MM-DD.json        # 每日论文元数据（全部）
│   └── filtered_YYYY-MM-DD.json     # 筛选结果（A档+B档）
├── TODO.md                           # 论文笔记进度追踪
├── ARCHITECTURE.md                   # 本文件
├── mkdocs.yml                        # 站点配置
└── README.md
```

缓存存放在 Auto Research 项目的统一目录：

```
paper_cache/
├── arxiv/                            # daily arXiv 论文缓存
│   ├── 2026-03-17/                   # 按日期分目录
│   │   ├── 2603.16021.txt
│   │   └── ...
│   ├── 2026-03-18/
│   └── 2026-03-19/
├── ICLR2026/                         # 会议论文缓存（已有）
├── CVPR2025/
└── ...
```

## 数据流

```
arXiv API ──fetch_daily.py──▶ logs/daily_YYYY-MM-DD.json (全部 ~400篇)
                                      │
                                      ├──filter_daily.py──▶ logs/filtered_YYYY-MM-DD.json (A档20 + B档40)
                                      │
                                      ├──gen_daily_page.py──▶ docs/YYYY-MM-DD/index.md  (速览页)
                                      │                       docs/index.md             (首页)
                                      │
                                      ├──gen_todo.py──▶ TODO.md (进度追踪)
                                      │
                                      └──download_daily.py──▶ paper_cache/arxiv/YYYY-MM-DD/*.txt
                                                                     │
                                                              write-note skill ──▶ docs/YYYY-MM-DD/notes/*.md
```

### 阶段说明

| 阶段 | 脚本 | 输入 | 输出 | 耗时 |
|------|------|------|------|------|
| 1. 获取论文 | `fetch_daily.py` | arXiv API | `logs/daily_*.json` | ~30s（~400篇/天） |
| 2. 筛选论文 | `filter_daily.py` | daily JSON | `logs/filtered_*.json` | <1s |
| 3. 生成页面 | `gen_daily_page.py` | daily JSON | `docs/*/index.md` | <1s |
| 4. 生成TODO | `gen_todo.py` | filtered JSON | `TODO.md` | <1s |
| 5. 下载全文 | `download_daily.py` | daily JSON | `paper_cache/arxiv/*/` | ~30min/天（5s/篇） |
| 6. 写 A 档笔记 | write-note skill | 缓存 txt (全文) | `docs/*/notes/*.md` | ~3min/篇 |
| 7. 写 B 档笔记 | write-note skill | abstract only | `docs/*/notes/*.md` | ~1min/篇 |

## 核心模块

### fetch_daily.py

通过 arXiv API 的 `submittedDate` 范围查询获取指定日期的论文。

- **API**: `http://export.arxiv.org/api/query`
- **查询**: `(cat:cs.CV OR cat:cs.CL OR cat:cs.AI OR cat:cs.LG OR cat:cs.MM OR cat:cs.IR OR cat:cs.RO) AND submittedDate:[YYYYMMDD0000 TO YYYYMMDD2359]`
- **批次**: 200 篇/请求，3.5s 间隔
- **输出**: JSON 数组，每篇包含 title, arxiv_id, abstract, authors, categories, published

### classify.py

28 个领域的关键词匹配规则，从 Auto Research 的 `reclassify_auto.py` 提取。

- 按优先级排序：视觉 → 医学 → RL/优化 → VLM → LLM 子领域 → 兜底
- 支持负面规则（如 "reinforcement learning" 但包含 "llm agent" 则不归类为 RL）
- 提供领域中文名和 Emoji 映射

### gen_daily_page.py

从 JSON 生成两种页面：

- **每日页面** (`YYYY-MM-DD/index.md`): 领域分布统计 + 按领域分组的论文速览表
- **首页** (`index.md`): 历史日期列表，每天显示论文数和热门领域

### filter_daily.py

从 daily JSON 中筛选值得写笔记的论文。

**筛选流程**: ~400篇 → 领域过滤(~200篇) → 打分排序 → 取 Top-20 (A档)

#### Step 1: 领域过滤

只保留 15 个关注领域，丢弃医学影像、强化学习、时间序列等：

```
multimodal_vlm, llm_reasoning, llm_agent, llm_efficiency, llm_alignment, llm_nlp,
image_generation, video_understanding, 3d_vision,
model_compression, self_supervised, nlp_understanding, nlp_generation,
robotics, ai_safety
```

#### Step 2: 多维打分 (总分 0-75)

| 维度 | 分数 | 规则 |
|------|------|------|
| 领域权重 | 0-15 | 均匀化设计，VLM/推理=15, Agent/效率/视频/图生/机器人=13-14, 其他=11-12 |
| 团队知名度 | 0-15 | **搜索 authors + abstract + comment** 匹配 27 个团队关键词（Google/Meta/清华等），每命中+5。仅搜作者名命中率~0%，加上 abstract 后提升到~10% |
| 高价值关键词 | 0-30 | abstract 匹配 24 个词（SOTA/benchmark/open-source等），每命中+3 |
| 有代码 | 0-5 | abstract 含 github.com / "code available" |
| 摘要长度 | 0-10 | >150词+5, >250词+5（详细摘要=更实质的工作） |
| 低价值惩罚 | -10 | "survey of" / "position paper" / "workshop" |

**领域权重设计原则**: 均匀化（15 vs 11，差距仅 4 分），避免单一领域主导 A 档。
高价值关键词和团队知名度的区分度更大（0-30 和 0-15），让论文质量信号>领域偏好。

**已知局限**:
- 团队识别搜索 authors + abstract + comment，命中率约 10%（arXiv API 不返回 affiliation，只能从文本中间接匹配）
- "we propose" 等宽泛关键词几乎所有论文都有，区分度低
- 无法感知论文的引用/影响力（arXiv 新论文无引用数据）

#### Step 3: 取 Top-20

- **A 档** (默认 20 篇): 得分最高，写深度笔记（读全文，100+ 行）
- 支持 `--top-a N` 自定义数量

### gen_todo.py

从 filtered JSON 生成 `TODO.md`，按日期和领域分组，追踪笔记完成进度。

- 自动扫描 `docs/*/notes/` 识别已完成的笔记
- checkbox 格式，与 Auto Research 的 TODO 风格一致

### download_daily.py

包装器脚本，从 daily JSON 提取 arXiv ID，调用 Auto Research 的 `fetch_arxiv_html.py` 下载。

- 缓存路径: `paper_cache/arxiv/YYYY-MM-DD/<arxiv_id>.txt`
- 复用已有的多线程下载 + 全局速率锁 + HTML 清洗逻辑

## 追踪类别

| 类别 | 全称 | 说明 |
|------|------|------|
| `cs.CV` | Computer Vision | CV 核心 |
| `cs.CL` | Computation and Language | NLP/LLM 核心 |
| `cs.AI` | Artificial Intelligence | AI 通用 |
| `cs.LG` | Machine Learning | ML 核心 |
| `cs.MM` | Multimedia | 多模态 |
| `cs.IR` | Information Retrieval | 检索/RAG |
| `cs.RO` | Robotics | 具身智能 |

## 与 Auto Research 的关系

| 组件 | 共享/独立 | 说明 |
|------|-----------|------|
| `fetch_arxiv_html.py` | 共享 | 论文下载复用 Auto Research 的脚本 |
| `paper_cache/` | 共享 | 缓存统一存放，daily 放在 `arxiv/` 子目录 |
| `classify.py` | 独立副本 | 从 `reclassify_auto.py` 提取，独立维护 |
| mkdocs 站点 | 独立 | 独立的 `mkdocs.yml`，独立部署 |
| write-note skill | 共享 | 深度笔记复用现有 skill |

## 每日速览页面结构

```markdown
# 📅 YYYY-MM-DD arXiv Daily

> 今日新论文: **N** 篇 | 涵盖 **M** 个领域

## 📊 领域分布
| 领域 | 数量 |
|------|------|
| 🎨 图像生成 | 32 |
| 🧠 LLM推理 | 15 |
| ...

## 📋 论文速览

### 🎨 图像生成 (32 篇)
| # | 论文 | arXiv | 作者 | 一句话说明 |
|---|------|-------|------|-----------|
| 1 | Title | link | A et al. | Abstract 首句 |
```

## 命令速查

```bash
# 1. 获取论文
python3 daily_arxiv/src/fetch_daily.py              # 获取昨天
python3 daily_arxiv/src/fetch_daily.py --days 3      # 获取过去 3 天
python3 daily_arxiv/src/fetch_daily.py 2026-03-20    # 获取指定日期

# 2. 筛选论文 (A/B 两档)
python3 daily_arxiv/src/filter_daily.py --days 3
python3 daily_arxiv/src/filter_daily.py 2026-03-20 --top-a 15 --top-b 30

# 3. 生成速览页面
python3 daily_arxiv/src/gen_daily_page.py

# 4. 生成 TODO
python3 daily_arxiv/src/gen_todo.py

# 5. 下载论文全文
python3 daily_arxiv/src/download_daily.py 2026-03-20
python3 daily_arxiv/src/download_daily.py --days 3

# 6. 本地预览
cd daily_arxiv && mkdocs serve -a 127.0.0.1:8200
```
