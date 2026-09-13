# HVAC Fault Detection & AI Diagnostic System

An evolving HVAC automation project that combines traditional fault detection, AI-assisted troubleshooting, and automated service lead management.

The project demonstrates how HVAC domain knowledge can be progressively integrated with Python, cloud automation, AI reasoning, and operational workflows.

---

## 📊 Project Evolution

### **Level 1 — HVAC Fault Detection** ✅

*Foundation: Rule-based fault detection*

A Python-based fault detection system using HVAC operating data such as supply air temperature, setpoint, and cooling command.

**Technology:** Python | Git
**Status:** Complete
**File:** `fault_detection.py`

**Purpose:**

* Demonstrate HVAC fault-detection logic
* Validate sensor data before analysis
* Classify fault severity
* Establish the foundation for future diagnostic intelligence

---

### **Level 2 — AI HVAC Troubleshooting Assistant** ✅

*AI-assisted diagnostic reasoning for HVAC service requests*

Converts HVAC service requests into structured diagnostic briefs that can assist technicians and dispatch teams.

**Workflow:**

1. A service request is submitted with system and problem information.
2. n8n captures and transforms the request.
3. AI analyzes the available HVAC information.
4. The system identifies:

   * Probable faults
   * Possible causes
   * Missing diagnostic information
   * Recommended next diagnostic test
5. A structured technician brief is generated.
6. Results can be delivered through Telegram, Google Sheets, and email.

**Key Components:**

* **AI Reasoning:** Claude
* **Workflow Automation:** n8n Cloud
* **Data Storage:** Google Sheets
* **Communication:** Telegram + Gmail

**Documentation:**
[`docs/ai-hvac-diagnostic-assistant/`](docs/ai-hvac-diagnostic-assistant/)

---

### **Level 3 — AI HVAC Lead Management** ✅

*Automated customer intake, lead qualification, and priority routing*

Converts incoming HVAC customer requests into structured, prioritized leads.

**Workflow:**

1. Customer submits an HVAC request through a Tally form.
2. n8n receives and processes the form submission.
3. AI analyzes the request and determines:

   * HVAC fault classification
   * Severity level
   * Priority score
   * Service urgency
4. The lead is recorded in Google Sheets.
5. Automated notifications are sent to the appropriate channels.
6. The customer receives an automated confirmation.
7. Dispatch teams receive structured lead information for follow-up.

**Key Components:**

* **Lead Capture:** Tally
* **AI Analysis:** Claude
* **Workflow Automation:** n8n Cloud
* **CRM / Data Storage:** Google Sheets
* **Team Notifications:** Telegram
* **Customer Communication:** Gmail

**Documentation:**
[`docs/ai-hvac-lead-management/`](docs/ai-hvac-lead-management/)

---

## 🚀 Future — HVAC Diagnostic Intelligence

The next stage is to connect individual diagnostic cases into a structured company knowledge system.

The planned system will include:

* Technician-validated diagnosis and resolution records
* Historical case matching
* Diagnostic pattern recognition
* Evidence-based troubleshooting
* Recommended next-best tests
* Confidence scoring
* Technician verification
* Reusable diagnostic knowledge
* Continuous improvement from confirmed service cases

### Planned Diagnostic Intelligence Loop

```text
Customer / Technician Request
            ↓
      Extract Information
            ↓
      Safety & Data Quality
            ↓
    Identify Missing Information
            ↓
      Retrieve Relevant Knowledge
            ↓
       Diagnostic Reasoning
            ↓
      Possible Causes + Evidence
            ↓
       Next Best Test
            ↓
       Confidence Assessment
            ↓
      Technician Verification
            ↓
       Confirmed Diagnosis
            ↓
     Diagnostic Case Memory
            ↓
      Future Case Matching
```

The goal is to evolve from simple automation into an HVAC service intelligence system that can support technicians, dispatchers, and service operations.

---

## 🏗️ Architecture Overview

