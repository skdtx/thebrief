---
name: thebrief
description: Write, edit, or audit Russian financial, banking, product, and business copy in a clear information style while preserving its meaning and commercial intent. Use for Telegram posts, client or partner presentation copy, one-pagers, product explainers, and requests to make complex finance understandable. Do not use for standalone fact-checking, legal review, investment advice, or basic spelling correction.
---

# TheBrief

Produce clear Russian copy without silently changing what the author means or wants the reader to do.

## Choose the operation

- **Write:** create copy from a brief. Infer obvious context; ask only when a missing answer would materially change audience, purpose, claim, or deliverable.
- **Edit:** improve supplied copy. Return the finished version first, then material changes and unresolved issues.
- **Audit:** assess fit against this skill without rewriting the whole text unless asked.

## Establish the brief

Before drafting, identify from the request and supplied material:

- deliverable and audience;
- reader's starting knowledge and task;
- desired change in understanding or action;
- main claim and supporting facts;
- applicable constraints, risks, and degree of commercial intent.

Ask a compact question only for a consequential gap. Otherwise proceed and mark local gaps in the draft.

## Protect the meaning

For editing, form a private **meaning contract**: subject, audience, purpose, desired reader action, key claims, confidence level, and material caveats. Preserve that contract through the edit.

Structural changes are allowed when they sharpen the same contract. If a useful change would alter a claim, promise, conclusion, position, audience, desired action, risk disclosure, or confidence level, put it under `Требует решения автора` instead of silently applying it.

Read [references/semantic-preservation.md](references/semantic-preservation.md) for editing, risky rewrites, or conflicting source text.

## Apply the method

Read [references/methodology.md](references/methodology.md) whenever writing, editing, or auditing. For finance explainers and longer educational copy, also read [references/article-patterns.md](references/article-patterns.md).

Core standard:

- lead with reader value or the conclusion;
- make one logical step at a time;
- explain a term at first meaningful use;
- support abstractions with mechanisms, examples, comparisons, or evidence;
- connect facts and numbers to what they mean for the reader;
- state uncertainty and limitations at the point where they matter;
- shorten language without thinning the substance;
- leave the Russian natural, calm, and specific.

The job is editorial, not factual verification. Preserve sourced facts. Mark missing evidence as `[Нужен факт: ...]`. Offer a useful type of fact or a clearly labeled `[Гипотеза для проверки: ...]`; never present the suggestion as established.

## Load the format

Read only the reference for the requested format:

- Telegram: [references/formats/telegram.md](references/formats/telegram.md)
- end-client presentation: [references/formats/client-presentation.md](references/formats/client-presentation.md)
- partner presentation: [references/formats/partner-presentation.md](references/formats/partner-presentation.md)
- one-pager: [references/formats/one-pager.md](references/formats/one-pager.md)

When no format matches, use the general method and the user's requested form. Telegram rules never spill into other formats by default.

## Return the result

For **Write**, give the ready text first. Then include `Нужно проверить` and `Требует решения автора` only when non-empty.

For **Edit**, default to:

1. `Готовый текст`
2. `Что и почему изменено` — only material editorial decisions
3. `Нужно проверить` — missing or doubtful facts and logical gaps
4. `Требует решения автора` — proposed meaning changes

For **Audit**, give a verdict, the highest-impact mismatches, and precise recommended changes. Separate method violations from missing evidence and author decisions.

Honor a request for clean copy only, but still surface critical factual, compliance, confidentiality, or meaning risks.

## Handle confidential material

Treat working copy as confidential unless the user says otherwise. Keep it within the current task and authorized tools; use anonymized or synthetic examples in reusable materials. A future public release does not make its draft public. Never place secrets, personal or client data, unpublished product terms, or internal approvals into examples or repository files.
