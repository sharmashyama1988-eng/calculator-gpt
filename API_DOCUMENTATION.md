# 🚀 Calculator GPT - Complete API Documentation

## ✨ Welcome!

**Calculator GPT API** is a production-ready REST API that leverages multiple AI models to solve mathematical problems using natural language.

**Base URL:** `https://calculator-gpt.vercel.app` (or your deployment URL)

---

## 📊 Quick Stats

| Feature | Details |
|---------|---------|
| **Models** | Gemini, Llama, GPT-4, Claude |
| **Rate Limit** | 100 requests/minute per IP |
| **Response Time** | < 2 seconds average |
| **Languages** | English, Hindi |
| **Max Query Size** | 1000 characters |
| **Batch Size** | Max 10 queries |

---

## 🔑 Authentication

Currently, the API is **open** (no API key required for basic usage). For production deployments, consider adding authentication.

---

## 📡 API Endpoints

### 1. Health Check
**GET** `/api/v1/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-05-15T18:50:00Z",
  "uptime": 12345.67,
  "environment": "production"
}
```

**cURL:**
```bash
curl https://calculator-gpt.vercel.app/api/v1/health
```

---

### 2. List Models
**GET** `/api/v1/models`

Get all available AI models.

**Response:**
```json
{
  "models": [
    {
      "id": "gemini",
      "name": "Google Gemini 2.0",
      "speed": "Very Fast",
      "accuracy": "High",
      "cost": "Free",
      "description": "Best for quick calculations"
    },
    {
      "id": "llama",
      "name": "Meta Llama 3.1 70B",
      "speed": "Fast",
      "accuracy": "High",
      "cost": "Free"
    },
    {
      "id": "gpt4",
      "name": "OpenAI GPT-4 Turbo",
      "speed": "Medium",
      "accuracy": "Very High",
      "cost": "Paid"
    },
    {
      "id": "claude",
      "name": "Anthropic Claude 3.5",
      "speed": "Medium",
      "accuracy": "Very High",
      "cost": "Paid"
    }
  ],
  "defaultModel": "gemini"
}
```

**cURL:**
```bash
curl https://calculator-gpt.vercel.app/api/v1/models
```

---

### 3. Single Calculation
**POST** `/api/v1/calculate`

Solve a single math problem using natural language.

**Request Body:**
```json
{
  "query": "What is 15% of 8500?",
  "model": "gemini",
  "language": "en",
  "detailed": false
}
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | Required | Your math question |
| `model` | string | `gemini` | AI model: gemini, llama, gpt4, claude |
| `language` | string | `en` | Language: en, hi |
| `detailed` | boolean | `false` | Get detailed explanation |

**Response:**
```json
{
  "success": true,
  "query": "What is 15% of 8500?",
  "answer": "15% of 8500 is 1275",
  "model": "gemini",
  "language": "en",
  "timestamp": "2026-05-15T18:50:00Z",
  "usage": {
    "prompt_tokens": 45,
    "completion_tokens": 12,
    "total_tokens": 57
  }
}
```

**cURL:**
```bash
curl -X POST https://calculator-gpt.vercel.app/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is 15% of 8500?",
    "model": "gemini"
  }'
```

**JavaScript:**
```javascript
const response = await fetch('https://calculator-gpt.vercel.app/api/v1/calculate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What is 15% of 8500?',
    model: 'gemini'
  })
});

const data = await response.json();
console.log(data.answer); // "15% of 8500 is 1275"
```

**Python:**
```python
import requests

response = requests.post(
  'https://calculator-gpt.vercel.app/api/v1/calculate',
  json={
    'query': 'What is 15% of 8500?',
    'model': 'gemini'
  }
)

print(response.json()['answer'])
```

---

### 4. Batch Calculations
**POST** `/api/v1/batch`

Process multiple calculations in a single request (max 10).

**Request Body:**
```json
{
  "queries": [
    "What is 25% of 1000?",
    "Convert 5 km to miles",
    "7 * 8 = ?"
  ],
  "model": "gemini",
  "language": "en"
}
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `queries` | array | Required | Array of queries (max 10) |
| `model` | string | `gemini` | AI model to use |
| `language` | string | `en` | Language: en, hi |

**Response:**
```json
{
  "success": true,
  "totalQueries": 3,
  "successfulQueries": 3,
  "results": [
    {
      "query": "What is 25% of 1000?",
      "answer": "25% of 1000 is 250",
      "status": "success"
    },
    {
      "query": "Convert 5 km to miles",
      "answer": "5 km is approximately 3.11 miles",
      "status": "success"
    },
    {
      "query": "7 * 8 = ?",
      "answer": "7 * 8 = 56",
      "status": "success"
    }
  ],
  "model": "gemini",
  "language": "en",
  "timestamp": "2026-05-15T18:50:00Z"
}
```

**cURL:**
```bash
curl -X POST https://calculator-gpt.vercel.app/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["25% of 1000?", "5km to miles", "7*8?"],
    "model": "gemini"
  }'
```

