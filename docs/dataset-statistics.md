# Dataset statistics

Every number on this page is computed directly from the released files
(`scripts/assign_ids.py` output) — not transcribed from the paper. Where the
paper and the files differ, both are given (see §6).

## 1. Zones and splits

| Zone | File | Rows | Content |
|---|---|---:|---|
| Human-annotated (train) | `data/human/train.json` | 797 | expert-annotated |
| Human-annotated (validation) | `data/val.json` | 100 | expert-annotated |
| Human-annotated (test) | `data/test.json` | 100 | expert-annotated |
| **Human total** | | **997** | |
| Augmented (train) | `data/augmented/train.json` | 3,797 | 797 human + 3,000 synthetic |
| Synthetic (train) | (within augmented) | 3,000 | see split below |
| **Full dataset (train+val+test)** | | | 3,997 ≈ the paper's "4,000" |

The paper describes the dataset as "1,000 human-annotated sentence–gloss pairs.
augmented with around 3,000 synthetically generated pairs" — a final count of
4,000 with a 1:3 original-to-augmentation ratio (§3.2). The distributed files
carry 997 human-annotated rows; see §6.

## 2. Synthetic rows by method

| `generation_type` | Method (paper §) | Rows | ID prefix |
|---|---|---:|---|
| `rag_aug` | Retrieval-augmented few-shot prompting (§3.2.3) | 2,119 | `bsgp-r-####` |
| `morph_aug` | Rule-based morphological transformation (§3.2.1) | 498 | `bsgp-m-####` |
| `context_aug` | Masked-Token Substitution, BanglaBERT (§3.2.2) | 383 | `bsgp-c-####` |
| **Total** | | **3,000** | |

Paper phrasing: "around 500" pairs were generated with each of the two rule
methods and 2,000 with RAG (§3.2.1–§3.2.3). The released counts are the exact
numbers in the files.

## 3. Tense distribution

| `tense` | Human rows | % of 997 | Synthetic rows | % of 3,000 |
|---|---:|---:|---:|---:|
| `simple_present` | 317 | 31.8% | 1,158 | 38.6% |
| `present_continuous` | 177 | 17.8% | 264 | 8.8% |
| `simple_past` | 165 | 16.5% | 678 | 22.6% |
| `present_perfect` | 142 | 14.2% | 250 | 8.3% |
| `simple_future` | 133 | 13.3% | 433 | 14.4% |
| `past_perfect` | 40 | 4.0% | 40 | 1.3% |
| `past_continuous` | 17 | 1.7% | 157 | 5.2% |
| `present_perfect_continuous` | 6 | 0.6% | 10 | 0.3% |
| `future_continuous` | 0 | 0.0% | 10 | 0.3% |

Notes:

- The human-annotated set contains no `future_continuous` rows; the synthetic
  side has 10.
- Tenses present in the data but absent from the seven published prompt-rule
  categories (`past_perfect`, `present_perfect_continuous`,
  `future_continuous`) sum to 46 human rows and 60 synthetic rows. See
  [linguistic-rules.md](linguistic-rules.md) §5.

## 4. Sentence structure

| `type` | Human | Synthetic |
|---|---:|---:|
| `simple` | 689 | 2,552 |
| `complex` | 198 | 353 |
| `compound` | 110 | 95 |

## 5. Topic coverage

- **22 topics**, **651 subtopics** across the human-annotated rows.
- Largest topics by human rows: `food` (164), `education` (79), `sports`
  (79), `crime` (72), `health_and_disease` (68),
  `family_and_relationships` (68), `natural_disasters` (63), `technology`
  (58).
- Topic labels are curation metadata from sentence collection (retrieval
  grouping), not sign annotations — see
  [glossing-conventions.md](glossing-conventions.md) §3.

## 6. Data observations worth knowing

Honest oddities we verified in the released data, so that downstream users
are not surprised:

1. **997 vs 1,000.** The paper's headline "1,000 human-annotated pairs" is
   close-but-not-equal to the 997 rows in the distributed files
   (797+100+100). The 1:3 ratio claim (4,000 total) is correspondingly
   3,997 total. If you cite the dataset, the released counts are the safest
   ones.
2. **Repeated sentence strings.** 990 distinct `sentence` strings cover the
   997 human-annotated rows; seven sentence strings appear more than once
   (each occurrence is a distinct row with its own ID — the pairs are not
   identical duplicates of each other as rows, but the underlying sentence
   string recurs; during construction these may reflect different sentence
   sources/topic contexts).
3. **Repeated synthetic pairs.** Of the 3,000 synthetic rows, three
   (sentence, gloss) combinations appear twice (as distinct rows with
   distinct IDs).
4. **Method counts vs "around 500".** `context_aug` released 383 rows against
   the paper's "around 500" phrasing; `morph_aug` is 498. If you need the
   authoritative reconciliation, contact the maintainers.

For file formats, label vocabularies and stable IDs, see
[data/README.md](../data/README.md) and
[glossing-conventions.md](glossing-conventions.md).
