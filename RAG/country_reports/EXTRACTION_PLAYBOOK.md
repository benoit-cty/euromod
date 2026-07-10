# Playbook: extracting a EUROMOD Country Report + matching it to `<CC>.policy.json`

How the FR extraction (`Y16_CR_FR.md` + `FR_parameter_matching.md`) was produced, so the same job can be redone for ES (`Y16_CR_ES.pdf` is already in this folder) or any other country in ~30 minutes of wall-clock, mostly agent time.

## 0. Tools to install / verify first

| Tool | Where | Install | Why |
|---|---|---|---|
| **poppler** | Windows | `winget install oschwartz10612.Poppler` (or conda/scoop) | The Claude Code `Read` tool needs it to render PDF pages visually. **It was missing on this machine**, so every agent had to fall back to text-layer extraction in WSL. Text extraction worked well for these reports (they have a clean text layer), but visual rendering is more robust for complex tables. |
| **jq** | Windows | `winget install jqlang.jq` (installed 2026-07-10, needs new shell) | Slicing the 3 MB policy JSON. Until the shell restart, use WSL's `/usr/bin/jq`. |
| **jq** | WSL | already at `/usr/bin/jq` | idem |
| **uv** | WSL | already at `~/.local/bin/uv` (login shell only — use `bash -lc` or full path) | `uv run --with pypdf python …` gives throwaway PDF tooling without polluting a venv. |
| **pypdf / PyMuPDF** | WSL, ephemeral | `uv run --with pypdf …` / `--with pymupdf` | Page count, outline (TOC), text extraction. No repo venv has them installed. |
| Disk space | WSL | `df -h /` | **A previous run died mid-extraction because the disk was full.** All 9 background agents were killed and could not be resumed (stopped agents are unrecoverable — relaunch). Check before fanning out. |

## 1. Recon the PDF (5 min, no agents)

```bash
# page count + bookmark outline = section → page map
wsl.exe -d Ubuntu-24.04 bash -lc "cd /home/ben/Euromod/euromod && uv run --with pypdf python - <<'EOF'
from pypdf import PdfReader
r = PdfReader('RAG/country_reports/Y16_CR_ES.pdf')
print('pages:', len(r.pages))
def walk(items, d=0):
    for it in items:
        if isinstance(it, list): walk(it, d+1)
        else: print('  '*d + f'{it.title} .... p{r.get_destination_page_number(it)}')
walk(r.outline)
EOF"
```

The CR outline is gold: **section titles embed the EUROMOD variable names** (`bch00_s`, `tin_s`, …), which is what makes the JSON matching mostly mechanical. Outline page numbers are 0-indexed-ish; add a ±1 overlap between ranges.

## 2. Fan out extraction agents (the bulk of the work)

Partition the report into **≤20-page ranges aligned to the outline** (the `Read` tool caps PDF reads at 20 pages/call). For the 189-page FR report, 9 parallel background agents worked well:

| # | Pages | Content | Output file |
|---|---|---|---|
| 1 | 8–27 | intro, scope of simulation, policy changes, spine, extensions | `cr_sec1_intro.md` |
| 2 | 27–46 | family & disability benefits | `cr_sec2_family.md` |
| 3 | 46–65 | social minima (RSA, PA, chèque énergie, ASPA), housing start | `cr_sec3_minima.md` |
| 4 | 65–84 | housing end, unemployment, sickness/parental leave | `cr_sec4_housing_unemp.md` |
| 5 | 84–98 | social insurance contributions | `cr_sec5_sic.md` |
| 6 | 98–111 | personal income tax | `cr_sec6_incometax.md` |
| 7 | 111–131 | extraordinary measures, consumption taxes | `cr_sec7_extra_consumption.md` |
| 8 | 131–146 | data & validation | `cr_sec8_data_validation.md` |
| 9 | 157–166 | Annex 1 uprating factors, Annex 2 policy effects | `cr_sec9_annexes.md` |

Prompt ingredients that mattered (reuse them):
- name the instruments AND their EUROMOD variable names expected in the range (from the outline);
- "capture ALL parameter values per year, copy the tables as markdown tables, preserve numbers/dates/legal references exactly";
- explicitly ask for the per-instrument **"EUROMOD modelling" notes** (simulated vs data, assumptions, deviations) — that's the part no legislation source has;
- fix the output file path and a `## N. Title (CR pages X–Y)` heading prefix (one agent still wrote `# ##` — check heading levels when assembling);
- ask for a 5-line summary as the final message (keeps the orchestrator context small).

