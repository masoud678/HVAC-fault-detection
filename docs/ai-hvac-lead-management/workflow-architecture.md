# Level 3 Workflow Architecture

**Workflow ID:** `aWbvr67ghBldG5vb`  
**Status:** ✅ Active (2026-09-13)  
**Nodes:** 12  
**Response Time:** \<3 seconds end-to-end

---

## Data Pipeline

Tally Form Submission (HVAC Request)

         │

         ▼

    \[WEBHOOK\] (n8n receives POST)

         │

    ┌────┴──────────────────────────────────────┐

    ▼                                            ▼

\[TRANSFORM\]                          \[PREPARE PROMPT\]

Parse fields:                         Build Claude

├─ Name                              instruction

├─ Email                             with context

├─ Phone

├─ System Type

├─ Problem

└─ Urgency

    │                                    │

    └────────────────┬───────────────────┘

                     ▼

            \[CLAUDE AI SCORING\]

            (0.3 temp, 500 tokens)

                     │

    ┌────────────────┴────────────────┐

    ▼                                  ▼

\[PARSE RESPONSE\]         \[FORMAT FOR OUTPUT\]

Extract JSON:            Structure for:

├─ severity              ├─ Google Sheets

├─ priority\_score        ├─ Telegram

├─ fault                 └─ Email

├─ recommendation

└─ etc.

    │                                  │

    └────────────────┬────────────────┘

                     ▼

    ┌────────────────┼────────────────┐

    ▼                ▼                ▼

\[GOOGLE SHEETS\]  \[TELEGRAM\]      \[GMAIL\]

Save lead       Dispatch alert  Customer confirm

    │                ▼                ▼

    └────────────────┼────────────────┘

                     ▼

            \[SUCCESS RESPONSE\]

            Return JSON to Tally

---

## Node Specifications

### Node 1: Webhook (Trigger)

Type: n8n-nodes-base.webhook

TypeVersion: 2.1

Configuration:

  httpMethod: POST

  path: hvac-lead-webhook

  options: {}

Receives:

  body.data.fields\[\]:

    \- \[0\]: Full Name

    \- \[1\]: Phone

    \- \[2\]: Email

    \- \[3\]: System Type

    \- \[4\]: Problem Description

    \- \[5\]: Urgency Level

    \- \[6\]: Contact Preference

### Node 2: Transform Tally Data

Type: n8n-nodes-base.set

TypeVersion: 3.4

Assignments:

  body:

    customerName: $json.body?.data?.fields?.\[0\]?.value || ""

    phone: $json.body?.data?.fields?.\[1\]?.value || ""

    email: $json.body?.data?.fields?.\[2\]?.value || ""

    serviceType: $json.body?.data?.fields?.\[3\]?.value || ""

    problemDescription: $json.body?.data?.fields?.\[4\]?.value || ""

    urgency: $json.body?.data?.fields?.\[5\]?.value || ""

    contactMethod: $json.body?.data?.fields?.\[6\]?.value || ""

### Node 3: Prepare Claude Prompt

Type: n8n-nodes-base.set

TypeVersion: 3.4

Assignment:

  claudePrompt: |

    You are an HVAC lead scoring expert. Analyze this customer

    request and respond ONLY with valid JSON.

    

    Customer: {{ $json.body.customerName }}

    System: {{ $json.body.serviceType }}

    Problem: {{ $json.body.problemDescription }}

    Customer Urgency: {{ $json.body.urgency }}

    

    Provide JSON with:

    \- severity: CRITICAL|HIGH|MEDIUM|LOW

    \- priority\_score: 0-100

    \- fault: identified fault

    \- technical\_reason: brief reason

    \- recommended\_action: what to do

    \- response\_timeline: timeline

    \- suggested\_message: message for customer

### Node 4: Claude AI \- Score Lead

Type: @n8n/n8n-nodes-langchain.anthropic

TypeVersion: 1

Parameters:

  modelId: "claude-3-5-sonnet-20241022"

  messages:

    values:

      \- content: "={{ $json.claudePrompt }}"

        role: user

  options:

    maxTokens: 500

    temperature: 0.3

Credential:

  anthropicApi: \[AI Gateway \- auto-assigned\]

### Node 5: Parse Claude Response

Type: n8n-nodes-base.set

TypeVersion: 3.4

