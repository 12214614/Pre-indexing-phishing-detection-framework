const DEFAULT_BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://127.0.0.1:8000/api/core'
  : '/api/core';

const configuredApiBaseUrl = process.env.REACT_APP_API_BASE_URL;
const hasPlaceholder = configuredApiBaseUrl && configuredApiBaseUrl.includes('your-backend-domain');
const resolvedApiBaseUrl = configuredApiBaseUrl && !hasPlaceholder
  ? configuredApiBaseUrl
  : DEFAULT_BASE_URL;

export const API_BASE_URL = resolvedApiBaseUrl.replace(/\/$/, '');

export const verifyUrl = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/submit-url/`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ website_url: url }),
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();
    return data;
  } catch (err) {
    console.error('Verify URL API error:', err);
    throw err;
  }
};

export const getDashboardStats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  } catch (err) {
    console.error('Dashboard stats API error:', err);
    throw err;
  }
};

export const getUrlList = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/url-list/`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  } catch (err) {
    console.error('URL list API error:', err);
    throw err;
  }
};
