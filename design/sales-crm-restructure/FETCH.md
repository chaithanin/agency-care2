# How the main project fetches these files

Three ways, in order of preference. **All three were tested from a clean container**, and the last
check in each case was applying the patch against a pristine `agency-care` checkout.

The files live in repo **`chaithanin/agency-care2`**, branch
**`claude/agency-care-test-project-zo163o`**, folder **`design/sales-crm-restructure/`**.

---

## A · Sparse clone — recommended

Pulls only this folder, about **1 MB**, not the whole repo.

```bash
git clone --depth 1 --filter=blob:none --sparse \
  -b claude/agency-care-test-project-zo163o \
  https://github.com/chaithanin/agency-care2 /tmp/crm-spec
cd /tmp/crm-spec && git sparse-checkout set design/sales-crm-restructure
ls design/sales-crm-restructure
```

You get 17 documents, 10 `.dc.html` sheets, the build scripts, and `patches/`.

Apply the patch straight from there:

```bash
cd /path/to/agency-care
git apply /tmp/crm-spec/design/sales-crm-restructure/patches/0001-audit-safe-fixes.patch
```

**Tested:** clone → sparse-checkout → `git apply --check` against pristine `ba63900` — passes.

## B · Attach the repo to the session

If the session is Claude Code on the web or a remote runner, attach it instead of cloning:

```
add_repo(owner="chaithanin", repo="agency-care2")
```

Then follow the clone command the tool returns. Do **not** pre-check with `curl` or `gh repo view`
first — an unauthenticated probe returns 404 on a private repo even when the session does have
access, and that false 404 will send you down the wrong path.

## C · Raw file URLs — no clone

For reading one or two files. Base:

```
https://raw.githubusercontent.com/chaithanin/agency-care2/claude/agency-care-test-project-zo163o/design/sales-crm-restructure/
```

```bash
B=https://raw.githubusercontent.com/chaithanin/agency-care2/claude/agency-care-test-project-zo163o/design/sales-crm-restructure
curl -sO $B/BRIEF.md
curl -sO $B/WORK_ORDERS.md
curl -s  $B/patches/0001-audit-safe-fixes.patch | git apply -
```

**Tested:** `BRIEF.md` fetched, 34,408 bytes, correct first line.

---

## What is in the folder

| File | What it is |
| --- | --- |
| `README.md` | Start here — the map |
| `BRIEF.md` | The whole requirement |
| `COMMAND.md` | The paste-ready kickoff message per phase |
| `WORK_ORDERS.md` | Five work orders, one per phase, with files and line numbers |
| `CODE_AUDIT.md` | Bugs and data linkage found in the live code, cited by file and line |
| `DEPLOY_IMPACT.md` | What changes in production, and what a rollback does not undo |
| `OPEN_DECISIONS.md` | Five open questions, each with a drafted safe default |
| `patches/` | One applyable patch, six verified fixes, plus its own README |
| `*.dc.html` | The 10 design sheets — also viewable as the canvas |
| `build_*.py`, `tokens.py`, `shell.py` | The generators, if a sheet needs regenerating |

Design canvas: https://claude.ai/artifact/SNAd42xy9r3icnxvxFfHhf

## Reading order

1. `README.md`
2. `BRIEF.md`
3. `WORK_ORDERS.md` — the phase you were given
4. `CODE_AUDIT.md` §4 — whether the audit changes that phase's scope
5. `DEPLOY_IMPACT.md` — before any traffic switch
6. `../PROJECT_RULES.md` — one level up, the main project's own rules

## Two things to know before reading

- **Every line number is against `feat/all-appointments-clean-on-118a2e2` at `ba63900`**, not `main`.
  The two differ by about 3,000 lines in `deals.service.ts` alone. If the branch has moved, re-run the
  counts before trusting a citation.
- **These files are a specification, not code to merge.** The only thing meant to land in
  `agency-care` verbatim is `patches/0001-audit-safe-fixes.patch`.
