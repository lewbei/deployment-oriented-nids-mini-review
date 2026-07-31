# Search protocol

## Publication window

Papers published from 1 January 2024 through 15 April 2026 were eligible. Publications after the final search date were outside the search window.

## Reported search window

The manuscript reports the publication window as 1 January 2024 through 15 April 2026 and does not state a search-execution date.

## Sources and reported counts

| Source | Records |
|---|---:|
| Google Scholar | 110 |
| Crossref | 37 |
| IEEE Xplore | 18 |
| ACM Digital Library | 6 |
| ScienceDirect | 18 |
| SpringerLink | 9 |
| Total | 198 |

## Boolean query

```text
("network intrusion detection" OR NIDS OR "network anomaly detection")
AND ("deep learning" OR "neural network")
AND ("cross-dataset" OR "domain shift" OR "domain adaptation" OR
     "open-set" OR "unknown attack" OR "zero-day" OR calibration OR
     uncertainty OR abstention)
```

The manuscript states that the same concept groups were used across all six sources with source-specific syntax adjustments and a 2024 through 2026 publication-year restriction.

## Deduplication

Duplicate records were assessed using exact DOI matching, normalized title matching, and manual review. Title normalization converted titles to lowercase and removed punctuation and extra spaces. When multiple versions existed, the final peer-reviewed version was retained.

## Screening

The 171 post-deduplication records were divided between KLL and KSS. Each author checked the records assigned to that author. Agent recommendations were stored in separate advisory fields and became live decisions only after the authors confirmed their assigned rows. Uncertain cases and later full-text decisions can be discussed jointly.

### Inclusion criteria

- Published from 2024 through 2026
- Within network intrusion detection or network anomaly detection
- Uses deep learning or a deep-learning-centered hybrid model
- Relates to cross-dataset generalization, open-set or unseen-attack recognition, reliability, abstention, or deployment adaptation

### Exclusion criteria

- No deployment relevance
- Cybersecurity study outside NIDS
- Published before 2024
- Inaccessible or insufficiently verifiable full text
- Preprint rather than a final peer-reviewed publication

## Current screening arithmetic

- 198 records were identified.
- 27 duplicate records were removed, leaving 171 records.
- Title and abstract screening excluded 71 records.
- 98 records were advanced to full-text assessment.
- 2 uncertain records were retained for further checking.
- 100 records formed the full-text queue.
- Full-text assessment of this queue was not completed.
- 29 full-text-verified empirical papers separately formed the curated evidence base used in the manuscript.
- Two review syntheses and four context papers were used for background outside the empirical evidence base.


## Publication-date audit

All retained 2026 records were checked after the six exports were merged and again after corpus alignment. The active ledger contains 80 records dated 2024, 97 dated 2025, and 21 dated 2026, with no blank publication year. Publisher pages, IEEE publication dates, Crossref metadata, and first-posting dates were used as appropriate. The evidence is recorded row by row in `data/publication_date_audit.csv`. The same file also verifies the six 2026 entries in the manuscript study inventory. All 27 audit rows are marked `VERIFIED_BEFORE_CUTOFF`.

An online-first or first-posting date was used when an article's later issue date fell after the cutoff. Preprints remain raw search records and are still subject to the stated screening exclusion rule.

## Full merge and duplicate flags

The six active source exports contain 198 records and are merged in `data/search_ledger.csv`. Exact DOI matching identifies 23 candidate groups, and normalized-title matching identifies 25 candidate groups. In total, 51 records participate in at least one automated candidate group. A subsequent fuzzy-title, author-overlap, and version check identified `GS014` as a differently titled preprint of the final paper represented by `GS017` and `IX003`. The active manual queue therefore contains 52 records in the same 25 connected groups. No candidate has been removed automatically.

The connected candidate groups were divided approximately equally between KLL and KSS. Each assigned author reviewed the groups, confirmed the preprint and final-version relationships, and recorded which version was retained.

The manual review queue is stored in `data/deduplication_review.csv`. It contains one row for each of the 52 candidate records, matching record identifiers, exact DOI and normalized-title groups where applicable, manually verified version groups, a connected review-group identifier, an assigned reviewer, and separate KLL and KSS fields. No connected group is split between reviewers. KLL completed 12 groups containing 26 rows, and KSS completed 13 groups containing 26 rows. `DRG015` was assigned to KSS and `DRG016` to KLL to preserve the exact 26-row split. Both authors confirmed all validated recommendations. The consensus retains one record per connected group, removes 27 duplicate records, and leaves 171 records before title and abstract screening.

