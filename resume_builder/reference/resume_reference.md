# Resume & CV Generation — Reference

> Resume/CV-specific rules. Read by `/make-resume` and `/edit-resume`.
> Companion files: `cl_reference.md` (CL rules), `critical_rules.md` (compact re-read).
> Shared rules (provenance, anti-fabrication): `CLAUDE.md`
>
> **Two different pipelines, by format:**
> - **Resume** (2-page): content YAML (`resume_content_template.yaml` shape) → `docx_builder.py` → `.docx`. Word-count budgets, validated by `content_check.py`.
> - **CV** (5-page): `cv_template.tex`/`cv.cls` → `pdflatex` → `.pdf`. Character-count budgets, validated by `char_count.py -f cv`. Unchanged from the original LaTeX system.
>
> Sections below are marked **[Resume]** or **[CV]** where they diverge; unmarked sections apply to both.

---

## QUICK BUDGET CARD (read this FIRST)

```
RESUME (2-page, docx_builder.py):  Work Experience = paragraph tiers (P-Short/Medium/Long) across 6-9 positions
                                    Skills / Work Samples / Cross-Functional Leadership = 5-7 flat bullets each | 5 pubs | no awards section
                                    Total body ~500-600 words for 2 pages (calibrate — see Page Fill Budgets)
CV     (5-page, cv.cls):           19-21 variable bullets (45 rendered lines) | Skills 17 lines (4-4-3-3-3) | all pubs | 6 awards

Resume paragraph (word count): P-Short 19-28w | P-Medium 35-48w | P-Long 53-61w
Resume flat bullet (Skills/Work Samples/Cross-Functional): 25-38 words
CV bullet (rendered char count): max 3 rendered lines | 2L: 168-182 chars | 3L: 250-268 chars (target ~175/~260)

Cover letter: Resume package = 1 page (250-300 words) | CV package = 1-2 pages (350-450 words)
Full package: Resume + CL = 3 pages | CV + CL = 6-7 pages
```

**If your content doesn't match the budget above, STOP and fix before generating.**

---

## Section-by-Section Specs

### Resume [Resume — docx]

1. **Header** (`header` YAML block): name, tagline, location, phone, email, LinkedIn, GitHub, languages, **and the immigration line** — all in the header block (not a separate section). Immigration line: include for USA JDs, omit the `immigration_line` field entirely for non-USA JDs.
2. **Summary** (`summary` field, bundle Section 2): 4-5 sentences. Bold the opening role-title phrase, e.g. `**Genomic Scientist** with...`. Target ~70-85 words.
3. **Work Experience** (`work_experience` list, experience files + achievement_reframing_guide.md): PARAGRAPH format, not bullets. Write each position's `paragraph` field FRESH per Experience Writing Protocol (below). 6-9 positions typical. Run `content_check.py` after each position.
   - **After all positions: verify total paragraph tier mix matches page budget** (see Page Fill Budgets)
4. **Technical Skills** (`technical_skills` list, bundle Section 4 + skills_taxonomy.md): flat bullet format — 5-7 groups, each a `label` + one-sentence `text` (no nested dashes). Target 25-38 words per bullet.
5. **Work Samples** (`work_samples` list, bundle Section 5 + experience files): flat bullet format — one bullet per category, comma-separated hyperlinked items sourced from bundle/experience files. Select/order categories by JD relevance. Never invent a URL.
6. **Education** (`education` list): FIXED — copy from your real data, never edited per JD.
7. **Selected Publications** (`publications.items`, pub_metadata.md): score ALL publications per JD relevance, list ONLY the top 5 — `docx_builder.py` also hard-caps at 5 as a safety net. Copy FIXED author+journal text, GENERATE JD-relevant ordering.
8. **Cross-Functional Leadership and Stakeholder Engagement** (`cross_functional_leadership` list, bundle Section 6 + experience files): flat bullet format — bold label + 1-2 sentence description, same shape as Technical Skills. Target 25-38 words per bullet.

> No Honors & Awards section in the resume format (dropped to match real-world convention). CV format keeps it — see below.

### CV (cv.cls) [CV — LaTeX, unchanged]

1. **Research Summary** (bundle Section 2): Exactly 6 body lines. 500-540 rendered chars (HARD MAX 545, floor ~490). Orphan: last line >= 62 chars. Technical identity, not narrative.
2. **Education**: FIXED — copy verbatim from cv_template.tex
3. **Technical Expertise** (bundle Section 4 + skills_taxonomy.md): 4-4-3-3-3 ALWAYS (17 body lines). Bold penalty: 91 - (0.25 x bold_chars).
4. **Research Experience**: Exactly 45 rendered bullet lines across 19-21 bullets, plus sub-theme lines.
   - cv.cls: Args 3+4 on SEPARATE italic lines
   - Max 3 rendered lines per bullet. CV-2L <= 190, CV-3L <= 280 (target ~175/~260)
   - **Running total must reach exactly 45 rendered lines**
