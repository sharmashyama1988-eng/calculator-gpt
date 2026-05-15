const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const axios = require('axios');
require('dotenv').config();

const app = express();

// Middleware
app.use(express.json());
app.use(cors({
  origin: '*',
  credentials: true,
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Rate limiter: 100 requests per minute
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100,
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false
});

app.use(limiter);

// Constants
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
const API_BASE_URL = 'https://openrouter.ai/api/v1/chat/completions';

const MODELS = {
  gemini: 'google/gemini-2.0-flash-exp:free',
  llama: 'meta-llama/llama-3.1-70b-instruct:free',
  gpt4: 'openai/gpt-4-turbo',
  claude: 'anthropic/claude-3.5-sonnet:beta'
};

// System prompts
const SYSTEM_PROMPTS = {
  en: `You are an expert AI calculator. When someone asks a mathematical question, provide:
1. The direct answer
2. The calculation steps (if relevant)
3. Any important notes

Be concise and clear. For percentage, conversion, and financial calculations, show the formula.
If the question is not mathematical, politely decline.`,

  hi: `आप एक विशेषज्ञ AI कैलकुलेटर हैं। जब कोई गणितीय प्रश्न पूछे:
1. सीधा उत्तर दें
2. गणना के चरण दिखाएं (यदि प्रासंगिक हो)
3. कोई महत्वपूर्ण नोट्स

संक्षिप्त और स्पष्ट रहें। प्रतिशत, रूपांतरण और वित्तीय गणनाओं के लिए सूत्र दिखाएं।`
};

/**
 * GET /api/v1/health
 * Check API health status
 */
app.get('/api/v1/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development'
  });
});

/**
 * GET /api/v1/models
 * List available AI models
 */
app.get('/api/v1/models', (req, res) => {
  res.json({
    models: [
      {
        id: 'gemini',
        name: 'Google Gemini 2.0 Flash',
        speed: 'Very Fast',
        accuracy: 'High',
        cost: 'Free',
        description: 'Best for quick calculations'
      },
      {
        id: 'llama',
        name: 'Meta Llama 3.1 70B',
        speed: 'Fast',
        accuracy: 'High',
        cost: 'Free',
        description: 'Good for complex math'
      },
      {
        id: 'gpt4',
        name: 'OpenAI GPT-4 Turbo',
        speed: 'Medium',
        accuracy: 'Very High',
        cost: 'Paid',
        description: 'Most accurate for edge cases'
      },
      {
        id: 'claude',
        name: 'Anthropic Claude 3.5 Sonnet',
        speed: 'Medium',
        accuracy: 'Very High',
        cost: 'Paid',
        description: 'Best explanations'
      }
    ],
    defaultModel: 'gemini'
  });
});

/**
 * POST /api/v1/calculate
 * Single calculation
 */
