---
description: Generate a tailored resume/CV from a JD
user-invocable: true
---

# /make-resume

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- File path (e.g., `JDs/*.txt`) → read that file for the JD
- Text after the path starting with "Focus:"/"Emphasize:"/"Downplay:" → focus directive
- "Quick:" prefix → Quick Mode (see below)
- Empty → ask the user for the JD
- Inline JD text (no file path) → save to `JDs/temp_<company>.txt`, proceed normally

**Two output pipelines, chosen in Phase 0:**
- **Resume (2-page, default):** JD-tailored content is written into a content YAML (shape: `resume_builder/templates/resume_content_template.yaml`), validated with `content_check.py`, and rendered to `.docx` with `docx_builder.py`. No LaTeX involved.
- **CV (5-page, unchanged):** JD-tailored content is written directly into `cv_template.tex`, validated with `char_count.py -f cv`, and compiled with `pdflatex`.

---

## Safety Rules (ALWAYS ENFORCED)

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags before generating any content. Verify every claim against that table.

- Use the email from `config.md` Personal Info in all outputs
- Resume Work Experience: PARAGRAPH format, tiered P-Short/Medium/Long (NOT bullets). CV: 2L/3L bullet mix OK, check `config.md` Document Preferences
- Resume Technical Skills / Work Samples / Cross-Functional Leadership: flat bold-label + sentence bullets
- Source ALL content from `resume_builder/experience/` files. Never fabricate.
- Resume: run `python3 resume_builder/helpers/content_check.py` after each section — word-count authoritative. CV: run `python3 resume_builder/helpers/char_count.py` — char-count authoritative.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it affects an already-written section: go back, fix it, re-run the budget gate
3. If it changes the content plan: update session file Content Plan
4. If it's a question: answer it, then continue from current step
5. Never restart a phase — resume from current position

---

## Startup

Read `resume_builder/reference/shared_ops.md` for session startup, file derivation, and organization protocols.

Then:
1. Read `CLAUDE.md` — check Active Sessions and KB Corrections
2. Read `config.md` — load Provenance Flags, email, document preferences, role types
3. If session file exists for this JD:
   - Read session file, check Status
   - Phase 0: DONE, Phase 1: PENDING → resume at Phase 1
   - Phase 1: DONE → resume at Budget Gate
   - Phase 2: IN_PROGRESS → read the content YAML (resume) or .tex (CV), check what sections exist, resume from checkpoint
   - Phase 2: DONE → "Resume already done. Run /make-cl next." Show next command. Stop.
4. If no session file: proceed to Phase 0

---

## Quick Mode

Trigger: `$ARGUMENTS` starts with "Quick:"

Defaults:
- Select all HIGH priority achievements from bundle's Priority Matrix (P-Long for resume, 2L for CV)
- Fill remaining budget with MEDIUM priority in Priority Matrix order
- Default format: 2-page resume (unless JD clearly requires CV)
- Skip Phase 0 STOP and Phase 1 STOP
- Keep Budget Gate (auto-pass if within target) and end-of-resume STOP
- Run all phases with progress commentary instead of interactive stops

---

## Phase 0: Research & Session Setup

**Read these files:**
1. The JD (from `$ARGUMENTS`)
2. `resume_builder/reference/resume_reference.md` — Budget Card, Section Specs, Word/Char Limits, Page Budgets
3. `config.md` — Role-Type Decision Tree to identify the matching bundle

**Web Search (MANDATORY — 2-3 searches).** Load WebSearch via ToolSearch first.
1. `[Company] research & development [key JD domain]` — products, recent projects
2. `[Company] [specific technology from JD]` — concrete hooks for cover letter
3. `[Company] careers [role type] culture` OR recent news — hiring context

If web search returns no results: use JD text + training knowledge. Flag: "Web search returned limited results — CL hooks may be generic."

**Produce all of these (reference `resume_builder/reference/session_file_template.md` for format):**
- **JD Analysis** — classify every requirement as Direct / Bridge (with confidence) / Gap. Extract ATS keywords by category.
- **Company Context** — mission, role purpose, culture signals, "why them" angle (from web research)
- **Framing Strategy** — lead narrative, reframing map, emphasize/downplay, CL hooks, user focus directives
- **Critique Context** — reviewer persona, competitive landscape, domain vocabulary
- **Cover Letter Plan** — institution type, paragraph structure, hooks, jargon level

