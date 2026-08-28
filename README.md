# 🧙‍♂️ 英语魔法师之语法俱乐部 (Magic Grammar)

> 一套专为小学生/初中生设计的互动式英语语法学习课件，22节课从基础句型到高级从句，像玩游戏一样学语法。

## 📚 课程简介

《英语魔法师之语法俱乐部》是一套基于《旋元佑文法》核心知识体系改编的儿童友好版互动课件。通过魔法主题视觉、AI生成插图、女老师语音讲解、互动测试和游戏化关卡地图，让孩子在冒险中掌握英语语法。

- **总课时**：22节课
- **每课页数**：16页（封面+课程地图+12页内容+互动测试+庆祝页）
- **目标受众**：小学高年级 / 初中生

## 🗺️ 三大关卡板块

### 🌲 第一大陆 · 翠绿森林（初级句型篇，第1-11课）
| 课次 | 课程主题 | 核心知识点 |
|------|----------|------------|
| 第1课 | 基本句型及补语 | 五种基本句型、连缀动词、补语、宾补检验法 |
| 第2课 | 名词词组与冠词 | 名词短语三段结构、a(n)=one/the=that语源、专有名词 |
| 第3课 | 动词时态 | 简单式/完成式、进行式、时态一致性 |
| 第4课 | 不定词短语 | to V的用法、不定词与动名词区别 |
| 第5课 | 动名词 | Ving作名词、动名词的被动/完成式 |
| 第6课 | 分词 | 现在分词/过去分词、分词形容词、分词构句 |
| 第7课 | 形容词 | 形容词的位置、比较级/最高级、名词化形容词 |
| 第8课 | 副词 | 副词的种类、位置、比较级 |
| 第9课 | 语气 | 陈述/祈使/虚拟语气、假设法 |
| 第10课 | 介系词 | 介系词短语、空间/时间介系词、固定搭配 |
| 第11课 | 主语动词一致性 | 主谓一致规则、集合名词、并列主语 |

### ❄️ 第二大陆 · 冰雪山脉（中级句型篇，第12-15课）
| 课次 | 课程主题 | 核心知识点 |
|------|----------|------------|
| 第12课 | 名词从句 | that/wh-从句、名词从句的句子成分 |
| 第13课 | 副词从句 | 时间/原因/条件/让步状语从句 |
| 第14课 | 关系从句 | 关系代词who/which/that、限定/非限定从句 |
| 第15课 | 对等连接词与对等从句 | and/but/or、并列结构 |

### 🌋 第三大陆 · 熔岩火山（高级句型篇，第16-22课）
| 课次 | 课程主题 | 核心知识点 |
|------|----------|------------|
| 第16课 | 从属从句简化的通则 | 从句简化原理、主语省略规则 |
| 第17课 | 形容词从句简化 | 关系从句简化为分词/不定词 |
| 第18课 | 名词从句简化 | 名词从句简化为不定词/动名词 |
| 第19课 | 副词从句简化之一 | 时间/条件/原因副词从句简化 |
| 第20课 | 副词从句简化之二 | 让步/目的/结果副词从句简化 |
| 第21课 | 简化从句练习 | 综合练习与辨析 |
| 第22课 | 倒装句 👑BOSS | 完全倒装/部分倒装、倒装句的用法 |

## ✨ 主要功能

- 🎮 **游戏化关卡地图**：Kingdom Rush风格三大区域，22个关卡节点，完成课程插旗解锁
- 🎙️ **女老师语音讲解**：每页配套温柔女老师讲解音频，支持自动播放
- 🔊 **语速调节**：预生成音频支持变速播放（慢/中/快/很快）
- 📝 **互动小测试**：每课4道选择题，即时反馈，未全对不可翻页，全对后经庆祝按钮进入结页
- 📕 **错题本**：自动记录错题，支持随时翻看和重新作答；**在错题本内答对才移出**（随堂测试重做结果不影响错题本记录）
- 🔧 **随堂测试错题直接更正**：测试页可即时修改错题，更正全对出现庆祝按钮
- 📊 **学习进度**：localStorage记录通关进度和错题数据
- 📱 **移动端适配**：支持手机/微信打开，响应式布局
- 🏠 **首页导航**：随时返回首页选择新课程
- 🗺️ **课程迷你地图**：每课第2页显示当前在冒险地图中的位置
- 🔐 **管理员入口**：右下角齿轮登录（admin / slj821130），登录后可跳转任意课程做页面测试
- 🔗 **原文参考**：首页统计栏外链，直达原书语雀资料

## 📁 仓库文档结构

