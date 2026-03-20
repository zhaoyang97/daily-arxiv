#!/usr/bin/env python3
"""Generate index.md for each date directory in docs/.

Scans docs/YYYY-MM-DD/*.md, extracts metadata from each note,
and generates a card-style index page.
"""

import os
import re
import glob

DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')

DOMAIN_EMOJI = {
    "图像生成": "🎨", "视频理解": "🎬", "3D视觉": "🧊",
    "目标检测": "🔍", "图像分割": "🎯", "图像修复": "🖼️",
    "自动驾驶": "🚗", "遥感": "🛰️", "人体理解": "👤",
    "医学影像": "🏥", "多模态/VLM": "👁️", "LLM推理": "🧠",
    "LLM Agent": "🦾", "LLM对齐": "⚖️", "LLM效率": "⚡",
    "LLM/NLP": "🗣️", "NLP理解": "📖", "NLP生成": "✍️",
    "模型压缩": "📦", "自监督学习": "🔄", "机器人": "🤖",
    "强化学习": "🎮", "图学习": "🕸️", "语音音频": "🔊",
    "时间序列": "📈", "推荐系统": "📋", "AI安全": "🛡️",
}


def extract_metadata(filepath):
    """Extract title, domain, summary from a note file."""
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    title = ''
    domain = ''
    summary = ''
    in_summary = False

    for i, line in enumerate(lines[:20]):
        line_s = line.strip()
        if line_s.startswith('# ') and not title:
            title = line_s[2:].strip()
        elif '**领域**:' in line_s or '**领域**：' in line_s:
            # Handle both "**领域**: X" and "| **领域**: X" formats
            m = re.search(r'\*\*领域\*\*[:：]\s*(.+?)(?:\s*\||\s*$)', line_s)
            if m:
                domain = m.group(1).strip().rstrip('*')
        elif line_s == '## 一句话总结':
            in_summary = True
        elif in_summary and line_s:
            summary = line_s
            break

    return title, domain, summary


def get_domain_emoji(domain_str):
    """Map domain string to emoji."""
    for key, emoji in DOMAIN_EMOJI.items():
        if key in domain_str:
            return emoji
    return "📄"


def generate_index(date_dir):
    """Generate index.md for a date directory."""
    date = os.path.basename(date_dir)
    notes = sorted(glob.glob(os.path.join(date_dir, '*.md')))
    notes = [n for n in notes if os.path.basename(n) != 'index.md']

    if not notes:
        return

    entries = []
    for note_path in notes:
        title, domain, summary = extract_metadata(note_path)
        if not title:
            continue
        slug = os.path.basename(note_path)
        emoji = get_domain_emoji(domain)
        entries.append((title, slug, domain, emoji, summary))

    lines = [f'# 📅 {date} 精选笔记\n']
    lines.append(f'\n> 共 **{len(entries)}** 篇\n')

    for title, slug, domain, emoji, summary in entries:
        lines.append(f'\n---\n')
        lines.append(f'\n### [{title}]({slug})\n')
        lines.append(f'\n{emoji} {domain}\n')
        if summary:
            lines.append(f'\n{summary}\n')

    lines.append('\n---\n')

    index_path = os.path.join(date_dir, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'  {date}: {len(entries)} papers')


def main():
    date_dirs = sorted(glob.glob(os.path.join(DOCS_DIR, '20*-*-*')),
                       reverse=True)
    for d in date_dirs:
        if os.path.isdir(d):
            generate_index(d)
    print('Done.')


if __name__ == '__main__':
    main()
