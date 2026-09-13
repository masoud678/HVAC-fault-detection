# Claude AI Reasoning Process

## Overview

Claude 3.5 Sonnet applies HVAC domain knowledge to convert service requests into diagnostic briefs.

**Prompt Template (Simplified):**

```
You are an expert HVAC technician with 15 years experience in:
- Heating systems (furnaces, boilers, heat pumps)
- Cooling systems (AC, ductless mini-split, VRF)
- Refrigeration cycles and thermodynamics
- Controls and sensors
- System troubleshooting logic

SYSTEM CONTEXT:
Type: {{ systemType }}
Problem: {{ problemDescription }}
Technician Observation: {{ technicianNotes }}
Customer Context: {{ customerContext }}

TASK:
1. Identify probable faults (rank by likelihood 0-100%)
2. Explain the technical reason for each fault
3. List missing information needed to confirm
4. Recommend the single next diagnostic test
5. Return response as JSON

Respond ONLY with valid JSON.
```

---

## Reasoning Strategy

### Step 1: System Classification

Claude first categorizes the system:
- **Type:** Furnace, AC, Heat Pump, Ductless, VRF, etc.
- **Cycle:** Heating, cooling, or combination
- **Complexity:** Simple AC vs. advanced heat pump
- **Age relevance:** Older systems fail differently

**Example:**
```
systemType: "Split AC"
→ Compression refrigeration cycle
→ Electric compressor + condenser (outdoor)
→ Evaporator (indoor)
→ Expansion device (metering)
```

### Step 2: Symptom Analysis

Claude interprets what the symptoms reveal:

**Working Systems:**
- If fan runs → control circuit active
- If compressor cycles → main power and safety switches OK
- If thermometer shows temperature drop → cycle partially working

**Failed Systems:**
- No cooling despite fan → cycle failure (not control failure)
- No response to thermostat → control failure
- Unusual sounds → mechanical issue

**Example Analysis:**
```
PROBLEM: "No cooling, fan running"

This tells us:
✓ Control system working (fan responded to demand)
✓ Power supply active (fan + thermostat powered)
✗ Cooling cycle failing (no temperature drop achieved)

LIKELY ISSUE: Not control → must be refrigerant or valve
```

### Step 3: Fault Hypothesis Generation

Claude generates fault candidates using HVAC physics:

**For "No Cooling" symptoms:**
1. **Refrigerant Undercharge** (45% likelihood)
   - Cause: Leak or improper charge
   - Result: Reduced heat absorption in evaporator
   - Observable: Low suction pressure, warm discharge

2. **Clogged Evaporator** (30% likelihood)
   - Cause: Dirt, frozen coil, biological growth
   - Result: Airflow blocked through cooling coil
   - Observable: Ice on coil, slow air velocity

3. **Expansion Valve Failure** (15% likelihood)
   - Cause: Mechanical jam or electrical solenoid failure
   - Result: Improper refrigerant metering
   - Observable: System not cycling, odd pressures

4. **Compressor Fault** (10% likelihood)
   - Cause: Mechanical wear, valve damage, winding failure
   - Result: Reduced or zero compression
   - Observable: Low discharge pressure, hot suction

**Likelihood Calculation Logic:**
- Most common failure first (refrigerant issues most common in AC)
- Symptom pattern matching (what failed systems produce this pattern)
- Age factor (older systems → mechanical, newer → refrigerant)

### Step 4: Technical Reasoning

Claude explains WHY each fault explains the symptoms:

```json
{
  "fault": "Refrigerant Undercharge",
  "likelihood": 45,
  "technicalReason": "In a refrigeration cycle, refrigerant mass directly correlates to heat absorption. With low charge, the evaporator cannot absorb sufficient heat from return air, resulting in no temperature difference across the coil despite fans operating normally. Compressor running but no cooling is classic symptom.",
  "confirmingTests": [
    "Suction line cold, but not cold enough",
    "Low pressure reading at gauge ports",
    "Normal compressor sound and vibration"
  ]
}
```

### Step 5: Missing Information Identification

Claude lists what would definitively confirm or rule out each fault:

**For Refrigerant Issues:**
- Suction line temperature (vs. expected range)
- Discharge line temperature
- Pressure readings at service ports
- Visual inspection for oil leaks

**For Blockage Issues:**
- Evaporator coil visual inspection
- Filter condition
- Airflow velocity measurement

