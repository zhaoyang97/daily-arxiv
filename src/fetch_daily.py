#!/usr/bin/env python3
"""
从 arXiv 获取每日新发布的 AI/LLM/NLP/CV 论文。

用法:
    python3 daily_arxiv/src/fetch_daily.py                    # 获取昨天
    python3 daily_arxiv/src/fetch_daily.py 2026-03-18         # 获取指定日期
    python3 daily_arxiv/src/fetch_daily.py --days 3           # 获取过去3天

输出: daily_arxiv/logs/daily_YYYY-MM-DD.json
"""
import json
import re
import ssl
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# 追踪的 arXiv 类别
CATEGORIES = ["cs.CV", "cs.CL", "cs.AI", "cs.LG", "cs.MM", "cs.IR", "cs.RO"]

# Proxy + SSL (与 Auto Research 保持一致)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
proxy_handler = urllib.request.ProxyHandler({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
})
https_handler = urllib.request.HTTPSHandler(context=ctx)
opener = urllib.request.build_opener(proxy_handler, https_handler)

NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def parse_entry(entry) -> dict | None:
    """解析 arXiv API 返回的单条 entry。"""
    id_elem = entry.find("atom:id", NS)
    if id_elem is None:
        return None
    id_text = id_elem.text.strip()
    if "api/errors" in id_text:
        return None

    title = entry.find("atom:title", NS).text.strip().replace("\n", " ")
    title = re.sub(r"\s+", " ", title)

    arxiv_id = id_text.split("/")[-1]
    arxiv_id = re.sub(r"v\d+$", "", arxiv_id)

    summary = entry.find("atom:summary", NS).text.strip().replace("\n", " ")
    summary = re.sub(r"\s+", " ", summary)

    categories = [c.get("term") for c in entry.findall("atom:category", NS)]
    primary_cat = categories[0] if categories else ""

    authors = [a.find("atom:name", NS).text for a in entry.findall("atom:author", NS)]

    published = entry.find("atom:published", NS).text.strip()[:10]

    comment_elem = entry.find("arxiv:comment", NS)
    comment = comment_elem.text.strip() if comment_elem is not None and comment_elem.text else ""

    # 只保留主类别在目标列表中的论文
    if not any(c in CATEGORIES for c in categories[:3]):
        return None

    return {
        "title": title,
        "arxiv_id": arxiv_id,
        "abstract": summary,
        "authors": authors[:5],
        "primary_category": primary_cat,
        "categories": categories[:5],
        "published": published,
        "comment": comment,
    }


def fetch_by_date_range(from_date: str, to_date: str) -> list[dict]:
    """用 submittedDate 范围查询获取论文。"""
    cat_query = "+OR+".join(f"cat:{c}" for c in CATEGORIES)
    fd = from_date.replace("-", "")
    td = to_date.replace("-", "")
    base_query = f"({cat_query})+AND+submittedDate:[{fd}0000+TO+{td}2359]"

    all_papers = []
    batch_size = 200
    max_total = 5000

    for start in range(0, max_total, batch_size):
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query={base_query}"
            f"&start={start}&max_results={batch_size}"
            f"&sortBy=submittedDate&sortOrder=descending"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DailyArxiv/1.0"})
            resp = opener.open(req, timeout=30)
            data = resp.read().decode("utf-8")
            root = ET.fromstring(data)
            entries = root.findall("atom:entry", NS)

            if not entries:
                break

            count = 0
            for entry in entries:
                paper = parse_entry(entry)
                if paper:
                    all_papers.append(paper)
                    count += 1

            print(f"  Batch start={start}: {len(entries)} entries, {count} kept (total: {len(all_papers)})")

            if len(entries) < batch_size:
                break

            time.sleep(3.5)

        except Exception as e:
            print(f"  ❌ Batch start={start} error: {e}")
            time.sleep(5)

    return all_papers


