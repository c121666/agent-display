# 交接 · 设置浮层项目勾选界面（采集选择 UI 化）+ git 板块定调

> 状态：🟡 待认领　｜　紧急度：常规

## 元信息

| 项 | 值 |
| --- | --- |
| 日期 | 2026-10-22 |
| 交接人 | AI pi（模型 xiaomi/mimo-v2.6-pro，会话 `01a1627d-39c1-75ed-924b-4ed719938547`） |
| 接手人 | 待认领 |
| 分支 | `dispatch-center-only` |
| 基线 commit | `71c4451`（接手前先 `git checkout dispatch-center-only && git pull` 对齐） |
| 交接原因 | 会话收尾（设置勾选界面落地） |
| 目标状态 | 🟡 进行中 |
| 关联文档 | [2026-10-22-opt-in-projects.md](./archive/2026-10-22-opt-in-projects.md)（隐私修正，已归档由本文覆盖）、`docs/specs/调度中心-数据同步设计.md`（第 6 节 + 第 8 节拍板记录）、`AGENTS.md` |

## 1. 目标

用户要求「项目选择应该点击设置后在界面里完成」（原 `--pick` 终端交互不够直观）。落地：设置浮层 = 候选项目勾选界面 +「复制采集命令」按钮；采集器 `--scan` 列候选。并记录用户对 git 板块的定调（见第 4 节）。

**验收标准**（做到这些才算完成）：

- [x] 点「设置」列出全部候选项目（含未采集的），可勾选统计范围、点项目名切换大屏显示
- [x] 「复制采集命令」把勾选项目拼成 `py tools/collect_tokens.py --project-dir ...` 进剪贴板（失败降级 `window.prompt` 手动复制）
- [x] 采集器 `--scan` 出 `data/_candidates.json`（12 个候选）；`--project-dir` 可重复并自动记入勾选清单；空清单默认运行给出两条选法提示
- [ ] 页面冒烟 / 交互 / 响应式人工复核（**未做**，四份交接累积）

## 2. 已完成

- [x] 设置浮层改勾选界面（commit `71c4451` · `index.html · renderProjList()/projCopy`）：候选 = `data/_candidates.json` ∪ 已有快照；勾选存 `localStorage['ops-collect']`（UI 侧记忆）+ 复制命令后由采集器写 `data/_projects.local.json`（执行侧清单）；点勾选框不切大屏项目（label 点击与行点击分流）。验证方式：check.py PASS（23 个 id，新增 `#projCopy`）
- [x] 采集器（commit `71c4451` · `tools/collect_tokens.py · scan()/main()`）：`--scan` 只读会话头 cwd 出候选清单；`--project-dir` 改可重复（`action="append"`）并自动保存勾选清单；`--pick` 废弃删除。验证方式：三步实测——`--scan` 出 12 候选、空清单默认运行提示两条选法、重复传 `--project-dir .` 正常去重出快照过校验
- [x] 文档同步（commit `71c4451`）：README 步骤 1/2 重写（scan + 两种勾选方式）、CHANGELOG、AGENTS.md（id 22 → 23、结构地图、树注释）、设计文档第 6 节与第 8 节拍板记录（选择入口 = 看板设置）

## 3. 进行中 / 未完成

- [ ] 人工冒烟（页面 / 交互 / 响应式，重点：设置浮层勾选 → 复制 → 粘终端全流程） · 四份交接累积未做 · 建议做法：第 6 步第 1 条
- [ ] **`tools/collect_dev.py`（git 数据采集，用户已定调开工范围）** · 当前状态：未开工 · 建议做法：只做热力图（`repos[].daily[].commits`，近 90 天 `git log --numstat`）+ 开发统计客观计数（提交 / 分支行数）；仓库范围复用勾选清单（`data/_projects.local.json` 里的路径当 git 仓库根）；语义类板块（任务 / 问题 / 测试）**不做**，见第 4 节
- [ ] P2：计费 / 配额面板展示（`today.cost`、`tokens.quota` 已在快照里，面板未渲染）
- [ ] P2：模型 / agent 分摊、契约 schemaVersion 2 定稿（定稿时同步改 `tools/validate_data.py` 的 `KNOWN_SCHEMA`）

