# Conception Report Generation Guide for AEGIS Entropy

**To the AI Agent:** You are tasked with generating or structuring the Conception Report for the `Portscan_IDS` (AEGIS Entropy) project. You must strictly follow the pedagogical framework outlined below. The professor evaluates this project based on rigorous adherence to specific methodologies (CPS, User Interviews, Data Instruments), not just on the code.

---

## 1. The "CPS" Framework (CRITICAL)
The core of the problem formulation must follow the **CPS (Contexte - Problématique - Solution)** template. This is a rigid 3-paragraph structure that must appear in the introduction.

*   **Paragraphe 1 : Contexte (Mise en situation)**
    *   *Concept:* Describe the current situation in the industry (Security Operations Centers). Explain how tasks are currently done (manual IDS rules) and the difficulties they cause (slowness, false positives, analyst fatigue). State the impact on cost and security.
*   **Paragraphe 2 : Problématique (Le Besoin)**
    *   *Concept:* This paragraph defines the exact problem. You **must** include a formulated question using this exact template format:
    *   *Required Sentence:* *"Comment peut-on **détecter et classifier les attaques de type PortScan** à partir de **données de trafic réseau (pcap/csv)** afin de **protéger l'infrastructure et alerter les équipes SOC en temps réel** ?"*
*   **Paragraphe 3 : Solution (Proposition)**
    *   *Concept:* Propose the AI solution (Apprentissage Supervisé / Classification).
    *   *Requirement:* You must propose **two** distinct AI orientations:
        1.  *Orientée aide à la décision:* The SOC Dashboard (Confidence scores for analysts).
        2.  *Orientée automatisation:* The Active Defense/MTD engine (Automatically blocking IPs via kernel routes).

---

## 2. User Validation & Interviews (La Règle d'Or)
The professor's "Golden Rule" states that an engineer cannot imagine a problem; it must be validated by real users.
*   **The Requirement:** The report must contain a section detailing that interviews were conducted with the target audience (SOC Analysts, Security Engineers, Students).
*   **Existing Content:** You already have the complete, translated interviews located here: `c:\Users\Adill\Documents\Ci_RST_S2\AI\New folder\mini_projet\Portscan_IDS\docs\reports\01_conception\interviews\Guide_et_Entretiens_Complets.md`.
*   **Instruction:** Do not invent new interviews. You must synthesize the 4 existing interviews from that file. Emphasize "Empathy" (listening to the hidden needs of analysts, like reducing false positives and the annoyance of manual blocking). Highlight that the methodology used a mix of *Qualitative* questions ("Why do legacy IDS fail?") and *Quantitative* questions.

---

## 3. Data Collection & "Instruments de Mesure"
For network projects, the professor requires explicit documentation of how data is measured and collected.
*   **Hybrid Sources:** The data comes from two sources:
    1.  *Internet (Open-Source):* The CIC-IDS2017 dataset from the University of New Brunswick (used for baseline training).
    2.  *Soi-même (Self-Collection):* Live traffic generated for the demo.
*   **Instruments de Mesure:** You must explicitly list the physical/software tools used to "measure" the reality:
    *   **Nmap:** The instrument used to generate the anomaly (Portscans).
    *   **Wireshark / Scapy:** The instruments used to capture the network packets.
*   **Étalonnage (Calibration):** You must include a sentence stating that "Before official collection, the instruments (Nmap/Scapy) were calibrated and tested in a controlled lab environment to ensure measurement accuracy."

---

## 4. Dictionnaire de Données (Data Dictionary)
The report must include a clear table identifying the variables used by the AI.
*   **Inputs (X) / Variables Explicatives:** Flow Duration, Packet Length, Flags, etc.
*   **Output (Y) / Variable Cible:** Label (Benign vs PortScan).
*   **Classification:** Explicitly state which features are *Quantitatives* (e.g., Duration) and which are *Qualitatives / Catégorielles* (e.g., Destination Port).

---

## 5. Qualité et Pré-traitement des Données (Data Cleaning)
The professor places immense weight on how "Invalid Data" is handled. Structure this section to match the actual ML pipeline:
*   **Données Invalides:** Explain that `NaN` and Infinite values were replaced by the mathematical *médiane*.
*   **Valeurs Aberrantes (Outliers):** Network traffic contains extreme outliers naturally. Explain that deleting them would destroy attack data. Instead, the pipeline uses the **IQR (Interquartile Range)** method to *cap/clamp* outliers at `Q3 + 1.5*IQR`.
*   **Mise à l'échelle (Standardisation vs Normalisation):** Explain that features like `Flow Duration` are in the millions, while `SYN Flags` are 0 or 1. To fix this difference in scale, the pipeline applies a **Log Transform (np.log1p)** followed by **Z-Score Standardisation (StandardScaler)**.

---

## 6. Required Table of Contents
Please structure the Conception Report using exactly this outline:

1. **Introduction: Cadre du Projet (Format CPS)**
2. **Définition des Objectifs (SMART)**
3. **Identification et Interviews du Public Cible (5 Interviews)**
4. **Stratégie de Collecte de Données**
5. **Instruments de Mesure Réseaux et Étalonnage**
6. **Dictionnaire des Données (X et Y)**
7. **Audit de Qualité et Pré-traitement des Données**
8. **Modélisation et Solutions IA Proposées**
