#!/usr/bin/env python3
# generate_brd.py  —  fpdf 1.7.2 compatible
from fpdf import FPDF

# ─────────────────── palette ──────────────────
DARK_BG    = (15,  23,  42)
ACCENT     = (6,  182, 212)
ACCENT2    = (16, 185, 129)
LIGHT      = (241, 245, 249)
TEXT_DARK  = (15,  23,  42)
TEXT_LIGHT = (248, 250, 252)
ROW_ALT    = (226, 232, 240)
GREY       = (100, 116, 139)


def rgb(t):
    return t[0], t[1], t[2]


class BRD(FPDF):

    # ── margins / page ────────────────────────
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*DARK_BG)
        self.rect(0, 0, 210, 12, 'F')
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*ACCENT)
        self.set_xy(10, 3)
        self.cell(0, 6, 'PortScan & Recon IDS/IPS  |  Hybrid BRD v2.0  |  AI Module')

    def footer(self):
        self.set_y(-12)
        self.set_fill_color(*DARK_BG)
        self.rect(0, 284, 210, 13, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*ACCENT)
        self.cell(0, 8, f'Page {self.page_no()}  |  AI Academic Project  |  ENSA', align='C')

    # ── cover ─────────────────────────────────
    def cover(self):
        self.add_page()
        self.set_fill_color(*DARK_BG)
        self.rect(0, 0, 210, 297, 'F')
        # top bar
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, 210, 4, 'F')
        # left strip
        self.set_fill_color(*ACCENT2)
        self.rect(0, 4, 5, 293, 'F')

        # badge
        self.set_fill_color(31, 41, 55)
        self.rect(18, 20, 80, 14, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*ACCENT)
        self.set_xy(18, 24)
        self.cell(80, 6, 'HYBRID BRD  v2.0', ln=0, align='C')

        # title
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(*TEXT_LIGHT)
        self.set_xy(18, 44)
        self.multi_cell(180, 12, 'AI-Based IDS/IPS\nPortScan & Network\nReconnaissance')

        # divider
        self.set_fill_color(*ACCENT)
        self.rect(18, 105, 165, 1, 'F')

        self.set_font('Helvetica', '', 12)
        self.set_text_color(148, 163, 184)
        self.set_xy(18, 110)
        self.multi_cell(180, 7, 'Decision-Making Needs Expression\nAI Lifecycle  |  Full CRISP-DM Scope')

        # metadata box
        self.set_fill_color(31, 41, 55)
        self.rect(18, 132, 175, 70, 'F')
        meta = [
            ('Module',       'Artificial Intelligence'),
            ('Attack Focus', 'Port Scanning & Network Reconnaissance'),
            ('Status',       'Academic Project  |  Final Submission'),
            ('Team',         '5 Members (ENSA Engineering)'),
            ('Version',      'Hybrid BRD v2.0 (April 2026)'),
            ('Severity',     'MEDIUM-HIGH'),
        ]
        y = 138
        for lbl, val in meta:
            self.set_xy(26, y)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*ACCENT)
            self.cell(44, 6, lbl + ':', ln=0)
            self.set_font('Helvetica', '', 9)
            self.set_text_color(*TEXT_LIGHT)
            self.cell(110, 6, val, ln=0)
            y += 8

        # hybrid badge
        self.set_fill_color(*ACCENT2)
        self.rect(18, 215, 175, 20, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*DARK_BG)
        self.set_xy(18, 219)
        self.multi_cell(175, 6,
            'Hybrid Design: BRD AI Core + Honeypot Response Layer\n'
            '+ 5-Person Team Roles + Week-by-Week Execution Timeline',
            align='C')

        self.set_font('Helvetica', '', 8)
        self.set_text_color(*GREY)
        self.set_xy(18, 272)
        self.cell(0, 6, 'Prepared by Team  |  AI Module  |  Semester 2  |  April 2026')

    # ── section bar ───────────────────────────
    def section(self, num, title):
        self.ln(5)
        x, y = self.get_x(), self.get_y()
        self.set_fill_color(*DARK_BG)
        self.rect(x, y, 190, 9, 'F')
        self.set_fill_color(*ACCENT)
        self.rect(x, y, 4, 9, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*TEXT_LIGHT)
        self.set_xy(x + 8, y)
        self.cell(0, 9, f'{num}. {title}', ln=1)
        self.ln(2)

    def subsection(self, title):
        x, y = self.get_x(), self.get_y()
        self.set_fill_color(*ACCENT2)
        self.rect(x, y, 3, 6, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*TEXT_DARK)
        self.set_xy(x + 6, y)
        self.cell(0, 6, title, ln=1)
        self.ln(1)

    def body(self, txt):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*TEXT_DARK)
        self.multi_cell(0, 5.5, txt)
        self.ln(2)

    def bullet(self, txt):
        x0 = self.get_x()
        self.set_x(x0 + 4)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*ACCENT)
        self.cell(5, 5.5, '*', ln=0)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*TEXT_DARK)
        self.multi_cell(175, 5.5, txt)

    def info_box(self, title, lines, color=None):
        color = color or DARK_BG
        h = 7 + len(lines) * 5.5 + 4
        x0, y0 = self.get_x(), self.get_y()
        self.set_fill_color(*color)
        self.rect(x0, y0, 190, h, 'F')
        self.set_fill_color(*ACCENT)
        self.rect(x0, y0, 4, h, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*ACCENT2)
        self.set_xy(x0 + 8, y0 + 1)
        self.cell(180, 7, title, ln=1)
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(*TEXT_LIGHT)
        for line in lines:
            self.set_x(x0 + 8)
            self.multi_cell(180, 5.5, line)
        self.ln(3)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            n = len(headers)
            col_widths = [190 // n] * n
        self.set_fill_color(*DARK_BG)
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*ACCENT)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, ' ' + h, border=0, fill=1, ln=0)
        self.ln()
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*TEXT_DARK)
        for ri, row in enumerate(rows):
            fc = ROW_ALT if ri % 2 == 0 else (255, 255, 255)
            self.set_fill_color(*fc)
            for ci, val in enumerate(row):
                self.cell(col_widths[ci], 6.5, ' ' + str(val), border=0, fill=1, ln=0)
            self.ln()
        self.ln(2)

    def feature_table(self, rows):
        cols = [50, 90, 50]
        rel_colors = {
            'Critical': (180, 20,  20),
            'Very':     (200, 80,   0),
            'High':     (160, 100,  0),
            'Medium':   ( 20, 140, 60),
            'Low':      ( 80, 100,120),
        }
        self.set_fill_color(*DARK_BG)
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*ACCENT)
        for h, w in zip(['Feature Name', 'Description', 'Relevance'], cols):
            self.cell(w, 7, ' ' + h, fill=1, ln=0)
        self.ln()
        self.set_font('Helvetica', '', 8)
        for ri, (fname, fdesc, frel) in enumerate(rows):
            fc = ROW_ALT if ri % 2 == 0 else (255, 255, 255)
            self.set_fill_color(*fc)
            self.set_text_color(*TEXT_DARK)
            self.cell(cols[0], 6.5, ' ' + fname, fill=1, ln=0)
            self.cell(cols[1], 6.5, ' ' + fdesc,  fill=1, ln=0)
            rc = rel_colors.get(frel.split()[0], TEXT_DARK)
            self.set_text_color(*rc)
            self.set_font('Helvetica', 'B', 8)
            self.cell(cols[2], 6.5, ' ' + frel, fill=1, ln=1)
            self.set_font('Helvetica', '', 8)
        self.ln(2)


