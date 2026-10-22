# 项目常驻指令 · 调度中心大屏

（本文件由 pi 在系统提示中加载，适用于本项目的每次会话。）

- **项目定位**：纯前端单文件大屏（`index.html`），分支 `dispatch-center-only` 只保留「调度中心」一款看板。禁止：恢复多主题 / 主题切换、把单文件拆成多文件、引入框架 / npm 依赖 / CDN 脚本（外部请求仅 Google Fonts）。
- **动手前**：改 `index.html` 之前先读根目录 `AGENTS.md`（结构地图、修改约定、边界），改文档先读 `docs/README.md` 的文档约定。
- **提交前**：必须跑验证清单（自动检查用 `/skill:verify-dashboard`，人工冒烟照 `AGENTS.md` 验证清单），验证状态如实记录，没跑过的写「未验证」。
- **收尾时**：完成一个工作段落（收尾、会话将结束、切换工作线）**自动**写交接（用户已授权，不必等吩咐，直接用 `/handoff`），并同步 `docs/handoff/README.md` 索引（可用 `/skill:handoff-index`）；规则见 `docs/handoff/HANDOFF-RULES.md`。
- **提交规范**：Conventional Commits（`feat:` / `fix:` / `docs:` …）+ 中文主题行；用户可见改动同步 `README.md` 与 `CHANGELOG.md`；不提交本地杂物（`server.log` 等）。
- **边界**：视觉大改先出方案再动手；不接真实数据源 / 后端 / 鉴权；不删除「DEVELOPED BY @赛博老爸」水印。
