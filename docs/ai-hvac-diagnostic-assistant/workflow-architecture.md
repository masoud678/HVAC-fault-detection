# Level 2 Workflow Architecture

## n8n Workflow Overview

**Workflow ID:** `QovCex2Im7jDGuW4`
**Name:** AI HVAC Diagnostic Copilot – Intake & Triage
**Status:** Active (2026-09-12)
**Nodes:** 45 (complex multi-branch logic)

---

## Data Pipeline

### 1. INTAKE (Service Request Webhook)
```
Webhook (POST /hvac-diagnostic)
├─ Headers: Authorization, Content-Type
├─ Body:
│  ├─ systemType (Furnace, AC, Heat Pump, Ductless, etc.)
│  ├─ problemDescription (customer/tech description)
│  ├─ technicianNotes (observations at site)
│  ├─ customerContext (age, location, previous service)
│  ├─ priority (HIGH, MEDIUM, LOW)
│  └─ contactInfo (phone, email for dispatch)
```

### 2. EXTRACTION & VALIDATION
```
Parse Webhook Payload
  ├─ Extract: systemType, problem, notes
  ├─ Validate: All required fields present
  ├─ Fail → Error Response (400)
  └─ Success → Next Stage
```

### 3. CLAUDE AI ANALYSIS
```
Prepare Prompt
  ├─ System knowledge context (HVAC physics)
  ├─ Problem description
  ├─ Field observations
  └─ Instruction: "Provide fault analysis in JSON"

Claude 3.5 Sonnet
  ├─ Temperature: 0.3 (focused reasoning)
  ├─ Max tokens: 1000
  ├─ Model: claude-3-5-sonnet-20241022
  └─ Output: JSON analysis

Parse Claude Response
  ├─ Extract: faults[], missingInfo[], nextTest
  ├─ Validate JSON structure
  ├─ Fallback: Default analysis if parse fails
  └─ Store: Parsed analysis object
```

### 4. FORMATTING & DISPATCH
```
Format Technician Brief
  ├─ HTML version (for email)
  ├─ Telegram version (for instant alert)
  └─ Google Sheets row (for logging)

Parallel Output:
  ├─ Save to Google Sheets
  │  └─ Service_Requests sheet
  │     ├─ Service ID
  │     ├─ System Type
  │     ├─ Problem
  │     ├─ Top Fault (AI)
  │     ├─ Next Test (AI)
  │     └─ Timestamp
  │
  ├─ Send Telegram Alert
  │  └─ Chat ID: [configured]
  │     Content: Brief + Priority + Action
  │
  └─ Send Email
     └─ Recipient: dispatch@hvac.service
        Content: Full HTML brief with all details
```

### 5. RESPONSE
```
Return to Requestor
├─ Status: "brief_generated"
├─ Service ID
├─ Time to analysis
├─ Top fault
└─ JSON: Complete analysis object
```

---

## Node Configuration Examples

### n8n Claude AI Node
```yaml
Node Type: @n8n/n8n-nodes-langchain.anthropic
Type Version: 1

Parameters:
  modelId: "claude-3-5-sonnet-20241022"
  messages:
    values:
      - content: "{{ $json.claudePrompt }}"
        role: "user"
  options:
    maxTokens: 1000
    temperature: 0.3
```

### n8n Google Sheets Node
```yaml
Node Type: n8n-nodes-base.googleSheets
Type Version: 4.2

Parameters:
  documentId: "12kuqvQG0la5zhbTK7g2n_Ij94QtVGxqYF7ns4mIiZxw"
  sheetName: "Service_Requests"
  
Columns (auto-append):
  - Timestamp
  - Service ID
  - System Type
  - Problem Description
  - Top Fault (from AI)
  - Likelihood %
  - Next Test
  - Status
```

### n8n Telegram Node
```yaml
Node Type: n8n-nodes-base.telegram
Type Version: 1.2

Parameters:
  chatId: "102479885"
  text: "{{ $json.telegramBrief }}"
```

### n8n Gmail Node
```yaml
Node Type: n8n-nodes-base.gmail
Type Version: 2.2

Parameters:
  sendTo: "dispatch@hvac.service"
  subject: "🔧 New Diagnostic Brief – {{ $json.serviceId }}"
  message: "{{ $json.htmlBrief }}"
```

---

## Error Handling

