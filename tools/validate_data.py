#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_data.py — 校验 data/ 快照是否符合数据契约

契约：docs/specs/数字汇报-数据契约.md（缺失态口径：null = 未采集，禁止补 0）
tokens 节：docs/specs/调度中心-数据同步设计.md 第 4 节（schemaVersion 2）

用法：py tools/validate_data.py data/<project-id>.json [more.json ...]
退出码：0 = 全部通过；1 = 有错误（有错误不要推送）
"""
import json
import re
import sys
from datetime import datetime

KNOWN_SCHEMA = 2
PROJECT_KEYS = ("id", "name", "updatedAt", "collector")
REQ_KEYS = ("total", "ok", "failed", "retried", "cacheHitRate", "successRateToday")


def err(msg, errors):
    errors.append(msg)


def is_num_or_null(x):
    return x is None or (isinstance(x, (int, float)) and not isinstance(x, bool))


def check_tokens(tok, errors):
    """tokens 节（schemaVersion 2）。字段缺失 = 未接入该字段，允许；类型错了才报。"""
    if not isinstance(tok, dict):
        return err("tokens: 必须是对象", errors)
    if "lastSync" in tok:
        try:
            datetime.fromisoformat(tok["lastSync"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            err("tokens.lastSync: 不是 ISO 8601 时间", errors)
    if "tps" in tok:
        t = tok["tps"]
        if not isinstance(t, dict):
            err("tokens.tps: 必须是对象", errors)
        else:
            for k in ("now", "peak30s", "avg30s"):
                if k in t and not is_num_or_null(t[k]):
                    err(f"tokens.tps.{k}: 必须是数字或 null", errors)
            if "series" in t:
                if not isinstance(t["series"], list) or not all(is_num_or_null(v) for v in t["series"]):
                    err("tokens.tps.series: 必须是数字数组（无活动的秒是真实 0）", errors)
    if "requests" in tok:
        r = tok["requests"]
        if not isinstance(r, dict):
            err("tokens.requests: 必须是对象", errors)
        else:
            for k in REQ_KEYS:
                if k in r and not is_num_or_null(r[k]):
                    err(f"tokens.requests.{k}: 必须是数字或 null（null = 未采集，禁补 0）", errors)
    for k in ("session", "today"):
        if k in tok:
            b = tok[k]
            if not isinstance(b, dict):
                err(f"tokens.{k}: 必须是对象", errors)
            else:
                for f, v in b.items():
                    if not is_num_or_null(v):
                        err(f"tokens.{k}.{f}: 必须是数字或 null", errors)
    if "quota" in tok:
        if not isinstance(tok["quota"], list):
            err("tokens.quota: 必须是数组", errors)
        else:
            for i, q in enumerate(tok["quota"]):
                if not isinstance(q, dict) or "remainingPct" not in q:
                    err(f"tokens.quota[{i}]: 必须是含 remainingPct 的对象", errors)
                elif not is_num_or_null(q["remainingPct"]) or (q["remainingPct"] is not None and not 0 <= q["remainingPct"] <= 100):
                    err(f"tokens.quota[{i}].remainingPct: 必须是 0-100 的数字或 null", errors)


def check_repos(repos, errors):
    """repos[] 节（契约 6.10）：git 提交数据，供热力图。"""
    if not isinstance(repos, list):
        return err("repos: 必须是数组", errors)
    for i, r in enumerate(repos):
        if not isinstance(r, dict) or not r.get("name"):
            err(f"repos[{i}]: 必须是含 name 的对象", errors)
            continue
        for k in ("ahead", "behind", "commitsToday", "linesToday"):
            if k in r and not is_num_or_null(r[k]):
                err(f"repos[{i}].{k}: 必须是数字或 null", errors)
        if "daily" not in r:
            continue
        if not isinstance(r["daily"], list):
            err(f"repos[{i}].daily: 必须是数组", errors)
            continue
        for j, d in enumerate(r["daily"]):
            ok = isinstance(d, dict) and d.get("date") and all(isinstance(d.get(k), int) for k in ("commits", "additions", "deletions"))
            if not ok:
                err(f"repos[{i}].daily[{j}]: 必须是含 date/commits/additions/deletions 的对象", errors)


def check_heat(heat, errors):
    """heat 节（设计文档 4 节）：提交按星期×小时分桶，供热力图「按时段」视图。"""
    if not isinstance(heat, dict):
        return err("heat: 必须是对象", errors)
    m = heat.get("byHour")
    bad = not isinstance(m, list) or len(m) != 7 or any(
        not isinstance(r, list) or len(r) != 24 or any(not isinstance(v, int) for v in r) for r in m)
    if bad:
        err("heat.byHour: 必须是 7×24 整数矩阵（周一~周日 × 0-23 时）", errors)
    b = heat.get("busiest")
    if b is not None and (not isinstance(b, dict) or not isinstance(b.get("weekday"), int) or not isinstance(b.get("hour"), int)):
        err("heat.busiest: 必须是 {weekday, hour} 或 null", errors)


def check_file(path):
    errors = []
    try:
        d = json.loads(open(path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as e:
        return [f"文件读不了 / 不是合法 JSON: {e}"]

    sv = d.get("schemaVersion")
    if not isinstance(sv, int):
        err("schemaVersion: 必填整数", errors)
    elif sv > KNOWN_SCHEMA:
        err(f"schemaVersion {sv} 过新（看板只认 <= {KNOWN_SCHEMA}），请更新看板", errors)

    p = d.get("project")
    if not isinstance(p, dict):
        err("project: 必填对象", errors)
    else:
        for k in PROJECT_KEYS:
            if not p.get(k):
                err(f"project.{k}: 必填", errors)
        if p.get("id") and not re.fullmatch(r"[a-z0-9-]+", str(p["id"])):
            err("project.id: 只允许小写字母/数字/短横线，且与文件名一致", errors)
        if p.get("updatedAt"):
            try:
                datetime.fromisoformat(str(p["updatedAt"]).replace("Z", "+00:00"))
            except ValueError:
                err("project.updatedAt: 不是 ISO 8601 时间", errors)

    if "tokens" in d:
        check_tokens(d["tokens"], errors)
    if "repos" in d:
        check_repos(d["repos"], errors)
    if "heat" in d:
        check_heat(d["heat"], errors)
    return errors


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    bad = 0
    for path in sys.argv[1:]:
        errors = check_file(path)
        if errors:
            bad = 1
            print(f"[fail] {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"[ok] {path}")
    return bad


if __name__ == "__main__":
    sys.exit(main())
