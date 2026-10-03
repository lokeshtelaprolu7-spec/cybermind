# CyberMIND — Cyber Memory Architecture

CyberMIND implements an organizational cybersecurity memory system enabling the platform to retain long-term institutional knowledge, learn from previous incidents, and recommend validated response playbooks.

## Four-Tier Memory Architecture

### 1. Episodic Memory ("What happened?")
Stores chronological records of security episodes:
- Initial alert triage logs
- Incident timelines and attacker dwell times
- Root-cause discovery notes
- Evidence artifacts gathered during investigations

### 2. Semantic Memory ("What do we know?")
Maintains the conceptual understanding of the enterprise:
- Asset inventories, critical IP subnets, and trust boundaries
- Designated Crown Jewel classifications (e.g. DB-01 Customer Data)
- Authorized software baselines and approved dependency versions

### 3. Procedural Memory ("What should we do?")
Stores actionable, proven response playbooks and remediation runbooks:
- `PB-01`: Autonomous Token Invalidation & Session Termination
- `PB-02`: Edge CIDR Rate-Limiting & WAF Blocklist Synchronization
- `PB-03`: S3 Bucket ACL Audit & Public Access Enforcement
- `PB-04`: Emergency PostgreSQL Connection Drain & Snapshot

### 4. Historical Memory ("What happened previously?")
Tracks recurrent security patterns across quarterly review cycles:
- Repeated vulnerability root-causes (e.g. recurring microservice authentication oversights)
- Closed detection gaps and newly implemented telemetry sensors
- Documented false positive signatures

## Similar Incident Engine
When an operator or agent investigates a new anomaly, the Similar Incident Engine computes semantic similarity vectors over historical incidents and outputs:
- Percentage similarity score
- Shared indicators of compromise (IOCs)
- Correlated MITRE ATT&CK techniques
- The exact playbook that resolved the past incident
