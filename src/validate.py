#!/usr/bin/env python3
"""Validates a course module authored as JSON (content/modules/*.json).
Usage:  python3 validate.py content/modules/meu-modulo.json
The build runs the same checks and stops on the first invalid module."""
import json, re, sys

RESERVED = {"academia", "csharp", "dotnet", "auth", "projeto"}
LESSON_TYPES = {"code", "cards", "table", "exercise"}
LANGS = {"cs", "sh", "json", "xml", "http", "txt"}
FORBIDDEN = [("ITSector", "no company names or logos"), ("Postman", "the academy uses Bruno only"), ("TODO", "unfinished text"), ("lorem", "placeholder text")]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
ID = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def _walk_strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from _walk_strings(v)
    elif isinstance(o, list):
        for v in o: yield from _walk_strings(v)


def _str(v): return isinstance(v, str) and v.strip() != ""


def validate_module(m, name="module"):
    e = []
    def err(msg): e.append(f"{name}: {msg}")
    if not isinstance(m, dict): return [f"{name}: the file must contain one JSON object"]
    mid = m.get("id")
    if not (_str(mid) and ID.match(mid)): err("id must be kebab-case, e.g. 'efcore'")
    elif mid in RESERVED: err(f"id '{mid}' is reserved")
    if m.get("kind") != "course": err("kind must be 'course'")
    for k in ("title", "short", "tagline"):
        if not _str(m.get(k)): err(f"'{k}' is required (non-empty text)")
    if _str(m.get("short")) and len(m["short"]) > 22: err("'short' is used in menus: max 22 characters")
    if _str(m.get("tagline")) and len(m["tagline"]) > 220: err("'tagline' max 220 characters (1 or 2 sentences)")
    chs = m.get("chapters")
    if not (isinstance(chs, list) and 1 <= len(chs) <= 8): err("'chapters' must be a list of 1 to 8 chapters"); chs = []
    lesson_ids = set()
    for ci, c in enumerate(chs):
        cp = f"chapter {ci + 1}"
        if not isinstance(c, dict): err(f"{cp}: must be an object"); continue
        cid = c.get("id", "")
        if not (_str(cid) and cid.startswith(f"{mid}-") and ID.match(cid)): err(f"{cp}: id must be '{mid}-<n>' (kebab-case)")
        for k in ("t", "intro"):
            if not _str(c.get(k)): err(f"{cp}: '{k}' is required")
        ls = c.get("lessons")
        if not (isinstance(ls, list) and 3 <= len(ls) <= 14): err(f"{cp}: needs 3 to 14 lessons"); ls = []
        for li, l in enumerate(ls):
            lp = f"{cp}, lesson {li + 1}"
            if not isinstance(l, dict): err(f"{lp}: must be an object"); continue
            lid = l.get("id", "")
            if not (_str(lid) and lid.startswith(f"{mid}-")): err(f"{lp}: id must start with '{mid}-' and be unique")
            elif lid in lesson_ids: err(f"{lp}: duplicate id '{lid}'")
            lesson_ids.add(lid)
            if not _str(l.get("t")): err(f"{lp}: 't' (title) is required")
            ty = l.get("type")
            if ty not in LESSON_TYPES: err(f"{lp}: type must be one of {sorted(LESSON_TYPES)}"); continue
            if ty == "code":
                if not _str(l.get("code")): err(f"{lp}: 'code' is required")
                elif l["code"].count("\n") > 24: err(f"{lp}: code block longer than 25 lines; split the lesson")
                if l.get("lang") not in LANGS: err(f"{lp}: lang must be one of {sorted(LANGS)}")
                pts = l.get("points")
                if not (isinstance(pts, list) and 2 <= len(pts) <= 4 and all(_str(p) for p in pts)): err(f"{lp}: 'points' must be 2 to 4 short sentences")
            elif ty == "cards":
                it = l.get("items")
                if not (isinstance(it, list) and 2 <= len(it) <= 6): err(f"{lp}: 'items' must have 2 to 6 cards")
                else:
                    for k, x in enumerate(it):
                        if not (isinstance(x, dict) and _str(x.get("t")) and isinstance(x.get("d"), list) and x["d"] and all(_str(s) for s in x["d"])):
                            err(f"{lp}, card {k + 1}: needs 't' (text) and 'd' (list of sentences)")
            elif ty == "table":
                rows = l.get("rows")
                if not (isinstance(rows, list) and len(rows) >= 2 and all(isinstance(r, list) and r and all(_str(c2) for c2 in r) for r in rows)): err(f"{lp}: 'rows' must be a list of rows (first row = header)")
                elif len({len(r) for r in rows}) != 1: err(f"{lp}: every row must have the same number of columns")
            elif ty == "exercise":
                st = l.get("steps")
                if not (isinstance(st, list) and 2 <= len(st) <= 8 and all(isinstance(s, dict) and "lead" in s and _str(s.get("text")) for s in st)): err(f"{lp}: 'steps' must be 2 to 8 objects with 'lead' and 'text'")
            mo = l.get("more")
            if mo is not None:
                if not (isinstance(mo, dict) and _str(mo.get("more"))): err(f"{lp}: 'more' must be an object with a 'more' text")
                elif set(mo) - {"more", "pit", "tryit"}: err(f"{lp}: 'more' only accepts more, pit, tryit")
        qz = c.get("quiz")
        if not (isinstance(qz, list) and 3 <= len(qz) <= 6): err(f"{cp}: quiz needs 3 to 6 questions"); qz = []
        for qi, q in enumerate(qz):
            qp = f"{cp}, question {qi + 1}"
            if not (isinstance(q, dict) and _str(q.get("q")) and isinstance(q.get("o"), list) and 3 <= len(q["o"]) <= 5 and all(_str(o) for o in q["o"])): err(f"{qp}: needs 'q' and 3 to 5 options in 'o'"); continue
            if not (isinstance(q.get("a"), int) and 0 <= q["a"] < len(q["o"])): err(f"{qp}: 'a' must be the index (from 0) of the correct option")
            if not _str(q.get("w")): err(f"{qp}: 'w' (why it is correct) is required")
            if len(set(q["o"])) != len(q["o"]): err(f"{qp}: duplicate options")
    out = m.get("outro")
    if not (isinstance(out, dict) and isinstance(out.get("done"), list) and out["done"] and all(_str(x) for x in out["done"])): err("'outro.done' must list what the student can do now")
    docs = (out or {}).get("docs") if isinstance(out, dict) else None
    if not (isinstance(docs, list) and docs and all(isinstance(d, dict) and _str(d.get("t")) and _str(d.get("u")) and d["u"].startswith("https://") for d in docs)): err("'outro.docs' must list official https links as {t, u}")
    pr = (out or {}).get("practice") if isinstance(out, dict) else None
    if not (isinstance(pr, list) and 2 <= len(pr) <= 6 and all(_str(x) for x in pr)): err("'outro.practice' must list 2 to 6 practice ideas (short sentences)")
    for s in _walk_strings(m):
        for bad, why in FORBIDDEN:
            if bad.lower() in s.lower(): err(f"forbidden text '{bad}' ({why}): {s[:60]}")
        if EMOJI.search(s): err(f"emoji are not allowed: {s[:60]}")
    return e


if __name__ == "__main__":
    ok = True
    for f in sys.argv[1:]:
        errs = validate_module(json.load(open(f, encoding="utf-8")), f)
        print("OK  " + f if not errs else "\n".join(errs)); ok = ok and not errs
    sys.exit(0 if ok else 1)
