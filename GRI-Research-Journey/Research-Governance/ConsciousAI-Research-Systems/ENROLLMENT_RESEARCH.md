# Enrollment research dashboard connection

The dashboard panel at /dashboard#enrollment-research consumes GET /intelligence/enrollment-research?q=identity&country=USA. It displays a curated incident and three primary institutional references. Coverage is initially United States only. Records distinguish an attributed classroom account from institutional mechanism and policy references; reference counts are not incident counts.

A standard library TF IDF index is fitted to three GRI authored institutional summaries. Queries use cosine similarity with matching terms shown for inspection. This is statistical document retrieval, not semantic understanding, a fraud classifier, a calibrated confidence score, or an independently evaluated predictive model. The classroom report is excluded from fitting. Corpus digests identify the exact indexed title and summary version. Precision and recall remain null until independently reviewed evaluation queries exist.

To extend coverage, review a primary source, add a uniquely identified record to enrollment_research.json, preserve dates, country, attribution and unknowns, and run python -m unittest test_enrollment_research -v. Only reviewed institutional references may set retrieval_eligible=true. Participant material, personal data and model training remain excluded. A new checked in corpus is indexed on the next request, so approved corpus updates flow through the existing deployment path without an autonomous model promotion or new collection schedule.

No automatic global collector or individual student investigation is enabled. Existing source schedules and enforcement controls are unchanged. Run the full service suite with python -m unittest discover -v before release.
