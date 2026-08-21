'use strict';

const DEFAULT_MODEL = process.env.ZARGOX_MODEL || 'deepseek-v4-flash';
const DEEPSEEK_API_URL = process.env.DEEPSEEK_API_URL || 'https://api.deepseek.com/chat/completions';

const SYSTEM_PROMPT = `You are Zargox, the public interactive AI of the MyZubster ecosystem.
Your job is to help everyone: beginners, students, citizens, makers, researchers and technical users.
Be useful, clear, respectful and practical. Reply in the user's language unless they ask otherwise.
When the user asks about MyZubster, explain it as an open environmental technology ecosystem and distinguish confirmed facts from ideas or proposals.
Never claim that fictional or narrative identities are real-world scientific facts.
Do not expose secrets, credentials or private system data.
For dangerous, illegal or harmful requests, refuse the harmful part and offer a safer alternative.
Keep answers concise by default, but expand when the user asks for detail.`;

function sanitizeHistory(history) {
  if (!Array.isArray(history)) return [];
  return history
    .slice(-12)
    .filter(item => item && (item.role === 'user' || item.role === 'assistant') && typeof item.content === 'string')
    .map(item => ({ role: item.role, content: item.content.slice(0, 6000) }));
}

async function getZargoxAIResponse(message, history = []) {
  const text = String(message || '').trim();
  if (!text) throw new Error('Message is required');

  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    const error = new Error('DEEPSEEK_API_KEY is not configured');
    error.code = 'deepseek_key_missing';
    throw error;
  }

  const messages = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...sanitizeHistory(history),
    { role: 'user', content: text.slice(0, 12000) }
  ];

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 45000);
  let response;
  try {
    response = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: DEFAULT_MODEL,
        messages,
        stream: false
      }),
      signal: controller.signal
    });
  } finally {
    clearTimeout(timer);
  }

  const raw = await response.text();
  let data;
  try {
    data = raw ? JSON.parse(raw) : {};
  } catch {
    const error = new Error(`DeepSeek returned invalid JSON (HTTP ${response.status})`);
    error.statusCode = response.status;
    throw error;
  }

  if (!response.ok) {
    const providerMessage = data?.error?.message || `DeepSeek request failed with HTTP ${response.status}`;
    const error = new Error(providerMessage);
    error.statusCode = response.status;
    throw error;
  }

  const output = data?.choices?.[0]?.message?.content;
  if (typeof output !== 'string' || !output.trim()) {
    throw new Error('DeepSeek returned an empty response');
  }

  return {
    text: output.trim(),
    model: data.model || DEFAULT_MODEL,
    provider: 'deepseek-direct'
  };
}

module.exports = { getZargoxAIResponse, DEFAULT_MODEL };
