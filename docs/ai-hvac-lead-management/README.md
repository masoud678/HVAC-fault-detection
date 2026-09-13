# Level 3 — AI HVAC Lead Management

**Status:** ✅ Active (2026-09-13)

## Problem Statement

Customer HVAC requests need:

- **Instant Response:** No waiting for manual lead scoring  
- **Intelligent Prioritization:** Know which leads need 1-hour vs. 24-hour response  
- **Automatic Routing:** Critical failures get emergency technician, standard issues get scheduled  
- **CRM Integration:** All leads tracked with AI assessment for follow-up

**Current pain:** Manual lead intake takes 10-15 minutes. Scoring adds another 5-10. Highest-priority jobs get lost in the queue.

---

## Solution Overview

When a customer submits an HVAC request via Tally form:

1. **Captures** customer inquiry (system type, problem, urgency level)  
2. **Scores** with Claude AI:  
   - Fault classification  
   - Severity (CRITICAL/HIGH/MEDIUM/LOW)  
   - Priority score (0-100)  
3. **Routes** instantly:  
   - Lead saved to CRM (Google Sheets)  
   - Confirmation email to customer  
   - Telegram alert to dispatch  
4. **Prioritizes** response:  
   - CRITICAL (90-100): Call within 1 hour  
   - HIGH (70-89): Call within 4 hours  
   - MEDIUM (40-69): Email \+ schedule within 24h  
   - LOW (1-39): Email \+ scheduling info

### Expected Lead Scoring Output

CUSTOMER: John Smith

PHONE: (555) 123-4567

EMAIL: john@example.com

SYSTEM: Furnace

PROBLEM: "No heat in master bedroom, other rooms warm"

URGENCY: "This week"

═════════════════════════════════════════════════════════════

AI SCORING:

Fault Classification: Zone control issue or damper failure

Severity: MEDIUM

Priority Score: 52/100

Technical Reasoning:

Zone heating problems suggest ductwork damper malfunction or 

control system issue. Not full system failure (other zones heat).

Seasonal timing (heating season) increases importance.

Immediate Service Required: No

Recommended Timeline: Within 24-48 hours

Suggested Response:

"Hello John, thank you for contacting us. We've received your 

heating issue report. Our technician will schedule a visit 

within the next 24 hours. In the meantime, check that the 

zone damper lever is fully open."

═════════════════════════════════════════════════════════════

Status: ASSIGNED\_FOR\_FOLLOW\_UP

Lead Score: 52

CRM Entry: Created

Customer Email: Sent

Dispatch Alert: Telegram

---

## Workflow Architecture

### n8n Workflow Components

Tally Form Submission

         │

         ▼

Webhook (n8n HVAC-Lead)

         │

         ▼

Parse Form Fields

  ├─ Full Name

  ├─ Phone Number

  ├─ Email

  ├─ System Type

  ├─ Problem Description

  ├─ Urgency Level

  └─ Preferred Contact

         │

         ▼

Claude AI Lead Scoring

  ├─ Fault classification

  ├─ Severity assessment

  ├─ Priority score (0-100)

  ├─ Response timeline

  └─ Suggested messaging

         │

    ┌────┴─────┬──────────────┬─────────────┐

    ▼          ▼              ▼             ▼

Save to CRM  Send Customer  Send Dispatch  Return JSON

(Google      Email           Alert          (Confirmation)

 Sheets)   (Confirmation) (Telegram)

---

## Claude AI Lead Scoring Logic

### Severity Classification

| Score | Level | Definition | Response SLA |
| :---- | :---- | :---- | :---- |
| 90-100 | **CRITICAL** | Dangerous or complete failure | **1 hour** |
| 70-89 | **HIGH** | Significant issue affecting comfort/safety | **4 hours** |
| 40-69 | **MEDIUM** | Partial failure or inconvenience | **24-48 hours** |
| 1-39 | **LOW** | Minor issue or maintenance request | **1 week** |

### Scoring Factors

Claude considers:

- **Safety risk:** Any hazard (gas, electrical, carbon monoxide)?  
- **Impact scope:** Whole house or one zone/room?  
- **Seasonal relevance:** Is this critical for current season?  
- **System age:** Older systems → higher likelihood of failure  
- **Previous calls:** Repeat issue? Suggests bigger problem  
- **Temperature outside:** Winter furnace issue worse than spring  
- **Household vulnerability:** Elderly, children, medical equipment?

### Example Scoring

**Case 1: No Heating in Winter**

Safety: Potential (no heat in cold \= health risk)

Scope: House-wide (complete system failure)

Seasonality: Critical (freezing temperatures)

Age: Unknown (assume standard)

Score: 85 → HIGH

Rationale: Full heating failure in winter is health/safety issue

Response: 4 hours

**Case 2: AC Runs Continuously, Cold**

Safety: Low (working, just running longer)

Scope: House-wide but partial (cooling works)

Seasonality: Moderate (comfort issue)

Age: Unknown

Score: 62 → MEDIUM

Rationale: System operating but inefficient. Could be capacitor, 

refrigerant, or control. Not emergency but needs attention.

Response: 24-48 hours

**Case 3: Squeaky Furnace Blower**

Safety: None (noise not hazard)

Scope: Comfort only

Seasonality: Not seasonal

Age: Irrelevant

Score: 28 → LOW

Rationale: Bearing wear or motor noise. No safety or comfort loss.

Response: 1 week or when convenient

---

## Data Flow

### Input (Tally Form)

Customer fills out form at: `https://tally.so/r/jaRqeE`

Full Name: Sarah Johnson

Phone: (555) 987-6543

Email: sarah.j@email.com

System: "Ductless Mini-Split"

Problem: "Cold in winter, hot in summer. Not switching properly."

Urgency: "Today" ← Customer indicates

Contact: "Call"

### Processing (Claude AI)

HVAC Lead Scoring Prompt:

A customer submitted this HVAC service request:

\- System: Ductless Mini-Split (heat pump)

\- Problem: "Cold in winter, hot in summer. Not switching properly."

\- Customer Urgency: "Today"

Analyze:

1\. What is the likely fault?

2\. How severe is it (1-100 scale)?

3\. What's your reasoning?

4\. What info is missing?

5\. Suggest response message

Respond in JSON format.

### Output (Lead Scoring)

{

  "customerName": "Sarah Johnson",

  "email": "sarah.j@email.com",

  "phone": "(555) 987-6543",

  "systemType": "Ductless Mini-Split",

  "problemDescription": "Not switching between heating/cooling",

  "severity": "HIGH",

  "priority\_score": 78,

  "fault": "Thermostat mode switch failure or refrigerant metering issue",

  "technical\_reason": "Mini-split operates cooling in summer and heating in winter. If not switching between modes, suggests thermostat control failure or refrigerant flow control (reversing valve or expansion device). System likely freezing or running inefficiently.",

  "immediate\_service\_required": true,

  "recommended\_action": "Call customer. Guide to thermostat mode switching. If mode stuck, may need immediate visit. Schedule technician for next 4 hours if available.",

  "missing\_information": \[

    "Current season (summer or winter)?",

    "Does thermostat display show mode selection?",

    "Can customer hear clicking/switching sounds?",

    "System age?"

  \],

  "summary": "Mini-split not switching heating/cooling modes. Likely thermostat or reversing valve issue. HIGH priority. Offer same-day response."

}

### Output Routing

**Google Sheets:**

Row: \[timestamp\] | Sarah Johnson | (555)987-6543 | ... | HIGH | 78 | Switch mode failure | PENDING\_CALL

**Customer Email:**

Subject: ✅ Your HVAC Request Received

Hi Sarah,

Thank you for contacting us about your ductless system.

We've reviewed your request about mode switching issues and 

assessed this as HIGH priority. Our team will call you within 

the next 4 hours at (555)987-6543 to schedule service.

In the meantime:

\- Check your thermostat to ensure it's set to HEAT mode

\- Listen for clicking sounds (indicates mode switch attempt)

\- Do not force settings \- wait for our call

