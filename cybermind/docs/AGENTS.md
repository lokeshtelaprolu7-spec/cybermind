# CyberMIND — Multi-Agent AI System Architecture

CyberMIND features a collaborative multi-agent architecture orchestrated through a LangGraph state machine. Each agent specializes in a distinct domain and communicates using structured JSON schemas.

## 1. Orchestrator Agent
- **Responsibilities:** Query intent detection, domain classification, investigation planning, agent routing, tool selection, synthesis, and final response assembly.

## 2. Specialized Security Agents
1. **SOC Agent (`SOCAgent`):** Log analysis, alert triage, anomaly detection, MITRE ATT&CK technique mapping.
2. **VAPT Agent (`VAPTAgent`):** Vulnerability explanation, CVSS calculation, patch validation, remediation planning.
3. **Web/API Agent (`WebAPIAgent`):** HTTP/REST analysis, OWASP Top 10 API Security mapping, auth/authz bypass analysis.
4. **Cloud Agent (`CloudAgent`):** Cloud misconfigurations, IAM least privilege audits, S3 bucket exposure.
5. **Threat Intelligence Agent (`ThreatIntelAgent`):** IOC correlation, reputation scoring, APT actor attribution.
6. **Digital Forensics Agent (`ForensicsAgent`):** Controlled artifact analysis, PCAP/log parsing, timeline reconstruction.
7. **Investigator Agent (`InvestigatorAgent`):** Multi-modal correlation across logs, assets, and threat intelligence.
8. **Attack Surface Agent (`AttackSurfaceAgent`):** Perimeter exposure quantification and route leak detection.
9. **Risk Agent (`RiskAgent`):** Deterministic explainable risk score calculation.
10. **Defender Agent (`DefenderAgent`):** Compensating controls, Sigma detection rules, and hardening guidance.
11. **Security Reviewer Agent (`ReviewerAgent`):** Adversarial self-check evaluating agent outputs for hallucinations, unsupported claims, and ungrounded statements.

## 3. Structured Contract Schema
Agents return structured JSON objects enforcing rigorous type contracts:
```json
{
  "agent": "threat_intelligence",
  "status": "completed",
  "domain": "Threat Intelligence",
  "findings": [],
  "evidence": [],
  "confidence": 0.92,
  "sources": [],
  "recommendations": []
}
```
Unstructured natural language is prohibited between internal agent communication hops.
