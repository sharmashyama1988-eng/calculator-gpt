"""Master Mathematical & Aptitude Reasoning Orchestrator for Calculator GPT.
Routes queries to specialized CAS, Aptitude, Statistics, and Discrete Math solvers.
Generates humanized AI-like step-by-step proofs and derivations.
"""

import re
import json
from typing import Dict, Any, List, Optional
import sympy as sp

from .nlp_parser import normalize_query, detect_intent, extract_numbers
from .cas_engine import (
    solve_derivative, solve_integral, solve_limit,
    solve_equation, solve_expansion, solve_factorization,
    solve_matrix, solve_series, safe_parse, format_sympy_res
)
from .aptitude_engine import (
    solve_train_problem, solve_time_work, solve_profit_loss, solve_interest, fmt, fmt_curr
)
from .stats_engine import solve_statistics
from .universal_solver import (
    solve_universal_motion, solve_universal_age, solve_universal_chain_work
)


def solve_number_theory(query: str) -> Optional[Dict[str, Any]]:
    """Handles LCM, HCF/GCD, Prime checks, nCr, nPr, and Factorials."""
    q = normalize_query(query).lower()
    nums = [int(n) for n in extract_numbers(q) if n.is_integer()]
    
    # LCM
    if re.search(r'\b(?:lcm|lowest common multiple|laghuttam)\b', q) and len(nums) >= 2:
        import math
        a, b = nums[0], nums[1]
        gcd_val = math.gcd(a, b)
        lcm_val = abs(a * b) // gcd_val
        return {
            "title": f"Lowest Common Multiple (LCM of {a} & {b})",
            "summary_value": str(lcm_val),
            "formula": "LCM(a, b) = (|a × b|) ÷ GCD(a, b)",
            "rows": [
                ["LCM Result", str(lcm_val)],
                ["GCD / HCF", str(gcd_val)],
                ["Product (a × b)", str(a * b)]
            ],
            "steps": [
                f"Numbers: a = {a}, b = {b}",
                f"Step 1: Compute Greatest Common Divisor: GCD({a}, {b}) = {gcd_val}",
                f"Step 2: Apply Fundamental Relation: LCM × HCF = a × b",
                f"Step 3: Calculate: ({a} × {b}) ÷ {gcd_val} = {a * b} ÷ {gcd_val} = {lcm_val}"
            ],
            "insights": "The product of the HCF and LCM of any two numbers is always exactly equal to the product of the numbers.",
            "raw": lcm_val
        }

    # HCF / GCD
    if re.search(r'\b(?:hcf|gcd|greatest common divisor|mahattam)\b', q) and len(nums) >= 2:
        import math
        a, b = nums[0], nums[1]
        gcd_val = math.gcd(a, b)
        return {
            "title": f"Highest Common Factor (HCF / GCD of {a} & {b})",
            "summary_value": str(gcd_val),
            "formula": "Euclidean Division Algorithm: GCD(a, b) = GCD(b, a mod b)",
            "rows": [
                ["HCF / GCD", str(gcd_val)],
                ["Tested Numbers", f"{a}, {b}"]
            ],
            "steps": [
                f"Find greatest common divisor between {a} and {b}",
                f"Euclidean algorithm step: remainder-based division yields GCD = {gcd_val}"
            ],
            "insights": "HCF is the largest integer that divides both numbers without leaving any remainder.",
            "raw": gcd_val
        }

    # Primality Test & Factorization
    if re.search(r'\b(?:prime|avibhajiya)\b', q) and len(nums) >= 1:
        n = nums[0]
        if n < 2:
            is_prime = False
        else:
            is_prime = sp.isprime(n)
            
        factors = sp.factorint(n) if n > 1 else {}
        fact_str = " · ".join([f"{base}^{exp}" if exp > 1 else str(base) for base, exp in factors.items()])
        
        return {
            "title": f"Primality Test & Factorization for {n}",
            "summary_value": "PRIME NUMBER" if is_prime else "COMPOSITE (Not Prime)",
            "formula": "Fundamental Theorem of Arithmetic",
            "rows": [
                ["Classification", "Prime Number" if is_prime else "Composite Number"],
                ["Prime Factorization", fact_str if fact_str else "N/A"],
                ["Divisors Count", str(sp.divisor_count(n)) if n > 0 else "0"]
            ],
            "steps": [
                f"Testing number N = {n}",
                f"Trial division up to √{n} ≈ {int(n**0.5)}",
                f"Result: {n} has " + ("no factors other than 1 and itself." if is_prime else f"prime factorization: {fact_str}")
            ],
            "insights": "A prime number is an integer greater than 1 whose only divisors are 1 and itself.",
            "raw": n if is_prime else None
        }

    # Combinations (nCr)
    if re.search(r'\b(?:combinations?|ncr)\b', q) or re.search(r'\d+c\d+', q):
        if len(nums) >= 2:
            import math
            n_val, r_val = max(nums[0], nums[1]), min(nums[0], nums[1])
            if n_val <= 200:
                comb = math.comb(n_val, r_val)
                return {
                    "title": f"Combinations ({n_val}C{r_val})",
                    "summary_value": f"{comb:,}",
                    "formula": "ⁿCᵣ = n! ÷ (r! × (n − r)!)",
                    "rows": [
                        ["Total Combinations", f"{comb:,}"],
                        ["Formula", f"{n_val}! ÷ ({r_val}! × {n_val - r_val}!)"],
                        ["Total Items (n)", str(n_val)],
                        ["Selected Items (r)", str(r_val)]
                    ],
                    "steps": [
                        f"Target: Choose {r_val} items out of {n_val} without regard to order.",
                        f"Formula: {n_val}! ÷ ({r_val}! × ({n_val}−{r_val})!)",
                        f"Result: {comb:,} possible distinct selections."
                    ],
                    "insights": "Combinations represent selection where arrangement order does NOT matter.",
                    "raw": comb
                }

    # Permutations (nPr)
    if re.search(r'\b(?:permutations?|npr)\b', q) or re.search(r'\d+p\d+', q):
        if len(nums) >= 2:
            import math
            n_val, r_val = max(nums[0], nums[1]), min(nums[0], nums[1])
            if n_val <= 200:
                perm = math.perm(n_val, r_val)
                return {
                    "title": f"Permutations ({n_val}P{r_val})",
                    "summary_value": f"{perm:,}",
                    "formula": "ⁿPᵣ = n! ÷ (n − r)!",
                    "rows": [
                        ["Total Permutations", f"{perm:,}"],
                        ["Formula", f"{n_val}! ÷ ({n_val} − {r_val})!"],
                        ["Total Items (n)", str(n_val)],
                        ["Arranged Items (r)", str(r_val)]
                    ],
                    "steps": [
                        f"Target: Order and arrange {r_val} items out of {n_val}.",
                        f"Formula: {n_val}! ÷ ({n_val}−{r_val})!",
                        f"Result: {perm:,} distinct ordered permutations."
                    ],
                    "insights": "Permutations represent ordered sequences where arrangement position DOES matter.",
                    "raw": perm
                }

    return None


