# CyberMIND — Attack Surface & Attack Path Engine

## 1. Attack Surface Calculation
The attack surface score is computed deterministically using weighted exposure factors:
$$\text{Attack Surface Index} = \sum (\text{Internet-Facing Assets} \times 15) + \sum (\text{Critical Vulnerabilities} \times 10) + \sum (\text{High Vulnerabilities} \times 5) - \sum (\text{Compensating Controls} \times 8)$$

The engine monitors:
- Internet-facing boundaries (public IP subnets, open ports, ingress routes)
- Unauthenticated API routes
- Cloud storage accessibility (e.g. S3 bucket public read/write ACLs)
- Correlated high-severity CVEs

## 2. Attack Path Discovery
Attack paths represent multi-hop trajectories an adversary could take from an untrusted perimeter entrypoint to sensitive Crown Jewels.

### Traversal Algorithm
The pathfinding engine traverses the directed graph from ingress nodes (`is_internet_facing == True` or public CIDR) to designated Crown Jewels (`criticality == CRITICAL`). Hops are validated against relationship protocols (HTTPS, TCP, SSH) and vulnerability exploitability.

Example Discovered Vector:
```
[Internet 0.0.0.0/0] 
       │ 
       ▼ (Port 443 HTTPS)
[WEB-01 (Nginx/React)] 
       │ 
       ▼ (Port 8080 Reverse Proxy)
[APP-01 (Spring Core Microservice)] 
       │ 
       ▼ (Port 5432 Database Connection)
[DB-01 (Crown Jewel Customer PostgreSQL)]
```
Each path identifies:
- Entry point
- Intermediate pivot points
- Target asset
- Compound risk score
- Associated MITRE ATT&CK techniques
- Specific compensating mitigation controls
