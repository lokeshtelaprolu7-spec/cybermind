# CyberMIND — Cybersecurity Digital Twin

## 1. Digital Twin Concept
The CyberMIND Digital Twin is a living computational model of an organization's actual infrastructure. It reflects real-time operational states, exposure levels, network topologies, software versions, and security controls.

## 2. In-Memory Cloning & Non-Destructive Simulation
When security operators evaluate speculative changes (e.g. "What happens if API-01 becomes public?"), the digital twin engine:
1. Creates an isolated clone of the topology graph in memory.
2. Applies the requested architectural mutations to the clone.
3. Re-evaluates network ingress paths, perimeter exposure, and attack vectors.
4. Generates a before-and-after comparison with differential risk metrics.
5. Produces actionable recommendations from the Defender Agent.

**Production safety:** Live infrastructure is never altered or touched during scenario evaluation.

## 3. Visualization
Interactive topology visualization is powered by React Flow with custom cybersecurity node cards displaying criticality badges, active CVE counts, network exposure indicators, and risk scores.
