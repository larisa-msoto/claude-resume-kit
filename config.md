# Configuration

> Edit this file with your personal details. Every skill reads this file.

---

## Personal Info

- **Name:** Larisa M. Soto
- **Degree suffix:** [e.g., Ph.D., M.S., or leave blank]
- **Email:** [your@email.com]
- **Phone:** +1 437 505 8222
- **Location:** Toronto, Canada
- **LinkedIn:** https://www.linkedin.com/in/larisa-msoto/
- **Google Scholar:** 
- **ORCID:** 
- **Website:** https://github.com/larisa-msoto
- **Languages:** Spanish, English, French

---

## Document Preferences

- **Resume pages:** 2
- **CV pages:** 2
- **Resume Work Experience variant:** paragraph tiers (P-Short/Medium/Long) — see resume_reference.md
- **CV bullet variant:** 2L/3L mix
- **Skills config (resume):** 4-3-2-2-2 (13 lines, 5 groups)
- **Skills config (CV):** 4-4-3-3-3 (17 lines, 5 groups)
- **Immigration line:** Yes | "Authorized to work in Mexico, Canada, and Europe"

---

## Provenance Flags

Track the publication status of your work. Skills check this table before every output.

| Item | Status | Correct Framing |
|------|--------|----------------|
| _Example: My Nature paper_ | _under review_ | _"under review at Nature" — never say "published in Nature"_ |
| _Example: Internal tool_ | _unpublished_ | _"infrastructure I developed" — never imply peer-reviewed_ |

Add your own rows. Delete the examples.

---

## KB Corrections Log

Verified errors to never re-introduce. Add entries as you catch mistakes.

| Correction | Details |
|-----------|---------|
| _Example: Tool X name_ | _It's "ToolX-v2" not "ToolX". Always use the correct name._ |

---

## Role Types

Define the role types you're targeting. Each gets a bundle during setup.

| Role Name | Target Employers | Tier | Bundle File |
|-----------|-----------------|------|-------------|
| Bioinformatician | Academic institutions, Big Pharma R&D | 1 | bundle_bioinformatician.md |
| Clinical Data Scientist | Health systems, pharma clinical data teams | 1 | bundle_clinical_data_scientist.md |
| Computational Biologist | Academic + industry computational biology | 1 | bundle_computational_biologist.md |
| AI Solutions & Enablement Specialist | AI/ML tooling, enablement, and training teams | 2 | bundle_ai_solutions_specialist.md |
| AI Scientist | AI/ML research teams | 2 | bundle_ai_scientist.md |

_Tiers/employers above are a best-effort read from your 5 existing resume variants — refine after review._

**Tier guide:** 1 = strongest evidence, full portfolio | 2 = strong with targeted emphasis | 3 = viable with careful framing

---

## Role-Type Decision Tree

Customize this to map JD keywords to your role types.

| If JD mentions... | Primary profile | Secondary (hybrid) |
|-------------------|----------------|-------------------|
| _[your domain keywords]_ | _[role type]_ | _[secondary or --]_ |

---

## FIXED Sections

List template sections that should NEVER be modified during generation.
These are copied verbatim from your template every time.

- Education
- Publications (CV)
- Header block (name, contact, links, immigration line for resume)
- _[Add any other fixed sections]_

> Note: the 2-page **resume** format no longer includes an Honors & Awards section (dropped to match real-world convention). This does not apply to the CV format.

---

## Output Rules

- **Email in all outputs:** [same as Personal Info email]
- **Resume package:** 2 pages (.docx, via `docx_builder.py`) + 1-page cover letter (.docx)
- **CV package:** [N] pages (.tex, user compiles locally) + 1-2 page cover letter (.docx)
- **Resume/CL output:** `.docx` only — no auto PDF export. Open in Word, confirm page fit, export to PDF yourself when submitting.
- **CV output:** `.tex` — user compiles locally with a LaTeX distribution.
- **Prerequisite for resume/CL:** `pip install python-docx pyyaml`. LaTeX distribution only needed if you use the CV format.
