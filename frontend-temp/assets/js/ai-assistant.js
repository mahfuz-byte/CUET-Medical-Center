/**
 * AI Assistant Frontend Integration
 * 
 * Usage:
 * - Unregistered users: Can use the chat endpoint without authentication
 * - Registered users: Can use chat and their history is stored
 */

// Send a message to the AI assistant
async function sendMessageToAI(userMessage) {
    try {
        const response = await fetch('/api/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage
            })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 429) {
                return '⚠️ API quota exceeded. The daily free tier limit has been reached. Please try again tomorrow or contact your administrator to enable billing.';
            }
            return data.error || 'Sorry, I encountered an error. Please try again.';
        }

        return data.ai_response;
    } catch (error) {
        console.error('Error:', error);
        return 'Sorry, I couldn\'t process your request. Please check your internet connection and try again.';
    }
}

// Get chat history (authenticated users only)
async function getChatHistory() {
    try {
        const token = localStorage.getItem('access_token');
        
        const response = await fetch('/api/ai/history/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch chat history');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

// Example usage in HTML
/*
<div id="chat-container">
    <div id="chat-messages"></div>
    <input type="text" id="user-message" placeholder="Ask anything...">
    <button onclick="handleChat()">Send</button>
</div>

<script>
async function handleChat() {
    const input = document.getElementById('user-message');
    const message = input.value;
    
    if (!message.trim()) return;
    
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
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    messagesDiv.appendChild(msgDiv);
}
</script>
*/
