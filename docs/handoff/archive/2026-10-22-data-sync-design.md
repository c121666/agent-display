# 交接 · 数据同步设计（含 token 统计口径）定稿待拍板

> 状态：🟡 待认领　｜　紧急度：常规

## 元信息

| 项 | 值 |
| --- | --- |
| 日期 | 2026-10-22 |
| 交接人 | AI pi（模型 xiaomi/mimo-v2.6-pro，会话 `01a1627d-39c1-75ed-924b-4ed719938547`） |
| 接手人 | 待认领 |
| 分支 | `dispatch-center-only` |
| 基线 commit | `54fbc31`（接手前先 `git checkout dispatch-center-only && git pull` 对齐） |
| 交接原因 | 会话收尾（工作段落完成，设计待用户拍板） |
| 目标状态 | 🟡 进行中 |
| 关联文档 | [2026-10-22-炫彩与上库.md](./2026-10-22-炫彩与上库.md)、`docs/specs/调度中心-数据同步设计.md`、`docs/specs/数字汇报-数据契约.md`、`AGENTS.md` |

## 1. 目标

为调度中心大屏设计「真实数据 → 大屏」的同步管道与 token 统计口径（参考 cc-switch v4.0 用量统计与 magpie usage），产出设计文档供拍板，不动 `index.html` 代码。

**验收标准**（做到这些才算完成）：

- [x] 设计文档落盘：`docs/specs/调度中心-数据同步设计.md`，覆盖采集 / 快照 / 消费三段、token 口径、契约扩展、落地阶段
- [x] token 口径对照 cc-switch / magpie 给出明确取舍（请求计数、TPS、rollup 维度、计费、同步节奏）
- [x] `docs/README.md` 索引补新文档条目
- [ ] 用户对文档第 8 节「待拍板问题」给出结论（**未完成，等拍板**）

## 2. 已完成

- [x] 调研 cc-switch / magpie 的 token 统计实现（验证方式：读 cc-switch `docs/user-manual/zh/4-proxy/4.4-usage.md`、`2.5-usage-query.md` 与仓库树 `src-tauri/src/proxy/usage/`、`database/dao/usage_rollup.rs`；读 magpie `README.md`、`docs/reference.md` usage 章节，2026-10-22 取 main 分支）
- [x] 写 `docs/specs/调度中心-数据同步设计.md`（commit `54fbc31`）：三段式同步管道（沿用《数字汇报-数据契约》推快照模式）、token 双采集路线（A 会话日志解析 / B 网关旁路）、计量口径表、rollup 维度、快照 `tokens` 节 schemaVersion 2 草案、`index.html · monShow()` 三标签映射、P0–P2 落地
- [x] `docs/README.md` 目录索引补条目（commit `54fbc31`）

## 3. 进行中 / 未完成

- [ ] 设计拍板：文档第 8 节 4 个问题（TPS 口径、成本币种、路线 B 是否做、`reasoning_tokens` 去留） · 当前状态：已列出待选方案 · 建议做法：用户逐条拍板后把结论回填到设计文档并在新交接里记录
- [ ] P1 采集器（路线 A：扫会话日志 → rollup → 推 `data/<id>.json`） · 当前状态：未开工（设计先行） · 建议做法：按设计文档第 3.1 / 3.5 节实现，`tools/validate_data.py` 加 `tokens` 节校验
- [ ] 看板侧 `tokens` 节数据源切换 · 当前状态：未开工，`index.html · step()` 仍全模拟 · 建议做法：P1 采集器就绪后再切，缺失态照数据契约第 4 节渲染

## 4. 关键决策与原因

| 决策 | 原因（为什么这么做） | 影响 / 注意 |
| --- | --- | --- |
| 同步管道复用《数字汇报-数据契约》推快照模式，不发明新机制 | 全量快照 + 原子写 + 缺失态口径已定稿，简单可回放 | 契约 `schemaVersion` 将升 2（新增 `tokens` 节），看板对不认识的节忽略 |
| token 口径抄 cc-switch / magpie 的成熟做法 | 请求计数（重试成功不算失败）、缓存命中率、指纹不存密钥等都是踩过坑的口径 | P1 用路线 A（日志解析，零侵入）；路线 B（网关旁路）P2 再评估，可能 YAGNI |
| TPS 取「每秒输出 token 总和」而非 magpie 的「首 token 后输出速度」 | 大屏看总吞吐，无诊断诉求，口径简单直观 | 若日后要诊断慢请求再升级（设计文档第 8 节问题 1） |
| 本次不改 `index.html` | AGENTS.md 边界：视觉/结构大改先出方案；本段落只做设计 | 页面仍是模拟数据 + 「示例数据」标注，属预期状态 |

## 5. 验证状态

本次仅新增 / 修改 Markdown 文档，`index.html` 未改动。

| 验证项 | 结果 | 备注 |
| --- | --- | --- |
| JS 语法（node --check） | ⚠️ 未验证 | index.html 未改动，接手后按需复跑 |
| id 完整性 | ⚠️ 未验证 | 同上 |
| 页面打开无报错 | ⚠️ 未验证 | 同上 |
| 交互（粒子切换 / 全屏 / 悬停） | ⚠️ 未验证 | 同上 |
| 响应式三档 | ⚠️ 未验证 | 同上 |

## 6. 下一步（按顺序执行）

1. 把 `docs/specs/调度中心-数据同步设计.md` 第 8 节 4 个待拍板问题交用户逐条拍板，结论回填文档对应小节。
2. 拍板后开 P1：实现路线 A 采集器（扫 Claude Code `~/.claude/`、Codex `~/.codex/sessions/` 等会话 JSONL → rollup → 原子写 `data/<project-id>.json`），验收：`python tools/validate_data.py data/<id>.json`（需先给该脚本加 `tokens` 节校验）通过。
3. 看板侧把 `index.html · step()` 生成的 mon 面板数据切到快照 `tokens` 节（映射表见设计文档第 5 节），验收：`data/` 缺失 / 字段 null 时按缺失态显示「未接入 / —」，不补 0。
4. 跑 `/skill:verify-dashboard` 全量验证后按提交约定提交，并写新交接链接本文档。

## 7. 风险与已知问题

- 设计未拍板即开工 P1 有返工风险（尤其 TPS 口径与 `reasoning_tokens` 去留）· 影响：采集器字段调整 · 规避：先拍板再动手。
- `file://` 双击打开时 fetch 不到 `data/`（CORS）· 影响：快照模式只在本地静态服务下可用 · 规避：沿用数据契约第 9 节方案 A / B。
- 各 agent 会话日志格式不统一（模型名、usage 字段缺失）· 影响：路线 A 精度 · 规避：模型名归一化 + 缺失字段置 null（cc-switch 同款做法）。

## 8. 环境备注

- 本地预览：`python -m http.server 8000`，访问 `http://localhost:8000`（快照模式必须走本地服务，双击 `file://` 读不到 `data/`）
- 调研用到的上游参考（在线抓取于 2026-10-22）：`github.com/farion1231/cc-switch`（main 分支）、`github.com/yetone/magpie`（main 分支）；其文档链接会漂移，口径以本仓库设计文档摘录为准。