## 4. 关键决策与原因

| 决策 | 原因（为什么这么做） | 影响 / 注意 |
| --- | --- | --- |
| 选择 UI 化但执行留终端（复制采集命令） | 纯前端单文件页面不能执行本机程序，且边界禁止引后端；用户要「点击设置然后选择」 | 勾选后必须粘命令跑一次才有新快照；`localStorage['ops-collect']` 只是 UI 记忆，真清单以 `data/_projects.local.json` 为准 |
| **推翻**上一份交接的 `--pick` 终端交互选项目 | 用户明确要求在设置界面里选（2026-10-22） | `--pick` 参数已删除，别按归档交接的命令操作 |
| git 板块只做客观计数（用户定调） | `git log` 只能直接给出热力图（提交次数）与开发统计计数；任务 / 问题 / 测试的语义要么靠**规范分支命名**（feat/fix/test 约定）要么靠 **agent 识别**提交记录，直接统计不可靠 | `collect_dev.py` 范围收到热力图 + 计数；语义板块等分支规范或 agent 归类方案定了再说 |

## 5. 验证状态

| 验证项 | 结果 | 备注 |
| --- | --- | --- |
| JS 语法（node --check） | ✅ 通过 | `py .pi/skills/verify-dashboard/scripts/check.py` PASS |
| id 完整性 | ✅ 通过 | 23 个 id 对齐（新增 `#projCopy`），AGENTS.md 计数已同步 |
| 页面打开无报错 | ⚠️ 未验证 | 人工冒烟仍未做 |
| 交互（设置勾选 / 复制命令 / 粒子切换 / 全屏） | ⚠️ 未验证 | 新浮层交互未人工复核 |
| 响应式三档 | ⚠️ 未验证 | 浮层 264px 定宽，窄屏未看 |

## 6. 下一步（按顺序执行）

1. 人工冒烟：`py tools/collect_tokens.py --scan && py -m http.server 8000` → `http://localhost:8000` → 点「设置」：确认 12 个候选都列出、勾选几个后点「复制采集命令」、粘终端跑、刷新后数字与脚注项目名正确、Console 无报错。
2. 开工 `tools/collect_dev.py`（范围见第 3 节）：热力图数据 `repos[].daily[]` 契约字段，快照并入 `data/<id>.json` 同一份（复用原子写与缺失态）；面板热力图 `index.html · renderHeat()` 一类的渲染点切数据源（先读 index.html 对应段再动）。
3. P2 项按第 3 节推进。
4. 收尾跑 `/skill:verify-dashboard`，提交并写新交接链接本文档。

## 7. 风险与已知问题

- 剪贴板 API 在非安全上下文（部分 `file://` 场景）不可用 · 表现：降级 `window.prompt` 手动复制 · 不是 bug。
- 勾选清单两处存储（localStorage「ops-collect」= UI 记忆；`data/_projects.local.json` = 执行清单）可能不同步 · 表现：UI 勾选与上次采集范围不一致 · 以复制命令跑过的那次为准，重开浮层会按快照回勾。
- 热力图口径注意：面板是近 30 天、契约 `repos[].daily` 是近 90 天，接数据时对齐窗口。
- 本机 `python` 命令损坏（rc=49）用 `py`；`file://` 读不到 `data/`。

## 8. 环境备注

- 流程：`py tools/collect_tokens.py --scan`（列候选）→ 看板「设置」勾选 → 复制采集命令粘终端 → `py tools/validate_data.py data/*.json` → `py -m http.server 8000` 看效果
- 本机日志源：`~/.pi/agent/sessions/`、`~/.claude/projects/`、`~/.codex/sessions/`（含 `archived_sessions/`）
