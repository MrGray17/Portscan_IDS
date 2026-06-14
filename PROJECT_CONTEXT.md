# Portscan IDS (AEGIS Entropy) — Complete Project Context & History

This document is the **single source of truth** for the entire Portscan_IDS project. It records every architectural decision, module implementation, report revision, and team contribution from inception through the final report restructuring session of June 2026.

---

## 1. Executive Summary & Project Identity

**Project name:** Portscan IDS / AEGIS Entropy  
**Type:** AI-based real-time Intrusion Detection System for Port Scanning & Network Reconnaissance  
**Academic context:** PFE (Projet de Fin d'Études) — 5-person team, ENSA (École Nationale des Sciences Appliquées)  
**Core domain:** Applied ML + Cybersecurity — supervised/unsupervised detection paired with active defense  
**Repository:** `github.com/adillekhbioui-collab/Portscan_IDS`  

### 1.1 The Threat

Port scanning is the primary reconnaissance phase of nearly all cyberattacks. Attackers probe host ports to identify active services, OS versions, and potential vulnerabilities. Traditional signature-based IDS struggle with rapidly mutating scan patterns and "low and slow" stealthy scans.

### 1.2 The AEGIS Approach

AEGIS combines three defense paradigms:

1. **Supervised ML Detection** — Random Forest + XGBoost classifiers trained on optimized flow features for instant scan recognition.
2. **Unsupervised Anomaly Detection** — Isolation Forest module for spotting abnormal behavior (slow/stealthy scans) that doesn't match baseline benign traffic.
3. **Active Deception & Moving Target Defense (MTD)** — Dynamic port shifting + honeypot redirection to waste attacker resources and collect threat intelligence.

### 1.3 Performance Targets

| Metric | Target | Achieved (RF) | Achieved (XGBoost) |
|--------|--------|---------------|---------------------|
| F1-Score | >= 88% | 99.92% | 99.92% |
| Accuracy | >= 90% | 99.91% | 99.91% |
| FPR | < 6% | 0.11% | 0.11% |
| AUC-ROC | — | 0.9997 | 0.9999 |

Isolation Forest failed on the CICIDS2017 dataset (F1=7.89%, FPR=66.94%) due to the **Majority Anomaly Paradox** — see Section 5.5 for full analysis.

---

## 2. Project History — Complete Timeline

### 2.1 Phase 0: Conception & Planning (Pre-Repository)

- Adil Lekhbioui initially paired with Anas El Kartouti (binôme).
- Multiple attack types explored: DDoS, Botnet, Brute Force, Port Scan.
- Port Scan selected as final attack type.
- Full Business Requirements Document (BRD) written: `PortScan_Recon_Needs_Expression.pdf`.
- Fraud detection PFE adopted as methodology benchmark: `Détection_des_fraudes_dans_les_transactions_bancaires.pdf`.

### 2.2 Phase 1: Group Merge & Scope Definition

- Adil changed groups → new 5-person team.
- Group proposals (Aegis-Morph, Project Sentinel) reviewed — both found academically weaker.
- Decision: keep Adil's BRD as AI core, borrow only the honeypot concept.
- **Hybrid BRD v2.0** generated via `generate_brd.py` using `fpdf 1.7.2` — this became the scope authority.
- Technical stack committed: Flask + Socket.IO + D3.js for dashboard.
- 7-week execution timeline established (4 CRISP-DM phases).
- Team roles assigned across: capture layer, ML pipeline, dashboard, attack simulation, documentation.

### 2.3 Phase 2: Team Contributions & Collab Merges

The repo was built incrementally through multiple team member merges:

| Contributor | Module | Key Contribution |
|-------------|--------|------------------|
| **Khadija** | `detection/` | ML pipeline — preprocessing, training (RF, XGBoost, IF), evaluation |
| **El Yazid** | `deception/` | Active defense — MTD port shuffling, honeypot redirection, iptables integration |
| **Anas Moulay** | VM Integration | VirtualBox topology, network configuration, VM setup guide |
| **Anas ElKartouti** | Documentation | Conception report, interviews, BRD support |
| **Adil Lekhbioui** | `dashboard/`, `bridge/`, `config.py`, final report | SOC-style dashboard, bridge middleware, global config, report restructuring |

Merges preserved in git history:
- `e24bc1e` — Khadija ML pipeline merge
- `02b7ef4` — Yazid deception engine merge
- `0ecba16` — Active defense + Flask dashboard integration
- `e5f455e` — Bridge CSV/Nmap-to-ML detection pipeline
- `290441d` — Kali port scan simulation demo
- `b03184b` — SOC-style dashboard redesign
- `700fbc3` — Team member attribution in README

### 2.4 Phase 3: Final Report Restructuring (June 14–15, 2026)

This was the bulk of the most recent session's work. The final academic report (`docs/reports/05_final/`) underwent a complete restructuring across multiple commits:

**Commit sequence:**
1. **`04b5f1c`** — Initial 10-chapter skeleton created
2. **`275946a` / `1afb64f`** — LaTeX files fixed for pdflatex compatibility
3. **`e254934`** — Unused `preamble.tex` removed (merged into `report.tex`)
4. **`8ec698f`** — Abstract removed; VirtualBox environment visuals added to ch06 (5 screenshots of VM configuration)
5. **`9cc530d`** — 3 high-value sections from Yazid's defense report integrated into ch07: mutator implementation, severity mapping table, honeypot flag accuracy insight
6. **`894c3f1`** — 2 sections from Khadija's ML report integrated into ch04: PDCA methodology, preprocessed dataset export
7. **`98435da`** — Full rewrite of ch04 (Data Preparation) and ch05 (Model Training & Evaluation) with regenerated confusion matrices/ROC curves; Isolation Forest metrics corrected to match `evaluation_metrics.json`
8. **`aaa6039`** — Final restructuring: 10 chapters → 9 chapters, new professional cover page with university logos, all inconsistencies and orphan references fixed
9. **`c15b515`** — Logo files moved from `figures/` up to `05_final/` root for correct LaTeX graphics path resolution

**Chapter mapping (old → new):**

| Old | New | Title |
|-----|-----|-------|
| ch01_introduction | ch01_state_of_art | Introduction & State of the Art |
| ch02_state_of_art | ch02_understanding | Data Understanding & Methodology |
| ch03_understanding | ch03_data_prep | Data Exploration & Preparation |
| ch04_data_prep | ch04_model_training | Model Training |
| ch05_implementation | ch05_capture | Capture & Detection Pipeline |
| ch06_capture | ch06_defense | Active Defense (MTD + Honeypot) |
| ch07_defense | ch07_integration | System Integration |
| ch08_integration | ch08_test_validation | Testing & Validation |
| ch09_test_validation | ch09_conclusion | Conclusion & Perspectives |
| ch10_conclusion | *(merged into ch09)* | — |

**Key decisions made during restructuring:**
- Abstract removed (not useful for an applied AI project report)
- Chapter count reduced from 10 to 9 (conclusion folded into perspectives)
- Figures regenerated from retrained models to reflect accurate metrics
- VirtualBox screenshots added for environment documentation
- External report sections selectively integrated (academically relevant only, implementation details excluded)
- Cover page redesigned with UIT and ENSA logos, formal academic styling

### 2.5 Phase 4: Current Session — Logo & Push (June 15, 2026)

- Moved `logo-UIT.png` and `ensa_logo.png` from `docs/reports/05_final/figures/` to `docs/reports/05_final/` for correct LaTeX `\includegraphics` resolution.
- Committed and pushed to `main` on GitHub (`c15b515`).

---

## 3. Repository Architecture & Blueprint

```
Portscan_IDS/
├── .gitignore                       # Excludes data files (>50MB), build artifacts
├── README.md                        # Full repository description with badges, architecture
├── config.py                        # Global configuration (paths, model params, IPs)
├── requirements.txt                 # Top-level Python dependencies
├── run_demo.py                      # Live demo: Kali port scan simulation against AEGIS
├── PROJECT_CONTEXT.md               # THIS FILE — complete project context & history
├── CLAUDE.md                        # Shorthand context for AI assistants (April 2026 snapshot)
├── YAZID_CONTEXT.md                 # Yazid's defense subsystem documentation
├── workspace.code-workspace         # VS Code multi-root workspace
│
├── detection/                       # ML PIPELINE MODULE (by Khadija, integrated by Adil)
│   ├── requirements.txt             # Module dependencies (imbalanced-learn, etc.)
│   ├── CHANGES.md                   # Changelog of pipeline modifications
│   ├── models/                      # Saved serializations (.pkl)
│   │   ├── scaler.pkl               # Fitted StandardScaler
│   │   ├── random_forest.pkl        # Trained Random Forest classifier
│   │   ├── xgboost.pkl              # Trained XGBoost classifier
│   │   └── isolation_forest.pkl     # Trained Isolation Forest anomaly detector
│   ├── data/                        # Preprocessed.csv (gitignored), evaluation_metrics.json
│   ├── results/                     # Generated plots and metrics CSV
│   ├── src/                         # ML engine source code
│   │   ├── data_preprocessing.py    # Loading, cleaning, winsorizing, log-transforming
│   │   ├── feature_selection.py     # Mapping, correlation analysis
│   │   ├── modeltrain.py            # Scaling, SMOTE, Stratified 10-Fold CV, fitting
│   │   ├── evaluate_model.py        # Metrics, ROC, confusion matrices, success validation
│   │   └── predict.py               # Production inference wrapper
│   └── report/                      # Khadija's standalone ML documentation (LaTeX)
│
├── dashboard/                       # FRONTEND COMMAND CENTER (by Adil)
│   ├── app.py                       # Flask + Socket.IO web server
│   ├── templates/                   # Jinja2 HTML templates (SOC-themed)
│   ├── static/                      # CSS/JS (D3.js heatmaps, real-time charts)
│   └── ...                          # Dashboard assets
│
├── bridge/                          # INTEGRATION MIDDLEWARE (by Adil)
│   └── bridge.py                    # Connects capture → detection → dashboard → deception
│                                    # Loads scaler/models, classifies, dispatches alerts
│
├── deception/                       # ACTIVE DEFENSE ENGINE (by El Yazid)
│   ├── honeypot/                    # Decoy port listeners, scanner logging
│   └── mtd/                         # Moving Target Defense — dynamic port shuffling
│
├── capture/                         # TRAFFIC SNIFFING MODULE
│   └── ...                          # Scapy/pypcap packet capture & flow aggregation
│
├── demo/                            # DEMO SCRIPTS
│   └── ...                          # Kali attack simulation, scenario runners
│
├── data/                            # Shared data directory
├── models/                          # Shared model directory (synced with detection/models/)
├── tools/                           # Utility scripts
│   └── regenerate_figures.py        # Rebuild all ML figures from retrained models
│
└── docs/                            # DOCUMENTATION
    ├── reports/
    │   ├── 01_conception/           # Conception report (BRD, interviews)
    │   ├── 04_capture/              # Capture module documentation
    │   └── 05_final/                # FINAL ACADEMIC REPORT (see Section 4)
    │         ├── report.tex         # Main LaTeX document (compiles with pdflatex)
    │         ├── AEGIS.pdf          # Compiled PDF output
    │         ├── references.bib     # Bibliography
    │         ├── logo-UIT.png       # Université Ibn Tofail logo
    │         ├── ensa_logo.png      # ENSA Kénitra logo
    │         ├── chapters/          # 9 chapter .tex files (ch01..ch09)
    │         └── figures/           # Figures organized by module
    │               ├── data/        # ML pipeline figures (confusion matrices, ROC, boxplots)
    │               ├── capture/     # VM screenshots, capture architecture
    │               └── defense/     # MTD/honeypot diagrams
    └── ...                          # Other documentation
```

---

## 4. The Final Academic Report — Detailed Structure

Located at `docs/reports/05_final/`. Compiles with `pdflatex report.tex`.

### 4.1 Cover Page

Professional academic cover page featuring:
- Université Ibn Tofail and ENSA Kénitra logos
- Project title: "AEGIS Entropy — AI-Based Port Scan Detection & Active Defense"
- Academic year, team members, supervisor information
- Formal French academic formatting

### 4.2 Chapter Outline

| Chapter | File | Content |
|---------|------|---------|
| Ch. 1 | `ch01_state_of_art.tex` | Introduction, problem statement, state of the art in IDS, port scanning taxonomy, related work, CRISP-DM methodology |
| Ch. 2 | `ch02_understanding.tex` | Data understanding — CICIDS2017 dataset, class distribution analysis, feature exploration, PDCA methodology alignment |
| Ch. 3 | `ch03_data_prep.tex` | Data preparation — whitespace stripping, inf→NaN→median imputation, IQR Winsorization with boxplot analysis, skewness correction via log1p, preprocessed dataset export |
| Ch. 4 | `ch04_model_training.tex` | Model training — SMOTE balancing, StandardScaler (train-only fit), 10-fold stratified CV, Random Forest + XGBoost + Isolation Forest fitting, hyperparameter details |
| Ch. 5 | `ch05_capture.tex` | Capture pipeline — VirtualBox environment setup (Kali attacker + Ubuntu victim VMs), network architecture, Scapy-based packet capture, flow aggregation, VirtualBox screenshots |
| Ch. 6 | `ch06_defense.tex` | Active defense — MTD port mutator implementation (iptables, background thread, PRNG), honeypot decoy system, severity mapping table (ML output → defense action), +2.3% accuracy from honeypot feedback |
| Ch. 7 | `ch07_integration.tex` | System integration — bridge module, capture→detection→defense→dashboard data flow, real-time alert dispatch, Socket.IO event pipeline |
| Ch. 8 | `ch08_test_validation.tex` | Testing & validation — confusion matrices, ROC curves, model comparison table, per-scan-type detection rates, NFR verification |
| Ch. 9 | `ch09_conclusion.tex` | Conclusion, limitations, future perspectives, ethical considerations |

### 4.3 Key Report Properties

- **Language:** English (all documentation and reports)
- **Compiler:** pdflatex (not xelatex/lualatex)
- **Graphics path:** `{figures/data/}`, `{figures/capture/}`, `{figures/defense/}`
- **Cover logos:** Loaded from `05_final/` root (same directory as `report.tex`)
- **Single-file build:** All preamble merged into `report.tex`; no external preamble
- **Chapter count:** 9 (reduced from original 10; conclusion folded into ch09)
- **Font size:** Chapters use `\Large` (not `\Huge`) for titles
- **Color scheme:** Formal academic — cyan, amber, red, green, purple, darkbg, codegray, LightGray, LightBlue

---

## 5. Module Deep-Dives

### 5.1 Detection Module (`detection/`)

The ML engine. See the original detailed sections below (6–9) for full pipeline details.

**Key files:**
- `data_preprocessing.py` — 4-step pipeline: whitespace strip → inf/NaN handling → IQR Winsorization → log1p skewness correction
- `feature_selection.py` — 13-feature mapping from Data Dictionary, correlation heatmap generation
- `modeltrain.py` — Stratified 80/20 split, StandardScaler (train-only), SMOTE, 10-fold CV, model fitting
- `evaluate_model.py` — Accuracy, Precision, Recall, F1, AUC-ROC, FPR, confusion matrices, ROC curves
- `predict.py` — Production inference wrapper

**Models:**
- `random_forest.pkl` — RF classifier (100 trees), F1=99.92%, FPR=0.11%
- `xgboost.pkl` — XGBoost classifier, F1=99.92%, FPR=0.11%
- `isolation_forest.pkl` — Anomaly detector, F1=7.89%, FPR=66.94% (failed — see 5.5)

### 5.2 Dashboard Module (`dashboard/`)

Flask + Socket.IO web application providing:
- SOC-themed dark UI (cyberpunk aesthetic)
- D3.js real-time heatmap of port activity
- Live traffic metric charts
- Alert feed with severity indicators
- Active scanner tracking
- Port state grid (MTD config visualization)

**Startup:** `python dashboard/app.py`

### 5.3 Bridge Module (`bridge/`)

Integration middleware connecting all modules:
1. Ingests feature arrays from `capture/` or CSV/Nmap data
2. Loads `scaler.pkl` using joblib, scales incoming features
3. Loads `random_forest.pkl`, runs classification
4. Adds placeholder features (`shadow_node_interaction`, `mtd_port_delta`)
5. Dispatches alerts to dashboard via POST routes
6. Supports JSONL logging and local file fallback

### 5.4 Deception Module (`deception/`)

Active defense engine by El Yazid:
- **MTD (Moving Target Defense):** Dynamically shifts active service ports on a pseudo-random schedule using iptables rules and a background thread with PRNG and grace periods
- **Honeypot:** Decoy listeners on old/dead ports; logs attacker probes; sets `shadow_node_interaction=1` flag to boost ML detection
- **Severity mapping:** ML confidence score → defense action (monitor / alert / block / redirect)

Empirical finding: honeypot feedback loop provides +2.3% accuracy improvement.

### 5.5 The Isolation Forest Failure — Majority Anomaly Paradox

Isolation Forest was integrated for detecting "low and slow" stealthy scans. On the static CICIDS2017 dataset, it achieved only 7.89% F1 with 66.94% FPR.

**Root cause:** Anomaly detection assumes anomalies are statistical minority (<5%). In the CICIDS2017 Friday PortScan slice, PortScan represents **55.48%** of data. The IF isolates benign traffic faster than attack traffic, categorizing normal behavior as anomalous.

**Remediation:** Train Isolation Forest exclusively on BENIGN traffic (~100,000 flows) in semi-supervised mode. Test on a downsampled validation set where scans are rare anomalies.

---

## 6. Feature Selection & Data Dictionary

### 6.1 Feature Mapping Table

| Theoretical Feature | CSV Column | Type | Description |
|---------------------|------------|------|-------------|
| Distinct Dest Ports | `Destination Port` | Integer | Proxy for port diversity (scanner signature) |
| SYN Flag Count | `SYN Flag Count` | Binary | TCP SYN scan detection |
| RST Flag Count | `RST Flag Count` | Binary | Connection reset detection |
| Flow Duration | `Flow Duration` | Float | Scan timing signature |
| Total Fwd Packets | `Total Fwd Packets` | Integer | Forward packet count |
| ACK Flag Count | `ACK Flag Count` | Binary | ACK scan detection |
| IAT Mean | `Flow IAT Mean` | Float | Inter-arrival time (scan speed proxy) |
| Bwd Packet Length | `Bwd Packet Length Mean` | Float | Response packet size |
| TCP Window Size | `Init_Win_bytes_forward` | Integer | Initial TCP window |
| Unique Dst IPs | *N/A* | — | Live capture only (absent from CSV) |
| TTL Value | *N/A* | — | Stripped at flow aggregation |
| Shadow Node Interaction | `shadow_node_interaction` | Binary | Placeholder (0 in training, 1 if honeypot hit) |
| MTD Port Delta | `mtd_port_delta` | Integer | Placeholder (0 in training, offset from active port) |

### 6.2 Port Range Entropy (New Feature)

Shannon entropy of destination ports — distinguishes randomized scans from sequential scans. RF-friendly, peer-cited. Added in Hybrid BRD v2.0.

---

## 7. Data Pipeline Mathematics

### 7.1 Winsorization (IQR Capping)

$$IQR = Q_3 - Q_1$$

$$LB = Q_1 - 1.5 \times IQR, \quad UB = Q_3 + 1.5 \times IQR$$

$$x_i = \begin{cases} LB & \text{if } x_i < LB \\ UB & \text{if } x_i > UB \\ x_i & \text{otherwise} \end{cases}$$

### 7.2 Skewness Correction

Fisher Skewness: $\gamma_1 = E\left[\left(\frac{X - \mu}{\sigma}\right)^3\right]$

Any feature with $|\gamma_1| > 1.0$ undergoes: $x'_i = \log(1 + x_i)$ (via `np.log1p`)

### 7.3 SMOTE

For each minority sample, select random neighbor (k=5), generate synthetic point:

$$x_{new} = x_i + \lambda(x_{neighbor} - x_i), \quad \lambda \sim U(0,1)$$

Applied **only** to scaled training set. Test set and unscaled data must never touch SMOTE.

### 7.4 Isolation Forest Anomaly Score

$$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$

where $h(x)$ is path length to isolate point $x$, and $c(n)$ is average path length of unsuccessful BST searches.

---

## 8. Evaluation Results

### 8.1 Model Performance

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC | FPR | Status |
|-------|----------|-----------|--------|-----|---------|-----|--------|
| Random Forest | 99.91% | 99.91% | 99.93% | 99.92% | 0.9997 | 0.11% | PASS |
| XGBoost | 99.91% | 99.91% | 99.94% | 99.92% | 0.9999 | 0.11% | PASS |
| Isolation Forest | 18.22% | 10.52% | 6.32% | 7.89% | N/A | 66.94% | FAIL |

### 8.2 Cross-Validation Stability

- Random Forest CV F1: $0.9993 \pm 0.0003$
- XGBoost CV F1: $0.9994 \pm 0.0003$

### 8.3 Dataset Statistics

- **Total samples:** 286,467
- **Training set:** 229,173 (PortScan: 127,144; BENIGN: 102,029)
- **Test set:** 57,294 (PortScan: 31,786; BENIGN: 25,508)
- **After SMOTE (train only):** 254,288 (balanced 50/50)

---

## 9. Deployment Architecture

```
[Live Network Traffic]
        │
        ▼
[Capture Layer] — Scapy BPF filter, rolling window aggregation per source IP
        │
        ▼
[Feature Extractor] — Pandas windowed aggregation → 9 flow features + 2 placeholders
        │
        ▼
[Bridge Module] — Load scaler.pkl → scale → load random_forest.pkl → classify
        │
        ├── BENIGN ──► [Continue monitoring]
        │
        └── PORT_SCAN ──► [Trigger Response]
                │
                ├──► [Deception] — MTD port shuffle + Honeypot redirect
                │
                └──► [Dashboard] — WebSocket real-time alert, heatmap, scanner profile
```

### 9.1 Response Pipeline

1. **Severity scoring:** ML confidence → severity level (LOW/MEDIUM/HIGH/CRITICAL)
2. **Blocking:** iptables DROP via Python subprocess → audit log → TTL-based auto-unblock
3. **Honeypot:** Fake listener on old/dead ports → probe logging → `shadow_node_interaction=1`
4. **MTD:** Background thread → periodic port shuffle → `mtd_port_delta` computed

### 9.2 Non-Functional Targets

| Requirement | Target |
|-------------|--------|
| Fast scan detection | < 8 seconds |
| Slow scan detection | < 90 seconds (sliding window) |
| Dashboard refresh | <= 5 seconds |
| Blocking response | < 15 seconds (detection → iptables DROP) |

---

## 10. Team & Contribution Attribution

| Team Member | Role | Key Deliverables |
|-------------|------|------------------|
| **Adil Lekhbioui** | Project lead, dashboard, bridge, config, final report | Flask dashboard, bridge middleware, global config, report restructuring (9 chapters, cover page), demo scripts |
| **Khadija** | ML pipeline | Preprocessing, SMOTE, RF/XGBoost/IF training, evaluation, ML report |
| **El Yazid** | Active defense | MTD mutator, honeypot system, iptables rules, defense documentation |
| **Anas Moulay** | VM Integration | VirtualBox topology, network configuration, VM setup guide |
| **Anas ElKartouti** | Documentation | Conception report, BRD, interviews, requirements |

---

## 11. How to Reproduce & Run

### 11.1 Environment Setup

```bash
pip install -r requirements.txt
pip install -r detection/requirements.txt
```

### 11.2 ML Pipeline (Offline)

```bash
cd detection/src/
python data_preprocessing.py    # Clean, winsorize, log-transform → preprocessed.csv
python feature_selection.py     # Correlation analysis
python modeltrain.py            # Scale, SMOTE, 10-fold CV, train models → .pkl files
python evaluate_model.py        # Metrics, confusion matrices, ROC → results/
```

### 11.3 Dashboard (Live)

```bash
cd dashboard/
python app.py
```

### 11.4 Live Demo

```bash
python run_demo.py              # Kali port scan simulation → bridge → dashboard
```

### 11.5 Final Report Compilation

```bash
cd docs/reports/05_final/
pdflatex report.tex             # First pass
bibtex report                   # Bibliography
pdflatex report.tex             # Second pass
pdflatex report.tex             # Third pass (resolve cross-refs)
```

### 11.6 Regenerate Figures

```bash
cd tools/
python regenerate_figures.py    # Rebuild all ML figures from retrained models
```

---

## 12. Commit History — Complete Log

```
c15b515 Move logo files up one directory level from figures/ to 05_final/
aaa6039 restructure final report: 9 chapters, new cover page, fix inconsistencies and orphan refs
98435da Full rewrite of ch04 and ch05 with regenerated figures
894c3f1 Re-include 2 minor sections from Khadija's ML report into ch04
9cc530d Re-include 3 high-value sections from Yazid's defense report into ch07
8ec698f Remove abstract and add VirtualBox environment visuals to ch06
e254934 Remove unused preamble.tex (merged into report.tex)
1afb64f Fix LaTeX report for pdflatex compatibility
275946a Fix LaTeX files for pdflatex compatibility
04b5f1c Add final report skeleton with all 10 chapters
6531834 docs: add Yazid context document
ec0caaa fix: retrain models with current sklearn version
b2b58f5 fix: wire dashboard-to-bridge data flow (POST routes, JSONL, local fallback)
8b2b5b6 docs: consolidate all reports into docs/reports/
b4bee2f chore: reorganize project — consolidate all docs and lab data into repo
9c92a7c merge: resolve conflicts from Adil's push
257e6f7 fix: update all IPs to match Anas M's VirtualBox topology
c826859 fix: resolve all cross-module conflicts from colleague merge
e1af376 Merge remote-tracking branch 'origin/main'
ca6ead5 docs: add defense subsystem LaTeX documentation
76553dd fix: resolve all cross-module conflicts from colleague merge
588c9fe Merge remote-tracking branch 'origin/main'
37bca92 docs: add VM implementation guide for team setup
fdf4fc3 Merge pull request #3 from MrGray17/main
e21c427 fix: retrain models with 11 features (Adil's Data Dictionary config)
7a26cfc Update README.md
8b21ac0 Update README.md
700fbc3 docs: add Anas ElKartouti and Anas Moulay to team
e08e0a4 docs: rewrite README with badges, architecture, results, structure
188b5d0 merge: resolve conflicts — combined .gitignore, kept dashboard, his README
917a979 merge: combine both repos — his ML pipeline + bridge, your dashboard + config
b03184b feat(dashboard): modern SOC-style redesign
cb1dd24 fix: add missing config attrs + venv to gitignore
290441d feat: add live demo — Kali port scan simulation against AEGIS
e5f455e feat(bridge): add CSV/Nmap to ML detection pipeline with offline dashboard dispatch
0ecba16 feat(deception): integrate active defense modules with Flask dashboard
0e76666 doc(detection): add detection/data/README.md with dataset curl link
32ed312 feat(detection): merge Khadija's updated ML pipeline
02b7ef4 feat(deception): merge El Yazid's active defense and deception engine
481552d refactor(config): align global config schema with trained ML models
a019c5c refactor(config): align global config schema with trained ML models
36ef6b4 feat: integrate Aegis Entropy MTD + clean project structure
3a039d4 feat: integrate Aegis Entropy MTD + full ML pipeline + merged dashboard
1288813 Merge pull request #2 from adillekhbioui-collab/merge-khadija-detection
ba13d21 feat(detection): merge Khadija's ML pipeline into central repo
d97dd0d feat(detection): add Khadija ML pipeline — preprocessing, training & report
e24bc1e feat(ml-pipeline): refactor preprocessing, training & evaluation pipeline
b8fb226 Merge pull request #1 from adillekhbioui-collab/feature/dashboard
642d325 refactor(repo): delete all placeholder stubs, create clean folder boundaries
49d7457 feat(dashboard): implement dashboard v2 with D3 heatmap, real-time metrics
9d2e57d ml
a4e0101 Initial commit
32e71fc first commit
1120339 Initial project scaffold
```

---

## 13. Current State & Next Steps

### 13.1 What Is Complete

- [x] ML pipeline — preprocessing, training, evaluation, all models (.pkl) ✅
- [x] Dashboard — Flask + Socket.IO + D3.js SOC-style UI ✅
- [x] Bridge module — capture→detection→dashboard→deception integration ✅
- [x] Deception module — MTD + honeypot (Yazid) ✅
- [x] Capture module — Scapy flow aggregation ✅
- [x] Live demo — Kali attack simulation ✅
- [x] Final report — 9 chapters, cover page, compiles with pdflatex ✅
- [x] Cross-module conflict resolution ✅
- [x] VM configuration documentation ✅

### 13.2 Pending / Optional

- [ ] Real-time capture integration (live traffic → bridge, currently offline/CSV-based)
- [ ] Isolation Forest semi-supervised retraining (BENIGN-only baseline)
- [ ] Multi-class scan type classification (SYN/UDP/ACK/XMAS/Connect)
- [ ] Per-scan-type detection rate table
- [ ] Hyperparameter tuning (GridSearchCV/RandomizedSearchCV)
- [ ] Containerization (Docker)
- [ ] Literature review expansion
- [ ] French résumé (if required by jury)

---

*This document was last updated: **June 15, 2026**. It supersedes all prior context documents including the April 2026 CLAUDE.md snapshot.*
