PART A DEPLOYMENT PLAN FOR SIEM, DAST, and SAST

Principles
1. Shift left, but verification is done at runtime. SAST and secret scanning catch problems in code. DAST catches them in the running app, and the SIEM catches what gets through to production
2. Start in report only mode, then enforce. Developers adopt tools that are fast and accurate, so noise is turned out before anything blocks a build
3. One feedback loop. Findings from every tool end up where developers and the security team can both see
4. Accounting for AI assisted development. Assistants introduce hallucinated packages, pasted secrets and subtle authorization flaws, so the plan adds checks for each


Tool selection
| Capability | Tool | Reason |
| --- | --- | --- |
| SAST | Semgrep (community rules plus custom AI flaw rules ) | Fast in CI, easy custom rules, low noise |
| Secrets | Gitleaks  (pre commit and CI) plus Github push protection | Catches secrets locally and server-side, including history |
| SCA | pip-audit or depandabot for known CVEs, plus a custom checker for hallucinated packages | Standard SCA misses packages that don't exist |
| DAST | OWASP ZAP API scan driven by the OpenAPI definition, plus a two user authorization test | Free, scriptable, good API support; generic scanners can't detect broken authorization |
| SIEM and detection | AWS (CloudTrail, Route 53 Resolver logs, WAF logs, GuardDuty, Security Hub CSPM, EventBridge) for a lean setup, or WAZUH/ OpenSearch for a full SIEM UI. Rules are written in Sigma so the stay portable | Low cost, integrated with the existing AWS environment, detections aren't locked to one product |
| CI/CD | Github Actions, authenticating to AWS through OIDC | Pipelines live beside the code |


IDE + AI assistant
   -> Pre-commit: gitleaks, dependency check          (blocks secrets and fake packages locally)
   -> Pull request
   -> CI: secrets scan, SAST, SCA                      (blocks high severity; SARIF to the Security tab)
   -> Deploy to STAGING
   -> DAST: ZAP passive on PRs, active nightly + authorization tests
   -> Production
   -> Logs: CloudTrail, WAF, API Gateway, DNS, GuardDuty
   -> SIEM: Sigma-based detections -> alerts -> ticket and on-call


Integration points

1.  Developer to repo: pre-commit hooks stop secrets and unknown packages before they leave the laptop. Push protection and the CI secrets scan back this up for anyone who bypasses the hook
2.  Repo to pipeline: secrets, SAST, and SCA run on every pull request. Findings appear as PR comments and SARIF results and high severity findings block the merge
3.  Pipeline to staging: DAST runs only against, with test accounts and synthetic data. (doesn't run against production )
4.  Production to SIEM: audit, network and application logs feed the detections for ransomware indicators and Shadow AI
5.  Back to developers: scanner results and SIEM alerts go to the SIEM or Security Hub and to the team's ticket queue, with an owner and a fix date. Repeated findings become training topics and new Semgrep rules



PART 2: PRE-COMMIT SECRET SCANNING and SCA FOR AI-HALLUCINATED DEPENDENCIES
1: Secrets and Copilot
A pre commit hook cannot stop a developer pasting a credential into copilot. It only scans what is committed. By the time the hook runs, the paste has already happened. So I treat this as two problems: stop secrets reaching the repo, and the reduce the chance they reach the assistant at all


Layered control

| Layer | Control | What it stops |
| --- | --- | --- |
| Prevent | No long lived secrets in code or local files: use of a secret manager, short lived credentials via SSO | Secrets existing in placeds they can be copied from |
| Assistant | Copilot content exclusions for sensitive paths | The assistant reading secret file as context |
| Endpoint and network | DLP or proxy rules that flag secret patterns and PHI in uploads to unapproved AI sites, SIEM detection for consumer AI Domains |
| Commit time | Pre commit hooks | Secrets, including AI suggested code containing them, entering git | 
| Server side | Github push protection plus a CI gitleaks scan of full history | Anyone who bypassed the local hook with --no-verify |
| Response | Treat any detected secret as compromised: rotate first, then clean up | Exposure that already happened | 


Pre commit configuration

A custom rule in .gitleaks.toml catches database connection strings with embedded passwords


2: SCA FOR HALLUCINATED DEPENDENCIES

The risks: AI assistants sometimes suggest package names that don't exist. Attackers register those names with malicious code, so a developer who runs pip install on an AI suggested name can install malware

Standard SCA matches packages against known vulnerabilities, so a brand new malicious package passes

Two checks are done against;
Known vulnerabilities 

Existence and trust signals (package existence and severity level)

Where it runs in the pipeline
1. Pre commit: runs on changed requirements*.txt and package.json files, so a bad suggestion is caught before it leaves
2. Pull request (CI): the same check plus pip-audit, as a required status check
3. Self-test job: the workflow also runs the checker on deliberately bad fixtures and fails if checker doesn't fail
4. Scheduled run: weekly, because new advisories appeat for dependencies that haven't changed



PART 4: HANDLING INCOMPLETE LOGS DURING INVESTIGATIONS

Principle
Missing logs limit what can be proved, not what must be decided. 

Approach
1. Confirm and bound the gap
    Which source, which time window, which systems and accounts?
    Why is it missing? It was never enabled, the retention expired, ingestion failed
    Checking source health alerts, delivery errors and audit events

2. Preserving what exists
    Copying of relevant logs to write one storage, recording of hashes, and note handler
    Extend retention immediately (once something ages out mid investigation)
    Snapshots of affected hosts and volumes before change

3. Reconstructing from secondary sources

| Missing | Seconday source |
| --- | --- |
| Application logs | API Gateway access logs, WAF logs, load balancer logs, Cloudtrail |
| Authentication logs | Identity provider, Cognito sign in events | VPN logs |
| Endpoint logs | EDR telemetry, DNS and proxy logs, network flow logs |
| Cloudtrail data events | S3 server acces logs, AWS config history, GuardDuty findings |
| Everything from one host | Backups and snapshots, memory and disk forensics | 


4. Corroborate
     Supporting each key conclusion with at least independent sources
     Alignining of time zones and checkk for clock drift


5. State confidence explicitly
    Labelling of each finding confirmed, probable, or unknown with the evidence behind it

6. Decision on worst plausible case
    When scope cannot be proven, containment and notification decisions rest on worst reasonable scope, I treat all records in the exposed store as potentially accessed

7. Fixing the gap
   Enable missing source and set retention to policy
   Add tamper protection: Cloudtrail log file validation, write once bucketsm and logs in separate account
   Add monitoring

Communicating results
Reports separate evidence from inference and list the limitations caused by gaps. Reviewers should be able to see exactly which conclusions would change of the 
A
