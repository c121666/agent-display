---
description: 按模板写 handoff 交接文档，更新交接索引并提交
argument-hint: "[slug] [补充说明]"
---
本次工作收尾交接。请产出一份交接文档，严格按仓库的交接机制执行：

1. 先读 `docs/handoff/HANDOFF-RULES.md`（规则）和 `docs/handoff/HANDOFF-TEMPLATE.md`（模板），逐项填写，保留模板的小节结构。
2. 用 git 核对事实：`git log --oneline -5`、`git status -s`、`git diff --stat`。交接里的分支名、commit hash、文件路径必须真实，禁止写"上次 / 最近"这类相对说法。
3. 文件名：`docs/handoff/YYYY-MM-DD-<slug>.md`，日期用今天。slug：${1:-用一句话概括本次工作的小写英文短横线词}。
4. 补充背景（可为空）：${@:2}
5. 验证状态如实填写：只写本次实际跑过的验证项结果，没跑过的写「未验证」，不许写成「已通过」。
6. 同步更新 `docs/handoff/README.md` 的「活跃交接」索引表（按日期倒序）。
7. 按提交约定提交到当前分支（`docs: 交接 <主题>…`，Conventional Commits + 中文主题行）。
8. 完成后告诉我：交接文档路径、本次交接的核心结论（已完成 / 未完成各几条、下一步第一步是什么）。
