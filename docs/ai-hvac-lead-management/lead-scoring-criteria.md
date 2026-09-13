# Lead Scoring Criteria

Detailed breakdown of how Claude AI scores HVAC leads on a 0-100 scale.

---

## Severity Scale

### 90-100: CRITICAL
**Definition:** Dangerous or complete system failure requiring immediate intervention.

**Examples:**
- Furnace won't heat in winter (freezing risk)
- AC emergency (heat stroke risk in summer)
- Gas smell (safety hazard)
- System shutting off repeatedly (safety lockout)
- No hot water (boiler failure)

**Response:** Call within 1 hour | Emergency dispatch

**Reasoning:**
- Health/safety impact (cold, heat, toxic exposure)
- System completely non-functional
- Seasonal vulnerability (winter heating = health hazard)
- Risk of property damage (frozen pipes)

**Example Scoring:**

```
CASE: "No heat, single digit temperatures outside"

Factors:
✓ Safety risk: YES (freezing hazard)
✓ System failure: Complete (no heat anywhere)
✓ Seasonal: CRITICAL (winter)
✓ Vulnerable: Possibly (elderly, children?)

Score: 94 → CRITICAL
SLA: 1 hour emergency response
```

---

### 70-89: HIGH  
**Definition:** Significant issue affecting comfort, partial failure, or seasonal importance.

**Examples:**
- AC not cooling in summer (partial system working)
- Heat pump in winter not heating efficiently
- Thermostat not responding
- Unusual sounds suggesting imminent failure
- Previous recurring issue (sign of bigger problem)

**Response:** Call within 4 hours | Priority scheduling

**Reasoning:**
- System partially functional but degraded
- Affects comfort but not immediate safety
- Seasonal context matters (summer AC harder to wait on)
- May lead to complete failure if not addressed

**Example Scoring:**

```
CASE: "AC running constantly but house still 78°F" (summer)

Factors:
✓ Safety risk: NO (but uncomfortable)
✓ System failure: Partial (AC running, just inefficient)
✓ Seasonal: HIGH (summer cooling critical)
✓ Trend: Could worsen (capacitor fail = complete failure)

Score: 75 → HIGH
SLA: 4-hour response
Reason: System degrading, summer urgent, not emergency
```

---

### 40-69: MEDIUM
**Definition:** Partial failure, convenience issue, or maintenance need with some urgency.

**Examples:**
- One zone not heating in multi-zone system
- System cycles frequently but maintains temperature
- Minor noise or vibration
- Filter needs replacement
- System over 10 years old with minor issue

**Response:** Schedule within 24-48 hours | Standard scheduling

**Reasoning:**
- System functional but degraded
- Affects part of house or efficiency
- Not seasonal emergency
- Can wait for next available slot

**Example Scoring:**

```
CASE: "Bedroom heating only up to 68°F, others are 72°F"

Factors:
✓ Safety risk: NO (still heating)
✓ System failure: Partial (some zones work)
✓ Seasonal: MODERATE (heating season)
✓ Impact: Minor (one zone)
✓ Trend: Stable (not getting worse)

Score: 54 → MEDIUM
SLA: 24-48 hours
Reason: Zone control issue, not emergency, can schedule normally
```

---

### 1-39: LOW
**Definition:** Minor maintenance, convenience, or cosmetic issue with no urgency.

**Examples:**
- Squeaky blower (noise only)
- System running but efficiency question
- Maintenance scheduling (filter, cleaning)
- Thermostat battery low
- Request for quote on upgrade

**Response:** Email with scheduling link | Schedule at convenience

**Reasoning:**
- System fully functional
- No safety, comfort, or efficiency impact
- Can wait days or weeks
- Might be "nice to have" vs. "must fix"

**Example Scoring:**

```
CASE: "Wondering if I should upgrade my 8-year-old system"

Factors:
✓ Safety risk: NO
✓ System failure: NO (working fine)
✓ Seasonal: NO
✓ Impact: NONE (informational)
✓ Urgency: None stated

Score: 18 → LOW
SLA: Email response + link to schedule (1 week OK)
Reason: Not a problem, informational inquiry
```

---

## Scoring Factors (Detailed)

### Factor 1: Safety Risk (+20-30 points)
Does this pose a danger?

| Risk | Points | Examples |
|------|--------|----------|
| Immediate hazard | 25-30 | Gas smell, electrical sparks, carbon monoxide risk |
| Health risk | 15-20 | No heating in winter, excessive heat in summer |
| Potential future hazard | 5-10 | Unusual sounds suggesting mechanical failure |
| No risk | 0 | Cosmetic or efficiency issue |

