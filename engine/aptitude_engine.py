"""Quantitative Aptitude & Word Problem Solver for Calculator GPT.
Handles complex competitive exam aptitude problems (trains, boats, work & time,
profit & loss, simple/compound interest, mixtures, and ages) with human-like step-by-step reasoning.
"""

import re
import math
from typing import Dict, Any, List, Optional, Tuple
from .nlp_parser import extract_numbers, normalize_query


def fmt(n: float, decimals: int = 2) -> str:
    """Formats numeric results cleanly for human presentation."""
    if not math.isfinite(n):
        return "Undefined"
    if n == int(n):
        return f"{int(n):,}"
    return f"{n:,.{decimals}f}".rstrip('0').rstrip('.')


def fmt_curr(n: float) -> str:
    """Formats numeric currency values in Indian numbering style (₹)."""
    if not math.isfinite(n):
        return "—"
    return f"₹{fmt(n, 2)}"


# ==============================================================================
# 1. TRAINS & RELATIVE SPEED
# ==============================================================================
def solve_train_problem(query: str) -> Optional[Dict[str, Any]]:
    """Solves train crossing problems, relative speeds, and platform lengths."""
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:train|trains|railgadi|platform|pole|bridge|speed|relative speed|opposite direction|same direction)\b', q):
        return None
    nums = extract_numbers(q)
    if len(nums) < 2:
        return None
        
    is_opposite = bool(re.search(r'opposite|aamne|samne|towards each other|ek dusre ki taraf', q))
    is_same = bool(re.search(r'same direction|ek hi disha|ek hi taraf', q))
    
    # Scenario A: Two trains speeds + Distance between them
    if len(nums) >= 3:
        # Sort or identify distance (usually the largest number if >= 100)
        s1, s2, dist = nums[0], nums[1], nums[2]
        if nums[2] > nums[0] and nums[2] > nums[1]:
            dist, s1, s2 = nums[2], nums[0], nums[1]
        elif nums[0] > nums[1] and nums[0] > nums[2]:
            dist, s1, s2 = nums[0], nums[1], nums[2]
            
        rel_speed = (s1 - s2) if (is_same and not is_opposite) else (s1 + s2)
        rel_speed = abs(rel_speed)
        
        if rel_speed == 0:
            return {
                "title": "Relative Speed (Train Problem)",
                "summary_value": "Never meet (Parallel speeds)",
                "formula": "Time = Distance ÷ Relative Speed",
                "rows": [["Relative Speed", "0 km/h"], ["Distance", f"{dist} km"]],
                "steps": ["Both trains have identical speeds in the same direction, so they maintain constant distance."],
                "insights": "When relative speed is 0, the gap between two bodies never closes.",
                "raw": None
            }
            
        time_hours = dist / rel_speed
        hrs = int(time_hours)
        mins = round((time_hours - hrs) * 60)
        
        time_str = f"{hrs}h {mins}m ({fmt(time_hours, 2)} hrs)" if hrs > 0 and mins > 0 else (f"{hrs} hours ({hrs} ghante)" if hrs > 0 else f"{mins} minutes")
        dir_name = "Opposite Direction (Speeds Add)" if not is_same else "Same Direction (Speeds Subtract)"
        
        steps = [
            f"Step 1: Identify train directions. Moving in {dir_name}.",
            f"Step 2: Calculate relative speed: S_rel = {s1} {'+' if not is_same else '−'} {s2} = {rel_speed} km/h.",
            f"Step 3: Distance to cover between them: D = {dist} km.",
            f"Step 4: Apply Time formula: T = Distance ÷ Relative Speed = {dist} ÷ {rel_speed} = {fmt(time_hours, 3)} hours.",
            f"Step 5: Convert decimal hours to minutes: {hrs} hours and {mins} minutes."
        ]
        
        return {
            "title": "Relative Speed (Train Problem)",
            "summary_value": time_str,
            "formula": "Time = Distance ÷ (Speed₁ ± Speed₂)",
            "rows": [
                ["Time to Meet", time_str],
                ["Relative Speed", f"{rel_speed} km/h ({dir_name})"],
                ["Total Distance", f"{dist} km"],
                ["Train 1 Speed", f"{s1} km/h"],
                ["Train 2 Speed", f"{s2} km/h"]
            ],
            "steps": steps,
            "insights": "Key Rule: When two objects move towards each other, their relative speed is S₁ + S₂. When moving in the same direction, it is |S₁ − S₂|.",
            "raw": time_hours
        }
        
    return None


