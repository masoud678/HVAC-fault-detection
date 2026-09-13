# Level 2 — AI HVAC Troubleshooting Assistant

**Status:** ✅ Active (2026-09-12)

## Problem Statement

Service technicians spend valuable time on diagnostics that could be accelerated by:

- Immediate AI-assisted fault analysis  
- Systematic missing-information identification  
- Recommended next test guidance  
- Documented case reasoning for later review

**Current pain:** Manual diagnosis takes 15-30 minutes. AI can provide initial brief in \<5 seconds.

---

## Solution Overview

When a technician submits a service request with system details and symptoms, n8n \+ Claude:

1. **Captures** service request (system type, problem description, technician notes)  
2. **Analyzes** with Claude AI applying HVAC domain knowledge  
3. **Identifies** probable faults and root causes  
4. **Recommends** next diagnostic step  
5. **Routes** technician brief to team (Telegram \+ Email \+ Google Sheets)

### Expected Output Example

🔧 TECHNICIAN BRIEF \- Service Request \#SK-12345

SYSTEM: Split AC / Heat Pump

PROBLEM: "No cooling, fan running"

TECHNICIAN NOTES: "Unit runs but no cold air. Outdoor unit sounds normal."

═══════════════════════════════════════════════════════════════

🔍 AI-ASSISTED DIAGNOSIS:

Probable Faults (ranked by likelihood):

  1\. Refrigerant undercharge (45%)

  2\. Clogged evaporator / filter (30%)

  3\. Expansion valve failure (15%)

  4\. Compressor fault (10%)

💡 Technical Reason:

  \- Fan operating \= system control working

  \- No temperature drop \= cooling cycle not functioning

  \- Outdoor unit normal \= compressor likely spinning

  → Points to refrigerant or valve issue

❓ Missing Information:

  \- Outdoor temperature (ambient)

  \- Suction line temperature

  \- Discharge line temperature

  \- System operating time

  \- Last service date

🎯 NEXT BEST TEST:

  1\. Check suction line temperature (should be 8-15°C below return air)

  2\. Measure pressure at gauge ports

  3\. Listen to compressor (should have load sound)

═══════════════════════════════════════════════════════════════

Generated: 2026-09-13 14:32:10 UTC

Status: PENDING\_DIAGNOSIS

---

## Workflow Architecture

### n8n Workflow Components (Simplified View)

Webhook (Service Request)

         │

         ▼

Extract & Validate Data

  ├─ System Type

  ├─ Problem Description

  ├─ Technician Notes

  ├─ Customer Context

  └─ Historical Notes (if available)

         │

         ▼

Claude AI Reasoning

  ├─ Probable Faults

  ├─ Root Cause Analysis

  ├─ Missing Information

  └─ Next Best Test Recommendation

         │

         ▼

Format Technician Brief

  ├─ HTML Email version

  ├─ Telegram message version

  └─ Google Sheets structured data

         │

    ┌────┴──────┬──────────────┐

    ▼           ▼              ▼

Google Sheets Telegram Email   Return JSON

(Logging)     (Alert)  (Archive)

---

## Claude AI Reasoning Process

Claude applies HVAC troubleshooting logic:

### Step 1: Parse & Understand

- System type (Furnace, AC, Heat Pump, etc.)  
- Problem symptoms  
- Environmental context  
- Previous diagnostics (if any)

### Step 2: Fault Hypothesis

Using HVAC physics:

- What system functions are working? (controls, fans, power)  
- What functions are failing? (cooling, heating, circulation)  
- What causes that symptom pattern?

### Step 3: Rank by Likelihood

Consider:

- Most common faults first  
- System-specific failure modes  
- Seasonal context  
- Previous service history

### Step 4: Identify Diagnostic Gaps

What information would confirm/rule out each hypothesis?

- Temperature measurements  
- Pressure readings  
- Component operation status  
- Time-based observations

### Step 5: Recommend Next Test

Which single test provides maximum information?

- Safety first (no risk to technician)  
- Quickest to perform  
- Most decisive result

---

## Data Flow

### Input (Webhook)

{

  "serviceId": "SK-12345",

  "systemType": "Split AC",

  "problemDescription": "No cooling, fan running",

  "technicianNotes": "Outdoor unit sound normal, indoor fan operating",

  "customerContext": "System 5 years old, no recent service",

  "ambientTemp": null,

  "priority": "HIGH"

}

### Claude Processing (Hidden)

HVAC TRIAGE PROMPT:

You are an expert HVAC technician. Analyze this service case:

\- System type: Split AC (cooling cycle, refrigerant-based)

\- Symptoms: "No cold air, fan running"

\- Observations: "Outdoor compressor running, indoor fan running"

This indicates:

