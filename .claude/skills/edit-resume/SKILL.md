---
description: Edit existing resume/CV or cover letter from critique feedback and user suggestions
user-invocable: true
---

# /edit-resume

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`: First argument is the file path (required) — the content `.yaml` for resume/CL, or the `.tex` for CV. A `.md` path is the critique file. Text in quotes is inline instructions.
- `/edit-resume output/Acme/e2e_acme_resume.yaml`
- `/edit-resume output/Acme/e2e_acme_cv.tex`
- `/edit-resume output/Acme/e2e_acme_resume.yaml output/Acme/critique_acme.md`
- `/edit-resume output/Acme/e2e_acme_resume.yaml "shorten Position 1, expand Work Samples"`

If only the file path and no instructions: ask the user what to fix.

**Two edit pipelines by file extension:**
- **`.yaml` (resume or cover letter):** edit the content YAML fields directly, re-run `content_check.py`, re-render with `docx_builder.py`.
- **`.tex` (CV):** edit the LaTeX source directly, re-run `char_count.py -f cv`, recompile with `pdflatex` (unchanged from the original workflow).

---

## Safety Rules (ALWAYS ENFORCED)

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags before editing any content. Verify every claim against that table.

- Use the email from `config.md` Personal Info in all outputs
- Source ALL content from `resume_builder/experience/` files. Never fabricate.
- Resume Work Experience: paragraph tiers (P-Short/Medium/Long), NOT bullets. CV: 2L/3L bullet mix OK (check `config.md` Document Preferences)
- Resume/CL: run `python3 resume_builder/helpers/content_check.py` after edits — word count authoritative. CV: run `python3 resume_builder/helpers/char_count.py -f cv` — char count authoritative.

### FIXED Sections — Refuse if Asked to Edit
Check `config.md` FIXED Sections for the list of template-locked sections. Say no and explain: these are template-locked across all outputs.

VARIABLE sections — Resume: Summary, Technical Skills, Work Samples, Work Experience paragraphs/headers, Cross-Functional Leadership. CV: Summary, Technical Expertise, Research Experience bullets/headers.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it affects an already-applied edit: go back, fix it, re-run the budget gate
3. If it changes the edit plan: update session file, adjust remaining edits
4. If it's a question: answer it, then continue from current step
5. Never restart a phase — resume from current position

---

## Startup

Read `resume_builder/reference/shared_ops.md` — Fresh Session Startup + Session File Derivation.
Read `CLAUDE.md` — check Active Sessions and KB Corrections.
Read `config.md` — load Provenance Flags, email, FIXED Sections, document preferences.
Find and read the session file (use derivation protocol from shared_ops.md).

**Recovery check:**
- Read session file, check for existing Edit N Status
- If Edit N Status shows IN_PROGRESS: read the content YAML or .tex, identify which edits are done, resume
- If no edit in progress: proceed to Phase 1

---

## Phase 1: Load Context

Read in this order:
1. **Session file** (`output/<FolderName>/session_<name>.md`) — note: Framing Strategy, Company Context, Content Plan, Edit History
2. `resume_builder/reference/resume_reference.md` — word/char limits, budgets, fixed sections
3. The file being edited (content YAML for resume/CL, or .tex for CV)
4. Critique file (if provided in `$ARGUMENTS`)
5. JD file (path from session file's JD Info section)
6. Record baseline:
   - **Resume/CL:** `python3 resume_builder/helpers/content_check.py resume|cover_letter [file.yaml]` — note total word count / estimated pages
   - **CV:** compile current .tex, record baseline page count, run `python3 resume_builder/helpers/char_count.py -f cv [file.tex]`

**Record baseline in session file** under `## Edit [N] Baseline` (scan existing Edit History sections; next N = max existing + 1, or 1 if none):

```
## Edit [N] Baseline
- Format: resume (docx) | CV (LaTeX) | cover letter (docx)
- Pages: [N or "not verified — docx, no compile step"]
- Word/char violations: [list or "none"]
- Orphan violations (CV only): [list or "none"]
- Total word count (resume/CL) or rendered lines (CV): [N]
```

Progress: "Reading session file — [company], [role type] bundle..." / "Baseline: 0 word-count violations, ~540 total words..."

---

## Phase 2: Diagnose & Plan Edits

Gather change requests from THREE sources:
1. **User instructions** from `$ARGUMENTS` (highest priority)
2. **Critique file** (Tier 1 fixes first, then Tier 2)
3. **Auto-detected issues** from Phase 1 (word/char violations, orphans (CV), page fill)

Cross-check against **session file framing strategy** — edits must stay consistent with decisions from `/make-resume`.

**For each change, classify:**
- **MODIFY:** Change text of an existing bullet/paragraph/summary/skills field. Budget unchanged.
- **SWAP:** Replace one bullet/position paragraph with another. Budget unchanged if same variant/tier.
- **ADD:** Insert new bullet or position. Budget increases.
- **REMOVE:** Drop a bullet or position. Budget decreases.
- **VARIANT CHANGE:** e.g., CV 2L → 3L, or resume P-Medium → P-Long. Budget changes accordingly.
- **FIXED:** Blocked — show in plan with `[FIXED — cannot edit]` and explain why.