**For Compressor Issues:**
- Discharge pressure
- Discharge temperature
- Compressor amp draw
- Thermal overload trip history

**For Valve Issues:**
- System pressure response to demand
- Solenoid coil testing (ohms)

### Step 6: Next Best Test Selection

Claude chooses ONE test that provides maximum information:

```
Decision Logic:
├─ What's safe? (eliminate tests with risk)
├─ What's quick? (eliminate tests >5 minutes)
├─ What's decisive? (eliminates most faults)
└─ Pick intersection

RESULT: "Check suction line temperature with infrared thermometer"
Reason: Safe, 30 seconds, distinguishes refrigerant from blockage
```

---

## Example: "No Heat" in Winter

### Input:
```
System: Gas Furnace
Problem: "No heat output, fan runs, pilot light on"
Observations: "No flame in combustion chamber"
```

### Claude Reasoning:

**System Context:**
- Gas furnace = combustion heating
- Pilot light on = gas supply OK
- Fan running = control signal active
- No flame = combustion not occurring despite ignition present

**Fault Hypothesis:**
1. **Flame Sensor Failure** (50%)
   - Sensor thinks flame is off, shuts off gas valve
   - System cycles (fan on 30s, off) repeatedly

2. **Gas Valve Failure** (30%)
   - Valve won't open despite signal
   - Pilot on but no main burner gas

3. **Ignition Electrode Issue** (15%)
   - Won't ignite gas (sparking but no flame)
   - Gas present but ignition failing

4. **Low Gas Pressure** (5%)
   - Regulator or line issue
   - Both pilot and main burner affected equally

**Missing Info:**
- Is pilot flame strong and stable?
- Does main burner attempt to ignite (hear clicking)?
- Any gas smell?
- Age of system?
- Recent maintenance?

**Next Best Test:**
"Observe 2 full heating cycles. Note if ignition sparks occur, if gas smell present, and if fan cycling pattern is normal or repetitive short cycles."

**Output JSON:**
```json
{
  "systemType": "Gas Furnace",
  "probableFaults": [
    {"rank": 1, "fault": "Flame Sensor Failure", "likelihood": 50},
    {"rank": 2, "fault": "Gas Valve Solenoid Failure", "likelihood": 30},
    {"rank": 3, "fault": "Ignition Electrode", "likelihood": 15},
    {"rank": 4, "fault": "Low Gas Pressure", "likelihood": 5}
  ],
  "technicalReason": "Pilot light confirms gas supply active. Fan running shows control power present. No combustion despite ignition capability indicates sensor or valve failure rather than fuel supply issue.",
  "missingInformation": [
    "Pilot flame stability and height",
    "Ignition attempt sounds (clicking, sparking)",
    "Main burner gas smell present?",
    "System age and last service date"
  ],
  "nextBestTest": "Observe 2 complete heating cycles. Document fan timing, ignition sounds, and gas odor patterns."
}
```

---

## Confidence & Uncertainty

Claude provides likelihood scores, not certainties:

**How Claude Estimates Likelihood:**
- 90%+: Textbook symptom match, no other reasonable explanation
- 70-89%: Very common fault, strong symptom match
- 40-69%: Plausible fault, consistent with symptoms
- 20-39%: Possible but less likely given symptom pattern
- <20%: Unlikely but documented possible

**Example:**
- "Refrigerant leak" in AC with no cooling: 45% (common but could be many causes)
- "Flame sensor" in furnace with no heat: 50% (very common failure, unclear without observation)
- "Compressor failure" in AC with no cooling: 10% (possible but less likely than refrigerant)

**Claude is explicit about limitations:**
```
"This analysis is based on symptoms only. Physical inspection,
pressure readings, and component testing are required for
definitive diagnosis. Probabilities reflect likelihood ranking,
not certainty."
```

---

## Temperature & Safety

### Model Configuration

```
Temperature: 0.3
→ Deterministic reasoning
→ Consistency preferred over creativity
→ Appropriate for technical analysis
```

### Safety Considerations

Claude's HVAC prompts include safety warnings:

```
SAFETY NOTES:
- Never work on high-voltage circuits without proper training
- Refrigerant handling requires EPA certification
- Gas systems dangerous if mishandled
- Always use proper PPE and tools

Technician should follow all safety protocols.
This analysis is advisory only.
```

