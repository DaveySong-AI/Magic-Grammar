#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析《语法俱乐部题库-修正版.md》 → 生成 question-bank.js
Issue #57：首页新增"题库"入口，22章分类测试 + 错题本联动（独立进度统计）

数据结构：
  window.BANK_DATA = {
    chapters: [{num, title, knowledge, count, note}],
    questions: [{id:"B3-1", ch:3, type:"choice"|"free", q:"题干", opts:[...]|null,
                 ans:"C"|"答案文本", exp:"解析", score: 每章100按题数均分}]
  }

题型判定：
  - 题面含 A/B/C/D 选项 → choice（即时判分）
  - 无选项 → free（作答区 + 参考答案对照，方案A）
  - 第5章练习一：无显式选项，但题意即 A=to V / B=Ving / C=两者皆可 → 由动词生成 3 个选项

已处理的源数据瑕疵：
  - 第12章第1题 "A) ..." 非标准选项格式
  - 第22章第18题答案误写为 "8." → 单调重编号
  - 第3章练习二：答案编号与对话行编号不对应 → 仅保留含空格的句子，按空格顺序匹配答案
"""
import re
import json

MD = "题库/语法俱乐部题库-修正版.md"
OUT = "question-bank.js"

CN = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cn2int(s):
    if '十' not in s:
        return CN[s]
    parts = s.split('十')
    tens = CN.get(parts[0], 1) if parts[0] else 1
    ones = CN.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
    return tens * 10 + ones

def read_lines():
    with open(MD, encoding='utf-8') as f:
        return f.read().split('\n')

def split_chapters(lines):
    blocks = []
    cur = None
    for ln in lines:
        if ln.startswith('## '):
            if cur:
                blocks.append(cur)
            cur = {'header': ln[3:].strip(), 'body': []}
        elif cur is not None:
            cur['body'].append(ln)
    if cur:
        blocks.append(cur)
    merged = []
    for b in blocks:
        m = re.match(r'^第([一二三四五六七八九十]+)章', b['header'])
        num = cn2int(m.group(1)) if m else None
        b['num'] = num
        if merged and merged[-1]['num'] == num:
            merged[-1]['body'] += b['body']
            merged[-1]['header'] = b['header']
        else:
            merged.append(b)
    return merged

def parse_header(header):
    m = re.match(r'^第([一二三四五六七八九十]+)章\s*(.*)$', header)
    if not m:
        return None
    num = cn2int(m.group(1))
    rest = m.group(2).strip()
    note = ''
    mn = re.search(r'[（(]([^）)]*)[）)]$', rest)
    if mn:
        note = mn.group(1).strip()
    title = re.sub(r'\s*[（(].*?[）)]$', '', rest).strip()
    return {'num': num, 'title': title, 'note': note}

def get_knowledge(body):
    for ln in body:
        if '本章知识点' in ln:
            return ln.split('：', 1)[-1].strip()
    return ''

def split_sections(lines, markers=('### 练习一', '### 练习二')):
    sections = []
    cur_label = ''
    cur_lines = []
    for ln in lines:
        t = ln.strip()
        if t in markers:
            sections.append((cur_label, cur_lines))
            cur_label = t
            cur_lines = []
        else:
            cur_lines.append(ln)
    sections.append((cur_label, cur_lines))
    return sections

def extract_prompt(qlines):
    """提取分段中的总题干指令（第一个 **请...** 行），如「请选出最适当的答案填入空格内」"""
    for ln in qlines:
        t = ln.strip()
        m = re.match(r'^\*\*(请.+?)\*\*$', t)
        if m:
            return m.group(1).strip()
    return ''

def extract_ch11_source_note(body):
    """提取第11章 题目来源说明（作为本章总题干）"""
    for ln in body:
        t = ln.strip()
        m = re.match(r'^\*\*题目来源说明\*\*：(.+)$', t)
        if m:
            return m.group(1).strip()
    return ''

def split_ch11_sections(q_area):
    """第11章按 ### 一、### 二、 等主题分段（而非 练习一/二）"""
    sections = []
    cur_label = ''
    cur_lines = []
    for ln in q_area:
        t = ln.strip()
        m = re.match(r'^###\s+(.+)$', t)
        if m:
            if cur_lines or cur_label:
                sections.append((cur_label, cur_lines))
            cur_label = m.group(1).strip()
            cur_lines = []
        else:
            cur_lines.append(ln)
    if cur_lines or cur_label:
        sections.append((cur_label, cur_lines))
    return sections

