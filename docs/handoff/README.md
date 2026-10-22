# 交接（handoff）· 总览与索引

交接文档 = 一次工作的上下文快照，让下一位不看聊天记录就能接手。规则见 [HANDOFF-RULES.md](./HANDOFF-RULES.md)，模板见 [HANDOFF-TEMPLATE.md](./HANDOFF-TEMPLATE.md)。

**三步上手**：① 读下面索引里最新的交接 → ② 读根目录 `AGENTS.md` 的约定与边界 → ③ 复跑验证清单后认领开工。

## 活跃交接（按日期倒序）

| 日期 | 文档 | 主题 | 状态 | 接手人 |
| --- | --- | --- | --- | --- |
| 2026-10-22 | [2026-10-22-heat-60d-use-bars.md](./2026-10-22-heat-60d-use-bars.md) | 热力图近 60 天日期视图 + USE 柱状图 | 🟡 待认领 | — |
| 2026-10-22 | [2026-10-22-炫彩与上库.md](./2026-10-22-炫彩与上库.md) | 炫彩主题九套 + 四视图 / 词表落地 + 首次上库 | 🟡 待认领 | — |
| 2026-10-22 | [2026-10-22-layout-freeze.md](./2026-10-22-layout-freeze.md) | 布局定稿（五面板冻结 + tab 扩展）+ 开发统计修复 | 🟡 待认领 | — |
| 2026-10-22 | [2026-10-22-devstats-tiles.md](./2026-10-22-devstats-tiles.md) | 开发统计占位三项换真（昨日遗留小件闭环） | 🟡 待认领 | — |
| 2026-10-21 | [2026-10-21-数字汇报改造.md](./2026-10-21-数字汇报改造.md) | 数字汇报看板改造第一阶段（四块面板落地） | 🟡 待认领 | — |
| 2026-10-21 | [2026-10-21-docs-handoff.md](./2026-10-21-docs-handoff.md) | 项目管理文档体系建立 + 分支现状 | 🟡 待认领 | — |

## 已归档

| 日期 | 文档 | 主题 | 归档原因 |
| --- | --- | --- | --- |
| 2026-10-22 | [2026-10-22-data-sync-design.md](./archive/2026-10-22-data-sync-design.md) | 数据同步设计（含 token 统计口径） | 事项全部闭环（拍板 + P1 落地，由 2026-10-22-data-sync-p1.md 接续） |
| 2026-10-22 | [2026-10-22-data-sync-p1.md](./archive/2026-10-22-data-sync-p1.md) | 数据同步 P1 落地（采集器 + 校验器 + 面板消费） | 未完项由 2026-10-22-project-selector.md 覆盖接续 |
| 2026-10-22 | [2026-10-22-project-selector.md](./archive/2026-10-22-project-selector.md) | 数据同步多项目（设置按钮选项目 + 口径修正） | 「--all 全盘扫描」被用户推翻，未完项由 2026-10-22-opt-in-projects.md 接续 |
| 2026-10-22 | [2026-10-22-opt-in-projects.md](./archive/2026-10-22-opt-in-projects.md) | 采集改用户勾选项目（--pick，隐私修正） | `--pick` 被设置界面勾选取代，未完项由 2026-10-22-settings-selection.md 接续 |
| 2026-10-22 | [2026-10-22-settings-selection.md](./archive/2026-10-22-settings-selection.md) | 设置浮层项目勾选界面 + git 板块定调 | 勾选 / `--scan` 流程被「直接选目录」推翻，未完项由 2026-10-22-data-sync-wave2.md 接续 |
| 2026-10-22 | [2026-10-22-data-sync-wave2.md](./archive/2026-10-22-data-sync-wave2.md) | 数据同步第二波（设置直选目录 + git 采集 + 热力图按时段） | 热力图「按时段」被同日推翻改日期视图，未完项由 2026-10-22-heat-60d-use-bars.md 接续 |

<!-- 归档文件放在 ./archive/ 下，内容不再修改（规则见 HANDOFF-RULES.md 第 5 节）。 -->
