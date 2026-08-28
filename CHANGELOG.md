# 更新日志

## [V1.3.1] - 2026-08-28

### 卡片↔解说词一致性 + 前3页解说词精简（#34–#53，QwenWork agent，7 并行研究 + 串行整合）
逐课（第1–15、17–20、22 课）落实 workbuddy 审核 issue 与其评论中的「P1/P3 精简」：改卡片优先、不动解说词（不重录）；自编例句补卡打「补充举例（原书未提）」标签；确需改的按评论精简 P1/P3 data-note 并登记重录。
- PartA 卡片一致性：补回解说词念到而卡片缺失的例句、卡片↔解说词同页两真相矛盾改卡片对齐、误挂标签订正；「庆祝页未闭合 div」经逐课实测均为抽取截断假象→未改
- PartB P1/P3 精简：20 课封面/引入 data-note 按评论【精简后文案】原样替换（引号统一全角满足 check_quotes），个别卡片删字面重复的欢迎/动机/学法预告句
- 每课跑 check_quotes（全程绿）/check_page_refs/check_slide_sync 回归；check_slide_sync 疑似脱节由 69 降至 42（其余为原书例句不强求上卡，按约定保留）
- 涉及结构「完整教学下移 P4」者（L1/L3/L12/L13/L17/L18/L19）未执行，仅在各 issue 回填标注待产品决定
- 逐课 commit（refs #34–#53，未关闭，评论回填交 workbuddy review）；《TTS待重录清单.md》登记各课 P1/P3

## [V1.3.0] - 2026-08-28

### TTS 音频批量重录（TTS待重录清单全部完成）
- 🎙️ 按 TTS 待重录清单批量重录 44 页女老师讲解音频（覆盖 Issue #8~#32 所有解说词改动），沿用「温柔亲切30岁女老师」音色与统一 prompt
- 🎙️ 覆盖范围：第2课 P8/P9、第3课 P4/P7/P9/P10、第4课 P5、第6课 P11、第7课 P12、第8课 P10、第10课 P2/P3/P6/P7/P10/P12/P13/P14、第12课 P8、第13课 P7/P8、第14课 P10、第15课 P11、第16课 P3/P9、第17课 P9/P11/P14、第18课 P7/P8/P9、第19课 P5/P7、第21课 P7~P13、第22课 P4/P5/P8/P14
- 🔧 新音频 URL 已精确关联到 `allAudioUrls` 对应索引（音频索引用 `currentSlide` 0-based，与 slide 顺序一致；第21课 P7~P13 对应 slide 6~12）
- 📝 生成明细记录于 `tts_urls_generated.json`；TTS 待重录清单 50 条全部标记 ✅ 已完成
- ✅ 校验：check_quotes / check_page_refs / node 语法检查全部通过，44/44 替换位置验证正确

### 自动播放恢复默认开启
- 🔊 语音自动播放恢复默认开启（`ttsAutoPlay = true`），进入课程自动播放讲解并翻页，对儿童更友好
- 🔧 修复自动播开关 UI 与状态不同步问题：初始化时同步 active 状态与图标（开启 ✅ / 关闭 🔄）
- 🛡️ 保留浏览器 autoplay 限制兜底：被拦截时状态栏提示点击页面任意位置后按播放键
- 📖 README 同步更新为「语音讲解默认开启」

## [V1.2.9] - 2026-08-28

### Skill 沉淀（审校期避坑指南）
- 📘 SKILL.md 新增「内容审校与回归避坑指南」章节（第12~18条），沉淀审校 issue #28~#32 的实战经验：
  - 第12条：data-note 属性值内禁止英文直引号（`check_quotes.py` 防复发）
  - 第13条：解说词改了、可见卡片必须同步（`check_slide_sync.py` 核查）
  - 第14条：批量精修改过头/残留旧句/衍字，改后必须逐句回读
  - 第15条：登记页码以 slide 注释标签为准（`check_page_refs.py` 核对），勿用序号推断
  - 第16条：自编例句先补卡打「补充举例」标签，不改解说词（避免重录音频）
  - 第17条：重写解说词后同步维护锚点文字与 TTS 清单登记
  - 第18条：三个校验脚本为防复发防线，改动 index.html 后提交前必跑