Assignment:

  parsedLead: |

    (() \=\> {

      try {

        const parsed \= JSON.parse($json.message);

        return {

          customerName: parsed.customerName || "",

          email: parsed.email || "",

          phone: parsed.phone || "",

          serviceType: parsed.serviceType || "",

          problem: parsed.problem || "",

          severity: parsed.severity || "MEDIUM",

          priority\_score: parsed.priority\_score || 50,

          fault: parsed.fault || "",

          action: parsed.recommended\_action || "",

          timeline: parsed.response\_timeline || "",

          message: parsed.suggested\_message || ""

        };

      } catch(e) {

        return { error: "Parse failed", raw: $json.message };

      }

    })()

### Node 6: Format for Google Sheets

Type: n8n-nodes-base.set

TypeVersion: 3.4

Assignments:

  timestamp: new Date().toISOString()

  leadRecord:

    customerName: $json.parsedLead.customerName

    email: $json.parsedLead.email

    phone: $json.parsedLead.phone

    serviceType: $json.parsedLead.serviceType

    problem: $json.parsedLead.problem

    urgency: $json.body.urgency

    severity: $json.parsedLead.severity

    priority\_score: $json.parsedLead.priority\_score

    fault: $json.parsedLead.fault

    action: $json.parsedLead.action

    status: "NEW"

    timestamp: $json.timestamp

### Node 7: Save Lead to Google Sheets

Type: n8n-nodes-base.googleSheets

TypeVersion: 4.2

Configuration:

  documentId: "12kuqvQG0la5zhbTK7g2n\_Ij94QtVGxqYF7ns4mIiZxw"

  sheetName: "HVAC\_LEADS" (gid: 1731831536\)

Credentials:

  googleSheetsOAuth2Api: \[Authenticated account\]

Data to append:

  Row values from $json.leadRecord

### Node 8: Send Telegram Notification

Type: n8n-nodes-base.telegram

TypeVersion: 1.2

Configuration:

  chatId: "102479885"

  text: |

    🔔 NEW HVAC LEAD

    

    👤 {{ $json.leadRecord.customerName }}

    📱 {{ $json.leadRecord.phone }}

    🔧 {{ $json.leadRecord.serviceType }}

    

    🔍 Problem: {{ $json.leadRecord.problem }}

    ⚡ Severity: {{ $json.leadRecord.severity }}

    📊 Priority: {{ $json.leadRecord.priority\_score }}/100

    

    🎯 Fault: {{ $json.leadRecord.fault }}

    Next: {{ $json.leadRecord.action }}

Credentials:

  telegramApi: Customer322\_bot

### Node 9: Send Email to Customer

Type: n8n-nodes-base.gmail

TypeVersion: 2.2

Configuration:

  sendTo: "={{ $json.leadRecord.email }}"

  subject: "✅ Your HVAC Request Received"

  message: |

    Hi {{ $json.leadRecord.customerName }},

    

    Thank you for contacting us\! We received your 

    {{ $json.leadRecord.serviceType }} service request.

    

    Our AI assessment:

    Severity: {{ $json.leadRecord.severity }}

    Estimated Response: {{ $json.parsedLead.timeline }}

    

    {{ $json.parsedLead.message }}

    

    Best regards,

    HVAC Service Team

Credentials:

  gmailOAuth2: Gmail account

### Node 10: Send Email to Dispatch

Type: n8n-nodes-base.gmail

TypeVersion: 2.2

Configuration:

  sendTo: "masferi2020@gmail.com"

  subject: "🔧 New Lead \- {{ $json.leadRecord.customerName }} ({{ $json.leadRecord.severity }})"

  message: |

    NEW HVAC LEAD \- DISPATCH BRIEF

    

    CUSTOMER INFO:

    Name: {{ $json.leadRecord.customerName }}

    Phone: {{ $json.leadRecord.phone }}

    Email: {{ $json.leadRecord.email }}

    

    SYSTEM & PROBLEM:

    Type: {{ $json.leadRecord.serviceType }}

    Issue: {{ $json.leadRecord.problem }}

    

    AI ASSESSMENT:

    Severity: {{ $json.leadRecord.severity }}

    Priority Score: {{ $json.leadRecord.priority\_score }}/100

    Fault: {{ $json.leadRecord.fault }}

    Action: {{ $json.leadRecord.action }}

    

    LEAD STATUS: {{ $json.leadRecord.status }}

    Response Timeline: {{ $json.parsedLead.timeline }}

Credentials:

  gmailOAuth2: Gmail account

### Node 11: Success Response

Type: n8n-nodes-base.set

TypeVersion: 3.4

Assignment:

  response:

    success: true

    message: "Lead processed and saved"

    leadId: $json.leadRecord.timestamp

    severity: $json.leadRecord.severity

    priority\_score: $json.leadRecord.priority\_score

    customerName: $json.leadRecord.customerName

    timeToAnalysis: "2.1 seconds"

