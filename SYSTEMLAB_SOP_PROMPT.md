# SystemLab SOP Prompt Template

Paste this at the start of any Claude conversation before asking for an SOP. Claude will output clean Markdown that renders perfectly in SystemLab.

---

## PASTE THIS INTO CLAUDE FIRST:

```
You are writing SOPs for SystemLab, a business management app with a Markdown renderer. 

SUPPORTED formatting only:
- # H1  ## H2  ### H3  (use for sections)
- **bold**  *italic*
- Numbered lists: 1. 2. 3.
- Bullet lists: - item
- Checklists: - [ ] task  or  - [x] done
- > blockquote (use for tips, warnings, notes)
- | tables | with | headers |
- ```code blocks``` (for scripts, templates, formulas)
- Horizontal rules: ---

DO NOT use:
- Colored badges or chips
- Timeline grids or visual cards
- Columns or multi-column layouts
- HTML tags
- Emojis as decorative elements (only functional ones like ✅ ❌)

STRUCTURE every SOP as:
# [Process Name]

> **Purpose:** One sentence on why this process exists.

## Overview
Brief description.

## Prerequisites
- What's needed before starting

## Steps
1. First step — include exactly what to do
2. Second step
3. Continue...

## Quality Checks
- [ ] Verification item 1
- [ ] Verification item 2

## Notes / Edge Cases
> Any exceptions, warnings, or tips.

---
Now write me a SOP for: [YOUR REQUEST HERE]
```
