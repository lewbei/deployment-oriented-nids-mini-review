#!/usr/bin/env python3
"""Validate the deposited Table 2 extraction and quality-assessment matrix."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "data" / "table2_extraction_and_quality_assessment.csv"
INVENTORY = ROOT / "data" / "study_inventory.csv"
SEARCH_RECORDS = ROOT / "data" / "search_records.csv"

RATING_FIELDS = (
    "data_separation_rating",
    "leakage_control_rating",
    "target_access_and_harmonization_rating",
    "selection_independence_rating",
    "statistical_reporting_rating",
    "reproducibility_rating",
)

ALLOWED_RATINGS = {"clear", "partial", "unclear", "not_applicable"}
EXPECTED_GROUPS = {
    "cross-dataset generalization": 8,
    "open-set recognition": 6,
    "reliability": 5,
    "deployment adaptation or realism": 10,
}
EXPECTED_CONFIDENCE = {"higher": 5, "moderate": 16, "limited": 8}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def numeric_tokens(value: str) -> list[str]:
    value = value.replace("--", "-")
    return re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", value)


def manuscript_rows(path: Path) -> list[tuple[str, str, str, str]]:
    source = path.read_text(encoding="utf-8")
    start = source.index(r"\label{tab:representative-studies}")
    end = source.index(r"\end{longtable}", start)
    block = source[start:end]
    pattern = re.compile(
        r"\\cite\{(R\d+)\}\s*&\s*(.*?)\s*&\s*(.*?)\s*&\s*"
        r"((?:Higher|Moderate|Limited) confidence\.\\newline\s*.*?)\s*\\\\"
    )
    return [match.groups() for match in pattern.finditer(block)]


def validate_optional_manuscript(
    assessment_rows: list[dict[str, str]], manuscript: Path
) -> None:
    rows = manuscript_rows(manuscript)
    require(len(rows) == 29, f"{manuscript} contains {len(rows)} parsed Table 2 rows")
    require(
        [row[0] for row in rows] == [row["record_id"] for row in assessment_rows],
        "manuscript Table 2 order does not match the deposited matrix",
    )

    for manuscript_row, assessment_row in zip(rows, assessment_rows, strict=True):
        record_id, result, front, quality = manuscript_row
        require(
            front.strip() == assessment_row["front_tested"],
            f"{record_id} front-tested field differs from the manuscript",
        )
        confidence = quality.split(" confidence.", 1)[0].lower()
        require(
            confidence == assessment_row["overall_confidence"],
            f"{record_id} confidence differs from the manuscript",
        )
        require(
            numeric_tokens(result)
            == numeric_tokens(assessment_row["reported_result_or_value"]),
            f"{record_id} extracted numerical tokens differ from the manuscript",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manuscript",
        type=Path,
        help="Optional manuscript source used to verify Table 2 row order, fronts, confidence, and numbers.",
    )
    args = parser.parse_args()

    assessment_rows = read_csv(ASSESSMENT)
    inventory_rows = read_csv(INVENTORY)
    search_rows = read_csv(SEARCH_RECORDS)

    require(len(assessment_rows) == 29, "assessment matrix must contain 29 rows")
    require(
        [int(row["row_order"]) for row in assessment_rows] == list(range(1, 30)),
        "row_order must be the consecutive range 1 through 29",
    )
    require(
        len({row["record_id"] for row in assessment_rows}) == 29,
        "record_id values must be unique",
    )

    empirical_inventory = {
        row["record_id"]: row
        for row in inventory_rows
        if row["review_role"] == "empirical"
    }
    search_by_id = {row["record_id"]: row for row in search_rows}
    assessment_ids = {row["record_id"] for row in assessment_rows}

    require(
        assessment_ids == set(empirical_inventory),
        "assessment IDs do not equal the 29 empirical inventory IDs",
    )
    require(
        assessment_ids == set(search_by_id),
        "assessment IDs do not equal the 29 selected search-record IDs",
    )

    allowed_empty = {"scope_exception"}
    for row in assessment_rows:
        record_id = row["record_id"]
        for field, value in row.items():
            require(
                field in allowed_empty or bool(value.strip()),
                f"{record_id} has an empty required field: {field}",
            )
        for field in RATING_FIELDS:
            require(
                row[field] in ALLOWED_RATINGS,
                f"{record_id} has an invalid {field}: {row[field]}",
            )

        inventory = empirical_inventory[record_id]
        search = search_by_id[record_id]
        for field in ("year", "title", "doi"):
            require(
                row[field] == inventory[field],
                f"{record_id} {field} differs from study_inventory.csv",
            )
        require(
            row["primary_group"] == inventory["primary_group"],
            f"{record_id} primary_group differs from study_inventory.csv",
        )
        require(
            row["primary_group"] == search["primary_selection_group"],
            f"{record_id} primary_group differs from search_records.csv",
        )
        require(
            row["scope_exception"] == search["scope_exception"],
            f"{record_id} scope_exception differs from search_records.csv",
        )
        require(
            row["evidence_url"] == f"https://doi.org/{row['doi']}",
            f"{record_id} evidence_url is not its DOI URL",
        )
        require(
            row["verification_status"] == "full_text_verified",
            f"{record_id} is not marked full_text_verified",
        )

    require(
        Counter(row["primary_group"] for row in assessment_rows) == EXPECTED_GROUPS,
        "primary-group arithmetic does not equal 8 + 6 + 5 + 10",
    )
    require(
        Counter(row["overall_confidence"] for row in assessment_rows)
        == EXPECTED_CONFIDENCE,
        "confidence arithmetic does not equal 5 higher + 16 moderate + 8 limited",
    )

    if args.manuscript:
        validate_optional_manuscript(assessment_rows, args.manuscript.resolve())

    print("validated_rows=29")
    print(f"primary_groups={dict(EXPECTED_GROUPS)}")
    print(f"overall_confidence={dict(EXPECTED_CONFIDENCE)}")
    print("status=ok")


if __name__ == "__main__":
    main()
