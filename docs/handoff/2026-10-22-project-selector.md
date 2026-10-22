# 交接 · 数据同步多项目（设置按钮选项目 + 口径修正）

> 状态：🟡 待认领　｜　紧急度：常规

## 元信息

| 项 | 值 |
| --- | --- |
| 日期 | 2026-10-22 |
| 交接人 | AI pi（模型 xiaomi/mimo-v2.6-pro，会话 `01a1627d-39c1-75ed-924b-4ed719938547`） |
| 接手人 | 待认领 |
| 分支 | `dispatch-center-only` |
| 基线 commit | `1e0d566`（接手前先 `git checkout dispatch-center-only && git pull` 对齐） |
| 交接原因 | 会话收尾（多项目支持开发完成，人工冒烟未做） |
| 目标状态 | 🟡 进行中 |
| 关联文档 | [2026-10-22-data-sync-p1.md](./archive/2026-10-22-data-sync-p1.md)（P1 交接，已归档由本文覆盖）、`docs/specs/调度中心-数据同步设计.md`、`docs/specs/数字汇报-数据契约.md`、`AGENTS.md` |

## 1. 目标

用户指出三个 agent（pi / Claude Code / Codex）的会话分属不同项目，需要看板主页加「设置」按钮选项目后再统计。落地：采集器 `--all` 逐项目出快照 + 看板项目选择浮层，并修正一处缺失态口径。

**验收标准**（做到这些才算完成）：

- [x] `py tools/collect_tokens.py --all` 每个项目写一份 `data/<id>.json`，`py tools/validate_data.py data/*.json` 全过
- [x] 看板「设置」按钮弹出项目列表，点选后 mon 面板按该项目统计，刷新后选择仍在（localStorage）
- [x] `/skill:verify-dashboard` 自动检查通过（JS 语法 + id，id 数 20 → 22）
- [ ] 页面冒烟 / 交互 / 响应式人工复核（**未做**，含新浮层）

## 2. 已完成

- [x] 采集器多项目（commit `1e0d566` · `tools/collect_tokens.py · main()/collect()`）：`--all` 按会话 cwd 分组逐项目 rollup + 原子写；同名目录自动加路径 md5 短哈希后缀去重。验证方式：本机实跑出 12 份快照（agent-display / project / admin / mail-workbench / new-chat-* / pi-pro 等），`validate_data.py data/*.json` 12 份全 `[ok]`
- [x] 看板项目选择（commit `1e0d566` · `index.html · renderProjList()/applySel()/curSnap()`）：右上「设置」按钮（`#proj`）弹 `#projPop` 浮层，列表 = 各快照项目名 / 路径 / 今日请求 / lastSync，按 lastSync 倒序；点选存 `localStorage['ops-proj']`，未选或所选项目消失时默认 lastSync 最新；点浮层外自动收起。验证方式：check.py PASS（22 个 id 对齐）；快照读取链路沿用 P1 已验的目录列表解析
- [x] 缺失态口径修正（commit `1e0d566` · `tools/collect_tokens.py · rollup()`）：当日无记录 = 真实 0（原实现灰显「—」与 `requests.total=0` 自相矛盾）；`cacheHitRate` / `successRateToday` 分母为 0 仍置 null。已回填设计文档第 4 节
- [x] 文档同步（commit `1e0d566`）：README（`--all` 用法 + 设置按钮）、CHANGELOG 未发布两条、AGENTS.md（id 20 → 22、结构地图 syncTokens 行）、设计文档口径注记

## 3. 进行中 / 未完成

- [ ] 人工冒烟（页面 / 交互 / 响应式，含新增项目浮层） · 当前状态：未做 · 建议做法：第 6 步第 1 条
- [ ] P2：计费 / 配额面板展示（`today.cost`、`tokens.quota` 已在快照里，面板未渲染；quota 数据有过期项照显不误） · 当前状态：数据侧就绪 · 建议做法：USE 标签加成本行、配额另行设计
- [ ] P2：模型 / agent 分摊、契约 schemaVersion 2 定稿（定稿时同步改 `tools/validate_data.py` 的 `KNOWN_SCHEMA`） · 当前状态：未开工

