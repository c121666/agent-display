# Agent 调度中心大屏 · OPS

一个纯前端的 **AI 智能体调度可视化大屏**（调度中心 · OPS 纸面工程主题）。单文件，无需构建、无需后端，双击即可打开，适合展厅、办公室电视或直播背景。

> 页面中的任务、指标默认是**模拟示例数据**，由内置模拟器生成，并未连接真实 agent 或业务接口。其中「任务 / token 监控」面板可消费本机快照同步真实 token 用量（见「配置 → 数据同步（token 统计）」）；其余面板的真实数据接入需要自行改造，见「配置」一节。

## 功能一览

- **数据飞轮**：左侧汇聚连线与三个任务节点（W01–W05：任务 / 修复 / 优化 / 测试 / 回归，每几秒轮换），中间旋转的代码和执行记录环带，右侧外射谱线，以及齿环、扫光与质检浮层。外圈刻度带秒标（今天第 N 秒，每秒滚动一格）。悬停节点可查看任务详情（汇入提交数 / 进行中 / 测试通过率）。
- **顶部指标**：任务、进行中、任务类、产出、已测试、待复核，以及实时时钟。
- **底部五个面板**：活跃四视图（热力图 / 任务 / 问题 / 测试，下划线标签点击切换；热力图 = git 提交次数 · 单项目：前后端按对显示 ≤2 对、孤行不显示，单体 ≤3 行，方块固定尺寸不拉伸；任务 = 当前任务执行进度（创建分支→规划→执行→测试）；问题 = 复发时间线；测试 = 通过率 + 趋势）、任务日志、任务 / token 监控（吞吐 / 请求 / 用量 3 标签 + 10s 自动轮换，任务标签已并入四视图）、最近动态（决策/日报/问题打字流）、开发统计十二格（提交 / 分支 / 任务 / 开发 / 测试 / 修复 / 回归 / 交接 / 问题 + 代码行数 ± / PR·合并 / 构建，今日口径）。
- **纸面 / 粒子荧光 / 炫彩九套配色**：默认跟随系统深浅色；点「粒子」按钮轮换 11 套配色：纸面 → 粒子 → 炫彩 A–I（A 霓虹赛博 / B 极光 / C 全息宝石 / D 酸性荧光 / E 激光 RGB / F 迈阿密 / G 烈焰熔岩 / H 深海荧光 / I 虹彩）→ 回到纸面。深色画面包含柔光与偶发横向故障效果；炫彩九套为暗底多色（谱线 / 热力图 / 选中标签按语义配色，带辉光），流派出处见 `docs/specs/mockups/主题-炫彩-配色-v0.html`。
- **任务 / token 监控**：3 标签监控面板——吞吐 TPS（token/s 大数字 + 滚动条形图，柱子为条纹线）、请求 REQ（全部 / 成功 / 失败 / 重试成功、缓存命中率）、用量 USE（当前聊天框与当天 token）；点击标签切换，无操作每 10 秒自动轮换（原「任务 TASK」标签已并入四视图面板）。存在 `data/*.json` 快照时自动切到同步数据（每 60 秒刷新，脚注显示 lastSync），缺失字段「—」灰显不补 0；右上「设置」按钮弹出项目选择（多项目各一份快照，选中后按项目统计，选择记在 localStorage）。
- **自适应**：宽屏五列面板，宽度 ≤1100px 时两列，手机竖屏单列。

## 快速开始

### 本地打开

直接双击 `index.html`，用支持 Shadow DOM 和 Canvas 的现代 Chrome / Edge / Safari / Firefox 打开。

也可以任选一种方式启动静态服务器：

```bash
python3 -m http.server 8000
# 或
npx serve .
```

使用 Python 命令后访问 `http://localhost:8000`；使用 `npx serve .` 时访问终端显示的地址。

### 部署到 GitHub Pages

1. 将文件推送到 GitHub 仓库。
2. 在仓库 Settings → Pages 中，将 Source 选为 `Deploy from a branch`，分支选 `main`，目录选 `/ (root)`。
3. 等待部署完成，使用 Pages 设置页提供的地址访问。

也可以部署到其他静态托管服务，无需安装运行时或构建项目。

### 放到大屏上

在电脑或小主机上打开页面，使用浏览器全屏功能（「全屏」按钮或 F11，Mac 为 Ctrl+Cmd+F）。推荐 1920×1080 或更高分辨率。

## 配置（换成你自己的数据）

业务与视觉配置主要位于 `index.html` 的 `mountOps(host, SR)` 挂载函数内。

