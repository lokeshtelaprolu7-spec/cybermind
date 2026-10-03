# CyberMIND — System Architecture Specification

## 1. Overview
CyberMIND is an **Agentic AI-Powered Cybersecurity Digital Twin for Autonomous Attack-Surface Analysis, Threat Investigation, Cyber Memory, and Evidence-Based Security Intelligence**.

```
                        CYBERMIND
                           │
                           ▼
                    NEXT.JS FRONTEND
                           │
                           ▼
                     FASTAPI BACKEND
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       AUTHENTICATION              API SERVICES
              │                         │
              └────────────┬────────────┘
                           ▼
                  AI ORCHESTRATOR
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
      AGENTS              RAG             KNOWLEDGE
        │                  │               GRAPH
        │                  │                  │
        ▼                  ▼                  ▼
   SOC Agent          Vector DB           Neo4j /
   VAPT Agent         Documents          NetworkX
   API Agent          Embeddings
   Cloud Agent
   Threat Agent
   Forensics Agent
   Investigator
   Risk Agent
   Attack Surface Agent
   Defender Agent
   Reviewer Agent
        │
        └──────────────────┬─────────────────┘
                           ▼
                    DIGITAL TWIN
                           │
                           ▼
                  ATTACK PATH ENGINE
                           │
                           ▼
                    SECURITY FINDINGS
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
         REPORT ENGINE          BLOCKCHAIN LAYER
                                      │
                                      ▼
                              EVIDENCE PROVENANCE
```

## 2. Core Pillars
1. **Digital Twin Modeling:** Real-time graph ontology mapping servers, applications, APIs, databases, cloud resources, vulnerabilities, and security controls.
2. **Deterministic Attack Path & Surface Engine:** Breadth-first graph traversal from unauthenticated public ingress to internal crown jewels.
3. **Multi-Agent Orchestrator:** LangGraph state machine directing 11 specialized security agents with adversarial reviewer verification.
4. **Cybersecurity RAG Brain:** Authoritative knowledge grounding across OWASP, MITRE ATT&CK, NIST CSF 2.0, CISA, and CVE.
5. **Cyber Memory:** Four-tier memory (Episodic, Semantic, Procedural, Historical) and vector-based similar incident correlation.
6. **Blockchain Evidence Provenance:** SHA-256 cryptographic hashing and immutable ledger anchoring for tamper-evident forensics.