- ✅ Bug 验证环节新增 **G. 内容审校回归检查** 清单，把上述检查纳入工作流

## [V1.2.8] - 2026-08-28

### 文档整理（README / CHANGELOG / REQUIREMENTS）
- 📝 README：仓库文档结构补充新增工具脚本（`check_quotes.py` / `check_page_refs.py` / `check_slide_sync.py`）、`TTS待重录清单.md`、宣传海报文件；主要功能补充管理员入口、随堂测试错题直接更正、错题本移出逻辑、原文参考按钮；版本号更新至 V1.2.7；开发协作表更新为审校阶段状态（#1~#6 已关、审校 issue #8~#32 推进）
- 📝 CHANGELOG：V1.2 部分补齐 08-27 遗漏记录——管理员入口、随堂测试与错题本逻辑优化、原文参考外链、3:4 海报二维码位置调整、管理员登录链路 6 项修复、Issue #5 部分完成说明（第6项已完成、第1项随 #28 修复、第2~5项待处理，issue 保持 open）
- 📝 REQUIREMENTS §2.3：删除"TTS 在线合成"（实际实现为预生成音频 CDN 直链 + 变速播放），与实现对齐（Issue #5 第3项建议）
- 🔧 同步修正：README 功能描述"TTS语音合成"→"语速调节"，技术栈"预生成音频+在线TTS"→"预生成音频 CDN 直链 + 变速播放"

## [V1.2.7] - 2026-08-28

### 工具修复（Issue #32 评论遗留工具级待办）
- 🛠 `check_slide_sync.py` v2：修复匹配逻辑失效（原 274 条例句 100% 误报）。改为卡片先去除全部标签、跨 span 拼接英文后整体 norm（小写、标点转空格），再与解说词例句做「最长连续 token 匹配」（LCS），命中规则 ≥4 词或覆盖 ≥50%；已打「补充举例」标签页面自动放行。实测 839 条已匹配、3 条已补卡放行、69 条合理提示（非误报，供人工核对，不阻断提交）
- 🛠 `check_page_refs.py`：第22课P8 锚点由已删除的「"I'm tired," said John」更新为新解说词锚点「the police said（主语加动词的正常顺序）」，8 处锚点核对全部可用
- 📝 TTS待重录清单 #28 行（第22课P8）锚点说明同步更新为现存解说词文字

### 核实（待办3）
- 第22课P9 口语例 "Here comes the bus" 经核实卡片本就存在（① 常见的 there/here 卡片），无需补卡或删句

## [V1.2.6] - 2026-08-28

### 修复（Issue #32：解说词-卡片脱节）
- 🐛 第22课P8：解说词删两组自造例（"I'm tired," said John / "What time is it?" asked the teacher），按课程脚本第五节重排为原书例句：直接引句 "None was killed in the accident," said the police（保留「也可不倒装、句尾 the police said 也对」要点）→ 间接引句 Cholera, warns the WHO, is coming back；"主语是代词不倒装 + they said"保留并加标注「（英文常见如此，原书未提，仅作提醒）」
- 📇 第22课P8：卡片 ⚠️ 行同步加「原书未提，仅作提醒」标注；卡片顺序（None 组在前）与解说词对齐

