# Documentation

Detailed reference for claude-resume-kit. For the quick overview, see [README.md](README.md).

---

## Architecture

```
claude-resume-kit/
├── CLAUDE.md                          # Auto-loaded project instructions
├── config.md                          # Your personal configuration
├── .claude/skills/                    # 6 skills (invoked as /skill-name)
│   ├── setup-extract/SKILL.md         # Extract from papers → structured data
│   ├── setup-build-kb/SKILL.md        # Synthesize KB from extractions
│   ├── make-resume/SKILL.md           # JD → tailored resume (.docx) or CV (.tex)
│   ├── make-cl/SKILL.md              # Session → cover letter (.docx)
│   ├── edit-resume/SKILL.md           # Edit from critique/feedback
│   └── critique/SKILL.md             # Independent quality review
├── resume_builder/
│   ├── reference/                     # Generation rules and protocols
│   │   ├── shared_ops.md              # Session workflow (all skills read this)
│   │   ├── resume_reference.md        # Resume (docx/word-count) + CV (LaTeX/char-count) rules
│   │   ├── cl_reference.md            # Cover letter rules
│   │   ├── critical_rules.md          # Compact re-read for generation phase
│   │   ├── session_file_template.md   # Session file format spec
│   │   └── critique_framework.md      # 8-part critique system
│   ├── templates/
│   │   ├── resume_content_template.yaml    # Resume structural template (docx pipeline)
│   │   ├── cover_letter_content_template.yaml  # Cover letter structural template (docx pipeline)
│   │   ├── cv.cls                     # CV LaTeX class (academic format only)
│   │   └── cv_template.tex            # CV structural template (LaTeX)
│   ├── helpers/
│   │   ├── docx_builder.py            # Renders resume/CL content YAML → .docx
│   │   ├── content_check.py           # Word-count budget validator (resume/CL)
│   │   └── char_count.py              # Character-count budget validator (CV only)
│   ├── examples/                      # Fictional "Dr. Jordan Chen" — full worked example
│   ├── experience/                    # YOUR experience files (built by /setup-build-kb)
│   ├── bundles/                       # YOUR role-type bundles (built by /setup-build-kb)
│   └── support/                       # Skills taxonomy, pub metadata, AI fingerprint rules
├── knowledge_base/
│   ├── extractions/                   # Paper extractions (built by /setup-extract)
│   ├── papers/                        # Drop your PDFs / .tex source here
│   └── notes/                         # Any other reference material
├── JDs/                               # Job descriptions (text files)
└── output/                            # Generated content YAMLs/.docx (resume/CL), .tex (CV), session files, critiques
```

---

## Concepts

### Session Files

Every JD gets a session file (`output/<Folder>/session_<name>.md`) that tracks:
- JD analysis and ATS keywords
- Which bundle was selected
- Content plan (which achievements, in what order, at what paragraph tier/bullet length)
- All generation decisions and their rationale
- Cover letter plan
- Critique scores

All 4 generation skills read and update this file. It's the single source of truth for each application.

### Experience Files

One file per position (e.g., `experience_postdoc_university.md`). Each achievement has:
- **Source paper** with citation
- **Methods and tools** used
- **Quantitative results**
- **Pre-written bullet variants** (2-line and 3-line)
- **Tags** for which role types this achievement is relevant to
- **Significance** context for cover letters

### Role-Type Bundles

One file per target audience (e.g., `bundle_academic.md`). Each bundle contains:
- **S1: Role Profile** — what this audience values, positioning strategy
- **S2: Summary Guide** — how to write the summary for this role type
- **S3: Achievement Reframing Map** — priority ranking of your achievements for this audience
- **S4: Skills Guide** — which tools to bold, which to include, grouping strategy
- **S5: Cover Letter Guide** — opening hooks, paragraph templates, anti-patterns

### Provenance Flags

