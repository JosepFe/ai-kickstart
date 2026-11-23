#!/usr/bin/env python3
"""Story status is the source of truth; EPIC.md and FEATURE.md tables follow it.

Usage (from the repo root):
  python3 scripts/epic-status.py                 check every epic, exit 1 on any mismatch
  python3 scripts/epic-status.py --write         fix the Status columns and feature/epic status
  python3 scripts/epic-status.py --summary E01   mechanical part of the epic QA pass (markdown)

Only the standard library. Works on English or Spanish headings.
"""
import re
import subprocess
import sys
from pathlib import Path

EPICS = Path("internal_docs/Epics")
STORY_ID = re.compile(r"US-\d+")
STATUS_COLS = {"status", "estado"}
NONE_VALUES = {"", "none", "ninguno", "ninguna", "-", "—"}
FLAG = re.compile(r"NOT RUN|NOT VERIFIED")
STORY_STATUSES = {"todo", "in-progress", "done", "deferred"}


def front(text):
    """Frontmatter as a dict (flat `key: value` lines only)."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def set_front(text, key, value):
    return re.sub(rf"^({key}:).*$", rf"\g<1> {value}", text, count=1, flags=re.M)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(lines):
    """Yield (header_index, header_cells, [row_indexes]) for every markdown table."""
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head, rows, j = cells(lines[i]), [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(j)
                j += 1
            yield i, head, rows
            i = j
        else:
            i += 1


def story_tables(lines):
    for h, head, rows in tables(lines):
        low = [c.lower() for c in head]
        if low and low[0] == "us" and STATUS_COLS & set(low):
            col = next(k for k, c in enumerate(low) if c in STATUS_COLS)
            yield col, rows


def first_word(cell):
    """`done (`fa8dbab`)` -> `done`: a table may add the commit after the status."""
    m = re.match(r"[a-z-]+", cell.strip().lower())
    return m.group() if m else cell.strip()


def derive(statuses, current):
    """Feature/epic status from its stories; None = leave it as it is (also with unknown story statuses)."""
    if not statuses or any(s not in STORY_STATUSES for s in statuses):
        return None
    if all(s in ("done", "deferred") for s in statuses) and "done" in statuses:
        return "done"
    if any(s in ("in-progress", "done") for s in statuses):
        return "in-progress"
    return None if current in ("draft", "ready") else "ready"


def load(epic_dir):
    stories = {}
    for f in sorted(epic_dir.glob("**/US-*.md")):
        sid = STORY_ID.search(f.name).group()
        text = f.read_text(encoding="utf-8")
        stories[sid] = {"path": f, "text": text, "fm": front(text), "feature": f.parent}
    return stories


def sync_doc(path, stories, statuses, write, problems):
    """Check (and fix) one EPIC.md or FEATURE.md against its stories."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    seen, has_status_table = set(), False
    for col, rows in story_tables(lines):
        has_status_table = True
        for r in rows:
            row = cells(lines[r])
            m = STORY_ID.search(row[0]) if row else None
            if not m:
                continue
            sid = m.group()
            seen.add(sid)
            if sid not in stories:
                problems.append((False, f"{path}: {sid} is in the table but has no file"))
                continue
            want = stories[sid]["fm"].get("status", "")
            if want not in STORY_STATUSES:
                continue  # reported once per story by check()
            if col < len(row) and first_word(row[col]) != want:
                problems.append((True, f"{path}: {sid} table says '{row[col]}', story says '{want}'"))
                row[col] = want
                lines[r] = "| " + " | ".join(row) + " |"
    # A table without a Status column (older templates) has nothing to keep in sync.
    for sid in sorted(set(statuses) - seen) if has_status_table else []:
        problems.append((False, f"{path}: {sid} has a file but no row in the table"))
    current = front(text).get("status", "")
    want = derive(list(statuses.values()), current)
    if want and want != current:
        problems.append((True, f"{path}: status '{current}', its stories say '{want}'"))
    if write:
        new = "\n".join(lines)
        if want and want != current:
            new = set_front(new, "status", want)
        if new != text:
            path.write_text(new, encoding="utf-8")


