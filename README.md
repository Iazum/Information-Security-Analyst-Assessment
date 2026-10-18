 Information-Security-Analyst-Assessment

 Author: Ian Muzai Agufana | Contact: https://www.linkedin.com/in/ian-muzai-9b948a186 

 1. Architecture diagram is in Section 1
 2. One page Incident report in Section 2A

What is in this repository

| Section | Topic | What you will find | 
| --- | --- | --- |
| 1A. Secure API Gateway | API Gateway, WAF, authentication and a controlled path to Enterprise LLMs on AWS | Architecture diagram and write up, step by step build, two Sample APIs plus an LLM gateway, WAF and rate limit evidence, AI Input/output guardrails design, risk register |
| 1B. Security engineering | SIEM, DAST, SAST, SCA and secret scanning for AI-assisted development | Working CI pipelines, custom Semgrep rules for AI-generated logic flaws, hallucinated-dependency checker, Sigma detections for ransomware and Shadow AI, SIEM onboarding runbook |
| 2. Soft skills and policy | Communication , prioritisation, policy enforcement | Answers to questions a to g, a one-page incident report (simulated), Safe Harbor handling of self-report versus cover-up | 


How the sections connect
The three parts tell one story. 
Section 1A builds a secured, AI-enabled API. 

Section 1B then applies the security pipeline to that same code (the Semgrep rules, dependency checks and DAST scan target the Section 1 API, and the SIEM monitors its logs). 

Section 2 covers the human side: how findings are communicated, how incidents are prioritised, and how people are treated when something goes wrong.


Repository structure

.
├── README.md                        <- you are here

├── .pre-commit-config.yaml          secret scanning + dependency check at commit time

├── .gitleaks.toml

├── .github/workflows/               secrets.yml, sast.yml, sca.yml, dast.yml

├── tests/fixtures/                  intentionally bad inputs used to prove the checks work

│

├── section-1-secure-api-gateway/

│   ├── README.md                    parts a to f

│   ├── apis/                        orders, summarize and LLM gateway Lambda code

│   ├── diagram/

│   ├── screenshots/

│   ├── evidence/

│   └── tests/                       run_tests.sh and captured results

│

└── section-1b-security-engineering/

    ├── README.md                    answers 1 to 6 plus the AI logic-flaw question
    
    ├── semgrep-rules/
    
    ├── sca/
    
    ├── dast/
    
    └── siem/
    
├── section-2-softskills-policy/

│   ├── README.md                    answers a to g

│   └── incident-report/             one-page report (Markdown and PDF)

│


Notes
1. No real secrets or personal data. All incident details, patient data, names and figures are fictional
2. Cloud resource: The AWS environment from Section 1 is torn down after evidence capture to avoid costs. Screenshots, logs and the exported template in the repository are the record
3. Scanning scope: DAST was run only against staging development

Where to look for specific skills

| Skill | Location |
| --- | --- |
| Cloud Architecture and secure design | Section 1, parts a and b |
| Hands on implementation | Section 1, parts c |
| AI security (guardrails, shadow AI, prompt injection | Section 1 parts e and f, Section 1b |
| Devsecops pipeline engineering | Section 1B .github workflows |
| Detection engineering | Section 1b, siem/sigma |
| Incident handling and communication | Section 1a, questions b,c and f |
| Stakeholder and policy skills | Section 1a, questions a, d, e and g |
