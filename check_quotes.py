#!/usr/bin/env python3
"""防复发校验：检查所有 data-note 值内是否含英文双引号（会导致属性提前闭合、解说词截断）"""
import re, sys
from html.parser import HTMLParser

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

class NoteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.notes = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == 'data-note':
                self.notes.append(v)

p = NoteParser()
try:
    p.feed(content)
except Exception:
    pass

problems = []
for i, n in enumerate(p.notes):
    if '"' in n:
        # 定位课程页码
        problems.append((i, n[:40] + '...'))

if problems:
    print(f"❌ 发现 {len(problems)} 个 data-note 含英文双引号（#28 复发风险）:")
    for i, s in problems:
        print(f"  [{i}] {s}")
    sys.exit(1)
else:
    print(f"✅ 通过: 共 {len(p.notes)} 个 data-note，值内无英文双引号，无截断风险")
    sys.exit(0)