def check(write):
    problems = []
    for epic_dir in sorted(p for p in EPICS.glob("E*") if p.is_dir()):
        stories = load(epic_dir)
        for sid, v in stories.items():
            st = v["fm"].get("status", "")
            if st not in STORY_STATUSES:
                old = v["fm"].get("state")
                hint = f" (old format: `state: {old}` holds the story status; move it to `status:`)" if old else ""
                problems.append((False, f"{v['path']}: status '{st}' is not one of {'|'.join(sorted(STORY_STATUSES))}{hint}"))
        for feature in sorted(epic_dir.glob("F*/FEATURE.md")):
            own = {s: v["fm"].get("status", "") for s, v in stories.items() if v["feature"] == feature.parent}
            sync_doc(feature, stories, own, write, problems)
        if (epic_dir / "EPIC.md").exists():
            sync_doc(epic_dir / "EPIC.md", stories, {s: v["fm"].get("status", "") for s, v in stories.items()}, write, problems)
    for fixable, p in problems:
        print(("fixed: " if write and fixable else "fix by hand: " if write else "") + p)
    if not problems:
        print("ok: story status, tables and feature/epic status agree")
    left = [p for fixable, p in problems if not (write and fixable)]
    return 1 if left else 0


def last_commit(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%h", "--", str(path)], capture_output=True, text=True)
        return out.stdout.strip() or "uncommitted"
    except OSError:
        return "?"


def section_rows(lines, first_cells):
    """Rows of tables whose first header cell is one of first_cells."""
    for h, head, rows in tables(lines):
        if head and head[0].lower() in first_cells:
            yield [cells(lines[r]) for r in rows]


def summary(epic_id):
    matches = [p for p in EPICS.glob(f"{epic_id}*") if p.is_dir()]
    if not matches:
        print(f"no epic folder {EPICS}/{epic_id}*")
        return 1
    epic_dir = matches[0]
    stories = load(epic_dir)
    epic_text = (epic_dir / "EPIC.md").read_text(encoding="utf-8")
    out, reasons = [f"# QA summary — {epic_dir.name}", ""], []

    waves = len(re.findall(r"^###\s+(Wave|Oleada)\b", epic_text, re.M | re.I))
    if waves > 1:
        reasons.append(f"{waves} waves")

    for feature in sorted(epic_dir.glob("F*/FEATURE.md")):
        lines = feature.read_text(encoding="utf-8").split("\n")
        own = {s: v for s, v in stories.items() if v["feature"] == feature.parent}
        out += [f"## {feature.parent.name}", "", "| US | Status | Started | Finished | Commit | Flags |", "|---|---|---|---|---|---|"]
        for sid, v in own.items():
            flags = sum(1 for l in v["text"].splitlines() if FLAG.search(l))
            out.append(f"| {sid} | {v['fm'].get('status', '?')} | {v['fm'].get('started', '')} | {v['fm'].get('finished', '')} | {last_commit(v['path'])} | {flags or ''} |")
        out.append("")
        for rows in section_rows(lines, {"id"}):
            for row in rows:
                if not re.match(r"C\d+", row[0]) or len(row) < 3:
                    continue
                cover = STORY_ID.findall(row[-1])
                undone = [s for s in cover if stories.get(s, {}).get("fm", {}).get("status") != "done"]
                if not cover:
                    out.append(f"- **{row[0]} has no story**")
                elif undone:
                    out.append(f"- {row[0]} covered by stories not done: {', '.join(undone)}")
        nfr = [r for rows in section_rows(lines, {"area", "área"}) for r in rows if len(r) > 1 and r[1].lower() not in NONE_VALUES]
        if nfr:
            reasons.append(f"{feature.parent.name}: {len(nfr)} non-functional requirement(s)")
        out.append("")

    out += ["## Decisions, assumptions, questions", ""]
    for rows in section_rows(epic_text.split("\n"), {"id"}):
        for row in rows:
            kind = row[0][:1]
            text = " | ".join(row)
            if kind == "Q" or (kind == "D" and "proposed" in text.lower()) or (kind == "D" and "propuesta" in text.lower()):
                out.append(f"- {text}")
    out += ["", "## NOT RUN / NOT VERIFIED", ""]
    for name, text in [("EPIC.md", epic_text)] + [(s, v["text"]) for s, v in stories.items()]:
        out += [f"- {name}: {l.strip()}" for l in text.splitlines() if FLAG.search(l)]
    out += ["", "## QA pass", "", f"qa-reviewer in epic mode: **{'yes' if reasons else 'no'}**" + (f" ({'; '.join(reasons)})" if reasons else " (one wave, no non-functional requirements: this summary is the QA)")]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    if not EPICS.is_dir():
        sys.exit(f"run from the repo root: {EPICS} not found")
    args = sys.argv[1:]
    if args[:1] == ["--summary"] and len(args) == 2:
        sys.exit(summary(args[1]))
    sys.exit(check(write=args == ["--write"]))
