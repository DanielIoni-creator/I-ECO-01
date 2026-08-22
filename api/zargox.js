'use strict';

const { getZargoxAIResponse, DEFAULT_MODEL } = require('./zargox-ai.js');

function setHeaders(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
}

module.exports = async function handler(req, res) {
  setHeaders(res);

  if (req.method === 'OPTIONS') return res.status(204).end();

  if (req.method === 'GET') {
    return res.status(200).json({
      ok: true,
      name: 'Zargox',
      service: 'MyZubster Public AI',
      provider: 'deepseek-direct',
      model: DEFAULT_MODEL,
      public: true,
      configured: Boolean(process.env.DEEPSEEK_API_KEY),
      live_context: String(process.env.ZARGOX_LIVE_CONTEXT_ENABLED || 'true').toLowerCase() !== 'false',
      live_sources: ['Wikipedia', 'GDELT (time-sensitive queries)']
    });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  try {
    const body = req.body || {};
    const message = typeof body.message === 'string' ? body.message.trim() : '';
    if (!message) return res.status(400).json({ ok: false, error: 'message is required' });
    if (message.length > 12000) return res.status(400).json({ ok: false, error: 'message too long' });

    const mode = String(body.mode || 'Assistente').slice(0, 40);
    const tone = String(body.tone || 'Chiaro').slice(0, 40);
    const contextualMessage = `[Modalità: ${mode}; stile: ${tone}]\n${message}`;
    const result = await getZargoxAIResponse(contextualMessage, body.history || []);

    return res.status(200).json({
      ok: true,
      name: 'Zargox',
      response: result.text,
      model: result.model,
      provider: result.provider || 'deepseek-direct',
      live_context_used: Boolean(result.liveContextUsed),
      live_sources: result.liveSources || [],
      live_context_errors: result.liveContextErrors || [],
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Zargox AI error:', error);
    const missingKey = error && error.code === 'deepseek_key_missing';
    return res.status(missingKey ? 503 : 500).json({
      ok: false,
      error: missingKey ? 'DeepSeek API is not configured' : 'Zargox AI is temporarily unavailable',
      detail: process.env.NODE_ENV === 'production' ? undefined : error.message
    });
  }
};
