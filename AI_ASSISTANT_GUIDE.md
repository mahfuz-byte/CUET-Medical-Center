# AI Assistant Implementation - Complete Guide

## Overview
The AI Assistant has been successfully integrated with your CUET Medical Center system using Google's Gemini API.

**Features:**
- Unregistered users can chat with the AI without authentication
- Registered users' chats are saved to history
- AI answers are powered by Gemini with context from your database
- Provides information about: doctors, ambulances, medicines, viral diseases, diet plans, stress relief, first aid

---

## What the AI Can Answer

The AI assistant provides intelligent responses on:

1. **Doctor Availability** - Lists available doctors from your database with specialization and hours
2. **Ambulance Services** - Ambulance status and contact information from your system
3. **Medicines** - Available medicines in your pharmacy
4. **Viral Diseases** - Current outbreak information, symptoms, prevention
5. **Diet Plans** - Nutrition advice and meal planning
6. **Stress Relief** - Mental health tips and techniques
7. **First Aid** - Basic first aid guidance for common emergencies
8. **General Health** - Wellness and health-related questions

---

## API Endpoints

### 1. Chat with AI (Unregistered Users Welcome)
**Endpoint:** `POST /api/ai/chat/`

**Request:**
```json
{
    "message": "What doctors are available?"
}
```

**Response:**
```json
{
    "user_message": "What doctors are available?",
    "ai_response": "Based on CUET Medical Center records, we have the following doctors available... [AI generates response with context]"
}
```

**Authentication:** Not required (but optional)

---

### 2. Get Chat History (Authenticated Users Only)
**Endpoint:** `GET /api/ai/history/`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Response:**
```json
[
    {
        "id": 1,
        "user_message": "What doctors are available?",
        "ai_response": "AI's response...",
        "created_at": "2026-04-17T13:20:00Z"
    }
]
```

**Authentication:** Required (use your JWT token from login)

---

## Database Context Provided to AI

The system automatically includes this information in the AI's system prompt:

### Doctor Information
- Doctor name, title, department, availability hours
- From: `roster.models.Doctor`

### Ambulance Services  
- Ambulance ID, status (Available/On Duty/Maintenance), contact
- From: `roster.models.Ambulance`

### Medicines
- Medicine name, dosage
- From: `records.models.Medicine`

---

## Frontend Integration

### Option 1: Using the Provided JavaScript Library
Include `ai-assistant.js` in your HTML:

```html
<script src="/assets/js/ai-assistant.js"></script>

<div id="chat-container">
    <div id="chat-messages" style="height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;"></div>
    <div style="display: flex; gap: 5px;">
        <input type="text" id="user-message" placeholder="Ask the AI assistant..." style="flex: 1; padding: 8px;">
        <button onclick="handleChat()" style="padding: 8px 15px;">Send</button>
    </div>
</div>

<script>
async function handleChat() {
    const input = document.getElementById('user-message');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Display user message
    displayMessage('You', message);
    input.value = '';
    
    // Get AI response
    const aiResponse = await sendMessageToAI(message);
    displayMessage('AI Assistant', aiResponse);
}

function displayMessage(sender, message) {
    const messagesDiv = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    msgDiv.style.cssText = 'margin-bottom: 10px; padding: 8px; background: ' + 
                           (sender === 'You' ? '#e3f2fd' : '#f5f5f5') + '; border-radius: 5px;';
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
</script>
```

### Option 2: Direct API Call with Fetch
```javascript
const response = await fetch('/api/ai/chat/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'Your question here'
    })
});

const data = await response.json();
console.log(data.ai_response);
```

### Option 3: With Authentication (Save to History)
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('/api/ai/chat/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        message: 'Your question here'
    })
});
```

---

## Configuration Details

### Where Everything Lives

**Backend Files:**
- Views: `ai_assistant/views.py` - Main chat logic and context builder
- URLs: `ai_assistant/urls.py` - API endpoints
- Models: `ai_assistant/models.py` - ChatHistory for storing conversations
- Serializers: `ai_assistant/serializers.py` - Request/response handling

**Frontend Files:**
- `frontend-temp/assets/js/ai-assistant.js` - Client-side library

**Settings:**
- Registered in: `cuet_medical/settings.py` (INSTALLED_APPS)
- Routes: `cuet_medical/urls.py` (at `/api/ai/`)

### API Key
- Stored in: `.env` file as `GEMINI_API_KEY`
- Current key: `AQ.Ab8RN6LWZRsBY5rKvrptf0yCFdDxxUCjWqkTm-E0B1muFs4Ohg`

---

## System Prompt Used

The AI receives this system instruction:

```
You are a helpful AI Health Assistant for CUET Medical Center.
You provide information about:
1. Doctor availability and expertise
2. Ambulance services and emergency support
3. Medicines and treatment advice
4. Viral disease information
5. Diet plans and nutrition advice
6. Stress relief and mental health tips
7. First aid techniques
8. General health and wellness guidance

[Database context with real-time doctor, ambulance, and medicine info]

GUIDELINES:
- Always be helpful and professional
- For serious conditions, recommend visiting a doctor
- Mention specific doctors from CUET when relevant
- Provide accurate health information
```

---

## Testing the AI

### Test 1: Check Doctor Information
```
Message: "Who are the available doctors?"
Expected: AI lists doctors from your roster database
```

### Test 2: Ambulance Info
```
Message: "How can I book an ambulance?"
Expected: AI provides ambulance contact and availability status
```

### Test 3: General Health Advice
```
Message: "What can I do for stress relief?"
Expected: AI provides practical stress management tips
```

### Test 4: Diet Planning
```
Message: "I'm diabetic. What should I eat?"
Expected: AI provides diet recommendations
```

---

## Admin Panel

View and manage chat history in Django admin:
- URL: `/admin/ai_assistant/chathistory/`
- Shows: User, message, response, timestamp
- Filter by date and user

---

## Limitations & Notes

1. **Free Tier Limits**: Gemini free API has 2000 requests/day
2. **Unregistered Users**: Their chats are NOT saved (privacy)
3. **Registered Users**: Chats are saved to database for history
4. **Real-time Data**: Doctor, ambulance, medicine info updates automatically
5. **Internet Required**: AI responses require internet connection to reach Gemini API

---

## Troubleshooting

**Issue: API returns 500 error**
- Check if `.env` file has valid `GEMINI_API_KEY`
- Ensure `google-generativeai` package is installed
- Check Django logs for detailed error

**Issue: No doctor information in response**
- Verify doctors are added to `roster_doctor` table
- Check that `get_medical_context()` is being called
- Run: `python manage.py shell -c "from roster.models import Doctor; print(Doctor.objects.count())"`

**Issue: Users not seeing history**
- Ensure they're authenticated (have valid JWT token)
- Check localStorage for `access_token`
- Use `/api/ai/history/` endpoint with Bearer token

---

## Next Steps

1. **Add to Your Pages**: Integrate the AI chat into `assistant.html` or `index.html`
2. **Customize Styling**: Modify CSS in `ai-assistant.js` to match your theme
3. **Add More Context**: Edit `get_medical_context()` in `views.py` to include more medical center data
4. **Monitor Usage**: Track API usage in Django admin

---

## Support & Maintenance

- API Key expires: Check Google Cloud Console
- Monitor quota: Gemini API dashboard
- Update Django/packages regularly for security
- Backup database containing chat history

---

**Created:** April 17, 2026  
**Status:** ✅ Production Ready