def normalize_section_label(raw_label, has_multiple):
    """把 split_sections 的原始标签转成展示名：''→'练习一'(多段时)，'### 练习二'→'练习二'"""
    if not raw_label:
        return '练习一' if has_multiple else ''
    return re.sub(r'^###\s*', '', raw_label).strip()

# ---------- 题目解析 ----------
QNUM = re.compile(r'^\s*(\d{1,2})\.\s*(.*)$')
EXNUM = re.compile(r'^\*\*Ex\.(\d{1,2})\*\*\s*(.*)$')
OPTB = re.compile(r'^\s*-\s*\*\*\(([A-D])\)\*\*\s*(.*)$')
OPTQ = re.compile(r'^\s*([A-D])\)\s*(.*)$')

def parse_questions(lines, ch):
    questions = []
    cur = None
    for ln in lines:
        t = ln.strip()
        mq = QNUM.match(ln)
        mex = EXNUM.match(ln) if ch == 11 else None
        mo = OPTB.match(ln)
        if not mo:
            mo = OPTQ.match(ln)
            if mo and re.search(r'\*\*\([A-D]\)\*\*', ln):
                mo = None
        if mq or mex:
            if cur:
                questions.append(cur)
            qnum = int((mq or mex).group(1))
            cur = {'qnum': qnum, 'stem': [(mq or mex).group(2)], 'opts': {}}
        elif mo and cur is not None:
            cur['opts'][mo.group(1)] = mo.group(2).strip()
        elif cur is not None and t:
            cur['stem'].append(t)
    if cur:
        questions.append(cur)
    return questions

def ving_form(v):
    special = {'be': 'being', 'see': 'seeing'}
    if v in special:
        return special[v]
    if v.endswith('ie'):
        return v[:-2] + 'ying'
    if v.endswith('e') and not v.endswith('ee'):
        return v[:-1] + 'ing'
    return v + 'ing'

def clean_stem(s):
    """清理题干：去除 markdown 粗体标记，把下划线跑规范化成可见空格 ____"""
    s = s.replace('**', '').replace('*', '')
    s = re.sub(r'_+', '____', s)
    return re.sub(r'\s+', ' ', s).strip()

# ---------- 答案解析 ----------
ANS_CHOICE = re.compile(r'^\s*(\d{1,2})\.\s*\*\*\(([A-D])\)\*\*\s*(.*)$')
ANS_CHOICE_SP = re.compile(r'^\s*(\d{1,2})\.\s*\(([A-D])\s?\)\s*(.*)$')  # 第22章 "4. (C )"
ANS_NUM = re.compile(r'^\s*(\d{1,2})\.\s*(.*)$')

def parse_answers(lines, ch):
    """返回 {qnum: {'letter','text','exp'}}；答案编号单调递增（修正第22章 '8.' 笔误）"""
    out = {}
    if ch == 11:
        for ln in lines:
            m = re.match(r'^\s*\|\s*Ex\.(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$', ln)
            if m:
                out[int(m.group(1))] = {'letter': None, 'text': m.group(2).strip(),
                                        'exp': m.group(3).strip()}
        return out
    cur = None
    last_num = 0
    for ln in lines:
        t = ln.strip()
        if not t:
            continue
        mc = ANS_CHOICE.match(ln) or ANS_CHOICE_SP.match(ln)
        mn = ANS_NUM.match(ln)
        if mc:
            if cur:
                out[cur['qnum']] = cur
            qnum = int(mc.group(1))
            if qnum <= last_num:      # 单调修正：17 -> 8(误写) -> 18
                qnum = last_num + 1
            last_num = qnum
            cur = {'qnum': qnum, 'letter': mc.group(2), 'text': None, 'exp': mc.group(3).strip()}
        elif mn:
            if cur:
                out[cur['qnum']] = cur
            qnum = int(mn.group(1))
            if qnum <= last_num:
                qnum = last_num + 1
            last_num = qnum
            cur = {'qnum': qnum, 'letter': None, 'text': mn.group(2).strip(), 'exp': ''}
        elif cur is not None:
            cur['exp'] = (cur['exp'] + '\n' + t).strip()
    if cur:
        out[cur['qnum']] = cur
    return out

