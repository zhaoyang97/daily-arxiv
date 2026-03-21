#!/usr/bin/env python3
"""Rebuild mkdocs.yml nav from docs/ directory structure.

Scans docs/YYYY-MM-DD/*.md, extracts titles, and rewrites the nav
section in mkdocs.yml. Preserves all other config.
"""

import os
import re
import glob
import yaml

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
MKDOCS_YML = os.path.join(BASE_DIR, 'mkdocs.yml')


def get_title(filepath):
    """Extract H1 title from a markdown file."""
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
    return os.path.basename(filepath).replace('.md', '')


def make_short_title(title):
    """Shorten title for nav display: 'Name: Long Subtitle...' → 'Name — Short'."""
    # If title has a colon, use the part before as name + short subtitle
    if ':' in title and not title.startswith('360'):
        parts = title.split(':', 1)
        name = parts[0].strip()
        subtitle = parts[1].strip()
        # Truncate subtitle
        if len(subtitle) > 30:
            subtitle = subtitle[:27] + '...'
        return f"{name} — {subtitle}"
    if len(title) > 45:
        return title[:42] + '...'
    return title


def build_nav():
    """Build nav structure from docs directory."""
    nav = [{'Home': 'index.md'}]

    date_dirs = sorted(glob.glob(os.path.join(DOCS_DIR, '20*-*-*')),
                       reverse=True)

    for date_dir in date_dirs:
        if not os.path.isdir(date_dir):
            continue
        date = os.path.basename(date_dir)
        notes = sorted(glob.glob(os.path.join(date_dir, '*.md')))

        section_items = []

        # Add index.md as section index if exists
        index_path = os.path.join(date_dir, 'index.md')
        if os.path.exists(index_path):
            section_items.append(f'{date}/index.md')

        for note_path in notes:
            fname = os.path.basename(note_path)
            if fname == 'index.md':
                continue
            title = get_title(note_path)
            short = make_short_title(title)
            section_items.append({short: f'{date}/{fname}'})

        if section_items:
            nav.append({date: section_items})

    return nav


def update_mkdocs_yml(nav):
    """Update nav section in mkdocs.yml while preserving other config."""
    with open(MKDOCS_YML, encoding='utf-8') as f:
        config = yaml.safe_load(f)

    config['nav'] = nav

    with open(MKDOCS_YML, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)

    # Count entries
    total = sum(len(v) - 1 for item in nav[1:] for v in item.values())
    dates = len(nav) - 1
    print(f'  nav: {dates} dates, {total} notes')


def main():
    nav = build_nav()
    update_mkdocs_yml(nav)
    print('Done.')


if __name__ == '__main__':
    main()