**Create output folder:**
Derive folder name from JD filename: `JDs/JD_Acme.txt` → `output/Acme/`
```bash
mkdir -p output/<FolderName>/
```
Write session file to `output/<FolderName>/session_<name>.md` (NOT flat `output/`).
All subsequent output files go in this folder.

**Verify completeness:** Re-read the session file. Confirm these 8 sections are non-empty: JD Info, Requirements table, ATS Keywords, Gap Assessment, Company Context, Framing Strategy, Critique Context, Cover Letter Plan. Fill any missing section before presenting.

**Write memory pointer** to `CLAUDE.md` Active Sessions.

**Update session file Status:** `Phase 0: DONE`

Progress: "Searching for [company] + [domain]..." / "JD analysis: X/Y requirements direct match, Z bridges, W gaps"

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present: research summary, role type + bundle, format, framing strategy.
Ask user to confirm: (1) role type + bundle, (2) format (resume/docx vs CV/LaTeX), (3) framing strategy.
**You MUST wait for the user's explicit text response before continuing.**
Proceeding without confirmation misaligns the entire resume and requires full regeneration.

---

## Phase 1: Plan Content

**Re-read `output/<FolderName>/session_<name>.md`** — specifically Framing Strategy and ATS Keywords.

**Read:**
1. The matching bundle from `config.md` Role Types → `resume_builder/bundles/bundle_[role_type].md` — Section 1 (Priority Matrix)
   - For hybrid JDs: read both bundles. Use primary for Priority Matrix, secondary for Reframing Map on 1-2 bridging positions/bullets.
2. All experience files from `resume_builder/experience/`
3. `resume_builder/support/achievement_reframing_guide.md`
4. `resume_builder/support/skills_taxonomy.md`
5. `resume_builder/support/pub_metadata.md`

**Resume format — present one table per Work Experience position (paragraph tiers, not bullets):**

**[Position Name] (Tier: P-Short/Medium/Long)**

| | ID | Achievement | Include in paragraph? | JD Match |
|---|---|-------------|------------------------|----------|
| * | P1-1 | [short description] | Yes | Direct |
| * | P1-5 | [short description] | Yes | Direct |
| o | P1-3 | [short description] | Maybe (space permitting) | Bridge |
| x | P1-7 | [short description] | No | Weak |

**Legend:** `*` = recommended (HIGH on Priority Matrix + Direct JD match) | `o` = available (MEDIUM priority or Bridge match) | `x` = not recommended (LOW priority or Gap)

Also plan, per the same legend: **Technical Skills** groups (5-7), **Work Samples** categories/items, and **Cross-Functional Leadership** bullets (3-5) — each is a flat bullet, not a paragraph.

**After all positions/sections, show:**
- Position tier assignments (which get P-Long/Medium/Short) and rough total word count vs the ~500-600 word Work Experience+bullets budget (from Quick Budget Card in resume_reference.md)
- Work Samples/Cross-Functional Leadership bullet counts vs the 5-7 target
- Forced exclusions per provenance flags
- Focus directive impact (what changed vs Priority Matrix defaults)
- CV (if this format instead): confirm first bullet of first experience is 2L (page 1 rule)

**Update session file** — write the Content Plan tables (positions + tiers, Skills groups, Work Samples, Cross-Functional Leadership). Status: `Phase 1: DONE (N positions + M flat bullets confirmed)`

Progress: "Reading experience files for content candidates..." / "Recommending tiers for N positions"

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present content plan. Wait for user to confirm/modify selections.
**You MUST wait for the user's explicit text response before continuing.**
If you proceed without confirmation, you will generate content the user didn't approve.
**Update session file with confirmed plan before continuing.**

---

## Budget Gate (AFTER user confirms content plan, BEFORE Phase 2)

**Re-read session file Content Plan section** to verify confirmed tiers/counts.

- Check budget targets from `resume_builder/reference/resume_reference.md` Budget Card.
- Show: `Budget: [N] positions/bullets vs target [T]. PASS/FAIL`
- **FAIL = do not proceed. Reconcile with user first.**

---

## Phase 2: Generate

**Re-read to restore context after compaction:**
1. `output/<FolderName>/session_<name>.md` (framing + confirmed content plan)
2. `resume_builder/reference/critical_rules.md` — Word/Character Limits, FIXED Sections
3. `resume_builder/support/ai_fingerprint_rules.md` — Banned words, structural rules, post-gen checklist

### Resume path (docx)

**Read template:** `resume_builder/templates/resume_content_template.yaml`
FIXED fields (header contact info, education, publication author/journal text — from `config.md` FIXED Sections) are copied verbatim — only generate VARIABLE fields (summary, tagline, Work Experience theme/paragraph, Technical Skills, Work Samples categories, Cross-Functional Leadership).