# ==============================================================================
# 2. TIME & WORK / PIPES & CISTERNS
# ==============================================================================
def solve_time_work(query: str) -> Optional[Dict[str, Any]]:
    """Solves individual & collective work problems, pipe filling/emptying."""
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:work|kaam|together|milkar|alone|pipe|pipes|cistern|tank|tanki|nal|days?|din|hours?|ghante)\b', q):
        return None
    nums = extract_numbers(q)
    if len(nums) < 2:
        return None
        
    # Scenario: Person A in X days, Person B in Y days
    if len(nums) == 2:
        d1, d2 = nums[0], nums[1]
        together = (d1 * d2) / (d1 + d2)
        
        steps = [
            f"Step 1: Work done by Person A in 1 day = 1/{d1}",
            f"Step 2: Work done by Person B in 1 day = 1/{d2}",
            f"Step 3: Combined work done in 1 day = (1/{d1}) + (1/{d2}) = ({d1} + {d2}) / ({d1} × {d2}) = {d1+d2}/{d1*d2}",
            f"Step 4: Reciprocal gives total days: Total Days = ({d1} × {d2}) ÷ ({d1} + {d2}) = {d1*d2} ÷ {d1+d2} = {fmt(together, 2)} days"
        ]
        
        return {
            "title": "Time & Work (Combined Effort)",
            "summary_value": f"{fmt(together, 2)} days",
            "formula": "Total Days = (A × B) ÷ (A + B)",
            "rows": [
                ["Combined Time (Dono Milkar)", f"{fmt(together, 2)} days"],
                ["Person A Time", f"{d1} days (Rate: 1/{d1}/day)"],
                ["Person B Time", f"{d2} days (Rate: 1/{d2}/day)"],
                ["Combined Daily Rate", f"1/{fmt(together, 2)} of total job"]
            ],
            "steps": steps,
            "insights": "Work is inversely proportional to time. When multiple entities collaborate, their individual rates add up.",
            "raw": together
        }
        
    # Scenario: 3 people
    if len(nums) == 3:
        d1, d2, d3 = nums[0], nums[1], nums[2]
        comb_rate = (1/d1) + (1/d2) + (1/d3)
        total_time = 1 / comb_rate
        
        return {
            "title": "Time & Work (3 Persons Together)",
            "summary_value": f"{fmt(total_time, 2)} days",
            "formula": "1/T_total = 1/A + 1/B + 1/C",
            "rows": [
                ["Together Time", f"{fmt(total_time, 2)} days"],
                ["Person A", f"{d1} days"],
                ["Person B", f"{d2} days"],
                ["Person C", f"{d3} days"]
            ],
            "steps": [
                f"Daily rate of A = 1/{d1}, B = 1/{d2}, C = 1/{d3}",
                f"Combined rate = 1/{d1} + 1/{d2} + 1/{d3} = {comb_rate:.4f} job/day",
                f"Total days = 1 ÷ {comb_rate:.4f} = {fmt(total_time, 2)} days"
            ],
            "insights": "Three contributors working in parallel reduce total duration proportionally to their sum of rates.",
            "raw": total_time
        }
        
    return None


# ==============================================================================
# 3. COMMERCIAL MATH: PROFIT, LOSS & DISCOUNT
# ==============================================================================
def solve_profit_loss(query: str) -> Optional[Dict[str, Any]]:
    """Calculates profit, loss, cost price, selling price, and discounts."""
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:profit|loss|gain|cost price|selling price|marked price|markup|margin|discount|successive|cp|sp|mp|khareeda|becha|faida|nuksan|chhut)\b', q):
        return None
    nums = extract_numbers(q)
    if len(nums) < 2:
        return None
        
    # Successive discounts (e.g., 20% and 10% discount)
    if re.search(r'successive|single equivalent|two discounts?|chhut', q):
        d1, d2 = nums[0], nums[1]
        equiv = d1 + d2 - (d1 * d2 / 100)
        return {
            "title": "Successive Discount (Equivalent Single Discount)",
            "summary_value": f"{fmt(equiv, 2)}%",
            "formula": "Equivalent Discount = d₁ + d₂ − (d₁ × d₂) ÷ 100",
            "rows": [
                ["Single Equivalent Discount", f"{fmt(equiv, 2)}%"],
                ["First Discount (d₁)", f"{d1}%"],
                ["Second Discount (d₂)", f"{d2}%"]
            ],
            "steps": [
                f"Let original price be ₹100.",
                f"After first discount of {d1}%: Price = 100 − {d1} = ₹{100-d1}.",
                f"Second discount of {d2}% on ₹{100-d1}: Discount = {d2}% × {100-d1} = ₹{(100-d1)*d2/100:.2f}.",
                f"Total discount = {d1} + {(100-d1)*d2/100:.2f} = {fmt(equiv, 2)}%."
            ],
            "insights": "Two successive discounts are always strictly LESS than their simple arithmetic sum.",
            "raw": equiv
        }
        
    # Standard Profit & Loss
    cp, sp = nums[0], nums[1]
    diff = sp - cp
    pct = (diff / cp) * 100
    
    is_profit = diff >= 0
    nature = "Profit (Gain / Faida)" if is_profit else "Loss (Nuksan)"
    
    steps = [
        f"Cost Price (CP) = {fmt_curr(cp)}",
        f"Selling Price (SP) = {fmt_curr(sp)}",
        f"Difference: SP − CP = {fmt_curr(sp)} − {fmt_curr(cp)} = {fmt_curr(abs(diff))} ({'Gain' if is_profit else 'Loss'})",
        f"Percentage Formula: (Difference ÷ Cost Price) × 100",
        f"Calculation: ({abs(diff)} ÷ {cp}) × 100 = {fmt(abs(pct), 2)}%"
    ]
    
    return {
        "title": f"Commercial Mathematics: {nature}",
        "summary_value": f"{nature}: {fmt_curr(abs(diff))} ({fmt(abs(pct), 2)}%)",
        "formula": "Profit % = ((SP − CP) ÷ CP) × 100",
        "rows": [
            [f"Total {nature}", fmt_curr(abs(diff))],
            ["Percentage", f"{fmt(abs(pct), 2)}%"],
            ["Selling Price (SP)", fmt_curr(sp)],
            ["Cost Price (CP)", fmt_curr(cp)]
        ],
        "steps": steps,
        "insights": "Profit or Loss percentage is ALWAYS strictly calculated over the Cost Price (CP), never over SP.",
        "raw": diff
    }


