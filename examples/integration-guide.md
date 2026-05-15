# 🚀 Integration Guide - Calculator GPT API

यह guide आपको Calculator GPT API को विभिन्न platforms और applications में integrate करने में मदद देगा।

## 📱 Frontend Integration

### React / Next.js

```jsx
// components/CalculatorWidget.jsx
import React, { useState } from 'react';

export default function CalculatorWidget() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState('gemini');

  const handleCalculate = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('https://calculator-gpt.vercel.app/api/v1/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, model })
      });
      
      const data = await response.json();
      setResult(data.answer || 'Error occurred');
    } catch (error) {
      setResult(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="calculator-widget">
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a math question..."
        onKeyPress={(e) => e.key === 'Enter' && handleCalculate()}
      />
      <select value={model} onChange={(e) => setModel(e.target.value)}>
        <option value="gemini">Gemini</option>
        <option value="llama">Llama</option>
        <option value="gpt4">GPT-4</option>
        <option value="claude">Claude</option>
      </select>
      <button onClick={handleCalculate} disabled={loading}>
        {loading ? 'Calculating...' : 'Calculate'}
      </button>
      {result && <div className="result">{result}</div>}
    </div>
  );
}
```

### Vue.js

```vue
<template>
  <div class="calculator">
    <input v-model="query" @keyup.enter="calculate" placeholder="Math question...">
    <button @click="calculate" :disabled="loading">
      {{ loading ? 'Calculating...' : 'Calculate' }}
    </button>
    <p v-if="result">{{ result }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      result: '',
      loading: false,
      model: 'gemini'
    }
  },
  methods: {
    async calculate() {
      this.loading = true;
      try {
        const res = await fetch('https://calculator-gpt.vercel.app/api/v1/calculate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: this.query, model: this.model })
        });
        const data = await res.json();
        this.result = data.answer;
      } catch (error) {
        this.result = `Error: ${error.message}`;
      }
      this.loading = false;
    }
  }
}
</script>
```

### Angular

```typescript
// calculator.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class CalculatorService {
  private apiUrl = 'https://calculator-gpt.vercel.app/api/v1/calculate';

  constructor(private http: HttpClient) {}

  calculate(query: string, model: string = 'gemini') {
    return this.http.post<any>(this.apiUrl, { query, model });
  }
}

// calculator.component.ts
import { Component } from '@angular/core';
import { CalculatorService } from './calculator.service';

@Component({
  selector: 'app-calculator',
  template: `
    <input [(ngModel)]="query" (keyup.enter)="calculate()">
    <button (click)="calculate()" [disabled]="loading">Calculate</button>
    <p>{{ result }}</p>
  `
})
export class CalculatorComponent {
  query = '';
  result = '';
  loading = false;

  constructor(private service: CalculatorService) {}

  calculate() {
    this.loading = true;
    this.service.calculate(this.query).subscribe({
      next: (data) => {
        this.result = data.answer;
        this.loading = false;
      },
      error: (err) => {
        this.result = `Error: ${err.message}`;
        this.loading = false;
      }
    });
  }
}
```

---

## 🤖 Chatbot Integration

### Discord Bot (discord.py)

```python
import discord
from discord.ext import commands
import aiohttp

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://calculator-gpt.vercel.app/api/v1/calculate"

    @commands.command(name='calc')
    async def calculate(self, ctx, *, query):
        """Calculate math using AI"""
        async with ctx.typing():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.api_url,
                        json={'query': query, 'model': 'gemini'}
                    ) as resp:
                        data = await resp.json()
                        
                        embed = discord.Embed(
                            title="🧮 Calculator GPT",
                            description=data.get('answer', 'Error'),
                            color=discord.Color.blue()
                        )
                        await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Calculator(bot))
```

### Telegram Bot (python-telegram-bot)

```python
from telegram import Update
from telegram.ext import ContextTypes
import aiohttp
import json

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /calc <question>")
        return

    query = ' '.join(context.args)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://calculator-gpt.vercel.app/api/v1/calculate',
                json={'query': query}
            ) as resp:
                data = await resp.json()
                answer = data.get('answer', 'Error')
                await update.message.reply_text(f"🧮 {answer}")
    except Exception as e:
        await update.message.reply_text(f"❌ {str(e)}")
```

### Slack Bot

```python
from flask import Flask, request
from slack_bolt import App
import requests

app = App(token="xoxb-your-token", signing_secret="your-secret")

@app.command("/calc")
def handle_calc(ack, body, say):
    ack()
    query = body.get("text")
    
    try:
        response = requests.post(
            'https://calculator-gpt.vercel.app/api/v1/calculate',
            json={'query': query}
        )
        data = response.json()
        say(f"🧮 {data.get('answer', 'Error')}")
    except Exception as e:
        say(f"❌ {str(e)}")
```

### WhatsApp Bot (Twilio)

