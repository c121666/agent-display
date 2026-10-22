# AGENTS.md

给 AI 编码助手（Codex / Claude Code / Cursor / Gemini CLI / pi 等）阅读的仓库工作说明。修改本仓库前先读完本文件，再读 `README.md`（面向人的完整文档）。

## 项目速览

- **产品**：Agent 调度中心大屏（OPS 纸面工程风格）——AI 智能体调度可视化大屏，展示任务流、智能体接力、执行记录与产出。
- **形态**：纯前端**单文件** HTML（`index.html`，约 1200 行 = HTML + CSS + JS）。无构建步骤、无后端、无包管理器、无框架。
- **数据**：全部为**模拟示例数据**，由内置模拟器生成，页面上标注「示例数据」。不连接任何真实接口。
- **分支定位**：本分支 `dispatch-center-only` 只保留调度中心一款看板。**不要**重新引入多主题（SPIDER / NEURAL）、主题切换面板或 three.js 等 CDN 脚本。

## 常用命令

```bash
# 本地预览（任选其一；或直接双击 index.html，file:// 即可运行）
python -m http.server 8000        # 访问 http://localhost:8000
npx serve .

# 校验 JS 语法（仓库无测试框架，提交前至少做这一步）
python -c "import re;open('_c.js','w',encoding='utf-8').write(re.search(r'<script>(.*)</script>',open('index.html',encoding='utf-8').read(),re.S).group(1))" && node --check _c.js && rm _c.js
```

无单元测试、无 lint 配置。修改后必须人工验证的项目见「验证清单」。

## 目录结构

```text
agent-display/
├── index.html          # 全部代码（HTML + CSS + JS），入口即交付物
├── AGENTS.md           # 本文件：AI 协作说明
├── README.md           # 面向人的文档（功能、部署、配置、改造方向）
├── CHANGELOG.md        # 版本记录（Keep a Changelog 风格）
├── tools/
│   ├── collect_tokens.py # 数据同步采集器：会话日志 → data/<id>.json 快照（token 统计；只采用户 --pick 勾选的项目）
│   └── validate_data.py  # 快照校验（数据契约 + tokens 节）
├── data/               # 同步快照输出目录（真实用量数据，不入库）
├── docs/
│   ├── README.md       # 文档索引与文档约定
│   └── handoff/        # 交接文档：规则、模板、索引、活跃交接、archive/
├── .pi/                # pi 项目配置（项目信任后生效）
│   ├── APPEND_SYSTEM.md        # 项目常驻指令
│   ├── prompts/handoff.md      # /handoff 一键写交接
│   └── skills/                 # verify-dashboard（验证清单）、handoff-index（交接索引）
└── LICENSE             # MIT
```

## index.html 结构地图

| 区块 | 位置 | 内容 |
| --- | --- | --- |
| head | 文件开头 | 基础样式、`<title>`、Google Fonts 引入（唯一的外部请求）、外壳 CSS（`.th-host`） |
| `<!-- 调度中心 · OPS ... -->` | host 容器 | `<div id="host-ops">`：Shadow DOM 的宿主 |
| `<template id="tpl-ops">` | 主体 | 看板全部结构 + 样式：`:host` 内的配色变量（纸面 / 粒子荧光 / 炫彩 A–I）、顶部指标、Canvas 舞台、底部五面板（活跃四视图：热力图 / 任务 / 问题 / 测试 · 任务日志 · 任务与 token 监控 · 最近动态 · 开发统计） |
| `<script>` | 文件末尾 | 见下 |

脚本内部分工：

| 符号 | 职责 |
| --- | --- |
| `mountOps(host, SR)` | 唯一的挂载函数，所有看板逻辑都在里面 |
| `CONFIG` | 业务文案配置：agent 名单、任务名、工作流名 |
| `CODEBITS` / `SPIN` | 飞轮环带的代码片段 / 飞轮转速 |
| `tasks` / `agents` / `wfs` | 模拟状态。接真实数据时替换这里的初始化与推进逻辑 |
| `step()`（900ms）/ `renderAll()` | 模拟推进 / 面板刷新 |
| `layoutStage()` / `drawStage(t, dt)` | Canvas 舞台（数据飞轮）布局与绘制 |
| `monShow()` / `tpsPaint()` | 任务 / token 监控面板（3 标签、点击与 10s 自动轮换、吞吐滚动图） |
| `syncTokens()` / `paintTokens()` / `renderProjList()` | 数据同步：扫 `data/*.json` 快照 → mon 面板三态（无快照=演示 / 有 tokens 节=同步 / 无 tokens 节=未接入），60s 轮询，缺失字段「—」灰显；「设置」按钮（`#proj` / `#projPop`）选项目，选择记 localStorage |
| `actTick()` / `renderAct()` | 最近动态面板（决策/日报/问题逐条打字滚动） |
| 外壳 IIFE（文件末尾） | `attachShadow` → 克隆 `tpl-ops` → 调用 `mountOps`。**只挂载这一款看板，不要往里加切换逻辑** |

