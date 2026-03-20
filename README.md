# Daily arXiv

每日自动追踪 arXiv 上 AI / LLM / NLP / CV 领域新发布的论文，筛选最值得关注的论文并生成深度笔记。

🌐 **在线浏览**: [zhaoyang97.github.io/daily-arxiv](https://zhaoyang97.github.io/daily-arxiv/)

## 特色

- 每天从 arXiv 获取 400+ 篇新论文，自动分类到 28 个研究领域
- 打分筛选出最值得关注的 ~20 篇，生成深度阅读笔记（100+ 行）
- 每日速览页：领域分布 + 全部论文一览表
- 自动部署到 GitHub Pages，推送即发布

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

## 目录结构

```
daily-arxiv/
├── docs/                        # 站点内容 (mkdocs 源文件)
│   ├── index.md                 # 首页：历史日期列表
│   └── YYYY-MM-DD/
│       ├── index.md             # 每日速览页
│       └── notes/*.md           # 深度论文笔记
├── src/                         # 自动化脚本
│   ├── fetch_daily.py           # 获取每日论文
│   ├── filter_daily.py          # 打分筛选
│   ├── classify.py              # 领域分类规则
│   ├── gen_daily_page.py        # 生成页面
│   ├── gen_todo.py              # 生成进度追踪
│   └── download_daily.py        # 下载论文全文
├── logs/                        # 原始数据 (不入 git)
├── mkdocs.yml
└── .github/workflows/deploy.yml # 自动部署
```

## License

MIT
│       └── index.md         # 每日页面 (自动生成)
├── logs/                    # 原始数据
│   └── daily_YYYY-MM-DD.json
├── mkdocs.yml
└── README.md
```
