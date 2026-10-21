# PHP2Shell | Technical evidence and institutional impact

**Grand Research Institute | Research case | 21 October 2026**

## Research question
How do memory safety failures in a shared runtime propagate into cross-sector exposure, and how quickly can institutions identify, patch and verify their dependent systems?

## 1. How it happened
The PHP security advisory describes two distinct defects:
* **CVE-2026-109618:** Out of memory handling interrupts partially initialized request data; cleanup can then operate on invalid internal data.
* **CVE-2026-109619:** Request-owned global state outlives its backing allocation; a later request in a reused worker can encounter stale state.

Both are reported as potentially enabling unauthenticated remote code execution. This is a runtime problem, not proof of a flaw in any specific WordPress plugin or website. Review original upstream fixes and regression tests before claiming a particular changed line caused an exploit.

## 2. What happened
On 21 October 2026 PHP published security releases 8.5.12, 8.4.27, 8.3.36 and 8.2.35. Public reporting documented precautionary service outages. Disclosure, attempted exploitation, confirmed exploitation and confirmed compromise are **different evidence categories**.

## 3. What it impacts
Potential outcomes include server-side code execution, confidentiality loss, integrity loss and service interruption. Exploitability depends on runtime and deployment conditions. PHP advises that all web-serving PHP installations be reviewed, including PHP-FPM, mod_php, php-cgi, FrankenPHP and LiteSpeed.

## 4. Where it impacts: evidence matrix
| System or organization | Relationship | Evidence classification | Required follow-up |
| --- | --- | --- | --- |
| PHP core | Vulnerable runtime | Vendor-confirmed vulnerability | Compare upstream fix commits and tests |
| WordPress / Drupal / Joomla | Applications commonly deployed on PHP | Potential dependent exposure; **not proof of vendor compromise** | Inventory hosting PHP and patch provenance |
| Apache mod_php / PHP-FPM / LiteSpeed | PHP execution environments | Vendor-identified deployment surfaces | Identify runtime package and worker restart |
| WordPress.com / WordPress VIP / WP Cloud / Pressable / Tumblr | Managed hosting | Operator reports protection as of 21 October | Verify operator statement and coverage |
| Government and public services | Dependent service operators | Precautionary outages reported by Reuters | Document named institution, date and restoration |
| GRI infrastructure | Research target | **Not audited in this case** | Inventory services, container images, runtime versions and evidence |

## 5. Where we go from here
1. Inventory direct and embedded PHP runtimes, including containers and managed hosting.
2. Prioritize internet-facing systems and apply vendor-fixed releases or supported vendor backports.
3. Restart affected workers and verify active runtime, not only installed package metadata.
4. Record the advisory, asset owner, remediation decision, patch timestamp, validation evidence and remaining exceptions.
5. Analyze **discovery → disclosure → authorization → remediation → verification** intervals as indicators of institutional adaptation.
6. Compare defensive AI code review capabilities with the verification, oversight and misuse risks of automated vulnerability research.

## Safe executable example
Run `python3 php_runtime_inventory.py inventory.json` with an explicitly prepared, authorized inventory. The script performs **offline** version triage only: no network probing, exploitation or credential access. Version labels are screening aids, not a substitute for vendor backport advisories.

Example input:
```json
{"assets":[{"name":"public-web-1","php_version":"8.3.35","internet_facing":true,"vendor_backport_verified":false},{"name":"managed-service","php_version":"8.3.35","internet_facing":true,"vendor_backport_verified":true}]}
```

## Primary evidence
* PHP vendor security announcements: https://www.php.net/
* Dutch National Cyber Security Centre operational record: https://github.com/NCSC-NL/php2shell
* Canadian Centre for Cyber Security: https://www.cyber.gc.ca/en/alerts-advisories/al26-026-critical-vulnerabilities-impacting-php-cve-2026-109618-cve-2026-109619
* Automattic operator statement: https://automattic.com/2026/10/21/your-sites-are-protected-against-the-php2shell-vulnerabilities/
* Reuters contemporaneous reporting: https://www.reuters.com/technology/websites-taken-offline-over-php-risks-2026-10-21/

**Research integrity:** This is an evidence-oriented research case, not an incident response certification, compromise attribution, or completed source code audit. No exploit payloads are included.