app.post('/api/v1/calculate', async (req, res) => {
  try {
    const { query, model = 'gemini', language = 'en', detailed = false } = req.body;

    if (!query || query.trim().length === 0) {
      return res.status(400).json({ error: 'Query is required' });
    }

    if (query.length > 1000) {
      return res.status(400).json({ error: 'Query too long (max 1000 chars)' });
    }

    const selectedModel = MODELS[model] || MODELS.gemini;
    const systemPrompt = SYSTEM_PROMPTS[language] || SYSTEM_PROMPTS.en;

    const response = await axios.post(
      API_BASE_URL,
      {
        model: selectedModel,
        messages: [
          {
            role: 'system',
            content: systemPrompt
          },
          {
            role: 'user',
            content: query
          }
        ],
        temperature: 0.3,
        max_tokens: detailed ? 500 : 200
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
          'HTTP-Referer': req.get('origin') || 'http://localhost:3000',
          'X-Title': 'Calculator GPT API'
        }
      }
    );

    const answer = response.data.choices[0].message.content;

    res.json({
      success: true,
      query,
      answer,
      model,
      language,
      timestamp: new Date().toISOString(),
      usage: {
        prompt_tokens: response.data.usage.prompt_tokens,
        completion_tokens: response.data.usage.completion_tokens,
        total_tokens: response.data.usage.total_tokens
      }
    });
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    res.status(500).json({
      error: 'Calculation failed',
      message: error.response?.data?.error?.message || error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * POST /api/v1/batch
 * Multiple calculations (max 10)
 */
app.post('/api/v1/batch', async (req, res) => {
  try {
    const { queries, model = 'gemini', language = 'en' } = req.body;

    if (!Array.isArray(queries) || queries.length === 0) {
      return res.status(400).json({ error: 'Queries must be a non-empty array' });
    }

    if (queries.length > 10) {
      return res.status(400).json({ error: 'Maximum 10 queries per batch' });
    }

    const selectedModel = MODELS[model] || MODELS.gemini;
    const systemPrompt = SYSTEM_PROMPTS[language] || SYSTEM_PROMPTS.en;

    const results = await Promise.all(
      queries.map(async (query) => {
        try {
          const response = await axios.post(
            API_BASE_URL,
            {
              model: selectedModel,
              messages: [
                {
                  role: 'system',
                  content: systemPrompt
                },
                {
                  role: 'user',
                  content: query
                }
              ],
              temperature: 0.3,
              max_tokens: 200
            },
            {
              headers: {
                'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
                'HTTP-Referer': req.get('origin') || 'http://localhost:3000',
                'X-Title': 'Calculator GPT API'
              }
            }
          );

          return {
            query,
            answer: response.data.choices[0].message.content,
            status: 'success'
          };
        } catch (error) {
          return {
            query,
            error: error.message,
            status: 'failed'
          };
        }
      })
    );

    res.json({
      success: true,
      totalQueries: queries.length,
      successfulQueries: results.filter(r => r.status === 'success').length,
      results,
      model,
      language,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Batch API Error:', error.message);
    res.status(500).json({
      error: 'Batch processing failed',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * POST /api/v1/advanced
 * Advanced calculation with detailed options
 */
app.post('/api/v1/advanced', async (req, res) => {
  try {
    const {
      query,
      model = 'gemini',
      language = 'en',
      showSteps = true,
      format = 'text'
    } = req.body;

    if (!query || query.trim().length === 0) {
      return res.status(400).json({ error: 'Query is required' });
    }

    const selectedModel = MODELS[model] || MODELS.gemini;
    
    let systemPrompt = SYSTEM_PROMPTS[language] || SYSTEM_PROMPTS.en;
    if (showSteps) {
      systemPrompt += '\n\nAlways provide step-by-step solution.';
    }
    if (format === 'json') {
      systemPrompt += '\n\nFormat response as valid JSON with fields: answer, steps[], formula, explanation';
    }

    const response = await axios.post(
      API_BASE_URL,
      {
        model: selectedModel,
        messages: [
          {
            role: 'system',
            content: systemPrompt
          },
          {
            role: 'user',
            content: query
          }
        ],
        temperature: 0.2,
        max_tokens: 800
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
          'HTTP-Referer': req.get('origin') || 'http://localhost:3000',
          'X-Title': 'Calculator GPT API'
        }
      }
    );

    let answer = response.data.choices[0].message.content;

    if (format === 'json') {
      try {
        answer = JSON.parse(answer);
      } catch (e) {
        // Return as is if JSON parsing fails
      }
    }

    res.json({
      success: true,
      query,
      answer,
      model,
      language,
      format,
      showSteps,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Advanced API Error:', error.response?.data || error.message);
    res.status(500).json({
      error: 'Advanced calculation failed',
      message: error.response?.data?.error?.message || error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message,
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
    availableEndpoints: [
      'GET /api/v1/health',
      'GET /api/v1/models',
      'POST /api/v1/calculate',
      'POST /api/v1/batch',
      'POST /api/v1/advanced'
    ]
  });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Calculator GPT API running on port ${PORT}`);
  console.log(`📝 API Documentation: https://github.com/sharmashyama1988-eng/calculator-gpt`);
  console.log(`🌍 Health check: http://localhost:${PORT}/api/v1/health`);
});

module.exports = app;
