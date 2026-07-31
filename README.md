# Deployment-Oriented Deep Learning NIDS Mini Review

This repository contains the reproducibility archive for the Mini Review on deployment-oriented evaluation of deep learning network intrusion detection systems.

## Literature Search and Selection

Papers were selected from 2024 to 2026. Records were identified through targeted scholarly search, then verified against the final journal, conference, publisher, and DOI records. The search sources were Google Scholar, Crossref, IEEE Xplore, ACM Digital Library, ScienceDirect, and SpringerLink. The same Boolean query was used across all six sources, with only source-specific syntax adjustments. The query was ("network intrusion detection" OR NIDS OR "network anomaly detection") AND ("deep learning" OR "neural network") AND ("cross-dataset" OR "domain shift" OR "domain adaptation" OR "open-set" OR "unknown attack" OR "zero-day" OR calibration OR uncertainty OR abstention).

The inclusion criteria were papers published from 2024 to 2026, papers within NIDS or network anomaly detection, and papers using deep learning or a deep-learning-centered hybrid model. Five studies without a deep-learning detector were retained as declared benchmark or deployment-support exceptions (R1, R6, R12, R32, R33). Each paper also had to relate to at least one deployment concern, specifically cross-dataset generalization, open-set or unseen-attack recognition, reliability through calibration or uncertainty, abstention, or deployment adaptation. The exclusion criteria were papers with no deployment relevance, cybersecurity papers outside NIDS, pre-2024 works, inaccessible full texts, insufficiently verifiable papers, and preprint papers. The publication window was 1 January 2024 through 15 April 2026. The same concept groups were tailored to the search syntax of each source.

The record set contained 198 records, comprising 110 from Google Scholar, 37 from Crossref, 18 from IEEE Xplore, 6 from the ACM Digital Library, 18 from ScienceDirect, and 9 from SpringerLink. Duplicate records were removed using exact DOI matching, normalized title matching, and manual review. Titles were converted to lowercase, with punctuation and extra spaces removed. When multiple versions existed, the final peer-reviewed version was kept. This removed 27 duplicate records and left 171 records for title and abstract screening. KLL and KSS screened their assigned records and discussed uncertain cases. Screening excluded 71 records, advanced 98 to full-text assessment, and retained 2 for further checking, forming a 100-record queue. Full-text assessment of this queue was not completed. The synthesis instead uses a separate curated evidence base of 29 full-text-verified empirical papers, without claiming that these were the only eligible papers among the 198 records. Two review papers and four context papers provided background and were not counted in the 29-paper empirical evidence base. Each empirical paper received one primary role, with secondary concerns recorded separately. No study in the curated evidence base jointly evaluated cross-dataset generalization, unknown-attack rejection, and reliability under one unified deployment protocol.

Study quality was assessed in six areas. These were data separation, leakage control, and target-domain access. Transparency of harmonization was also checked. Model, hyperparameter, and threshold selection had to be independent of the test set. Statistical reporting and availability of data, code, and details were included.

This mini-review did not train a model or select a new decision threshold. In the study-quality assessment, threshold selection was considered independent only when training or validation data were used before held-out test evaluation. Test-informed or unreported threshold selection lowered confidence.

This mini-review did not perform new statistical tests or a meta-analysis. Statistical tests reported by the included studies were interpreted as within-study evidence only. A small number of folds or runs and uncorrected pairwise comparisons limited claims of statistical superiority.

## Study inventory

The study inventory contains 35 papers.

- 29 empirical papers in the evidence matrix
- 2 review syntheses discussed separately
- 4 framing and context papers discussed separately

The records are listed in `data/study_inventory.csv`.

## Table 2 extraction and study-quality assessment

`data/table2_extraction_and_quality_assessment.csv` contains one completed row for each of the 29 empirical papers. It records the result or value reported in Table 2, the primary group, the front tested, secondary coverage, the DOI evidence link, the overall confidence rating, the quality rationale, the deployment limitation, and any declared scope exception.

The study-quality assessment is also decomposed into the six areas used in the manuscript:

- data separation
- leakage control
- target-domain access and harmonisation
- test-independent model, hyperparameter, threshold, or cutoff selection
- statistical reporting
- reproducibility and availability of data, code, and methodological details

The domain ratings do not form a numerical score. The overall rating follows the manuscript rule that a critical concern, such as leakage or test-informed selection, can limit confidence even when other areas are clear. The deposited overall ratings match Table 2 at 5 higher, 16 moderate, and 8 limited.

This completed matrix applies only to the separately curated 29-paper evidence base.

Run `python3 scripts/validate_table2_assessment.py` from the repository root to verify the 29-paper identity, metadata, primary-group arithmetic, scope exceptions, required fields, allowed ratings, and confidence totals.

## Files

- `data/study_inventory.csv` — study inventory.
- `data/search_records.csv` — included empirical papers.
- `data/table2_extraction_and_quality_assessment.csv` — Table 2 extraction and quality assessment.
- `data/source_access_log.csv` — retrieval attempt log.
- `data/deduplication_review.csv` — candidate records and review groups.
- `data/deduplicated_screening_records.csv` — post-deduplication ledger.
- `data/title_abstract_screening.csv` — title-and-abstract screening.
- `data/full_text_screening.csv` — full-text queue.
- `data/publication_date_audit.csv` — publication-date verification.
- `data/source_exports/*.csv` — per-source search results (Google Scholar, Crossref, IEEE Xplore, ACM, ScienceDirect, SpringerLink).
- `scripts/add_title_abstract_recommendations.py` — generate title-and-abstract recommendations.
- `scripts/confirm_title_abstract_recommendations.py` — confirm recommendations.
- `scripts/prepare_full_text_screening.py` — create full-text queue.
- `scripts/add_empirical_selection_rationales.py` — add selection rationales.
- `scripts/validate_table2_assessment.py` — validate Table 2 and counts.
- `protocol/search_protocol.md` — search protocol and screening rules.

## Copyright

This repository contains bibliographic metadata, screening decisions, and author-created extraction materials only. Publisher PDFs and copyrighted full texts must not be uploaded.