```text
CUSTOMER / TECHNICIAN REQUEST
            │
            ▼
     [TALLY / SERVICE FORM]
            │
            ▼
        [n8n WEBHOOK]
            │
      ┌─────┴─────┐
      ▼           ▼
 [LEAD INTAKE] [DIAGNOSTIC REQUEST]
      │           │
      └─────┬─────┘
            ▼
        [CLAUDE AI]
            │
      ┌─────┼──────────────┐
      ▼     ▼              ▼
 [ANALYSIS] [PRIORITY] [DIAGNOSTIC LOGIC]
      │     │              │
      └─────┴──────┬───────┘
                   ▼
            [GOOGLE SHEETS]
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   [TELEGRAM]   [GMAIL]    [CRM RECORD]
        │          │          │
        └──────────┴──────────┘
                   ▼
             [SERVICE TEAM]
                   │
             ┌─────┴─────┐
             ▼           ▼
     [TECHNICIAN]   [FOLLOW-UP]
```

---

## 📁 Repository Structure

```text
HVAC-fault-detection/
│
├── README.md
├── fault_detection.py
├── DEPLOYMENT_SUMMARY.md
│
├── docs/
│   ├── ai-hvac-diagnostic-assistant/
│   │   ├── README.md
│   │   ├── workflow-architecture.md
│   │   ├── claude-reasoning-process.md
│   │   └── setup-guide.md
│   │
│   └── ai-hvac-lead-management/
│       ├── README.md
│       ├── workflow-architecture.md
│       ├── lead-scoring-criteria.md
│       └── setup-guide.md
│
└── .git/
```

---

## 🚀 Getting Started

### Understand the Project

Start with:

1. This README
2. `fault_detection.py` — Level 1 Python foundation
3. `docs/ai-hvac-diagnostic-assistant/` — Level 2 AI troubleshooting system
4. `docs/ai-hvac-lead-management/` — Level 3 lead management system
5. `DEPLOYMENT_SUMMARY.md` — Overall implementation summary

### Level 2 — Diagnostic Assistant

See:

[`docs/ai-hvac-diagnostic-assistant/setup-guide.md`](docs/ai-hvac-diagnostic-assistant/setup-guide.md)

### Level 3 — Lead Management

See:

[`docs/ai-hvac-lead-management/setup-guide.md`](docs/ai-hvac-lead-management/setup-guide.md)

---

## 💡 Technology Stack

| Component         | Level 1      | Level 2          | Level 3          |
| ----------------- | ------------ | ---------------- | ---------------- |
| **Intake**        | Python       | Service Request  | Tally            |
| **Orchestration** | Python       | n8n Cloud        | n8n Cloud        |
| **AI / Logic**    | Rule-based   | Claude           | Claude           |
| **Storage**       | Runtime data | Google Sheets    | Google Sheets    |
| **Communication** | Console      | Telegram + Gmail | Telegram + Gmail |
| **Automation**    | Local Python | Cloud workflow   | Cloud workflow   |

---

## 🔒 Security & Privacy

This repository does **not** contain:

* API keys
* Authentication credentials
* Customer personal information
* Technician contact information
* Private business data

Credentials and service connections are managed separately through secure configuration and credential-management systems.

---

## 📈 Project Development Philosophy

The project is developed incrementally:

* ✅ Start with simple HVAC logic
* ✅ Validate data before making decisions
* ✅ Add AI-assisted reasoning
* ✅ Automate repetitive service workflows
* ✅ Store structured operational data
* ✅ Keep technician verification in the diagnostic loop
* 🚀 Progress toward reusable HVAC diagnostic intelligence

The objective is not to replace HVAC technicians.

The objective is to **give HVAC service teams better information, faster workflows, and more consistent diagnostic support.**

---

## 📊 Current Status

| Level                                | Status       | Description                                   |
| ------------------------------------ | ------------ | --------------------------------------------- |
| **Level 1 — Python FDD**             | ✅ Complete   | Rule-based HVAC fault detection               |
| **Level 2 — Diagnostic AI**          | ✅ Active     | AI-assisted troubleshooting workflow          |
| **Level 3 — Lead Management**        | ✅ Active     | Automated HVAC lead qualification and routing |
| **Future — Diagnostic Intelligence** | 🚀 In Design | Knowledge-based diagnostic intelligence       |

---

## 🤝 Development Workflow

The project follows an incremental Git-based development process:

1. Develop a feature
2. Test the workflow
3. Document the implementation
4. Commit changes with clear messages
5. Push to GitHub
6. Continue building on the validated foundation

---

## 📝 License

This project is part of Amran Consulting Ltd's HVAC AI initiative.

---

**HVAC knowledge → Python → AI reasoning → Workflow automation → Diagnostic intelligence**
