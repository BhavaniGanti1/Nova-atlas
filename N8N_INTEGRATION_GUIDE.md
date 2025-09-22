# 🚀 Nova Atlas Travel Agent - n8n Integration Guide

## Overview
This guide shows you how to integrate your Nova Atlas Travel Agent API with n8n to create automated workflows that respond to travel requests via Telegram, WhatsApp, and other social media platforms.

## 🏗️ Current Setup
- ✅ FastAPI server with travel agent endpoints
- ✅ n8n workflow automation tool running
- ✅ Telegram bot configured
- 🎯 **Goal**: Connect everything for automated travel assistance

## 🔌 API Endpoints Available

### 1. Home Endpoint
- **URL**: `GET http://localhost:8000/`
- **Purpose**: Check if API is running
- **Response**: `{"message": "Nova Atlas Travel Agent API is running"}`

### 2. Travel Request Endpoint
- **URL**: `POST http://localhost:8000/travel-request`
- **Purpose**: Process structured travel requests
- **Payload**:
```json
{
    "destination": "Goa, India",
    "duration": "3 days",
    "budget": "$500",
    "interests": "beaches, food, culture",
    "user_id": "user123",
    "platform": "telegram"
}
```

### 3. Generate Endpoint
- **URL**: `POST http://localhost:8000/generate`
- **Purpose**: Process free-form travel instructions
- **Payload**:
```json
{
    "instruction": "Plan a weekend trip to Mumbai for food lovers",
    "user_id": "user456",
    "platform": "whatsapp"
}
```

## 🔄 n8n Workflow Setup

### Step 1: Update Your Current Workflow
Your current workflow has:
- Webhook node (trigger)
- Send text message node

### Step 2: Add HTTP Request Node
1. **Add HTTP Request node** between Webhook and Send Message
2. **Configure HTTP Request**:
   - Method: `POST`
   - URL: `http://localhost:8000/travel-request`
   - Headers: `Content-Type: application/json`
   - Body: Use data from Webhook

### Step 3: Enhanced Workflow Structure
```
Webhook → HTTP Request → Send Message
   ↓           ↓           ↓
Trigger   Travel API   Response
```

## 📱 Platform-Specific Responses

### Telegram Bot Integration
- Use the `/travel-request` endpoint
- Set `"platform": "telegram"`
- Format responses for Telegram's character limits

### WhatsApp Integration
- Use the `/travel-request` endpoint  
- Set `"platform": "whatsapp"`
- Consider WhatsApp Business API formatting

### Social Media Posts
- Extract `social_post` from API response
- Use for Twitter, Instagram, Facebook posts
- Schedule posts using n8n's delay nodes

## 🧪 Testing Your Integration

### 1. Test API Locally
```bash
python test_api.py
```

### 2. Test n8n Webhook
- Use the webhook URL from your n8n workflow
- Send test travel requests
- Verify responses in Telegram

### 3. Sample Test Payload
```json
{
    "destination": "Paris, France",
    "duration": "5 days",
    "budget": "$2000",
    "interests": "art, food, culture, romance",
    "user_id": "test_user",
    "platform": "telegram"
}
```

## 🔧 Advanced Workflow Features

### 1. Multi-Platform Broadcasting
- Send travel plans to multiple platforms
- Customize content per platform
- Track engagement metrics

### 2. User Management
- Store user preferences in n8n variables
- Create personalized travel recommendations
- Build user profiles over time

### 3. Error Handling
- Add error handling nodes
- Retry failed requests
- Log errors for debugging

## 🚀 Next Steps

1. **Test the API**: Run `python test_api.py`
2. **Update n8n workflow**: Add HTTP Request node
3. **Test Telegram integration**: Send test requests
4. **Add more platforms**: WhatsApp, social media
5. **Enhance AI prompts**: Customize for different travel types

## 📞 Support
- Check API logs in your terminal
- Verify n8n workflow execution history
- Test individual endpoints with Postman/curl

## 🎯 Success Metrics
- ✅ Travel requests processed automatically
- ✅ Responses sent via Telegram
- ✅ Multi-platform support working
- ✅ AI-generated travel plans
- ✅ Social media content created

---

**Ready to automate your travel agency? Let's get started! 🎉**
