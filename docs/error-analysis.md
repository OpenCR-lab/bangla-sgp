# Error analysis of fine-tuned models

Reproduced from Table 4 of the paper (p. 10464): examples of model-generated
gloss errors compared with corrected forms, showing the recurring failure
patterns the paper identifies — **tense handling, lexical ambiguity, and
pronoun selection** (§4.3). Anyone building on Bangla-SGP should know these
patterns: they are the linguistic gaps most worth fixing in prompt design or
data extensions, and most of them connect directly to the rules documented in
[linguistic-rules.md](linguistic-rules.md).

| Category | Bangla text | Transliteration | English translation |
|---|---|---|---|
| Text 1 | তার মাথায় গুলির ক্ষতিচিহ্ন রয়েছে | Tar mathay gulir khotochihno royeche | There is a bullet wound mark on his head. |
| Gloss (Incorrect) | তার মাথা গুলি ক্ষতিচিহ্ন থাকা আছে | Tar matha guli khotochihno thaka ache | His head bullets scar mark being is. |
| Gloss (Correct) | তার মাথা গুলি ব্যাথা চিহ্ন আছে | Tar matha guli byatha chihno ache | His head bullets pain mark is. |
| Text 2 | এই কাজটিই তিনি করে দেখিয়েছেন | Ei kajti-i tini kore dekhiyechen | He has done this work. |
| Gloss (Incorrect) | এই কাজ ওরা করা দেখা হয়েছ | Ei kaj ora kora dekha hoyeche | This work they doing seen has been. |
| Gloss (Correct) | এই কাজ তিনি করা দেখা হয়েছ | Ei kaj tini kora dekha hoyeche | This work he doing seen has been. |
| Text 3 | এখানে প্রকৃতি খুবই উদার | Ekhane prokiti khub-i udar | Nature is very generous here. |
| Gloss (Incorrect) | এখানে প্রকৃতি অনেক উদার | Ekhane prokiti onek udar | Here nature much generous. |
| Gloss (Correct) | এখানে প্রকৃতি অনেক দয়ালু | Ekhane prokiti onek doyalu | Here nature much kind. |

## Reading the examples

1. **Lexical ambiguity (Text 1):** the model kept the written-Bangla compound
   "ক্ষতিচিহ্ন" (‘injury mark’) inside the gloss; the corrected form decomposes
   it the way a signer would — "ব্যাথা চিহ্ন" (‘pain mark’). Signed
   vocabulary prefers plain, decomposable words over long derived compounds.
2. **Pronoun selection (Text 2):** a single person-marking slip ("ওরা" ‘they’
   for "তিনি" ‘he’) changes who the sentence is about — pronouns are
   semantically load-bearing in glosses even when the surrounding structure
   is right.
3. **Tense handling (Text 3):** glosses blur "খুবই" (‘very’) into quantity
   ("অনেক" ‘much’) and lose adjective precision ("উদার" ‘generous’ vs.
   "দয়ালু" ‘kind’). The paper's experiments showed consistent gains after
   augmentation but errors of this class persist (§4.3–4.4).

## Context: where the numbers come from

Models fine-tuned on Bangla-SGP perform comparably to, and mostly better
than, the same models on RWTH-PHOENIX-2014T under identical settings
(BLEU-4 / COMET for mBART-50: 27.31 / 0.8261 here vs. 21.49 / 0.6673 there;
for mT5-small: 20.28 / 0.8602 vs. 18.73 / 0.6205). The paper is explicit that
the side-by-side numbers "are presented for reference purposes only; direct
cross-linguistic comparison of BLEU scores is not implied" (Table 3 note).
Full results are in the README's results tables and in the paper (§4.3–4.4).

## Known open issues worth research attention

From the paper's limitations (§7.1), these remain unsolved in the released
data — natural extension targets:

- Names and landmarks have **no dedicated gloss tokens** (no FS-NAME-style
  markers, no fingerspelled character sequences like A+D+A+M).
- Non-manual markers (facial expression, body movement) are absent — glosses
  cannot carry them; this requires the Phase-2 video component planned in
  §7.2.
- Tenses beyond the seven published rule categories
  (`past_perfect`, `future_continuous`, `present_perfect_continuous`) appear
  in the data but were not induced as explicit prompt-rule categories.
