#!/usr/bin/env python3
"""防页码错位：给定 data-note 中的锚点关键词，输出其所在 slide 的注释页码标签。
用于核对 CHANGELOG / TTS 清单登记页码是否与实际 slide 注释一致。"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def find_page(anchor):
    idx = content.find(anchor)
    if idx == -1:
        return f"❌ 找不到锚点 [{anchor}]"
    before = content[:idx]
    comments = list(re.finditer(r'<!--\s*=+\s*P\s*(\d+)\s*[^>]*?-->', before))
    if comments:
        return f"锚点[{anchor[:15]}...] → {comments[-1].group(0).strip()}"
    return f"锚点[{anchor[:15]}...] → 无前向注释"

if __name__ == '__main__':
    # 默认核对 #28 的 8 处
    anchors = [
        '交代是「一名」委员',      # 第2课
        '就有「完成」的暗示',       # 第6课
        'the指的是「那一个」风景区', # 第7课
        '自然说「在睡觉」',         # 第13课
        '想说「篮子里',             # 第14课
        '「但加工程序低科技」',      # 第15课
        '「空洞或与主句重复」',      # 第16课
        'the police said（主语加动词的正常顺序）', # 第22课 P8（#32 改写后新锚点，原"I'm tired"例已删）
    ]
    for a in anchors:
        print(find_page(a))