### 卡片吸收（9 页补卡，均加「补充举例（原书未提）」标签，解说词不动、音频不重录）
- 第11课P12：补 Some of the books / Some of the water（some 视 of 后名词单复数）
- 第11课P13：补 Measles is common / My family is large / My family are all tall / Statistics is a required course
- 第19课P5：补 young/Beijing 例句链（When young ✅ / Being young ✅ / Young ❌ 省过头）
- 第19课P7：补 as if crazy 例（并标注原书对应例 as if trying to hit her）
- 第19课P8：补 doctor 第3例（Being a doctor / As a doctor）
- 第19课P10：补 Having finished his homework 例
- 第7课P8：补 a beautiful small old round yellow Chinese wooden table（美小圆旧黄）
- 第7课P10：补 The news made her happy（标注「由原书 She makes everyone happy 变化」）
- 第13课P10：补 Whoever comes, welcome（与原书 Whoever calls, I won't answer 并列）

### 其他
- 🛠 新增 `check_slide_sync.py` 提交前提示工具：解析解说词英文例句与同页卡片可见文本比对，报告潜在脱节供人工核对（辅助性，不阻断）
- 📝 TTS待重录清单.md 追加 #32 记录（仅第22课P8需重录，9页补卡不涉及音频）

## [V1.2.5] - 2026-08-28

### Bug 修复（回归审校 #28/#29/#30）
- 🐛 Issue #28：修复 8 处 `data-note` 英文直引号导致的解说词截断（`9ed625f` 批量精修引入）。第2课P9、第6课P11、第7课P12、第13课P7、第14课P10、第15课P11、第16课P9、第22课P8——英文引号改为中文「」，属性值完整恢复，溢出乱码清除。新增 `check_quotes.py` 防复发校验（351 个 data-note 全部通过）
- 🐛 Issue #29：修复 5 处"解说词已改但可见卡片未同步"冲突
  - 第3课P4：解说词补限定语"动词短语比较长的时候，里面一定会有be动词"（原书口径）
  - 第3课P9：两处"而是"讹误改回"是"
  - 第12课P8：可见卡片"补语/同位语位置 that 不能省"改"可不省"，与解说词对齐
  - 第13课P8：可见卡片"so that 结果"残留目的句，换回原书真结果句（反锁门例）
  - 第22课P8：根因归 #28 引号截断，随 #28 一并恢复
- 🐛 Issue #30：修复 `9ed625f` 改过头/残留/衍字 3 处
  - 第8课P10：卡片"不影响句子结构"改"去掉只是语气变弱、意思不变"，与 Intensifiers 归位口径一致
  - 第18课P8：卡片"词类/意思都不对"改回原书口径"语法可成立、意思稍异，being 保留「做老师」含义"
  - 第21课P11：删衍字"助动词 why"→"will、can"；"两个要点"改"以下要点"
  - （第5课随堂测试 Q3 设答可议，不在本轮范围，未改动）

### 其他
- 📝 TTS待重录清单.md 追加 #28/#29/#30 修改记录，供统一重录音频

## [V1.2.4] - 2026-08-28

### 内容补录（P2·重要缺失）
- ➕ Issue #8（第2课）：补原书 c02s03 Sunday 对比例——"要判断专有名词不容易，唯一性看语境"：There are five Sundays this month（可复数→非专有）vs an appointment on Sunday（唯一→专有），并铺垫 the John Smith；教案 §四、大纲 P8、课件 P8 同步
- ➕ Issue #9（第3课）：补原书 c03s02 全节唯一"不含 be 动词"的过去完成时例句 Many soldiers had died from pneumonia before the discovery of penicillin.（1928 为箭头截止；had+过去分词），教案 §六、大纲 P10、课件 P10 同步并将"had been"口诀放宽为"had + 过去分词"
- ➕ Issue #20（第14课）：补原书 c14s03 反例 "I like books, whatever the subject, that have illustrations."（成对逗号括的是插入语、从句仍具指示功能仍可用 that，破除"逗号后一律无 that"）与 c14s05 plague 组 "A plague broke out which lasted 20 years."（紧跟先行词反颠三倒四、从句后置更合逻辑），教案 §五、§七 同步
- ➕ Issue #22（第16课）：补原书 c16s01–s02 命名由来——通行术语"非限定从句（Nonfinite Clauses）/非限定动词"及旋元佑改提"简化从句（Reduced Clauses）"的两因、回溯修辞"清楚+简洁"；教案 §二、大纲 P3、课件 P3（新增说明卡 + 解说词延长）同步
- ➕ Issue #24（第18课）：补原书 c18s01 告诫"不定词 to V 不能放在介系词后面（如 used to 后要用 Ving）"；教案 §六、大纲 P9、课件 P9（新增⚠️卡 + 记住行 + 解说词延长）同步
- ➕ Issue #26（第21课）：教案脚本补写"例七：从五个单句到 what to say"整节（原书 c21 五步：as…as 比较级合并→about the possibility→介系词后用 forgetting→what to say）+ 例六"括弧助动词 (will)/(can)"记号说明；课件 P12 例七已在 V1.2.3 换回原句，本次补齐文字讲解

