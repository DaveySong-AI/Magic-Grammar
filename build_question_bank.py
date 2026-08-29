#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 题库/TestNN-题目与答案(grammar-club).md 系列（权威数据源）解析 → 生成 question-bank.js
Issue #58：以新上传题库为基准，逐章刷新题目、答案、解析，补全第17-20章下划线标记

知识点仍从旧的 题库/语法俱乐部题库-修正版.md 提取（新文件无知识点列表）。
练习序号（练习一/二等）和题干要求从新文件 ## 分段标题提取。

数据结构：
  window.BANK_DATA = {
    chapters: [{num, title, knowledge, count, prompt, note}],
    questions: [{id:"B3-1", ch:3, type:"choice"|"free", q:"题干", opts:{...}|null,
                 ans:"C"|"答案文本", exp:"解析", score, section, section_prompt}]
  }
"""
import re
import json
import os

BANK_DIR = "题库"
OLD_MD = os.path.join(BANK_DIR, "语法俱乐部题库-修正版.md")
OUT = "question-bank.js"

# ============================================================
# 1. 从旧文件提取章节知识点
# ============================================================
def extract_knowledge():
    """返回 {ch_num: knowledge_str}"""
    knowledge = {}
    if not os.path.exists(OLD_MD):
        return knowledge
    with open(OLD_MD, encoding='utf-8') as f:
        lines = f.read().split('\n')
    cur_ch = None
    for ln in lines:
        # 章节标题: ## 第X章 ...
        m = re.match(r'^##\s+第([一二三四五六七八九十]+)章', ln)
        if m:
            cur_ch = cn2int(m.group(1))
            continue
        # 知识点行
        m = re.match(r'^\*\*本章知识点\*\*[：:]\s*(.+)', ln.strip())
        if m and cur_ch:
            knowledge[cur_ch] = m.group(1).strip()
    return knowledge

CN = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cn2int(s):
    if '十' not in s:
        return CN.get(s, 0)
    parts = s.split('十')
    tens = CN.get(parts[0], 1) if parts[0] else 1
    ones = CN.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
    return tens * 10 + ones

# ============================================================
# 2. 解析单个 TestNN 文件
# ============================================================
def parse_test_file(filepath, ch_num):
    """解析一个 TestNN 文件，返回 (chapter_meta, questions_list)"""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    # 提取章节标题
    title = ""
    for ln in lines[:5]:
        m = re.match(r'^#\s+Test\s*\d+\s*[（(](第[一二三四五六七八九十]+章)\s+(.+?)[）)]', ln)
        if m:
            title = m.group(2).strip()
            break
    if not title:
        for ln in lines[:5]:
            m = re.match(r'^#\s+Test\s*\d+\s*[（(](.+?)[）)]', ln)
            if m:
                title = m.group(1).strip()
                break

    questions = []
    cur_section = ""
    cur_prompt = ""
    cur_q = None
    in_answer = False
    in_explanation = False
    in_table = False
    in_translation = False
    answer_lines = []
    exp_lines = []
    translations = []  # 收集译文段落
    cur_translation = []

    def flush_question():
        nonlocal cur_q, answer_lines, exp_lines, in_answer, in_explanation
        if cur_q is None:
            return
        # 合并答案行
        ans_text = ' '.join(answer_lines).strip()
        exp_text = '\n'.join(exp_lines).strip()
        # 清理答案文本
        ans_text = re.sub(r'^[（(]?[A-E][）)]?\s*', '', ans_text).strip()
        cur_q['ans'] = ans_text if ans_text else cur_q.get('ans_raw', '')
        cur_q['exp'] = exp_text
        # 保留 ans_raw 供后处理使用
        questions.append(cur_q)
        cur_q = None
        answer_lines = []
        exp_lines = []
        in_answer = False
        in_explanation = False

    i = 0
    while i < len(lines):
        ln = lines[i]
        stripped = ln.strip()

        # 译文部分（必须在分段标题之前检测）
        if stripped.startswith('## 译文'):
            flush_question()
            in_translation = True
            i += 1
            continue

        # 分段标题
        if stripped.startswith('## '):
            flush_question()
            section_text = stripped[3:].strip()
            cur_section, cur_prompt = parse_section_header(section_text)
            i += 1
            continue

        # 跳过引用、答案一览等非题目内容
        if stripped.startswith('> ') or stripped.startswith('## 答案') or stripped.startswith('## 五大'):
            i += 1
            continue

        # 题目开始: **1.** 或 **Ex.1** 或 **Ex.1.** 
        m = re.match(r'^\*\*(?:Ex\.)?(\d+)\.?\*\*\s*(.*)', stripped)
        if m:
            flush_question()
            qnum = int(m.group(1))
            qtext = m.group(2).strip()
            # 跳过空的"题目："行（第3章练习二的对话分隔）
            if qtext in ('题目：', '题目:', ''):
                i += 1
                continue
            cur_q = {
                'num': qnum,
                'q': qtext,
                'opts': {},
                'type': 'free',  # 暂定，有选项则改 choice
                'ans_raw': '',
                'wordTypes': [],  # 第6章：词↔类型映射
                'section': cur_section,
                'section_prompt': cur_prompt,
            }
            in_answer = False
            in_explanation = False
            in_table = False
            answer_lines = []
            exp_lines = []
            i += 1
            continue

        # 译文段落收集（必须在 cur_q is None 之前处理）
        if in_translation:
            if stripped:
                cur_translation.append(stripped)
            elif cur_translation:
                translations.append(' '.join(cur_translation))
                cur_translation = []
            i += 1
            continue

        if cur_q is None:
            i += 1
            continue

        # 选项行: - (A) text 或 - A. text
        m_opt = re.match(r'^[-*]\s*\(?([A-E])\)?[\.\)]?\s*(.*)', stripped)
        if m_opt and not in_answer and not in_explanation:
            letter = m_opt.group(1)
            opt_text = m_opt.group(2).strip()
            opt_text = re.sub(r'\s*✅\s*$', '', opt_text).strip()
            cur_q['opts'][letter] = opt_text
            cur_q['type'] = 'choice'
            i += 1
            continue

        # 答案行: **答案：(C)** 或 **答案：A** text 或 **答案（...）：**
        m_ans = re.match(r'^\*\*答案[（(]?[^）)]*[）)]?[：:]\s*\(?([A-E])\)?\s*(.*)', stripped)
        if m_ans:
            in_answer = True
            in_explanation = False
            cur_q['ans_raw'] = m_ans.group(1)
            rest = m_ans.group(2).strip()
            if rest:
                answer_lines.append(rest)
            i += 1
            continue

        # 解析行: **解析：** 内容 或 **解析：**内容
        m_exp = re.match(r'^\*\*解析[：:]\*{0,2}\s*(.*)', stripped)
        if m_exp:
            in_explanation = True
            in_answer = False
            rest = m_exp.group(1).strip()
            if rest:
                exp_lines.append(rest)
            i += 1
            continue

        # free题答案行: &nbsp;&nbsp;&nbsp;&nbsp;答案： 或 &nbsp;&nbsp;&nbsp;&nbsp;**答案（...）：**
        if '&nbsp;' in stripped or stripped.startswith('答案：') or stripped.startswith('答案:'):
            clean = stripped.replace('&nbsp;', '').strip()
            m_free = re.match(r'^\*{0,2}答案[（(]?[^）)]*[）)]?\*{0,2}[：:]\s*(.*)', clean)
            if m_free:
                in_answer = True
                in_explanation = False
                rest = m_free.group(1).strip()
                if rest:
                    answer_lines.append(rest)
                i += 1
                continue

        # 译文部分：## 译文：
        if stripped.startswith('## 译文'):
            in_translation = True
            in_answer = False
            in_explanation = False
            in_table = False
            i += 1
            continue

        # 表格表头：| 序号 | 画底线词 | 类型 |
        if re.match(r'^\|\s*序号\s*\|\s*画底线词\s*\|\s*类型\s*\|', stripped):
            in_table = True
            in_answer = False
            in_explanation = False
            i += 1
            continue

        # 表格分隔行：|---|---|---|
        if in_table and re.match(r'^\|[\s\-|]+\|$', stripped):
            i += 1
            continue

        # 表格数据行：| 1 | living | pp |
        if in_table and stripped.startswith('|'):
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if len(cells) >= 3 and cur_q:
                try:
                    seq = int(cells[0])
                    word = cells[1]
                    wtype = cells[2]
                    cur_q['wordTypes'].append({'num': seq, 'word': word, 'type': wtype})
                except ValueError:
                    pass
            i += 1
            continue

        # 表格结束（遇到非表格行且有题目在处理）
        if in_table and not stripped.startswith('|') and stripped:
            in_table = False

        # 续行
        if in_explanation:
            if stripped:
                exp_lines.append(stripped)
        elif in_answer:
            if stripped and not stripped.startswith('**'):
                answer_lines.append(stripped)
        elif cur_q and stripped:
            # 题目续行（如长段落）
            if not stripped.startswith('-') and not stripped.startswith('**'):
                cur_q['q'] += ' ' + stripped

        i += 1

    flush_question()
    # 处理最后一段译文
    if cur_translation:
        translations.append(' '.join(cur_translation))

    # 后处理：为每题分配 id、score，清理数据
    result = []
    for idx, q in enumerate(questions):
        # 过滤掉非题目（如 "II." 分段标记、纯数字等）
        qtext_raw = q['q'].strip()
        if re.match(r'^[IVX]+\.?$', qtext_raw) or re.match(r'^\d+\.$', qtext_raw):
            continue
        qid = f"B{ch_num}-{q['num']}"
        # choice 题 ans 用字母
        if q['type'] == 'choice':
            ans = q.get('ans_raw', '') or q.get('ans', '')
            ans = re.sub(r'[^A-E]', '', ans)[:1]
        else:
            # free 题：优先用 ans，没有则用解析第一句作为参考答案
            ans = q.get('ans', '') or q.get('ans_raw', '')
            if not ans and q.get('exp'):
                first_line = q['exp'].split('\n')[0].strip()
                ans = first_line[:100]
        # 清理题干：去掉开头的 "题目：N. " 前缀（第17章改写题）
        qtext = re.sub(r'^题目[：:]\s*\d+\.\s*', '', q['q']).strip()
        # 清理解析中的 ** 前缀
        exp = re.sub(r'^\*{1,2}\s*', '', q.get('exp', ''), flags=re.M)
        # 第6章：词类型映射和译文
        word_types = q.get('wordTypes', [])
        translation = translations[idx] if idx < len(translations) else ''
        # 如果有词类型映射，把格式化的映射存入 ans（兼容通用渲染）
        if word_types and not ans:
            ans = '；'.join(f"{wt['word']}→{wt['type']}" for wt in word_types)
        result.append({
            'id': qid,
            'ch': ch_num,
            'type': q['type'],
            'q': qtext,
            'opts': q['opts'] if q['type'] == 'choice' else None,
            'ans': ans,
            'exp': exp,
            'score': 0,  # 后面统一算
            'section': q.get('section', ''),
            'section_prompt': q.get('section_prompt', ''),
            'wordTypes': word_types if word_types else None,
            'translation': translation if translation else None,
        })

    return title, result


def parse_section_header(text):
    """解析 ## 分段标题，返回 (section_label, prompt)
    支持格式：
      练习一 — 题干指令
      练习
      一、主题
      请选出...（单分段无标签）
    """
    text = text.strip()
    # "练习一 — 题干" 格式
    m = re.match(r'^(练习[一二三四五六七八九十]+)\s*[—\-–]\s*(.+)', text)
    if m:
        return m.group(1), m.group(2).strip()
    # "练习一" 无题干
    m = re.match(r'^(练习[一二三四五六七八九十]+)$', text)
    if m:
        return m.group(1), ''
    # "一、主题" 格式（第11章）
    m = re.match(r'^([一二三四五六七八九十]+、.+)$', text)
    if m:
        return m.group(1), ''
    # 纯题干（无标签）
    return '', text


# ============================================================
# 3. 主流程
# ============================================================
def main():
    knowledge_map = extract_knowledge()

    # 收集所有 TestNN 文件
    test_files = []
    for f in sorted(os.listdir(BANK_DIR)):
        m = re.match(r'Test(\d+)-题目与答案', f)
        if m:
            ch_num = int(m.group(1))
            test_files.append((ch_num, os.path.join(BANK_DIR, f)))

    chapters = []
    all_questions = []

    for ch_num, filepath in test_files:
        title, questions = parse_test_file(filepath, ch_num)
        count = len(questions)
        # 分值：每章100分，按题数均分
        score = round(100 / count, 1) if count > 0 else 0
        for q in questions:
            q['score'] = score
        all_questions.extend(questions)

        # 本章总题干（第11章用）
        chapter_prompt = ""
        note = ""
        if ch_num == 11:
            chapter_prompt = "本章练习嵌入在各小节正文中（Ex.1–Ex.55），共 55 题。题型为“选出正确的主谓一致性形式（括弧内为备选动词原形）”。"
            note = "Ex.1–Ex.55"

        chapters.append({
            'num': ch_num,
            'title': title,
            'knowledge': knowledge_map.get(ch_num, ''),
            'count': count,
            'prompt': chapter_prompt,
            'note': note,
        })

    # 按章号排序
    chapters.sort(key=lambda c: c['num'])

    data = {
        'chapters': chapters,
        'questions': all_questions,
    }

    js = f"/* 由 build_question_bank.py 从 题库/TestNN-题目与答案(grammar-club).md 自动生成 */\nwindow.BANK_DATA = {json.dumps(data, ensure_ascii=False)};\n"

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(js)

    # 统计报告
    total = len(all_questions)
    choice_count = sum(1 for q in all_questions if q['type'] == 'choice')
    free_count = total - choice_count
    missing_ans = [q['id'] for q in all_questions if not q['ans']]
    choice_bad = [q['id'] for q in all_questions if q['type'] == 'choice' and q['ans'] and q['ans'] not in q.get('opts', {})]

    print(f"总题数: {total} (选择 {choice_count}, 填空/改写 {free_count})")
    print(f"章节数: {len(chapters)}")
    print(f"缺失答案: {len(missing_ans)} {missing_ans[:10]}")
    print(f"choice 答案不在选项中: {len(choice_bad)} {choice_bad[:10]}")
    print(f"输出: {OUT}")


if __name__ == '__main__':
    main()