**Budget revalidation (if any change is ADD, REMOVE, SWAP-with-different-variant, or VARIANT CHANGE):**
Recalculate total word count (resume/CL) or rendered lines (CV). Compare against budget from resume_reference.md.
If OVER budget: present overflow and ask user which item to drop or shorten.
Show: `Budget: [N words/lines] vs target [T]. PASS/FAIL`

If edit targets **cover letter**: note this — Phase 4 will use CL-specific gates. Load CL content YAML path from session file Output Files section.

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present numbered edit plan. Each item shows: what, why, source, classification (MODIFY/ADD/SWAP/FIXED).
**You MUST wait for the user's explicit text response before continuing.**
Proceeding without confirmation may make unwanted edits that break package consistency.

---

## Phase 3: Load Reference Files (only confirmed edits)

Load ONLY what the confirmed edits need:

- **All edits:** `resume_builder/support/ai_fingerprint_rules.md` — scan for banned words/patterns before and after edits
- **Position/bullet expand/rewrite/add:** `resume_builder/experience/` files + matching bundle + `resume_builder/support/achievement_reframing_guide.md`
- **Summary rewrite:** Bundle (S2 summary guide) + `resume_builder/support/skills_taxonomy.md`
- **Cover letter edits:** `resume_builder/support/significance_*.md` + `resume_builder/reference/cl_reference.md`
- **Simple fixes** (spacing, header text): No extra files needed

---

## Phase 4: Execute Edits

### Resume/CL path (docx)

Edit the content YAML field(s) directly (`output/<FolderName>/e2e_<name>_[resume|cover_letter].yaml`). After each edited field:

1. Run content check:
   ```bash
   python3 resume_builder/helpers/content_check.py resume|cover_letter output/<FolderName>/e2e_<name>_[resume|cover_letter].yaml
   ```
2. Fix any OVER violations before the next field
3. If a paragraph doesn't land in its target tier (e.g. targeting P-Medium but landing SHORT), adjust immediately

Update session file Edit N Status after each individual edit.

Once all edits for this pass are applied, re-render:
```bash
python3 resume_builder/helpers/docx_builder.py render resume|cover_letter output/<FolderName>/e2e_<name>_[resume|cover_letter].yaml output/<FolderName>/e2e_<name>_[resume|cover_letter].docx
```

#### Resume/CL Verification Gates
| Gate | Check | If FAIL |
|------|-------|---------|
| Word count | Within tier target from resume_reference.md / cl_reference.md | Trim/expand |
| Render | `docx_builder.py` exits cleanly | Fix content YAML, re-render |
| Package cohesion (CL) | CL claims traceable to resume content, no contradictions | Fix |
| Anti-patterns (CL) | No generic opener, no defensive framing, no credential dump | Rewrite |

There's no automated page-fit check for `.docx` — remind the user to open the file and confirm page count/formatting.

### CV path (LaTeX, unchanged)

Edit the `.tex` source directly. After each edited section:

1. Run char count gate:
   ```bash
   python3 resume_builder/helpers/char_count.py -f cv output/<FolderName>/[file].tex
   ```
2. Fix any OVER violations or orphans before next section
3. If a bullet expansion doesn't render as expected (2L when targeting 3L, etc.), adjust immediately

Update session file Edit N Status after each individual edit.

#### CV Verification Gates
| Gate | Check | If FAIL |
|------|-------|---------|
| Char count | No OVER violations | Fix bullet before proceeding |
| Page fill | Check rendered line target from resume_reference.md | Expand/trim variable bullets |
| Page count | Match `config.md` Document Preferences | Trim/expand variable content |
| Orphan | 2L bullet last line >= 70% | Pad or trim |
| Title width | Position title + date fits 1 line | Shorten title |
| Compile | Clean pdflatex | Fix LaTeX errors |

After all edits, compile:
```bash
pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> output/<FolderName>/[file].tex
```
Use the Read tool to view the compiled PDF — check page count, white space, orphans, header wrapping.

Progress: "Editing Position 1 paragraph — was 33 words (SHORT), now 42 (OK)..." / "Rendering..." / "Compiling... 2 pages, page fill OK"

---

## Phase 5: Update Session File & Present

1. **Append Edit History** (use the N from Phase 1 baseline):
   ```
   ### Edit [N] ([date]): [short description]
   - Changes: [what changed]
   - Source: critique item # / user request / auto-detected
   - Verification: gates passed
   ```

2. **Compare against baseline:**

   | Metric | Before | After | Delta |
   |--------|--------|-------|-------|
   | Page count (CV) / total words (resume/CL) | [N] | [N] | [+/-] |
   | Word/char violations | [N] | [N] | [+/-] |
   | Orphans (CV only) | [N] | [N] | [+/-] |

   Flag any metric that worsened.

3. **Update Status** — mark critique as STALE if edits made after last critique. Update Next.

4. **Update memory pointer** if status changed.

5. **Present:** Changes summary + delta table + rendered `.docx` (resume/CL) or compiled PDF (CV).

### >>>>>> MANDATORY STOP <<<<<<
Show results. Wait for user approval or further edits.
**Resume/CL only:** remind the user to open the `.docx` to confirm page fit/formatting.
**You MUST wait for the user's explicit text response before continuing.**

### When user approves / says "looks good" / finalizes:
Run file organization from `resume_builder/reference/shared_ops.md` — Finalization check.