### Factor 2: System Impact (+15-25 points)
How much of the system failed?

| Scope | Points | Examples |
|-------|--------|----------|
| Complete failure | 20-25 | No heat, no cooling at all |
| Major partial | 15-20 | No cooling but heating works; one of two units out |
| Partial | 8-15 | One zone not working; system degraded but operating |
| Minor | 0-8 | Noise, inefficiency, single component |

### Factor 3: Seasonal Context (+10-20 points)
Is this critical for current season?

| Timing | Points | Notes |
|--------|--------|-------|
| Winter + no heat | 20 | Freezing risk, health hazard |
| Summer + no cooling | 15-18 | Heat exhaustion risk, comfort critical |
| Wrong season | 2-5 | Customer mentions "when winter comes" in summer |
| Off-season | 0 | Mentioned issue, not immediate |

**Example:**
- "AC not cooling" in June = +18 points (summer, comfort critical)
- "AC not cooling" in December = +3 points (winter, not needed now)

### Factor 4: System Age (+0-15 points)
How likely to fail further?

| Age | Points | Reasoning |
|-----|--------|-----------|
| 15+ years | 12-15 | High failure probability, likely multiple issues |
| 10-15 years | 8-12 | Mid-life, common failures, more vulnerable |
| 5-10 years | 3-8 | Generally reliable, single faults more likely |
| <5 years | 0-3 | Usually under warranty, less risk |

### Factor 5: Frequency/Pattern (+5-15 points)
Is this recurring or new?

| Pattern | Points | Examples |
|---------|--------|----------|
| Recurring (3+) | 12-15 | "This is the third time this month" |
| Chronic (2-3) | 8-12 | "Happens every winter" |
| Escalating | 5-10 | "Getting worse each week" |
| New onset | 0-5 | "Just started today" |

**Reasoning:** Recurring issues suggest root problem, not just symptom.

### Factor 6: Vulnerability Score (+0-10 points)
Who is in the household?

| Factor | Points | Examples |
|--------|--------|----------|
| Elderly (65+) | 5 | Heat/cold more dangerous |
| Young children | 5 | Same risk factors |
| Medical equipment | 8 | "Mother uses oxygen concentrator" |
| Pets | 2 | Less critical but consideration |
| None noted | 0 | Standard household |

---

## Scoring Calculation Example

### Example Case: Heat Pump Not Heating (Winter, Age 12)

**Input:**
```
System: Heat Pump
Problem: "Not heating, just blowing cold air"
Season: January (winter)
Customer: "Elderly customer, gets cold easily"
Previous: First time this season
```

**Calculation:**

| Factor | Assessment | Points |
|--------|-----------|--------|
| Safety Risk | Health (no heat in winter) | +18 |
| System Impact | Complete heating failure (partial AC) | +22 |
| Seasonal Context | Winter, critical for heating | +19 |
| System Age | 12 years old (mid-life failure) | +10 |
| Frequency | New issue, first occurrence | +2 |
| Vulnerability | Elderly customer | +5 |
| **TOTAL** | | **76** |

**Result:** SCORE: 76 → **HIGH Priority**
- **Severity:** HIGH
- **SLA:** 4 hours
- **Reason:** Winter heating failure on older system with vulnerable occupant

**Suggested Response:**
```
"Hello Mrs. Smith, we received your heating issue report and 
assessed it as HIGH priority. Heat loss in winter is serious, 
and our team will call you within 4 hours to arrange immediate 
technician visit.

Common causes include: refrigerant issue, reversing valve 
failure, or thermostat mode stuck on cooling.

Our technician can likely resolve same-day or next morning. 
Please ensure someone is home to let them in. We'll call 
30 minutes before arrival."
```

---

## Scoring Ranges by System Type

### Furnace Issues
- No heat in winter: 85-95 (CRITICAL)
- Weak heat: 60-75 (MEDIUM to HIGH)
- Noise: 25-40 (LOW to MEDIUM)
- Efficiency question: 15-25 (LOW)

### AC/Cooling Issues
- No cooling in summer: 80-90 (HIGH to CRITICAL)
- Slow cooling: 55-70 (MEDIUM to HIGH)
- Noise: 20-35 (LOW)
- Upgrade inquiry: 10-20 (LOW)

### Heat Pump (Hybrid)
- No heat in winter: 85-95 (CRITICAL)
- No cooling in summer: 80-90 (HIGH to CRITICAL)
- Switching issues: 65-80 (HIGH)
- Inefficiency: 40-60 (MEDIUM)

