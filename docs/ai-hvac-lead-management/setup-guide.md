# Level 3 Setup Guide

**Time Required:** 20-30 minutes  
**Difficulty:** Intermediate (n8n, Google Sheets, Tally)

---

## Overview

Level 3 converts customer Tally form submissions into AI-scored leads with instant CRM entry and dispatch alerts.

---

## Prerequisites

- [ ] Tally account (free at tally.so)
- [ ] n8n cloud account
- [ ] Google account with Sheets
- [ ] Telegram account (for alerts)
- [ ] Gmail account (for customer emails)

---

## Step 1: Set Up Tally Form

### 1a. Create/Update Tally Form

If you don't have a form, create new at: https://tally.so

**Required Fields:**
1. Full Name (Text)
2. Phone Number (Phone)
3. Email (Email)
4. What is your system? (Multiple choice)
   - Options: Furnace, AC Split, Heat Pump, Ductless, VRF, Boiler, Other
5. Tell us about your problem (Long text)
6. How urgent? (Multiple choice)
   - Options: Emergency, Today, This week, As soon as you can, No rush
7. How should we contact you? (Multiple choice)
   - Options: Call, Email, Text

**Form URL:** `https://tally.so/r/jaRqeE` *(or your own form ID)*

### 1b. Set Up Tally Webhook

1. Go to Tally form settings
2. Integrations → Webhooks
3. Add webhook:
   - **URL:** (Get from n8n in Step 2)
   - **Method:** POST
   - **Content-Type:** application/json

Save the webhook URL from n8n before configuring Tally.

---

## Step 2: Set Up n8n Credentials

### 2a. Google Sheets
1. n8n Settings → Credentials → New
2. Select: Google Sheets
3. Authenticate with your Google account
4. Save & copy Credential ID

### 2b. Gmail
1. Credentials → New → Gmail
2. Authenticate
3. Save & copy Credential ID

### 2c. Telegram
1. Create bot: Message @BotFather on Telegram
2. `/newbot` → Follow prompts
3. Copy bot token
4. Credentials → New → Telegram
5. Paste token
6. Save & copy Credential ID

---

## Step 3: Create Google Sheets CRM

### 3a. Create Sheet
1. Google Sheets: https://sheets.google.com
2. New blank spreadsheet
3. Name: `HVAC Leads`

### 3b. Create Columns (Row 1)

```
Timestamp | Name | Email | Phone | System Type | Problem | 
Urgency | Severity | Priority Score | Top Fault | 
Recommended Action | Status | Created_Date
```

### 3c. Share with n8n
1. Share button (top right)
2. Add: `cloud@n8n.io`
3. Grant: Editor
4. Save