The system enforces accuracy through provenance tracking in `config.md`. Every achievement is tagged with its publication status. The skills check this table before every output and will never:
- Claim unpublished work is published
- Claim internal tools are peer-reviewed
- Use full-ownership verbs for shared work
- Inflate author position

### The Critique System

The `/critique` skill runs a multi-part assessment:
1. **Domain-Specialist Lens** — reviewer persona, gap analysis, competitive landscape
2. **Five-Perspective Read-Through** — ATS bot, recruiter (10s), HR (30s), hiring manager (2min), technical reviewer (10min)
3. **Eight-Dimension Scoring** — weighted score out of 100
4. **Interview Likelihood** — per-reader probability estimates
5. **Tiered Improvements** — ranked by point impact
6. **Interview Bridge Points** — resume-to-interview talking points
7. **Cover Letter Critique** — 6 sub-checks (anti-patterns, tailoring, context-specific, ATS keywords, structural, package cohesion)
8. **Post-Generation Verification** — mechanical and content checklists including AI fingerprint scan

---

## Three-Session Workflow

For best results, use a **separate Claude Code session** for each step. This gives each skill fresh context, which produces better quality (especially for critique — you want fresh eyes, not the same context that generated the resume).

```
Session 1:  /make-resume JDs/job.txt     → resume .docx (or CV .tex)
            /clear
Session 2:  /make-cl                      → cover letter .docx
            /clear
Session 3:  /critique                     → critique .md with score
            /clear
            /edit-resume                  → refined .docx/.tex (if needed)
```

---

## Customization

### Everything in `config.md` (edit directly)

| Setting | What it controls | Example |
|---------|-----------------|---------|
| **Personal Info** | Name, email, phone, links on all outputs | Your contact details |
| **Document Preferences** | Page counts, paragraph/bullet variants, skills layout | `Resume: 2 pages, CV: 5 pages` |
| **Provenance Flags** | What claims are safe to make | `ML paper: under review → never say "published"` |
| **Role Types** | Target audiences and their bundles | `Academic (Tier 1), Industry R&D (Tier 2)` |
| **Decision Tree** | How JD keywords map to role types | `"tenure-track" → Academic` |
| **FIXED Sections** | Template sections that never change per JD | `Education, Publications, Awards` |
| **Output Rules** | Package formats and constraints | `Resume: 2pg + 1pg CL = 3pg package` |
| **KB Corrections** | Errors to never re-introduce | `Spearman is 0.82, not 0.85` |

### Resume/Cover Letter Templates (docx pipeline — edit directly)

- **Fonts, colors, margins, heading style** — modify the `STYLE` dict at the top of `resume_builder/helpers/docx_builder.py` (one change affects every future resume/CL)
- **Section order** — code-locked in `docx_builder.py`'s `build_resume()`/`build_cover_letter()`; reorder there if you want a different structure
- **FIXED content** — fill in education, publications, header contact fields in `resume_content_template.yaml`
- **Word-count budgets** — adjust the tier ranges in `resume_reference.md`/`critical_rules.md` and the matching tiers in `content_check.py`

### CV Templates (LaTeX, academic format only — edit directly)

- **Fonts, colors, spacing** — modify `cv.cls`
- **Section order** — reorder sections in `cv_template.tex`
- **FIXED content** — fill in education, awards, publications, header
- **Icons** — replace `GS.png` / `orcid.png` with your own
- **Page geometry** — adjust margins in `cv.cls` if needed

### Knowledge Base (built by skills, then editable)

| File | How to customize |
|------|-----------------|
| **Experience files** | Edit bullet text, add/remove achievements, adjust tags |
| **Bundles** | Change priority matrices, rewrite summary guides, add role types |
| **Skills taxonomy** | Add/remove skills, change groupings, adjust bold rules |
| **Pub metadata** | Update citation counts, add new publications |

### Reference Docs (advanced)

