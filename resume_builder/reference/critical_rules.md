# Critical Rules — Compact Re-Read

> Quick reference for Phase 2 generation. Full rules in `resume_reference.md`.
> Resume = docx/word-count pipeline. CV = LaTeX/char-count pipeline (unchanged). Sections below are marked accordingly.

## Word Limits — Resume [docx]

**Work Experience paragraph tiers (word count, no bullets):**

| Tier | Sentences | Word Range | HARD MAX |
|------|-----------|------------|----------|
| P-Short | 1 | 19-28 | 32 |
| P-Medium | 2 | 35-48 | 54 |
| P-Long | 3-4 | 53-61 | 68 |

**Flat bullets (Technical Skills / Work Samples / Cross-Functional Leadership):** 25-38 words each, HARD MAX 44.

No orphan rule, no bold-width penalty math — Word reflows text, so there's no exact per-line guarantee. Verify with:
```bash
python3 resume_builder/helpers/content_check.py resume <content.yaml>
```

## Character Limits — CV [LaTeX, unchanged]

**CV (11pt, textwidth=7.5in):**

| Target Lines | Rendered Char Range | HARD MAX | Orphan Threshold |
|-------|---------------|---------|------------------|
| 1 line | 88-93 chars | 101 | -- |
| 2 lines | 168-182 chars | 190 | Last line >= 65 chars |
| 3 lines | 250-268 chars | 280 | Last line >= 65 chars |

CV Bold Width Penalty: Effective limit = 91 - (0.25 x bold_char_count)

CV Orphan Rule: multi-line bullet's last rendered line must fill >= 70% of line width. 2L: >= 65 chars. 3L: >= 65 chars.

Verify with: `python3 resume_builder/helpers/char_count.py -f cv <file.tex>`

## Variant Naming (combined)

| Variant | Document | Budget Unit | Target Range | HARD MAX |
|---------|----------|-------------|---------------|----------|
| Resume P-Short | 2-page resume (Work Experience) | words | 19-28 | 32 |
| Resume P-Medium | 2-page resume (Work Experience) | words | 35-48 | 54 |
| Resume P-Long | 2-page resume (Work Experience) | words | 53-61 | 68 |
| Resume flat bullet | 2-page resume (Skills/Work Samples/Cross-Functional) | words | 25-38 | 44 |
| CV-2L | 5-page CV | rendered chars | 168-182 | 190 |
| CV-3L | 5-page CV | rendered chars | 250-268 | 280 |

## FIXED Sections — NEVER Modify

**Resume:** header contact fields (name/location/phone/email/LinkedIn/GitHub/languages/immigration line), education, publications author/journal text, any FIXED position paragraph. **No Honors & Awards section.** `docx_builder.py`'s STYLE dict and section order are code-locked — never touched per generation.
**CV:** internships, education, publications, honors/awards, header block — all set in the template. NEVER change: `\vspace` values, `\geometry` settings, `.cls` formatting, header layout.

Resume VARIABLE fields: `summary`, `tagline`, Technical Skills/Work Samples/Cross-Functional Leadership text, Work Experience `theme`/`paragraph`.
CV VARIABLE sections: Summary, Technical Expertise, Research Experience bullets/headers.

## Provenance Flags

See `CLAUDE.md` for your project-specific provenance flags. Common patterns:

| Item Status | Rule |
|-------------|------|
| Under review | State journal name: "under review at [Journal]" |
| Unpublished | No specific numbers or publication claims |
| Internal/proprietary | "infrastructure I developed" — not peer-reviewed |
| Preprint only | Always flag provenance |

## Inline Markup

**Resume/CL (docx):** `**bold**` and `[link text](url)` — parsed by `docx_builder.py` into real bold runs / hyperlinks. No LaTeX notation needed or used.

**CV (LaTeX) — Notation Quick-Ref:**

| Item | Correct LaTeX | Wrong | Rendered |
|------|--------------|-------|----------|
| Chemical formulas | `\ce{H2O}` | `H2O`, `H$_2$O` | H₂O |
| Superscript labels | `X$^2$Y` | `X2Y` | X²Y |
| R² values | `R$^2$=0.99` | `R^2`, `R2` | R² |
| Greek letters | `$\alpha$-phase` | `alpha-phase` | α-phase |
| Approximately | `$\sim$64` | `~64` (LaTeX non-breaking space!) | ~64 |

CRITICAL (CV only): ~ in LaTeX = non-breaking space. Use $\sim$ for "approximately."

## KB Corrections

See `CLAUDE.md` for your project-specific KB corrections log. Always check before generation to avoid re-introducing known errors.

## Budget Reminder

**Resume:** 6-9 Work Experience positions as paragraphs (P-Short/Medium/Long mix), plus 5-7 flat bullets each in Technical Skills/Work Samples/Cross-Functional Leadership. Target ~500-600 total body words for 2 pages (calibrate — see resume_reference.md Page Fill Budgets). No exact page-fit guarantee — open the `.docx` to confirm before submitting.

**CV:** 19-21 bullets, 45 rendered lines. CV bullets: 2L/3L mix OK. **CV Page 1 rule:** First bullet of first experience MUST be 2L. A 3L first bullet overflows page 1.
