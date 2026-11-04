# How to serve Bangla-SGP on Hugging Face

The HF dataset repository mirrors this GitHub repository's `data/` layout, so
the card in `README.md` (this folder) is portable as-is.

## What to upload

```
OpenCR-lab/Bangla-SGP/
├── README.md              ← copy of hf/README.md (the dataset card with the
│                            configs YAML at the top)
├── data/
│   ├── human/train.json   ← from this repo's data/human/
│   ├── augmented/train.json
│   ├── val.json
│   └── test.json
```

Do **not** upload `data/raw/` (duplicates the same rows without IDs and can
confuse the viewer) or the paper documents.

## Commands

```bash
# once: login (or use an org token with write access)
huggingface-cli login

# create the dataset repository
huggingface-cli repo create Bangla-SGP --repo_type dataset \
    --org OpenCR-lab

# upload (run from a staging folder that contains the 5 files above,
# or push the subset files directly from this repo)
huggingface-cli upload OpenCR-lab/Bangla-SGP hf/README.md README.md
huggingface-cli upload OpenCR-lab/Bangla-SGP \
    data/human/train.json data/human/train.json \
    --repo-type dataset
huggingface-cli upload OpenCR-lab/Bangla-SGP \
    data/augmented/train.json data/augmented/train.json \
    --repo-type dataset
huggingface-cli upload OpenCR-lab/Bangla-SGP \
    data/val.json data/val.json --repo-type dataset
huggingface-cli upload OpenCR-lab/Bangla-SGP \
    data/test.json data/test.json --repo-type dataset
```

(Equivalent via the `huggingface_hub` Python library with `api.upload_folder`
if you prefer one call.)

## Checklist after upload

1. **Viewer works for both configs** — the card's YAML declares
   `config_name: human` (default) and `config_name: augmented` sharing
   `data/val.json` and `data/test.json`. The Hub docs (datasets-manual-
   configuration) define this subset form; whether one file feeding two
   viewer configs passes validation has not been observed on a live dataset
   yet — verify the Dataset Viewer tab directly after upload, and if the
   viewer rejects the shared files, fall back to duplicating `val.json` /
   `test.json` into each config's folder (and say so in the card).
2. **License badge shows CC BY-4.0** (from the card YAML).
3. **`datasets.load_dataset("OpenCR-lab/Bangla-SGP", "human")` returns
   797/100/100 rows** for train/validation/test, and `"augmented"` returns
   3,797/100/100.
4. **Link back:** the card's "Code and full documentation" link points to
   this repository; per the org conventions, HF cards carry Paper / Code
   links (structure reference: MIT HAN Lab cards).
5. **Tag releases to match** `CITATION.cff` (v1.0.0 now).
