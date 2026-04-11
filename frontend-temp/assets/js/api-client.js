// Shared API helper for frontend pages.
(function () {
  var API_BASE_URL = 'http://127.0.0.1:8000/api';

  function getAuthHeaders() {
    var token = localStorage.getItem('accessToken');
    var headers = { 'Content-Type': 'application/json' };
    if (token) headers.Authorization = 'Bearer ' + token;
    return headers;
  }

  async function askHealthQuestion(question) {
    var res = await fetch(API_BASE_URL + '/assistant/ask/', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ question: question })
    });

    var data = await res.json().catch(function () {
      return {};
    });

    if (!res.ok) {
      throw new Error(data.detail || 'Assistant request failed.');
    }

    return data.answer || 'No answer generated.';
  }

  window.CUETApiClient = {
    API_BASE_URL: API_BASE_URL,
    getAuthHeaders: getAuthHeaders,
    askHealthQuestion: askHealthQuestion
  };
})();