### 3d. Get Sheet Info
From URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`

Copy:
- **SHEET_ID:** The long ID from URL
- **Sheet Name:** Tab at bottom (default: "Sheet1")

---

## Step 4: Create n8n Workflow

### 4a. New Workflow
1. n8n: Create New Workflow
2. Name: "HVAC Lead Manager"

### 4b. Add Webhook Node

**Type:** Webhook
- **Method:** POST
- **Path:** `/hvac-lead-webhook`
- **Response Mode:** "Immediately"

**Copy the Production URL** → Use this in Tally settings

### 4c. Add Parse Node

**Type:** Set
- **Name:** "Parse Form Data"
- **Assignment:**
  ```
  {
    "name": $json.body.fields[0].value,
    "phone": $json.body.fields[1].value,
    "email": $json.body.fields[2].value,
    "systemType": $json.body.fields[3].value,
    "problem": $json.body.fields[4].value,
    "urgency": $json.body.fields[5].value,
    "contact": $json.body.fields[6].value
  }
  ```

### 4d. Add Prompt Node

**Type:** Set
- **Name:** "Prepare Claude Prompt"
- **Assignment: `claudePrompt`**
  ```
  You are an HVAC lead scoring expert. Score this customer request:
  
  Customer: {{ $json.name }}
  System: {{ $json.systemType }}
  Problem: {{ $json.problem }}
  Customer Urgency: {{ $json.urgency }}
  
  Analyze and respond ONLY with JSON containing:
  {
    "severity": "CRITICAL|HIGH|MEDIUM|LOW",
    "priority_score": 0-100,
    "fault": "identified fault",
    "technical_reason": "brief explanation",
    "recommended_action": "what to do",
    "response_timeline": "timeline",
    "suggested_message": "customer message"
  }
  ```

### 4e. Add Claude Node

**Type:** Language Models → Anthropic Claude
- **Model:** claude-3-5-sonnet-20241022
- **Message:** `{{ $json.claudePrompt }}`
- **Temperature:** 0.3
- **Max Tokens:** 800

### 4f. Add Parse Response Node

**Type:** Set
- **Name:** "Parse Claude"
- **Assignment:**
  ```
  {
    "analysis": JSON.parse($json.message)
  }
  ```

### 4g. Add Format Node

**Type:** Set
- **Name:** "Format for Sheets"
- **Assignments:**
  ```
  timestamp: new Date().toISOString()
  name: $json.name
  email: $json.email
  phone: $json.phone
  systemType: $json.systemType
  problem: $json.problem
  urgency: $json.urgency
  severity: $json.analysis.severity
  priority_score: $json.analysis.priority_score
  fault: $json.analysis.fault
  action: $json.analysis.recommended_action
  status: "NEW"
  ```

### 4h. Add Google Sheets Node

**Type:** Google Sheets
- **Document ID:** Your SHEET_ID
- **Sheet Name:** "Sheet1" (or your tab)
- **Credentials:** (from Step 2a)

### 4i. Add Telegram Node

**Type:** Telegram
- **Chat ID:** (Get from Telegram, step in next section)
- **Message:**
  ```
  🔔 NEW HVAC LEAD

  👤 {{ $json.name }}
  📱 {{ $json.phone }}
  🔧 {{ $json.systemType }}

  PROBLEM: {{ $json.problem }}
  
  ⚡ Severity: {{ $json.analysis.severity }}
  📊 Priority: {{ $json.analysis.priority_score }}/100
  
  ACTION: {{ $json.analysis.recommended_action }}
  
  Status: PENDING_FOLLOWUP
  ```
- **Credentials:** (from Step 2c)

### 4j. Add Email Node

**Type:** Gmail
- **To:** `{{ $json.email }}`
- **Subject:** ✅ Your HVAC Request Received
- **Message:**
  ```
  Hi {{ $json.name }},
  
  Thank you for contacting us! We've received your HVAC 
  service request and scored it as {{ $json.analysis.severity }} priority.
  
  Our team will {{ $json.analysis.response_timeline }}.
  
  {{ $json.analysis.suggested_message }}
  
  Best regards,
  HVAC Service Team
  ```
- **Credentials:** (from Step 2b)

### 4k. Add Response Node

**Type:** Set
- **Name:** "Success Response"
- **Assignment:**
  ```
  {
    "status": "lead_created",
    "name": $json.name,
    "score": $json.analysis.priority_score,
    "severity": $json.analysis.severity,
    "crmStatus": "recorded"
  }
  ```

---

## Step 5: Connect Nodes

Connect in order:
```
Webhook → Parse Form Data → Prepare Claude Prompt → 
Claude → Parse Claude → Format for Sheets → 
(parallel: Google Sheets, Telegram, Gmail) → Success Response
```

---

## Step 6: Configure Telegram Chat ID

### 6a. Get Chat ID
1. Send message to your Telegram bot
2. Visit: `https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates`
3. Find your chat ID (number)

### 6b. Update Telegram Node
Paste chat ID into Telegram node's `chatId` field

---

## Step 7: Test Workflow

### 7a. Manual Test

Click "Test" on Webhook node:
```json
{
  "body": {
    "fields": [
      {"value": "John Smith"},
      {"value": "(555)123-4567"},
      {"value": "john@example.com"},
      {"value": "Furnace"},
      {"value": "No heat in winter"},
      {"value": "Emergency"},
      {"value": "Call"}
    ]
  }
}
```

### 7b. Verify Output
- ✅ New row in Google Sheets
- ✅ Telegram message received
- ✅ Email sent to test address
- ✅ Workflow returns success

---

## Step 8: Activate & Deploy

### 8a. Activate Workflow
Click "Activate" (top right)

### 8b. Get Webhook URL
From Webhook node → Copy "Production URL"

### 8c. Configure Tally
1. Tally form settings
2. Integrations → Webhooks
3. Paste n8n webhook URL
4. Method: POST
5. Save

### 8d. Test End-to-End
Submit test response via Tally form → Verify all outputs

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Tally webhook not firing | Check URL matches exactly, check "Active" toggle |
| Google Sheets not updating | Verify sheet shared with n8n, check credential |
| Telegram not sending | Verify bot token correct, chat ID is number |
| Email not sending | Verify Gmail credential, test manually |
| Claude timeout | Increase max wait, check API status |

---

## Monitoring

### Daily Checks
- [ ] Leads arriving in Google Sheets
- [ ] Telegram alerts send
- [ ] Customer emails send

### Weekly Review
- [ ] Export leads (Google Sheets)
- [ ] Check dispatch team feedback on scores
- [ ] Any refinements needed?

---

## Customization

### Change Response Timeline
Edit "Prepare Claude Prompt" node to include more context:
```
Customer Context: ...
System Age: ...
Previous Service: ...
```

### Change Scoring Weights
Add to prompt:
```
Scoring emphasis:
- Winter heating issues: +20%
- Summer cooling issues: +15%
- Elderly customers: +10%
```

### Add Lead Source Tracking
Add field: `source: "tally"` to format node

---

## Next Steps

After deployment:
1. Gather dispatch feedback
2. Refine scoring prompt
3. Track lead conversion (which scores close fastest?)
4. Integrate with Level 2 (diagnostic for HIGH priority leads)

---

## Related Docs

- [`README.md`](README.md) — Overview
- [`lead-scoring-criteria.md`](lead-scoring-criteria.md) — Detailed scoring rules
- [`workflow-architecture.md`](workflow-architecture.md) — Technical details

---

**Support:**  
n8n Docs: https://docs.n8n.io  
Tally Help: https://tally.so/help

**Last Updated:** 2026-09-13
