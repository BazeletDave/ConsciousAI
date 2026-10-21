# PHP2Shell | Patch provenance and institutional timeline dataset

This dataset complements [the executable PHP case study](php_case_study.py) and [source to platform mapping](SOURCE_TO_PLATFORM_EVIDENCE.md).

[Download the machine readable research register](patch_and_institutional_evidence.json).

## Research protocol
The supplied October 21 code proposed specific modified C functions, PHPT regression test paths, advisory identifiers, and five exact UTC timestamps. These are **claims awaiting primary-source verification**, not source confirmed facts. No commit hashes, source diffs, PHPT files, CAB minutes or institution specific incident records were supplied to substantiate them.

The dataset therefore retains candidate functions and test paths as **claimed** fields, with null provenance links and explicit verification status. It intentionally does **not** publish the proposed 10:00, 12:00, 13:30, 14:15 or 16:00 UTC times as observed events.

## Technical audit steps
1. Locate each advisory in the upstream `php/php-src` security records.
2. Identify patch commits by release branch and compare parent and fixed revisions.
3. Confirm modified function names directly from the diff.
4. Link actual PHPT regression tests and verify what each asserts.
5. Identify independent deployment-specific exploit prerequisites; avoid treating potential WAF bypass or cross-tenant effects as demonstrated.

## Institutional impact steps
1. Obtain each operator's dated public notice.
2. Record distinct discovery, disclosure, authorization, deployment and verification timestamps.
3. Classify direct operator evidence separately from secondary reporting and hypotheses.
4. Compute remediation latency **only** for institutions with complete, attributable timestamps.
5. Apply the Nelson Model to explain variation in rules, actors, interests, power, options, commitments and adaptation.

## Security and research limits
This is a provenance register, not an exploit demonstration, vulnerability confirmation for any particular asset, or an audited real-world incident timeline. No invented container digests, change tickets, asset owners or patch success claims are used.
