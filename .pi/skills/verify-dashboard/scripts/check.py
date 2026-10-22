#!/usr/bin/env python3
"""调度中心大屏 · 自动检查（verify-dashboard 技能脚本）

用法：在仓库根目录运行  python .pi/skills/verify-dashboard/scripts/check.py [index.html 路径]

检查项：
  1. 提取 <script> 并用 node --check 校验 JS 语法
  2. JS 引用的元素 id 与 tpl-ops 模板内 id 一一对应
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

def main() -> int:
    html_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.html")
    if not html_path.exists():
        print(f"[FAIL] 找不到 {html_path}（请在仓库根目录运行）")
        return 1
    html = html_path.read_text(encoding="utf-8")

    m = re.search(r"<script>(.*)</script>", html, re.S)
    if not m:
        print("[FAIL] index.html 里没有 <script> 区块")
        return 1
    js = m.group(1)

    ok = True

    # 1. JS 语法
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    try:
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode == 0:
            print("[PASS] JS 语法（node --check）")
        else:
            ok = False
            print("[FAIL] JS 语法（node --check）：")
            print(r.stderr.strip())
    except FileNotFoundError:
        ok = False
        print("[FAIL] 没找到 node，无法校验 JS 语法")
    finally:
        Path(tmp).unlink(missing_ok=True)

    # 2. id 完整性
    tpl = re.search(r'<template id="tpl-ops">(.*)</template>', html, re.S)
    if not tpl:
        ok = False
        print("[FAIL] 找不到 <template id=\"tpl-ops\">")
    else:
        tpl_ids = set(re.findall(r'id="([^"]+)"', tpl.group(1)))
        used = set(re.findall(r"\$\('#([\w-]+)'\)", js)) | set(
            re.findall(r"getElementById\('([\w-]+)'\)", js)
        )
        ignore = {"host-ops", "tpl-ops"}
        missing = used - tpl_ids - ignore
        unused = tpl_ids - used
        if missing:
            ok = False
            print(f"[FAIL] JS 引用但模板里不存在的 id：{sorted(missing)}")
        else:
            print(f"[PASS] id 完整性：JS 引用 {len(used)} 个，全部在模板中找到")
        if unused:
            print(f"[INFO] 模板里未被 JS 引用的 id（通常正常）：{sorted(unused)}")

    print("== 全部通过 ==" if ok else "== 存在失败项，请修复后重跑 ==")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