# ==============================================================================
# 4. FINANCIAL: COMPOUND & SIMPLE INTEREST / EMI
# ==============================================================================
def solve_interest(query: str) -> Optional[Dict[str, Any]]:
    """Calculates Simple Interest, Compound Interest, and Amortized Loan EMIs."""
    q = normalize_query(query).lower()
    nums = extract_numbers(q)
    if len(nums) < 3:
        return None
        
    p, r, t = nums[0], nums[1], nums[2]
    
    # EMI Calculation
    if re.search(r'\b(?:emi|loan|kisht)\b', q):
        months = t if ('month' in q and 'year' not in q) else t * 12
        i = (r / 100) / 12
        emi = p * i * ((1 + i)**months) / (((1 + i)**months) - 1) if i > 0 else p / months
        total_paid = emi * months
        total_interest = total_paid - p
        
        return {
            "title": "Loan EMI & Amortization Breakdown",
            "summary_value": fmt_curr(emi) + " / month",
            "formula": "EMI = P × r × (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1)",
            "rows": [
                ["Monthly EMI", fmt_curr(emi)],
                ["Total Interest Payable", fmt_curr(total_interest)],
                ["Total Amount Payable", fmt_curr(total_paid)],
                ["Principal Loan Amount", fmt_curr(p)],
                ["Interest Rate", f"{r}% p.a."],
                ["Tenure", f"{int(months)} months ({fmt(months/12, 1)} years)"]
            ],
            "steps": [
                f"Principal Loan P = {fmt_curr(p)}",
                f"Monthly interest rate r = {r}% / 12 = {i*100:.4f}% = {i:.6f}",
                f"Total installments n = {int(months)} months",
                f"EMI Formula: P × r × (1+r)ⁿ ÷ ((1+r)ⁿ − 1) = {fmt_curr(emi)}",
                f"Total Repayment = EMI × {int(months)} = {fmt_curr(total_paid)}"
            ],
            "insights": "Early EMI payments contain a higher ratio of interest to principal. As the balance reduces, interest decreases.",
            "raw": emi
        }
        
    # Compound Interest
    if re.search(r'\b(?:compound|ci|chakravriddhi)\b', q):
        amount = p * ((1 + (r / 100))**t)
        ci = amount - p
        return {
            "title": "Compound Interest (Annual Compounding)",
            "summary_value": fmt_curr(ci),
            "formula": "A = P(1 + r/100)ᵗ,  CI = A − P",
            "rows": [
                ["Compound Interest Earned", fmt_curr(ci)],
                ["Total Maturity Amount (A)", fmt_curr(amount)],
                ["Principal Invested (P)", fmt_curr(p)],
                ["Annual Rate (r)", f"{r}%"],
                ["Duration (t)", f"{t} years"]
            ],
            "steps": [
                f"Principal P = {fmt_curr(p)}, Rate r = {r}%, Time t = {t} years",
                f"Maturity Formula: A = P × (1 + r/100)ᵗ = {p} × (1 + {r/100})^{t}",
                f"Total Maturity = {fmt_curr(amount)}",
                f"Interest CI = A − P = {fmt_curr(amount)} − {fmt_curr(p)} = {fmt_curr(ci)}"
            ],
            "insights": "Compound interest exponentially accelerates growth because interest earns its own interest each period.",
            "raw": ci
        }
        
    # Simple Interest
    si = (p * r * t) / 100
    maturity = p + si
    return {
        "title": "Simple Interest (SI)",
        "summary_value": fmt_curr(si),
        "formula": "SI = (Principal × Rate × Time) ÷ 100",
        "rows": [
            ["Interest Amount (SI)", fmt_curr(si)],
            ["Total Maturity (P + SI)", fmt_curr(maturity)],
            ["Principal (P)", fmt_curr(p)],
            ["Interest Rate", f"{r}% per annum"],
            ["Time Period", f"{t} years"]
        ],
        "steps": [
            f"SI Formula: (P × R × T) ÷ 100",
            f"Calculation: ({p} × {r} × {t}) ÷ 100 = {fmt_curr(si)}",
            f"Total Maturity Amount = Principal + Interest = {fmt_curr(p)} + {fmt_curr(si)} = {fmt_curr(maturity)}"
        ],
        "insights": "In simple interest, the principal remains completely constant throughout the entire tenure.",
        "raw": si
    }