```python
from flask import Flask, request
from twilio.rest import Client
import requests

app = Flask(__name__)
client = Client("account_sid", "auth_token")

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From')

    try:
        response = requests.post(
            'https://calculator-gpt.vercel.app/api/v1/calculate',
            json={'query': incoming_msg}
        )
        data = response.json()
        answer = data.get('answer', 'Error')
    except:
        answer = "Unable to calculate"

    client.messages.create(
        body=f"🧮 {answer}",
        from_="whatsapp:+14155552671",
        to=sender
    )
    return "OK", 200
```

---

## 🔗 Automation & Workflow Integration

### Zapier

1. Create new workflow
2. Trigger: Form submission / Email / Any event
3. Action: Webhook POST
4. URL: `https://calculator-gpt.vercel.app/api/v1/calculate`
5. Request:
```json
{
  "query": "{{trigger_field}}"
}
```

### Make (formerly Integromat)

1. Create new scenario
2. Add Webhook trigger
3. Add HTTP module → POST
4. URL: `https://calculator-gpt.vercel.app/api/v1/calculate`
5. Body: 
```json
{
  "query": "{{1.body.question}}"
}
```

### IFTTT

1. If: Google Home / Alexa / Any trigger
2. Then: Webhook
3. URL: `https://calculator-gpt.vercel.app/api/v1/calculate`
4. Method: POST
5. Content Type: `application/json`
6. Body: `{"query":"{{TextField}}"}`

---

## 🤖 AI Agent Integration

### LangChain (Python)

```python
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
import requests

def calculator_gpt(query: str) -> str:
    """Calculate math problems"""
    response = requests.post(
        'https://calculator-gpt.vercel.app/api/v1/calculate',
        json={'query': query}
    )
    return response.json()['answer']

tools = [
    Tool(
        name="Calculator",
        func=calculator_gpt,
        description="Useful for mathematical calculations and conversions"
    )
]

llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

result = agent.run("What is 25% of 8000?")
print(result)
```

### LangChain.js (Node.js)

```javascript
import { Tool } from "langchain/tools";
import { initializeAgentExecutorWithOptions } from "langchain/agents";
import { OpenAI } from "langchain/llms/openai";

const calculatorTool = new Tool({
  name: "calculator_gpt",
  description: "Useful for math calculations",
  func: async (query) => {
    const res = await fetch(
      "https://calculator-gpt.vercel.app/api/v1/calculate",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      }
    );
    const data = await res.json();
    return data.answer;
  }
});

const tools = [calculatorTool];
const llm = new OpenAI({ temperature: 0 });

const executor = await initializeAgentExecutorWithOptions(tools, llm, {
  agentType: "zero-shot-react-description"
});

const result = await executor.call({ input: "What is 15% of 5000?" });
console.log(result);
```

### AutoGPT Plugin

```json
{
  "schema_version": "v1",
  "name_for_human": "Calculator GPT",
  "name_for_model": "calculator_gpt",
  "description_for_human": "AI Calculator for natural language math",
  "description_for_model": "Plugin for mathematical calculations in natural language",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "https://calculator-gpt.vercel.app/.well-known/openapi.json"
  },
  "contact_email": "sharmashyama1988@gmail.com",
  "legal_info_url": "https://github.com/sharmashyama1988-eng/calculator-gpt"
}
```

---

## 📊 Analytics & Logging

### Logging Integration

```javascript
// Middleware to log all API calls
async function logCalculation(query, answer, model, timestamp) {
  await fetch('YOUR_LOGGING_SERVICE/log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      answer,
      model,
      timestamp,
      source: 'calculator-gpt-api'
    })
  });
}

// Usage
const response = await fetch('https://calculator-gpt.vercel.app/api/v1/calculate', {
  method: 'POST',
  body: JSON.stringify({ query: "25% of 1000?" })
});
const data = await response.json();
await logCalculation("25% of 1000?", data.answer, 'gemini', new Date());
```

---

## 🔒 Security Best Practices

1. **Rate Limiting:** Implement on client side
```javascript
const RateLimiter = {
  lastCall: 0,
  minInterval: 1000, // 1 second
  
  async call(fn) {
    const now = Date.now();
    if (now - this.lastCall < this.minInterval) {
      throw new Error('Rate limited');
    }
    this.lastCall = now;
    return await fn();
  }
};
```

2. **Input Validation:**
```javascript
function validateQuery(query) {
  if (!query || query.length > 500) {
    throw new Error('Invalid query');
  }
  return query.trim();
}
```

3. **Error Handling:**
```javascript
try {
  const result = await calculate(query);
  return result;
} catch (error) {
  console.error('API Error:', error);
  return { error: 'Calculation failed', retryAfter: 60 };
}
```

---

## 📈 Performance Tips

1. **Batch Requests:** Use `/batch` endpoint for multiple calculations
2. **Cache Results:** Store frequently used calculations
3. **Use Appropriate Model:** 
   - `gemini`: Fast & free
   - `llama`: Good for complex math
   - `gpt4`: Most accurate
   - `claude`: Best for detailed explanations

4. **Connection Pooling:** Reuse HTTP connections
5. **Async Processing:** Use queues for batch operations

---

**Happy Integrating! 🚀**

For more examples, visit: https://github.com/sharmashyama1988-eng/calculator-gpt