# ══════════════════════════════════════════════
pdf = BRD()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(10, 15, 10)
pdf.cover()

# ── 1. Executive Summary ──────────────────────
pdf.add_page()
pdf.section('1', 'Executive Summary')
pdf.body(
    'This document presents the formal Needs Expression for the design, implementation, testing, '
    'and validation of an AI model dedicated to real-time detection and automated mitigation of '
    'Port Scanning and Network Reconnaissance attacks within a controlled LAN.\n\n'
    'Reconnaissance is the first phase of any cyberattack kill chain. Attackers probe the network '
    'to map active hosts, open ports, and running services before launching a targeted attack. '
    'Early detection and containment of this phase prevents subsequent, more destructive intrusions.\n\n'
    'This Hybrid BRD v2.0 extends the original scope with: (1) an optional Honeypot redirect '
    'layer for attacker intelligence gathering, (2) a week-by-week execution timeline, and (3) '
    'explicit 5-person team role assignments  all aligned to the core AI/ML pipeline.'
)

# ── 2. Problem Statement ──────────────────────
pdf.section('2', 'Problem Statement')
pdf.body(
    'Port scanning in its various forms (SYN, ACK, UDP, XMAS, FIN scan) produces distinctive traffic '
    'patterns fundamentally different from normal user activity. An attacker running Nmap sends probes '
    'to hundreds of ports in rapid succession, producing anomalous SYN packet distributions, RST '
    'responses, and unanswered connections.\n\n'
    'The core challenge is detecting stealthy or slow-rate scans where attackers deliberately space '
    'probes over time to evade threshold-based IDS systems. This requires ML models capable of '
    'identifying behavioral anomalies across time windows, not instantaneous packet analysis.'
)

