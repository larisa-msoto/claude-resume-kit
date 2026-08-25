#!/usr/bin/env python3
"""
Validate word counts in a resume/cover-letter content YAML against the
paragraph/bullet tier budgets in resume_reference.md and cl_reference.md.

This is the docx-pipeline equivalent of char_count.py (which stays in use
for the CV/LaTeX path). Word counts, not rendered characters, because Word
reflows text -- exact line-fitting isn't knowable without opening the file.

Usage:
  python3 content_check.py resume resume_content.yaml
  python3 content_check.py cover_letter cl_content.yaml --institution industry
"""

import argparse
import re
import sys

import yaml


# WORDS_PER_PAGE is a starting estimate for a 2-page resume at 10.5pt Calibri,
# 0.6in margins (see docx_builder.py STYLE). Calibrate against a real compiled
# doc (see resume_reference.md Verification) and adjust this constant.
WORDS_PER_PAGE = 600

RESUME_TIERS = [
    ('P-Short', 19, 28, 32),
    ('P-Medium', 35, 48, 54),
    ('P-Long', 53, 61, 68),
]
FLAT_BULLET_TIER = ('Flat', 25, 38, 44)

CL_WORD_TARGETS = {
    'industry': (250, 300),
    'national_lab': (350, 450),
    'academic_postdoc': (350, 450),
    'academic_faculty': (450, 650),
}


def strip_markdown(text):
    """Strip **bold** and [text](url) markup to get rendered word content."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1', text)
    return text


def word_count(text):
    return len(strip_markdown(text).split())


def classify(n, tiers):
    for variant, lo, hi, hard_max in tiers:
        if n <= hard_max:
            if n < lo:
                status = 'SHORT'
            elif n <= hi:
                status = 'OK'
            else:
                status = 'NEAR MAX'
            return variant, status, lo, hi, hard_max
    return 'OVER', 'OVER LIMIT', 0, 0, 0


def check_resume(content):
    total_words = 0
    print('Work Experience paragraphs:\n')
    for i, pos in enumerate(content['work_experience'], 1):
        n = word_count(pos['paragraph'])
        total_words += n
        variant, status, lo, hi, hard_max = classify(n, RESUME_TIERS)
        print(f"  Position {i} ({pos.get('theme', '')[:40]}): {n:3d} words | {variant} | {status} "
              f"(target {lo}-{hi}, max {hard_max})")

    def check_flat_section(title, items):
        nonlocal total_words
        print(f'\n{title}:\n')
        for i, (label, text) in enumerate(items, 1):
            combined = f'{label}: {text}' if label else text
            n = word_count(combined)
            total_words += n
            variant, status, lo, hi, hard_max = classify(n, [FLAT_BULLET_TIER])
            print(f"  Bullet {i}: {n:3d} words | {status} (target {lo}-{hi}, max {hard_max})")

    check_flat_section('Technical Skills', [(s['label'], s['text']) for s in content['technical_skills']])
    check_flat_section('Cross-Functional Leadership', [(c['label'], c['text']) for c in content['cross_functional_leadership']])

    ws_items = []
    for group in content['work_samples']:
        item_text = ', '.join(i['text'] for i in group['items'])
        ws_items.append((group['category'], item_text))
    check_flat_section('Work Samples', ws_items)

    summary_words = word_count(content['summary'])
    total_words += summary_words
    print(f'\nSummary: {summary_words} words')

    pub_words = sum(word_count(p) for p in content['publications']['items'][:5])
    total_words += pub_words
    n_pubs = len(content['publications']['items'])
    print(f"Publications: {min(n_pubs, 5)} entries (capped at 5), {pub_words} words"
          + (f'  [WARNING: {n_pubs} provided, only first 5 used]' if n_pubs > 5 else ''))

    est_pages = total_words / WORDS_PER_PAGE
    print(f'\nTotal body words: {total_words}')
    print(f'Estimated pages: {est_pages:.2f} (at {WORDS_PER_PAGE} words/page -- calibrate this constant, see resume_reference.md)')


def check_cover_letter(content, institution):
    total_words = sum(word_count(p) for p in content['body_paragraphs'])
    print(f'Body paragraphs: {len(content["body_paragraphs"])}')
    print(f'Total words: {total_words}')
    if institution and institution in CL_WORD_TARGETS:
        lo, hi = CL_WORD_TARGETS[institution]
        status = 'SHORT' if total_words < lo else ('OK' if total_words <= hi else 'OVER')
        print(f'Target ({institution}): {lo}-{hi} words -- {status}')
    else:
        print('No --institution given (or unrecognized) -- pass industry/national_lab/academic_postdoc/academic_faculty to check against a target range.')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('doc_type', choices=['resume', 'cover_letter'])
    parser.add_argument('content_path')
    parser.add_argument('--institution', choices=list(CL_WORD_TARGETS.keys()), default=None)
    args = parser.parse_args()

    with open(args.content_path) as f:
        content = yaml.safe_load(f)

    if args.doc_type == 'resume':
        check_resume(content)
    else:
        check_cover_letter(content, args.institution)


if __name__ == '__main__':
    main()