### 内容精修（P3·解说词差异，7 个并行 agent 研究 + 串行整合，共 68 处补丁）
- ✏️ #8 第2课 P9：补 a member / campaign partner 宾补例（"一群当中的一个"）
- ✏️ #9 第3课：P6 补 doorbell"最小时点括弧"例；P13 综合表加"一般动词无 be 时直接变位"注
- ✏️ #11 第5课：P10 being invited 改"被动态省主语不歧义、借 be 变 being"；P12 删绝对化"只能用"+去 5-2 检验法
- ✏️ #12 第6课：P11 who live→who are living、补 being auctioned 例；P12 Having finished 改"had→having 词类变化"、补 pigeon after flying 例（含可见正文）
- ✏️ #13 第7课：P12 换回 Yangmingshan 最高级补语例；P13 换回 chimp I.Q. 倒装"距离—清楚性"（含可见正文）
- ✏️ #14 第8课：P13 补回分离副词推导（Scientifically 还原、逗号来源、honestly 对比）；P14 补 -ly 双音节比较级 more sweetly；P10/P12 加强语气"去掉只是语气变弱、意思不变"
- ✏️ #15 第9课 P3：补四语气"真/不确定/假/想成真"档位一览
- ✏️ #17 第11课：P8 as well as you 改"比较级从句简化"；P14 补三道课堂快答
- ✏️ #18 第12课：P7/P8/P13/P14 修正"that 只看位置"为"看省略后是否清楚"，补 The important thing is…/I am afraid… 可省（含可见正文）
- ✏️ #19 第13课：P7 恢复 If he calls 三重时态 + suppose 假设语气；P8 so that 结果/目的对举
- ✏️ #20 第14课：P10 basket/plague 位置服从清楚（含两张可见卡）；P11 关系副词省略改"看词类、择一省略"+ how/I need 病句对比例
- ✏️ #21 第15课：P5/P11/P14 but also he is→but he is also（三处，含可见正文）；P11 例9 改原书订单 that 对称；P6/P8 例三 fetus"of 可省不可省"（含可见正文）
- ✏️ #22 第16课 P9：删错误示范 The news to leave is true、收回为"主语须空洞/重复"驳斥（含可见正文）
- ✏️ #23 第17课：P8 your brother to do 两步拆解；P12 同位语词类冲突改原书表述
- ✏️ #24 第18课：P6 his 限定词表述；P8 a teacher 语义/词类错框改回"意思稍有出入"
- ✏️ #25 第19课：P4 分词构句段收回（去 P4/P5 重叠）；P9/P10 having finished 完成式讲法、after 省略→Having written 推理；P11 Dangling Modifier 两改法对齐原书
- ✏️ #27 第22课：P7 假设倒装限定 Had/Were/Should；P13/P14 Long live 由"虚拟语气倒装"改回"某些祈使句句型倒装"（含可见正文）
- #10 第4课、#16 第10课、#26 第21课 的 ③ 项经核对已在 P1/P2 涵盖，自动跳过