# ── 3. Project Objectives ─────────────────────
pdf.section('3', 'Project Objectives')
pdf.table(
    ['Objective', 'Description'],
    [
        ('Primary Detection',   'Train ML model to detect port scanning and recon traffic on the LAN'),
        ('Scan Type Coverage',  'Detect SYN Scan (stealth), TCP Connect, UDP, ACK, and XMAS variants'),
        ('Slow Scan Detection', 'Identify slow/distributed scans that evade threshold-based IDS'),
        ('Attacker Profiling',  'Profile: source IP, MAC, scan type inferred, ports probed, duration'),
        ('Real-time Alerting',  'Trigger alerts with scan type, confidence score, and risk level'),
        ('Automated Response',  'Block scanning IP via iptables; optional honeypot redirect'),
    ],
    col_widths=[58, 132]
)

# ── 4. Functional Requirements ────────────────
pdf.section('4', 'Functional Requirements')
pdf.subsection('4.1  System Inputs')
for b in [
    'Raw TCP/UDP packets on LAN interface, filtered for SYN-only or partial handshake connections',
    'Training datasets: CICIDS2017 (PortScan ~158K flows) and UNSW-NB15 (Reconnaissance ~13K records)',
    'Sliding time-window aggregated features per source IP: 10-second and 60-second windows',
    'Network metadata: src/dst IP, MAC, port, protocol, TCP flags, TTL, timestamp',
]:
    pdf.bullet(b)
pdf.ln(2)
pdf.subsection('4.2  System Outputs')
for b in [
    'Real-time dashboard: unique ports probed per source IP, port heat map, active scanners list',
    'Classification per window: BENIGN or PORT_SCAN with inferred scan type and confidence score',
    'Attacker profile: source IP, MAC, targeted hosts, port range probed, first/last seen timestamps',
    'Alert with scan type label (SYN / Full Connect / UDP / Stealth) and severity score',
    'iptables DROP rule for scanning source IP with event logged to database',
    '[OPTIONAL] Honeypot: redirect scanner to fake listener on original IP, log all probes',
]:
    pdf.bullet(b)

# ── 5. Dataset Specification ──────────────────
pdf.section('5', 'Dataset Specification')
pdf.table(
    ['Dataset', 'Subset', 'Samples (approx.)', 'Source', 'Status'],
    [
        ('CICIDS2017',      'PortScan category',        '~158,000 flows',  'UNB / CIC',      'PRIMARY'),
        ('UNSW-NB15',       'Reconnaissance category',  '~13,000 records', 'UNSW Australia', 'SECONDARY'),
        ('CAIDA Telescope', 'Backscatter / SYN probes', 'Variable',        'CAIDA.org',      'OPTIONAL'),
    ],
    col_widths=[38, 48, 36, 36, 32]
)
pdf.info_box(
    'Dataset Rationale',
    [
        'CICIDS2017: modern IDS benchmark with labeled attack flows and realistic traffic patterns.',
        'UNSW-NB15: adds diversity  different capture environment and attack representation.',
        'KDD-99 (1999) explicitly REJECTED  universally obsolete in IDS literature since 2010.',
    ]
)

