# Glossing conventions in Bangla-SGP

How to read `sentence` and `gloss` fields, what the annotation labels mean,
and what a valid gloss looks like. For *how* glosses are derived from the
text form, see [linguistic-rules.md](linguistic-rules.md); for how annotation
and validation were carried out, see [annotation-protocol.md](annotation-protocol.md).

## 1. What a gloss is here

A **gloss sequence** is a textual representation of how a Bangla sentence is
expressed in Bangladesh Sign Language (BdSL). Each "word" of the sequence is
a gloss: a sign that the sentence's meaning decomposes into. Glosses serve as
an **intermediate representation** for continuous signing — the bridge
between written Bangla and sign video or 3D animation pipelines that the
paper targets (§1, §7.2).

Two important boundary conditions, stated plainly:

- Bangla-SGP contains **no video, no pose and no sign-recording** layers. It
  is a sentence–gloss parallel corpus.
- A gloss here is written **in Bangla script as natural text**, not as
  uppercase English tokens and not as fingerspelling sequences. This
  reflects how the professional signer writes gloss sequences when
  transcribing signed Bangla sentences.

## 2. The pair

| Field | In practice |
|---|---|
| `sentence` | The **written/spoken** form: standard orthographic Bangla as found in newspapers, literature, textbooks and the development book's sentences. |
| `gloss` | The **signed** form: the sequence a signer would produce, with BdSL word order and the tense/nominalisation transformations applied. Not a translation of the sentence — a transcription of its signing. |

Worked contrast from the paper (§3.2.1): the written sentence
"আমি কাজ করব" (ami kaj korbo) ’I will work’ becomes the gloss
"আমি কাজ করা হবে" (ami kaj kora hobe) ’I work do will be’ — the verb is
nominalised and the tense auxiliary takes the final slot, because that is
the order in which the meanings are signed. Where models get such pairs
wrong, and how the errors look, see [error-analysis.md](error-analysis.md).

## 3. Annotation labels

Every row carries five labels describing the sentence, assigned during
creation according to the paper §3.1–3.2 and our validation form.

### `tense`

The tense vocabulary comes from the dataset sources; the human-annotated
splits establish the terminology. Values in the released data:

`simple_present`, `simple_past`, `simple_future`, `present_continuous`,
`present_perfect`, `past_continuous`, `past_perfect`,
`present_perfect_continuous`, `future_continuous`.

### `type`

Structural class of the written sentence: `simple`, `complex`, `compound`.

### `topic` / `subtopic`

Broad theme (e.g., `health_and_disease`, `food`, `technology`,
`family_and_relationships`, `crime`, `asking_for_information`) and a
snake_case subtopic (e.g., `mobile_medical_team`, `cooking_oil`, `email`).
Topics exist because sentence collection was curated from multiple corpora
and needed retrieval groups; the topic labels are not part of the sign
annotation (for the retrieval stage, groups help; for translation, ignore
them).

### `generation_type`

Provenance of the row — which of the three augmentation methods produced it:

| Value | Meaning | Count | Stable-ID prefix |
|---|---|---|---|
| `human_annotation` | expert-annotated by a professional signer | 997 | `bsgp-h-` |
| `morph_aug` | Rule-based morphological transformation of a human-annotated pair | 498 | `bsgp-m-` |
| `context_aug` | Masked-Token Substitution with BanglaBERT | 383 | `bsgp-c-` |
| `rag_aug` | Retrieval-augmented few-shot generation (two-stage prompting) | 2,119 | `bsgp-r-` |

An example of decompositional convention: the paper (§7.1) states that words
without single signs, e.g. "সপ্তাহ" ’week’, are represented with whatever
multi-gloss sequence the signer uses ("সাত দিন" ’seven days’). There is no
wrapper token; the decomposition is plain text in `gloss`.

## 4. Punctuation and casing

- Gloss text keeps sentence-final punctuation, matching the sentence's
  punctuation style in most rows.
- No uppercase-casing convention exists (Bangla has no case).
- No transliteration field exists in v1; transliterations in our docs follow
  the paper's romanization (lowercase words, e.g., `ami bhaat khai`).

## 5. Stable row IDs

`id` is added at release by `scripts/assign_ids.py`. Format:

- `bsgp-h-0001` … `bsgp-h-0997`: human-annotated rows, numbered across train
  (1–797), validation (798–897) and test (898–997) splits in file order.
- `bsgp-m-####` / `bsgp-c-####` / `bsgp-r-####`: synthetic rows by method,
  numbered in file order within `data/augmented/train.json`.

IDs are frozen: corrected errata rows get new IDs; existing IDs never change.
If you publish derived data, keep the `id` field so papers can point back to
exact rows.