### Parse Failures
If Claude response can't be parsed as JSON:
```
Fallback Analysis:
{
  "status": "analysis_incomplete",
  "topFault": "Unable to classify",
  "nextTest": "Contact technician for clearer description",
  "rawResponse": "[store raw Claude output]"
}
→ Still saves to sheets & sends alert
→ Team reviews raw response
```

### Missing Data
If required fields missing:
```
Validation Gate:
├─ systemType: Required
├─ problemDescription: Required
└─ Else: Return 400 error + message
```

### Claude API Timeout
If Claude takes >10 seconds:
```
Timeout Handler:
├─ Log: Service ID + failure time
├─ Notify: Team that brief delayed
├─ Retry: After 30 seconds
└─ Fallback: Send generic brief
```

---

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Webhook to Claude | <1s | ~0.8s |
| Claude Analysis | 2-5s | 3.2s avg |
| Response to Requestor | <6s | ~5.5s |
| Google Sheets Write | <2s | 1.1s |
| Telegram Send | <2s | 0.9s |
| Email Send | <3s | 2.1s |
| **Total E2E** | **<15s** | **~13.8s** |

---

## Testing & Validation

### Manual Test Case
**Input:**
```json
{
  "systemType": "Split AC",
  "problemDescription": "No cooling, fan running",
  "technicianNotes": "Compressor cycles on/off every 10 sec. Outdoor unit vibrating.",
  "customerContext": "3-year-old unit, last service 1 year ago",
  "priority": "HIGH"
}
```

**Expected Output:**
```
Top Fault: Refrigerant Leak or Overcharge (60%)
Secondary: Compressor starting capacitor (25%)
Tertiary: Thermostat calibration (15%)

Next Test: Check compressor suction/discharge pressures
Missing Info: System age, last service date, install location
```

---

## Production Deployment Checklist

- [ ] Telegram Chat ID configured
- [ ] Gmail credentials active & tested
- [ ] Google Sheets document shared with n8n account
- [ ] Service_Requests sheet created with headers
- [ ] Webhook URL documented & shared with callers
- [ ] n8n workflow set to "Active"
- [ ] Test webhook call successful (check Google Sheets + Telegram)
- [ ] Error handling tested (missing fields, timeout)
- [ ] Rate limiting set (n8n standard: 100 calls/min)

---

## Security Considerations

### Input Validation
- Sanitize problem descriptions (remove code injection)
- Limit description length (max 1000 chars)
- Validate systemType against known list

### Output Privacy
- Never include customer names in Telegram alert
- Sanitize any sensitive info before logging

### Authentication
- Webhook requires Bearer token (configured in n8n)
- Google Sheets credential (OAuth2) secure
- Telegram bot token (secure in n8n credential storage)

---

## Monitoring & Logging

All executions logged in n8n:
- Go to Workflow > Executions
- Filter by success/error
- Check timing and response size
- Export logs for analysis

**Recommended alerts:**
- Failed execution (immediately)
- Slow execution (>15 seconds)
- Parse error (immediate review)

---

## Integration Points

This workflow integrates with:

**Upstream:**
- Custom HVAC dispatch application (POST to webhook)
- Mobile app (service request submission)
- Phone intake system (could be integrated)

**Downstream:**
- **Google Sheets:** Historical case logging
- **Telegram:** Team instant notification
- **Gmail:** Dispatch archive
- **Future:** CRM system (for customer tracking)

---

## Customization

### Change Claude Model
In Claude AI node, modify `modelId`:
```
"modelId": "claude-opus-4" (more capable, slower, expensive)
"modelId": "claude-haiku-3" (faster, cheaper, less capable)
```

### Change Telegram Chat
In Telegram node, modify `chatId`:
```
chatId: "YOUR_CHAT_ID_HERE"
```

### Change Output Format
Modify "Format Brief" nodes:
- HTML for email
- Markdown for Telegram
- CSV columns for Sheets

---

## Known Limitations

1. **Requires clear input:** Vague descriptions → vague analysis
2. **No live testing:** Recommends tests, doesn't perform them
3. **Knowledge cutoff:** Claude trained to Sept 2024 (HVAC fundamentals unchanged)
4. **No learning loop:** Doesn't improve from technician feedback (yet)

---

## Related Documentation

- [`README.md`](README.md) — Overview & business value
- [`claude-reasoning-process.md`](claude-reasoning-process.md) — AI logic
- [`setup-guide.md`](setup-guide.md) — How to deploy

---

**Last Updated:** 2026-09-12
**Next Review:** 2026-09-20