## 4. 关键决策与原因

| 决策 | 原因（为什么这么做） | 影响 / 注意 |
| --- | --- | --- |
| 项目选择放 localStorage（`ops-proj`），不回写快照 | 看板只读不回写（数据契约总则）；storage 拿不到时选择只本次生效，已 try/catch | 隐私模式下刷新会回到默认项目（lastSync 最新） |
| 同名项目目录加路径 md5 前 6 位后缀 | 本机存在多个 `new-chat` 目录，id 会撞 | 快照文件名如 `new-chat-4ad2dc.json`；换机器路径不同则后缀不同（id 不稳定，做展示够用） |
| 当日无记录 = 真实 0，比率类分母 0 = null | 缺失态的灵魂是「不许把没测的说成 0」，但扫过确实没请求就是 0；比值无意义时才置「—」 | 与数据契约第 4 节「数字 0 必须是真实 0」一致，已写进设计文档第 4 节 |
| `requests` 四计数窗口 = 当日（沿用 P1） | 与「今日成功率」同窗 | 项目列表里「今日请求 0」= 今天没干活，不是没数据 |

## 5. 验证状态

| 验证项 | 结果 | 备注 |
| --- | --- | --- |
| JS 语法（node --check） | ✅ 通过 | `py .pi/skills/verify-dashboard/scripts/check.py` PASS |
| id 完整性 | ✅ 通过 | 22 个 id 对齐（新增 `#proj`、`#projPop`），AGENTS.md 计数已同步 |
| 页面打开无报错 | ⚠️ 未验证 | DevTools 人工冒烟未做；快照读取链路 curl 级已验（P1 交接记录） |
| 交互（设置浮层 / 粒子切换 / 全屏 / 悬停） | ⚠️ 未验证 | 新增浮层的点选 / 外点收起未人工复核 |
| 响应式三档 | ⚠️ 未验证 | 浮层固定右上 264px 宽，窄屏表现未看 |

## 6. 下一步（按顺序执行）

1. 人工冒烟：`py -m http.server 8000` 开服务 → `py tools/collect_tokens.py --all` → 访问 `http://localhost:8000` 确认 ① 点「设置」出 12 项列表、点选后 mon 面板数字与脚注项目名变化、刷新后选择保持 ② 选一个「今日请求 0」的项目，REQ / USE 显示 0 与「—」混合符合口径 ③ Console 无报错、浮层窄屏不溢出。结果回填第 5 节。
2. P2 项按第 3 节逐条推进。
3. 新会话产生后重跑 `py tools/collect_tokens.py --all` 刷新快照（快照是时点数据，不自动更新）。
4. 收尾跑 `/skill:verify-dashboard`，提交并写新交接链接本文档。

## 7. 风险与已知问题

- 快照项目 id 含路径哈希后缀，换机器 / 改目录名后 id 变化 · 影响：localStorage 里存的旧 id 失效 · 表现：自动回退 lastSync 最新项目，不是 bug。
- quota 项是会话日志里最后一次见到的配额，可能已过期（如 `new-chat-2` 显示 2026-10-13 的重置点） · 影响：P2 做配额展示时须带「数据截至 lastSync」提示。
- `file://` 双击读不到 `data/`、本机 `python` 命令损坏（rc=49）要用 `py` · 同 P1 交接第 7 节。

## 8. 环境备注

- 本地预览：`py -m http.server 8000`，访问 `http://localhost:8000`（注意：会话进行中可能已有同端口服务在跑，先 `netstat -ano | grep :8000` 确认）
- 采集全部项目：`py tools/collect_tokens.py --all`（本机 12 个项目约 10-30 秒）；校验：`py tools/validate_data.py data/*.json`
- 本机日志源：`~/.pi/agent/sessions/`、`~/.claude/projects/`、`~/.codex/sessions/`（含 `archived_sessions/`）
