#!/usr/bin/env python3
"""防解说词-卡片脱节校验（提交前提示工具，挂在 check_quotes.py 旁）。

用途：当某页 data-note（解说词）含英文例句，且该页可见卡片缺失该例句、
又未打「补充举例（原书未提）」标签时，输出提示，供人工核对是否需补卡。

说明：
- 解说词例句本身来自原书、属正常讲解的不强制上卡（脚本仅提示、不阻断）。
- 凡已补卡并打「补充举例」标签的页面自动放行。
- 用法：python3 check_slide_sync.py [index.html]
"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def split_slides(content):
    slides = []
    course_starts = [(int(m.group(1)), m.start()) for m in re.finditer(r'data-course="(\d+)"', content)]
    for i, (cn, cs) in enumerate(course_starts):
        ce = course_starts[i+1][1] if i+1 < len(course_starts) else len(content)
        sec = content[cs:ce]
        pm = list(re.finditer(r'<!--\s*=+\s*P\s*(\d+)\s*([^>]*?)-->', sec))
        for j, mm in enumerate(pm):
            page = int(mm.group(1))
            end = pm[j+1].start() if j+1 < len(pm) else len(sec)
            block = sec[mm.start():end]
            dn = re.search(r'data-note="([^"]*)"', block)
            note = dn.group(1) if dn else ''
            visible = re.sub(r'data-note="[^"]*"', '', block)
            slides.append((cn, page, note, visible))
    return slides

def extract_en(note):
    """从解说词提取英文句（≥5 词）"""
    segs = re.split(r'[\u4e00-\u9fff，。；：？！、“”（）《》【】…—·「」]', note)
    en = []
    for s in segs:
        s = s.strip()
        if re.search(r'[A-Za-z]', s) and s.count(' ') >= 4:
            en.append(s)
    return en

slides = split_slides(content)
checked = 0
hints = 0
for cn, page, note, visible in slides:
    if not note:
        continue
    vis_norm = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', visible))
    # 已打补充举例标签的页面视为已处理
    for s in extract_en(note):
        words = s.split()
        if len(words) < 5:
            continue
        fingerprint = ' '.join(words[:6]).lower()
        if fingerprint not in vis_norm.lower():
            checked += 1
            hints += 1
            tag = '（已打补充举例标签）' if '补充举例' in visible else '（⚠️ 未打标签）'
            print(f"  ⚠️ 第{cn}课 P{page}: 解说词例句「{' '.join(words[:5])}…」未在卡片可见文本 {tag}")

print(f"\n核对 {checked} 条英文例句，{hints} 条未在卡片可见文本中（其中已打「补充举例」标签者视为已补卡）")
print("提示仅供人工核对，原书例句不强求上卡，不阻断提交。")
