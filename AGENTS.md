# AGENTS.md — 项目约定

## GitHub 操作署名规范（用户要求，2026-08-28 确认）

对本仓库（DaveySong-AI/Magic-Grammar）执行任何 GitHub 操作时，默认署名：

> **「Davey's Doubao agent」**

适用场景包括但不限于：
- issue 创建 / 评论 / 关闭时的落款（如 `— Davey's Doubao agent`）
- Pull Request 的描述与评论落款
- commit message 中的署名行（如需，可加 `Signed-off-by: Davey's Doubao agent`）
- 其他对外可见的 GitHub 操作文本

## 其他既有约定（从历史操作沉淀）

- 仓库通过 SSH（`git@github.com:DaveySong-AI/Magic-Grammar.git`）推送，无 gh CLI / token 时优先用 git。
- 修改代码/解说词后需同步更新 `CHANGELOG.md` 与 `README.md`（如需）。
- 解说词改动且涉及音频的，登记到 `TTS待重录清单.md`，等统一重录。
- 内容审校避坑规范见 `SKILL.md`「内容审校与回归避坑指南」章节。
