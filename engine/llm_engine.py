"""Calculator GPT - Offline Micro-LLM Reasoning Engine (SmolLM2-135M).
Runs locally via llama-cpp-python with zero external API calls or internet connection.
Provides natural language reasoning, conceptual explanations, and mathematical guidance.
"""

import os
import sys
import re
import threading
from typing import Dict, Any, Optional

_MODEL_INSTANCE = None
_MODEL_LOCK = threading.Lock()
_MODEL_LOAD_FAILED = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "models", "smollm2-135m-instruct-q4_k_m.gguf")

SYSTEM_PROMPT = """You are "Calculator GPT", an elite offline mathematical AI and precision reasoning engine.
Your purpose:
1. Explain mathematical concepts, formulas, and theorems with clarity and rigor.
2. When answering, provide:
   - The primary formula or result directly.
   - Brief, bulleted derivation or reasoning steps.
   - A key practical insight or shortcut.
3. Keep responses concise, elegant, and strictly mathematical. No conversational fluff or disclaimers."""


def get_llm():
    """Lazily loads SmolLM2-135M in thread-safe manner."""
    global _MODEL_INSTANCE, _MODEL_LOAD_FAILED
    if _MODEL_INSTANCE is not None:
        return _MODEL_INSTANCE
    if _MODEL_LOAD_FAILED:
        return None

    with _MODEL_LOCK:
        if _MODEL_INSTANCE is not None:
            return _MODEL_INSTANCE
        
        # Resolve model path across standalone script, frozen onedir, or onefile
        candidates = []
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                candidates.append(os.path.join(sys._MEIPASS, "models", "smollm2-135m-instruct-q4_k_m.gguf"))
            candidates.append(os.path.join(os.path.dirname(sys.executable), "models", "smollm2-135m-instruct-q4_k_m.gguf"))
        candidates.append(DEFAULT_MODEL_PATH)
        candidates.append(os.path.join(os.getcwd(), "models", "smollm2-135m-instruct-q4_k_m.gguf"))

        model_path = None
        for p in candidates:
            if os.path.exists(p):
                model_path = p
                break

        if not model_path:
            print("[!] Warning: SmolLM2-135M model file not found in any candidate path.")
            _MODEL_LOAD_FAILED = True
            return None

        try:
            from llama_cpp import Llama
            _MODEL_INSTANCE = Llama(
                model_path=model_path,
                n_ctx=1024,
                n_threads=4,
                verbose=False
            )
            print("[*] Calculator GPT SmolLM2-135M Brain Initialized Successfully.")
            return _MODEL_INSTANCE
        except Exception as e:
            print(f"[!] Warning: Could not initialize SmolLM2-135M: {e}")
            _MODEL_LOAD_FAILED = True
            return None


def preload_llm_async():
    """Pre-warms the model in a background thread so the UI opens instantly."""
    t = threading.Thread(target=get_llm, daemon=True)
    t.start()


def solve_with_llm(query: str) -> Optional[Dict[str, Any]]:
    """Generates an intelligent mathematical explanation using local SmolLM2-135M."""
    llm = get_llm()
    if llm is None:
        return None

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Answer concisely and mathematically:\n{query}"}
        ]
        
        response = llm.create_chat_completion(
            messages=messages,
            temperature=0.15,
            max_tokens=180
        )
        
        content = response['choices'][0]['message']['content'].strip()
        if not content:
            return None

        # Extract structured elements from response text
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        summary = lines[0] if lines else "Mathematical Solution"
        formula = ""
        steps = []
        insights = ""

        # Look for explicit formula indicators
        for line in lines:
            if re.search(r'formula|identity|equation|holds?:', line, flags=re.I):
                formula = re.sub(r'^(?:formula|identity|equation)[:\s]*', '', line, flags=re.I).strip()
                break
        
        # Extract steps
        for line in lines[1:]:
            if re.match(r'^(?:[-*•]|\d+[\.)])\s+', line):
                step_text = re.sub(r'^(?:[-*•]|\d+[\.)])\s+', '', line).strip()
                if step_text:
                    steps.append(step_text)
            elif not formula and '=' in line and len(line) < 60:
                formula = line.strip()

        if not steps and len(lines) > 1:
            steps = lines[1:4]

        # Extract insights
        for line in lines:
            if re.search(r'insight|note|shortcut|tip|remember:', line, flags=re.I):
                insights = re.sub(r'^(?:insight|note|shortcut|tip|remember:)[:\s]*', '', line, flags=re.I).strip()
                break

        if not insights:
            insights = "Generated locally via Calculator GPT SmolLM2-135M offline neural model."

        return {
            "title": "Calculator GPT AI Reasoning",
            "summary_value": summary,
            "formula": formula if formula else summary,
            "rows": [
                ["Engine", "SmolLM2-135M (Offline)"],
                ["Hardware", "Local CPU AVX2 Bytecode"],
                ["Query", query]
            ],
            "steps": steps if steps else ["Evaluated using local neural mathematical reasoning model."],
            "insights": insights,
            "raw": None
        }
    except Exception as e:
        print(f"[!] LLM inference error: {e}")
        return None