# ── 6. Key Features ───────────────────────────
pdf.section('6', 'Key Network Features for the ML Model')
pdf.feature_table([
    ('Distinct Dst Ports/IP', '# unique destination ports per source',        'Critical  core scanning signature'),
    ('SYN Flag Count',        'SYN sent without completing handshake',         'Critical  stealth SYN scan'),
    ('RST Flag Count',        'RST responses from closed ports',               'Very High  port probe rejection'),
    ('Flow Duration',         'Duration of each individual probe connection',  'High  very short in fast scans'),
    ('Total Fwd Packets',     'Packets per flow from scanner',                 'High  usually 1 per probe'),
    ('IAT Mean',              'Mean inter-arrival time between probes',        'High  slow scans have large IAT'),
    ('ACK Flag Count',        'ACK packets without prior SYN',                'Medium  ACK scan detection'),
    ('Unique Dst IPs/Src',    '# distinct destination hosts contacted',       'Medium  host discovery phase'),
    ('Bwd Packet Length',     'Response packet size (RST vs SYN-ACK ratio)',  'Medium  bidirectional profile'),
    ('TTL Value',             'Time-to-live in IP header',                    'Low  OS fingerprinting'),
    ('Port Range Entropy',    'Shannon entropy of destination ports',         'High  randomized vs sequential'),
])
pdf.info_box(
    'Feature Engineering Notes',
    [
        'Port Range Entropy (NEW addition): high entropy signals randomized scans  RF-friendly, peer-cited.',
        'Compute all features per (src_ip, 10s window) AND (src_ip, 60s window) independently.',
        'SMOTE applied on training fold only  never on validation or test splits  prevents leakage.',
    ]
)

# ── 7. ML Model Strategy ──────────────────────
pdf.section('7', 'Machine Learning Model Strategy')
pdf.table(
    ['Component', 'Detail'],
    [
        ('Primary Model',         'Random Forest Classifier  high-dimensional tabular data, feature importance'),
        ('Comparison Model',      'XGBoost  gradient boosting compared on time-windowed aggregated features'),
        ('Slow Scan Layer',       'Isolation Forest (unsupervised) on 60-second sliding window per source IP'),
        ('Imbalance Handling',    'SMOTE applied on training split only  prevents data leakage'),
        ('Hyperparameter Tuning', 'GridSearchCV / RandomizedSearchCV on RF and XGBoost'),
        ('Evaluation Metrics',    'Accuracy, Precision, Recall, F1-Score, AUC-ROC, per-scan-type detection rate'),
        ('Validation Strategy',   'Stratified K-Fold (k=10) + temporal holdout (last 20% chronologically)'),
        ('v1 Output',             'Binary: BENIGN vs PORT_SCAN with confidence score'),
        ('v2+ Output',            'Multi-class: SYN / UDP / ACK / XMAS / Connect Scan'),
    ],
    col_widths=[58, 132]
)

# ── 8. Non-Functional Requirements ────────────
pdf.section('8', 'Non-Functional Requirements')
pdf.table(
    ['Requirement', 'Criterion', 'Target'],
    [
        ('Fast Scan Detection',  'Detection time for aggressive Nmap scan',      '< 8 seconds'),
        ('Slow Scan Detection',  'Detection time for stealthy / slow scan',       '< 90s (sliding window)'),
        ('Model F1-Score',       'On CICIDS2017 PortScan test subset',            '>= 88%'),
        ('Model Accuracy',       'Overall classification on test set',             '>= 90%'),
        ('False Positive Rate',  'Normal connections flagged as scans',            '< 6%'),
        ('Dashboard Refresh',    'Scanner activity heat map update frequency',     '<= 5 seconds'),
        ('Blocking Response',    'Time from detection to iptables DROP rule',      '< 15 seconds'),
    ],
    col_widths=[55, 95, 40]
)

