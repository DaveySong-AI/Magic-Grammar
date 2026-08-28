#!/usr/bin/env python3
"""防解说词-卡片脱节校验（提交前提示工具，挂在 check_quotes.py 旁）。

用途：当某页 data-note（解说词）含英文例句，且该页可见卡片缺失该例句核心、
又未打「补充举例（原书未提）」标签时，输出提示，供人工核对是否需补卡。

匹配逻辑（v2，修复 100% 误报）：
- 卡片先去除所有 <span> 等标签、跨 span 拼接英文后整体 norm（小写、标点转空格）
- 解说词英文例句 norm 后与卡片做「最长连续 token 匹配」（LCS）
- 命中规则：最长连续匹配 ≥4 词 或 覆盖例句核心词 ≥50% → 视为已在卡片
- 已打「补充举例」标签的页面视为已处理、直接放行
- 原书例句不强求上卡，脚本仅提示、不阻断提交

用法：python3 check_slide_sync.py [index.html]
"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def norm_text(s):
    """去标签、跨span拼接、转小写、标点转空格、压缩"""
    s = re.sub(r'<[^>]+>', ' ', s)          # 去所有标签（含span）
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s\'\-]', ' ', s)  # 标点转空格
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def extract_en(note):
    """从解说词提取英文句（≥5 词）"""
    segs = re.split(r'[\u4e00-\u9fff，。；：？！、“”（）《》【】…—·「」]', note)
    en = []
    for s in segs:
        s = s.strip()
        if re.search(r'[A-Za-z]', s) and s.count(' ') >= 4:
            en.append(s)
    return en

def longest_run(ex_tokens, vis_tokens):
    """解说词 token 序列在卡片 token 中的最长连续匹配长度"""
    best = 0
    for i in range(len(ex_tokens)):
        for j in range(len(vis_tokens)):
            k = 0
            while (i+k < len(ex_tokens) and j+k < len(vis_tokens)
                   and ex_tokens[i+k] == vis_tokens[j+k]):
                k += 1
            best = max(best, k)
    return best

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

slides = split_slides(content)
print(f"共解析 {len(slides)} 个 slide\n")

MIN_RUN = 4      # 最长连续匹配 ≥4 词 → 判定已在卡片
MIN_RATIO = 0.5  # 或覆盖例句 ≥50% → 判定已在卡片

matched = 0
unmatched = 0
supplemented = 0
for cn, page, note, visible in slides:
    if not note:
        continue
    vis_norm = norm_text(visible)
    vis_tokens = vis_norm.split() if vis_norm else []
    for s in extract_en(note):
        words = s.split()
        if len(words) < 5:
            continue
        ex_tokens = norm_text(s).split()
        if not ex_tokens:
            continue
        run = longest_run(ex_tokens, vis_tokens)
        ratio = run / len(ex_tokens)
        if run >= MIN_RUN or ratio >= MIN_RATIO:
            matched += 1
            continue
        # 未命中：看是否已打补充举例标签
        if '补充举例' in visible or '原书未提' in visible:
            supplemented += 1
            continue
        unmatched += 1
        print(f"⚠️ 第{cn}课 P{page}: 解说词例句「{' '.join(words[:5])}…」未在卡片可见文本"
              f"（最长匹配 {run}/{len(ex_tokens)}），且无「补充举例」标签")

print(f"\n结果：已匹配 {matched} 条，已补卡放行 {supplemented} 条，疑似脱节 {unmatched} 条")
print("提示仅供人工核对，原书例句不强求上卡，不阻断提交。")
sys.exit(1 if unmatched > 0 else 0)
