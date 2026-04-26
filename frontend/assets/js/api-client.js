// Shared API helper for frontend pages.
(function () {
  // Dynamic API URL - works for both local and production
  var API_BASE_URL;
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    API_BASE_URL = '/api';  // Local: use relative path
  } else {
    API_BASE_URL = window.location.origin + '/api';  // Production: use full origin URL
  }

  function getAuthHeaders() {
    var token = localStorage.getItem('accessToken');
    var headers = { 'Content-Type': 'application/json' };
    if (token) headers.Authorization = 'Bearer ' + token;
    return headers;
  }

  async function askHealthQuestion(question) {
    const N8N_WEBHOOK_URL = 'https://cuetmedical.app.n8n.cloud/webhook-test/medical-assistant';

    try {
      var res = await fetch(N8N_WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: question,
          timestamp: new Date().toISOString(),
          source: 'student_ai_portal'
        })
      });

      if (!res.ok) {
        throw new Error('Assistant request failed.');
      }

      var data;
      const contentType = res.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await res.json().catch(() => ({}));
      } else {
        data = await res.text();
      }

      // Handle common n8n response patterns (array or object)
      if (Array.isArray(data)) {
        data = data[0] || {};
      }

      let answer = '';
      if (typeof data === 'string') {
        answer = data;
      } else {
        // Check common result fields returned by AI nodes in n8n
        answer = data.output || data.answer || data.response || data.text;
      }

      return answer || (typeof data === 'string' ? data : 'I received your message but couldn\'t generate a specific answer. Please try again.');
    } catch (err) {
      console.error('N8N Webhook Error:', err);
      throw new Error('Connection to AI Assistant failed. Please check your internet or try again later.');
    }
  }

  window.CUETApiClient = {
    API_BASE_URL: API_BASE_URL,
    getAuthHeaders: getAuthHeaders,
    askHealthQuestion: askHealthQuestion
  };
})();