5. **Fellowships & Honors**: FIXED — items from cv_template.tex
6. **Publications**: FIXED — full list from cv_template.tex
7-10. **Presentations, Mentorship, Collaborations, Computing**: All FIXED from cv_template.tex

---

## Word & Character Limits

### Resume [Resume — word counts, ZERO precision guarantee]

Word documents reflow — there is no exact "this renders as N lines" guarantee the way LaTeX gave us. Treat these as budgets to write toward, not hard per-line stops. `content_check.py` classifies against the ranges below; there is no orphan rule (Word wraps naturally) and no bold-character penalty math (proportional-font bold width isn't precisely predictable without rendering).

**Work Experience paragraph tiers:**

| Tier | Sentences | Word Target | HARD MAX |
|------|-----------|-------------|----------|
| P-Short | 1 | 19-28 words | 32 |
| P-Medium | 2 | 35-48 words | 54 |
| P-Long | 3-4 | 53-61 words | 68 |

**Technical Skills / Work Samples / Cross-Functional Leadership flat bullets:**

| Target | Word Range | HARD MAX |
|--------|------------|----------|
| 1 bullet | 25-38 words | 44 |

**MANDATORY: Run `content_check.py` after writing each position/bullet, not just at the end.** If OVER the hard max, trim before moving to the next element.

```bash
python3 resume_builder/helpers/content_check.py resume output/<FolderName>/resume_content.yaml
```

### CV (11pt, textwidth=7.5in) [CV — rendered character counts, unchanged]

**MANDATORY: Count rendered characters for EVERY bullet BEFORE writing it.** Strip LaTeX markup before counting: `\textbf{X}` -> X, `\textit{X}` -> X, `\ce{X}` -> X, `$\beta$` -> 1 char, `\sim` -> 1 char, `$<$` -> 1 char, `$^\dagger$` -> 1 char, `--` -> 1 char (en-dash), `\underline{X}` -> X, `\href{url}{text}` -> text only.

| Target Lines | Rendered Char Range | HARD MAX | Orphan Threshold |
|-------|---------------|---------|------------------|
| 1 line | 88-93 chars | 101 | -- |
| 2 lines | 168-182 chars | 190 | Last line >= 65 chars |
| 3 lines | 250-268 chars | 280 | Last line >= 65 chars |

> **WARNING: AIM FOR THE MIDDLE OF THE TARGET RANGE — NOT THE HARD MAX.** A CV-2L should target ~175, not 190. Em-dash (---) counts as 1 char but renders ~2x wide — budget 2 extra chars per em-dash.

**CV Bold Width Penalty:** Effective limit = 91 - (0.25 x bold_char_count)
- 0 bold: safe up to 91 chars/line (HARD MAX 93)
- 2-3 bold tools (~10-18 bold chars): 85-88 effective --> use 83-88 as default
- 5+ bold tools (~28+ bold chars): 83-85 effective --> tighten to 80-85

**CV orphan rule:** last rendered line of a multi-line bullet must fill >= 70% of line width.

**CV per-bullet enforcement protocol:**
1. Write the bullet text (LaTeX source)
2. Strip all markup mentally → count rendered chars
3. If count > HARD MAX → rewrite immediately (do NOT proceed)
4. If multi-line and last line < orphan threshold → rewrite to fill or shorten
5. **Aim for the middle of the range**, not the max.

**CV verification tool:** `python3 resume_builder/helpers/char_count.py -f cv output/file.tex`

### Variant Naming (combined reference)

| Variant | Document | Budget Unit | Target Range | HARD MAX |
|---------|----------|-------------|---------------|----------|
| Resume P-Short | 2-page resume (Work Experience) | words | 19-28 | 32 |
| Resume P-Medium | 2-page resume (Work Experience) | words | 35-48 | 54 |
| Resume P-Long | 2-page resume (Work Experience) | words | 53-61 | 68 |
| Resume flat bullet | 2-page resume (Skills/Work Samples/Cross-Functional) | words | 25-38 | 44 |
| CV-2L | 5-page CV | rendered chars | 168-182 | 190 |
| CV-3L | 5-page CV | rendered chars | 250-268 | 280 |

---

## Page Fill Budgets

### 2-Page Resume [Resume — docx, word-count based]

Work Experience uses paragraph tiers (P-Short/Medium/Long), not bullets. Technical Skills, Work Samples, and Cross-Functional Leadership all use the flat bold-label + sentence bullet format (5-7 bullets each).

**Paragraph Tier Budget:**

Across 6-9 Work Experience positions, allocate:
- **2-3 positions** (most JD-relevant, typically the most recent) → **P-Long** (53-61 words each)
- **2-4 positions** (supporting relevance) → **P-Medium** (35-48 words each)
- **2-4 positions** (older/tangential) → **P-Short** (19-28 words each)

**Total body word count target: ~500-600 words** across Summary + Work Experience + Technical Skills + Work Samples + Publications (5) + Cross-Functional Leadership, for a 2-page document at `docx_builder.py`'s default margins/font (see `STYLE` dict). `content_check.py` reports this total and an estimated page count using a `WORDS_PER_PAGE` constant.

**This constant is a starting estimate, not a verified fact.** Calibrate it once: render a test resume with realistic content, open it in Word, note the actual page count, then adjust `WORDS_PER_PAGE` in `content_check.py` (and the target ranges above, if needed) to match. Re-run this check any time the header/margins/font in `docx_builder.py`'s `STYLE` dict change.

**Adjustments:**
- Fewer positions selected (JD calls for a tighter resume): shift budget toward P-Long on the remaining positions
- Running short of 2 pages: add a Work Samples/Cross-Functional Leadership bullet, or upgrade a P-Medium position to P-Long
- Running over 2 pages: trim the weakest P-Short position's word count, or drop it and redistribute

**No exact page-fit guarantee.** Unlike the old LaTeX pipeline, there is no compile-and-count-lines step. After generating, **the user opens the `.docx` in Word to do the final visual check** (page count, spacing, header wrapping) before submitting — see the note in Post-Generation Verification.

### 5-Page CV (cv.cls, 11pt) — LOCKED [CV — LaTeX, unchanged]

Total: **~209 rendered text lines** across 5 pages. 1-2 lines slack at bottom of page 5 is acceptable.

The exact line budget depends on your template's FIXED sections (publications, presentations, awards, etc.). Count the FIXED lines in your template, then allocate the remainder to JD-dependent content. The key constraints:

| Category | Status |
|----------|--------|
| Header, Education, Honors, Pubs, Presentations, etc. | FIXED (count from template) |
| Research Summary | JD-DEPENDENT (typically 7 lines: 1 heading + 6 body) |
| Technical Expertise | JD-DEPENDENT (typically 18 lines: 1 heading + 17 body) |
| Experience bullets | JD-DEPENDENT (**target 45 rendered lines**, 19-21 bullets, 2L/3L mix) |
| Sub-theme names | JD-DEPENDENT (varies by position count) |

**Experience bullet mix options (45 rendered lines):**
- 18x2L + 3x3L = 21 bullets | 15x2L + 5x3L = 20 | 12x2L + 7x3L = 19
- Allocate more bullets to JD-relevant positions, fewer to tangential ones

**Sub-theme rebalancing:** To shift bullet weight toward a more JD-relevant sub-theme: (a) drop the weakest bullet from a less-relevant sub-theme (-2L), (b) split a high-content 3L achievement into two 2L bullets (method + finding, +1L). Net = -1L saved while adding a bullet where it matters. Both split bullets must stay within char limits. Never split a 2L bullet — it becomes two 1L fragments that look thin.

**Position header rule:** The position title + date must fit on ONE line. If the title is too long, shorten the title so the date doesn't wrap to a second line. Test by compiling — if the date wraps, trim the title.

**CV Page 1 rule:** The FIRST bullet of the FIRST experience position MUST be 2L (not 3L). A 3L first bullet pushes content below the page 1 fold. Plan this during Phase 1 bullet planning.

**Budget workflow:** The line budget is pre-calculated from your template. Do NOT recalculate. Use the bullet counts above directly. After generation, verify that total bullet rendered lines = 45.

---

## Experience Writing Protocol (Experience-File-First)

**DO NOT use pre-written content.** Write every position's content FRESH from experience files, reframed for the target JD. Resume Work Experience is PARAGRAPH format (2-4 sentences, no bullets, written into the `paragraph` YAML field); CV Research Experience stays BULLET format (2L/3L, LaTeX `\item`s).

**Required files:** Experience files (all) + achievement_reframing_guide.md + bundle Section 1 (Priority Matrix) + bundle Section 3 (Reframing Map)

**Protocol:**
1. Determine document format -> look up variant (Resume: P-Short/Medium/Long paragraph tier; CV: 2L/3L bullet) and budget
2. Allocate paragraph tier (resume) or bullet count (CV) per position by JD relevance
3. For each position, consult bundle's **Priority Matrix** (Section 1) to rank achievements
4. For each achievement, consult **Achievement Reframing Guide** for role-type-specific framing directives
5. Write the paragraph/bullet FRESH using target-domain vocabulary from bundle's **Reframing Map** (Section 3). For resume paragraphs: weave 2-4 selected achievements into flowing sentences (first- or third-person, but consistent throughout the document) rather than a list.
6. Verify word count (resume, `content_check.py`) or char count (CV, `char_count.py`) per-position/bullet BEFORE moving to the next one
7. After all positions written: run the **First-Pass Reframing Checklist** (in achievement_reframing_guide.md)

**Reframing during writing (NOT after):** Every paragraph/bullet should use target-domain vocabulary from the start. This is the single highest-ROI step: reframing alone moves scores from ~60 to ~85.

**Hybrid JDs (two role types):** Use primary role type's Priority Matrix for achievement ranking. Use secondary role type's Reframing Map for 1-2 positions/bullets that bridge to the secondary domain.

---

## Position Title Format

**Resume — FLIPPED format (JD theme as bold title, role as subtitle):** [Resume]
Bold `theme` field = JD-customized domain theme (the single most powerful JD customization lever).
Italic `role_institution` field = formal role + institution.

| Position | `theme` (JD-customizable) | `role_institution` |
|----------|-----------------------------|----------|
| Position 1 | [Theme, e.g., "First-Principles Discovery & ML-Accelerated Simulation"] | [Your Role], [Institution] |
| Position 2 | [Theme] ([Notable Award if applicable]) | [Your Role], [Institution] |
| Internship | [Theme — FIXED] | [Your Role], [Company] |

Body under each header is a single paragraph, written directly in the position's `paragraph` YAML field — see Section-by-Section Specs above.

**CV -- CONVENTIONAL format:** [CV]
Bold line = formal role title. Mentors on separate line. Sub-headers = story threads (underlined).

---

## Immutable Elements — NEVER Modify

### Resume [Resume — docx]

- **`docx_builder.py` STYLE dict** (fonts, margins, colors, heading rule) — calibrated. Never override per-generation; if the look needs to change, edit the dict itself (a one-time change affecting all future resumes), not a single output.
- **Section functions/order in `build_resume()`** — the section list and order (Header → Summary → Work Experience → Technical Skills → Work Samples → Education → Selected Publications → Cross-Functional Leadership) is code-locked. Don't reorder or add sections in a single content YAML.
- **FIXED content fields**: `header` (except the JD-tailored `tagline`), `education`, publication author/journal text, any position marked FIXED. Copy verbatim from your real data every time.
- **No Honors & Awards section.**

**If content overflows 2 pages:** Fix by shortening VARIABLE content only (summary, flat bullets, Work Experience paragraphs). Run `content_check.py` to check each element is within its tier's word range — an OVER element is the most common cause of overflow. There's no compile step to catch this automatically; **open the rendered `.docx` to confirm actual page count** before calling the output done.

**When updating an existing resume (not generating from scratch):** Only modify VARIABLE fields in the content YAML — `summary`, `tagline`, `technical_skills`/`work_samples`/`cross_functional_leadership` text, `work_experience[].theme`/`paragraph`. Never touch `header` contact fields, `education`, or publication author/journal text, even if a critique flags them as improvable. Re-render via `docx_builder.py` after every edit.

### CV [CV — LaTeX, unchanged]

- **`\vspace` values** between sections — calibrated. Do not add, remove, or adjust.
- **`\geometry` settings** (margins, textwidth, textheight) — locked per template.
- **FIXED section content**: Education, Fellowships, Publications, Presentations, Mentorship, Collaborations, Computing, Internship. Copy verbatim from template.
- **`.cls` formatting** (font sizes, section rules, item separators, skill group spacing) — never override with inline LaTeX.
- **Header layout** (name, email, location, icons) — structure is template-locked. Only the email address and link URLs are configurable.

**If content spills to an extra page:** Fix by shortening VARIABLE content only. Count rendered characters to ensure bullets fit their target line count. Compile with `pdflatex` and verify page count = 5.

**When updating an existing CV output:** Only modify VARIABLE content. Never touch FIXED sections, vspaces, geometry, or cls overrides.

---

## Post-Generation Verification

Run this checklist before critique. Also used as Part 7 of critique_framework.md.

Before presenting final output, verify:

- [ ] **[Resume]** `content_check.py` shows no OVER violations; total word count within the page-fill target
- [ ] **[Resume]** `docx_builder.py render` exits cleanly (no traceback) and produces a `.docx`
- [ ] **[Resume]** Note to user: "Open the .docx in Word to confirm page count/spacing before submitting — layout is not automatically verified"
- [ ] **[CV]** `char_count.py -f cv` shows no OVER violations; no orphan violations
- [ ] **[CV]** `pdflatex` compiles cleanly; page count = 5 (verified via Read tool on the PDF)
- [ ] Em-dash count: max 2 per document (resume or CL)
- [ ] No -ing analysis endings on bullets or paragraph sentences ("...advancing the field", "...contributing to Y"). Restructure to end with a concrete result or metric.
- [ ] All content checks pass (ATS, terms, inflation, provenance, pubs, cover letter)
- [ ] All narrative checks pass (scan test, per-position flow, cross-position arc, CV sub-headers)
- [ ] Company/institution name spelled correctly throughout
- [ ] Date format consistent (Mon YYYY -- Mon YYYY)

---

## Role-Type Decision Tree

| If JD mentions... | Primary profile | Secondary (hybrid) |
|-------------------|----------------|-------------------|
| _[your domain keywords]_ | _[your role type]_ | _[secondary or --]_ |
| _Example: national lab, DOE, postdoc_ | _National Lab_ | _--_ |
| _Example: machine learning, neural networks_ | _ML/AI_ | _National Lab_ |
| _Example: protein modeling, structural biology_ | _Computational Biology_ | _--_ |

**Hybrid resumes:** When a JD spans two role types, merge the two profiles. Primary sets priority matrix; secondary contributes supplementary bullets and keywords.

Customize the decision tree above with your own role types, tools, and domains in `CLAUDE.md`.

---

## Gap Assessment & Bridge Mappings

For each identified gap, assess:
- **Gap description:** What the JD asks for
- **Bridge framing (if available):** Use "methodology transferable to X" or "equivalent experience with Y" -- NEVER "experienced with X" unless directly demonstrated
- **Bridge confidence:** HIGH / MEDIUM / LOW
- **User decision:** Omit or bridge? (User decides per gap)

**Example bridge mappings** (customize for your own tools/methods):
- Tool A → "Custom solvers (Tool B/Tool C; computational methodology transferable to Tool A)" [HIGH]
- Framework A → "Deep learning framework expertise (Framework B; directly transferable to Framework A)" [HIGH]
- Simulation Package A → "Molecular dynamics expertise (Package B; transferable to Package A)" [HIGH]
- Language A → "Scientific computing (Language B, Language C; transferable to Language A)" [MEDIUM]

---

## Content Density Rules

| Format | Work Experience | Skills/Work Samples/Cross-Functional | Publications | Awards |
|--------|-----------------|---------------------------------------|-------------|--------|
| 2-page resume | 6-9 positions, paragraph tiers (P-Short/Medium/Long) | 5-7 flat bullets each | 5 | none (section removed) |
| 5-page CV | Comprehensive, 19-21 bullets (2L/3L) | Format C, 17 lines | All published + under review | All |
| Full CV | Everything | Format C | All published + under review | All |

---

## Files to Upload (by format)

**For resumes (2-page):** [Resume — docx]
1. `bundle_[role_type].md` — Role-specific generation content (Sections 1-5, plus Work Samples/Cross-Functional Leadership source material)
2. `achievement_reframing_guide.md` — Role-type framing directives for all achievements (paragraph writing for resume, bullets for CV)
3. `skills_taxonomy.md` — Full skills inventory for flat-bullet Technical Skills generation
4. `pub_metadata.md` — Publication database with scoring tags
5. `resume_builder/helpers/docx_builder.py` — Renderer (content YAML → .docx), never edited per generation
6. `resume_builder/templates/resume_content_template.yaml` — Structural template (contains FIXED fields)
7. Experience files from `resume_builder/experience/`

**For CVs (5-page or full):** [CV — LaTeX, unchanged]
1. `bundle_[role_type].md` — Role-specific generation content (Sections 1-5)
2. `achievement_reframing_guide.md` — Role-type framing directives for all achievements
3. `skills_taxonomy.md` — Full skills inventory for Technical Expertise generation
4. `pub_metadata.md` — Publication database with scoring tags
5. `cv.cls` — Document class file
6. `cv_template.tex` — Structural template (contains FIXED sections)
7. Experience files from `resume_builder/experience/`

**Role type to bundle mapping:**
Bundles live in `resume_builder/bundles/`. Map each JD role type to its corresponding bundle file (e.g., `bundle_[role_type].md`).
