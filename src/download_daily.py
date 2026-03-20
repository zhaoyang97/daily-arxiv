#!/usr/bin/env python3
"""
下载 daily arXiv 论文的 HTML 到 paper_cache。

复用 Auto Research 的 fetch_arxiv_html.py，按日期下载。

用法:
    python3 daily_arxiv/src/download_daily.py 2026-03-19
    python3 daily_arxiv/src/download_daily.py --days 3
    python3 daily_arxiv/src/download_daily.py --days 3 --max 50
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"
PROJECT_ROOT = ROOT.parent  # Auto Research root


def main():
    target_dates = []
    max_per_day = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--days":
            n = int(args[i + 1])
            for d in range(n):
                dt = datetime.now() - timedelta(days=d + 1)
                target_dates.append(dt.strftime("%Y-%m-%d"))
            i += 2
        elif args[i] == "--max":
            max_per_day = int(args[i + 1])
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

        ids = [p["arxiv_id"] for p in papers if p.get("arxiv_id")]
        if max_per_day:
            ids = ids[:max_per_day]

        if not ids:
            print(f"⚠️  {date}: 没有论文可下载")
            continue

        conference = f"arxiv/{date}"
        print(f"\n📥 {date}: 下载 {len(ids)} 篇论文到 paper_cache/{conference}/")

        # 调用现有的 fetch_arxiv_html.py (conference 是 positional arg)
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / "src" / "fetch_arxiv_html.py"),
            conference,
            "--ids", *ids,
        ]
        subprocess.run(cmd)

    print("\n✅ 下载完成")


if __name__ == "__main__":
    main()
