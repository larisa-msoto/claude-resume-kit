---
description: Re-critique existing resume/CV output files against a JD
user-invocable: true
---

# /critique

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- Session file path (e.g., `output/Acme/session_acme_engineer.md`) → read session file, derive output paths from Output Files (`.yaml`+`.docx` for resume/CL, `.tex` for CV)
- File path(s) + JD source (existing format) → backward compatible
- Session name (e.g., `acme_engineer`) → find session file via derivation

If no CL provided or found in session file, critique resume/CV alone (Part 7 adjustments noted below).

---

## Safety Rules

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags. Verify every claim against that table.
Check `config.md` KB Corrections Log — do not flag corrected items as errors.
Use the email from `config.md` Personal Info — flag if a different email appears in output.
FIXED sections (from `config.md` FIXED Sections) are template-locked — do not flag for editing. Flag only VARIABLE sections.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it changes scoring criteria or focus: adjust the critique accordingly
3. Never restart — resume from current position

---

## Startup

Read `resume_builder/reference/shared_ops.md` — Fresh Session Startup + Session File Derivation.
Read `CLAUDE.md` — check Active Sessions and KB Corrections.
Read `config.md` — load Provenance Flags, FIXED Sections, email.
Find and read the session file for the output being critiqued (use derivation protocol from shared_ops.md).

**Recovery check:**
- If CL not DONE in session file → "CL not yet generated. Run `/make-cl` first."
- If Critique: CURRENT → "Already critiqued (score X/100). Re-run? Waiting for confirmation."
- If Critique: STALE → "Edits made since last critique. Re-critiquing."
- If Critique: PENDING → proceed

---

## Protocol

1. **Read session file** — specifically note:
   - **Company Context** → reviewer persona, "why this company"
   - **Framing Strategy** → intentional reframing decisions (flag only execution inconsistencies, not the strategy itself)
   - **Cover Letter Plan** → CL structure rationale
   - **Critique Context** → reviewer persona, competitive landscape, domain vocabulary
   - If session file lacks Company Context or Critique Context: do 1-2 web searches to fill gaps
2. Read `resume_builder/reference/critique_framework.md`
3. Read `resume_builder/support/ai_fingerprint_rules.md` — use Section 6 checklist in Part 7 verification
4. Read the resume/CV/CL content — derive paths from session file Output Files, or from `$ARGUMENTS`:
   - **Resume/CL (docx):** read the content `.yaml` (this is where the actual text lives — the `.docx` is a render artifact). If you need to confirm what actually rendered, extract text from the `.docx` with `python-docx` rather than trying to read the binary directly.
   - **CV (LaTeX):** read the `.tex` source directly.
5. Read the JD (path from `$ARGUMENTS` or session file)
6. Read the relevant bundle (`resume_builder/bundles/bundle_[role_type].md` — from session file)
7. Run the budget check:
   - **Resume/CL:** `python3 resume_builder/helpers/content_check.py resume|cover_letter [file.yaml]`
   - **CV:** `python3 resume_builder/helpers/char_count.py -f cv [file.tex]`
8. Verify rendering:
   - **Resume/CL:** `python3 resume_builder/helpers/docx_builder.py render resume|cover_letter [file.yaml] [file.docx]` — confirm it exits cleanly. **There is no automated visual/page-fit check for `.docx`** — note in Part 8: "Visual layout not verified — content and word-count budgets checked, but page fit, spacing, and header wrapping require opening the .docx in Word." Do not claim page count or layout quality you haven't actually seen.
   - **CV:** `pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> [file.tex]`, then use the Read tool to view the compiled PDF — check orphans, page fill, header wrapping. If compile fails: note "COMPILE FAILED — visual checks could not be verified" in Part 8.
9. If a prior critique exists (`output/<FolderName>/critique_<name>.md`): read it and note previous score.
10. **Paper Hook Verification:** If the CL cites named papers, PIs, programs, or publications, web-search to verify title, journal, year, and PI affiliation. Flag factual errors as Tier 1 fixes.

11. **Run the full critique per critique_framework.md. The output MUST contain ALL 8 sections** (even if the framework file has partially compacted, produce every section):

    1. **Domain-Specialist Lens** — 7 elements:
       (a) Reviewer persona (b) Company context (c) JD vocabulary extraction (d) Domain vocabulary map
       (e) Gap ranking (fatal/serious/cosmetic) (f) Methodology transfer test (g) Competitive landscape
    2. **Five-Perspective Read-Through** — ATS, Recruiter (10s), HR (30s), HM (2min), Technical (10min) — each with verdict
    3. **Eight-Dimension Scoring** — weighted table summing to 100
       (ATS 15%, Summary 10%, Skills 10%, Bullets 25%, Publications 10%, Narrative 15%, Visual 5%, Credibility 10%)
       - For the resume format, "Bullets" covers Work Experience paragraphs (P-Short/Medium/Long) plus the flat bullets in Technical Skills/Work Samples/Cross-Functional Leadership — score against `resume_reference.md`'s word-count specs, not char counts. CV scoring is unchanged.
       - **Visual (5%)** for resume/CL: score based on content structure/formatting choices visible in the content YAML (section order, use of bold/links) — not actual rendered layout, which isn't verified. Say so explicitly if this caps your confidence in this sub-score.
    4. **Interview Likelihood** — per-reader probability + ceiling analysis
    5. **Tiered Improvements** — Tier 1 (>=1pt each), Tier 2 (0.3-0.9), Tier 3 (<0.3)
    6. **Interview Bridge Points** — 5-7 resume-to-interview talking points
    7. **Cover Letter Critique** — 6 sub-checks (6A anti-patterns, 6B tailoring, 6C context-specific, 6D ATS, 6E structural, 6F package cohesion)
       - **If no CL provided:** Skip 6A-6E. Run 6F as resume standalone assessment — evaluate whether the resume earns an interview without a CL. Note: "Cover letter not provided — package cohesion not assessed."
    8. **Post-Generation Verification** — mechanical + content + structural checklists (see resume_reference.md — includes the resume/CL "open in Word to confirm layout" reminder)

12. Save to `output/<FolderName>/critique_<name>.md`
13. **Update session file** — Critique Summary (score, findings, tier 1 fixes), Status → Critique: CURRENT
14. **Update memory pointer** with new score

Progress: "Reading session file for framing context..." / "Running ATS keyword scan — 16/20 match..." / "Scoring 8 dimensions..." / "Score: 87.0/100"

### >>>>>> MANDATORY STOP <<<<<<
Present: score table + tier 1 actionable fixes + interview likelihood.
**Resume/CL:** remind the user the visual layout (page fit, spacing) wasn't automatically verified — open the .docx to confirm.
**You MUST wait for the user's explicit text response before continuing.**
If edits needed, tell user to run `/edit-resume`.

### When user approves / says "looks good" / finalizes:
Verify all expected files exist in `output/<FolderName>/`:
- session file
- Resume: `.yaml` + `.docx` — OR CV: `.tex` + `.pdf` + compile artifacts
- CL: `.yaml` + `.docx`
- critique `.md`
Confirm to user: "Package complete in output/<FolderName>/ — [list files]"
