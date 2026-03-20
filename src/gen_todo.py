#!/usr/bin/env python3
"""生成 daily_arxiv/TODO.md"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify import DOMAIN_NAMES, DOMAIN_EMOJI

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"

# 已写的笔记 (arxiv_id)
WRITTEN = {"2603.19235", "2603.19234", "2603.19232", "2603.19233", "2603.19231"}


def main():
    # 找到所有 filtered JSON
    filtered_files = sorted(LOGS_DIR.glob("filtered_*.json"))
    if not filtered_files:
        print("❌ 没有找到 filtered JSON 文件")
        return

    lines = []
    lines.append("# Daily arXiv 论文笔记 TODO\n")
    lines.append("> A档: 深度笔记 (读全文, 100+行) | B档: 轻量笔记 (只读abstract, 50行)\n")

    total_a = 0
    done = 0

    for fpath in filtered_files:
        date = fpath.stem.replace("filtered_", "")
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        tier_a = data["tier_a"]
        total_a += len(tier_a)

        lines.append(f"## 📅 {date} (A档 {len(tier_a)} 篇)\n")

        # 扫描 notes 目录看哪些已写
        notes_dir = ROOT / "docs" / date / "notes"
        written_ids = set(WRITTEN)
        if notes_dir.exists():
            for md in notes_dir.glob("*.md"):
                # 从文件内容提取 arxiv_id
                content = md.read_text(encoding="utf-8")
                for line in content.split("\n")[:10]:
                    if "arxiv.org/abs/" in line:
                        aid = line.split("arxiv.org/abs/")[-1].split(")")[0].strip()
                        written_ids.add(aid)

        # 按领域分组
        by_domain: dict[str, list] = {}
        for p in tier_a:
            by_domain.setdefault(p["domain"], []).append(p)

        for domain in sorted(by_domain, key=lambda d: -len(by_domain[d])):
            emoji = DOMAIN_EMOJI.get(domain, "📄")
            name = DOMAIN_NAMES.get(domain, domain)
            papers = by_domain[domain]
            lines.append(f"### {emoji} {name}")
            for p in papers:
                aid = p["arxiv_id"]
                title = p["title"][:80]
                check = "x" if aid in written_ids else " "
                if aid in written_ids:
                    done += 1
                lines.append(
                    f"- [{check}] [{title}](https://arxiv.org/abs/{aid})"
                    f" | `{aid}` | 得分:{p['score']:.0f}"
                )
            lines.append("")

    # 插入统计
    lines.insert(2, f"> 总计: {total_a} 篇 | 已完成: {done} | 待写: {total_a - done}\n")

    todo_path = ROOT / "TODO.md"
    with open(todo_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ TODO.md: {total_a} 篇 A档, {done} 已完成, {total_a - done} 待写")


if __name__ == "__main__":
    main()
