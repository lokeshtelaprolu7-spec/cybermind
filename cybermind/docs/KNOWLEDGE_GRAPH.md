# CyberMIND — Knowledge Graph Architecture

## 1. Graph Model & Schema
CyberMIND models enterprise infrastructure as a directed property graph. Nodes represent architectural entities and edges capture trust boundaries, network connectivity, and operational relationships.

### Node Labels
- `Organization`: Enterprise boundary
- `Asset`: Physical/virtual host or resource
- `Application`: Running application tier
- `API`: Exposed or internal microservice API endpoint
- `Database`: Persistent data store (often Crown Jewels)
- `CloudResource`: S3 bucket, IAM role, VPC, or cloud service
- `Container`: Docker/Kubernetes container instance
- `Network`: Subnet, VPN gateway, or router
- `Software`: Installed runtime, library, or OS
- `CVE`: Known vulnerability identifier
- `Technique`: MITRE ATT&CK technique (e.g. T1190)
- `SecurityControl`: Defensive control (WAF, EDR, MFA, Firewall)
- `Finding`: Correlated security finding
- `Incident`: Active or historical incident

### Relationship Types
- `(:User)-[:HAS_ACCESS]->(:Application)`
- `(:Application)-[:CONNECTS_TO]->(:Database)`
- `(:Server)-[:RUNS]->(:Software)`
- `(:Software)-[:AFFECTED_BY]->(:CVE)`
- `(:API)-[:EXPOSED_TO]->(:Network)`
- `(:Asset)-[:PROTECTED_BY]->(:SecurityControl)`
- `(:Finding)-[:AFFECTS]->(:Asset)`
- `(:Incident)-[:INVOLVES]->(:Asset)`

## 2. Graph Engine Implementation
The graph engine supports:
1. **Neo4j (Production):** Cypher queries for path traversal and complex dependency analysis.
2. **NetworkX (Standalone / Demo):** In-memory directed graph engine executing shortest-path (Dijkstra) and all-simple-paths algorithms without requiring external Neo4j daemon.