Agents will discover `Read` can't render the PDF and fall back to pypdf/PyMuPDF in WSL on their own — with poppler installed this detour disappears.

## 3. Assemble

Write a header + table of contents, then concatenate the section files with `---` separators. Sanity checks: `grep -n "^## "` gives exactly one heading per section; spot-read one big table (e.g. the IRPP schedule) against the PDF.

## 4. Inventory the policy JSON (jq, no agents)

`extracted_parameters/<CC>.policy.json` = **array of parameter objects** `{information, values[]}` produced by the euromod-connector from the EUROMOD master. Useful queries (all via `wsl.exe … jq`; **beware nested-quoting** — for anything with `--arg` or loops, write a script to `\\wsl.localhost\Ubuntu-24.04\tmp\x.sh` with the Write tool and run `bash -c "bash /tmp/x.sh"`, because inline `\$var` gets eaten):

```bash
jq 'length'                                                    # count
jq -r '[.[] | .information.model_target | split("/")[3]] | group_by(.) | map({p:.[0],n:length}) | sort_by(-.n)'   # params per policy sheet
jq -r '[.[] | .information.unit // "null"] | group_by(.) | map("\(.[0]): \(length)")'                              # unit distribution
jq '[.[] | select([.values[].valid_from] | map(.[0:4]) | index("2025"))] | length'                                 # 2025 coverage
jq '[.[] | select([.values[].value] | map(type) | index("string"))] | length'                                      # formula-valued params
```

Things to check that were true for FR and are likely true elsewhere:
- all targets are `def_const` → **in-function parameters (tax schedules, QF ceilings…) are missing**;
- `values[].references` empty, `review_status: pending`, classification by haiku;
- formula values: FYA mid-year weighted averages `(a*n+b*m)/12#m` and cross-refs `$PSS * 4`;
- period suffixes: `#m` monthly, `#y` yearly (÷12), `#q` quarterly (÷3), `#w` weekly (×4.34), `#d` daily (×30.5), `#l` labour day (×21.73), `#s` labour day 6-day week (×26.07), `#c` capital (no conversion);
- units unreliable (rates stored as `currency`).

## 5. Write the matching doc

Structure that worked (`FR_parameter_matching.md`): JSON anatomy → value quirks → temporal coverage → sheet-by-CR-section tables (benefits / taxes separately, with page numbers and 2025-coverage) → **gaps both ways** (in CR but not JSON; in JSON but dormant) → implications for RAG ingestion and eval → generated full inventory as appendix (jq → markdown, `cat`-appended).

The matching itself is mostly name-driven: sheet `bch00_fr` ↔ CR section titled `… bch00_s …`. The non-obvious FR mappings to look for again: ARE unemployment-insurance constants hide in `ConstDef_fr` as `$UB_*`; Covid wage compensation as `$mc_*`; CSG thresholds sit in the income-tax sheet (`tinty_fr`), not the CSG sheet; VAT/excises are one giant `tco_fr` sheet with COICOP-coded names and hard-dated (`valid_to` set) series.

## 6. Cross-check and fold back

After assembly, feed surprises from the extraction back into the matching doc. FR examples: CR Table 2.3 contradicts its own narrative on SMIC/PSS percentages (CR ≠ infallible ground truth); `$bsa00_BTA_rate` is a behavioural calibration, not legislation; the 2025 CDHR exists in the CR but has no constants.

## Gotchas recap

1. **No poppler → Read can't render PDFs**; install it or let agents fall back to WSL text extraction.
2. **≤20 PDF pages per Read call**; partition on the outline.
3. **Disk-full kills all background agents unrecoverably** — check `df -h` first, relaunch (don't try to resume) if it happens.
4. **wsl.exe + Git Bash quoting mangles `$vars` and bare `/tmp/...` args** — write scripts via UNC to `/tmp`, invoke as `bash -c "bash /tmp/x.sh"`.
5. Agent heading discipline is imperfect — normalize `^## ` levels when assembling.