def solve_geometry(query: str) -> Optional[Dict[str, Any]]:
    """Calculates geometric properties (Circles, Cylinders, Triangles, Cones, Spheres)."""
    import math
    q = normalize_query(query).lower()
    nums = extract_numbers(q)
    
    # Circle
    if 'circle' in q and len(nums) >= 1:
        r = nums[0]
        area = math.pi * r * r
        circ = 2 * math.pi * r
        return {
            "title": f"Circle Geometry (Radius r = {r})",
            "summary_value": f"Area = {area:.2f} · Circumference = {circ:.2f}",
            "formula": "Area = πr²,  Circumference = 2πr",
            "rows": [
                ["Area (πr²)", f"{area:.3f}"],
                ["Circumference (2πr)", f"{circ:.3f}"],
                ["Radius (r)", str(r)],
                ["Diameter (2r)", str(2 * r)]
            ],
            "steps": [
                f"Radius given: r = {r}",
                f"Area = π × {r}² = {math.pi:.4f} × {r*r} = {area:.4f}",
                f"Circumference = 2 × π × {r} = {circ:.4f}"
            ],
            "insights": "The ratio of a circle's circumference to its diameter is the universal constant π ≈ 3.14159.",
            "raw": area
        }

    # Pythagoras / Hypotenuse
    if re.search(r'hypotenuse|pythagoras|right triangle', q) and len(nums) >= 2:
        a, b = nums[0], nums[1]
        c = math.hypot(a, b)
        return {
            "title": "Right Triangle Hypotenuse (Pythagorean Theorem)",
            "summary_value": f"Hypotenuse c = {c:.2f}",
            "formula": "c = √(a² + b²)",
            "rows": [
                ["Hypotenuse (c)", f"{c:.3f}"],
                ["Base (a)", str(a)],
                ["Perpendicular (b)", str(b)],
                ["Area of Triangle", f"{(a * b) / 2:.2f}"]
            ],
            "steps": [
                f"Given legs: a = {a}, b = {b}",
                f"Apply Pythagoras: c² = a² + b² = {a}² + {b}² = {a*a} + {b*b} = {a*a + b*b}",
                f"Take square root: c = √({a*a + b*b}) = {c:.4f}"
            ],
            "insights": "In any Euclidean right-angled triangle, the area of the square on the hypotenuse equals the sum of areas of squares on the other two legs.",
            "raw": c
        }

    return None


