"""Natural Language & Intent Parser for Calculator GPT.
Detects user intention, normalizes Indian/Western numbering systems (Lakh, Crore, Million, k),
parses Hinglish & English mathematical queries, and extracts entities without external APIs.
"""

import re
from typing import Dict, Any, List, Optional, Tuple


def normalize_query(text: str) -> str:
    """Cleans up text, normalizes currencies, numbering abbreviations, and operators."""
    if not text:
        return ""
    
    q = text.strip()
    
    # Currency symbols & prefixes
    q = re.sub(r'[₹$€£]', '', q)
    q = re.sub(r'\b(?:rs\.?|inr|rupees?|bucks?)\s*', '', q, flags=re.IGNORECASE)
    
    # Comma separation in numbers (e.g., 25,00,000 -> 2500000)
    q = re.sub(r'(\d),(\d)', r'\1\2', q)
    
    # Indian & Western Number word expansions
    def expand_crore(m):
        val = float(m.group(1))
        return str(int(val * 1e7) if (val * 1e7).is_integer() else val * 1e7)
    
    def expand_lakh(m):
        val = float(m.group(1))
        return str(int(val * 1e5) if (val * 1e5).is_integer() else val * 1e5)
    
    def expand_million(m):
        val = float(m.group(1))
        return str(int(val * 1e6) if (val * 1e6).is_integer() else val * 1e6)
    
    def expand_k(m):
        val = float(m.group(1))
        return str(int(val * 1e3) if (val * 1e3).is_integer() else val * 1e3)

    q = re.sub(r'(\d+(?:\.\d+)?)\s*(?:crores?|cr)\b', expand_crore, q, flags=re.IGNORECASE)
    q = re.sub(r'(\d+(?:\.\d+)?)\s*(?:lakhs?|lacs?)\b', expand_lakh, q, flags=re.IGNORECASE)
    q = re.sub(r'(\d+(?:\.\d+)?)\s*(?:millions?|mn)\b', expand_million, q, flags=re.IGNORECASE)
    q = re.sub(r'(\d+(?:\.\d+)?)\s*k\b', expand_k, q, flags=re.IGNORECASE)
    
    # Mathematical operator normalization
    q = q.replace('×', '*').replace('÷', '/').replace('−', '-').replace('–', '-')
    q = q.replace('²', '^2').replace('³', '^3')
    
    return q


def extract_numbers(text: str) -> List[float]:
    """Extracts all integer and float numbers from a text string."""
    matches = re.findall(r'[-+]?\d*\.?\d+', text)
    nums = []
    for m in matches:
        try:
            nums.append(float(m))
        except ValueError:
            continue
    return nums


def detect_intent(text: str) -> str:
    """Classifies the user's mathematical intent based on keywords, syntax, and patterns."""
    q = text.lower()
    
    # 1. Calculus: Derivative & Integration
    if re.search(r'\b(?:diff|differentiate|derivative|d/dx|slope of|tangent to)\b', q):
        return "CALCULUS_DERIVATIVE"
    if re.search(r'\b(?:integrate|integration|integral|antiderivative|area under|int\b)', q):
        return "CALCULUS_INTEGRAL"
    if re.search(r'\b(?:limit|lim\b|approaches|as x ->)', q):
        return "CALCULUS_LIMIT"
        
    # 2. Statistics
    if re.search(r'\b(?:mean|median|mode|variance|standard deviation|std dev|deviation|stat|stats|average|avg)\b', q) and len(extract_numbers(q)) >= 3:
        return "STATISTICS"
        
    # 3. Algebra & Equations
    if re.search(r'\b(?:solve|roots? of|find x|equation|samikaran)\b', q) or ('=' in q and re.search(r'[a-zA-Z]', q)):
        return "EQUATION_SOLVER"
    if re.search(r'\b(?:expand|whole square|whole cube|polynomial|prasar)\b', q) or re.search(r'\([a-zA-Z0-9\s+-]+\)\s*\^[23]', q):
        return "ALGEBRA_EXPAND"
    if re.search(r'\b(?:factor|factorise|factorize|gudankhand)\b', q):
        return "ALGEBRA_FACTOR"
        
    # 4. Quantitative Aptitude & Word Problems
    if re.search(r'\b(?:train|trains|railgadi|opposite direction|same direction|aamne samne|ek hi disha|relative speed|crossing|platform|pole)\b', q):
        return "APTITUDE_TRAIN"
    if re.search(r'\b(?:boat|stream|current|upstream|downstream|dhara|nau|naav)\b', q):
        return "APTITUDE_BOAT"
    if re.search(r'\b(?:work|kaam|together|milkar|alone|dono milkar|alternate days?|pipe|cistern|tank|nal)\b', q):
        return "APTITUDE_TIME_WORK"
    if re.search(r'\b(?:profit|loss|gain|cost price|selling price|marked price|discount|cp|sp|mp|khareeda|becha|faida|nuksan|chhut)\b', q):
        return "APTITUDE_PROFIT_LOSS"
    if re.search(r'\b(?:emi|loan|kisht)\b', q):
        return "APTITUDE_EMI"
    if re.search(r'\b(?:compound interest|ci|chakravriddhi|compounded|maturity)\b', q):
        return "APTITUDE_CI"
    if re.search(r'\b(?:simple interest|si|sadharan byaj|interest rate)\b', q):
        return "APTITUDE_SI"
    if re.search(r'\b(?:gst|tax|vat)\b', q):
        return "APTITUDE_GST"
    if re.search(r'\b(?:mixture|alligation|solution|ratio of milk|mishran)\b', q):
        return "APTITUDE_MIXTURE"
    if re.search(r'\b(?:age|ages|father|son|mother|daughter|years ago|hence|umra|aayu)\b', q):
        return "APTITUDE_AGE"
        
    # 5. Number Theory & Discrete Math
    if re.search(r'\b(?:lcm|lowest common multiple|laghuttam)\b', q):
        return "NUMBER_THEORY_LCM"
    if re.search(r'\b(?:hcf|gcd|greatest common divisor|mahattam)\b', q):
        return "NUMBER_THEORY_GCD"
    if re.search(r'\b(?:prime|avibhajiya|composite)\b', q):
        return "NUMBER_THEORY_PRIME"
    if re.search(r'\b(?:factors?|divisors?)\b', q):
        return "NUMBER_THEORY_FACTORS"
    if re.search(r'\b(?:combination|combinations|ncr|\d+c\d+)\b', q):
        return "NUMBER_THEORY_NCR"
    if re.search(r'\b(?:permutation|permutations|npr|\d+p\d+)\b', q):
        return "NUMBER_THEORY_NPR"
    if re.search(r'\b(?:fibonacci|series|ap|arithmetic progression|gp|geometric progression)\b', q):
        return "NUMBER_THEORY_SERIES"
        
    # 6. Matrices & Linear Algebra
    if re.search(r'\b(?:matrix|determinant|det|inverse of matrix|eigenvalues?|transpose)\b', q):
        return "MATRIX_OPERATIONS"
        
    # 7. Geometry & Trigonometry
    if re.search(r'\b(?:circle|radius|diameter|circumference|cylinder|cone|sphere|hypotenuse|pythagoras|triangle|rectangle|area|volume)\b', q):
        return "GEOMETRY"
        
    # 8. Direct arithmetic evaluation fallback
    return "ARITHMETIC_EXPR"
