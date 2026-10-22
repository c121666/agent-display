# 交接 · 数据同步第二波（设置直选目录 + git 采集 + 热力图按时段）

> 状态：🟡 待认领　｜　紧急度：常规

## 元信息

| 项 | 值 |
| --- | --- |
| 日期 | 2026-10-22 |
| 交接人 | AI pi（模型 xiaomi/mimo-v2.6-pro，会话 `01a1627d-39c1-75ed-924b-4ed719938547`） |
| 接手人 | 待认领 |
| 分支 | `dispatch-center-only` |
| 基线 commit | `2edc795`（接手前先 `git checkout dispatch-center-only && git pull` 对齐） |
| 交接原因 | 会话收尾（第二波开发完成） |
| 目标状态 | 🟡 进行中 |
| 关联文档 | [2026-10-22-settings-selection.md](./archive/2026-10-22-settings-selection.md)（已归档由本文覆盖）、`docs/specs/调度中心-数据同步设计.md`（第 4.1 / 6 / 8 节已更新）、`AGENTS.md` |

## 1. 目标

三件事（2026-10-22 用户当轮定）：① 设置选择方式改成**直接选目录、可多选**（否掉「预扫描候选再勾选」）；② 开工 git 数据采集；③ 热力图按用户样图改**按时段视图**（星期 × 小时，行固定、不分前后端）。

**验收标准**（做到这些才算完成）：

- [x] 「设置」浮层直接输入/添加项目目录（可多个、可 ✕ 移除），工具不再预扫描候选（`--scan`/`--pick` 已删）
- [x] 采集器采 git 数据入快照：`repos[]`（契约 6.10）+ `heat`（星期×小时分桶）
- [x] 热力图按时段视图：周一~周日 7 排 × 0-23 时，右上时区、下方「最忙: 周X HH:00」+ 5 档图例；快照有 `heat` 节即真数据
- [ ] 页面冒烟 / 交互 / 响应式人工复核（**未做**，五份交接累积）

## 2. 已完成

- [x] 设置直选目录（commit `2edc795` · `index.html · addDirs()/renderProjList()`）：输入框添加目录（`;` 分隔可一次多个、剥引号）、✕ 移除、清单存 `localStorage['ops-dirs']`；「复制采集命令」拼 `--project-dir` 串；点项目名仍切换大屏显示
- [x] 采集器 git 采集（commit `2edc795` · `tools/collect_tokens.py · git_data()`）：`git log --since=90.days --date=iso-local --numstat` → `repos[].daily`（每日提交/增删行）+ `heat.byHour`（7×24 提交矩阵）+ `heat.busiest` + `heat.tz`；项目目录非仓库时找内嵌子仓库（≤4 个）；非 git 项目省略整节（= 未接入）。验证方式：本机实测快照 `heat` 7×24 总 19 提交、峰值周四 16 点、`repos` 1 仓（branch dispatch-center-only）
- [x] 热力图按时段视图（commit `2edc795` · `index.html · heatHtml()/paintHeatReal()/paintHeatNa()`）：按用户样图（标题「按时段」+ 右上时区 + 周一~周日行 + 0/6/12/18 时标 + 「最忙」+ 少→多 5 档图例）；旧「行成对 / 前后端 ≤2 对」规则与 `heatVisible()`/`HEAT_ROWS` 全删；示例数据形态贴近真实作息（工作时段重、周末轻）
- [x] 校验器支持 `repos`/`heat` 节（commit `2edc795` · `tools/validate_data.py`）；文档同步（README / CHANGELOG / AGENTS.md / 设计文档 4.1 节与拍板记录）

## 3. 进行中 / 未完成

- [ ] 人工冒烟（页面 / 交互 / 响应式，重点：设置添加目录→复制→粘终端、热力图按时段渲染） · 五份交接累积未做 · 建议做法：第 6 步第 1 条
- [ ] 色阶阈值 1/3/6/10 与图例 5 档是自定的（样图没给数值） · 建议做法：用户看效果后微调 `index.html · HEAT_LV`
- [ ] 语义类板块（任务 / 问题 / 测试视图、最近动态）：git 直采不可靠，需**规范分支命名**（feat/fix/test 约定）或 **agent 识别**提交记录（2026-10-22 用户定调，先不做）
- [ ] P2：计费 / 配额面板展示（`today.cost`、`tokens.quota` 数据已在快照）
- [ ] P2：模型 / agent 分摊、契约 schemaVersion 2 定稿（定稿时同步 `validate_data.py` 的 `KNOWN_SCHEMA`）

