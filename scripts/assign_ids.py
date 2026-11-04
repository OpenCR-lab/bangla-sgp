#!/usr/bin/env python3
"""Assign stable row IDs to Bangla-SGP and write the canonical data files.

Reads the untouched archive copies in ``data/raw/`` and writes the canonical
release files under ``data/`` with a stable ``id`` field inserted as the first
key of every row.

ID scheme (frozen at v1.0.0):
- ``bsgp-h-####``  human-annotated pair, numbered across train, then val,
  then test, in file order.
- ``bsgp-m-####``  synthetic pair produced by Rule-based Morphological
  Transformation (``generation_type: morph_aug``).
- ``bsgp-c-####``  synthetic pair produced by Masked-Token Substitution
  (``generation_type: context_aug``).
- ``bsgp-r-####``  synthetic pair produced by RAG-based few-shot prompting
  (``generation_type: rag_aug``).

Human-annotated rows appear both in the ``human`` zone (all of them) and in
the ``augmented`` training file (its train split); they carry the *same* ID in
both places so the zones can be joined on ``id``.

Usage::

    python3 scripts/assign_ids.py

Run from the repository root. Idempotent: re-running produces identical
output from the same raw input.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data")

RAW_HUMAN = RAW / "human-annotated" / "train.json"
RAW_VAL = RAW / "val.json"
RAW_TEST = RAW / "test.json"
RAW_AUG = RAW / "augmented" / "train.json"

SYNTH_PREFIX = {"morph_aug": "m", "context_aug": "c", "rag_aug": "r"}


def row_key(row: dict) -> str:
    """Stable identity of an untouched row (to link duplicate copies)."""
    blob = json.dumps(row, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def with_id(row: dict, row_id: str) -> dict:
    """Insert ``id`` as the first key, keep every other key in file order."""
    return {"id": row_id, **row}


def load(path: Path) -> list:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit(f"{path}: expected a JSON array of rows")
    return rows


def dump(rows: list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"wrote {len(rows):5d} rows -> {path}")


def main() -> None:
    human_train = load(RAW_HUMAN)
    val = load(RAW_VAL)
    test = load(RAW_TEST)
    aug_train = load(RAW_AUG)

    counters = {"h": 0, "m": 0, "c": 0, "r": 0}

    def next_id(prefix: str) -> str:
        counters[prefix] += 1
        return f"bsgp-{prefix}-{counters[prefix]:04d}"

    for rows in (human_train, val, test):
        for row in rows:
            if row.get("generation_type") != "human_annotation":
                raise SystemExit(
                    f"unexpected row in human-annotated zone: {row.get('generation_type')!r}"
                )
    if len(human_train) + len(val) + len(test) != 997:
        raise SystemExit(
            "expected 997 human-annotated rows (797 train + 100 val + 100 test), "
            f"got {len(human_train) + len(val) + len(test)}"
        )

    # Human zone: bsgp-h runs across train, then val, then test.
    human_train_tagged = [with_id(r, next_id("h")) for r in human_train]
    val_tagged = [with_id(r, next_id("h")) for r in val]
    test_tagged = [with_id(r, next_id("h")) for r in test]
    id_by_key = {}
    for tagged in (human_train_tagged, val_tagged, test_tagged):
        for row in tagged:
            id_by_key[row_key({k: v for k, v in row.items() if k != "id"})] = row["id"]

    # Augmented zone: synthetic rows get their own prefix, in file order;
    # embedded copies of human-annotated rows reuse the human-zone IDs.
    augmented_tagged = []
    for row in aug_train:
        gtype = row.get("generation_type")
        if gtype == "human_annotation":
            key = row_key(row)
            if key not in id_by_key:
                raise SystemExit(f"embedded human row not found in human zone: {key[:12]}…")
            augmented_tagged.append(with_id(row, id_by_key[key]))
        elif gtype in SYNTH_PREFIX:
            augmented_tagged.append(with_id(row, next_id(SYNTH_PREFIX[gtype])))
        else:
            raise SystemExit(f"unknown generation_type: {gtype!r}")

    dump(human_train_tagged, OUT / "human" / "train.json")
    dump(val_tagged, OUT / "val.json")
    dump(test_tagged, OUT / "test.json")
    dump(augmented_tagged, OUT / "augmented" / "train.json")

    n_synthetic = counters["m"] + counters["c"] + counters["r"]
    print(
        "counts:",
        f"human={counters['h']}, morph={counters['m']}, "
        f"context={counters['c']}, rag={counters['r']}, synthetic={n_synthetic}",
    )
    if n_synthetic != 3000:
        raise SystemExit(f"expected 3000 synthetic rows, got {n_synthetic}")


if __name__ == "__main__":
    main()