def ch3_l2_special(qs, answers):
    """第3章练习二：仅保留含空格的对话行，按空格顺序匹配答案（含 "____ see)" 残缺格式）"""
    BLANK = re.compile(r'_{1,}\s*\(?[a-z]+\)')
    def has_blank(q):
        return bool(BLANK.search(' '.join(q['stem'])))
    blank_lines = [q for q in qs if has_blank(q)]
    ans_items = sorted(answers.items())
    used_ans = [a for _, a in ans_items]
    result = []
    ai = 0
    for q in blank_lines:
        s = ' '.join(q['stem'])
        n_blank = len(BLANK.findall(s))
        if n_blank == 0:
            continue
        parts = []
        for _ in range(n_blank):
            if ai < len(used_ans):
                a = used_ans[ai]
                parts.append(a.get('text') or a.get('letter') or '')
                ai += 1
        ans_text = ' / '.join([p for p in parts if p])
        exp = ''
        if ai > 0 and used_ans[ai - 1].get('exp'):
            exp = '\n'.join(x for x in used_ans[ai - 1]['exp'].split('\n')
                            if x.strip() and x.strip() != '---')
        result.append({'qnum': q['qnum'], 'stem': q['stem'], 'opts': {},
                       'ans': ans_text, 'exp': exp})
    return result

