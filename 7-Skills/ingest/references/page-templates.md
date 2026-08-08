# Page templates

Loaded at step 4 of the ingest. These are the shapes to paste.

What the fields mean, what makes a page a concept or an entity, and the naming and subfolder rules are in `8-System/brain.md` under Conventions. Read that once per session; this file is only the skeletons.

---

## Concept page

The reasoning lives here, and the page is as long as the argument needs.

```markdown
---
title: [Readable Title]
type: concept
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
source_count: [n]
status: draft
sources:
  - source-file-1.md
  - source-file-2.md
---

# [Readable Title]

[Compiled content. Synthesis, not copy-paste - if a paragraph could be pasted
back into the source unchanged, it has not been compiled.]

[Every claim cites its source: [source: file-name.md]]

## Related
- [[Another Wiki Page]] - how it connects
```

---

## Entity page

A hub, not an essay. It says who this is and what they argue, then points at the concept pages where the reasoning sits.

```markdown
---
title: [Entity Name]
type: entity
entity_kind: person | company | tool | product
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
source_count: [n]
status: draft
sources:
  - source-file.md
---

# [Entity Name]

[One paragraph. What this is and why it earns a page here.]

## What they argue / What it does
- [One line per claim or capability, each cited. A claim that needs a paragraph
  belongs on a concept page.]

## Where it shows up
- [[Concept Page]] - what this entity contributed there

## Track record
[Only if you have it: what happened, numbers, outcomes. Delete the section if empty.]

## Open questions
```

---

## While writing

Set `status: needs_update` when this source contradicts what the page already says and you flagged a `> CONTRADICTION:`.

Bump `last_updated` and `source_count` on every page you touch, including the ones you only added a line to. A page that gets edited without its `last_updated` moving is invisible to the `lint` skill.
