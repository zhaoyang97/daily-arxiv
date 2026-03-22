#!/usr/bin/env python3
"""
从 daily JSON 生成 mkdocs 页面。

用法:
    python3 daily_arxiv/src/gen_daily_page.py                 # 重建所有页面
    python3 daily_arxiv/src/gen_daily_page.py 2026-03-18      # 只生成指定日期

输出:
    daily_arxiv/docs/YYYY-MM-DD/index.md   (每日页面)
    daily_arxiv/docs/index.md              (首页)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"
DOCS_DIR = ROOT / "docs"

# 从 classify 模块导入
sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify import (
    DOMAIN_EMOJI,
    DOMAIN_NAMES,
    classify_paper,
)

# 领域排序 (视觉系 → NLP/LLM 系 → 其他)
DOMAIN_ORDER = [
    "image_generation", "video_understanding", "3d_vision",
    "object_detection", "segmentation", "image_restoration",
    "autonomous_driving", "remote_sensing", "human_understanding",
    "medical_imaging",
    "multimodal_vlm", "llm_reasoning", "llm_agent", "llm_alignment",
    "llm_efficiency", "llm_nlp", "nlp_understanding", "nlp_generation",
    "model_compression", "self_supervised",
    "robotics", "reinforcement_learning", "graph_learning",
    "audio_speech", "time_series", "recommender", "ai_safety",
    "others",
]


def domain_sort_key(domain: str) -> int:
    if domain in DOMAIN_ORDER:
        return DOMAIN_ORDER.index(domain)
    return len(DOMAIN_ORDER)


def gen_daily_page(date: str, papers: list[dict]) -> str:
    """生成某天的 daily page markdown。"""
    # 分类论文
    for p in papers:
        if "domain" not in p:
            p["domain"] = classify_paper(p["title"], p["abstract"])

    # 按领域分组
    by_domain: dict[str, list[dict]] = {}
    for p in papers:
        by_domain.setdefault(p["domain"], []).append(p)

    # 统计
    total = len(papers)
    domain_count = len(by_domain)

    lines = []
    lines.append(f"# 📅 {date} arXiv Daily\n")
    lines.append(f"> 今日新论文: **{total}** 篇 | 涵盖 **{domain_count}** 个领域\n")

    # 领域分布表
    lines.append("## 📊 领域分布\n")
    lines.append("| 领域 | 数量 |")
    lines.append("|------|------|")
    for domain in sorted(by_domain.keys(), key=domain_sort_key):
        emoji = DOMAIN_EMOJI.get(domain, "📄")
        name = DOMAIN_NAMES.get(domain, domain)
        count = len(by_domain[domain])
        lines.append(f"| {emoji} {name} | {count} |")
    lines.append("")

    # 每个领域的论文列表
    lines.append("---\n")
    lines.append("## 📋 论文速览\n")

    for domain in sorted(by_domain.keys(), key=domain_sort_key):
        domain_papers = by_domain[domain]
        emoji = DOMAIN_EMOJI.get(domain, "📄")
        name = DOMAIN_NAMES.get(domain, domain)
        lines.append(f"### {emoji} {name} ({len(domain_papers)} 篇)\n")

        lines.append("| # | 论文 | arXiv | 作者 | 一句话说明 |")
        lines.append("|---|------|-------|------|-----------|")

        for i, p in enumerate(domain_papers, 1):
            title = p["title"]
            arxiv_id = p["arxiv_id"]
            arxiv_link = f"[{arxiv_id}](https://arxiv.org/abs/{arxiv_id})"
            authors = ", ".join(p["authors"][:3])
            if len(p["authors"]) > 3:
                authors += " et al."
            summary = p.get("summary", "")
            # 转义 markdown 表格中的 |
            summary = summary.replace("|", "\\|")
            title = title.replace("|", "\\|")
            lines.append(f"| {i} | {title} | {arxiv_link} | {authors} | {summary} |")

        lines.append("")

    return "\n".join(lines)


def gen_main_index() -> str:
    """生成首页，列出所有已有的 daily 页面。"""
    # 扫描 logs 目录找到所有 daily JSON
    daily_files = sorted(LOGS_DIR.glob("daily_*.json"), reverse=True)

    lines = []
    lines.append("# 📰 Daily arXiv\n")
    lines.append("每日自动追踪 arXiv 上 AI / LLM / NLP / CV 领域新发布的论文。\n")
    lines.append("**追踪类别**: `cs.CV` `cs.CL` `cs.AI` `cs.LG` `cs.MM` `cs.IR` `cs.RO`\n")
    lines.append("---\n")
    lines.append("## 📅 历史记录\n")
    lines.append("| 日期 | 论文数 | 热门领域 |")
    lines.append("|------|--------|----------|")

    for jf in daily_files:
        m = re.search(r"daily_(\d{4}-\d{2}-\d{2})\.json", jf.name)
        if not m:
            continue
        date = m.group(1)

        # 优先展示 filtered 数据
        filtered_path = LOGS_DIR / f"filtered_{date}.json"
        if filtered_path.exists():
            with open(filtered_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            tier_a = data.get("tier_a", [])
            total = data.get("stats", {}).get("total", 0)
            display_count = f"{len(tier_a)} 精选 / {total} 总"
            papers_for_domain = tier_a
        else:
            with open(jf, "r", encoding="utf-8") as f:
                papers_for_domain = json.load(f)
            display_count = str(len(papers_for_domain))

        if not papers_for_domain:
            lines.append(f"| {date} | 0 | - |")
            continue

        # 分类并找热门领域
        domain_counts: dict[str, int] = {}
        for p in papers_for_domain:
            d = p.get("domain") or classify_paper(p["title"], p["abstract"])
            domain_counts[d] = domain_counts.get(d, 0) + 1

        top_domains = sorted(domain_counts.items(), key=lambda x: -x[1])[:3]
        hot = ", ".join(
            f"{DOMAIN_EMOJI.get(d, '')} {DOMAIN_NAMES.get(d, d)}"
            for d, _ in top_domains
        )
        lines.append(f"| [{date}](./{date}/) | {display_count} | {hot} |")

    lines.append("")
    return "\n".join(lines)


def main():
    # 解析参数
    specific_date = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        specific_date = sys.argv[1]

    # 找到要处理的 JSON 文件
    if specific_date:
        json_files = [LOGS_DIR / f"daily_{specific_date}.json"]
    else:
        json_files = sorted(LOGS_DIR.glob("daily_*.json"))

    if not json_files:
        print("❌ 没有找到 daily JSON 文件")
        return

    # 为每个日期生成页面
    for jf in json_files:
        if not jf.exists():
            print(f"⚠️  {jf} 不存在，跳过")
            continue

        m = re.search(r"daily_(\d{4}-\d{2}-\d{2})\.json", jf.name)
        if not m:
            continue
        date = m.group(1)

        # 优先使用 filtered JSON（只含 A 档），否则 fallback 到全量
        filtered_path = LOGS_DIR / f"filtered_{date}.json"
        if filtered_path.exists():
            with open(filtered_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            papers = data.get("tier_a", [])
            print(f"  📄 {date}: 使用 filtered (A档 {len(papers)} 篇)")
        else:
            with open(jf, "r", encoding="utf-8") as f:
                papers = json.load(f)
            print(f"  📄 {date}: 使用全量 ({len(papers)} 篇，未筛选)")

        # 生成每日页面
        out_dir = DOCS_DIR / date
        out_dir.mkdir(parents=True, exist_ok=True)
        page = gen_daily_page(date, papers)
        out_path = out_dir / "index.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  📄 {date}: {len(papers)} 篇 → {out_path}")

    # 生成首页
    index = gen_main_index()
    index_path = DOCS_DIR / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)
    print(f"  🏠 首页 → {index_path}")


if __name__ == "__main__":
    main()