## 修改约定

1. **保持单文件**。不引入构建工具、打包器、框架、npm 依赖。代码再长也不拆文件（交付形态就是单 HTML）。
2. **样式隔离**。看板样式写在 `<template>` 内的 `<style>` 里，用 `:host` / `:host([data-theme=...])` 代替 `:root`；JS 里用 `SR.querySelector` 查询元素。禁止把主题样式写到外壳 style。
3. **id 同步**。JS 引用的元素 id（`$('#xx')` / `getElementById`）与模板内 `id="xx"` 必须一一对应，当前共 22 个。增删 id 时两边同步改，并跑一遍「验证清单」第 1 条。
4. **外部依赖只允许 Google Fonts**（Archivo / JetBrains Mono / Noto Sans SC / Michroma）。不新增 CDN 脚本、不引入第三方库；字体加载失败时须能回退系统字体正常显示。
5. **示例数据**。所有数字由模拟器生成，页面保留「示例数据」标注；不要接真实接口、不要写入任何密钥或真实业务数据。
6. **文案风格**：中文为主，指标 / 按钮 / 标签保留英文大写风格（TASKS、AGENTS、OUTPUTS…）；数字带单位与千分位。
7. **水印**：保留画面中的「DEVELOPED BY @赛博老爸」系列水印，不改文案。
8. **可访问性与降级**：`prefers-reduced-motion` 时减少动画而非停摆；不支持 Canvas 柔光 / 锥形渐变时降级渲染而非报错。
9. **响应式**：宽屏五列面板，≤1100px 两列，手机竖屏单列。改动布局后需三档都看一眼。

## 验证清单（提交前必做）

> 提效：第 1 条自动检查可直接跑 `/skill:verify-dashboard`（内部调用 `.pi/skills/verify-dashboard/scripts/check.py`，已含 JS 语法 + id 两项）。

1. **JS 语法**：跑上面「常用命令」里的 `node --check` 校验脚本。
2. **id 完整性**：JS 引用的 id 都能在 `tpl-ops` 里找到（改 id 时必查）。
3. **打开页面**：无控制台报错；数据飞轮在转、顶部时钟在走、五面板有内容在刷新。
4. **交互**：「粒子」按钮能在纸面 / 荧光间切换；「全屏」可用；悬停飞轮节点出详情浮层。
5. **响应式**：1920×1080、约 1100px、手机竖屏三档布局正常。
6. **文件体积**：`index.html` 单文件体积异常暴涨（如超过 400 KB）时检查是否误提交了冗余内容。

## 提交约定

- Conventional Commits：`feat:` / `fix:` / `docs:` / `refactor:` / `perf:` / `chore:`，主题行用中文简述。
- 用户可见的改动同步更新 `README.md`，并在 `CHANGELOG.md` 顶部按 Keep a Changelog 格式追加条目。
- 不提交本地杂物（`server.log`、临时校验脚本等）。

## 交接（handoff）

工作收尾、上下文将满、换人 / 换模型、切换工作线、阻塞求助、里程碑达成时，必须按交接机制留档：

- **规则**：`docs/handoff/HANDOFF-RULES.md`（何时写、怎么写、怎么接、怎么归档）
- **模板**：`docs/handoff/HANDOFF-TEMPLATE.md`（复制为 `docs/handoff/YYYY-MM-DD-<slug>.md` 填写）
- **索引**：`docs/handoff/README.md`（新增 / 归档交接后更新索引表）
- **填写示例**：`docs/handoff/2026-10-21-docs-handoff.md`
- **一键命令**：pi 会话里用 `/handoff [slug] [补充说明]`（`.pi/prompts/handoff.md`）自动按模板写交接、更新索引、提交；索引与归档维护用 `/skill:handoff-index`。

AI 收到「交接 / 收尾 / 留档」指令时必须按模板产出交接文档、提交到当前分支、把文件路径告诉用户；验证状态如实填写，没跑过的写「未验证」。

**自动交接（用户已授权）**：完成一个工作段落（收尾、会话将结束、切换工作线）时，AI **自动**写交接，不必等用户开口。

## 边界（做之前先确认）

- 不要恢复 / 新增**多看板主题系统**（SPIDER / NEURAL 那类，本分支明确移除）。同一块调度中心看板的**配色变体**（纸面 / 粒子 / 炫彩 A–I）不在禁列（2026-10-22 用户加定炫彩）。
- 不要把单文件拆成多文件或多模块。
- 不要引入真实数据源、后端服务或鉴权。
- 涉及视觉大改（配色、布局、飞轮表现）先描述方案再动手，改动幅度大时先问一句。
