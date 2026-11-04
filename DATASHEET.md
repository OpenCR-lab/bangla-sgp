# Bangla-SGP Dataset Datasheet

Recommended citation of this document: the *Datasheets for Datasets* format
(Gebru et al., 2021). Blueprint for the questions people ask before adopting
a dataset; answers are specific to Bangla-SGP v1.0. Cross-references:
[docs/annotation-protocol.md](docs/annotation-protocol.md) (how annotation
and validation were done), [docs/dataset-statistics.md](docs/dataset-statistics.md)
(counts), [DATA_LICENSE.md](DATA_LICENSE.md) (licence).

## 1. Motivation

**For what purpose was the dataset created?** Bangla Sign Language (BdSL)
translation is a low-resource NLP problem: prior work was limited to
word-level and alphabet-level detection, and no large-scale sentence-level
dataset existed. Bangla-SGP was created as *Phase 1* of a multi-modal BdSL
dataset programme: a parallel corpus of Bangla sentences and their BdSL
gloss sequences, usable to train and evaluate transformer-based
text-to-gloss translation models (and, downstream, gloss-driven 3D signing
pipelines).

**Who created the dataset?** Neelavro Saha, Rafi Shahriyar, Nafis Ashraf
Roudra, Saadman Sakib and Annajiat Alim Rasel (Department of Computer Science
and Engineering, BRAC University, Bangladesh), publishing as the Bangla-SGP
paper in the Proceedings of LREC 2026 (pp. 10457–10466). Gloss annotation and
validation were performed by the professional signers credited in §8.

**Funding:** not stated in the released materials. The research was carried
out inside an academic curriculum at BRAC University.

## 2. Composition

**What do the instances represent?** One instance = one Bangla sentence
(`sentence`) paired with its BdSL gloss sequence (`gloss`), plus four
annotation labels (`topic`, `subtopic`, `tense`, `type`) and a provenance
tag (`generation_type`, `id`). Schemas and ID scheme:
[data/README.md](data/README.md).

**How many instances?**

| Zone | Rows |
|---|---:|
| Human-annotated (all splits) | 997 |
| Synthetic (augments the train split) | 3,000 |
| **Full dataset (train+val+test)** | **3,997** |

The paper reports this as 1,000 + ~3,000 ≈ 4,000; the released files
determine the exact numbers.

**What data?** Text only. Written/spoken Bangla sentences (newspaper
corpora, Bangla literature, the BdSL language development book, educational
Bangla books; further synthetic candidates drawn from the public Bangla
Corpus by Nuhash Afnan) and Bangla-script gloss sequences. **No video, no
audio, no pose data, no images.** Non-manual markers (facial expression,
body movement) are therefore outside the dataset's scope by design — the
paper's §7.1 lists this among limitations.

**Is any information confidential or offensive?** The dataset contains news,
educational and everyday-life sentences. Some rows concern crime or health
topics because sentence sources included newspapers; content is descriptive
news prose, not personal data. No participant data is included.

**Duplicate content (verified):** 990 distinct sentence strings cover the 997
human-annotated rows; three synthetic (sentence, gloss) combinations appear
twice. See [docs/dataset-statistics.md](docs/dataset-statistics.md) §6.

## 3. Collection and annotation process

Performed by the authors and the professional signers described in
detail in [docs/annotation-protocol.md](docs/annotation-protocol.md):

- Sentences were curated by the research team from the sources above.
- Glosses were annotated by **Mr. Ariful Islam**, an experienced Bangla sign
  language presenter at BTV.
- Synthetic pairs were produced by the three published methods
  (rule-based morphological transformation; masked-token substitution with
  BanglaBERT; RAG-based few-shot prompting with GPT-4.1-nano and two-stage
  prompting; see [docs/augmentation-methods.md](docs/augmentation-methods.md)).
- A 15% sample of RAG-generated pairs was validated independently by two
  professional signers (**Mr. Ariful Islam, Mrs. Tanjila Tartushi**), with
  Yes/No + 1–5 rating fields and Cohen's kappa reported
  (κ = 0.7489 binary / κ = 0.3496 quality; 75.3% average validation rate).

**Was review/consent collected?** Yes — the paper's ethics statement (§7.3):
gloss annotation was done "with explicit consent from a certified Bangla
Sign Language (BdSL) interpreter", with informed consent obtained and the
signers aware that the data would be used for academic research purposes.

## 4. Preprocessing, cleaning, labelling

- Punctuation follows the sentence sources; we do not re-normalise dots vs.
  the Bangla danda (।) between fields — rows carry whatever their creation
  pipeline produced.
- The only transformation applied for this release is the stable row `id`
  prepended to each row; all field values are byte-identical to the
  originally distributed archive.
- No rows were removed, deduplicated or edited for release.

## 5. Uses and limits

**Recommended uses:** training/fine-tuning/evaluating Bangla
sentence-to-gloss (text-to-gloss) translation models; studying BdSL gloss
formation and augmentation for low-resource sign languages; benchmarking
against the settings published with the paper (BLEU, COMET; shared val/test
protocol).

**Not recommended:** ASL/dialect claims beyond BdSL; sign recognition tasks
(there is no video); training on synthetic rows without validation-aware
analysis (the synthetic distribution skews toward `simple_present` — see
statistics); linguistic conclusions about regional variation — the paper notes the
 dataset "may include signer bias" from single-annotator base creation and
 contains no fingerspelling/FS-NAME handling for names and landmarks.

**Known limitations (paper §7.1):** synthetic set small relative to modern
transformer needs; single expert annotator (signer bias); no non-manual
markers; limited sign vocabulary coverage (words decomposed into gloss
sets); no dedicated handling of names/landmarks; NLLB-200-1.3B could not be
evaluated on the augmented dataset for compute reasons (so no empirical
check whether augmentation benefits generalise to it).

## 6. Distribution

**Distribution channel:** this repository is the official release promised
by the paper's Dataset Availability Statement (§6). Mirrors, if any, will be
listed in the repository README.

**Licence:** dataset **CC BY-4.0** ([DATA_LICENSE.md](DATA_LICENSE.md));
repository code and written documentation **MIT** ([LICENSE](LICENSE)).
The paper text itself is under the LREC 2026 proceedings copyright (ELRA).

**Maintenance:** errata and extensions will be released as tagged versions;
existing row IDs will never be reused or altered. Major multimodal extension
(synchronized sign videos + non-manual markers) is planned as Phase 2 per
the paper's §7.2 and would be a new release generation of this project.

## 7. Annotator compensation

Compensation arrangements for the professional signers are internal to the
team and not published with the dataset. The credit and consent details
that are public are recorded above and in the README's acknowledgements.

## 8. Crediting the signers

Anyone using the dataset should credit the professional signers, whose
linguistic judgement is the dataset's reliability foundation:

- **Mr. Ariful Islam** — professional sign language presenter, BTV; gloss
  annotation of the full pair set; joint validation of synthetic samples.
- **Mrs. Tanjila Tartushi** — professional sign presenter, BTV; independent
  validation of synthetic samples.
