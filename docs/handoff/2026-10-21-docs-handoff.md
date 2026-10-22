<!-- 本文件按 HANDOFF-TEMPLATE.md 填写，可作为填写示例。 -->

# 交接 · 项目管理文档体系建立 + 分支现状

> 状态：🟡 待认领　｜　紧急度：常规

## 元信息

| 项 | 值 |
| --- | --- |
| 日期 | 2026-10-21 |
| 交接人 | AI（Claude Code · 本会话） |
| 接手人 | 待认领 |
| 分支 | `dispatch-center-only` |
| 基线 commit | `3081892`（docs 体系与本交接在随后的同一提交中，接手前 `git log --oneline -3` 对齐） |
| 交接原因 | 会话收尾 |
| 目标状态 | 🟡 进行中 |
| 关联文档 | `AGENTS.md`、`docs/README.md`、`docs/handoff/HANDOFF-RULES.md` |

## 1. 目标

为「调度中心单看板」分支建立 AI 项目管理体系：`AGENTS.md`（已建）+ `docs/` 文档体系与 handoff 交接机制（本次），并给出后续补全建议。

**验收标准**：

- [x] `AGENTS.md` 覆盖：项目速览、命令、结构地图、修改约定、验证清单、提交约定、边界
- [x] `docs/` 含 handoff：模板（HANDOFF-TEMPLATE）、规则（HANDOFF-RULES）、索引（README）
- [x] 交接模板规则明确：何时写、怎么写、怎么接、怎么归档
- [x] 有一份按模板填写的真实交接（即本文件）
- [ ] AGENTS.md / README / CHANGELOG 与新目录结构同步

## 2. 已完成

- [x] 分支精简：只保留调度中心看板，移除 SPIDER / NEURAL 与主题切换（commit `b99fa43` · `index.html`）
- [x] `AGENTS.md` + `.gitignore`（commit `3081892`）。校验命令已实测可跑
- [x] `docs/README.md`：文档索引与文档约定
- [x] `docs/handoff/HANDOFF-RULES.md`：交接规则（触发条件、命名、写作 8 条、接手 6 步、归档、AI 特别约定）
- [x] `docs/handoff/HANDOFF-TEMPLATE.md`：交接模板（8 节，含填写说明）
- [x] `docs/handoff/README.md`：交接索引（活跃 / 已归档两张表）
- [x] 验证：`node --check` 通过、23 个 id 全部对应、页面 file:// 打开无报错（见第 5 节）

## 3. 进行中 / 未完成

- [x] AGENTS.md / README / CHANGELOG 同步新目录结构
- [x] ~~冒烟测试 + CI~~ **经用户决定跳过**（2026-10-21）：纯前端演示大屏，人工验证清单已覆盖；将来需要回归再议
- [x] `docs/adr/` 架构决策记录 0001–0003（单文件交付、Shadow DOM 隔离、全模拟数据）
- [x] 版本 tag `v3.1`（本地 tag 已打；推送远程用 `git push origin v3.1`）
- [x] pi 项目设施：`.pi/prompts/handoff.md`（`/handoff` 一键交接）、`.pi/skills/verify-dashboard`（验证清单，含 `scripts/check.py`）、`.pi/skills/handoff-index`（交接索引）、`.pi/APPEND_SYSTEM.md`（项目常驻指令）

## 4. 关键决策与原因

| 决策 | 原因（为什么这么做） | 影响 / 注意 |
| --- | --- | --- |
| 只保留调度中心一款看板 | 用户明确要求，分支 `dispatch-center-only` 即此定位 | 不要恢复多主题 / 主题面板 / three.js（AGENTS.md 边界已写） |
| 交接规则独立成文（RULES + TEMPLATE 分离） | 规则稳定、模板常被复制，混在一起会越改越乱 | 改流程改 RULES，改字段改 TEMPLATE |
| 交接文件放 `docs/handoff/` 并建索引 | 索引让接手者 10 秒内找到最新交接 | 新增 / 归档交接后必须更新索引表 |
| 保留单文件形态 | 交付形态就是单 HTML，双击即用 | AI 想拆文件时先读 AGENTS.md 边界 |
| 不做多 AI 工具兼容层（CLAUDE.md / .cursor/rules / copilot-instructions） | 只用 pi；pi 原生自动发现 `AGENTS.md` 作为上下文文件（pi 文档 configuration.md「Context files」） | 写一份 `AGENTS.md` 就够，别建第二份要同步的文档 |

## 5. 验证状态

| 验证项 | 结果 | 备注 |
| --- | --- | --- |
| JS 语法（node --check） | ✅ 通过 | 2026-10-21，AGENTS.md 中的命令 |
| id 完整性 | ✅ 通过 | 23 个 id 与 `tpl-ops` 一一对应 |
| 页面打开无报错 | ✅ 通过 | file:// 直接打开，飞轮 / 时钟 / 面板正常 |
| 交互（粒子切换 / 全屏 / 悬停） | ⚠️ 部分验证 | 粒子切换已看；全屏、悬停浮层未逐项点过 |
| 响应式三档 | ⚠️ 未验证 | 1920×1080 / 1100px / 竖屏未逐档查看 |

## 6. 下一步（按顺序执行）

1. `git checkout dispatch-center-only && git log --oneline -3` 对齐到基线 commit。
2. 复跑 `AGENTS.md`「验证清单」（尤其第 4、5 条：交互与响应式三档，本交接未验完）。
3. 认领：把本文档「元信息」的接手人填上，状态改「🟡 进行中」。
4. 剩余事项：冒烟测试 + CI 已跳过（见第 3 节），ADR 已建、tag `v3.1` 已打。若将来要复活 CI、接真实数据或推翻现有设计，先读 `docs/adr/README.md` 并重开 ADR 评估。
5. 再次收尾时按模板写**新**交接，链接本文件；本文件闭环后移入 `docs/handoff/archive/`。

## 7. 风险与已知问题

- 无自动化测试，AI 改动全靠人工验证清单兜底 —— 冒烟测试 + CI 已决定跳过，任何改动都要认真跑第 5 节同类验证。
- `README.md` / `AGENTS.md` 中的行数、数量类描述（如"约 900 行""23 个 id"）会随代码漂移，改动代码后记得同步。

## 8. 环境备注

- 单文件纯前端，`file://` 双击即可运行；`python -m http.server 8000` 可选（用完记得停，`server.log` 已被 `.gitignore` 忽略）。
- 外部请求仅 Google Fonts，离线时回退系统字体，属正常现象。