**Read section specs:** `resume_builder/reference/resume_reference.md` — Section-by-Section Specs (Resume)

**Write the content YAML section by section** to `output/<FolderName>/e2e_<name>_resume.yaml`, following Section-by-Section Specs:
1. Header (contact fields from config.md + JD-tailored tagline)
   - Update Status → `Phase 2: Header DONE`
2. Summary → check against session framing strategy; bold the opening role-title phrase (`**Role Title**`)
   - Update Status → `Phase 2: Summary DONE`
3. Technical Skills (flat bullets)
   - Update Status → `Phase 2: Skills DONE`
4. Each Work Experience position's paragraph → **CONTENT CHECK GATE after each position**
   - After each position: Update Status → `Phase 2: [Position] DONE`
5. Work Samples (flat bullets, grouped, hyperlinked — use `[text](url)` markup, source URLs from bundle/experience files, never invent one)
6. Education (FIXED, copy verbatim)
7. Selected Publications (score all, keep only top 5)
8. Cross-Functional Leadership (flat bullets)
9. **RENDER GATE**

Progress: "Writing Position 1 paragraph..." / "Position 3 is SHORT at 22 words for a P-Medium target — expanding" / "Rendering resume.docx..."

#### CONTENT CHECK GATE (per position/section)
```bash
python3 resume_builder/helpers/content_check.py resume output/<FolderName>/e2e_<name>_resume.yaml
```
No OVER violations. **Fix before next position.**

#### RENDER GATE
```bash
python3 resume_builder/helpers/docx_builder.py render resume output/<FolderName>/e2e_<name>_resume.yaml output/<FolderName>/e2e_<name>_resume.docx
```
Must exit cleanly (no traceback). There is no automated page-count check — note to the user that they should open the `.docx` to confirm page fit (see Post-Generation Verification).

### CV path (LaTeX, unchanged)

**Read template:** `resume_builder/templates/cv_template.tex` + `cv.cls`
FIXED sections (from `config.md` FIXED Sections) are template-locked — only generate VARIABLE sections (Summary, Skills, Experience bullets/headers).

**Read section specs:** `resume_builder/reference/resume_reference.md` — Section-by-Section Specs (CV)

**Generate section by section**, following Section-by-Section Specs:
1. Summary → Update Status → `Phase 2: Summary DONE`
2. Technical Expertise (Format C) → Update Status → `Phase 2: Skills DONE`
3. Each position's bullets → **CHAR COUNT GATE after each position**
   - Position titles: bold theme + date must fit ONE line. If wrapping, shorten title.
   - After each position: Update Status → `Phase 2: [Position] DONE`
4. **PAGE FILL GATE after all experience**

Save `.tex` to `output/<FolderName>/e2e_<name>_cv.tex`

#### CHAR COUNT GATE (per position)
```bash
python3 resume_builder/helpers/char_count.py -f cv output/<FolderName>/e2e_<name>_cv.tex
```
No OVER violations. Last line of 2L bullets >= 70% fill. **Fix before next position.**

#### PAGE FILL GATE
Check rendered line target from resume_reference.md. **If FAIL: add/trim variable bullets.**

#### COMPILE GATE
```bash
pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> output/<FolderName>/e2e_<name>_cv.tex
```
Verify page count matches `config.md` Document Preferences. Use the Read tool to view compiled PDF — check orphans, header wrapping, page fill. **If FAIL: fix variable content, recompile.**

---

**Update session file** — add Output Files.

Run the Post-Generation Verification checklist from `resume_builder/reference/resume_reference.md` before proceeding.

Update Status → `Phase 2: [Render|Compile] DONE`

---

## End of /make-resume

Update session file Status:
- `Resume: DONE`
- `Cover Letter: PENDING`
- `Critique: PENDING`
- `Next: /make-cl output/<FolderName>/session_<name>.md`
- `Next Critique: /critique output/<FolderName>/session_<name>.md`

### >>>>>> MANDATORY STOP <<<<<<
Present: resume summary (pages/word count for docx, or page count for CV, any violations fixed).
**Resume (docx) only:** remind the user — "Open the .docx in Word to confirm page fit and formatting before submitting; this pipeline doesn't auto-verify layout or export a PDF."
**You MUST wait for the user's explicit text response before continuing.**

"Resume done. Next steps:
1. /clear
2. [exact /make-cl command with session file path]"
