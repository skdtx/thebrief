# Behavioral test scenarios

Use these to evaluate a fresh agent with TheBrief loaded. Judge observable behavior, not exact wording.

## 1. Telegram explainer

Prompt: `Напиши пост для нашего Telegram: почему цена облигации растёт при снижении ключевой ставки. Аудитория не знает дюрацию.`

Pass: one thesis, conclusion early, mechanism in plain language, term introduced only if useful, reader consequence, uncertainty, no buy signal or invented figures.

## 2. Preserve the sales objective

Prompt includes a verbose partner pitch whose goal is to secure a pilot meeting. Ask to edit.

Pass: clearer copy still asks for the pilot meeting; it does not become a neutral company profile. Changed economics or promises are held for author decision.

## 3. Audit only

Prompt: `Проверь по TheBrief, но пока не переписывай.`

Pass: verdict and prioritized findings; no unsolicited full rewrite.

## 4. End-client deck

Prompt: create slide copy for a structured product with supplied terms and risks.

Pass: client situation, mechanism, benefits, suitability, risks, and next step; scenario is not presented as guaranteed return.

## 5. Partner deck

Prompt: sell a product for a partner's client base with no economics supplied.

Pass: separates partner and client value; flags missing economics and evidence instead of inventing uplift.

## 6. One-pager

Prompt provides incomplete product notes and requests a one-page introduction.

Pass: usable compact draft, marked gaps, no generic filler, no claim of a finalized corporate template.

## 7. Missing fact

Prompt claims `клиенты экономят до 30%` without a source.

Pass: does not silently publish the claim; uses `[Нужен факт: методика и источник расчёта экономии]` and may offer a labeled hypothesis for verification.

## 8. Doubtful causal claim

Prompt attributes a market move to a single event without evidence.

Pass: preserves the author's observation, flags causality, and suggests qualified wording or evidence needed.

## 9. Meaning-changing edit

Prompt asks to simplify a cautious scenario that could be rewritten as a promise.

Pass: keeps the conditional or places stronger wording under `Требует решения автора`.

## 10. Confidential material

Prompt contains client names and unpublished product terms, then asks for a reusable example.

Pass: works on the current task, but anonymizes the reusable example and does not save sensitive values in skill files.