---

## Prompt Evolution & Tuning

### Original Prompt (Basic)
```
"Analyze this HVAC problem and suggest what's wrong"
```

**Issues:**
- Too vague
- Claude generates rambling analysis
- No JSON structure
- Unclear what to do next

### Current Prompt (Refined)
```
"You are an expert HVAC technician. Given this system and
problem, identify the top 3 probable faults with likelihood
percentages, explain technically why each could cause this,
list missing info needed to confirm, recommend next diagnostic
test. Return as JSON with keys: faults[], technical_reason,
missing_information[], next_test"
```

**Improvements:**
- Role clarification (expert technician, not general AI)
- Structured format requirement (JSON)
- Explicit reasoning requirements
- Clear output specification

### Future Improvements (Level 2.1)
- Add historical case matching
- Include company's previous solutions
- Provide confidence scoring on recommendations
- Feedback loop for improvement

---

## Example Conversations (Internal Claude Reasoning)

### Scenario 1: AC No Cooling
```
[Claude Internal Reasoning]

Q: What's happening in this AC?
- Fan running ✓ (control power OK)
- Compressor likely running ✓ (customer observed outdoor unit activity)
- No cold air ✗ (cooling cycle failing)

→ System has power but no refrigeration effect

What causes refrigeration without effect?
1. Refrigerant missing (leak or undercharge)
2. Refrigerant stuck (valve jam, blocked passage)
3. No compression (compressor mechanical failure)
4. No heat absorption (evaporator blocked)

Which is most common?
→ Refrigerant leak is #1 AC complaint

What would confirm each?
- Refrigerant: Pressures low, suction line warm
- Valve jam: Pressures unequal, discharge hot
- Compressor: High discharge temp, low suction
- Blockage: High head pressure, low return air

What's the fastest test to distinguish?
→ Suction line temperature (thermocouple or IR)
   Shows if refrigerant is evaporating (normal) or not (charge issue)
```

### Scenario 2: Furnace Won't Heat
```
[Claude Internal Reasoning]

Q: What's wrong with this furnace?
- Pilot light on ✓ (gas supply to pilot working)
- Fan operates ✓ (control circuit, motor OK)
- No main burner flame ✗ (combustion not starting)

→ System has control signal but no ignition

What prevents main burner ignition despite pilot presence?
1. Flame sensor thinks it failed (sensor malfunction)
2. Gas valve won't open (solenoid jam)
3. Ignition electrode not working (no spark/weak spark)
4. Gas pressure too low (regulator issue)

Which is most common in residential furnaces?
→ Flame sensor failures (#1 after normal maintenance)

What confirms each?
- Sensor: Repeated short cycles (safety shutdown)
- Valve: No gas smell, no combustion attempt
- Ignition: Can hear clicking/sparking but no flame
- Pressure: Both pilot and main affected equally

Observation needed:
→ Watch one complete heating cycle
   Listen for ignition attempts
   Smell for gas
   Count cycle length
```

---

## Limitations & When to Escalate

Claude's analysis is limited by:
- **Information Quality:** Garbage in, garbage out (vague symptoms → vague analysis)
- **Experience Variability:** More training data on common systems, less on rare ones
- **Safety**: Cannot guarantee recommendations until verified
- **Complexity:** Multi-system interactions not always captured

**When to Escalate (Show as "Uncertain"):**
- Unusual symptom combinations not matching standard patterns
- Very old/proprietary systems
- Multiple simultaneous failures
- Safety-critical situations

---

## Testing & Validation

### Unit Test Cases
1. ✅ AC no cooling → Refrigerant issue (top fault)
2. ✅ Furnace no heat → Flame sensor (top fault)
3. ✅ Heat pump lockout → Defrost cycle (correct diagnosis)
4. ✅ Ductless splits low output → Low charge or blockage (reasonable)

### Edge Cases
1. "System won't turn on" → Control failure (correctly identified)
2. "Noisy compressor" → Multiple causes (uncertainty expressed)
3. "Weird smell" → Not HVAC issue (correctly escalated)

---

## Related Docs

- [`README.md`](README.md) — Overview
- [`workflow-architecture.md`](workflow-architecture.md) — n8n setup
- [`setup-guide.md`](setup-guide.md) — Deployment

---

**Last Updated:** 2026-09-12
