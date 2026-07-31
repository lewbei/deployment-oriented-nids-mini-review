#!/usr/bin/env python3
"""Add full-text-verified inclusion rationales to the 29-paper corpus."""

from __future__ import annotations

import csv
import os
from collections import Counter
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
REPOSITORY = Path(__file__).resolve().parents[1]
CORPUS = REPOSITORY / "data" / "search_records.csv"
INVENTORY = REPOSITORY / "data" / "study_inventory.csv"

RATIONALE_FIELDS = [
    "primary_selection_group",
    "full_text_inclusion_reason",
    "selection_boundary",
    "scope_exception",
    "selection_evidence_source",
]

RATIONALES = {
    "R1": (
        "cross-dataset generalization",
        "Direct empirical evidence that strong within-dataset NIDS results can collapse when training and testing use different network datasets.",
        "The evaluated classifiers are conventional machine-learning models, so this paper is retained as a cross-dataset benchmark anchor rather than as deep-model performance evidence.",
        "non_dl_empirical_benchmark",
    ),
    "R2": (
        "reliability",
        "Evaluates uncertainty-aware NIDS, including a Bayesian neural model, for overconfidence, out-of-distribution traffic, and unknown-class handling.",
        "It is a reliability and OoD anchor, not a cross-dataset deployment study.",
        "",
    ),
    "R4": (
        "cross-dataset generalization",
        "Provides rare joint evidence on Transformer-based cross-dataset NIDS performance and probability calibration.",
        "The study remains closed-set and does not test a complete three-front deployment protocol.",
        "",
    ),
    "R5": (
        "deployment adaptation or realism",
        "Tests LSTM and Transformer federated IDS models under in-domain, cross-dataset, and combined multi-dataset conditions with heterogeneous clients.",
        "The multi-dataset federation uses data from participating environments and is not source-only deployment to an unseen target.",
        "",
    ),
    "R6": (
        "open-set recognition",
        "Implements a genuine multiclass open-set NIDS decision with an explicit suspicious outcome when no known traffic class fits.",
        "The energy-based flow classifier is statistical rather than deep learning, so it is retained as open-set method and comparator evidence.",
        "non_dl_open_set_method_context",
    ),
    "R7": (
        "open-set recognition",
        "Combines unsupervised representation learning with OpenMax-style recognition to detect unknown intrusion traffic rather than forcing every flow into a known class.",
        "Its main evaluation is a within-dataset open-set design rather than cross-dataset deployment.",
        "",
    ),
    "R9": (
        "deployment adaptation or realism",
        "Combines cross-domain stress, adversarial hardening, explainability, federated aggregation, continual replay, and device-oriented evaluation in one IIoT pipeline.",
        "It supports broad deployment realism but does not provide calibration, uncertainty, or abstention evidence.",
        "",
    ),
    "R10": (
        "open-set recognition",
        "Jointly studies open-set unknown-intrusion handling and domain adaptation across heterogeneous IoT tasks.",
        "The method uses target-domain adaptation, so it is not equivalent to source-only deployment on an unseen network.",
        "",
    ),
    "R11": (
        "cross-dataset generalization",
        "Directly evaluates temporal and network-domain shift and shows how IDS performance and benign false alarms change in future-internet transfer settings.",
        "It is an evaluation study with mixed model families and does not test open-set recognition or confidence reliability.",
        "",
    ),
    "R12": (
        "cross-dataset generalization",
        "Provides a verified heterogeneous IoT benchmark for comparing multiple domain-adaptation families, including open-set domain adaptation.",
        "TriHID is an evaluation dataset and protocol resource, not a detector architecture.",
        "evaluation_resource_not_detector",
    ),
    "R13": (
        "reliability",
        "Uses Bayesian deep anomaly detection to separate aleatoric and epistemic uncertainty and evaluates rejection based on uncertainty.",
        "It supports network-anomaly trustworthiness but is not a standard calibrated multiclass NIDS or cross-dataset study.",
        "",
    ),
    "R15": (
        "cross-dataset generalization",
        "Evaluates a deep few-shot cross-domain NIDS using multi-domain fusion and cross-attention under limited labeled data.",
        "The target setting supplies labeled examples and therefore differs from source-only unseen-target generalization.",
        "",
    ),
    "R16": (
        "reliability",
        "Implements a reject option using WisdomNet and Monte Carlo dropout uncertainty so doubtful NIDS predictions can be deferred.",
        "It is abstention evidence on older benchmark settings, not calibration or cross-dataset evidence.",
        "",
    ),
    "R17": (
        "reliability",
        "Evaluates temperature scaling, Monte Carlo dropout, calibration metrics, uncertainty filtering, and out-of-distribution-style attack stress for deep IoT detection.",
        "Its shift evaluation is within the IoT-23 experimental design rather than train-on-one-dataset and test-on-another transfer.",
        "",
    ),
    "R18": (
        "reliability",
        "Combines CNN-LSTM detectors, Monte Carlo dropout, and Bayesian model averaging to produce per-alert predictive uncertainty in SDN intrusion detection.",
        "It is uncertainty-quantification evidence rather than a cross-dataset benchmark or a complete calibration study.",
        "",
    ),
    "R19": (
        "deployment adaptation or realism",
        "Tests class-incremental, network-agnostic NIDS adaptation when benign traffic changes across IoT network environments.",
        "The model updates after deployment and therefore does not represent fixed source-only generalization.",
        "",
    ),
    "R20": (
        "open-set recognition",
        "Extends unknown-sample recognition with constrained-clustering inspection to support analyst follow-up after unknown traffic is detected.",
        "Its value is open-world handling and inspection, not cross-dataset reliability.",
        "",
    ),
    "R21": (
        "cross-dataset generalization",
        "Evaluates multi-source adversarial domain adaptation and category-level alignment for limited-sample IoT intrusion detection.",
        "It relies on source-target adaptation and limited target samples rather than source-only evaluation.",
        "",
    ),
    "R22": (
        "cross-dataset generalization",
        "Evaluates Wasserstein-guided Transformer domain adaptation across multiple NetFlow datasets and many source-target transfer tasks.",
        "It uses unlabeled target data and pseudo-labeling, so it must not be conflated with source-only cross-dataset generalization.",
        "",
    ),
    "R24": (
        "cross-dataset generalization",
        "Aligns heterogeneous source and target feature spaces with explicit feature re-encoding, MMD, and a Transformer ensemble for cross-domain NIDS.",
        "Target-specific feature harmonization and alignment are part of the method, so this is domain adaptation rather than unseen-target deployment.",
        "",
    ),
    "R25": (
        "open-set recognition",
        "Evaluates one model for known-class classification, novel-attack detection, and multiclass novelty detection.",
        "The evidence comes from within-dataset novelty protocols and does not establish cross-network deployment robustness.",
        "",
    ),
    "R26": (
        "deployment adaptation or realism",
        "Studies few-shot class-incremental NIDS adaptation when newly observed attack classes become available with very limited labels.",
        "It requires labeled new-class samples and is continual adaptation rather than open-set rejection.",
        "",
    ),
    "R27": (
        "deployment adaptation or realism",
        "Studies federated transfer of rare and newly observed attack knowledge among clients and rounds in distributed NIDS.",
        "The transfer occurs inside a federated ecosystem and is not a train-on-one-dataset, test-on-another benchmark.",
        "",
    ),
    "R28": (
        "deployment adaptation or realism",
        "Evaluates trustworthy collaborative industrial intrusion detection when federated participants are exposed to poisoning attacks.",
        "Trustworthiness concerns robust aggregation and training integrity, not probability calibration or per-prediction uncertainty.",
        "",
    ),
    "R29": (
        "deployment adaptation or realism",
        "Provides neural-model scalability and multi-dataset feature-stability evidence across CICIDS, MQTT, and ToN-IoT settings.",
        "It does not perform a clean source-trained, target-tested transfer experiment or implement an invariant-learning penalty.",
        "",
    ),
    "R30": (
        "open-set recognition",
        "Uses normal-only semi-supervised deep anomaly detection to identify unknown attacks across benchmark and vehicle-network settings.",
        "It is anomaly-based unknown-attack evidence rather than class-incremental learning or calibrated open-set classification.",
        "",
    ),
    "R31": (
        "deployment adaptation or realism",
        "Evaluates semi-supervised federated deep anomaly detection under non-IID IoT data, partial gateway participation, and network-scale constraints.",
        "It supports deployment realism but does not directly test cross-dataset transfer, open-set recognition, or calibration.",
        "",
    ),
    "R32": (
        "deployment adaptation or realism",
        "Evaluates online drift adaptation, SHAP-based explanations, and low-latency IIoT edge operation on Raspberry Pi hardware, with a deep hybrid comparator.",
        "The primary adaptive ensemble uses lightweight online machine-learning models rather than a deep-learning-centered architecture.",
        "primary_method_not_dl_centered",
    ),
    "R33": (
        "deployment adaptation or realism",
        "Evaluates autonomous attack-candidate extraction and federated sharing across IoT networks to improve handling of emerging attacks.",
        "The proposed IDAC detector is based on Online OC-SVM rather than deep learning and is retained only as deployment-support evidence.",
        "primary_method_not_dl_centered",
    ),
}