One canonical record was identified for each connected group. Selection followed a fixed order. A final peer-reviewed publication was preferred over its preprint. A native publisher or database record was preferred over an aggregator record. When no native record was present, fuller structured Crossref metadata was preferred over an abbreviated Google Scholar row. The base repository object was preferred over a version-specific DOI alias. For otherwise identical records from the same source, the earlier retrieved row was preferred. Applying this rule produced 25 `retain_preferred_version` decisions and 27 `remove_as_duplicate` decisions, all confirmed in the author and consensus fields.

Official DOI metadata was recovered for six Google Scholar rows during the title-only review. Of the 51 automated candidates, 46 are supported by both exact DOI and normalized-title identity and five were initially supported by normalized title only. The five normalized-title groups were compared using authors, URLs, Scholar clusters, abstracts, repository identifiers, and version history. Three groups are repeated hits for the same publication, one links a Research Square preprint to its final IEEE conference version, and one contains base and version-specific DOI forms for the same institutional-repository thesis. The later manual version check added `GS014` as the 52nd candidate even though its preprint title differs from the final title. These findings and the author-confirmed decisions are recorded in the worksheet.

The version relationship in `DRG001` is recorded explicitly. `CR005` is the 2024 Research Square preprint of the work published as the 2025 IEEE conference paper represented by `GS106` and `GS108`. The latter two records carry the same final-publication DOI. The confirmed decision retains `GS106`, removes `GS108` as a repeated final-paper record, and removes `CR005` as the superseded preprint.

The version relationship in `DRG016` is also recorded explicitly. `GS014`, arXiv DOI `10.48550/arXiv.2402.10974`, lists the same three authors, the IEEE Access journal reference, and related final DOI `10.1109/ACCESS.2024.3472907`. `GS017` and `IX003` are repeated records of that final publication. The confirmed decision retains `IX003`, removes `GS017` as a repeated final-paper record, and removes `GS014` as the superseded preprint.

A complete similarity recheck found no candidate group containing unrelated papers that merely have similar titles. Twenty-one connected groups consist only of repeated records carrying an identical DOI. `DRG013` is a repeated Google Scholar record supported by the same normalized title, authors, year, URL, and Scholar cluster despite having no DOI in the retrieved metadata. `DRG001` and `DRG016` are the two preprint-to-final-publication relationships described above, and `DRG004` is one thesis repository object represented by base and version-specific DOI forms.

Two identical-DOI groups use different source-year labels. For `DRG007`, Crossref publisher metadata records online publication on 28 December 2024 and print publication in August 2025. For `DRG017`, Crossref publisher metadata records online publication on 1 January 2025 and a 2025 print year, while the DOI metadata record was created on 31 December 2024. These timing differences explain the source-year discrepancies and do not indicate distinct papers. The evidence is also recorded in the corresponding worksheet rows.

## Author-confirmed post-deduplication screening set

Applying the 25 author-confirmed retains and 27 author-confirmed removals produces `data/deduplicated_screening_records.csv` with 171 records. The 27 removed source identifiers remain traceable through their retained review-group record. The confirmed ledger has no repeated exact DOI or normalized title and still represents all 29 empirical manuscript papers. It does not alter the 198-record identification ledger.

The 171 author-confirmed retained records were copied to `data/title_abstract_screening.csv`. A deterministic SHA-256 ordering of the source-record identifiers was used before alternating assignments, producing 86 rows for KLL and 85 for KSS without using source order as the assignment rule. The assigned author's title-and-abstract decision was left empty before confirmation, while the other author's field was `not_assigned`.

Abstract retrieval was performed in a fixed sequence using the audited local full texts, Crossref metadata, arXiv metadata, OpenAlex metadata, the supplied source pages, web-assisted extraction, indexed publisher and author pages, and direct source PDFs. Abstracts were retrieved for 170 of the 171 records. The retrieved set comprises 31 local full-text abstracts, 24 Crossref abstracts, 72 OpenAlex abstracts, 16 source-webpage metadata abstracts, 15 web-assisted source-page abstracts, 8 additional verified source-webpage abstracts, and 4 direct source-PDF abstracts. No abstract was added during the arXiv phase, and all six arXiv-labelled records were subsequently retrieved through OpenAlex. Each retrieved row records the abstract source and retrieval status.

