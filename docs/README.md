# docs · 项目文档

本目录存放项目的协作与管理文档。代码即文档的主体在 `index.html`，AI 工作说明在根目录 [`../AGENTS.md`](../AGENTS.md)。

## 目录索引

| 路径 | 内容 | 什么时候看 |
| --- | --- | --- |
| [`handoff/README.md`](handoff/README.md) | 交接（handoff）总览与文档索引 | 接手任何工作之前 |
| [`handoff/HANDOFF-RULES.md`](handoff/HANDOFF-RULES.md) | 交接规则：何时写、怎么写、怎么接、怎么归档 | 写交接 / 接手时 |
| [`handoff/HANDOFF-TEMPLATE.md`](handoff/HANDOFF-TEMPLATE.md) | 交接文档模板（复制即用，含逐项填写说明） | 写新交接时 |
| `handoff/archive/` | 已归档的历史交接 | 查历史上下文时 |
| [`adr/README.md`](adr/README.md) | 架构决策记录（ADR）索引与规则 | 想动架构 / 推翻现有设计之前 |
| [`adr/0001-单文件交付.md`](adr/0001-单文件交付.md) | 为什么单文件、不引构建与框架 | 想拆文件 / 引框架时必读 |
| [`adr/0002-Shadow-DOM-样式与-id-隔离.md`](adr/0002-Shadow-DOM-样式与-id-隔离.md) | 为什么用 Shadow DOM 隔离样式与 id | 改样式 / 改 id 时必读 |
| [`adr/0003-全模拟数据.md`](adr/0003-全模拟数据.md) | 为什么不接真实接口 | 想接真实数据 / 报真实指标时必读 |
| [`specs/数字汇报-改造计划.md`](specs/数字汇报-改造计划.md) | 数字汇报改造的**规划台账**（阶段 / 待拍板问题 / 决策与问题日志） | 改动前必看、改动后补记 |
| [`specs/数字汇报-核心需求.md`](specs/数字汇报-核心需求.md) | 数字汇报看板原始需求（只读参考） | 了解需求边界时 |
| [`specs/数字汇报-数据契约.md`](specs/数字汇报-数据契约.md) | 数据契约 JSON 格式草案（待评审） | 对接推送 skill 时 |
| [`specs/调度中心-数据同步设计.md`](specs/调度中心-数据同步设计.md) | 数据同步管道 + token 统计口径设计（参考 cc-switch / magpie，待拍板） | 做数据同步 / token 统计 / 写采集器前必读 |

后续规划中的文档位（按需建立，先不占坑）：

- `specs/`：需求与验收标准（spec 驱动开发）

## 文档约定

1. 全部使用 Markdown，中文撰写，标题层级从 `#` 开始，一份文档只讲一个主题。
2. 文档里引用代码必须给出**文件路径 + 符号名**（如 `index.html · mountOps()`），不写行号（行号会漂移）。
3. 引用版本给出 **commit hash 或版本号**，不写"上次 / 最近"这类相对说法。
4. 命令必须是可以直接粘贴执行的完整命令。
5. 文档与代码同步：代码改动影响文档描述时，同一个提交里更新文档。
