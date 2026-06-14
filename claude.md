# Claude Context — PortScan Recon IDS/IPS Project

## 0) SITUATION SUMMARY (Read This First)

**Last updated: April 19, 2026**

Adil changed groups (from binôme with Anas El Kartouti → new 5-person group). The new group's
proposals (Aegis-Morph, Project Sentinel) were reviewed and found academically weaker. Strategic
decision: **keep Adil's BRD as the AI core**, borrow only the honeypot concept.

**✅ PLANNING PHASE COMPLETE.** The Hybrid BRD v2.0 (`PortScan_IDS_Hybrid_BRD_v2.pdf`)
has been generated via `generate_brd.py`. The document is the current scope authority.

**Current priority: implementation — environment setup, dataset download, ML pipeline.**

---

## 1) Project Identity

- **Project type:** PFE-style applied ML + cybersecurity system (semester-end academic project)
- **Core domain:** AI-based real-time detection and automated mitigation of Port Scanning & Network Reconnaissance attacks
- **Attack focus:** Port Scanning / Network Reconnaissance (confirmed, locked)
- **Team:** 5 members (Adil Lekhbioui confirmed; other 4 from new group, names TBC)
- **Operating context:** Controlled LAN lab, virtualized environment (academic but implementation-oriented)
- **Graded primarily on:** AI lifecycle documentation quality (CRISP-DM flow, data prep, model comparison, validation, deployment clarity)

---

## 2) Project History — What Has Been Done

### 2.1 Previous Group (Binôme Phase)

- Adil was paired with Anas El Kartouti.
- Multiple attack types explored and compared: DDoS, Botnet, Brute Force, Port Scan.
- Port Scan selected as the final attack type.
- A full **Business Requirements Document (BRD)** was written: `PortScan_Recon_Needs_Expression.pdf`
- The fraud detection PFE adopted as methodology + structure benchmark: `Détection_des_fraudes_dans_les_transactions_bancaires.pdf`

### 2.2 BRD Review Findings (Completed)

The BRD was reviewed section-by-section against the fraud PFE benchmark.

**Strengths:**
- Section 6 (Key Network Features table) — strongest section; features directly justified against attack behavior
- Section 7 (ML Model Strategy) — academically mature: RF primary, XGBoost secondary, Isolation Forest for slow scans; SMOTE; stratified K-fold + temporal holdout
- Section 8 (NFRs) — fully quantified targets (F1 ≥ 88%, FPR < 6%, detection < 8s, etc.)
- Section 11 (Success Criteria) — measurable and tied back to NFRs

**Issues to fix before submission:**
- Document title "Decision-Making Needs Expression" → rename to proper Expression des Besoins title
- Section 3 (Objectives) conflates objectives with functional requirements → restructure into 3 clean high-level objectives; move Alerting/Response items to Section 4
- CAIDA dataset listed with "Variable captures" — vague; either specify subset or remove it
- Technical Stack lists Flask+D3.js AND Grafana+InfluxDB as alternatives → must commit to one
- Project phases have no timeline estimates → add week estimates per phase
- Section 7 missing: hyperparameter tuning mention (GridSearchCV / RandomizedSearchCV)
- Missing from final report (not BRD): literature review, ethical considerations, architecture diagram, French abstract

### 2.3 New Group Proposals (Reviewed and Compared)

**Aegis-Morph**: Isolation Forest only + IP Polymorphism + Honeypot. Uses KDD-99 (1999, obsolete).
No supervised pipeline, no F1/precision/recall possible. **Verdict: 3/10 vs Adil's BRD 8.5/10.**

**Project Sentinel**: Anomaly detection + Port Hopping + Honeypot + Streamlit. No dataset, no features,
no validation. 3-page pitch, not a BRD. **Verdict: least developed.**

**Decision:** Use Adil's BRD as AI/ML core. Borrow only **honeypot redirect** from Sentinel.
Reject: KDD-99, IP Polymorphism, Port Hopping (sysadmin tasks, zero AI grading value).

### 2.4 Hybrid BRD v2.0 — Generated ✅

- `generate_brd.py` written using `fpdf 1.7.2` — generates a styled, multi-section PDF.
- `PortScan_IDS_Hybrid_BRD_v2.pdf` produced — **this is now the scope authority document.**
- Comparative review saved in `brd_vs_aegis_review.md.resolved`.

**What the Hybrid BRD v2.0 adds over the original:**
- Section 10: Honeypot Response Layer (fake listener, iptables REDIRECT, probe logger)
- Section 11: 5-person team role assignments with per-role deliverables
- Section 12: Week-by-week 7-week execution timeline (4 CRISP-DM phases)
- Port Range Entropy as 11th ML feature (Shannon entropy of dst ports — RF-friendly, peer-cited)
- Dashboard stack committed: **Flask + Socket.IO + D3.js**