## [V1.2.3] - 2026-08-28

### Bug 修复
- 🐛 Issue #26：第21课「简化从句练习」5 处严重错误修复（例句被自造/失真替换）
  - 例二（P7）：换回原书 The summer tourists are all gone / The resort town has resumed its air of tranquillity，改用 now that 引导、with + 宾语 + 补语结构
  - 例三（P8）：换回 Confucius 竹简/东周/东汉三句，paper not being available 表原因（删除"when paper was not available"错误等价改写）
  - 例四（P9）：删除自造柏林墙例句，整体换回 Gutenberg 活版印刷三句 + an event 同位语 → marking 概括整件事
  - 例五（P10）：换回 Ben Kook 三句，恢复"at times 已省 → when 不宜省"的交叉教学点
  - 例六（P11）：换回原书三句（I'd like something. / You will meet… / Then you can leave.），补回助动词→to V 推导与 before + 动名词
  - 例七（P12）：脚本缺此例，按语雀原书 c21 补全五句，恢复 as much as I should 比较级、about forgetting、what to say 三个关键步骤
  - 例八（P13）：删除自造"学生考试"七句，换回原书 A. Fries 七句合一（对等省略 he is、名词补语作同位语、team's loss、by+动名词）
  - 5 页幻灯片可见正文与 `data-note` 同步重写；《TTS待重录清单.md》登记第21课 P7–P13 共 7 页待重录
- 🐛 Issue #24：第18课「名词从句简化」3 处严重错误修复
  - ①-1 教案大纲 P13 判断流程图公式写错 → 改为"助动词→to V；进行式 be+Ving→留 Ving；单纯 be/被动态→being（being Ven）；无 be 无助动词→加 -ing→Ving"（课件 P13 本就正确，仅教案）
  - ①-2 解说词 P7 方法三讲乱：删除凭空造的病句 "I am worried about that my son lies to me" 与 "加 of/用 for"，改按原书补出 about the fact 同位语，给 my son's lying／my son lying 两式并比较（可见正文同步）
  - ①-3 解说词 P8 例句破坏简化条件：把 "That I am called a liar／That I am a teacher" 换回原书空泛主语 "That anyone…／That one…"（可见正文同步）；《TTS待重录清单.md》登记第18课 P7/P8 待重录
- 🐛 Issue #23：第17课「定语从句简化」2 处严重错误修复（均在解说词，脚本/大纲本就正确）
  - ①-1 解说词 P9 不定词主动/被动判断去绝对化：删"先行词是发出者→主动、承受者→被动"的一刀切（自举的 a man to trust 恰好推翻自己），改按原书"还原成关系从句、看从句本身语态、不可一概而论"（可见正文同步）
  - ①-2 解说词 P11「形容词的两种位置」纠正：由"名词前／名词后"改回原书"名词短语中／补语位置"二分，恢复"两处都不是→简化形容词从句残留补语"检验，前置/后置降为①内部补充观察；P14 回顾第六条同步（可见正文同步）；《TTS待重录清单.md》登记第17课 P9/P11/P14 待重录
