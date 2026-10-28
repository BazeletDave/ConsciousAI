# Evidence integrity benchmark engineering

## Scope and current state

This module evaluates evidence publication gate predictions against steward attested human assessments. It does not measure universal AI accuracy, certify factual truth, train a model, or authorize publication. The current four watchlist entries are candidate references, not a reviewed benchmark. TAM 582 materials and private coursework are excluded.

GET `/assurance/review-queue` exports a seed manifest of candidate claims, references, SHA256 evidence digests and next steps. It is not an authenticated annotation application and does not claim to track review activity. GET `/assurance/overview` now recomputes benchmark results if a private dataset is configured; otherwise it shows the unmet review requirement.

## Workflow

1. Expand beyond the seed entries. Collect specific source documents with stable content digests, bounded claims, permission decisions and source retrieval dates. A homepage alone is insufficient evidence.
2. Have the data steward approve permissions, assign two independent nonauthor reviewers, and retain authenticated identities, conflicts, rationales and audit records in an access controlled review system. Follow INDEPENDENT_REVIEW_SOP.md.
3. Separate training from evaluation by case family and shared sources. Freeze the actual prediction artifacts before the reviewers label the holdout. The steward must audit near duplicates and family assignments; software cannot establish these facts from strings.
4. Each reviewer labels whether the evidence meets the publication gate criteria: supported, unsupported or indeterminate. This is a gate eligibility task, not a claim truth task. Disagreement and indeterminate outcomes are excluded and counted. An adjudicated study is a future extension; this evaluator requires agreement by the original two reviewers.
5. After review, the steward approves the completed bundle. Run the CLI below. Inspect confusion matrix, majority baseline, error cases and the Wilson accuracy interval. Thirty binary labeled examples and both classes are minimum computational requirements, not proof of adequate statistical power or representativeness.
6. Mount the reviewed dataset privately and set `ASSURANCE_EVALUATION_DATASET` to its absolute path. The dashboard receives aggregate results only. Do not commit reviewer records, private evidence, personal information or restricted sources to this public repository.

## Dataset contract

Top level fields: schema_version `1.0`, task `evidence_publication_gate`, data_origin `independently_reviewed_real_evidence`, model_version, dataset_version, nonempty author_ids, training_case_families, predictions_frozen_at, steward_approval and records.

steward_approval contains rights_cleared=true, holdout_locked=true, review_system_reference and approved_at. Times must contain timezones. Approval must follow the freeze and every review.

Each record contains record_id, case_family, holdout=true, evidence (claim and sources with document references), evidence_digest (`assurance_engine.canonical_hash(evidence)`), boolean prediction, predicted_at, optional probability in [0,1], and exactly two reviews. Each review contains reviewer_id, independence_attested=true, label, rationale, audit_reference, reviewed_at and evidence_digest. Predictions precede the freeze; reviews follow it. Evidence hashes bind reviews to exact evidence objects. Source document content hashes must be included in those evidence objects and checked by the steward against retained artifacts.

The software enforces structural checks and attested reviewer separation. It does not authenticate reviewers, verify rights, independently establish ground truth, prove that predictions were actually frozen, or detect semantically related cases assigned different family names. Public results explicitly identify these limitations.

## Reproduction

```bash
python3 assurance_benchmark.py /private/reviewed-holdout.json --output /private/benchmark-summary.json
python3 -m unittest test_assurance_benchmark -v
```

The CLI refuses invalid bundles. The service suppresses metrics when a configured file is missing or invalid. No private rows, reviewer identities, audit references or filesystem paths appear in the public report. Model and dataset version identifiers must be suitable for public disclosure.

Classification metrics are accuracy, precision, recall, false positive rate and false negative rate. Undefined denominators remain null. Brier score requires probabilistic predictions for every scored record. No probability is fabricated from a binary decision. Drift and bias remain null until separate valid studies exist. Recomputing a report is evaluation, not continuous model learning.

Synthetic unit fixtures verify known results and rejection paths only. They are never loaded into the dashboard or presented as an independently reviewed real benchmark.
