# 交接 · 采集改用户勾选项目（--pick，隐私修正）

> 状态：🟡 待认领　｜　紧急度：常规

## 元信息

| 项 | 值 |
| --- | --- |
| 日期 | 2026-10-22 |
| 交接人 | AI pi（模型 xiaomi/mimo-v2.6-pro，会话 `01a1627d-39c1-75ed-924b-4ed719938547`） |
| 接手人 | 待认领 |
| 分支 | `dispatch-center-only` |
| 基线 commit | `53bec43`（接手前先 `git checkout dispatch-center-only && git pull` 对齐） |
| 交接原因 | 会话收尾（隐私修正完成） |
| 目标状态 | 🟡 进行中 |
| 关联文档 | [2026-10-22-project-selector.md](./archive/2026-10-22-project-selector.md)（多项目支持，已归档由本文覆盖）、`docs/specs/调度中心-数据同步设计.md`（第 6 节隐私约定）、`AGENTS.md` |

## 1. 目标

用户指出「采集器不应直接读我全部项目，应由用的人自己选项目」。修正：`--all` 全盘扫描废弃，改为 `--pick` 交互式勾选，**只解析勾选项目的会话内容**。

**验收标准**（做到这些才算完成）：

- [x] `--pick` 只读会话文件头的 cwd 列候选（不读内容），勾选清单存 `data/_projects.local.json`
- [x] 未勾选时默认运行拒绝采集并提示 `--pick`；`--project-dir` 单项目模式不受影响
- [x] 之前全盘扫出的 12 份快照已删除，只保留显式采集的 `agent-display.json`
- [ ] 页面冒烟 / 交互 / 响应式人工复核（仍未做，沿袭前两份交接）

## 2. 已完成

- [x] 采集器 opt-in 改造（commit `53bec43` · `tools/collect_tokens.py · discover()/pick()/main()`）：`--pick` 交互式多选（逗号分隔编号），清单存 `data/_projects.local.json`（`_` 前缀被看板忽略、`data/` 不入库）；默认运行只采清单内项目；`--project-dir` 一次性单项目。验证方式：实测三步——候选列表 12 项正常、空选后默认运行提示「尚未勾选项目。先跑 --pick」、`--project-dir .` 产出 `data/agent-display.json` 过校验
- [x] 隐私边界收紧（commit `53bec43` · `collect()` docstring）：未勾选项目只读会话头的 cwd 用于匹配，不解析会话内容；全盘解析的代码路径已不存在
- [x] 清理未授权数据：删除 `--all` 时期扫出的 12 份快照（含其他项目用量与成本），现 `data/` 仅 `_projects.local.json`（空清单）+ 显式采集的 `agent-display.json`
- [x] 文档同步（commit `53bec43`）：README 四步用法、CHANGELOG 重写多项目条目、设计文档第 6 节加勾选约定、AGENTS.md 树注释、看板浮层提示文案（`--all` → `--pick`）

## 3. 进行中 / 未完成

- [ ] 人工冒烟（页面 / 交互 / 响应式，含设置浮层） · 当前状态：三份交接累积未做 · 建议做法：第 6 步第 1 条
- [ ] 用户自行勾选项目并采集 · 当前状态：`data/_projects.local.json` 是空清单 · 建议做法：跑 `py tools/collect_tokens.py --pick` 按提示选编号
- [ ] P2：计费 / 配额面板展示（`today.cost`、`tokens.quota` 已在快照里，面板未渲染） · 建议做法：USE 标签加成本行
- [ ] P2：模型 / agent 分摊、契约 schemaVersion 2 定稿（定稿时同步改 `tools/validate_data.py` 的 `KNOWN_SCHEMA`）

## 4. 关键决策与原因

| 决策 | 原因（为什么这么做） | 影响 / 注意 |
| --- | --- | --- |
| **推翻**前交接的「`--all` 全盘扫描」，改为 `--pick` 勾选 | 用户明确反对：工具不应直接读全部项目，用的人自己选（2026-10-22） | 之前的 `--all` 参数已删除；README / CHANGELOG 已改，勿按归档交接里的命令操作 |
| 候选列表只读会话文件头的 cwd | 要列候选就得知道有哪些项目；只读头一行是最低披露 | 文件头含会话元数据（时间、cwd），不含对话内容 |
| 勾选清单存 `data/_projects.local.json` | `data/` 已 gitignore 不入库；`_` 前缀被看板 fetch 过滤器跳过 | 换机器 / 清 data/ 后需重跑 `--pick` |
| 看板「设置」浮层保持现状（显示已有快照） | 看板只读不回写，选「采哪些项目」必须在采集器侧做 | 浮层选的是「看哪个项目」，`--pick` 选的是「采哪些项目」，两层选择别混 |

## 5. 验证状态

| 验证项 | 结果 | 备注 |
| --- | --- | --- |
| JS 语法（node --check） | ✅ 通过 | `py .pi/skills/verify-dashboard/scripts/check.py` PASS |
| id 完整性 | ✅ 通过 | 22 个 id 对齐；本次仅改一处提示文案 |
| 页面打开无报错 | ⚠️ 未验证 | 人工冒烟仍未做 |
| 交互（设置浮层 / 粒子切换 / 全屏 / 悬停） | ⚠️ 未验证 | 同上 |
| 响应式三档 | ⚠️ 未验证 | 同上 |

## 6. 下一步（按顺序执行）

1. 人工冒烟：`py -m http.server 8000` → 访问 `http://localhost:8000`，确认设置浮层、Console 无报错、窄屏不溢出（前两份交接遗留，最优先补掉）。
2. `py tools/collect_tokens.py --pick` 按提示勾选你要统计的项目（输编号逗号分隔），再跑 `py tools/collect_tokens.py` + `py tools/validate_data.py data/*.json`。
3. P2 项按第 3 节推进。
4. 收尾跑 `/skill:verify-dashboard`，提交并写新交接链接本文档。

## 7. 风险与已知问题

- `--pick` 是交互式命令（stdin 输入编号），脚本化调用需管道喂输入（如 `printf "6\n" | py tools/collect_tokens.py --pick`）。
- 换机器后勾选清单里的 Windows 路径失效 · 表现：默认运行「选中的项目没扫到会话记录」 · 解决：重跑 `--pick`。
- `file://` 双击读不到 `data/`、本机 `python` 命令损坏（rc=49）要用 `py` · 同前两份交接。

## 8. 环境备注

- 本地预览：`py -m http.server 8000`，访问 `http://localhost:8000`（用前先 `netstat -ano | grep :8000` 确认端口没有旧服务）
- 采集：`py tools/collect_tokens.py --pick`（勾选）→ `py tools/collect_tokens.py`（采集）
- 本机日志源：`~/.pi/agent/sessions/`、`~/.claude/projects/`、`~/.codex/sessions/`（含 `archived_sessions/`）
