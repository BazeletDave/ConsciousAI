# GRI staging backup security and release gate

Staging only. Do not merge to production before CI passes and the data-handling owner approves.

1. Run `python -m pip install cryptography` and `python -m unittest discover -s research_tools -p 'test_*.py' -v` from repository root.
2. Export a restricted candidate ledger with `python research_tools/storage_portability.py export --db /secure/evidence.sqlite --output /secure/restricted.json`.
3. Generate a random 32-byte encryption key with an approved secret manager. Set `GRI_BACKUP_KEY_HEX` as a protected secret, **never commit it**.
4. Encrypt with `python research_tools/encrypted_backup.py encrypt --source /secure/restricted.json --destination /secure/restricted.json.enc`.
5. Transfer ciphertext to an **independently controlled** private offsite storage account. Verify object retention, access controls, versioning, deletion policy, and restore permissions. This repository does **not** configure or claim an offsite backup.
6. On a separate recovery machine, retrieve ciphertext, decrypt with the separately retained key, verify the exported JSON and SHA-256 manifest, and test restoration into a clean staging database. Document recovery timing and reviewer.
7. Remove plaintext staging exports under the approved retention schedule. Never place restricted exports, keys, or identifiable participants in public GitHub or Actions artifacts.

**Free Render PostgreSQL:** This utility does not back up PostgreSQL. An authorized PostgreSQL logical export and an independently stored encrypted copy are still required before the free instance expires. No production writes, secrets, external connections, or billable resources are configured by this change.