| File | What you'd change |
|------|-------------------|
| `resume_reference.md` | Page budgets, character limits, section specs |
| `cl_reference.md` | Cover letter paragraph templates, word count targets |
| `critical_rules.md` | Generation-time rules tables |
| `critique_framework.md` | Scoring weights, critique dimensions |
| `shared_ops.md` | Session workflow, file derivation logic |

### Skill Prompts (advanced)

Each skill is a markdown file in `.claude/skills/<name>/SKILL.md`. You can:
- Add STOP points for more user control
- Change the number of web searches in Phase 0
- Adjust how many bullets per position
- Modify the critique scoring weights
- Add new skills for your workflow

---

## Key Design Decisions

- **Accuracy > Relevance > Impact > ATS > Brevity** — the priority hierarchy for every generation decision
- **Local, no-cloud output** — resume/CL render straight to `.docx` via `python-docx`; the CV format still compiles LaTeX locally. No formatting service, no data leaves your machine beyond the Claude Code conversation.
- **FLIPPED position format** — the bold line under each position title is a JD-customized theme, not a generic description. This is the strongest tailoring lever.
- **Structured provenance** — every achievement is tracked from source paper through extraction to experience file to resume content
- **Calibrated budgets, not exact guarantees** — resume/CL content targets word-count tiers (Word reflows, so there's no exact per-line promise); the CV format still uses character-precise budgets calibrated to its fixed LaTeX geometry
- **Session files as state** — all decisions for a JD live in one file. Skills can recover from interruptions.
- **Anti-fabrication by design** — provenance flags, verb discipline, and corrections logs prevent overclaiming even under pressure to impress
- **AI fingerprint avoidance** — a dedicated rules file is loaded by all generation and critique skills, covering banned words and phrases (with technical exceptions), structural anti-patterns, positive markers, and a 12-item post-generation checklist

---

## FAQ

**Q: Do I need to know LaTeX?**
No, not for the resume or cover letter — Claude renders those straight to `.docx` and you open them in Word. Only the optional 5-page academic CV format uses LaTeX; if you use it, Claude generates the `.tex` and you compile it (`pdflatex file.tex`).

**Q: Why doesn't the resume auto-export a PDF?**
The `.docx` pipeline intentionally has no automated page-count/layout verification (Word reflows text, unlike LaTeX) and no PDF-export automation, to keep the toolchain to just `python-docx`/`pyyaml` — no LibreOffice or MS Word automation dependency. Open the `.docx`, confirm it looks right, and export to PDF yourself when you're ready to submit.

**Q: How many papers should I extract?**
All papers where you're first author or co-first author, plus key contributing-author papers. Quality matters more than quantity — 5 well-extracted papers beat 20 shallow ones.

**Q: Can I use this for non-academic roles?**
Yes. The framework supports any role type — define them in `config.md`. Industry R&D, consulting, data science, and engineering roles all work. Just create appropriate bundles.

**Q: What if I don't have a Google Scholar / ORCID?**
Remove those fields from `resume_content_template.yaml` (or `cv_template.tex` for the CV format). The framework adapts to what you have.

**Q: How do I update after publishing new papers?**
Run `/setup-extract` on the new paper, then update your experience file and bundles. Existing session files are not affected.

**Q: Can I use this with resume formats other than the included templates?**
Yes. For the resume/CL, the `STYLE` dict and section functions in `docx_builder.py` define the visual style and structure — modify them (or add new ones) to change the look or section list. For the CV, the `.cls` files define the visual style; modify them or write your own. Either way, update the `[GENERATE: ...]` and `[FIXED: ...]` markers in your content template to match.

**Q: Can multiple people use the same kit?**
Each person needs their own clone with their own `config.md`, knowledge base, and templates. The framework itself is shared; the content is personal.

**Q: What Claude model should I use?**
The skills are designed for Claude's most capable models (Opus, Sonnet). Less capable models may skip steps or produce lower-quality output.