def main() -> None:
    with CORPUS.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        original_fields = list(reader.fieldnames or [])
        rows = list(reader)

    if len(rows) != 29:
        raise ValueError(f"Expected 29 empirical records, found {len(rows)}")
    if {row["record_id"] for row in rows} != set(RATIONALES):
        raise ValueError("The live corpus identifiers do not match the rationale map")

    with INVENTORY.open(encoding="utf-8-sig", newline="") as handle:
        inventory = {
            row["record_id"]: row
            for row in csv.DictReader(handle)
            if row["review_role"] == "empirical"
        }
    if set(inventory) != set(RATIONALES):
        raise ValueError("The empirical inventory does not match the rationale map")

    protected_fields = [
        field for field in original_fields if field not in RATIONALE_FIELDS
    ]
    protected_snapshot = [
        (
            row["record_id"],
            tuple(row[field] for field in protected_fields),
        )
        for row in rows
    ]

    for row in rows:
        record_id = row["record_id"]
        group, reason, boundary, exception = RATIONALES[record_id]
        if inventory[record_id]["primary_group"] != group:
            raise ValueError(
                f"{record_id} group mismatch: {group!r} versus "
                f"{inventory[record_id]['primary_group']!r}"
            )
        evidence_path = WORKSPACE / "paper_text" / f"{record_id}.txt"
        if not evidence_path.is_file():
            raise FileNotFoundError(evidence_path)

        row["primary_selection_group"] = group
        row["full_text_inclusion_reason"] = reason
        row["selection_boundary"] = boundary
        row["scope_exception"] = exception
        row["selection_evidence_source"] = f"paper_text/{record_id}.txt"

    current_protected_snapshot = [
        (
            row["record_id"],
            tuple(row[field] for field in protected_fields),
        )
        for row in rows
    ]
    if current_protected_snapshot != protected_snapshot:
        raise ValueError("A pre-existing corpus field changed")

    output_fields = [
        field for field in original_fields if field not in RATIONALE_FIELDS
    ]
    insert_at = output_fields.index("notes")
    output_fields[insert_at:insert_at] = RATIONALE_FIELDS

    temporary = CORPUS.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, CORPUS)

    print(f"Updated {CORPUS}")
    print(
        "groups="
        + str(Counter(row["primary_selection_group"] for row in rows))
    )
    print(
        "scope_exceptions="
        + str(Counter(bool(row["scope_exception"]) for row in rows))
    )


if __name__ == "__main__":
    main()
