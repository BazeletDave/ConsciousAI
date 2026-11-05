# Data lifecycle and consent gate

Grand Research Institute | Offline research controls | November 2026

This prototype processes **synthetic local files only** for the public demonstration. The presence of a consent flag in a JSON record is **not proof of legally or ethically valid consent**. Real participant ingestion is disabled by governance policy until a private consent registry, identity verification, retention schedule, withdrawal procedure, access controls, encryption and any applicable ethics review have been independently approved.

## Export and deletion

Local JSON files are controlled by the researcher who holds them. The CLI supports writing derived, nonidentifying outputs with `--output`; the original file is never altered by the program. To withdraw a local record from a privately held research dataset, the custodian must remove it and its derivatives, record a withdrawal event in a separately protected audit log, and apply the approved retention and backup deletion policy. No remote collection, storage, account creation, deletion endpoint or participant export portal is implemented. Do not represent this document as an operational consent registry.

## Publication and privacy

Never commit personal trip histories, passenger data, credentials, precise private locations or participant consent evidence to this public repository. Test files are clearly synthetic. Data minimization, provenance and explicit event state are prerequisites, not substitutes for authorization. Forecast outputs are uncalibrated illustrative baselines.