# ── 9. System Architecture ────────────────────
pdf.section('9', 'System Architecture Vision')
layers = [
    ('Capture Layer',
     'Scapy BPF filter on LAN interface (SYN-only or full TCP/UDP)\n'
     '  Rolling aggregation per source IP over 10s and 60s windows'),
    ('Feature Layer',
     'Pandas windowed aggregation -> feature vector per (src_ip, time_window)\n'
     '  Port Range Entropy, SMOTE applied on training split only'),
    ('Detection Layer',
     'v1: RF binary classifier -> BENIGN / PORT_SCAN + confidence score\n'
     '  v2+: multi-class scan type (SYN / UDP / ACK / XMAS)\n'
     '  Parallel: Isolation Forest on 60s window for slow scan anomalies'),
    ('Response Layer',
     'Alert: severity score + scan type -> event store\n'
     '  Blocking: iptables DROP via Python subprocess -> audit log\n'
     '  [OPTIONAL] Honeypot: redirect scanner to fake listener -> log all probes'),
    ('Observability Layer',
     'Real-time dashboard -> Active scanners list, Port activity heat map\n'
     '  Attacker profile (IP, MAC, ports probed, first/last seen timestamps)\n'
     '  Alert feed with confidence, severity, and scan type label'),
]
for name, desc in layers:
    x, y = pdf.get_x(), pdf.get_y()
    pdf.set_fill_color(*DARK_BG)
    pdf.rect(x, y, 190, 7, 'F')
    pdf.set_fill_color(*ACCENT2)
    pdf.rect(x, y, 4, 7, 'F')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*TEXT_LIGHT)
    pdf.set_xy(x + 8, y)
    pdf.cell(0, 7, name, ln=1)
    x2, y2 = pdf.get_x(), pdf.get_y()
    nlines = desc.count('\n') + 1
    bh = nlines * 5.5 + 4
    pdf.set_fill_color(*LIGHT)
    pdf.rect(x2, y2, 190, bh, 'F')
    pdf.set_fill_color(*ACCENT2)
    pdf.rect(x2, y2, 3, bh, 'F')
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(*TEXT_DARK)
    pdf.set_xy(x2 + 6, y2 + 2)
    pdf.multi_cell(182, 5.5, desc)
    pdf.ln(2)

# ── 10. Honeypot Layer (NEW) ──────────────────
pdf.add_page()
pdf.section('10', 'Honeypot Response Layer  [NEW  Hybrid v2.0]')
pdf.body(
    'The Honeypot layer is an optional but recommended addition. When the IDS classifies a source IP as '
    'PORT_SCAN with confidence >= 0.85, instead of (or in addition to) an iptables DROP, the system '
    'redirects the attacker to a lightweight fake listener. This fake service mimics open ports, responds '
    'with plausible banners, and logs every probe  providing rich attacker intelligence without exposing '
    'real services.'
)
pdf.subsection('10.1  How It Works')
for b in [
    'Detection Layer raises PORT_SCAN alert with confidence >= 0.85 for the source IP.',
    'Response Layer issues iptables REDIRECT: traffic from attacker IP -> honeypot listener port.',
    'Honeypot process (Python socket server) accepts connections, returns fake banners (SSH, HTTP, FTP).',
    'All interactions are logged: timestamp, port probed, banner grabbing attempts, payloads sent.',
    'After TTL expiry the iptables rule is removed; attacker loses access to the fake listener.',
]:
    pdf.bullet(b)