- 🐛 Issue #13：第7课「形容词」脚本第五节 leather/glove 内容·形式说反还原为原书 c07s02（leather 是内容、glove 是形式），仅教案、课件未涉及该论证
- 🐛 Issue #20：第14课「定语从句」脚本第六节关系副词省略，删错误"甚至两个都省略"→按原书 c14s06"择一省略"，并修正"副词性质"表述，仅教案
- 🐛 Issue #9：第3课「动词时态」例句 Bush→Trump（"布什是美国总统"已不成立、"此刻事实"示范失效），恢复原书 c03s01，教案大纲 P7/脚本、课件 P7 可见正文与解说词同步；《TTS待重录清单.md》登记第3课 P7 待重录
- 🐛 Issue #27：第22课「倒装句」比较级倒装第一个条件由"助动词或 do 动词不宜省略"改回原书 c22s01"助动词或 be 动词不宜省略"（do 属助动词之一，原写窄化歪曲条件），教案脚本第二节 + 课件 P4/P5/P14 解说词与可见正文共 6 处；《TTS待重录清单.md》登记第22课 P4/P5/P14 待重录
- 🐛 Issue #25：第19课「状语从句简化之一」按原书 c19s01 六修正"省过头"的光杆补语式：P5 删错误式 "Young, he lived in Beijing" 改列 When young…／Being young…；P7 still 让步式由 "Tired, he still…" 改为 "Being tired, he still…"（解说词+可见正文）；《TTS待重录清单.md》登记第19课 P5/P7 待重录
- 🐛 Issue #14：第8课「副词」术语误用修正：上位类"强调语气的副词"误括注 (Intensifiers) → 删括注/改注 Adverbs of Emphasis，Intensifiers 归位于其下"加强语气的副词"小类（课件 P10 标题/解说词/②小类、P2 学习目标、教案大纲 P10 行与关键词表同步）；《TTS待重录清单.md》登记第8课 P10 待重录

## [V1.2.2] - 2026-08-28

### Bug 修复
- 🐛 Issue #16：第10课「介系词」审校修复
  - **严重错误·预告跳课**：P13/P14 解说词与 PPT 正文、教案大纲 P14、脚本八的"下节课进入第二篇·名词从句"改为"下节课第11课·主语动词一致性（第一篇收官），第12课起进入第二篇复句"；P16 庆祝页原本已正确，未动
  - **解说词 P7**：arrive 例句换回原书反差对比例（We'll arrive at Honolulu 虽大当"中途点"用 at / The home-coming hero arrived in town 虽小表"进入"用 in），替换 station/Taipei 泛例，PPT 正文同步
  - **解说词 P10**：from...to 不再断言"不含端点/通常不含周五/可能不含5点整"，改为"起讫不指明、端点含不含未言明；through 头尾都包括"（对齐原书 c10s04）；P10 正文卡片、P12 对照表、P13 总结口诀同口径修正
  - **备注项**：第10课定位由"第一篇最后一章"改为"简单句理论的收尾章"，消除与第11课"最后一章"的表述冲突（大纲头部、P2 行、脚本一、解说词 P2/P3）；P6"特定日期像面"类比注明为帮助记忆的说法（正文+解说词）
  - 教案（大纲+脚本）与课件同步；《TTS待重录清单.md》登记第10课 P2/P3/P6/P7/P10/P12/P13/P14 共 8 页待重录

## [V1.2.1] - 2026-08-28

### Bug 修复
- 🐛 Issue #10：第4课「不定式短语」审校修复
  - 删除 P14 误植页（整页复制自第1课总结，含错误的"下节课预告：名词词组与冠词"），同步移除 allAudioUrls[4] 对应音频，第4课变为 15 页
  - 互动测试/庆祝页注释顺移为 P14/P15，P1–P13 与大纲逐页一一对应
  - P5「共同点①③」补讲原书 may/might 论证：might 并非 may 的过去式、猜测语气不表过去；新增"听雨/看云"铺垫例句（It must be raining now / It may rain any minute / It might even snow），同步修正解说词与 PPT 正文的绝对化表述
  - 教案同步：大纲 P5 行与脚本第三节按同一口径修订
- ➕ 新增《TTS待重录清单.md》：跟踪各审校 issue 引起的音频重录/废弃需求（本次：第4课 P5 待重录、原 P14 音频废弃）

## [V1.2] - 2026-08-27