\- Control system: working (fan on)

\- Cooling cycle: NOT working (no temperature drop)

\- Compressor: likely operating

What are probable faults? Rank by likelihood.

What information is missing to confirm?

What's the next diagnostic step?

### Output (Technician Brief)

{

  "serviceId": "SK-12345",

  "probableFaults": \[

    {"fault": "Refrigerant undercharge", "likelihood": 45},

    {"fault": "Clogged evaporator", "likelihood": 30},

    {"fault": "Expansion valve failure", "likelihood": 15},

    {"fault": "Compressor fault", "likelihood": 10}

  \],

  "technicalReason": "Fan operating \= controls working. No cooling \= cycle failure. Compressor spinning \= likely not mechanical failure. Points to refrigerant or valve.",

  "missingInformation": \[

    "Suction line temperature",

    "Discharge line temperature",

    "Ambient temperature",

    "System running time"

  \],

  "nextBestTest": "Check suction line temperature with infrared thermometer",

  "briefHTML": "...",

  "briefTelegram": "..."

}

---

## System Outputs

### 1\. **Google Sheets Log**

Persistent record of all diagnostic requests and AI recommendations

- Service ID  
- System Type  
- Problem  
- AI Diagnosis (top 3 faults)  
- Next Test  
- Timestamp

### 2\. **Telegram Notification** (Real-time Alert)

Dispatch team gets instant brief:

🔧 NEW SERVICE REQUEST \#SK-12345

SYSTEM: Split AC

PROBLEM: No cooling, fan running

⚡ PRIORITY: HIGH

AI DIAGNOSIS:

Top cause: Refrigerant undercharge (45%)

Next test: Check suction line temp

→ Brief sent to email

### 3\. **Email Dispatch** (Full Documentation)

Detailed HTML brief with:

- Complete fault analysis  
- Technical reasoning  
- Missing information checklist  
- Step-by-step next test instructions  
- Safety warnings (if applicable)

### 4\. **Return to Requestor** (Workflow Response)

API response includes:

{

  "status": "brief\_generated",

  "serviceId": "SK-12345",

  "timeToAnalysis": "3.2 seconds",

  "topFault": "Refrigerant undercharge",

  "nextAction": "measure\_suction\_line"

}

---

## Business Value

### For Dispatch Team

- ⏱️ **Time savings (expected):** Designed to return a diagnosis in seconds, versus an estimated 15-30 min for manual review — manual baseline not formally measured  
- 🎯 **Capability:** Ranks probable faults by likelihood to help narrow down trial-and-error troubleshooting — actual impact on diagnostic accuracy has not been measured  
- 📊 **Consistency:** Standardized diagnostic approach  
- 📈 **Learning:** Patterns visible across all cases

### For Technicians

- 📱 **Mobile brief:** Telegram message on-the-go  
- ✓ **Checklist:** Clear next steps before arriving  
- 🔍 **Systematic:** Organized fault likelihood (most likely first)  
- 🧠 **Learning:** AI reasoning transparency

### For Business

- 💰 **Revenue (potential):** Faster diagnostics may shorten service calls and support higher daily job capacity — not yet measured  
- 👥 **Capacity:** Same team handles more calls  
- 📉 **Callbacks:** Better diagnostics \= fewer revisits  
- 📚 **Knowledge:** Documented reasoning for training

---

## Implementation Notes

### Current Setup

- **n8n Workflow ID:** `QovCex2Im7jDGuW4` (Intake & Triage)  
- **Claude Model:** Claude 3.5 Sonnet  
- **Data Storage:** Google Sheets (Service\_Requests sheet)  
- **Team Notification:** Telegram \+ Gmail  
- **Response Time:** 2-5 seconds end-to-end

### Known Limitations

- Requires clear problem description (not useful for "system not working")  
- Can't perform actual tests (only recommends them)  
- Depends on technician's accurate initial observation  
- Missing information may require callback to customer

### Next Steps (Level 2.1)

- Add historical case matching (compare new request to past similar cases)  
- Implement confidence scoring (AI uncertainty about recommendations)  
- Feedback loop (technician confirms diagnosis, improves future recommendations)

---

## Technical Details

See:

- [`workflow-architecture.md`](http://workflow-architecture.md) — n8n node-by-node breakdown  
- [`claude-reasoning-process.md`](http://claude-reasoning-process.md) — AI logic and prompting  
- [`setup-guide.md`](http://setup-guide.md) — How to deploy this system

---

## Questions?

This Level 2 system complements:

- **Level 1** (Python FDD): Basic rule-based detection  
- **Level 3** (Lead Management): Customer intake & scoring  
- **Future** (Diagnostic Intelligence): Company knowledge base

For broader context, see main [`README.md`](http://../../README.md)  