# ---------- 主流程 ----------
def main():
    lines = read_lines()
    chapters = split_chapters(lines)
    BANK_CHAPTERS = []
    BANK_QUESTIONS = []
    qa_missing = []
    qa_sample = []

    for blk in chapters:
        num = blk['num']
        header = parse_header(blk['header'])
        if header is None:
            continue
        body = blk['body']
        knowledge = get_knowledge(body)
        ans_idx = None
        for i, ln in enumerate(body):
            if ln.strip() == '### 参考答案':
                ans_idx = i
                break
        if ans_idx is None:
            q_area, a_area = body, []
        else:
            q_area, a_area = body[:ans_idx], body[ans_idx + 1:]

        # 第11章按主题分段（### 一、二、…），其余按 练习一/二 分段
        if num == 11:
            q_sections = split_ch11_sections(q_area)
        else:
            q_sections = split_sections(q_area)
        a_sections = split_sections(a_area)
        a_dict = {label: ls for label, ls in a_sections}

        # 本章总题干：第11章用「题目来源说明」；单分段章用该段指令；多分段章各段自带
        chapter_prompt = ''
        if num == 11:
            chapter_prompt = extract_ch11_source_note(body)

        # 统计有效分段数（含题目的），用于把首段 '' 归一化为「练习一」
        _valid_secs = [s for s in q_sections
                       if any(QNUM.match(l) or (num == 11 and EXNUM.match(l)) for l in s[1])]
        has_multiple = len(_valid_secs) > 1

        if num == 16:
            BANK_CHAPTERS.append({'num': 16, 'title': header['title'],
                                  'knowledge': knowledge, 'count': 0, 'note': '结语'})
            continue

        qlist = []
        for label, qlines in q_sections:
            if not any(QNUM.match(l) or (num == 11 and EXNUM.match(l)) for l in qlines):
                continue
            sec_label = normalize_section_label(label, has_multiple)
            sec_prompt = extract_prompt(qlines)
            qs = parse_questions(qlines, num)
            # 第11章答案为统一表格，不分段；其余按段匹配
            if num == 11:
                alines = a_area
            else:
                alines = a_dict.get(label, [])
            answers = parse_answers(alines, num) if alines else {}

            if num == 3 and label == '### 练习二':
                special = ch3_l2_special(qs, answers)
                for s in special:
                    ans_val = s['ans']
                    qlist.append({
                        'id': 'B3-%d' % (len(qlist) + 1), 'ch': 3, 'type': 'free',
                        'q': clean_stem(' '.join(s['stem'])),
                        'opts': None, 'ans': ans_val, 'exp': s['exp'],
                        'section': sec_label, 'section_prompt': sec_prompt
                    })
                continue

            for q in qs:
                a = answers.get(q['qnum'])
                if not a:
                    qa_missing.append((num, q['qnum']))
                    a = {'letter': None, 'text': '', 'exp': ''}
                stem = clean_stem(' '.join(q['stem']))
                opts = q['opts'] or None
                qtype = 'choice' if opts else 'free'

                if num == 5 and qtype == 'free':
                    m = re.search(r'\(([A-Za-z]+)\)', stem)
                    if m:
                        v = m.group(1).lower()
                        opts = {'A': 'to ' + v, 'B': ving_form(v), 'C': '两者都可以（to V 与 Ving 均可）'}
                        qtype = 'choice'

                # 解析字段
                if qtype == 'choice':
                    ans_val = a.get('letter') or ''
                    exp = (a.get('exp') or '')
                else:
                    # free：答案 = 完整参考答案文本；exp 仅在确实有解析时保留
                    if num == 1:
                        lines = [x for x in (a.get('exp') or '').split('\n')
                                 if x.strip() and x.strip() != '---']
                        ans_val = lines[-1] if lines else ''
                        exp = ''
                    elif num == 6:
                        txt = a.get('text') or ''
                        idx = txt.find('译文')
                        if idx != -1:
                            txt = txt[:idx]
                        ans_val = txt.strip()
                        exp = ''
                    elif num == 11:
                        ans_val = a.get('text') or ''
                        exp = a.get('exp') or ''
                    else:
                        ans_val = ((a.get('text') or '') + ('\n' + a['exp'] if a.get('exp') else '')).strip()
                        exp = ''
                # 清理答案/解析尾部的 markdown 分隔符与空行
                if exp:
                    exp = '\n'.join(x for x in exp.split('\n')
                                    if x.strip() != '---' and x.strip() != '')
                if ans_val:
                    ans_val = ans_val.strip()

                qlist.append({
                    'id': 'B%d-%d' % (num, len(qlist) + 1), 'ch': num,
                    'type': qtype, 'q': stem, 'opts': opts, 'ans': ans_val, 'exp': exp,
                    'section': sec_label, 'section_prompt': sec_prompt
                })

        # 解析字段兜底（Issue #57 需求3）：
        #   优先用逐题解析（第11章来自答案表"要点"列，已在 parse_answers 提取）；
        #   无逐题解析时，用「章节知识点」兜底。
        for q in qlist:
            if not (q.get('exp') or '').strip() and knowledge:
                q['exp'] = knowledge

        count = len(qlist)
        for q in qlist:
            q['score'] = round(100.0 / count, 3) if count else 0
        BANK_QUESTIONS.extend(qlist)
        BANK_CHAPTERS.append({'num': num, 'title': header['title'],
                              'knowledge': knowledge, 'count': count, 'prompt': chapter_prompt,
                              'note': header['note'] if header['note'] and header['note'] != 'Test ' + str(num) else ''})

    data = {'chapters': BANK_CHAPTERS, 'questions': BANK_QUESTIONS}
    js = '/* 由 build_question_bank.py 从 题库/语法俱乐部题库-修正版.md 自动生成 */\n'
    js += 'window.BANK_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n'
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(js)

    # QA
    print('===== QA 报告 =====')
    total = 0
    for ch in BANK_CHAPTERS:
        total += ch['count']
    print('总题数:', total)
    from collections import Counter
    tc = Counter(q['type'] for q in BANK_QUESTIONS)
    print('题型分布:', dict(tc))
    print('缺失答案:', len(qa_missing), qa_missing[:30])
    # 检查 choice 题目答案字母是否在选项内
    bad = []
    for q in BANK_QUESTIONS:
        if q['type'] == 'choice':
            if not q['opts'] or q['ans'] not in q['opts']:
                bad.append((q['id'], q['ans'], list((q['opts'] or {}).keys())))
    print('choice 答案不在选项中:', len(bad), bad[:15])
    print('===== 各章 =====')
    for ch in BANK_CHAPTERS:
        n_c = sum(1 for q in BANK_QUESTIONS if q['ch'] == ch['num'] and q['type'] == 'choice')
        n_f = sum(1 for q in BANK_QUESTIONS if q['ch'] == ch['num'] and q['type'] == 'free')
        print('第%2d章 %-12s 题=%3d (choice=%2d free=%2d) %s' % (ch['num'], ch['title'][:12], ch['count'], n_c, n_f, ch['note'] or ''))
    # 打印少量样例
    print('===== 样例 =====')
    for qid in ['B1-1', 'B3-1', 'B3-11', 'B5-1', 'B11-1', 'B12-1', 'B16-1', 'B21-1', 'B22-18']:
        q = next((x for x in BANK_QUESTIONS if x['id'] == qid), None)
        if q:
            print(json.dumps(q, ensure_ascii=False)[:220])

if __name__ == '__main__':
    main()