### 新增功能
- ✅ 首页免责声明：添加中英文免责声明，说明内容参考自旋元佑老师《英语魔法师之语法俱乐部》，明确非营利用途（Issue #2）
- ✅ 首页作者联系方式：页脚添加两个联系邮箱（songlinjian@163.com / songlinjian@agent.qq.com）（Issue #1）
- ✅ 首页 GitHub 仓库入口：页脚添加可点击的 GitHub 仓库链接（Issue #1）
- ✅ 首页版权信息：页脚添加 Copyright © 2026（Issue #1）
- ✅ 网站二维码：生成标准二维码和分享版二维码（1080×1440，适合朋友圈/小红书），方便分享传播
- ✅ 宣传海报：生成面向儿童的魔法主题宣传海报，含可爱魔法师角色、金色标题、卖点卡片和可扫描二维码，提供 3:4 打印版（1536×2048）和 9:16 手机竖版（1152×2048）两种比例
- ✅ 首页推荐海报功能：首页统计栏新增「推荐海报」按钮，点击弹出海报模态框，支持预览海报、下载 3:4 打印版和 9:16 手机版，手机端提示长按保存或截图分享
- ✅ 管理员入口：首页右下角齿轮进入管理员登录页（用户名 admin / 密码 slj821130），登录后可直接跳转任意课程做页面测试
- ✅ 随堂测试与错题本逻辑优化：① 随堂测试未全对不可翻页，仅能经「庆祝」按钮进入结页 ② 错题可在测试页直接修改更正，更正全对出现庆祝按钮 ③ 错题本仅在「错题本内答对」时移出，不再受随堂测试重做结果影响
- ✅ 首页「原文参考」外链按钮：统计栏最左新增，链接到原书语雀资料（Issue #6）

### 功能优化
- 🔧 新增 `.disclaimer-box` 和 `.site-footer` 样式，与现有魔法主题视觉风格统一
- 🔧 3:4 宣传海报二维码位置上移：参考 9:16 版本比例，置于白色「扫码开始学习」区域居中位置
- 🔧 README 更新：补充实际在线访问地址、二维码引用、仓库文档结构更新
- 🔧 修复 GitHub Pages 无法播放语音：CDN Referer 防盗链导致第三方域名被拒，添加 `<meta name="referrer" content="no-referrer">` 和 `audioPlayer.referrerPolicy='no-referrer'` 双重修复

### Bug 修复
- 🐛 Issue #4：修复互动测试 4 个交互 Bug
  - Bug1：切课时 `quizAnswered`/`quizCorrectCount` 不重置，导致第2课起测试失效 → `showCourse()` 中重置状态并恢复测试页UI
  - Bug2：`id="celebrateBtn"` 在22课中重复，除第1课外全对后庆祝按钮永不显示 → 改为 `class="celebrate-btn"`，用 `closest('.slide').querySelector()` 定位当前页按钮
  - Bug3：`feedbacks` 只定义第1课文案，其他课答题反馈串课显示第1课解析 → key 改为 `课号-题号-选项`，未定义时用通用文案
  - Bug4：`openCourse()` 点开即记录通关，点第一关解锁全部22关 → 通关记录改到 `goToCelebrate()` 中写入（完成课程时通关）
- 🐛 Issue #3：修复第3~22课随堂测试与庆祝页为第2课复制残留
  - 自动解析 `courses/` 下20份随堂测试 md，提取前4道选择题及答案
  - 自动解析20份课程大纲，提取教学目标（证书三行）和下节课预告
  - 逐课替换 P15 互动测试（题干、选项、正确答案）和 P16 庆祝页（课次标题、证书核心知识点、下节课预告）
  - 修复后：第3课考动词时态、第4课考不定词短语...第22课考倒装句