pdf.ln(2)
pdf.subsection('10.2  Implementation Scope')
pdf.table(
    ['Component', 'Tool', 'Effort'],
    [
        ('Fake listener (Python socket)',   'Python stdlib socket module',       '~2 hours'),
        ('Attacker probe logger',           'SQLite / structured JSON log',      '~1 hour'),
        ('iptables REDIRECT rule',          'Python subprocess + netfilter',     '~1 hour'),
        ('Dashboard integration',           'Add Honeypot Activity tab',         '~2 hours'),
        ('Banner database (SSH/HTTP/FTP)',  'Static string constants',            '~30 min'),
    ],
    col_widths=[76, 70, 44]
)
pdf.info_box(
    'Academic Value of the Honeypot',
    [
        'Adds a Deployment & Response chapter to the CRISP-DM report with concrete attacker intelligence output.',
        'Zero risk to real services  completely isolated fake listener process on a dedicated port.',
        'Total implementation time: ~6-7 hours. DEFER to Phase 4 if time is tight.',
        'Do NOT implement IP Polymorphism or Port Hopping  sysadmin tasks with zero AI grading value.',
    ]
)

# ── 11. Team Roles (NEW) ──────────────────────
pdf.section('11', '5-Person Team Role Assignments  [NEW  Hybrid v2.0]')
pdf.body(
    'Each role maps to a deliverable that contributes to the AI lifecycle documentation grade. '
    'No role involves IP Polymorphism or Port Hopping. Every member owns a graded chapter of the final report.'
)
roles = [
    ('Role 1', 'ML Pipeline Lead',                'Adil Lekhbioui (confirmed)',
     ['Download & preprocess CICIDS2017 PortScan and UNSW-NB15 datasets',
      'Implement SMOTE, time-window aggregation, Port Range Entropy feature',
      'Train RF and XGBoost; run GridSearchCV tuning; generate comparison table',
      'Report chapters: Data Preparation + Modeling']),
    ('Role 2', 'Anomaly & Slow Scan Specialist',   'TBC',
     ['Implement Isolation Forest on 60s sliding window per source IP',
      'Calibrate contamination parameter, validate against labeled slow scans',
      'Integrate IF output with RF confidence in unified alert score',
      'Report chapters: Unsupervised detection layer + evaluation results']),
    ('Role 3', 'Capture & Feature Pipeline',       'TBC',
     ['Write Scapy listener with BPF filter (SYN-only / full TCP-UDP)',
      'Implement rolling aggregation windows (10s, 60s) per source IP',
      'Compute all features from Section 6 in real time',
      'Report chapters: Data Understanding + architecture diagram']),
    ('Role 4', 'Dashboard & Alert System',         'TBC',
     ['Build real-time dashboard (Flask + Socket.IO + D3.js recommended)',
      'Implement port heat map, active scanners list, attacker profile view',
      'Integrate alert feed (scan type, confidence, severity, timestamp)',
      'Implement optional Honeypot Activity dashboard tab',
      'Report chapters: Deployment architecture + demo recording']),
    ('Role 5', 'Attack Simulation & Documentation','TBC',
     ['Run Nmap scan types (SYN, UDP, ACK, XMAS, Connect) against test VM',
      'Implement optional Honeypot listener (Python socket server)',
      'Produce per-scan-type detection rate table from live tests',
      "Write literature review, ethical considerations, French abstract",
      'Report chapters: Problem Statement + Evaluation results']),
]
for role_num, role_title, assignee, duties in roles:
    x, y = pdf.get_x(), pdf.get_y()
    pdf.set_fill_color(*DARK_BG)
    pdf.rect(x, y, 190, 8, 'F')
    pdf.set_fill_color(*ACCENT)
    pdf.rect(x, y, 4, 8, 'F')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*ACCENT2)
    pdf.set_xy(x + 8, y)
    pdf.cell(28, 8, role_num + ':', ln=0)
    pdf.set_text_color(*TEXT_LIGHT)
    pdf.cell(90, 8, role_title, ln=0)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 8, 'Assigned: ' + assignee, ln=1)
    for d in duties:
        pdf.bullet(d)
    pdf.ln(2)

