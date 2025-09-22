# Nova-Atlas Travel Assistant Setup Guide

## Overview
This setup integrates your MCP server with n8n workflow automation to create an AI-powered travel assistant with Telegram integration.

## Architecture
```
MCP Server → n8n Webhook → Telegram (Confirmation) → User Response → FastAPI → Results
```

## Step 1: Environment Setup

Create a `.env` file in the `nova-atlas-mcp` directory with:

```env
TELEGRAM_BOT_TOKEN=8355010122:AAF9aW5JzsKTY9ON35WK_RbRT3JTrCCS5Yc
TELEGRAM_CHAT_ID=1944334268
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/travel-request
```

## Step 2: n8n Setup

### 2.1 Import Workflow
1. Open your n8n instance
2. Go to Workflows → Import from File
3. Select `n8n-workflow.json` from this directory
4. The workflow will be imported with all nodes configured

### 2.2 Configure Telegram Credentials
1. In n8n, go to Settings → Credentials
2. Add a new Telegram credential with your bot token
3. Update all Telegram nodes to use this credential

### 2.3 Get Webhook URL
1. Activate the workflow in n8n
2. Copy the webhook URL from the "Webhook Trigger" node
3. Update your `.env` file with this URL

## Step 3: MCP Server Usage

### Available Tools

#### 1. `requestTravelPlan(instruction, chatId)`
Triggers the n8n workflow with confirmation buttons.

**Example:**
```json
{
  "instruction": "Plan a 3-day Goa trip and write a travel caption",
  "chatId": "1944334268"
}
```

#### 2. `sendTravelConfirmation(chatId, instruction)`
Sends confirmation message directly (bypasses n8n).

#### 3. `generatePlan(instruction)`
Direct API call to FastAPI (no Telegram integration).

#### 4. `sendTelegram(chatId, text, replyMarkup?, parseMode?)`
Direct Telegram message sending.

## Step 4: Testing

### Test the Complete Flow
1. Start your MCP server:
   ```bash
   cd nova-atlas-mcp
   python server.py
   ```

2. Use the `requestTravelPlan` tool in Cursor:
   ```json
   {
     "instruction": "Plan a 3-day Goa trip and write a travel caption",
     "chatId": "1944334268"
   }
   ```

3. Check your Telegram for the confirmation message with Yes/No buttons

4. Click "Yes" or reply with "yes" to generate the travel plan

### Expected Flow
1. MCP server sends request to n8n webhook
2. n8n sends confirmation message to Telegram
3. User responds with Yes/No (button or text)
4. n8n calls your FastAPI endpoint
5. n8n sends results back to Telegram

## Step 5: Troubleshooting

### Common Issues

#### 1. Webhook Not Found
- Ensure n8n workflow is activated
- Check webhook URL in `.env` file
- Verify n8n instance is accessible

#### 2. Telegram Bot Not Responding
- Verify bot token is correct
- Check if bot is added to the chat
- Ensure bot has permission to send messages

#### 3. FastAPI Call Failing
- Verify FastAPI endpoint is accessible
- Check network connectivity
- Review FastAPI logs for errors

#### 4. MCP Server Errors
- Check all environment variables are set
- Verify Python dependencies are installed
- Review server logs for detailed error messages

## Step 6: Customization

### Modify Messages
Edit the message text in the n8n workflow nodes to customize:
- Confirmation message
- Success message
- No response message
- Invalid response message

### Add Error Handling
- Add error nodes after HTTP requests
- Implement retry logic for failed API calls
- Add logging for debugging

### Extend Functionality
- Add more travel-related tools
- Implement user preferences storage
- Add multi-language support
- Integrate with booking APIs

## Security Notes

1. **Keep your bot token secure** - never commit it to version control
2. **Use HTTPS** for n8n webhook URLs in production
3. **Implement rate limiting** to prevent abuse
4. **Validate user inputs** before processing
5. **Monitor usage** and set up alerts for unusual activity

## Support

If you encounter issues:
1. Check the n8n execution logs
2. Review MCP server console output
3. Verify all environment variables are set correctly
4. Test each component individually before integration
