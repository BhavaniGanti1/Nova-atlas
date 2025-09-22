# Manual n8n Workflow Setup Guide

Since the JSON import is causing compatibility issues, let's build the workflow manually step by step.

## Step 1: Create New Workflow

1. In n8n, click **"Add first step..."** or the **"+"** button
2. Name your workflow: **"Nova-Atlas Travel Assistant"**

## Step 2: Add Webhook Trigger

1. Search for **"Webhook"** in the node search
2. Add **"Webhook Trigger"** node
3. Configure:
   - **HTTP Method**: POST
   - **Path**: `travel-request`
4. **Save** the workflow to get the webhook URL

## Step 3: Add Telegram Send Message

1. Add **"Telegram"** node
2. Connect it to the Webhook Trigger
3. Configure:
   - **Operation**: Send Message
   - **Chat ID**: `{{ $json.chat_id }}`
   - **Text**: 
   ```
   🤖 Nova-Atlas Travel Assistant

   I received your request: {{ $json.instruction }}

   Would you like me to generate a detailed travel plan and social media caption for you?

   Please confirm with the buttons below.
   ```
   - **Parse Mode**: Markdown
   - **Reply Markup**: 
   ```json
   {
     "inline_keyboard": [
       [
         {
           "text": "✅ Yes, generate plan",
           "callback_data": "confirm_yes:{{ $json.instruction }}"
         },
         {
           "text": "❌ No, cancel",
           "callback_data": "confirm_no"
         }
       ]
     ]
   }
   ```

## Step 4: Create Second Workflow (Telegram Response Handler)

1. Create a **new workflow** (separate from the first one)
2. Name it: **"Telegram Response Handler"**

## Step 5: Add Telegram Trigger

1. Add **"Telegram Trigger"** node
2. Configure:
   - **Trigger On**: Callback Query
   - **Credential**: Your Telegram bot token
3. This will listen for button clicks

## Step 6: Add IF Node

1. Add **"IF"** node
2. Connect it to Telegram Trigger
3. Configure condition:
   - **Left Value**: `{{ $json.callback_query.data }}`
   - **Operator**: Contains
   - **Right Value**: `confirm_yes`

## Step 7: Add HTTP Request (Yes Path)

1. Add **"HTTP Request"** node
2. Connect it to the **TRUE** output of IF node
3. Configure:
   - **Method**: POST
   - **URL**: `https://nova-atlas-2.onrender.com/generate`
   - **Headers**: 
     - Name: `Content-Type`
     - Value: `application/json`
   - **Body**: 
     - Name: `instruction`
     - Value: `{{ $json.callback_query.data.split(':')[1] }}`

## Step 8: Add Telegram Success Message

1. Add **"Telegram"** node
2. Connect it to HTTP Request
3. Configure:
   - **Operation**: Send Message
   - **Chat ID**: `{{ $json.callback_query.message.chat.id }}`
   - **Text**:
   ```
   🎉 Your Travel Plan is Ready!

   🧭 Travel Plan:
   {{ $('HTTP Request').item.json.travel_plan }}

   📝 Social Media Caption:
   {{ $('HTTP Request').item.json.social_post }}

   Happy travels! ✈️
   ```
   - **Parse Mode**: Markdown

## Step 9: Add Telegram No Response

1. Add **"Telegram"** node
2. Connect it to the **FALSE** output of IF node
3. Configure:
   - **Operation**: Send Message
   - **Chat ID**: `{{ $json.callback_query.message.chat.id }}`
   - **Text**:
   ```
   👋 No worries!

   If you change your mind, just send me another travel request anytime.

   Happy planning! 🗺️
   ```
   - **Parse Mode**: Markdown

## Step 10: Configure Credentials

1. Go to **Settings** → **Credentials**
2. Add **Telegram** credential:
   - **Bot Token**: `8355010122:AAF9aW5JzsKTY9ON35WK_RbRT3JTrCCS5Yc`
3. Update all Telegram nodes to use this credential

## Step 11: Activate Workflows

1. **Activate both workflows**:
   - Webhook workflow (receives requests)
   - Telegram Trigger workflow (handles responses)

## Step 12: Get Webhook URL

1. Copy the webhook URL from the **Webhook Trigger** node
2. Update your `.env` file:
   ```env
   N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/travel-request
   ```

## Step 13: Test the Setup

1. Start your MCP server:
   ```bash
   cd nova-atlas-mcp
   python server.py
   ```

2. Use the `requestTravelPlan` tool:
   ```json
   {
     "instruction": "Plan a 3-day Goa trip and write a travel caption",
     "chatId": "1944334268"
   }
   ```

## Troubleshooting

### If Telegram Bot Not Responding:
- Check if bot token is correct
- Ensure bot is added to the chat
- Verify bot has permission to send messages

### If Webhook Not Working:
- Check if workflow is activated
- Verify webhook URL is correct
- Test webhook with a simple POST request

### If API Call Fails:
- Check if FastAPI endpoint is accessible
- Verify network connectivity
- Review API response format

### If "Referenced node doesn't exist" Error:
- Make sure you're using `{{ $json.callback_query.data.split(':')[1] }}` in Workflow 2
- Don't reference nodes from other workflows

## Final Workflow Structure

```
Workflow 1 (Webhook):
Webhook Trigger → Telegram Send Message (with instruction in button data)

Workflow 2 (Telegram):
Telegram Trigger → IF Node → HTTP Request → Telegram Success
                    ↓
                Telegram No Response
```

## Data Flow Explanation

1. **Workflow 1** receives instruction and embeds it in button callback data
2. **User clicks button** in Telegram
3. **Workflow 2** extracts instruction from callback data using `split(':')[1]`
4. **Workflow 2** calls API and sends results back

This approach ensures data flows correctly between the two separate workflows! 🎉
