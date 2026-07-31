#!/usr/bin/env python3
"""Create the full-text screening worksheet from confirmed title screening."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "title_abstract_screening.csv"
OUTPUT = ROOT / "data" / "full_text_screening.csv"

OUTPUT_FIELDS = [
    "full_text_row_id",
    "screening_row_id",
    "source_record_id",
    "title",
    "authors",
    "year",
    "doi",
    "url",
    "record_type",
    "venue",
    "title_abstract_final_decision",
    "title_abstract_final_reason",
    "title_abstract_reviewer",
    "agent_eligibility_signals",
    "assigned_reviewer",
]


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing worksheet: {OUTPUT}")

    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 171:
        raise ValueError(f"Expected 171 title-and-abstract rows, found {len(rows)}")

    advanced = [
        row
        for row in rows
        if row["final_title_abstract_decision"]
        in {"include_for_full_text", "uncertain_full_text_check"}
    ]
    if len(advanced) != 100:
        raise ValueError(f"Expected 100 full-text records, found {len(advanced)}")

    if Counter(row["final_title_abstract_decision"] for row in advanced) != Counter(
        {"include_for_full_text": 98, "uncertain_full_text_check": 2}
    ):
        raise ValueError("Unexpected title-and-abstract disposition counts")

    local_count = sum(
        1 for row in advanced if row["abstract_source_url"].startswith("local:paper_text/")
    )
    letter_count = sum(1 for row in advanced if row["screening_row_id"] == "TA072")
    not_local_count = 100 - local_count - letter_count
    if (local_count, letter_count, not_local_count) != (29, 1, 70):
        raise ValueError(
            f"Unexpected full-text access counts: "
            f"local={local_count}, letter={letter_count}, not_local={not_local_count}"
        )

    output_rows: list[dict[str, str]] = []
    for number, row in enumerate(advanced, start=1):
        reviewer = row["assigned_reviewer"]
        if reviewer not in {"KLL", "KSS"}:
            raise ValueError(f"Unexpected reviewer on {row['screening_row_id']}")

        output_rows.append(
            {
                "full_text_row_id": f"FT{number:03d}",
                "screening_row_id": row["screening_row_id"],
                "source_record_id": row["source_record_id"],
                "title": row["title"],
                "authors": row["authors"],
                "year": row["year"],
                "doi": row["doi"],
                "url": row["url"],
                "record_type": row["record_type"],
                "venue": row["venue"],
                "title_abstract_final_decision": row[
                    "final_title_abstract_decision"
                ],
                "title_abstract_final_reason": row["final_exclusion_reason"],
                "title_abstract_reviewer": reviewer,
                "agent_eligibility_signals": row["agent_eligibility_signals"],
                "assigned_reviewer": reviewer,
            }
        )

    with OUTPUT.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Created {OUTPUT}")
    print(f"records={len(output_rows)}")
    print(f"reviewers={dict(Counter(row['assigned_reviewer'] for row in output_rows))}")
    print(f"full_text_counts=local:{local_count}, letter:{letter_count}, not_local:{not_local_count}")


if __name__ == "__main__":
    main()