## 4. 关键决策与原因

| 决策 | 原因（为什么这么做） | 影响 / 注意 |
| --- | --- | --- |
| **推翻**「预扫描候选 + 勾选」，改为用户直接输入目录 | 用户：不能先读了本地项目再让人勾选；要直接选目录、可多选（2026-10-22） | `--scan`/`--pick`/`_candidates.json` 全删；工具只碰用户给的目录（`collect()` 仍读各日志文件头一行做 cwd 匹配，这是最低限度） |
| 热力图按时段（星期×小时 7×24），**不分前后端** | 用户附样图定稿（标题「按时段」/ 时区 / 最忙 / 5 档图例）；「几排就固定了」= 行固定 7 排 | 旧「行成对 / 前后端 ≤2 对 / 单体 ≤3 行」规则废除（设计文档第 8 节有记录）；数据节从按日改为 `heat` 分桶 |
| git 采集并入 `collect_tokens.py`（不建 `collect_dev.py`） | 快照一份、id 规则一套、原子写一处，避免两工具写同一文件的合并逻辑 | 工具名带 tokens 但已含 git 数据，文档已注明；将来数据源多了再考虑改名 |
| 色阶分档 1/3/6/10、时区显示 `UTC+08:00` | 样图未给数值阈值；IANA 时区名跨平台取不到（无依赖前提），偏移量诚实 | 阈值在 `index.html · HEAT_LV` 一行可调；想要「Asia/Shanghai」字样需引入时区映射 |

## 5. 验证状态

| 验证项 | 结果 | 备注 |
| --- | --- | --- |
| JS 语法（node --check） | ✅ 通过 | `py .pi/skills/verify-dashboard/scripts/check.py` PASS |
| id 完整性 | ✅ 通过 | 25 个 id 对齐（新增 `#projPath`/`#projAdd`），AGENTS.md 计数已同步 |
| 采集链路 | ✅ 通过 | 实测：采集 → `validate_data.py` `[ok]`，`heat` 7×24 / `repos` 内容正确 |
| 页面打开无报错 | ⚠️ 未验证 | 人工冒烟未做 |
| 交互（设置添加目录 / 复制命令 / 热力图悬停） | ⚠️ 未验证 | 同上 |
| 响应式三档 | ⚠️ 未验证 | 热力图改 24 列后窄屏未看 |

## 6. 下一步（按顺序执行）

1. 人工冒烟：`py tools/collect_tokens.py --project-dir .` → `py -m http.server 8000` → `http://localhost:8000`：确认 ① 热力图按时段渲染（7 排、时区、最忙、图例）且数字与 git 实况对得上 ② 设置浮层添加目录 → 复制采集命令 → 粘终端全流程 ③ Console 无报错、~1100px 与手机竖屏不溢出。
2. 用户确认热力图色阶观感，需调则改 `index.html · HEAT_LV`（一行）。
3. 语义类板块等「规范分支 / agent 归类」方案定了再动（见第 3 节）。
4. P2 项推进；收尾跑 `/skill:verify-dashboard`，提交并写新交接链接本文档。

## 7. 风险与已知问题

- 热力图小时桶按 git **作者时间**（%ad）本地时区归档 · 影响：改过系统时区的历史提交会落到别的格 · 可接受。
- `heat.busiest` 只算峰值格，多峰并列只显示第一个 · 样图如此，够用。
- 快照 id 含路径哈希后缀的规则沿用前交接；`file://` 读不到 `data/`、本机 `python` 命令损坏（rc=49）用 `py`。

## 8. 环境备注

- 流程：看板「设置」添加项目目录 → 复制采集命令粘终端（或直接 `py tools/collect_tokens.py --project-dir <路径>`）→ `py tools/validate_data.py data/*.json` → `py -m http.server 8000`
- 样图语义备忘（用户 2026-10-22 提供）：行=周一~周日、列=0-23 时、右上 Asia/Shanghai（现实现 UTC+08:00）、左下「最忙: 周二 17:00」、右下「少 ▢▢▢▢▢ 多」