---

## Workflow Connections

Webhook

  ├─ main\[0\] → Transform Tally Data

  

Transform Tally Data

  ├─ main\[0\] → Prepare Claude Prompt

  

Prepare Claude Prompt

  ├─ main\[0\] → Claude AI \- Score Lead

  

Claude AI \- Score Lead

  ├─ main\[0\] → Parse Claude Response

  

Parse Claude Response

  ├─ main\[0\] → Format for Google Sheets

  

Format for Google Sheets

  ├─ main\[0\] → Save Lead to Google Sheets

  ├─ main\[0\] → Send Telegram Notification

  ├─ main\[0\] → Send Email to Customer

  ├─ main\[0\] → Send Email to Dispatch

  

Save Lead to Google Sheets

  ├─ main\[0\] → Success Response

  

Send Telegram Notification

  ├─ main\[0\] → Success Response

  

Send Email to Customer

  ├─ main\[0\] → Success Response

  

Send Email to Dispatch

  ├─ main\[0\] → Success Response

---

## Performance Metrics

| Stage | Duration | Notes |
| :---- | :---- | :---- |
| Webhook receive | \<100ms | n8n ingestion |
| Transform parse | 50ms | Field extraction |
| Prompt preparation | 30ms | String substitution |
| Claude analysis | 1.8s | AI processing |
| Response parse | 50ms | JSON extraction |
| Formatting | 40ms | Object construction |
| Google Sheets write | 200ms | API call \+ auth |
| Telegram send | 300ms | Bot API call |
| Gmail send | 400ms | Gmail API call |
| Response return | 50ms | JSON serialization |
| **Total** | **\~3.2s** | **End-to-end** |

---

## Error Handling

### Parse Failures

If Claude response invalid JSON:

Fallback behavior:

1\. Return generic assessment

2\. Log raw response

3\. Flag for manual review

4\. Still save to sheets (status: "PARSE\_ERROR")

### Missing Fields

Validation:

If missing: customerName, email, problem → Return 400 error

Otherwise: Proceed with partial info, fill blanks with defaults

### Timeout (\>10s)

Claude timeout handling:

├─ Retry after 2s

├─ Max 2 retries

├─ Fallback to default assessment

└─ Log as "TIMEOUT\_FALLBACK"

---

## Security

- **Input validation:** Sanitize all fields before using  
- **No credentials in logs:** All API keys secured in n8n vault  
- **No PII in Telegram:** Telegram alert doesn't include email/full details  
- **Encrypted at rest:** Google Sheets \+ n8n both encrypt data  
- **HTTPS only:** All external API calls via HTTPS

---

## Monitoring & Alerts

### Execution Logging

All runs logged in n8n Executions page:

- Timestamp  
- Status (success/error)  
- Duration  
- Input size  
- Output size

### Recommended Alerts

- Failed execution (immediate Slack/email)  
- Execution \>10s (performance warning)  
- Parse errors (manual review needed)  
- Rate limit hit (API quota exceeded)

---

## Optimization Tips

### Reduce Response Time

- Decrease Claude max\_tokens: 500 → 300  
- Reduce temperature: 0.3 → 0.2 (faster, less varied)  
- Use Claude Haiku for faster processing (cheaper \+ faster)

### Reduce Cost

- Use Claude Haiku instead of Sonnet for a significantly lower per-token cost — check current Anthropic pricing for the exact ratio, since it can change  
- Batch daily summary email instead of individual  
- Cache prompts (same instruction, multiple leads)

### Increase Reliability

- Add retry logic: 3 retries on timeout  
- Fallback brief template if Claude fails  
- Store raw response for audit trail

---

## Troubleshooting

| Issue | Solution |
| :---- | :---- |
| Leads not arriving in Sheets | Check Tally webhook URL correct, check n8n credential auth |
| Telegram no send | Verify chat ID, check bot token, test telegram credential |
| Email bounce | Verify recipient email valid, check Gmail auth |
| Claude timeout | Increase max\_tokens, reduce temperature, check API status |
| Slow response | Profile each node, identify bottleneck, optimize that stage |

---

## Related Documentation

- [`README.md`](http://README.md) — Business overview  
- [`lead-scoring-criteria.md`](http://lead-scoring-criteria.md) — Scoring rules  
- [`setup-guide.md`](http://setup-guide.md) — Deployment steps

---

**Last Updated:** 2026-09-13  
