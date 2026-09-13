# HVAC Fault Detection & AI Diagnostic System

A comprehensive evolution from basic Python fault detection to production AI-powered HVAC service automation.

---

## 📊 Project Evolution Map

### **Level 1 — HVAC Fault Detection** ✅
*Foundation: Rule-based temperature monitoring*

Basic Python logic detecting HVAC faults using supply air temperature, setpoint, and cooling command.

**Technology:** Python | Git
**Status:** Complete (see `fault_detection.py`)
**Purpose:** Proof-of-concept for fault detection logic

---

### **Level 2 — AI HVAC Troubleshooting Assistant** ✅
*Scaling: Cloud-based AI reasoning for technician support*

Converts service requests into AI-assisted diagnostic briefs with detailed reasoning.

**What happens:**
1. Technician submits service request (system type, problem, urgency)
2. n8n webhook captures and transforms request data
3. Claude AI applies HVAC expertise:
   - Identifies probable faults
   - Suggests likely causes
   - Identifies missing diagnostic information
   - Recommends next best test
4. System formats technician brief (Telegram + Google Sheets + Email)
5. Dispatch team acts with AI-informed guidance

**Key Components:**
- **AI Reasoning:** Claude 3.5 Sonnet (HVAC domain knowledge)
- **Workflow Automation:** n8n (cloud-based orchestration)
- **Data Storage:** Google Sheets (service request log)
- **Team Communication:** Telegram + Gmail (real-time dispatch)

**Documentation:** See [`docs/ai-hvac-diagnostic-assistant/`](docs/ai-hvac-diagnostic-assistant/)

---

### **Level 3 — AI HVAC Lead Management** ✅
*Optimization: Automated customer lead scoring & prioritization*

Converts customer inquiries into priority-scored leads with instant response routing.

**What happens:**
1. Customer submits HVAC request via Tally form
2. n8n webhook receives form data
3. Claude AI scores the lead:
   - Fault classification
   - Severity level (CRITICAL/HIGH/MEDIUM/LOW)
   - Priority score (0-100)
   - Service urgency assessment
4. Lead automatically saved to CRM (Google Sheets)
5. Instant notifications:
   - Customer receives confirmation email
   - Dispatch team gets Telegram alert with score
6. Response routing based on priority (1 hour for CRITICAL, 24h for MEDIUM)

**Key Components:**
- **Lead Capture:** Tally forms (customer-friendly intake)
- **AI Scoring:** Claude 3.5 Sonnet (HVAC fault + urgency reasoning)
- **Workflow Automation:** n8n (sub-second lead processing)
- **CRM:** Google Sheets (lead database + scoring history)
- **Dispatch:** Telegram notifications (real-time alerts)

**Documentation:** See [`docs/ai-hvac-lead-management/`](docs/ai-hvac-lead-management/)

---

### **Future — HVAC Diagnostic Intelligence** 🚀
*Vision: Company-wide knowledge base + continuous learning*

Building on Levels 2 & 3:
- Confirmed case repository (technician-validated resolutions)
- Knowledge matching (new requests against historical cases)
- Continuous improvement (pattern detection across all service data)
- Predictive diagnostics (what tests predict successful resolution)
- Team learning system (automatic brief generation from success patterns)

---

## 🏗️ Architecture Overview

```
CUSTOMER / TECHNICIAN REQUEST
         │
         ▼
    [TALLY FORM] or [SERVICE REQUEST FORM]
         │
         ▼
    [n8n WEBHOOK] ──────────────────┬─────────────────┐
         │                          │                 │
         ├──► Level 3: Lead Intake  │                 │
         │    (AI Scoring)          │                 │
         │                          │                 │
         └──► Level 2: Diagnostic   │                 │
              Request               │                 │
              (AI Reasoning)        │                 │
                                    ▼                 ▼
                            [CLAUDE AI] ──► [GOOGLE SHEETS]
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            [TELEGRAM ALERT]  [EMAIL DISPATCH]  [CRM RECORD]
                    │               │               │
                    └───────────────┴───────────────┘
                            │
                            ▼
                    [DISPATCH TEAM]
                            │
                    ┌───────┴───────┐
                    ▼               ▼
            [TECHNICIAN BRIEF]  [LEAD FOLLOW-UP]
```

---

## 📁 Repository Structure

```
HVAC-fault-detection/
├── README.md                           # This file
├── fault_detection.py                  # Level 1: Python rule-based detection
│
├── docs/
│   ├── ai-hvac-diagnostic-assistant/
│   │   ├── README.md                   # Level 2 overview & architecture
│   │   ├── workflow-architecture.md    # Detailed n8n workflow design
│   │   ├── claude-reasoning-process.md # AI decision logic
│   │   └── setup-guide.md              # Implementation steps
│   │
│   └── ai-hvac-lead-management/
│       ├── README.md                   # Level 3 overview & business case
│       ├── workflow-architecture.md    # Lead scoring & routing
│       ├── lead-scoring-criteria.md    # Severity classification
│       └── setup-guide.md              # Tally + n8n configuration
│
└── .git/                               # Version history
```

---

## 🚀 Getting Started

### For Understanding the Project Evolution
1. Read this README (you are here)
2. Review `fault_detection.py` (Level 1 foundation)
3. Explore `docs/` folders for Level 2 & 3 details

### For Implementing Level 2 (Diagnostic Assistant)
See [`docs/ai-hvac-diagnostic-assistant/setup-guide.md`](docs/ai-hvac-diagnostic-assistant/setup-guide.md)

### For Implementing Level 3 (Lead Management)
See [`docs/ai-hvac-lead-management/setup-guide.md`](docs/ai-hvac-lead-management/setup-guide.md)

---

## 💡 Technology Stack

| Component | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|
| **Intake** | Python (local) | Service form | Tally (form) |
| **Orchestration** | Python logic | n8n (cloud) | n8n (cloud) |
| **AI Reasoning** | Rule-based | Claude 3.5 Sonnet | Claude 3.5 Sonnet |
| **Storage** | In-memory | Google Sheets | Google Sheets |
| **Output** | Console print | Telegram + Gmail | Telegram + Gmail |
| **Response Time** | Instant | 2-5 seconds | 1-3 seconds |

---

## 🔒 Security & Privacy

This repository does **not** contain:
- API keys or credentials
- Customer personal information
- Service technician contact details
- Sensitive business data

All configuration is managed through environment variables and secure credential storage in n8n.

---

## 📖 Project Philosophy

This project is developed **incrementally and transparently**:

- ✅ Each level is self-contained and testable
- ✅ Each stage builds on the previous one
- ✅ All work is committed with clear messages
- ✅ Project evolution is fully documented
- ✅ From simple Python → cloud AI → business automation

---

## 📞 Current Status (2026-09-13)

| Level | Status | Last Updated |
|-------|--------|--------------|
| Level 1 (Python FDD) | ✅ Complete | 2026-09-08 |
| Level 2 (Diagnostic AI) | ✅ Active | 2026-09-12 |
| Level 3 (Lead Management) | ✅ Active | 2026-09-13 |
| Future (Diagnostic Intelligence) | 🚀 In Design | — |

---

## 🤝 Contributing

The project follows git-based incremental development:

1. Work on a feature/level
2. Test thoroughly
3. Commit with clear message
4. Update relevant documentation
5. Push to GitHub

---

## 📝 License

This project is part of Amran Consulting Ltd's HVAC AI initiative.

---

**For detailed information on each level, see the documentation folders.**
