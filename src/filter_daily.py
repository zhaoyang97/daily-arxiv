#!/usr/bin/env python3
"""
从 daily JSON 中筛选值得写笔记的论文，分 A/B 两档。

用法:
    python3 daily_arxiv/src/filter_daily.py 2026-03-19
    python3 daily_arxiv/src/filter_daily.py --days 3
    python3 daily_arxiv/src/filter_daily.py 2026-03-19 --top-a 20 --top-b 40

输出: daily_arxiv/logs/filtered_YYYY-MM-DD.json
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify import classify_paper, DOMAIN_NAMES, DOMAIN_EMOJI

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"

# ── 配置 ──────────────────────────────────────────────────────

# 关注的领域 (只有这些领域的论文会被筛选)
FOCUS_DOMAINS = {
    # 核心
    "multimodal_vlm", "llm_reasoning", "llm_agent", "llm_efficiency",
    "llm_alignment", "llm_nlp",
    # CV
    "image_generation", "video_understanding", "3d_vision",
    "model_compression", "self_supervised",
    # NLP
    "nlp_understanding", "nlp_generation",
    # 应用
    "robotics", "ai_safety",
}

# 知名团队/机构关键词 (从作者名或 affiliation 推断)
TOP_TEAMS = [
    "google", "deepmind", "openai", "meta", "fair",
    "microsoft", "nvidia", "apple", "anthropic",
    "tsinghua", "peking", "tencent", "alibaba", "baidu", "bytedance",
    "stanford", "mit", "berkeley", "cmu", "princeton", "harvard",
    "oxford", "cambridge", "eth zurich", "epfl",
    "kaist", "seoul national", "tokyo",
]

# 高价值关键词 (abstract 中出现加分)
HIGH_VALUE_KEYWORDS = [
    # 方法创新
    "state-of-the-art", "sota", "novel framework", "first to",
    "we propose", "we introduce", "new paradigm", "unified",
    "surpass", "outperform",
    # 重要主题
    "scaling law", "emergent", "chain-of-thought", "in-context",
    "instruction tuning", "rlhf", "direct preference",
    "world model", "test-time", "inference-time",
    "long context", "mixture of expert", "moe",
    "multimodal", "vision-language", "video generation",
    "diffusion", "flow matching", "autoregressive",
    "benchmark", "evaluation",
    # 实用性
    "open-source", "code available", "publicly available",
]

# 低价值信号 (降分)
LOW_VALUE_SIGNALS = [
    "survey of", "review of", "a survey",
    "position paper", "workshop",
    "dataset only", "annotation tool",
]


def score_paper(paper: dict, domain: str) -> float:
    """对论文打分 (0-100)。"""
    score = 0.0
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    authors = [a.lower() for a in paper.get("authors", [])]
    text = f"{title} {abstract}"

    # 1. 领域权重 (0-20)
    domain_weights = {
        "multimodal_vlm": 20, "llm_reasoning": 18, "llm_agent": 16,
        "llm_efficiency": 15, "llm_alignment": 14, "llm_nlp": 12,
        "image_generation": 14, "video_understanding": 13, "3d_vision": 12,
        "model_compression": 10, "self_supervised": 10,
        "nlp_understanding": 10, "nlp_generation": 10,
        "robotics": 12, "ai_safety": 11,
    }
    score += domain_weights.get(domain, 5)

    # 2. 团队加分 (0-15)
    author_text = " ".join(authors)
    team_hits = sum(1 for t in TOP_TEAMS if t in author_text)
    score += min(team_hits * 5, 15)

    # 3. 高价值关键词 (0-30)
    kw_hits = sum(1 for kw in HIGH_VALUE_KEYWORDS if kw in text)
    score += min(kw_hits * 3, 30)

    # 4. 有代码 (0-5)
    if "github.com" in text or "code available" in text or "open-source" in text:
        score += 5

    # 5. 摘要长度和质量信号 (0-10)
    abstract_len = len(abstract.split())
    if abstract_len > 150:
        score += 5  # 详细摘要通常意味着更实质的工作
    if abstract_len > 250:
        score += 5

    # 6. 低价值惩罚 (-10)
    if any(s in text for s in LOW_VALUE_SIGNALS):
        score -= 10

    return max(score, 0)


def filter_papers(papers: list[dict], top_a: int = 20, top_b: int = 40) -> dict:
    """筛选论文，返回 A/B 两档。"""
    # 分类 + 打分
    scored = []
    for p in papers:
        domain = classify_paper(p["title"], p["abstract"])
        if domain not in FOCUS_DOMAINS:
            continue
        s = score_paper(p, domain)
        scored.append({**p, "domain": domain, "score": s})

    # 按分数排序
    scored.sort(key=lambda x: -x["score"])

    # 分档
    tier_a = scored[:top_a]
    tier_b = scored[top_a:top_a + top_b]

    return {
        "tier_a": tier_a,
        "tier_b": tier_b,
        "stats": {
            "total": len(papers),
            "in_focus": len(scored),
            "tier_a_count": len(tier_a),
            "tier_b_count": len(tier_b),
            "tier_a_min_score": tier_a[-1]["score"] if tier_a else 0,
            "tier_b_min_score": tier_b[-1]["score"] if tier_b else 0,
        },
    }


def print_summary(date: str, result: dict):
    """打印筛选结果摘要。"""
    stats = result["stats"]
    print(f"\n{'='*60}")
    print(f"📅 {date} 筛选结果")
    print(f"{'='*60}")
    print(f"  总论文: {stats['total']} | 关注领域: {stats['in_focus']} | "
          f"A档: {stats['tier_a_count']} | B档: {stats['tier_b_count']}")
    print(f"  A档分数线: {stats['tier_a_min_score']:.0f} | "
          f"B档分数线: {stats['tier_b_min_score']:.0f}")

    for tier_name, papers in [("🅰️  A档 (深度笔记)", result["tier_a"]),
                               ("🅱️  B档 (轻量笔记)", result["tier_b"])]:
        print(f"\n  {tier_name}:")
        # 按领域分组
        by_domain: dict[str, list] = {}
        for p in papers:
            by_domain.setdefault(p["domain"], []).append(p)
        for domain in sorted(by_domain, key=lambda d: -len(by_domain[d])):
            emoji = DOMAIN_EMOJI.get(domain, "📄")
            name = DOMAIN_NAMES.get(domain, domain)
            domain_papers = by_domain[domain]
            print(f"    {emoji} {name} ({len(domain_papers)}篇)")
            for p in domain_papers[:5]:  # 每个领域最多显示5篇
                short_title = p["title"][:60] + ("..." if len(p["title"]) > 60 else "")
                print(f"      [{p['score']:.0f}] {short_title}")
            if len(domain_papers) > 5:
                print(f"      ... +{len(domain_papers)-5} 篇")


def main():
    target_dates = []
    top_a = 20
    top_b = 40

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--days":
            n = int(args[i + 1])
            for d in range(n):
                dt = datetime.now() - timedelta(days=d + 1)
                target_dates.append(dt.strftime("%Y-%m-%d"))
            i += 2
        elif args[i] == "--top-a":
            top_a = int(args[i + 1])
            i += 2
        elif args[i] == "--top-b":
            top_b = int(args[i + 1])
            i += 2
        elif not args[i].startswith("-"):
            target_dates.append(args[i])
            i += 1
        else:
            i += 1

    if not target_dates:
        yesterday = datetime.now() - timedelta(days=1)
        target_dates.append(yesterday.strftime("%Y-%m-%d"))

    target_dates.sort()

    for date in target_dates:
        json_path = LOGS_DIR / f"daily_{date}.json"
        if not json_path.exists():
            print(f"⚠️  {json_path} 不存在，跳过 {date}")
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            papers = json.load(f)

        result = filter_papers(papers, top_a, top_b)
        print_summary(date, result)

        # 保存
        out_path = LOGS_DIR / f"filtered_{date}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n  💾 保存到 {out_path}")


if __name__ == "__main__":
    main()
