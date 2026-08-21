'use strict';

const DEFAULT_MODEL = process.env.ZARGOX_MODEL || 'openai/gpt-5.4-mini';

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

  const { generateText } = await import('ai');
  const messages = [...sanitizeHistory(history), { role: 'user', content: text.slice(0, 12000) }];

  const result = await generateText({
    model: DEFAULT_MODEL,
    system: SYSTEM_PROMPT,
    messages
  });

  return {
    text: result.text,
    model: DEFAULT_MODEL
  };
}

module.exports = { getZargoxAIResponse, DEFAULT_MODEL };