---

## 3) Confirmed Technical Decisions (Locked)

- **Attack type:** Port Scanning & Network Reconnaissance
- **Dataset primary:** CICIDS2017 PortScan subset (~158,000 flows)
- **Dataset secondary:** UNSW-NB15 Reconnaissance category (~13,000 records)
- **Models:** Random Forest (primary) + XGBoost (comparison) + Isolation Forest (slow scan anomaly layer)
- **Imbalance handling:** SMOTE on training set only
- **Validation:** Stratified K-Fold (k=10) + temporal holdout (last 20% chronologically)
- **Evaluation metrics:** Accuracy, Precision, Recall, F1, AUC-ROC, per-scan-type detection rate
- **v1 output:** Binary BENIGN vs PORT_SCAN
- **v2+ output:** Scan type classification (SYN / UDP / ACK / XMAS / Connect)
- **Auto-blocking:** iptables DROP with TTL-based auto-unblock and audit log
- **Optional add-on:** Honeypot redirect (fake listener on old IP logs attacker probes)
- **Language:** English only for all documentation and reports
- **Python version:** 3.10+

---

## 4) Open Decisions (New Team Must Align On These)

1. ~~**Dashboard stack:**~~ ✅ **Resolved — Flask + Socket.IO + D3.js** (Grafana alternative dropped)
2. **Team role assignments:** capture layer / ML pipeline / dashboard / attack simulation / documentation (Role 1 = Adil confirmed; Roles 2-5 TBC)
3. **Virtualization platform:** VirtualBox or VMware or GNS3 — confirm based on hardware
4. **Deployment target:** Single host multi-VM or distributed? Containerized?
5. **Blocking policy:** Confidence threshold (≥ 0.85 for honeypot redirect), TTL duration, IP whitelist
6. ~~**Timeline:**~~ ✅ **Resolved — 7-week plan in BRD v2.0 Section 12**
7. **CAIDA dataset:** Use or drop from scope?
8. **Honeypot add-on:** Defer to Phase 3 (Week 5) per timeline — implement if time permits

---

## 5) Non-Functional Targets (From BRD)

| Requirement | Target |
|---|---|
| Fast scan detection | < 8 seconds |
| Slow scan detection | < 90 seconds (sliding window) |
| Model F1-Score | ≥ 88% on CICIDS2017 test subset |
| Model Accuracy | ≥ 90% overall |
| False Positive Rate | < 6% |
| Dashboard Refresh | ≤ 5 seconds |
| Blocking Response | < 15 seconds from detection to iptables DROP |

---

## 6) ML Strategy Detail

- **Primary:** Random Forest Classifier — high-dimensional tabular data, feature importance for explainability
- **Comparison:** XGBoost — compared on time-windowed aggregated features
- **Slow scan layer:** Isolation Forest (unsupervised) on sliding 60s window per IP
- **Feature engineering:** Time-window aggregation — ports/IP/10s, SYN-ratio, distinct_dst_ports over rolling windows
- **Imbalance:** SMOTE on training set only
- **Validation:** Stratified K-Fold (k=10) + temporal holdout (last 20% by chronological order) — prevents leakage
- **Tuning:** GridSearchCV / RandomizedSearchCV on RF and XGBoost — quantify gains vs defaults
- **Evaluation:** Accuracy, Precision, Recall, F1, AUC-ROC + per-scan-type detection rate table

---

## 7) Key Features for the ML Model

| Feature | Relevance |
|---|---|
| Distinct Dst Ports/IP | Critical — core scanning signature |
| SYN Flag Count (no handshake) | Critical — stealth SYN scan |
| RST Flag Count | Very High — port probe rejection |
| Flow Duration | High — very short in fast scans |
| Total Fwd Packets | High — usually 1 per probe |
| IAT Mean | High — slow scans have large inter-arrival time |
| ACK Flag Count | Medium — ACK scan detection |
| Unique Dst IPs/Src | Medium — host discovery phase |
| Bwd Packet Length | Medium — RST vs SYN-ACK ratio |
| TTL Value | Low — OS fingerprinting attempts |
| **Port Range Entropy** ✅ NEW | **High — Shannon entropy of dst ports; randomized vs sequential scan** |

Compute all features per (src_ip, 10s window) AND (src_ip, 60s window) independently.

---

## 8) System Architecture Vision

```
[Capture Layer]
  Scapy BPF filter on LAN interface (SYN-only or full TCP/UDP)
  → Rolling aggregation per source IP (10s and 60s windows)

[Feature Layer]
  Pandas windowed aggregation → feature vector per (src_ip, time_window)

[Detection Layer]
  v1: RF binary classifier → BENIGN / PORT_SCAN + confidence score
  v2+: multi-class scan type classifier (SYN / UDP / ACK / XMAS)
  Parallel: Isolation Forest on 60s window for slow scan anomalies

[Response Layer]
  Alert: severity score + scan type label → event store
  Blocking: iptables DROP via Python subprocess → audit log
  Optional: honeypot redirect to fake listener on old IP

[Observability Layer]
  Real-time dashboard (stack TBD)
  → Active scanners list
  → Port activity heat map
  → Attacker profile (IP, MAC, ports probed, first/last seen)
  → Alert feed with confidence and severity
```

