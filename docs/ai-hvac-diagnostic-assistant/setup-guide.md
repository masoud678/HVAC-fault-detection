# Level 2 Setup Guide

**Time Required:** 30-45 minutes  
**Difficulty:** Intermediate (requires n8n access & Google Sheets)

---

## Prerequisites

- [ ] n8n cloud account (https://app.n8n.cloud)
- [ ] Google account with Google Sheets access
- [ ] Telegram account (for notifications)
- [ ] Gmail account (for dispatch emails)
- [ ] Anthropic API access (Claude 3.5 Sonnet) *via n8n gateway*

---

## Step 1: Prepare Google Sheets

### 1a. Create New Google Sheet
1. Open Google Sheets: https://sheets.google.com
2. Create New → Blank spreadsheet
3. Name it: `HVAC Service Requests`

### 1b. Create Sheet Tab
1. Add sheet named: `Diagnostic_Requests`
2. Add headers (row 1):
   ```
   Timestamp | Service_ID | System_Type | Problem | 
   Top_Fault | Likelihood | Next_Test | Status | 
   Created_By | Notes
   ```

### 1c. Share Sheet with n8n
1. Click Share (top right)
2. Add: `cloud@n8n.io` (if using n8n Cloud)
3. Grant: Editor access

### 1d. Get Sheet ID
From the URL: `https://docs.google.com/spreadsheets/d/**SHEET_ID**/edit`

Copy the **SHEET_ID** for step 3.

---

## Step 2: Set Up n8n Credentials

### 2a. Google Sheets Credential
1. Go to n8n: https://app.n8n.cloud
2. Settings → Credentials
3. New → Google Sheets
4. Authenticate with your Google account
5. Grant access to Sheets
6. Save & copy the credential ID

### 2b. Gmail Credential  
1. Credentials → New → Gmail
2. Authenticate with Gmail account
3. Save & copy the credential ID

### 2c. Telegram Credential
1. Create Telegram Bot via @BotFather
2. Copy the bot token
3. Credentials → New → Telegram Bot API
4. Paste token
5. Save & copy credential ID

---

## Step 3: Import Workflow (Or Create New)

### Option A: Import Existing Workflow
*If you have the workflow JSON file:*

1. Go to n8n Workflows
2. Click "Import"
3. Upload workflow JSON
4. Skip to Step 4

### Option B: Create from Scratch

1. Create New Workflow
2. Add nodes in this order:

#### Node 1: Webhook (Trigger)
- Type: Webhook
- Method: POST
- Path: `/hvac-diagnostic`
- Response mode: "Immediately"

#### Node 2: Parse Request
- Type: Set (Variables)
- Assignments:
  ```
  systemType: $json.body.systemType
  problem: $json.body.problemDescription
  notes: $json.body.technicianNotes
  priority: $json.body.priority
  ```

#### Node 3: Prepare Claude Prompt
- Type: Set
- Assignment: `claudePrompt`
  ```
  You are an expert HVAC technician. Analyze this service request:
  
  System: {{ $json.systemType }}
  Problem: {{ $json.problem }}
  Notes: {{ $json.notes }}
  
  Respond ONLY with JSON containing:
  {
    "probableFaults": [{"fault": "", "likelihood": 0}],
    "technicalReason": "",
    "missingInformation": [],
    "nextBestTest": ""
  }
  ```

#### Node 4: Call Claude AI
- Type: Language Models → Claude (Anthropic)
- Model: `claude-3-5-sonnet-20241022`
- Message: `{{ $json.claudePrompt }}`
- Temperature: 0.3
- Max Tokens: 1000

#### Node 5: Parse Claude Response
- Type: Set
- Assignment: Parse JSON response from Claude

#### Node 6: Format for Google Sheets
- Type: Set
- Assignments:
  ```
  timestamp: now()
  serviceId: $json.body.serviceId
  systemType: $json.systemType
  problem: $json.problem
  topFault: $json.probableFaults[0].fault
  likelihood: $json.probableFaults[0].likelihood
  nextTest: $json.nextBestTest
  status: "PENDING_DISPATCH"
  ```

#### Node 7: Save to Google Sheets
- Type: Google Sheets
- Sheet: Select your sheet
- Sheet Name: "Diagnostic_Requests"
- Credentials: Use credential from Step 2a

#### Node 8: Send Telegram Alert
- Type: Telegram
- Chat ID: *(get from Telegram group)*
- Message: 
  ```
  🔧 NEW DIAGNOSTIC REQUEST

  Service ID: {{ $json.serviceId }}
  System: {{ $json.systemType }}
  Problem: {{ $json.problem }}
  
  Top Fault: {{ $json.topFault }} ({{ $json.likelihood }}%)
  Next Test: {{ $json.nextTest }}
  
  Status: PENDING
  ```
- Credentials: Use credential from Step 2c

#### Node 9: Send Email Dispatch
- Type: Gmail
- To: Your dispatch email
- Subject: `🔧 New Diagnostic Brief – {{ $json.serviceId }}`
- Message: *(HTML formatted brief)*
- Credentials: Use credential from Step 2b

#### Node 10: Return Success
- Type: Set
- Assignment:
  ```
  {
    "status": "brief_generated",
    "serviceId": $json.serviceId,
    "topFault": $json.topFault,
    "nextAction": "review_and_dispatch"
  }
  ```

---

## Step 4: Configure & Test

### 4a. Set Telegram Chat ID
1. Send a message to your Telegram bot
2. Visit: `https://api.telegram.org/bot{TOKEN}/getUpdates`
3. Find your chat ID
4. Copy it to Telegram nodes: `chatId` field

### 4b. Configure Email Addresses
1. In Gmail nodes, set dispatch email address
2. Test email sending first (manual run)

### 4c. Test Workflow

**Test Input (POST to webhook):**
```json
{
  "serviceId": "TEST-001",
  "systemType": "Split AC",
  "problemDescription": "No cooling, fan running",
  "technicianNotes": "Compressor cycles, outdoor unit normal",
  "priority": "HIGH"
}
```

**Expected Output:**
- ✅ New row in Google Sheets
- ✅ Telegram message received
- ✅ Email sent to dispatch
- ✅ Workflow returns success JSON

### 4d. Verify Each Output
1. **Google Sheets:** Check that row was added with Claude analysis
2. **Telegram:** Confirm message with fault and next test
3. **Email:** Check dispatch email with full brief
4. **Workflow:** Check execution shows all nodes successful

---

## Step 5: Deploy to Production

### 5a. Activate Workflow
- Click "Activate" (top right)
- Set to "Active"

### 5b. Get Webhook URL
- From Webhook node: Copy "Production URL"
- This is your endpoint for service requests:
  ```
  https://n8n.yourinstance.cloud/webhook/hvac-diagnostic
  ```

### 5c. Document the URL
Share with:
- Dispatch team
- Mobile app developers
- Phone intake system
- Any other requestor

### 5d. Monitor Executions
- Go to Workflow → Executions
- Check that requests are arriving
- Verify successful completion rate
- Monitor response time

---

## Step 6: Integrate with Your System

### 6a. From Dispatch App
Send POST request:
```bash
curl -X POST https://n8n.yourinstance.cloud/webhook/hvac-diagnostic \
  -H "Content-Type: application/json" \
  -d '{
    "serviceId": "SK-12345",
    "systemType": "Heat Pump",
    "problemDescription": "Low heating",
    "technicianNotes": "Outdoor temperature 20F, system icing up",
    "priority": "HIGH"
  }'
```

### 6b. From Phone System
*(Configure based on your telephony system)*

### 6c. From Mobile App
*(Configure API endpoint in app settings)*

---

## Troubleshooting

### Webhook not triggering
- [ ] Verify webhook is active (toggle on in node)
- [ ] Check URL is correct
- [ ] Check firewall allows inbound
- [ ] Test with curl (command above)

### Claude Analysis Fails
- [ ] Check n8n credentials are valid
- [ ] Verify prompt format (claudePrompt variable)
- [ ] Check temperature/max tokens settings
- [ ] Review Claude API status

### Google Sheets not updating
- [ ] Verify sheet is shared with n8n account
- [ ] Check sheet name matches configuration
- [ ] Verify headers exist in row 1
- [ ] Test Google Sheets credential manually

### Telegram message not sent
- [ ] Verify bot token is correct
- [ ] Check chat ID is correct (must be number)
- [ ] Verify bot has permission to post in group
- [ ] Test with manual Telegram node execution

### Email not sending
- [ ] Verify Gmail credentials are valid
- [ ] Check recipient email is correct
- [ ] Verify Gmail account allows "Less secure" app access
- [ ] Test Gmail credential manually

---

## Performance Optimization

### Reduce Response Time
1. Decrease Claude max_tokens from 1000 → 500
2. Set temperature from 0.3 → 0.2 (faster, less varied)
3. Add execution timeout: 10 seconds max

### Increase Reliability  
1. Add retry logic to Claude node (3 retries, 2s delay)
2. Add fallback brief if Claude fails
3. Log all failures to Google Sheets for review

### Cost Management
1. Use Claude Haiku for simpler analysis (cheaper)
2. Batch requests (daily summary instead of per-request)
3. Monitor token usage in n8n billing

---

## Monitoring Checklist

Daily:
- [ ] Check execution success rate (aim for >99%)
- [ ] Verify Google Sheets updates
- [ ] Review Telegram alerts (correctness)

Weekly:
- [ ] Export logs for analysis
- [ ] Check response times (should be <10s)
- [ ] Review failed executions

Monthly:
- [ ] Analyze dispatch team feedback
- [ ] Compare AI recommendations vs. actual diagnoses
- [ ] Identify prompt improvements

---

## Next Steps

After deployment:

1. **Gather Feedback:** Ask dispatch team for input on brief quality
2. **Tune Prompt:** Refine Claude prompt based on feedback
3. **Add History:** Link to previous cases for pattern matching
4. **Measure Impact:** Track how briefs affect first-call resolution
5. **Iterate:** Continuous improvement (Level 2.1)

---

## Related Documentation

- [`README.md`](README.md) — Overview
- [`workflow-architecture.md`](workflow-architecture.md) — Technical details
- [`claude-reasoning-process.md`](claude-reasoning-process.md) — AI logic

---

**Support:** For n8n help, see https://docs.n8n.io  
**Questions?** Review main project [`README.md`](../../README.md)

**Last Updated:** 2026-09-12