### Water Heater
- No hot water in winter: 75-85 (HIGH to CRITICAL)
- Slow heating: 45-60 (MEDIUM)
- Noise: 30-45 (MEDIUM to LOW)

---

## Qualitative Adjustments

After calculating raw score, Claude may adjust based on qualifiers:

### +5 Bonus Points
- Customer mentions "unsafe" or "dangerous"
- Previous urgent service calls
- System completely down (not degraded)
- Business/multi-unit property

### -5 Penalty Points
- Customer seems uncertain or exploratory
- "Just checking if this is normal"
- "Wondering about maintenance"
- Inquiry for future need

### Note Examples

```
SCORE: 48 → 52 (+4 for "emergency")
Reason: Customer emphasized urgency despite technical medium rating

SCORE: 62 → 58 (-4 for "informational")
Reason: Genuine concern but exploratory, not urgent

SCORE: 78 → 82 (+4 for "commercial property")
Reason: Business interruption = higher priority than residential
```

---

## Confidence & Uncertainty

When Claude can't clearly score:

```
SCORE: 55 (±10)
Status: MODERATE UNCERTAINTY

Reason: Problem description unclear. Could be low-priority 
maintenance or high-priority efficiency issue.

Recommendation: Call customer to clarify before scheduling.
Key questions:
- When did this start?
- Is system completely off or just slow?
- Any unusual sounds or smells?
```

---

## Feedback Loop (For Improvement)

After technician completes service, record actual severity:

```
Lead Score: 62 (AI prediction)
Actual Severity: 75 (technician assessment)
Time Spent: 2.5 hours
Resolution: Refrigerant recharge + valve cleaning
Repeat Issue: No
Customer Satisfaction: 5/5

Feedback: AI underestimated complexity. Multiple issues found.
Score adjustment: AI was reasonable, issue more complex than 
apparent from description.
```

This feedback trains Claude to improve future scoring.

---

## Common Scoring Errors (To Avoid)

### ❌ Under-scoring (Missing urgency)
```
WRONG: "System cycles on/off" → Score: 25
RIGHT: "System cycles every 10 sec, ancient unit" → Score: 65
Lesson: Cycling + age = reliability concern, not just minor
```

### ❌ Over-scoring (False urgency)
```
WRONG: "Wondering about upgrade" → Score: 68
RIGHT: "Informational inquiry" → Score: 18
Lesson: Curiosity ≠ urgency
```

### ❌ Missing context
```
WRONG: "No cooling" → Score: 55
RIGHT: "No cooling in July, 95F outside, two kids home" → Score: 88
Lesson: Seasonal + vulnerability context critical
```

---

## Testing Scoring Against Real Cases

### Test Case 1: Winter Furnace
- **Description:** No heat, 15°F outside, customer elderly
- **Correct Score:** 90+ (CRITICAL)
- **Why:** Safety + winter + vulnerable person
- ✅ Pass

### Test Case 2: Squeaky Blower
- **Description:** Furnace runs fine but makes noise
- **Correct Score:** 28 (LOW)
- **Why:** System functional, no hazard, aesthetic only
- ✅ Pass

### Test Case 3: AC Efficiency Question
- **Description:** "Should I replace my 8-year-old AC?" (summer)
- **Correct Score:** 20-30 (LOW)
- **Why:** Informational, system working
- ✅ Pass

### Test Case 4: Partial Zone Failure (Heating Season)
- **Description:** One bedroom heating but others okay
- **Correct Score:** 52 (MEDIUM)
- **Why:** Partial failure, not emergency, in season
- ✅ Pass

---

## Using Scores for Business Decisions

### Lead Routing
- **CRITICAL:** Send to senior technician immediately
- **HIGH:** Assign to available tech, schedule today or next day
- **MEDIUM:** Schedule within week, assign routine technician
- **LOW:** Send info/quote via email, follow up next month

### Response Time
- **CRITICAL:** Phone call within 1 hour
- **HIGH:** Phone call within 4 hours
- **MEDIUM:** Email within 24 hours + scheduling
- **LOW:** Auto-reply with info, email within 2 days

### Dispatch Priority
```
Queue Order: CRITICAL > HIGH > MEDIUM > LOW
Interrupt Rule: CRITICAL pulls technician off other job
Escalation: CRITICAL > can call owner/dispatcher
```

---

**Last Updated:** 2026-09-13

See also:
- [`README.md`](README.md) — Lead management overview
- [`workflow-architecture.md`](workflow-architecture.md) — Technical implementation