**JavaScript:**
```javascript
const queries = [
  "25% of 1000?",
  "5km to miles",
  "7*8?"
];

const response = await fetch('https://calculator-gpt.vercel.app/api/v1/batch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ queries, model: 'gemini' })
});

const data = await response.json();
data.results.forEach(r => console.log(r.answer));
```

---

### 5. Advanced Calculation
**POST** `/api/v1/advanced`

Get detailed calculations with step-by-step solutions.

**Request Body:**
```json
{
  "query": "Simple interest on ₹10000 at 8% for 3 years",
  "model": "gemini",
  "language": "en",
  "showSteps": true,
  "format": "text"
}
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | Required | Your math question |
| `model` | string | `gemini` | AI model to use |
| `language` | string | `en` | Language: en, hi |
| `showSteps` | boolean | `true` | Show step-by-step solution |
| `format` | string | `text` | Output format: text, json |

**Response (text format):**
```json
{
  "success": true,
  "query": "Simple interest on ₹10000 at 8% for 3 years",
  "answer": "Simple Interest = (Principal × Rate × Time) / 100\n= (10000 × 8 × 3) / 100\n= 2400\n\nTotal Amount = Principal + Interest = 10000 + 2400 = ₹12400",
  "model": "gemini",
  "language": "en",
  "format": "text",
  "showSteps": true,
  "timestamp": "2026-05-15T18:50:00Z"
}
```

**Response (JSON format):**
```json
{
  "success": true,
  "query": "Simple interest on ₹10000 at 8% for 3 years",
  "answer": {
    "principal": 10000,
    "rate": 8,
    "time": 3,
    "formula": "SI = (P × R × T) / 100",
    "interest": 2400,
    "total_amount": 12400,
    "steps": [
      "Principal = ₹10000",
      "Rate = 8% per year",
      "Time = 3 years",
      "SI = (10000 × 8 × 3) / 100",
      "SI = ₹2400",
      "Total = 10000 + 2400 = ₹12400"
    ]
  },
  "model": "gemini",
  "format": "json",
  "showSteps": true,
  "timestamp": "2026-05-15T18:50:00Z"
}
```

**cURL:**
```bash
curl -X POST https://calculator-gpt.vercel.app/api/v1/advanced \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Simple interest on 10000 at 8% for 3 years",
    "model": "gemini",
    "showSteps": true
  }'
```

---

## ❌ Error Responses

### Bad Request (400)
```json
{
  "error": "Query is required",
  "timestamp": "2026-05-15T18:50:00Z"
}
```

### Rate Limited (429)
```json
{
  "error": "Too many requests, please try again later",
  "retryAfter": 60
}
```

### Server Error (500)
```json
{
  "error": "Calculation failed",
  "message": "OpenRouter API error",
  "timestamp": "2026-05-15T18:50:00Z"
}
```

---

## 📈 Rate Limiting

- **Limit:** 100 requests per minute per IP
- **Reset:** Every 60 seconds
- **Headers:** `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`

**Example Response Headers:**
```
RateLimit-Limit: 100
RateLimit-Remaining: 95
RateLimit-Reset: 1684163460
```

---

## 🎯 Example Queries

```
"What is 15% of 8500?"
"Convert 5 kilometers to miles"
"Simple interest on ₹10000 at 8% for 3 years"
"What is the square root of 144?"
"7 * 8 + 5 - 2"
"Convert 98.6 Fahrenheit to Celsius"
"30% discount on ₹5000 = ?"
"Compound interest on ₹1000 at 5% for 2 years"
"What is 2^10?"
"Find 3/4 of 200"
```

---

## 🔧 Best Practices

1. **Use Batch API** for multiple calculations
2. **Cache Results** when possible
3. **Handle Errors** gracefully
4. **Respect Rate Limits** (100/min)
5. **Use Appropriate Model** for your use case
   - Gemini: Fast & free (default)
   - Llama: Good for complex math
   - GPT-4: Most accurate
   - Claude: Best explanations

---

## 🚀 Deployment

### Vercel (Recommended)
```bash
vercel --prod
```

### Docker
```bash
docker build -t calculator-gpt .
docker run -p 3000:3000 -e OPENROUTER_API_KEY=sk-or-xxx calculator-gpt
```

### Heroku
```bash
git push heroku main
```

---

## 📚 Integration Examples

See `examples/integration-guide.md` for:
- React, Vue, Angular
- Discord, Telegram, Slack bots
- LangChain agents
- Zapier workflows
- Python scripts
- And more!

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check OpenRouter API key |
| 429 Too Many Requests | Wait 60 seconds, then retry |
| 500 Server Error | Check server logs |
| Slow responses | Use faster model (gemini) or check network |

---

## 📞 Support

- **GitHub:** https://github.com/sharmashyama1988-eng/calculator-gpt
- **Issues:** https://github.com/sharmashyama1988-eng/calculator-gpt/issues
- **Email:** sharmashyama1988@gmail.com

---

## 📄 License

MIT License - Feel free to use in your projects!

---

*Last updated: May 15, 2026*
*Build with ❤️ by Amit Kumar*
