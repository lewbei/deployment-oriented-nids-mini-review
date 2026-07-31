#!/usr/bin/env python3
"""Add agent-only title-and-abstract screening recommendations.

The author decision, consensus, and adjudication fields are deliberately left
unchanged. The row-level mapping is fixed so that the recommendation pass can
be audited and reproduced.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSHEET = ROOT / "data" / "title_abstract_screening.csv"

AGENT_FIELDS = [
    "agent_title_abstract_recommendation",
    "agent_eligibility_signals",
    "agent_exclusion_reason",
    "agent_notes",
    "agent_screening_basis",
]


def ids(numbers: list[int]) -> set[str]:
    return {f"TA{number:03d}" for number in numbers}


INCLUDE = ids(
    [
        4, 5, 8, 9, 10, 13, 15, 16, 17, 18, 19, 22, 23, 24, 28, 30, 31,
        33, 34, 36, 37, 39, 40, 42, 43, 44, 45, 48, 49, 51, 53, 54, 55,
        56, 57, 59, 65, 66, 68, 69, 70, 71, 72, 73, 75, 76, 77, 79, 80,
        81, 85, 87, 89, 90, 91, 92, 94, 96, 97, 99, 105, 106, 109, 110,
        111, 112, 115, 116, 124, 126, 129, 130, 131, 133, 134, 135, 136,
        137, 138, 139, 143, 145, 146, 147, 149, 150, 151, 154, 155, 156,
        157, 159, 161, 162, 165, 166, 168, 169,
    ]
)

UNCERTAIN = ids([152, 167])

REVIEW_OR_CONTEXT = ids(
    [6, 20, 21, 46, 62, 63, 102, 108, 118, 125, 128, 142, 148, 158]
)
OUTSIDE_NIDS = ids([14, 32, 60, 64, 160])
NOT_DL_CENTERED = ids([25])
NOT_FINAL_PEER_REVIEWED = ids(
    [27, 38, 67, 74, 88, 93, 98, 101, 107, 114, 121, 122, 132, 140]
)
RETRACTED = ids([153])
NO_DEPLOYMENT_RELEVANCE = ids(
    [
        1, 2, 3, 7, 11, 12, 26, 29, 35, 41, 47, 50, 52, 58, 61, 78,
        82, 83, 84, 86, 95, 100, 103, 104, 113, 117, 119, 120, 123,
        127, 141, 144, 163, 164, 170, 171,
    ]
)

EXCLUSION_GROUPS = {
    "review_or_context_only": REVIEW_OR_CONTEXT,
    "outside_nids": OUTSIDE_NIDS,
    "not_deep_learning_centered": NOT_DL_CENTERED,
    "not_final_peer_reviewed_publication": NOT_FINAL_PEER_REVIEWED,
    "retracted_publication": RETRACTED,
    "no_deployment_relevance": NO_DEPLOYMENT_RELEVANCE,
}

CROSS_DATASET = ids(
    [
        4, 9, 13, 15, 16, 19, 28, 33, 43, 45, 48, 51, 53, 65, 68, 69,
        70, 80, 90, 92, 94, 97, 105, 111, 115, 124, 129, 131, 136,
        137, 143, 145, 156, 166, 167, 169,
    ]
)
OPEN_SET = ids(
    [
        5, 8, 10, 15, 23, 24, 30, 31, 34, 37, 39, 40, 43, 44, 45, 54,
        56, 57, 59, 66, 70, 73, 76, 77, 79, 80, 81, 85, 89, 109, 112,
        116, 126, 130, 133, 134, 138, 139, 150, 151, 152, 155, 157,
        159, 161, 162, 168,
    ]
)
RELIABILITY = ids([30, 37, 49, 51, 54, 55, 96, 99, 106, 147, 155, 157, 161])
DEPLOYMENT_ADAPTATION = ids(
    [
        10, 17, 18, 22, 23, 24, 31, 33, 34, 36, 39, 40, 42, 43, 44,
        45, 48, 53, 54, 57, 59, 70, 71, 72, 75, 76, 77, 80, 81, 87,
        91, 92, 94, 105, 110, 115, 116, 124, 130, 135, 138, 146, 149,
        154, 162, 165, 166,
    ]
)

SIGNAL_GROUPS = [
    ("cross_dataset_or_domain_shift", CROSS_DATASET),
    ("open_set_or_unseen_attack", OPEN_SET),
    ("calibration_uncertainty_ood_or_confidence", RELIABILITY),
    ("deployment_adaptation_or_realism", DEPLOYMENT_ADAPTATION),
]

INCLUDE_NOTE = (
    "Advance because the title and abstract provide an explicit deployment-front "
    "signal recorded in agent_eligibility_signals. Eligibility and evidence quality "
    "still require full-text confirmation."
)

EXCLUSION_NOTES = {
    "review_or_context_only": (
        "This is a review, survey, or broad context article rather than an eligible "
        "primary empirical study. It may be considered separately for background."
    ),
    "outside_nids": (
        "The title and abstract concern broader cybersecurity, wireless "
        "communications, encryption, malware, or fault diagnosis rather than an "
        "eligible deep-learning network intrusion or network-anomaly study."
    ),
    "not_deep_learning_centered": (
        "The proposed primary method is not deep-learning-centered, so it does not "
        "meet the model-scope criterion."
    ),
    "not_final_peer_reviewed_publication": (
        "The retrieved record is a preprint, SSRN item, repository work, or other "
        "record without a verified final peer-reviewed publication."
    ),
    "retracted_publication": (
        "The record is explicitly marked as retracted and cannot enter the empirical "
        "evidence base."
    ),
    "no_deployment_relevance": (
        "The record proposes or compares a NIDS model on benchmark data, but the "
        "title and abstract do not report cross-dataset or domain-shift evaluation, "
        "a defined open-set or unseen-attack protocol, calibration or uncertainty "
        "assessment, or a concrete deployment-adaptation test."
    ),
}

NOTE_OVERRIDES = {
    "TA007": (
        "The abstract uses broad robustness and uncertainty language, but reports "
        "only a CIC-IoT-2023 model evaluation and no distinct deployment-front "
        "protocol."
    ),
    "TA011": (
        "Emerging attacks motivate the study, but the abstract does not describe a "
        "held-out unknown-class, open-set, cross-dataset, or reliability protocol."
    ),
    "TA070": (
        "Advance on relevance because the abstract reports cross-dataset testing and "
        "a live enterprise deployment. The unusually strong operational claims need "
        "source and study-quality verification at full text."
    ),
    "TA072": (
        "Advance on deployment realism because the verified full-text Letter studies "
        "deep NIDS learning under noisy labels. The publication has no separate "
        "abstract."
    ),
    "TA084": (
        "Zero-day attacks appear only as motivation. The reported experiment uses "
        "CIC-IDS2017 and does not describe a held-out unknown-class or open-set "
        "evaluation."
    ),
    "TA086": (
        "The abstract claims performance on sophisticated and zero-day threats, but "
        "reports a CICIDS2017 architecture comparison without a defined unseen-class "
        "or deployment-front protocol."
    ),
    "TA100": (
        "The models are evaluated separately on three benchmark datasets. The "
        "abstract does not report training on one dataset and testing on another."
    ),
    "TA104": (
        "The abstract reports a hybrid model on one benchmark and uses broad "
        "adaptability language, but does not evaluate a defined deployment front."
    ),
    "TA123": (
        "Near-real-time use is asserted from a single CSE-CIC-IDS2018 experiment, "
        "without a deployment, cross-dataset, open-set, or reliability assessment."
    ),
    "TA152": (
        "The available abstract field is only a truncated source snippet. The title "
        "and snippet suggest unknown or zero-day IoT intrusion detection, so the full "
        "text is needed before an eligibility decision."
    ),
    "TA161": (
        "Advance on relevance because the abstract specifies uncertainty-based "
        "zero-day anomaly detection and deployment considerations. Venue and "
        "study-quality evidence still require full-text assessment."
    ),
    "TA164": (
        "New and unanticipated attacks are used as general motivation, but the "
        "reported study is a single-dataset CNN performance evaluation without a "
        "defined unseen-class protocol."
    ),
    "TA167": (
        "The abstract is directly relevant to cross-dataset deep NIDS evaluation, "
        "but the record has no venue or DOI and is sourced only from ResearchGate. "
        "Full text and final peer-reviewed publication status must be verified."
    ),
}

FIXED_EMPIRICAL_ROWS = ids(
    [
        9, 13, 16, 17, 19, 24, 30, 37, 43, 49, 51, 56, 79, 80, 85, 90,
        91, 92, 96, 99, 129, 131, 133, 139, 147, 149, 151, 166, 169,
    ]
)


def exclusion_reason(row_id: str) -> str:
    matches = [reason for reason, members in EXCLUSION_GROUPS.items() if row_id in members]
    if len(matches) != 1:
        raise ValueError(f"{row_id} has {len(matches)} exclusion reasons: {matches}")
    return matches[0]


def eligibility_signals(row_id: str) -> str:
    signals = [label for label, members in SIGNAL_GROUPS if row_id in members]
    return ";".join(signals)


def main() -> None:
    with WORKSHEET.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        original_fields = list(reader.fieldnames or [])
        rows = list(reader)

    if len(rows) != 171:
        raise ValueError(f"Expected 171 screening rows, found {len(rows)}")

    row_ids = {row["screening_row_id"] for row in rows}
    excluded = set().union(*EXCLUSION_GROUPS.values())
    classified = INCLUDE | UNCERTAIN | excluded
    if classified != row_ids:
        missing = sorted(row_ids - classified)
        extra = sorted(classified - row_ids)
        raise ValueError(f"Classification mismatch; missing={missing}, extra={extra}")

    if INCLUDE & UNCERTAIN or INCLUDE & excluded or UNCERTAIN & excluded:
        raise ValueError("Recommendation groups overlap")
    if not FIXED_EMPIRICAL_ROWS <= INCLUDE:
        raise ValueError("A known empirical manuscript paper was not advanced")

    author_fields = [
        "assigned_reviewer",
        "kll_title_abstract_decision",
        "kll_exclusion_reason",
        "kll_notes",
        "kss_title_abstract_decision",
        "kss_exclusion_reason",
        "kss_notes",
        "final_title_abstract_decision",
        "final_exclusion_reason",
        "consensus_reason",
        "adjudication_status",
    ]
    author_snapshot = [
        (row["screening_row_id"], tuple(row[field] for field in author_fields))
        for row in rows
    ]

    for row in rows:
        row_id = row["screening_row_id"]
        signals = eligibility_signals(row_id)

        if row_id in INCLUDE:
            if not signals:
                raise ValueError(f"{row_id} is advanced without an eligibility signal")
            recommendation = "include_for_full_text"
            reason = ""
            note = INCLUDE_NOTE
        elif row_id in UNCERTAIN:
            if not signals:
                raise ValueError(f"{row_id} is uncertain without an eligibility signal")
            recommendation = "uncertain_full_text_check"
            reason = "insufficient_information"
            note = "Full text is required before a defensible eligibility decision."
        else:
            recommendation = "exclude_at_title_abstract"
            reason = exclusion_reason(row_id)
            note = EXCLUSION_NOTES[reason]
            signals = ""

        row["agent_title_abstract_recommendation"] = recommendation
        row["agent_eligibility_signals"] = signals
        row["agent_exclusion_reason"] = reason
        row["agent_notes"] = NOTE_OVERRIDES.get(row_id, note)
        row["agent_screening_basis"] = (
            "title_and_verified_full_text_letter"
            if row_id == "TA072"
            else (
                "title_and_partial_source_snippet"
                if row_id == "TA152"
                else "title_and_abstract"
            )
        )

    current_author_snapshot = [
        (row["screening_row_id"], tuple(row[field] for field in author_fields))
        for row in rows
    ]
    if current_author_snapshot != author_snapshot:
        raise ValueError("An author, consensus, or adjudication field changed")

    output_fields = [field for field in original_fields if field not in AGENT_FIELDS]
    insert_at = output_fields.index("assigned_reviewer")
    output_fields[insert_at:insert_at] = AGENT_FIELDS

    temporary = WORKSHEET.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, WORKSHEET)

    print(f"Updated {WORKSHEET}")
    print(f"include_for_full_text={len(INCLUDE)}")
    print(f"uncertain_full_text_check={len(UNCERTAIN)}")
    print(f"exclude_at_title_abstract={len(excluded)}")


if __name__ == "__main__":
    main()