def fetch_recent_sorted(max_results: int = 3000) -> list[dict]:
    """备用方案: 不用日期范围，获取最近的论文按日期排序。"""
    cat_query = "+OR+".join(f"cat:{c}" for c in CATEGORIES)

    all_papers = []
    batch_size = 200

    for start in range(0, max_results, batch_size):
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query={cat_query}"
            f"&start={start}&max_results={batch_size}"
            f"&sortBy=submittedDate&sortOrder=descending"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DailyArxiv/1.0"})
            resp = opener.open(req, timeout=30)
            data = resp.read().decode("utf-8")
            root = ET.fromstring(data)
            entries = root.findall("atom:entry", NS)

            if not entries:
                break

            count = 0
            for entry in entries:
                paper = parse_entry(entry)
                if paper:
                    all_papers.append(paper)
                    count += 1

            print(f"  Batch start={start}: {len(entries)} entries, {count} kept (total: {len(all_papers)})")

            if len(entries) < batch_size:
                break

            time.sleep(3.5)

        except Exception as e:
            print(f"  ❌ Batch start={start} error: {e}")
            time.sleep(5)

    return all_papers


def extract_summary(abstract: str) -> str:
    """从摘要中提取第一句话作为一句话总结。"""
    match = re.match(r"^(.+?\.)\s", abstract)
    if match:
        sent = match.group(1)
        if len(sent) > 200:
            return sent[:197] + "..."
        return sent
    if len(abstract) > 200:
        return abstract[:197] + "..."
    return abstract


def deduplicate(papers: list[dict]) -> list[dict]:
    """按 arxiv_id 去重。"""
    seen = set()
    unique = []
    for p in papers:
        if p["arxiv_id"] not in seen:
            seen.add(p["arxiv_id"])
            unique.append(p)
    return unique


def main():
    # 解析参数
    target_dates = []

    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        n = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 3
        for i in range(n):
            d = datetime.now() - timedelta(days=i + 1)
            target_dates.append(d.strftime("%Y-%m-%d"))
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        target_dates.append(sys.argv[1])
    else:
        yesterday = datetime.now() - timedelta(days=1)
        target_dates.append(yesterday.strftime("%Y-%m-%d"))

    target_dates.sort()
    from_date = target_dates[0]
    to_date = target_dates[-1]

    print(f"📅 获取 {from_date} ~ {to_date} 的 arXiv 论文")
    print(f"📂 类别: {', '.join(CATEGORIES)}")

    # 日期范围扩展 1 天，确保不遗漏
    from_dt = datetime.strptime(from_date, "%Y-%m-%d") - timedelta(days=1)
    to_dt = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
    from_ext = from_dt.strftime("%Y-%m-%d")
    to_ext = to_dt.strftime("%Y-%m-%d")

    print(f"🔍 查询范围 (含 margin): {from_ext} ~ {to_ext}")

    # 先尝试 submittedDate 范围查询
    papers = fetch_by_date_range(from_ext, to_ext)

    # 如果没拿到结果，使用备用方案
    if len(papers) == 0:
        print("⚠️  submittedDate 范围查询无结果，使用备用方案...")
        papers = fetch_recent_sorted()

    papers = deduplicate(papers)
    print(f"\n✅ 总计获取 {len(papers)} 篇去重论文")

    # 按 published 日期分组
    by_date: dict[str, list[dict]] = {}
    for p in papers:
        d = p["published"]
        by_date.setdefault(d, []).append(p)

    # 保存目标日期的 JSON
    for d in target_dates:
        date_papers = by_date.get(d, [])
        for p in date_papers:
            p["summary"] = extract_summary(p["abstract"])
        out_path = LOGS_DIR / f"daily_{d}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(date_papers, f, indent=2, ensure_ascii=False)
        print(f"  💾 {d}: {len(date_papers)} 篇 → {out_path}")

    # 报告其他日期 (不保存)
    for d in sorted(by_date.keys()):
        if d not in target_dates:
            print(f"  ℹ️  {d}: {len(by_date[d])} 篇 (非目标日期)")


if __name__ == "__main__":
    main()
