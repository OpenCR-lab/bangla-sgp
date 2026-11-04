---
pretty_name: Bangla-SGP
license: cc-by-4.0
language:
- bn
task_categories:
- translation
tags:
- sign-language
- gloss
- bangla
- bdsl
- low-resource
- data-augmentation
size_categories:
- 1K<n<10K
source_datasets: []
configs:
- config_name: human
  default: true
  data_files:
  - split: train
    path: data/human/train.json
  - split: validation
    path: data/val.json
  - split: test
    path: data/test.json
- config_name: augmented
  data_files:
  - split: train
    path: data/augmented/train.json
  - split: validation
    path: data/val.json
  - split: test
    path: data/test.json
---

# Bangla-SGP

**Bangla-SGP** is a parallel dataset of human-annotated and rule-augmented
Bangla sentence–gloss pairs for **Bangla Sign Language (BdSL) translation
research**: 997 human-annotated pairs (annotated by a professional signer)
plus 3,000 synthetically generated pairs (rule-based morphological
transformation, masked-token substitution, and RAG-based few-shot
prompting released with a GPT-4.1-nano two-stage pipeline).

Paper: *Introducing A Bangla Sentence – Gloss Pair Dataset for Bangla Sign
Language Translation and Research* (LREC 2026, pp. 10457–10466,
[landing page](https://lrec.elra.info/lrec2026-main-820),
[DOI](https://doi.org/10.63317/38qenrwzegr9)).

Code and full documentation: [github.com/OpenCR-lab/bangla-sgp](https://github.com/OpenCR-lab/bangla-sgp).

## Why: the creation rationale

Gloss sequences — individual Bangla sign–supported words in signed order —
serve as an intermediate representation for continuous signing. Bangladesh
has ~13 million people with hearing difficulties (3 million deaf); research
on sentence-level BdSL was blocked by the lack of a sentence-level dataset.
Bangla-SGP supplies that layer, annotated by a professional signer.

## Configuration and structure

Two configurations share the same validation and test files (the original
1,000-pair set was split 80/10/10; identical val/test are used both times so
results with and without augmentation stay comparable):

| config | train | validation | test | what it is |
|---|---|---:|---:|---|
| `human` (default) | `data/human/train.json` | `data/val.json` | `data/test.json` | expert-annotated pairs only (997) |
| `augmented` | `data/augmented/train.json` | `data/val.json` | `data/test.json` | the shared human train rows + 3,000 synthetic pairs (3,797) |

Each row: `id` (stable ID), `sentence` (Bangla), `gloss` (BdSL gloss
sequence, Bangla script), `topic`, `subtopic`, `tense`, `type`,
`generation_type` (`human_annotation` / `morph_aug` / `context_aug` /
`rag_aug`). Example:

```json
{"id": "bsgp-h-0001",
 "sentence": "প্লাবিত গ্রামে মোবাইল মেডিকেল টিম পাঠানো হয়েছে।",
 "gloss": "পানির প্লাবিত গ্রাম ওখানে মোবাইল মেডিকেল টিম যাওয়া হয়েছে।",
 "topic": "health_and_disease", "subtopic": "mobile_medical_team",
 "tense": "present_perfect", "type": "simple",
 "generation_type": "human_annotation"}
```

## Augmentation methods (summary)

1. **Rule-based Morphological Transformation** (`morph_aug`, 498): tense
   rules compiled with the professional signer (e.g., future: verb →
   nominalised verb + "হবে").
2. **Masked-Token Substitution** (`context_aug`, 383): BanglaBERT fills
   masked nouns/verbs inside rule-safe templates to build lexical variants.
3. **RAG-based few-shot prompting** (`rag_aug`, 2,119): LaBSE embeddings +
   Pinecone retrieval (threshold 0.5, fallback to rules-only), two-stage
   prompting with GPT-4.1-nano; published validation 75.3% validation rate,
   quality 3.19/5, binary κ = 0.7489.

Full rules and prompt templates: [`docs/prompts/translation-rules-prompt.md`](https://github.com/OpenCR-lab/bangla-sgp/blob/main/docs/prompts/translation-rules-prompt.md)
and [`docs/linguistic-rules.md`](https://github.com/OpenCR-lab/bangla-sgp/blob/main/docs/linguistic-rules.md).
Datasheet: [`DATASHEET.md`](https://github.com/OpenCR-lab/bangla-sgp/blob/main/DATASHEET.md).

## Results on this dataset (from the paper, Tables 2–3)

| Model | Dataset | BLEU-1 | BLEU-2 | BLEU-3 | BLEU-4 | COMET |
|---|---|---:|---:|---:|---:|---:|
| mT5-small | Base (1K) | 51.79 | 36.26 | 25.73 | 17.56 | 0.8564 |
| mT5-small | Augmented (4K) | 55.33 | 40.11 | 29.06 | 20.28 | 0.8602 |
| mBART-50 | Base (1K) | 56.65 | 40.96 | 29.36 | 21.06 | 0.7829 |
| mBART-50 | Augmented (4K) | 61.09 | 46.01 | 35.09 | 27.31 | 0.8261 |
| GPT-4.1-nano | Augmented (4K) | 57.11 | 41.50 | 31.11 | 22.42 | 0.8913 |
| NLLB-200-1.3B | Base (1K) | 67.99 | 40.82 | 26.49 | 16.67 | 0.907 |

Reference-only side-by-side with RWTH-PHOENIX-2014T is printed in the paper
with the explicit note that direct cross-linguistic comparison of BLEU
scores is not implied.

## Limitations & considerations

- **Text-only.** No video, audio, pose, or non-manual markers; glosses cannot
  represent facial expression or body movement. Phase 2 (synchronized video +
  non-manual markers) is planned (paper §7.2).
- **Single base annotator** — the paper flags potential signer bias.
- **No dedicated handling of names/landmarks** (no FS-NAME-style tokens, no
  fingerspelled sequences).
- **Signer credit:** Mr. Ariful Islam (BTV) annotated; Mr. Ariful Islam and
  Mrs. Tanjila Tartushi (BTV) validated independently — with the annotators'
  informed consent (paper §7.3).
- Counts: paper round-phrases are "1,000 / ~3,000 / 4,000"; the released
  files carry 997 / 3,000 / 3,997 rows. Seven human sentence strings recur;
  three synthetic pairs repeat
  ([details](https://github.com/OpenCR-lab/bangla-sgp/blob/main/docs/dataset-statistics.md),
  §6).

## Licence

Data: **CC BY-4.0**. Repository code and documentation: **MIT**. Attribution
requirements: cite the paper and the dataset; see `DATA_LICENSE.md`.

## Citation

See the repository's [CITATION.cff](https://github.com/OpenCR-lab/bangla-sgp) for the
machine-readable form; BibliTeX:

```bibtex
@inproceedings{saha-etal-2026-introducing,
  title     = "Introducing A Bangla Sentence -- Gloss Pair Dataset for
               Bangla Sign Language Translation and Research",
  author    = {Saha, Neelavro and Shahriyar, Rafi and Roudra, Nafis Ashraf and
               Sakib, Saadman and Rasel, Annajiat Alim},
  booktitle = {Proceedings of the Fifteenth Language Resources and Evaluation
               Conference (LREC 2026)},
  pages     = {10457--10466},
  year      = {2026},
  publisher = {European Language Resources Association (ELRA)},
  doi       = {10.63317/38qenrwzegr9},
  url       = {https://lrec.elra.info/lrec2026-main-820}
}
```

Questions: the organisation's contact on the GitHub repository README.