- 🐛 管理员登录链路 6 项修复：const 暂时性死区（TDZ）导致点击课程无反应、openCourse 中 event.currentTarget 问题、管理员模式初始化 slides 未定义、管理员工具栏 CSS display:flex 重复导致始终显示、管理员入口按钮可见性、管理员登录 undefined 改用函数内字符串字面量；登录失败时分别提示用户名/密码错误便于定位
- 🐛 Issue #5：TTS 语音与课程内容一致性核查——`updateSlide()` 空数组保护（防止 slides 为空时崩坏）、`goToSlide()` 增加 `ttsStop()`（翻页时停止上一页语音）；第四优先级清理优化——删除 `file` 死字段、统一课次数字格式
- 🐛 修复 `courseView` 未闭合导致推荐海报模态框不可见的问题

### Issue 关闭
- ✅ Issue #1：首页新增作者联系方式、GitHub 仓库入口与版权信息
- ✅ Issue #2：首页添加免责声明（参考《英语魔法师之语法俱乐部》，非营利用途）
- ✅ Issue #3：第3~22课随堂测试与庆祝页内容为第2课复制残留
- ✅ Issue #4：互动测试交互逻辑 4 个 bug
- 🟡 Issue #5：P1 TTS 语音与课程内容一致性核查——已完成第6项（updateSlide 空数组保护、goToSlide 停止语音、删除 file 死字段、统一课次数字格式）；第1项 P8 截断随 #28 修复；第2~5项（字数上限、TTS 在线合成未实现、自动播放默认、5页抽听）仍未处理，issue 保持 open
- ✅ Issue #6：首页「原文参考」外链按钮

## [V1.1] - 2026-08-26

### 新增功能
- ✅ 错题本功能：自动记录课后习题错题，首页提供错题本入口，支持翻看和重新作答
- ✅ 移动端适配：支持手机/微信打开，响应式布局，顶部控件一行显示，标题不被遮挡
- ✅ 游戏化关卡地图：Kingdom Rush风格三大区域（翠绿森林/冰雪山脉/熔岩火山），AI生成精美地图背景
- ✅ 课程迷你地图：每课第2页显示当前在冒险地图中的位置
- ✅ 返回首页按钮：每课左上角可随时返回关卡选择
- ✅ 关卡解锁状态：已完成关卡插旗，进度统计

### 功能优化
- 🔧 自动翻页逻辑：互动测试页语音播完后不自动翻页，等待学生手动做题；最后一页自动播放
- 🔧 PC/移动端响应式分离：PC端大尺寸充分利用宽度，移动端缩小样式写在@media内
- 🔧 庆祝页可滚动：底部内容不被截断
- 🔧 顶部TTS面板：移动端强制一行显示，按钮文字缩小
- 🔧 句子结构图：移动端不换行，缩小尺寸保证一行显示
- 🔧 庆祝页图片尺寸：从55vw缩小到42vw，避免挤占空间

### Bug修复
- 🐛 修复第2-22课学习目标内容重复的问题
- 🐛 修复音频数组中注释导致URL被截断的问题
- 🐛 修复多余`</div>`导致slide数量不足的问题
- 🐛 修复重复ID导致迷你地图不更新的问题
- 🐛 修复第22课内容多无法滚动的问题
- 🐛 修复测试页自动翻页学生来不及做题的问题
- 🐛 修复移动端顶部拥挤换行遮挡标题的问题
- 🐛 修复"像一座桥"绝对定位元素被截断的问题
- 🐛 修复移动端缩小样式影响PC端显示的问题
- 🐛 修复庆祝页底部内容被截断的问题
- 🐛 修复const变量无法重新赋值的问题

## [V1.0] - 2026-08-25

### 初始版本
- ✅ 22课完整互动HTML课件
- ✅ 每课16页（封面+课程地图+12页内容+互动测试+庆祝页）
- ✅ 女老师语音讲解（每页配套音频）
- ✅ TTS在线语音合成，语速可调
- ✅ 自动播放模式
- ✅ 互动小测试（每课4道选择题）
- ✅ 庆祝结束页（课程完成证书）
- ✅ AI生成插图（封面、内容、庆祝页）
- ✅ 魔法主题视觉设计
- ✅ 单文件HTML交付