Best regards,

HVAC Service Team

**Telegram Alert:**

🔔 NEW HVAC LEAD

👤 Sarah Johnson

📱 (555) 987-6543

⚙️ Ductless Mini-Split

🔧 Fault: Heating/cooling mode switch failure

⚡ PRIORITY: HIGH (78/100)

⏱️ SLA: Call within 4 hours

🎯 Next Action: Assign to available technician

---

## Business Value

### For Customers

- ✅ Instant confirmation (within minutes, not hours)  
- ✅ Smart prioritization (emergency gets attention)  
- ✅ Clear next steps (know when you'll hear from us)  
- ✅ Professional impression (AI-powered service)

### For Dispatch Team

- ⏱️ **Speed:** Lead ready in \<2 seconds vs. 10+ minutes manual  
- 🎯 **Accuracy:** AI consistent, no missed priorities  
- 📊 **Visibility:** All leads in CRM with scores  
- 🤖 **Efficiency:** Automatic routing, less back-and-forth

### For Business

- 💰 **Revenue:** Faster response \= happier customers \= repeat business  
- 👥 **Capacity (estimated):** May allow the same team to handle meaningfully more leads by eliminating \~10-15 min of manual triage per lead — not yet measured  
- 📈 **Conversion (expected):** Faster follow-up is generally associated with higher close rates; this workflow's actual effect on conversion has not been measured  
- 📚 **Data:** Historical lead scores show what problems \= revenue

### Target Outcomes (Projected — Not Yet Measured)

*The figures below are process-design targets based on removing manual triage steps, not measured production results. They have not been validated against real before/after data.*

| Metric | Prior Baseline (est.) | Target | Basis |
| :---- | :---- | :---- | :---- |
| Lead response time | \~30 min (manual) | \<2 min | Automated scoring removes manual triage step |
| Manual scoring time | \~10 min | 0 min | Fully automated |
| CRITICAL leads missed | not yet measured | target \<1% | To be tracked once sufficient volume data exists |
| First-call resolution | Not measured | Target: improve | Indirect potential benefit; actual impact is not measured by this workflow |
| Customer satisfaction | Not measured | Target: improve | CSAT data is not currently collected |

---

## Integration Points

### Where Leads Come From

- **Tally Form** (primary): [https://tally.so/r/jaRqeE](https://tally.so/r/jaRqeE)  
- **Phone System** (future): IVR → webhook  
- **Website Chat** (future): Chat widget → webhook  
- **Mobile App** (future): Native app → API

### Where Leads Go To

- **Google Sheets CRM:** All leads \+ scores \+ history  
- **Telegram:** Real-time dispatch alerts  
- **Email:** Confirmation \+ follow-up  
- **Future:** Salesforce, HubSpot, or internal CRM

---

## Current Implementation Status

### ✅ Complete

- Tally form integration  
- Claude AI scoring  
- Google Sheets CRM logging  
- Customer confirmation email  
- Telegram dispatch alerts  
- End-to-end testing

### 🚀 Next Phase (Level 3.1)

- Callback history tracking (repeat customers)  
- Lead source analysis (which channels convert best)  
- A/B testing (different response messages)  
- Integration with Level 2 (diagnostic follow-up)  
- Feedback loop (technician confirms scoring accuracy)

---

## Documentation

See:

- [`workflow-architecture.md`](http://workflow-architecture.md) — n8n workflow details  
- [`lead-scoring-criteria.md`](http://lead-scoring-criteria.md) — Detailed scoring rules  
- [`setup-guide.md`](http://setup-guide.md) — How to deploy

---

## Related Systems

This Level 3 leads into:

- **Level 2:** If lead scoring HIGH, auto-trigger diagnostic assistant  
- **Future:** Confirmed cases from Level 2 inform scoring for Level 3

---

**Last Updated:** 2026-09-13  
**Status:** Production Active  
**Expected Volume:** 50+ leads/week (target estimate based on prior manual-process volume; not yet confirmed under this workflow)

For broader context, see main [`README.md`](http://../../README.md)  
