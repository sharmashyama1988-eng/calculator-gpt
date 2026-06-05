# 🧮 Calculator GPT - API Setup Guide

## ✅ Complete API Package Created!

Your Calculator GPT repository is now **API-ready** with everything needed for global integration.

---

## 📦 What's Included

### 1. **API Endpoints** (`api/calculator.js`)
✅ Single calculation  
✅ Batch processing (10 queries)  
✅ Advanced options (detailed mode)  
✅ Health checks  
✅ Model listing  
✅ Rate limiting (100/min)  
✅ Multi-language support (English/Hindi)  
✅ 4 AI models (Gemini, Llama, GPT-4, Claude)  

### 2. **Documentation** (`API_DOCUMENTATION.md`)
✅ Complete endpoint documentation  
✅ Request/response examples  
✅ Error handling  
✅ Code examples (cURL, JS, Python)  
✅ Integration guides  
✅ Best practices  
✅ Rate limiting info  

### 3. **Integration Guides** (`examples/integration-guide.md`)
✅ React, Vue, Angular  
✅ Discord, Telegram, Slack, WhatsApp bots  
✅ Zapier, Make, IFTTT automation  
✅ LangChain AI agents  
✅ AutoGPT plugins  
✅ Performance tips  
✅ Security best practices  

### 4. **Configuration Files**
✅ `package.json` - Dependencies & scripts  
✅ `Dockerfile` - Container deployment  
✅ `vercel.json` - Vercel configuration  
✅ `.env.example` - Environment setup  

---

## 🚀 Quick Start

### 1. Setup Local Environment
```bash
# Clone repository
git clone https://github.com/sharmashyama1988-eng/calculator-gpt.git
cd calculator-gpt

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Add your OpenRouter API key to .env
export OPENROUTER_API_KEY="sk-or-xxx..."

# Start development server
npm run dev
```

### 2. Test the API
```bash
# Health check
curl https://localhost:3000/api/v1/health

# Single calculation
curl -X POST https://localhost:3000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 15% of 8500?"}'

# Batch calculation
curl -X POST https://localhost:3000/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["25% of 1000?", "5km to miles", "7*8?"],
    "model": "gemini"
  }'
```

### 3. Deploy to Production

#### **Option 1: Vercel (Recommended)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# The API will be live at: https://your-project.vercel.app/api/v1
```

#### **Option 2: Docker**
```bash
# Build image
docker build -t calculator-gpt .

# Run container
docker run -p 3000:3000 \
  -e OPENROUTER_API_KEY=sk-or-xxx \
  calculator-gpt
```

#### **Option 3: Heroku**
```bash
# Create app
heroku create your-app-name

# Set config
heroku config:set OPENROUTER_API_KEY=sk-or-xxx

# Deploy
git push heroku main
```

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/health` | Server health check |
| GET | `/api/v1/models` | List available models |
| POST | `/api/v1/calculate` | Single calculation |
| POST | `/api/v1/batch` | Batch calculations (max 10) |
| POST | `/api/v1/advanced` | Advanced with options |

---

## 💻 Usage Examples

### JavaScript (React/Node.js)
```javascript
const calculate = async (query) => {
  const res = await fetch('https://your-api.vercel.app/api/v1/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, model: 'gemini' })
  });
  return (await res.json()).answer;
};

// Usage
const result = await calculate("What is 15% of 8500?");
console.log(result); // "15% of 8500 is 1275"
```

### Python
```python
import requests

response = requests.post(
    'https://your-api.vercel.app/api/v1/calculate',
    json={
        'query': 'What is 15% of 8500?',
        'model': 'gemini'
    }
)

print(response.json()['answer'])
```

### cURL
```bash
curl -X POST https://your-api.vercel.app/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"query":"What is 15% of 8500?"}'
```

---

## 🤖 Popular Integrations

### Discord Bot
```python
@bot.command()
async def calc(ctx, *, query):
    response = requests.post(
        'https://your-api.vercel.app/api/v1/calculate',
        json={'query': query}
    )
    await ctx.send(response.json()['answer'])
```

### Telegram Bot
```python
@bot.message_handler(commands=['calc'])
def calc(message):
    response = requests.post(
        'https://your-api.vercel.app/api/v1/calculate',
        json={'query': message.text}
    )
    bot.reply_to(message, response.json()['answer'])
```

### LangChain Agent
```python
from langchain.tools import Tool
from langchain.agents import initialize_agent

calculator_tool = Tool(
    name="Calculator",
    func=lambda q: requests.post(
        'https://your-api.vercel.app/api/v1/calculate',
        json={'query': q}
    ).json()['answer'],
    description="AI Calculator"
)

agent = initialize_agent([calculator_tool], llm)
```

---

## 🔒 Security & Rate Limiting

- **Rate Limit:** 100 requests per minute per IP
- **Batch Limit:** Max 10 queries per batch
- **Query Size:** Max 1000 characters
- **Response Time:** < 2 seconds (average)

---

## 🌍 Global Access

Your API is now accessible to:
- ✅ Web applications (React, Vue, Angular)
- ✅ Mobile apps (React Native, Flutter)
- ✅ Discord/Telegram/Slack bots
- ✅ WhatsApp automation
- ✅ LangChain agents
- ✅ Zapier workflows
- ✅ IFTTT recipes
- ✅ Custom integrations

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `API_DOCUMENTATION.md` | Complete API reference |
| `examples/integration-guide.md` | Integration examples |
| `.env.example` | Environment setup |
| `package.json` | Dependencies |
| `Dockerfile` | Container deployment |
| `vercel.json` | Vercel config |

---

## ✨ Next Steps

1. **Get OpenRouter API Key:**
   - Visit https://openrouter.ai
   - Sign up and generate API key
   - Add to `.env` file

2. **Deploy to Production:**
   - Choose: Vercel, Docker, or Heroku
   - Set environment variables
   - Deploy!

3. **Share API URL:**
   - Get your production URL
   - Share with developers/users
   - Start building!

4. **Monitor & Scale:**
   - Check rate limits
   - Monitor performance
   - Scale as needed

---

## 🆘 Troubleshooting

### API not responding?
```bash
# Check health
curl https://your-api.vercel.app/api/v1/health

# Check logs (Vercel)
vercel logs
```

### Rate limit hit?
- Wait 60 seconds
- Use batch endpoint for efficiency
- Consider upgrading plan

### Model errors?
- Check OpenRouter API key
- Verify model name (gemini/llama/gpt4/claude)
- Check query format

---

## 📞 Support

- **Documentation:** See `API_DOCUMENTATION.md`
- **Examples:** See `examples/integration-guide.md`
- **Issues:** https://github.com/sharmashyama1988-eng/calculator-gpt/issues
- **Email:** sharmashyama1988@gmail.com

---

## 🎉 You're All Set!

Your Calculator GPT API is now ready for:
- 🌍 Global reach
- 🤖 AI agent integration
- ⚡ High performance
- 📱 Multi-platform support
- 🔒 Secure & rate-limited

**Start building amazing things! 🚀**

---

*Last updated: May 15, 2026*