# ── 12. Timeline (NEW) ────────────────────────
pdf.add_page()
pdf.section('12', 'Week-by-Week Execution Timeline  [NEW  Hybrid v2.0]')
pdf.body('Each week maps to a concrete CRISP-DM deliverable.')
phases = [
    ('Phase 1  Design & Setup', [
        ('Wk 1', 'VM creation (Ubuntu IDS, Kali attacker), network isolation, Git repo, role confirmation',  'R3+R5', 'Network diagram, Git repo'),
        ('Wk 1', 'Download CICIDS2017 + UNSW-NB15, EDA: class distribution, missing values, stats',          'R1',    'Data understanding report'),
    ]),
    ('Phase 2  Implementation', [
        ('Wk 2', 'Data preprocessing: SMOTE, time-window aggregation (10s/60s), Port Range Entropy',         'R1+R3', 'Clean dataset + feature set'),
        ('Wk 2', 'Scapy live capture: BPF filter, rolling aggregation, real-time feature vector output',    'R3',    'capture_pipeline.py'),
        ('Wk 3', 'Train RF and XGBoost: baseline -> GridSearchCV tuning -> model comparison table',          'R1',    'Trained .pkl + comparison table'),
        ('Wk 3', 'Isolation Forest: contamination tuning, integration with RF confidence scores',            'R2',    'slow_scan_detector.py'),
        ('Wk 4', 'Flask/D3.js dashboard: heat map, active scanners, alert feed, attacker profile',          'R4',    'dashboard/ module'),
        ('Wk 4', 'iptables blocking engine: Python subprocess, TTL auto-unblock, audit log',                'R3+R4', 'response_engine.py'),
    ]),
    ('Phase 3  Testing', [
        ('Wk 5', 'Attack simulation: Nmap SYN/Connect/UDP/XMAS/ACK scans against test VM',                  'R5',    'Per-scan detection rate table'),
        ('Wk 5', 'False positive testing: legitimate traffic scenarios (file transfers, browsing)',           'R2+R5', 'FPR measurement report'),
        ('Wk 5', 'Honeypot: fake listener, probe logger, iptables REDIRECT rule [OPTIONAL]',                'R5',    'honeypot.py'),
    ]),
    ('Phase 4  Validation & Report', [
        ('Wk 6', 'K-Fold cross-validation (k=10) + temporal holdout evaluation + AUC-ROC curves',          'R1+R2', 'Validation chapter + graphs'),
        ('Wk 6', 'End-to-end integration test: live scan -> detection -> alert -> block',                   'All',   'Demo recording'),
        ('Wk 7', 'Final report: CRISP-DM structure, literature review, ethical considerations',             'All',   'Final report PDF'),
        ('Wk 7', 'French abstract (resume), English abstract, architecture diagram, slides',                'R5',    'Submission package'),
    ]),
]
cw = [14, 98, 22, 56]
for phase_name, weeks in phases:
    x, y = pdf.get_x(), pdf.get_y()
    pdf.set_fill_color(*ACCENT2)
    pdf.rect(x, y, 190, 7, 'F')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*DARK_BG)
    pdf.set_xy(x + 4, y)
    pdf.cell(0, 7, phase_name, ln=1)
    pdf.set_fill_color(*DARK_BG)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(*ACCENT)
    for w, h in zip(cw, ['Week', 'Activities', 'Owner', 'Deliverable']):
        pdf.cell(w, 6, ' ' + h, fill=1, ln=0)
    pdf.ln()
    pdf.set_font('Helvetica', '', 7.5)
    for ri, (wk, act, owner, deliv) in enumerate(weeks):
        fc = ROW_ALT if ri % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*fc)
        pdf.set_text_color(*TEXT_DARK)
        pdf.cell(cw[0], 6, ' ' + wk,  fill=1, ln=0, align='C')
        pdf.cell(cw[1], 6, ' ' + (act[:84] + ('...' if len(act) > 84 else '')), fill=1, ln=0)
        pdf.set_text_color(*ACCENT2)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.cell(cw[2], 6, ' ' + owner, fill=1, ln=0, align='C')
        pdf.set_text_color(*TEXT_DARK)
        pdf.set_font('Helvetica', '', 7.5)
        pdf.cell(cw[3], 6, ' ' + deliv, fill=1, ln=1)
    pdf.ln(3)