def solve_query(raw_query: str) -> Dict[str, Any]:
    """Master single query solver using intent routing, SymPy CAS, and aptitude engines."""
    if not raw_query or not raw_query.strip():
        return {
            "title": "Empty Query",
            "summary_value": "Please enter a mathematical question or equation.",
            "formula": "",
            "rows": [],
            "steps": [],
            "insights": "",
            "raw": None
        }

    q = raw_query.strip()
    intent = detect_intent(q)
    
    # Intent-based routing with safe fallbacks
    try:
        if intent == "CALCULUS_DERIVATIVE":
            return solve_derivative(q)
        elif intent == "CALCULUS_INTEGRAL":
            return solve_integral(q)
        elif intent == "CALCULUS_LIMIT":
            return solve_limit(q)
        elif intent == "EQUATION_SOLVER":
            return solve_equation(q)
        elif intent == "ALGEBRA_EXPAND":
            return solve_expansion(q)
        elif intent == "ALGEBRA_FACTOR":
            return solve_factorization(q)
        elif intent == "APTITUDE_TRAIN":
            res = solve_universal_motion(q) or solve_train_problem(q)
            if res:
                return res
        elif intent == "APTITUDE_TIME_WORK":
            res = solve_universal_chain_work(q) or solve_time_work(q)
            if res:
                return res
        elif intent == "APTITUDE_AGE":
            res = solve_universal_age(q)
            if res:
                return res
        elif intent == "APTITUDE_PROFIT_LOSS":
            res = solve_profit_loss(q)
            if res:
                return res
        elif intent in ("APTITUDE_EMI", "APTITUDE_CI", "APTITUDE_SI"):
            res = solve_interest(q)
            if res:
                return res
        elif intent == "STATISTICS":
            res = solve_statistics(q)
            if res:
                return res
        elif intent.startswith("NUMBER_THEORY"):
            res = solve_number_theory(q)
            if res:
                return res
        elif intent == "MATRIX_OPERATIONS":
            res = solve_matrix(q)
            if res:
                return res
        elif intent == "GEOMETRY":
            res = solve_geometry(q)
            if res:
                return res
    except Exception as e:
        # Fall through to general solver
        pass

    # Universal physical & algebraic solver sweep (Handles ANY unseen dynamic problem)
    for solver in [
        solve_universal_motion, solve_universal_age, solve_universal_chain_work,
        solve_matrix, solve_series, solve_train_problem, solve_time_work, solve_profit_loss,
        solve_interest, solve_statistics, solve_number_theory, solve_geometry
    ]:
        try:
            r = solver(q)
            if r:
                return r
        except Exception:
            continue

    # SymPy general expression evaluator fallback
    try:
        expr = safe_parse(normalize_query(q))
        simplified = sp.simplify(expr)
        num_val = None
        try:
            if simplified.is_number:
                num_val = float(simplified.evalf())
        except Exception:
            pass

        return {
            "title": "Mathematical Expression Evaluation",
            "summary_value": format_sympy_res(simplified),
            "formula": "Standard Mathematical Simplification",
            "rows": [
                ["Calculated Result", format_sympy_res(simplified)],
                ["Original Expression", raw_query],
                ["Numerical Value", f"{num_val:.6f}".rstrip('0').rstrip('.') if num_val is not None else "Exact Symbolic"]
            ],
            "steps": [
                f"Parsed expression: {format_sympy_res(expr)}",
                f"Apply algebraic identity simplification & arithmetic operations",
                f"Final simplified evaluation: {format_sympy_res(simplified)}"
            ],
            "insights": "Evaluated using exact arbitrary-precision symbolic mathematics via SymPy.",
            "raw": num_val
        }
    except Exception:
        pass

    return {
        "title": "General Query",
        "summary_value": "Could not parse query",
        "formula": "",
        "rows": [["Input", raw_query]],
        "steps": ["Try phrasing as an equation (e.g., 'solve 2x^2 + 5x - 3 = 0'), stats ('mean of 10, 15, 20'), or train problem."],
        "insights": "Calculator GPT supports algebra, calculus, train speed, time & work, statistics, and financial math.",
        "raw": None
    }


def process_all_queries(raw_input: str) -> List[Dict[str, Any]]:
    """Splits multiple quoted or semicolon-separated questions and solves each."""
    if not raw_input:
        return []
        
    # Check for quoted items: "Q1" "Q2"
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', raw_input)
    queries = []
    if quoted:
        for m in quoted:
            val = m[0] or m[1]
            if val.strip():
                queries.append(val.strip())
    else:
        # Check for multiple questions separated by semicolons
        if ';' in raw_input:
            queries = [s.strip() for s in raw_input.split(';') if s.strip()]
        else:
            queries = [raw_input.strip()]
            
    results = []
    for q in queries:
        ans = solve_query(q)
        ans["query"] = q
        results.append(ans)
    return results
