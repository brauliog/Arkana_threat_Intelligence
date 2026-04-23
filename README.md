# Arkana Threat Intelligence

**Map the attack. Not just the URL.**

Arkana is a phishing intelligence platform that detects, clusters, and tracks phishing campaigns by analyzing infrastructure reuse, page similarity, and domain behavior.

Instead of answering:
> “Is this URL malicious?”

Arkana answers:
> “What campaign is this part of, how is it evolving, and what infrastructure is behind it?”

---

## Why Arkana Exists

Modern phishing detection tools operate at the **indicator level**:
- One URL at a time
- Little context
- No campaign awareness

Attackers don’t operate that way.

They reuse:
- hosting infrastructure
- TLS certificates
- phishing kits
- domain patterns

Arkana is built to model phishing as a **connected system**, not isolated events.

---

## Core Capabilities

### 🔍 URL Intelligence & Enrichment
- DNS resolution
- TLS certificate analysis
- HTTP + HTML extraction
- Domain metadata (age, registrar, entropy)

---

### Campaign Detection Engine (Key Feature)
Arkana groups related phishing assets into campaigns using:

- shared IP / ASN infrastructure  
- HTML template similarity  
- TLS certificate reuse  
- domain naming patterns  

---

### Graph-Based Threat Modeling
Phishing data is stored as a graph:

This enables:
- multi-hop threat discovery
- infrastructure tracing
- hidden domain discovery

---

### Risk Scoring Engine
Each URL is scored based on weighted signals:

- domain age
- URL entropy / obfuscation
- phishing kit similarity
- infrastructure reputation

---

### Campaign Intelligence Reports
Arkana generates analyst-ready reports including:

- campaign summary
- infrastructure overview
- indicators of compromise (IOCs)
- recommended response actions


