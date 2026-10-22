#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""collect_tokens.py — 采集本地 agent 会话日志 → rollup → 原子写 data/<project-id>.json

口径依据：docs/specs/调度中心-数据同步设计.md（采集路线 = 会话日志解析，唯一路线）
快照契约：docs/specs/数字汇报-数据契约.md（全量快照、原子写、缺失态禁补 0）

支持的日志源（本机只扫属于 --project-dir 的会话，按文件内 cwd 过滤）：
  pi      ~/.pi/agent/sessions/**/*.jsonl
  claude  ~/.claude/projects/**/*.jsonl
  codex   ~/.codex/sessions/**/*.jsonl + ~/.codex/archived_sessions/*.jsonl

用法：
  py tools/collect_tokens.py --scan           # 只列候选项目写 data/_candidates.json（只读会话头的 cwd）
  py tools/collect_tokens.py --project-dir <项目路径> [--project-dir <项目路径> ...]
                                            # 采集这些项目（同时记入勾选清单）
  py tools/collect_tokens.py                  # 只采勾选清单里的项目（没清单时提示怎么选）

项目选择在看板「设置」浮层里勾选（勾完点「复制采集命令」粘到终端）；也可直接传 --project-dir。
隐私约定：只解析用户勾选项目的会话内容；未勾选的项目只读会话文件头的 cwd（列候选用），不读内容。
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()


def ts_local(s):
    """ISO 时间戳 → 本地时区 datetime；解析失败返回 None。"""
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone()
    except (ValueError, TypeError):
        return None


def iso(dt):
    return dt.isoformat(timespec="seconds")


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def read_jsonl(path):
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def file_cwd(path, limit=30):
    """从文件头几行找会话的 cwd（pi=type:session / codex=session_meta / claude=记录自带）。"""
    for i, d in enumerate(read_jsonl(path)):
        if i >= limit:
            break
        if d.get("type") == "session" and d.get("cwd"):
            return d["cwd"]
        if d.get("type") == "session_meta" and (d.get("payload") or {}).get("cwd"):
            return d["payload"]["cwd"]
        if d.get("cwd"):
            return d["cwd"]
    return None


def same_dir(a, b):
    return os.path.normcase(os.path.abspath(str(a))) == os.path.normcase(os.path.abspath(str(b)))


# ---------- 各日志源解析：统一产出 {ts, agent, model, input, output, cacheRead, cacheWrite, cost, ok} ----------
# input = 提示侧总 token（含缓存）；output 含推理 token（不单列，2026-10-22 拍板）。

def parse_pi(path):
    for d in read_jsonl(path):
        if d.get("type") != "message":
            continue
        m = d.get("message") or {}
        if m.get("role") != "assistant":
            continue
        u = m.get("usage") or {}
        ts = ts_local(d.get("timestamp") or m.get("timestamp"))
        if not ts:
            continue
        cr, cw = num(u.get("cacheRead")) or 0, num(u.get("cacheWrite")) or 0
        yield {
            "ts": ts,
            "agent": "pi",
            "model": "/".join(filter(None, [m.get("provider"), m.get("model")])),
            "input": (num(u.get("input")) or 0) + cr + cw,
            "output": num(u.get("output")) or 0,
            "cacheRead": cr,
            "cacheWrite": cw,
            "cost": num((u.get("cost") or {}).get("total")),
            "ok": not m.get("errorMessage"),
        }


def parse_claude(path):
    seen = set()  # 同一 message.id 的流式续写记录只计一次
    for d in read_jsonl(path):
        if d.get("type") != "assistant":
            continue
        m = d.get("message") or {}
        u = m.get("usage") or {}
        mid = m.get("id")
        if mid:
            if mid in seen:
                continue
            seen.add(mid)
        ts = ts_local(d.get("timestamp"))
        if not ts:
            continue
        cr = num(u.get("cache_read_input_tokens")) or 0
        cw = num(u.get("cache_creation_input_tokens")) or 0
        yield {
            "ts": ts,
            "agent": "claude",
            "model": m.get("model") or "",
            "input": (num(u.get("input_tokens")) or 0) + cr + cw,
            "output": num(u.get("output_tokens")) or 0,
            "cacheRead": cr,
            "cacheWrite": cw,
            "cost": None,
            "ok": not d.get("isApiErrorMessage"),
        }


def parse_codex(path):
    model = ""
    for d in read_jsonl(path):
        if d.get("type") == "turn_context":
            model = (d.get("payload") or {}).get("model") or model
        if d.get("type") != "event_msg":
            continue
        p = d.get("payload") or {}
        if p.get("type") != "token_count":
            continue
        lu = (p.get("info") or {}).get("last_token_usage") or {}
        ts = ts_local(d.get("timestamp"))
        if not ts:
            continue
        cr = num(lu.get("cached_input_tokens")) or 0
        yield {
            "ts": ts,
            "agent": "codex",
            "model": model,
            "input": num(lu.get("input_tokens")) or 0,
            "output": num(lu.get("output_tokens")) or 0,
            "cacheRead": cr,
            "cacheWrite": num(lu.get("cache_write_input_tokens")) or 0,
            "cost": None,
            "ok": True,
            "_quota": p.get("rate_limits"),  # 最新一条胜出，rollup 时消费
        }


SOURCES = [
    ("pi", parse_pi, [HOME / ".pi/agent/sessions"]),
    ("claude", parse_claude, [HOME / ".claude/projects"]),
    ("codex", parse_codex, [HOME / ".codex/sessions", HOME / ".codex/archived_sessions"]),
]


def discover():
    """列候选项目：只读会话文件头的 cwd（不解析会话内容），返回 [(cwd, 会话文件数)]。"""
    found = {}
    for _name, _parser, roots in SOURCES:
        for root in roots:
            if not root.is_dir():
                continue
            for f in root.rglob("*.jsonl"):
                cwd = file_cwd(f)
                if cwd:
                    key = str(Path(cwd).resolve())
                    found[key] = found.get(key, 0) + 1
    return sorted(found.items())


def collect(project_dirs):
    """只解析 project_dirs 里项目的会话；其他项目只读会话头的 cwd 用于匹配，不读内容。"""
    records = []
    for _name, parser, roots in SOURCES:
        files = [p for root in roots if root.is_dir() for p in root.rglob("*.jsonl")]
        for f in files:
            cwd = file_cwd(f)
            if not cwd or not any(same_dir(cwd, d) for d in project_dirs):
                continue
            try:
                recs = list(parser(f))
                for r in recs:
                    r["src"] = str(f)   # 供「当前聊天框」按会话文件聚合
                    r["cwd"] = str(Path(cwd).resolve())
                records.extend(recs)
            except OSError as e:
                print(f"[warn] 读不动 {f}: {e}", file=sys.stderr)
    records.sort(key=lambda r: r["ts"])
    return records


def rollup(records, project, now):
    """按设计文档 3.3 口径聚合成快照 tokens 节。缺失一律 null，禁补 0。"""
    today = now.date()

    def s(recs, key):
        return sum(r[key] for r in recs)

    # tps：近 30 个整秒桶（秒桶 = 该秒内完成请求的输出 token 之和）；无活动是真实 0
    series = [0] * 30
    for r in records:
        sec = int((now - r["ts"]).total_seconds())
        if 0 <= sec < 30:
            series[29 - sec] += r["output"]
    tps = {
        "now": series[29],
        "peak30s": max(series),
        "avg30s": round(sum(series) / 30),
        "series": series,
    }

    # 请求四计数：窗口 = 当日（与「今日成功率」同窗）；retried 会话日志分不出 → null（未采集）
    day = [r for r in records if r["ts"].date() == today]
    total, ok = len(day), sum(1 for r in day if r["ok"])
    failed = total - ok
    reqs = {
        "total": total,
        "ok": ok,
        "failed": failed,
        "retried": None,
        "cacheHitRate": round(s(day, "cacheRead") / s(day, "input"), 4) if day and s(day, "input") else None,
        "successRateToday": round(ok / total, 4) if total else None,
    }

    # 当前聊天框 = 最近一个会话文件的合计
    ses = {"input": None, "output": None, "cacheRead": None}
    if records:
        last = records[-1]
        sess = [r for r in records if r.get("src") == last.get("src")]
        ses = {"input": s(sess, "input"), "output": s(sess, "output"), "cacheRead": s(sess, "cacheRead")}

    # 当天消耗：今日无记录 = 真实 0（不是 null）；cost 只有 pi 有，当日记录不全带 cost 时置 null（未采集），不显示半截账
    today_block = {
        "input": s(day, "input"),
        "output": s(day, "output"),
        "cacheRead": s(day, "cacheRead"),
        "cost": s(day, "cost") if all(r["cost"] is not None for r in day) else None,
    }

    # 配额：codex rate_limits 最新一条 / 每（limit_id, 档位）
    quota = {}
    for r in records:
        rl = r.get("_quota") or {}
        for key in ("primary", "secondary"):
            q = rl.get(key) or {}
            if q.get("used_percent") is None:
                continue
            quota[(rl.get("limit_id"), key)] = {
                "account": f"codex:{rl.get('limit_id')}:{key}",
                "remainingPct": round(100 - q["used_percent"], 1),
                "resetAt": iso(datetime.fromtimestamp(q["resets_at"]).astimezone()) if q.get("resets_at") else None,
                "note": f"{(q.get('window_minutes') or 0) // 60}h 窗",
            }

    return {
        "schemaVersion": 2,
        "project": project,
        "tokens": {
            "lastSync": iso(now),
            "tps": tps,
            "requests": reqs,
            "session": ses,
            "today": today_block,
            "quota": list(quota.values()),
        },
    }


def write_snap(out, now, cwd, recs, pid=None, name=None):
    """一个项目一份快照：rollup → 原子写 data/<pid>.json。"""
    d = Path(cwd)
    pid = pid or re.sub(r"[^a-z0-9]+", "-", d.name.lower()).strip("-") or "project"
    stack = ["html"] if (d / "index.html").exists() else []
    if (d / "package.json").exists():
        try:
            stack = list((json.loads((d / "package.json").read_text(encoding="utf-8")).get("dependencies") or {}).keys())[:8]
        except (json.JSONDecodeError, OSError):
            pass
    snap = rollup(recs, {
        "id": pid,
        "name": name or d.name,
        "path": str(d),
        "stack": stack,
        "updatedAt": iso(now),
        "collector": "tool:collect_tokens@agent-display",
    }, now)
    tmp = out / f"{pid}.json.tmp"
    final = out / f"{pid}.json"
    tmp.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, final)  # 原子写，看板不会读到半截文件
    t = snap["tokens"]
    print(f"[ok] {final}  请求(今日) {t['requests']['total']} 条 · 今日 input/output "
          f"{t['today']['input']}/{t['today']['output']} · lastSync {t['lastSync']}")


def scan(out):
    """发现候选项目（只读会话文件头的 cwd，不读内容），写 data/_candidates.json 供看板「设置」列清单。"""
    payload = [{"name": Path(c).name, "path": c, "sessions": n} for c, n in discover()]
    f = out / "_candidates.json"
    f.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] {f}  {len(payload)} 个候选项目（只读了会话头的 cwd，未读会话内容）")


def main():
    ap = argparse.ArgumentParser(description="采集用户勾选项目的会话日志并写 data/<id>.json 快照")
    ap.add_argument("--scan", action="store_true", help="只列候选项目写 data/_candidates.json（看板「设置」列清单用）")
    ap.add_argument("--project-dir", action="append", default=None, metavar="DIR",
                    help="采集这些项目（可重复传多个；同时记入勾选清单）")
    ap.add_argument("--out", default="data", help="快照输出目录（默认 data/）")
    ap.add_argument("--id", default=None, help="project.id / 文件名（默认取项目目录名；仅单项目时生效）")
    ap.add_argument("--name", default=None, help="project.name（默认取目录名；仅单项目时生效）")
    args = ap.parse_args()

    now = datetime.now().astimezone()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if args.scan:
        scan(out)
        return

    pf = out / "_projects.local.json"
    if args.project_dir:
        dirs = [str(Path(d).resolve()) for d in args.project_dir]
        pf.write_text(json.dumps({"projects": dirs}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[ok] 勾选清单已更新：{pf}（{len(dirs)} 个项目，下次直接 py tools/collect_tokens.py）")
    else:
        dirs = (json.loads(pf.read_text(encoding="utf-8")).get("projects") or []) if pf.exists() else []
        if not dirs:
            print("尚未勾选项目。二选一：\n"
                  "  1) 看板「设置」浮层勾选项目 → 点「复制采集命令」→ 粘到终端\n"
                  "  2) py tools/collect_tokens.py --scan 后用 --project-dir <路径> 指定", file=sys.stderr)
            return

    groups = {}
    for r in collect(dirs):
        groups.setdefault(r["cwd"], []).append(r)
    if not groups and dirs:
        print("[warn] 选中的项目没扫到会话记录", file=sys.stderr)

    if len(groups) == 1 and (args.id or args.name):
        cwd, recs = next(iter(groups.items()))
        write_snap(out, now, cwd, recs, args.id, args.name)
        return

    ids = {}
    for cwd in groups:
        ids[cwd] = re.sub(r"[^a-z0-9]+", "-", Path(cwd).name.lower()).strip("-") or "project"
    for pid in set(ids.values()):  # 同名不同路径：加路径短哈希区分
        cwds = [c for c, p in ids.items() if p == pid]
        if len(cwds) > 1:
            for c in cwds:
                ids[c] = f"{pid}-{hashlib.md5(c.encode('utf-8')).hexdigest()[:6]}"
    for cwd, recs in sorted(groups.items()):
        write_snap(out, now, cwd, recs, ids[cwd])


if __name__ == "__main__":
    main()