---

## 9) Methodology Quality Reference (Fraud Detection PFE)

Replicate these structural patterns from `Détection_des_fraudes_dans_les_transactions_bancaires.pdf`:

1. CRISP-DM chapter structure: problem → data understanding → prep → modeling → evaluation → deployment → perspectives
2. Comparative model benchmark table (accuracy, F1, AUC across models)
3. Class imbalance section with before/after SMOTE analysis
4. Hyperparameter tuning section with quantified gains
5. Explainability outputs (feature importance charts)
6. Deployment architecture diagram
7. Both French résumé and English abstract
8. Literature review / État de l'Art chapter covering existing IDS approaches
9. Ethical considerations (privacy, automated blocking implications)

---

## 10) File Reference

| File | Purpose | Status |
|---|---|---|
| `PortScan_IDS_Hybrid_BRD_v2.pdf` | **Hybrid BRD v2.0 — current scope authority** | ✅ Generated |
| `expression_de_besoin.tex` | **Expression de Besoin / Problématique — LaTeX (prof's required format)** | ✅ Complete |
| `generate_brd.py` | Python script (fpdf 1.7.2) that generates the Hybrid BRD PDF | ✅ Complete |
| `brd_vs_aegis_review.md.resolved` | Detailed comparative review (BRD vs Aegis-Morph vs Sentinel) | ✅ Complete |
| `PortScan_Recon_Needs_Expression.pdf` | Original BRD v1 — superseded by Hybrid BRD v2.0 | Reference only |
| `Détection_des_fraudes_dans_les_transactions_bancaires.pdf` | Methodology/structure benchmark (CRISP-DM) | Reference only |
| `Aegis_Morph_Master_Blueprint_Full.pdf` | New group proposal — reviewed, not adopted | Reference only |
| `Project_Sentinel_The_Ghost_Castle.pdf` | New group concept — reviewed, not adopted | Reference only |

> **File format note:** All `.pdf` files in this project are ZIP archives containing numbered `.txt`
> files and a `manifest.json`. Use Python's `zipfile` module. `pdftotext` and `pypdf` will fail.

## 11) Implementation Status Tracker

| Phase | Status | Next Step |
|---|---|---|
| Attack type selection | ✅ Done | — |
| BRD v1 written | ✅ Done | — |
| Group proposals reviewed | ✅ Done | — |
| Hybrid BRD v2.0 generated | ✅ Done | — |
| Expression de Besoin (LaTeX) | ✅ Done | Compile with `pdflatex` |
| Environment setup (VMs) | ⬜ Not started | Ubuntu IDS VM + Kali attacker VM |
| Dataset download | ⬜ Not started | CICIDS2017 PortScan + UNSW-NB15 Recon |
| ML pipeline (RF + XGBoost + IF) | ⬜ Not started | Starts after data prep |
| Capture pipeline (Scapy) | ⬜ Not started | BPF filter + rolling window aggregation |
| Dashboard (Flask + D3.js) | ⬜ Not started | Week 4 per timeline |
| Honeypot layer | ⬜ Optional | Week 5, defer if time tight |

---

## 12) Review Protocol for AI Assistance

Before giving any suggestion, edit, or recommendation:

1. Re-read `PortScan_IDS_Hybrid_BRD_v2.pdf` (Hybrid v2.0) for scope alignment
2. Cross-check against fraud PFE methodology patterns
3. Label every suggestion as: **MANDATORY** / **RECOMMENDED** / **OPTIONAL**
4. State impact on: AI lifecycle documentation quality, latency, recall, false positives
5. Remember: planning is done — prioritize practical implementation steps

---

## 13) Reusable Prompt Snippet

> "Project context: 5-person team, AI-based IDS/IPS for PortScan/Recon detection on a controlled LAN.
> **Current scope authority: `PortScan_IDS_Hybrid_BRD_v2.pdf` (Hybrid BRD v2.0).**
> Use fraud detection PFE as methodology benchmark (CRISP-DM, class imbalance, model comparison,
> tuning, deployment). ML core: RF + XGBoost + Isolation Forest, CICIDS2017 + UNSW-NB15, SMOTE,
> temporal holdout. Dashboard: Flask + Socket.IO + D3.js. Honeypot redirect: optional (Week 5).
> Rejected: IP Polymorphism, Port Hopping, KDD-99. Graded on AI lifecycle documentation quality.
> Planning complete — next phase is implementation."