# ── 13. Phases & Deliverables ─────────────────
pdf.section('13', 'Project Phases & Deliverables')
pdf.table(
    ['Phase', 'Activities', 'Key Deliverables'],
    [
        ('1  Design',         'LAN topology, time-window feature design, scan type taxonomy', 'Network diagram, feature set document, scan taxonomy'),
        ('2  Implementation', 'CICIDS2017 preprocessing, RF+XGBoost+IF training, capture pipeline, dashboard', 'Trained .pkl models, IDS pipeline, port heat map dashboard'),
        ('3  Testing',        'Simulate Nmap SYN/Connect/UDP/XMAS; measure per-type detection rate', 'Per-scan detection table, ROC curves, FPR results'),
        ('4  Validation',     'K-Fold cross-validation, temporal holdout, end-to-end scenario', 'Final report, demo recording, multi-model comparison table'),
    ],
    col_widths=[26, 92, 72]
)

# ── 14. Technical Stack ───────────────────────
pdf.section('14', 'Technical Stack Summary')
pdf.table(
    ['Component', 'Tool / Library', 'Notes'],
    [
        ('OS / Virtualization',  'Ubuntu Server (IDS), Kali Linux (attacker), GNS3 / VirtualBox', ''),
        ('Programming Language', 'Python 3.10+',                                                   ''),
        ('Traffic Capture',      'Scapy (BPF), PyShark, sliding window aggregation',               ''),
        ('ML Libraries',         'Scikit-learn, XGBoost, imbalanced-learn, Pandas, NumPy',         ''),
        ('Web Dashboard',        'Flask + Socket.IO + D3.js',                                       'Alt: Grafana + InfluxDB'),
        ('Blocking Engine',      'Linux iptables DROP/REDIRECT via Python subprocess, TTL unblock', ''),
        ('Attack Simulation',    'Nmap (SYN/ACK/UDP/XMAS/Connect), Masscan, Scapy scripts',        ''),
        ('Honeypot (optional)',  'Python socket + SQLite probe log + iptables REDIRECT',            'NEW v2.0'),
        ('Version Control',      'Git + GitHub  feature branches per module',                       ''),
    ],
    col_widths=[44, 108, 38]
)

# ── 15. Success Criteria ──────────────────────
pdf.section('15', 'Expected Outcomes & Success Criteria')
for c in [
    'Model achieves F1-Score >= 88% on CICIDS2017 PortScan test subset.',
    'Nmap SYN stealth scan detected and alert triggered within 8 seconds of initiation.',
    'Slow-rate scan (1 probe/second) detected within the 90-second analysis window.',
    'Dashboard heat map correctly highlights targeted ports and the scanning source IP.',
    'Attacker profile correctly identifies scan type (SYN / UDP / ACK / XMAS) in most cases.',
    'Legitimate traffic produces a false positive rate below 6%.',
    '[OPTIONAL] Honeypot successfully logs attacker probes after iptables REDIRECT is applied.',
]:
    x0 = pdf.get_x()
    pdf.set_x(x0 + 4)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*ACCENT2)
    pdf.cell(6, 6, '[OK]', ln=0)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*TEXT_DARK)
    pdf.multi_cell(178, 6, c)

pdf.ln(4)
pdf.info_box(
    'CRISP-DM Chapter Coverage Checklist',
    [
        '[ ] 1. Business Understanding   Sections 1-3 of this BRD',
        '[ ] 2. Data Understanding       Section 5 (datasets) + Section 6 (features)',
        '[ ] 3. Data Preparation         SMOTE, time-window aggregation (Section 7)',
        '[ ] 4. Modeling                 RF + XGBoost + Isolation Forest (Section 7)',
        '[ ] 5. Evaluation               K-Fold, temporal holdout, comparison table (Section 8)',
        '[ ] 6. Deployment               Architecture (Sec 9), Honeypot (Sec 10), Dashboard',
        '[ ] Extras (for top grade)      Literature review, ethical considerations, French abstract',
    ]
)

out = r'c:\Users\Adill\Documents\Ci_RST_S2\AI\mini_projet\PortScan_IDS_Hybrid_BRD_v2.pdf'
pdf.output(out)
print(f'PDF generated successfully: {out}')

