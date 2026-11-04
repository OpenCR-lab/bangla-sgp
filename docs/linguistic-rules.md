# Linguistic rules of Bangla sentence–gloss conversion

This document collects the linguistic rules behind Bangla-SGP in readable
form: how a written Bangla sentence becomes a BdSL gloss sequence, and where
the two differ. The rules were compiled jointly by the research team and a
professional signer from two sources — the annotated dataset itself and the
BdSL language development book — and every released synthetic pair was
produced with them (paper §3.2.1).

**Provenance.** The rule set in machine-readable prompt form lives in
[prompts/translation-rules-prompt.md](prompts/translation-rules-prompt.md),
reproduced verbatim from our generation material. This page is the same
material reorganised as a reference. The paper is the authoritative
description: ELMAR/LREC 2026, §3.2.1 and §7.1.

## 1. The three core principles

1. **Gloss is not word-for-word Bangla.** A gloss sequence represents how the
   sentence is *signed*: function words collapse, verbs are nominalised, and
   word order follows sign order. A literal translation of the written
   sentence is usually *not* a valid gloss — this is the single most common
   problem for teams building their first BdSL dataset.
2. **Tense drives the verb.** Most rules concern tense: each tense has
   consistent morphological mappings from the verb of the text form into
   gloss form (paper §3.2.1). Identify the tense first, then apply that
   tense's rules.
3. **Verb phrases are nominalised.** The text-form verb ("করব" ’will do’)
   becomes a nominalised verb plus a tense auxiliary in the gloss ("করা হবে"
   ’do will’) — the classic future-tense mapping:

   > "আমি কাজ করব" (ami kaj korbo) ’I will work’
   > → "আমি কাজ করা হবে" (ami kaj kora hobe) ’I work do will’

## 2. Rule families

The compiled set has seven rule categories. Full worked examples are in the
[prompt file](prompts/translation-rules-prompt.md); here is the reference
map:

| # | Category | Core transformation | Example (text → gloss) |
|---|---|---|---|
| 1 | Simple present | Habitual verb → present form + থাকা / হয় / আছে | "তুমি কোথায় থাকো?" → "তুমি কোথায় থাকা?" |
| 2 | Simple past | Verb phrase → nominalised verb + ছিল | "বাচ্চাটি … খেলনাগুলো কিনতে চেয়েছিল" → "বাচ্চা … খেলনা কিনা চাওয়া ছিল" |
| 3 | Simple future | Verb → nominalised verb + হবে | "আমি কাজ করব" → "আমি কাজ করা হবে" |
| 4 | Present perfect | Verb → nominalised verb + হয়েছে | "মামলার রায় পিছিয়েছে" → "মামলা রায় পিছানো হয়েছে" |
| 5 | Present continuous | Verb phrase → nominalised verb + আছে | "কষ্ট দিচ্ছে" → "কষ্ট দেওয়া আছে" |
| 6 | Past continuous | Verb phrase → nominalised verb + ছিল | "আনন্দ করছিল" → "আনন্দ ছিল" |
| 7 | Numerical values | Numerals move toward the end; ∗টা/∗টি/∗জন markers drop | "তিনটা পেন্সিল আছে" → "পেন্সিল আছে তিন" |

Cross-cutting transformations that apply inside any tense:

- **Temporal adverbs become explicit numeric forms.** "গত বছর" ’last year’ →
  "এক বছর আগে" ’one year ago’; "পরের সপ্তাহে" ’next week’ → "সাত দিন পর"
  ’seven days later’. Signers count explicitly rather than using deictic
  relative phrases.
- **Plural marking:** "[Noun] রা → [Noun] ওরা" — an agentic plural marker
  replaces the normal plural suffix.
- **Promotion of the object with ∗কে into subject position:** "পুলিশকর্মীকে বিরক্ত করছিলো"
  → "পুলিশ বিরক্ত ছিল" — the marked object is restated as the acting entity.
- **Complex/derived phrases are simplified:** "শরৎকালীন পিঠার মেলা" →
  "শরৎ সময় পিঠা মেলা" (derived adjectival phrases unfold into time word
  + noun).

## 3. Where written Bangla and signed Bangla disagree

These observational facts come from the paper (§3.2.2 discussion and §7.1) and
from preliminary experiments during dataset construction. They are exactly the
points our RAG pipeline was built to preserve:

1. **Determiner order:** written "ছেলেটি" ’the boy’ is signed as
   "ছেলে এটি" ’boy it is’ — the noun precedes its demonstrative in the
   signed sequence. A model that never saw this pattern reproduced it badly;
   exposing the pattern through Masked-Token Substitution widened coverage.
2. **Missing signs get decomposed.** Bangla sign vocabulary does not cover
   every word of the hearing community. Signers break such words into a set of
   glosses: "সপ্তাহ" (shoptaho) ’week’ becomes "সাত দিন" (shat din) ’seven
   days’; "রেসিপি" ’recipe’ becomes "খাবার রান্নার নিয়ম" ’food cooking rules’
   (the paper's example motivating the RAG pipeline, §3.2.3).
3. **Names and landmarks are not specially marked.** The released dataset does
   not use dedicated gloss tokens (e.g., FS-NAME) or fingerspelling
   character sequences (e.g., A+D+A+M); such rows were not specifically
   handled and are listed in the paper's limitations (§7.1).
4. **Non-manual markers are absent by design.** Glosses, as an intermediary,
   cannot capture facial expression, body movement, or tone; the dataset has
   no video component and so captures none of these (paper §7.1).

## 4. Using these rules to extend the dataset

The paper found that augmented pairs remain linguistically accurate "because
the glosses were generated using verified rules rather than arbitrary
transformations" (§3.2.1). If you extend the dataset in your own project:

1. Identify the tense first (that is the two-stage prompting design).
2. Apply only the rules of that tense.
3. Verify the resulting pairs with a professional signer before releasing
   them — our validation protocol is described in
   [annotation-protocol.md](annotation-protocol.md), and the rates we measured
   (75.3% validation on a synthetic sample, κ = 0.7489 binary agreement) set
   the bar in the paper (§3.2.1).

## 5. What this release does not include

- The full compiled rule inventory beyond the published rule categories — the
  tense-specific decomposition used inside the two-stage prompting pipeline is
  documented here and in the prompt file only up to what the paper and the
  experiment material expose (flagged to the authors for a v1.1 decision).
- Tense categories not induced by the 7 rule families — the released data also
  contains rows labelled `past_perfect`, `future_continuous` and
  `present_perfect_continuous` — see `dataset-statistics.md` for exact counts
  and the augmentation-methods page for how these were handled.
- Sign-level (video) information; the dataset is text-only by design.