One record, `TA072`, remains without abstract text. Its complete three-page full-text PDF was checked and shows that the journal Letter begins with section 1 Introduction immediately after the title and authors, with no separate abstract section. This is therefore a publication-format exception rather than a retrieval failure.


## Agent-assisted title-and-abstract recommendation pass

An advisory title-and-abstract pass was completed for all 171 records using the written inclusion and exclusion criteria. The controlled recommendations are `include_for_full_text`, `exclude_at_title_abstract`, and `uncertain_full_text_check`. Relevance signals are recorded separately for cross-dataset or domain-shift evaluation, open-set or unseen-attack recognition, calibration or uncertainty-related reliability, and deployment adaptation or realism.

The advisory pass recommends 98 records for full-text assessment, excludes 71 records at title and abstract, and marks 2 records for a full-text or publication-status check before a decision. The 71 proposed exclusions comprise 36 records with no explicit deployment-front evaluation, 14 reviews or context articles, 14 records without a verified final peer-reviewed publication, 5 records outside NIDS, 1 study that is not deep-learning-centered, and 1 retracted article. `TA152` requires full text because its available abstract is only a truncated source snippet. `TA167` is directly relevant but requires verification of its final peer-reviewed publication status.

All 29 empirical papers already used in the manuscript are among the 98 recommendations for full-text assessment. This is a consistency check, not a rule that determined the other recommendations.

The advisory fields were added by `scripts/add_title_abstract_recommendations.py`. A field-level comparison confirmed that no metadata, abstract, assignment, author-decision, consensus, or adjudication field changed.

## Author-confirmed title-and-abstract outcome

KLL and KSS confirmed all advisory recommendations for their assigned records. KLL confirmed 54 records for full-text assessment, 31 title-and-abstract exclusions, and 1 uncertain full-text check. KSS confirmed 44 records for full-text assessment, 40 title-and-abstract exclusions, and 1 uncertain full-text check. The unassigned author's field remains `not_assigned` on every row.

The live final fields therefore contain 98 `include_for_full_text`, 71 `exclude_at_title_abstract`, and 2 `uncertain_full_text_check` decisions. No adjudication was required. A field-level comparison confirmed that only the assigned-author, final-decision, reason, consensus, and adjudication fields changed.

The 98 includes and 2 uncertain checks form a 100-record full-text queue in `data/full_text_screening.csv`. KLL is assigned 55 records and KSS is assigned 45. Twenty-nine records have audited local full text in `paper_text/`, `TA072` has a verified complete Letter with no separate abstract, and 70 full texts were not retrieved. The queue does not include full-text decision, study-quality assessment, or data-extraction fields because that stage was not completed.

The confirmation workflow is reproduced by `scripts/confirm_title_abstract_recommendations.py`, and the full-text queue is reproduced by `scripts/prepare_full_text_screening.py`.


## Table 2 extraction and study-quality assessment

The completed paper-level extraction is stored in `data/table2_extraction_and_quality_assessment.csv`. It contains exactly the 29 empirical papers in `data/study_inventory.csv` and `data/search_records.csv`, in the same order as manuscript Table 2.

For every paper, the worksheet records the tested front, secondary coverage, reported result or value, DOI evidence link, overall confidence, quality rationale, deployment limitation, and any declared scope exception. All 29 result rows were checked against the active full text before deposition.

The manuscript's study-quality criteria are represented as six worksheet areas:

1. data separation
2. leakage control
3. target-domain access and harmonisation
4. test-independent model, hyperparameter, threshold, or cutoff selection
5. statistical reporting
6. reproducibility and availability of data, code, and methodological details

These ratings are structured qualitative judgments rather than a numerical checklist. The overall confidence rating is not computed by averaging the six areas. A critical flaw such as leakage, test-informed selection, or a contradictory protocol can lower the overall rating. The completed worksheet contains 5 higher-confidence, 16 moderate-confidence, and 8 limited-confidence papers, matching Table 2.

The completed worksheet applies to the separately curated 29-paper evidence base. It does not complete the comparative eligibility assessment of the live 100-record full-text queue.

The command `python3 scripts/validate_table2_assessment.py` verifies that the worksheet contains 29 unique empirical identifiers, matches the inventory and selected-paper metadata, preserves the `8 + 6 + 5 + 10` primary-category arithmetic and the five declared scope exceptions, uses only the allowed assessment labels, and contains no missing required field. When the manuscript source is locally available, the optional `--manuscript` argument additionally checks Table 2 row order, tested fronts, confidence ratings, and numerical tokens.
