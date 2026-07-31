#!/usr/bin/env python3
"""Record author confirmation of the advisory title-and-abstract decisions."""

from __future__ import annotations

import csv
import os
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSHEET = ROOT / "data" / "title_abstract_screening.csv"
CONFIRMATION_LABEL = "author_confirmed"

VALID_RECOMMENDATIONS = {
    "include_for_full_text",
    "exclude_at_title_abstract",
    "uncertain_full_text_check",
}

EXPECTED_RECOMMENDATION_COUNTS = Counter(
    {
        "include_for_full_text": 98,
        "exclude_at_title_abstract": 71,
        "uncertain_full_text_check": 2,
    }
)

AUTHOR_FIELDS = {
    "KLL": {
        "decision": "kll_title_abstract_decision",
        "reason": "kll_exclusion_reason",
        "notes": "kll_notes",
        "other_decision": "kss_title_abstract_decision",
        "expected_rows": 86,
    },
    "KSS": {
        "decision": "kss_title_abstract_decision",
        "reason": "kss_exclusion_reason",
        "notes": "kss_notes",
        "other_decision": "kll_title_abstract_decision",
        "expected_rows": 85,
    },
}


def main() -> None:
    with WORKSHEET.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if len(rows) != 171:
        raise ValueError(f"Expected 171 rows, found {len(rows)}")

    recommendation_counts = Counter(
        row["agent_title_abstract_recommendation"] for row in rows
    )
    if recommendation_counts != EXPECTED_RECOMMENDATION_COUNTS:
        raise ValueError(
            "Unexpected advisory counts: "
            f"{dict(recommendation_counts)}"
        )

    if not all(
        row["agent_title_abstract_recommendation"] in VALID_RECOMMENDATIONS
        for row in rows
    ):
        raise ValueError("The worksheet contains an unknown advisory recommendation")

    for reviewer, fields in AUTHOR_FIELDS.items():
        assigned_rows = [
            row for row in rows if row["assigned_reviewer"] == reviewer
        ]
        if len(assigned_rows) != fields["expected_rows"]:
            raise ValueError(
                f"{reviewer} has {len(assigned_rows)} assigned rows, "
                f"expected {fields['expected_rows']}"
            )
        if not all(row[fields["decision"]] == "" for row in assigned_rows):
            raise ValueError(f"{reviewer} has a non-empty assigned decision")
        if not all(
            row[fields["other_decision"]] == "not_assigned"
            for row in assigned_rows
        ):
            raise ValueError(f"{reviewer} has an unexpected unassigned-author value")

    if not all(row["final_title_abstract_decision"] == "" for row in rows):
        raise ValueError("A final title-and-abstract decision is already populated")

    protected_fields = [
        field
        for field in fieldnames
        if field
        not in {
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
        }
    ]
    protected_snapshot = [
        (
            row["screening_row_id"],
            tuple(row[field] for field in protected_fields),
        )
        for row in rows
    ]

    for row in rows:
        reviewer = row["assigned_reviewer"]
        fields = AUTHOR_FIELDS[reviewer]
        recommendation = row["agent_title_abstract_recommendation"]
        reason = row["agent_exclusion_reason"]

        if recommendation == "include_for_full_text" and reason:
            raise ValueError(
                f"{row['screening_row_id']} has an exclusion reason despite inclusion"
            )
        if recommendation != "include_for_full_text" and not reason:
            raise ValueError(
                f"{row['screening_row_id']} lacks a reason for a non-include decision"
            )

        row[fields["decision"]] = recommendation
        row[fields["reason"]] = reason
        row[fields["notes"]] = (
            f"{reviewer} confirmed the advisory recommendation."
        )
        row["final_title_abstract_decision"] = recommendation
        row["final_exclusion_reason"] = reason
        row["consensus_reason"] = (
            "authors_confirmed_assigned_recommendations"
        )
        row["adjudication_status"] = "not_required_author_confirmation"

    current_protected_snapshot = [
        (
            row["screening_row_id"],
            tuple(row[field] for field in protected_fields),
        )
        for row in rows
    ]
    if current_protected_snapshot != protected_snapshot:
        raise ValueError("A protected metadata or advisory field changed")

    temporary = WORKSHEET.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, WORKSHEET)

    print(f"Updated {WORKSHEET}")
    for reviewer, fields in AUTHOR_FIELDS.items():
        counts = Counter(
            row[fields["decision"]]
            for row in rows
            if row["assigned_reviewer"] == reviewer
        )
        print(f"{reviewer}: {dict(counts)}")
    print(f"Final: {dict(recommendation_counts)}")


if __name__ == "__main__":
    main()
