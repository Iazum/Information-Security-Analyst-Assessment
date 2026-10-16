SOFT SKILLS AND POLICY ENFORCEMENT

PART A

THE BUSINESS REFUSES A CONTROL BECAUSE OF COST

POSITION: security spending is a business decision. My job is to make the risk and the options clear, not to win the argument

Approach

1. Understand the objection. Is it budget, timing, doubt about valid, or competing priorities
2. Separate the non negotible from the optional. Controls required by law, contract or regulation
3. Quantify in business terms. Likelihood times impact regulatory exposure, customer or contract risk and downtime cost
4. Offer cheaper routes. Open source tooling, a phased rollout covering only the highest risk systems first
5. Documentation of risk acceptance if they decline. Signed by the accountable executive, with an expiry date and triggers that reopen it.
6. Follow through. Addition to the risk register, monitoring residual risk and reviewing.

Illustrative example

The business rejects a paid DAST subscription for the patient portal (roughly $15k per year). I estimate the risk of an exploitable web flaw leading to a data breach at 10% per year with an impact of about $400k, so roughly $40k of expected annual loss. 

I propose free OWASPZAP baseline scans in CI for the portal only and a review after one quarter using real findings. If they still decline, they sign risk acceptance


PART B: PRIORITISING MULTIPLE SIMULTANEOUS ALERTS

Principle: prioritise by potential business harm and urgency, and contain active spread before investigating anything that is not spreading

Factors I score for each alert

| Factor | Question | 
| --- | --- |
| Evidence | Is this confirmed malicious activity or only a signal? |
| Spread | Is it active and spreading, or static? |
| Asset criticality | Does it involve a crown jewel system ( patient records)
| Data sensitivity | Is it regulated or confidential data involved? | 
| Privilege | Is an admin or service account involved? |
| Time sensitivity | Does delay make it much worse? |


PART C: ONE PAGE INCIDENT REPORT

Scenario chosen: a developer pastes patient data into a public AI chatbot, because it ties together the AI risk theme

The file is in incident-report folder


PART D: TRANSLATING SIEM, DAST and SAST findings for business stakeholders

Principle: leading with business impact and the decision needed and keep the technical detail underneath

Format I use for every finding
1. What we found
2. Why it matters (data, customers, money, regulation, reputation)
3. How likely (evidence, exposure, ease of exploitation)
4. Options (cost, effort, time, risk reduced)
5. Recommendation and the decision I need

Translation examples

| Technical finding  | Business translation |
| --- | --- |
| DAST: SQL Injection in the login endpoint | An attacker could read patient records through the website. That is a reportable breach with regulatory, legal and reputational cost. A fix is about two days of developer time. | 
| SAST: hardcoded database password in the repository | Anyone with code acess can reach the patient database. Passwords to be rotated and moved to secrets manager | 
| SIEM: 400 failed logins then one success from foreign IP | Employee's credentials are brute forced thus account is locked |
| SIEM: repeated uploads to a consumer AI site | Third party may be receiving patient data thus a decision is needed on an approved AI tool and a policy |


PART E: DEVOPS AND SECUITY COLLABORATION WHEN ROLLING OUT SAST/DAST

Principle: security joins the team's workflow. Developers will adopt tools that are fast, accurate and come with clear fix guidance

Rollout
| Phase | What happens | Why |
| --- | --- | --- | 
| 0. Align | Agree shared goals, pipeline time budget | Removes the "security slows us down |
| 1. Pilot | One willing team, tools in report only mode | Low risk |
| 2. Tune | Review findings together weekly, false positives are suppressed | Cuts noise |
| 3. | Gate selectively | Block builds only on high or critical findings | Predictable |
| 4. Scale | Templates, documentation, security champions in each team | Adoptions without a security bottleneck |
| 5. Improve | Joint dashboard and monthly review | Keeps it a shared programme |


PART F: SAFE HARBOR: SELF REPORT VERSUS COVER UP

Scenario: a developer pastes a hardcoded database connection string into a public LLM

Principle: the technical response is identical in both cases, because the credentials has to be treated as compromised either way. What differs is how we treat the person and what timeline tells us.

Safe harbor protects prompt, honest reporting of accidents. It does not protect deliberate concealment. 

Shared technical response
1. Rotation of  the credential immediately
2. Reviewing of database authentication logs
3. Limiting of reach: the database not to have internet exposed, network allowlists tightened
4. Scoping of what is exposed
5. Vendor to delete the conversation and turn off history
6. Finding of other copies of the same secret in code
7. Closure of root cause

PART G: BALANCING USER PRIVACY AND SECURITY MONITORING

Principle: monitoring to have legitimate purpose, collect only what that purpose needs 

| Principle | Practice |
| --- | --- |
| Purpose limitation | Essence of monitoring to be defined and prohibition of other users |
| Data minimisation | Metadata over content. Inspect content only with pattern based DLP |
| Transparency | A published acceptable use and monitoring policy, acknowledged by staff |
| Pseudonymisation | Analysts to see user IDs that are pseudonymisation by default |
| Access control | Role based access to logs |
| Retention limits | retention of logs as needed for detection and legal requirements then are deleted |
| Asssesment before rollout | A privacy mipact assessment for any new monitoring |
| Oversight | Periodic review of monitoring rules |