| 位置 | 配置 | 内容 |
| --- | --- | --- |
| `mountOps(host, SR)` | `CONFIG` | agent 名单（模拟）、任务名称、任务类（W01–W05） |
| `mountOps(host, SR)` | `CODEBITS`、`SPIN`、`SEC_STEP` | 环带代码片段、飞轮转速、秒标间隔（秒） |

配色在 `<template id="tpl-ops">` 内的 `<style>` 中：`:host` 定义纸面配色，`:host([data-theme="dark"])` 和系统深色媒体查询定义粒子荧光配色，`:host([data-theme="glowA–I"])` 定义炫彩九套配色（含热力图多色色阶与选中标签强调色）；Canvas 从这些变量读取颜色。

### 数据同步（token 统计，2026-10-22 起可用）

「任务 / token 监控」面板可消费本机采集的 token 用量快照，口径见 [`docs/specs/调度中心-数据同步设计.md`](docs/specs/调度中心-数据同步设计.md)（已拍板：单采集路线 = 会话日志解析，TPS = 每秒输出 token 总和，成本美元，不单列推理 token）。三步：

```bash
# 1. 采集：扫本机 agent 会话日志（pi / Claude Code / Codex）→ rollup → 原子写 data/<project-id>.json
py tools/collect_tokens.py --all            # 全部项目，每项目一份快照（推荐，看板「设置」里可选项目）
py tools/collect_tokens.py --project-dir .  # 只要当前项目

# 2. 校验（失败不要推送，契约见 docs/specs/数字汇报-数据契约.md）
py tools/validate_data.py data/*.json

# 3. 预览（file:// 双击读不到 data/，面板保持模拟数据）
python3 -m http.server 8000
```

面板三态：无快照 = 模拟示例数据；快照有 `tokens` 节 = 同步真数据（脚注显示项目名 + lastSync）；快照无 `tokens` 节 = 显示「未接入」。字段缺失一律「—」灰显，**不补 0**（当日无记录 = 真实 0，比率类分母为 0 置 null）。点「设置」选项目，选择记在本机 localStorage。`data/` 为真实用量数据，默认不入库（见 `.gitignore`）。

### 接入真实数据的改造方向

当前没有现成的数据连接器或后端服务。下面是改造入口，需要开发者自行实现接口、字段映射、状态更新与错误处理。

- `mountOps` 中的 `tasks`、`agents`、`wfs` 保存模拟状态，`step()` 每 900 毫秒更新，`renderAll()` 刷新面板。可替换模拟更新逻辑，将业务接口返回的数据映射到这些状态；日志可通过 `log(verb, task)` 追加，动作包括 `read`、`build`、`check`、`review`。

## 技术说明

- 单文件 HTML，无构建步骤。原生 JavaScript + CSS + Canvas 2D。
- 大屏由 `<template id="tpl-ops">`、独立 Shadow DOM 与 `mountOps(host, SR)` 函数组成，页面末尾的外壳脚本负责挂载。
- 字体为 Archivo、JetBrains Mono、Noto Sans SC、Michroma，经 Google Fonts 加载。字体无法加载时回退至系统字体；完全离线使用需要自行本地化字体。
- 系统的 `prefers-reduced-motion` 设置不会让大屏默认停住；部分 CSS 动画及故障闪烁仍会降级。
- 部分静态图层使用离屏画布缓存；荧光发光会增加渲染开销。不支持 Canvas 柔光或锥形渐变时，相关效果会降级。

## 目录结构

```text
agent-display/
├── index.html          # 调度中心大屏（HTML + CSS + JS）
├── AGENTS.md           # AI 协作说明
├── README.md
├── CHANGELOG.md
├── tools/
│   ├── collect_tokens.py # 数据同步采集器：会话日志 → data/<id>.json 快照
│   └── validate_data.py  # 快照校验（数据契约 + tokens 节）
├── data/               # 同步快照输出目录（真实用量数据，不入库）
├── docs/
│   └── handoff/        # 交接文档（规则、模板、索引、历史交接）
├── .pi/                # pi 项目配置（/handoff 命令、验证与交接技能）
└── LICENSE             # MIT 许可证
```

版本记录见 [CHANGELOG.md](CHANGELOG.md)。

## 致谢

OPS 纸面工程的视觉风格灵感来自网上流传的 Claude Code「Paper Lab」演示视频（纸面工程图 / 夜间荧光两种风格）。本项目为独立实现，代码和示例数据均为原创，与原视频作者及 Anthropic 没有关联。

DEVELOPED BY @赛博老爸

## 许可证

MIT，详见 [LICENSE](LICENSE)。
