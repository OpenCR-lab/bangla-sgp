# `data/` — Bangla-SGP dataset files

Three zones, all JSON arrays of rows with one object per sentence–gloss pair.
Every row has a stable `id` as its first field.

```
data/
├── human/
│   └── train.json        797 human-annotated pairs (train split)
├── augmented/
│   └── train.json        3,797 pairs = 797 human (train split) + 3,000 synthetic
├── val.json              100 human-annotated pairs   (validation split, shared)
├── test.json             100 human-annotated pairs   (test split, shared)
└── raw/                  untouched copies of the distributed archive (no ids)
```

- The dataset in the paper is described as 1,000 human-annotated + ~3,000
  augmented pairs (4,000 total); the distributed files contain 997
  human-annotated rows (797 + 100 + 100) and exactly 3,000 synthetic rows.
- The human-annotated rows appear in both the `human` zone and the
  `augmented` training file; they carry the **same `id`** in both places.
- IDs are assigned by `scripts/assign_ids.py` from `data/raw/` and are frozen
  at release: existing IDs never change or get recycled.

## Row schema

| Field | Type | Description |
|---|---|---|
| `id` | string | stable ID (`bsgp-h-####` human, `bsgp-m-####` / `bsgp-c-####` / `bsgp-r-####` synthetic) |
| `sentence` | string | Bangla sentence (written/spoken form) |
| `gloss` | string | BdSL gloss sequence (signed form, see `docs/glossing-conventions.md`) |
| `topic` | string | broad topic label (snake_case) |
| `subtopic` | string | topic refinement (snake_case) |
| `tense` | string | tense label, e.g. `simple_present`, `present_perfect` |
| `type` | string | sentence structure: `simple`, `complex`, `compound` |
| `generation_type` | string | provenance: `human_annotation`, `morph_aug`, `context_aug`, `rag_aug` |

Examples:

```json
{
  "id": "bsgp-h-0001",
  "sentence": "প্লাবিত গ্রামে মোবাইল মেডিকেল টিম পাঠানো হয়েছে।",
  "gloss": "পানির প্লাবিত গ্রাম ওখানে মোবাইল মেডিকেল টিম যাওয়া হয়েছে।",
  "topic": "health_and_disease",
  "subtopic": "mobile_medical_team",
  "tense": "present_perfect",
  "type": "simple",
  "generation_type": "human_annotation"
}
```

```json
{
  "id": "bsgp-r-0001",
  "sentence": "…",
  "gloss": "…",
  "topic": "…",
  "subtopic": "…",
  "tense": "…",
  "type": "…",
  "generation_type": "rag_aug"
}
```

## Loading

Python (plain):

```python
import json
train = json.load(open("data/human/train.json", encoding="utf-8"))
```

Hugging Face (after the HF upload; two configs share the same val/test files):

```python
from datasets import load_dataset
human = load_dataset("OpenCR-lab/Bangla-SGP", "human")
aug   = load_dataset("OpenCR-lab/Bangla-SGP", "augmented")
```

See `hf/README.md` for the dataset card and `hf/UPLOAD.md` for how the HF
repository mirrors this layout.
