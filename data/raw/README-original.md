# Bangla-SGP Dataset

\*\*This Repository contains the dataset, Bangla-SGP for the Paper **"Introducing a Bangla Sentence–Gloss Pair Dataset for Bangla Sign Language Translation and Research."**

Two versions of the dataset are included:

- **Bangla-SGP\_humanAnnotated** – Around 1,000 *human-annotated* Bangla sentence–gloss pairs  
- **Bangla-SGP\_Augmeneted** – Around 4,000 *human-annotated \+ augmented* pairs

---

## Folder Structure

```
Bangla-SGP/
│
├── bangla-sgp_humanAnnotated/
│   └── train.json
│
├── bangla-sgp_Augmented/
│   └── train.json
│
├── val.json
├── test.json
└── README.md


```

**Note:** The original dataset of 1,000 expert-annotated sentence–gloss pairs was split into training, validation, and test sets in the proportions of 80%, 10%, and 10%, respectively.  
The same test and val set was used when evaluating the augmented dataset to ensure a fair comparison.

---