```
Magic-Grammar/
├── index.html              # 主课件文件（单文件，22课全部包含）
├── README.md               # 项目说明文档（本文件）
├── REQUIREMENTS.md         # 需求文档（功能规格说明）
├── CHANGELOG.md            # 版本更新日志
├── SKILL.md                # 课件制作Skill（含Bug验证环节）
├── TTS待重录清单.md         # TTS音频重录跟踪清单（各审校issue登记）
├── check_quotes.py         # 提交前校验：data-note 引号截断防复发
├── check_page_refs.py      # 提交前校验：登记页码与 slide 注释标签一致性
├── check_slide_sync.py     # 提交前提示：解说词例句与卡片可见文本脱节核查
├── Magic-Grammar-QRCode.png       # 网站二维码（标准版）
├── Magic-Grammar-QRCode-Share.png # 网站二维码（分享版，1080×1440）
├── Magic-Grammar-Poster.png       # 宣传海报（3:4 打印版，1536×2048）
├── Magic-Grammar-Poster-9x16.png  # 宣传海报（9:16 手机竖版，1152×2048）
└── courses/                # 22课教案文档
    ├── 第1节课-课程大纲与讲解脚本.md
    ├── 第1节课-随堂测试.md
    ├── 第2节课-课程大纲与讲解脚本.md
    ├── 第2节课-随堂测试.md
    ├── ...
    ├── 第22节课-课程大纲与讲解脚本.md
    └── 第22节课-随堂测试.md
```

## 🚀 使用方法

### 在线访问
🌐 **https://daveysong-ai.github.io/Magic-Grammar/**

📱 手机扫码访问：

![Magic Grammar 二维码](Magic-Grammar-QRCode.png)

### 分享传播
适合发朋友圈/小红书的分享版二维码（1080×1440）：

![Magic Grammar 分享版二维码](Magic-Grammar-QRCode-Share.png)

### 本地使用
1. 下载 `index.html`
2. 双击用 Chrome/Edge/Safari 打开
3. 点击关卡开始学习
4. 语音讲解默认开启，进入课程自动播放语音和翻页；若被浏览器拦截，点击右上角「自动播」或页面任意位置后按播放键即可

## 🛠️ 技术栈

- 纯 HTML + CSS + JavaScript（单文件，无构建依赖）
- AI生成插图（Seedream）
- 语音讲解（预生成音频 CDN 直链 + 变速播放）
- localStorage 本地数据存储
- 响应式设计（PC/移动端自适应）

## 🤝 开发协作 / Development Workflow

本项目采用**多工具协作研发模式**，统一在 GitHub 上进行管理：

| 角色 Role | 工具 Tool | 职责 Responsibility | 状态 Status |
|-----------|-----------|---------------------|-------------|
| 项目管理 / 产品设计 (PM + PD) | **WorkBuddy**（本项目 AI Agent） | 项目管理、需求定制与拆分、issue 跟进 | 🟢 进行中（跟进审校 issue #8~#32） |
| 主力开发 (Dev) | **Doubao Work** | 课件与功能实现、内容审校修复 | 🟢 进行中 |
| 代码审查 (Code Review) | **千问办公（Qwen）** | 代码质量把关 | 🟢 进行中（审校 issue 复验） |

> 需求变更统一通过 GitHub Issue 提交，由 WorkBuddy 作为 PM/PD 跟进落地。功能 issue #1~#4、#6 已关闭；当前处于《旋元佑文法》原书内容审校阶段（issue #5 部分完成待续 + #8~#32，按 P1 严重错误 → P2 重要缺失 → P3 解说词差异 → 回归复验 推进）。

**English**

This project uses a **multi-tool collaboration model**, managed entirely on GitHub:

| Role | Tool | Responsibility | Status |
|------|------|----------------|--------|
| Project Management / Product Design (PM + PD) | **WorkBuddy** (this project's AI Agent) | Project management, requirement definition, issue follow-up | 🟢 In progress (tracking review issues #8–#32) |
| Primary Development (Dev) | **Doubao Work** | Courseware and feature implementation, content review fixes | 🟢 In progress |
| Code Review | **Qwen Office (千问办公)** | Code quality gate | 🟢 In progress (review issue re-verification) |

> Requirement changes are submitted via GitHub Issues and tracked by WorkBuddy as PM/PD. Feature issues #1–#4, #6 are closed; the project is now in the content review phase against 《旋元佑文法》(issue #5 partially done and pending + issues #8–#32, progressing from P1 critical errors → P2 major omissions → P3 narration differences → regression re-verification).

## 📝 版本

- **当前版本**：V1.2.7
- 详见 [CHANGELOG.md](./CHANGELOG.md)

## 📄 许可

本项目仅供学习交流使用。
