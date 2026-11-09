"""Symbolic Computer Algebra System (CAS) for Calculator GPT.
Powered by SymPy with human-like step-by-step reasoning, derivation proofs, and verification.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
import sympy as sp
from sympy import (
    Symbol, symbols, diff, integrate, limit, solve, factor, expand,
    simplify, Matrix, latex, Eq, Rational, oo, pi, E, sqrt, sin, cos, tan,
    log, exp, Abs, nsimplify, Function, Derivative, dsolve, classify_ode,
    re as sym_re, im as sym_im, arg as sym_arg, conjugate as sym_conjugate,
    deg as sym_deg, I
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


def safe_parse(expr_str: str) -> sp.Expr:
    """Safely parses mathematical string into a SymPy expression."""
    s = expr_str.strip()
    s = s.replace('^', '**').replace('²', '**2').replace('³', '**3')
    s = s.replace('×', '*').replace('÷', '/').replace('−', '-')
    
    # Common function cleanups
    s = re.sub(r'\bln\b', 'log', s)
    # Support imaginary unit i: e.g. 3i -> 3*I, 4*i -> 4*I, bare i -> I
    s = re.sub(r'(?<=\d)i\b', '*I', s)
    s = re.sub(r'(?<=[+-/*(])\s*i\b', 'I', s)
    s = re.sub(r'\bi(?=[+-/*)])', 'I', s)
    s = re.sub(r'^i$', 'I', s)
    return parse_expr(s, transformations=TRANSFORMS)


def format_sympy_res(expr: Any) -> str:
    """Formats a SymPy expression into clean, comfortable, user-oriented textbook algebra."""
    s = str(expr)
    # 1. Superscript powers
    s = s.replace('**2', '²').replace('**3', '³').replace('**4', '⁴').replace('**5', '⁵').replace('**', '^')
    
    # 2. Implicit multiplication between numbers and variables (e.g. 2*a -> 2a, 12*x -> 12x)
    s = re.sub(r'(\d)\s*\*\s*([a-zA-Z])', r'\g<1>\g<2>', s)
    
    # 3. Implicit multiplication between variables / powers (e.g. a*b -> ab, a²*b -> a²b, x*y -> xy)
    for _ in range(3):
        s = re.sub(r'([a-zA-Z²³⁴⁵^0-9])\s*\*\s*([a-zA-Z])', r'\g<1>\g<2>', s)
        
    # 4. Implicit multiplication around parentheses: (a - b)*(a + b) -> (a - b)(a + b), 2*(x + y) -> 2(x + y)
    s = re.sub(r'\)\s*\*\s*\(', r')(', s)
    s = re.sub(r'([a-zA-Z0-9²³⁴⁵])\s*\*\s*\(', r'\g<1>(', s)
    s = re.sub(r'\)\s*\*\s*([a-zA-Z0-9])', r')\g<1>', s)
    
    # 5. Remaining * between plain numbers becomes standard ×
    s = re.sub(r'(\d)\s*\*\s*(\d)', r'\g<1> × \g<2>', s)
    
    # 6. Any other stray * is cleaned up
    s = s.replace('*', '')
    
    # 7. Comfortable spacing around operators
    s = re.sub(r'\s*\+\s*', ' + ', s)
    s = re.sub(r'(?<=\w)\s*-\s*(?=\w)', ' − ', s)
    s = s.replace('I', 'i')
    return s.strip()

# ==============================================================================
# 1. CALCULUS: DERIVATIVES (Step-by-Step Derivation)
# ==============================================================================
def solve_derivative(query: str) -> Dict[str, Any]:
    """Computes symbolic derivatives with detailed pedagogical steps and rules."""
    q = query.replace('−', '-')
    
    # Extract variable (default to x)
    var_match = re.search(r'w\.?r\.?t\.?\s*([a-zA-Z])|with respect to\s*([a-zA-Z])', q, re.I)
    v_char = var_match.group(1) or var_match.group(2) if var_match else 'x'
    x = Symbol(v_char)
    
    # Check for order of derivative (e.g. 2nd derivative, d2/dx2)
    order = 1
    if re.search(r'\b(?:second|2nd|d2/dx2|d\^2/dx\^2)\b', q, re.I):
        order = 2
        
    # Extract the target expression
    cleaned = re.sub(r'.*?(?:differentiate|derivative of|diff|d/dx|find derivative)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'\s*(?:with respect to|w\.?r\.?t\.?)\s*[a-zA-Z].*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    expr = safe_parse(cleaned)
    derivative = diff(expr, x, order)
    
    # Step-by-step explanation generation
    steps = []
    rule = "General Differentiation Rules"
    
    steps.append(f"Given function: f({v_char}) = {format_sympy_res(expr)}")
    steps.append(f"Target: Compute {'first' if order == 1 else 'second'} derivative with respect to '{v_char}'")
    
    # Identify rule used
    if expr.is_Add:
        rule = "Sum / Difference Rule"
        steps.append(f"Rule: (d/d{v_char})[u + v] = (d/d{v_char})[u] + (d/d{v_char})[v]")
        terms = expr.as_ordered_terms()
        term_diffs = [f"(d/d{v_char})[{format_sympy_res(t)}] = {format_sympy_res(diff(t, x))}" for t in terms]
        steps.append("Differentiate term-by-term: " + ", ".join(term_diffs))
    elif expr.is_Mul:
        rule = "Product Rule / Constant Multiple Rule"
        consts, funcs = expr.as_coeff_Mul()
        if consts != 1:
            steps.append(f"Constant factor: pull out {consts} → {consts} × (d/d{v_char})[{format_sympy_res(funcs)}]")
        else:
            steps.append(f"Rule: (d/d{v_char})[u · v] = u · (dv/d{v_char}) + v · (du/d{v_char})")
    elif expr.is_Pow:
        rule = "Power Rule / Chain Rule"
        base, exp_ = expr.as_base_exp()
        steps.append(f"Rule: (d/d{v_char})[u^n] = n · u^(n-1) · (du/d{v_char})")
    elif expr.func in (sin, cos, tan, exp, log):
        rule = "Trigonometric / Transcendental & Chain Rule"
        arg = expr.args[0]
        steps.append(f"Outer derivative: (d/du)[{expr.func.__name__}(u)]")
        if arg != x:
            steps.append(f"Inner function (Chain Rule): u = {format_sympy_res(arg)} ⟹ du/d{v_char} = {format_sympy_res(diff(arg, x))}")
            
    steps.append(f"Combine and simplify terms: (d/d{v_char})[{format_sympy_res(expr)}] = {format_sympy_res(derivative)}")
    
    return {
        "title": f"Symbolic Derivative ({'d/d' + v_char if order == 1 else 'd²/' + v_char + '²'})",
        "summary_value": format_sympy_res(derivative),
        "formula": f"d/d{v_char}[f({v_char})] = f'({v_char})",
        "rows": [
            [f"Derivative ({'d/d' + v_char if order == 1 else 'd²/' + v_char + '²'})", format_sympy_res(derivative)],
            ["Original Expression", format_sympy_res(expr)],
            ["Variable of Differentiation", v_char],
            ["Primary Rule Applied", rule]
        ],
        "steps": steps,
        "insights": f"The derivative represents the instantaneous rate of change or the slope of the tangent line to f({v_char}) at any point.",
        "raw": None
    }


# ==============================================================================
# 2. CALCULUS: INTEGRALS (Indefinite & Definite)
# ==============================================================================
def solve_integral(query: str) -> Dict[str, Any]:
    """Computes indefinite or definite integrals with pedagogical steps."""
    q = query.replace('−', '-')
    
    # Check if limits of integration are specified (e.g. from 0 to 2)
    limits_match = re.search(r'(?:from|between)\s*([-+]?\d*\.?\d+)\s*(?:to|and)\s*([-+]?\d*\.?\d+)', q, re.I)
    
    cleaned = re.sub(r'.*?(?:integrate|integral of|int)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'(?:from|between)\s*[-+]?\d*\.?\d+\s*(?:to|and)\s*[-+]?\d*\.?\d+.*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'\s*(?:with respect to|w\.?r\.?t\.?|dx)\s*.*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    x = Symbol('x')
    expr = safe_parse(cleaned)
    
    steps = [f"Given integrand: f(x) = {format_sympy_res(expr)}"]
    
    if limits_match:
        a_val, b_val = float(limits_match.group(1)), float(limits_match.group(2))
        antideriv = integrate(expr, x)
        result = integrate(expr, (x, a_val, b_val))
        
        steps.append(f"Step 1: Compute indefinite antiderivative F(x): F(x) = {format_sympy_res(antideriv)}")
        steps.append(f"Step 2: Apply Fundamental Theorem of Calculus: ∫[{a_val} to {b_val}] f(x) dx = F({b_val}) − F({a_val})")
        steps.append(f"Step 3: Evaluate limits: F({b_val}) = {float(antideriv.subs(x, b_val)):.4f}, F({a_val}) = {float(antideriv.subs(x, a_val)):.4f}")
        steps.append(f"Step 4: Net definite value: {format_sympy_res(result)}")
        
        return {
            "title": "Definite Integral",
            "summary_value": format_sympy_res(result),
            "formula": "∫[a to b] f(x) dx = F(b) − F(a)",
            "rows": [
                [f"Definite Value ({a_val} to {b_val})", format_sympy_res(result)],
                ["Antiderivative F(x)", f"{format_sympy_res(antideriv)} + C"],
                ["Lower Limit (a)", str(a_val)],
                ["Upper Limit (b)", str(b_val)]
            ],
            "steps": steps,
            "insights": "The definite integral calculates the exact signed net area bounded by the curve f(x) and the x-axis between x=a and x=b.",
            "raw": float(result) if result.is_number else None
        }
    else:
        antideriv = integrate(expr, x)
        formatted_ans = f"{format_sympy_res(antideriv)} + C"
        
        steps.append(f"Step 1: Apply standard integration rules to each term of f(x) = {format_sympy_res(expr)}")
        steps.append(f"Step 2: Antiderivative obtained: {format_sympy_res(antideriv)}")
        steps.append("Step 3: Append the arbitrary constant of integration (+ C) for the indefinite family of curves.")
        
        return {
            "title": "Indefinite Integral (Antiderivative)",
            "summary_value": formatted_ans,
            "formula": "∫ f(x) dx = F(x) + C",
            "rows": [
                ["Antiderivative ∫f(x)dx", formatted_ans],
                ["Integrand f(x)", format_sympy_res(expr)],
                ["Integration Variable", "x"]
            ],
            "steps": steps,
            "insights": "Integration is the reverse process of differentiation. The + C represents an infinite family of parallel curves sharing the same derivative.",
            "raw": None
        }


# ==============================================================================
# 3. CALCULUS: LIMITS
# ==============================================================================
def solve_limit(query: str) -> Dict[str, Any]:
    """Evaluates limits as x approaches a value."""
    q = query.replace('−', '-')
    
    target_match = re.search(r'(?:as x ->|approaches|towards|to)\s*([-+]?\d*\.?\d+|oo|infinity|0)', q, re.I)
    target_str = target_match.group(1) if target_match else '0'
    target_val = oo if re.search(r'oo|infinity', target_str, re.I) else float(target_str)
    
    cleaned = re.sub(r'.*?(?:limit of|limit|lim)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'(?:as x ->|approaches|towards|to)\s*[-+]?\d*\.?\d+.*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    x = Symbol('x')
    expr = safe_parse(cleaned)
    lim_val = limit(expr, x, target_val)
    
    steps = [
        f"Target expression: f(x) = {format_sympy_res(expr)}",
        f"Evaluation point: x ⟶ {target_str}",
        "Step 1: Test direct substitution to check for indeterminate forms (0/0, ∞/∞).",
        f"Step 2: Analytical limit calculation yields: {format_sympy_res(lim_val)}"
    ]
    
    return {
        "title": "Calculus Limit",
        "summary_value": format_sympy_res(lim_val),
        "formula": f"lim (x ⟶ {target_str}) [f(x)]",
        "rows": [
            ["Limit Value", format_sympy_res(lim_val)],
            ["Function f(x)", format_sympy_res(expr)],
            ["Approaching Point", str(target_str)]
        ],
        "steps": steps,
        "insights": "Limits describe the behavior of a function near a point, rather than its value at that point.",
        "raw": float(lim_val) if lim_val.is_number and lim_val.is_finite else None
    }


# ==============================================================================
# 4. EQUATIONS & SYSTEMS OF EQUATIONS
# ==============================================================================
def solve_equation(query: str) -> Dict[str, Any]:
    """Solves linear, quadratic, polynomial, or simultaneous systems of equations."""
    q = query.replace('−', '-')
    
    # Check for simultaneous linear equations (e.g., 2x + y = 7, x - y = 1)
    if ',' in q or ' and ' in q or re.search(r'=.*?=', q):
        eq_strings = [s.strip() for s in re.split(r'[,;]|\band\b', q) if '=' in s]
        if len(eq_strings) >= 2:
            eqs = []
            vars_found = set()
            for s in eq_strings:
                parts = s.split('=')
                lhs, rhs = safe_parse(parts[0]), safe_parse(parts[1])
                eq = Eq(lhs, rhs)
                eqs.append(eq)
                vars_found.update(eq.free_symbols)
                
            var_list = sorted(list(vars_found), key=lambda sym: sym.name)
            sol = solve(eqs, var_list)
            
            rows = []
            if isinstance(sol, dict):
                for v in var_list:
                    rows.append([f"Variable {v.name}", format_sympy_res(sol.get(v, ''))])
            elif isinstance(sol, list) and len(sol) > 0:
                first = sol[0]
                if isinstance(first, tuple):
                    for idx, v in enumerate(var_list):
                        rows.append([f"Variable {v.name}", format_sympy_res(first[idx])])
                else:
                    rows.append(["Solution", format_sympy_res(first)])
                    
            return {
                "title": f"System of Simultaneous Equations ({len(eqs)} equations)",
                "summary_value": ", ".join([f"{r[0].split()[-1]} = {r[1]}" for r in rows]),
                "formula": "Simultaneous Linear System (Elimination / Matrix Inversion)",
                "rows": rows + [["Equations", "; ".join(eq_strings)]],
                "steps": [
                    f"Equations: {'; '.join(eq_strings)}",
                    f"Variables identified: {[v.name for v in var_list]}",
                    "Method: Linear algebraic elimination and substitution",
                    f"Unique solution vector: {rows}"
                ],
                "insights": "A system of N independent linear equations with N variables has exactly one unique solution intersection.",
                "raw": None
            }

    # Single Equation (Quadratic or Linear)
    eq_str = re.sub(r'.*?(?:solve|roots? of|find x|equation|samikaran)\s*', '', q, flags=re.I)
    eq_str = re.sub(r'[?.,]$', '', eq_str).strip()
    if '=' not in eq_str:
        eq_str += ' = 0'
        
    parts = eq_str.split('=')
    lhs, rhs = safe_parse(parts[0]), safe_parse(parts[1])
    eq_expr = lhs - rhs
    
    # Identify variable
    free = list(eq_expr.free_symbols)
    var = free[0] if free else Symbol('x')
    
    degree = sp.degree(eq_expr, var) if eq_expr.is_polynomial(var) else None
    roots = solve(eq_expr, var)
    
    steps = [
        f"Original equation: {parts[0].strip()} = {parts[1].strip()}",
        f"Standard form: {format_sympy_res(eq_expr)} = 0"
    ]
    
    rows = []
    
    # Quadratic Equation with Discriminant Steps
    if degree == 2:
        poly = eq_expr.as_poly(var)
        coeffs = poly.all_coeffs()
        a, b, c = coeffs[0], coeffs[1], coeffs[2]
        D = b**2 - 4*a*c
        
        steps.append(f"Quadratic coefficients: a = {a}, b = {b}, c = {c}")
        steps.append(f"Discriminant formula: D = b² − 4ac = ({b})² − 4({a})({c}) = {D}")
        
        nature = "Real and Distinct" if D > 0 else ("Real and Equal (Repeated)" if D == 0 else "Complex Conjugates")
        steps.append(f"Discriminant value D = {D} ⟹ Nature of roots: {nature}")
        steps.append(f"Quadratic Formula: {var.name} = (−b ± √D) ÷ 2a")
        
        for idx, r in enumerate(roots, 1):
            rows.append([f"Root {var.name}{idx}", format_sympy_res(r)])
            
        rows.append(["Discriminant (D)", str(D)])
        rows.append(["Nature of Roots", nature])
        rows.append(["Vertex / Extreme Point", f"({-b/(2*a):.3f}, {poly(-b/(2*a)):.3f})"])
        
        return {
            "title": f"Quadratic Equation Solution ({nature})",
            "summary_value": f"{var.name} = " + ", ".join([format_sympy_res(r) for r in roots]),
            "formula": f"{var.name} = (-b ± √(b² - 4ac)) ÷ 2a",
            "rows": rows,
            "steps": steps,
            "insights": f"The discriminant D determines root geometry: D > 0 cuts the axis twice, D = 0 touches at vertex, D < 0 has no real x-intercepts.",
            "raw": float(roots[0]) if len(roots) > 0 and roots[0].is_real else None
        }
    else:
        for idx, r in enumerate(roots, 1):
            rows.append([f"Solution {var.name}{idx if len(roots)>1 else ''}", format_sympy_res(r)])
        rows.append(["Standard Form", f"{format_sympy_res(eq_expr)} = 0"])
        
        steps.append(f"Algebraic isolation of '{var.name}' gives roots: {[format_sympy_res(r) for r in roots]}")
        
        return {
            "title": f"Equation Solution ({'Linear' if degree == 1 else 'Polynomial'})",
            "summary_value": f"{var.name} = " + ", ".join([format_sympy_res(r) for r in roots]),
            "formula": "f(x) = 0",
            "rows": rows,
            "steps": steps,
            "insights": "A polynomial equation of degree N has exactly N complex roots according to the Fundamental Theorem of Algebra.",
            "raw": float(roots[0]) if len(roots) > 0 and roots[0].is_real else None
        }


# ==============================================================================
# 5. ALGEBRA: EXPANSION & FACTORIZATION
# ==============================================================================
def solve_expansion(query: str) -> Dict[str, Any]:
    """Expands polynomials and algebraic products like (a + b)^2, (2x - 3)^3, a+b whole square."""
    q = query.replace('−', '-').replace('–', '-')
    q_work = re.sub(r'^(?:what is (?:the )?|find (?:the )?|tell me (?:the )?|calculate (?:the )?|give (?:me )?|formula (?:of|for|ka) )+', '', q, flags=re.I).strip()
    q_work = re.sub(r'(?:formula|batao|kya hai|kya hoga|likho)[?.]*$', '', q_work, flags=re.I).strip()
    q_work = re.sub(r'plus', '+', q_work, flags=re.I)
    q_work = re.sub(r'minus', '-', q_work, flags=re.I)
    
    m_sq = re.match(r'^(?:expand\s+)?\(?([a-zA-Z0-9\s+\-*\/]+?)\)?\s*(?:ka\s+)?(?:whole\s*square|whole\s*sq|square)\s*$', q_work, flags=re.I)
    m_cu = re.match(r'^(?:expand\s+)?\(?([a-zA-Z0-9\s+\-*\/]+?)\)?\s*(?:ka\s+)?(?:whole\s*cube|cube)\s*$', q_work, flags=re.I)
    
    if m_sq and ('+' in m_sq.group(1) or '-' in m_sq.group(1)):
        inner = m_sq.group(1).strip()
        expr_str = f"({inner})**2"
    elif m_cu and ('+' in m_cu.group(1) or '-' in m_cu.group(1)):
        inner = m_cu.group(1).strip()
        expr_str = f"({inner})**3"
    else:
        cleaned = re.sub(r'.*?(?:expand|expansion of)\s*', '', q_work, flags=re.I)
        cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
        expr_str = cleaned if cleaned else q_work

    expr = safe_parse(expr_str)
    expanded = expand(expr)
    
    steps = [
        f"Original expression: {format_sympy_res(expr)}",
        "Step 1: Apply binomial expansion / distributive multiplication laws.",
        f"Step 2: Collect like terms and order by degree: {format_sympy_res(expanded)}"
    ]
    
    return {
        "title": "Algebraic Polynomial Expansion",
        "summary_value": format_sympy_res(expanded),
        "formula": "(a + b)ⁿ = Σ ⁿCₖ · aⁿ⁻ᵏ · bᵏ",
        "rows": [
            ["Expanded Polynomial", format_sympy_res(expanded)],
            ["Original Expression", format_sympy_res(expr)]
        ],
        "steps": steps,
        "insights": "Expansion converts compact factored expressions into canonical polynomial standard form.",
        "raw": None
    }


def solve_factorization(query: str) -> Dict[str, Any]:
    """Factors polynomials and expressions into irreducible components."""
    q = query.replace('−', '-')
    cleaned = re.sub(r'.*?(?:factor|factorise|factorize|gudankhand)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    expr = safe_parse(cleaned)
    factored = factor(expr)
    
    return {
        "title": "Algebraic Factorization",
        "summary_value": format_sympy_res(factored),
        "formula": "P(x) = c · (x − r₁) · (x − r₂) ...",
        "rows": [
            ["Factored Form", format_sympy_res(factored)],
            ["Original Expression", format_sympy_res(expr)]
        ],
        "steps": [
            f"Given expression: {format_sympy_res(expr)}",
            "Identify common algebraic identities (a² − b², sum of cubes, quadratic trinomials)",
            f"Irreducible factored components: {format_sympy_res(factored)}"
        ],
        "insights": "Factoring breaks down an expression into a product of simpler terms whose roots are immediately readable.",
        "raw": None
    }


# ==============================================================================
# 6. LINEAR ALGEBRA: MATRICES
# ==============================================================================
def solve_matrix(query: str) -> Optional[Dict[str, Any]]:
    """Calculates matrix determinant, inverse, trace, eigenvalues, and eigenvectors."""
    import ast
    q = query.replace('−', '-')
    
    # Try finding matrix literal [[1, 2], [3, 4]]
    m_match = re.search(r'\[\[.*?\]\]', q)
    if not m_match:
        # Try finding semicolon notation [1 2; 3 4] or [1, 2; 3, 4]
        semi_match = re.search(r'\[([0-9\s,;.-]+)\]', q)
        if semi_match and ';' in semi_match.group(1):
            rows_raw = semi_match.group(1).split(';')
            mat_data = []
            for r in rows_raw:
                nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', r)]
                if nums:
                    mat_data.append(nums)
        else:
            return None
    else:
        try:
            mat_data = ast.literal_eval(m_match.group(0))
        except Exception:
            return None

    try:
        M = Matrix(mat_data)
        rows, cols = M.shape
        det_val = None
        inv_str = "Non-invertible (Singular)"
        
        is_eigs_query = bool(re.search(r'\b(?:eigenvalues?|eigenvectors?|characteristic)\b', q, re.I))
        
        steps = [
            f"Input Matrix dimensions: {rows} × {cols}",
            f"Matrix M = {M.tolist()}"
        ]
        
        card_rows = [
            ["Matrix Dimensions", f"{rows} × {cols}"],
            ["Rank of Matrix", str(M.rank())],
            ["Transpose (Mᵀ)", str(M.T.tolist())]
        ]
        
        eig_summary = ""
        trace_val = None
        
        if rows == cols:
            det_val = M.det()
            trace_val = M.trace()
            card_rows.insert(0, ["Determinant (det M)", format_sympy_res(det_val)])
            card_rows.insert(1, ["Trace (Tr M)", format_sympy_res(trace_val)])
            steps.append(f"Determinant det(M) = {format_sympy_res(det_val)}")
            steps.append(f"Trace (Sum of main diagonal) = {format_sympy_res(trace_val)}")
            
            if det_val != 0:
                inv_M = M.inv()
                inv_str = str(inv_M.tolist())
                card_rows.append(["Inverse Matrix M⁻¹", inv_str])
                steps.append(f"Invertible because det(M) ≠ 0. Inverse M⁻¹ = {inv_str}")
            else:
                card_rows.append(["Inverse Matrix M⁻¹", "Singular / Non-invertible (det = 0)"])
                steps.append("Matrix is singular (det = 0); inverse does not exist.")
                
            if rows <= 4:
                # Characteristic Polynomial
                lam = Symbol('λ')
                char_poly = M.charpoly(lam).as_expr()
                card_rows.append(["Characteristic Polynomial", format_sympy_res(char_poly) + " = 0"])
                steps.append(f"Characteristic Equation det(M − λI) = {format_sympy_res(char_poly)} = 0")
                
                # Eigenvalues
                eigs = M.eigenvals()
                eig_list = []
                for k, v in eigs.items():
                    eig_list.append(f"λ = {format_sympy_res(k)} (multiplicity {v})")
                eig_summary = ", ".join(eig_list)
                card_rows.append(["Eigenvalues (λ)", eig_summary])
                steps.append(f"Eigenvalues: {eig_summary}")
                
                # Eigenvectors
                try:
                    vects = M.eigenvects()
                    vect_descs = []
                    for val, mult, bas in vects:
                        bas_strs = [str(b.T.tolist()[0]) for b in bas]
                        vect_descs.append(f"λ = {format_sympy_res(val)}: Basis {bas_strs}")
                    card_rows.append(["Eigenvectors Basis", "; ".join(vect_descs)])
                    steps.append("Eigenvector Eigenspaces: " + "; ".join(vect_descs))
                except Exception:
                    pass

        summary_title = "Eigenvalues & Linear Algebra" if is_eigs_query else f"Matrix Linear Algebra ({rows}×{cols})"
        if is_eigs_query and rows == cols and eig_summary:
            summary_val = eig_summary
        elif det_val is not None:
            summary_val = f"det(M) = {format_sympy_res(det_val)} · Tr = {format_sympy_res(trace_val)}"
        else:
            summary_val = f"{rows}×{cols} Matrix"

        return {
            "title": summary_title,
            "summary_value": summary_val,
            "formula": "det(M),  M⁻¹ = (1/det(M)) · adj(M),  det(M − λI) = 0",
            "rows": card_rows,
            "steps": steps,
            "insights": "Eigenvalues characterize the scalar factors by which eigenvectors are stretched or flipped under the linear transformation M.",
            "raw": float(det_val) if det_val is not None and det_val.is_number else None
        }
    except Exception:
        return None

    try:
        M = Matrix(mat_data)
        rows, cols = M.shape
        det_val = None
        inv_str = "Non-invertible (Singular)"
        
        steps = [
            f"Input Matrix dimensions: {rows} × {cols}",
            f"Matrix entries: {M.tolist()}"
        ]
        
        card_rows = [
            ["Matrix Dimensions", f"{rows} × {cols}"],
            ["Trace", format_sympy_res(M.trace()) if rows == cols else "N/A"]
        ]
        
        if rows == cols:
            det_val = M.det()
            card_rows.insert(0, ["Determinant (det M)", format_sympy_res(det_val)])
            steps.append(f"Calculate Determinant: det(M) = {format_sympy_res(det_val)}")
            
            if det_val != 0:
                inv_M = M.inv()
                inv_str = str(inv_M.tolist())
                card_rows.append(["Inverse Matrix M⁻¹", inv_str])
                steps.append(f"Invertible because det(M) ≠ 0. Inverse M⁻¹ = {inv_str}")
            else:
                card_rows.append(["Inverse Matrix M⁻¹", "Does not exist (det = 0)"])
                steps.append("Matrix is singular (det = 0); inverse does not exist.")
                
            if rows <= 3:
                eigs = M.eigenvals()
                eig_str = ", ".join([f"λ = {format_sympy_res(k)} (mult {v})" for k, v in eigs.items()])
                card_rows.append(["Eigenvalues (λ)", eig_str])
                steps.append(f"Characteristic polynomial roots (Eigenvalues): {eig_str}")

        return {
            "title": f"Matrix Linear Algebra ({rows}×{cols})",
            "summary_value": f"det(M) = {format_sympy_res(det_val)}" if det_val is not None else f"{rows}×{cols} Matrix",
            "formula": "det(M),  M⁻¹ = (1/det(M)) · adj(M)",
            "rows": card_rows,
            "steps": steps,
            "insights": "Determinant measures the scaling factor of the transformation. An invertible matrix represents a bijective linear transformation.",
            "raw": float(det_val) if det_val is not None and det_val.is_number else None
        }
    except Exception:
        return None


# ==============================================================================
# 7. CALCULUS: TAYLOR / MACLAURIN SERIES
# ==============================================================================
def solve_series(query: str) -> Optional[Dict[str, Any]]:
    """Generates Taylor or Maclaurin series expansion of a function."""
    q = query.replace('−', '-').replace('–', '-')
    if not re.search(r'(?:taylor|maclaurin|power series|series of|series expansion)', q, flags=re.I):
        return None
    cleaned = re.sub(r'.*?(?:taylor series|maclaurin series|series expansion of|series of)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'\s*(?:around|about|at)\s*.*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    try:
        x = Symbol('x')
        expr = safe_parse(cleaned)
        ser = expr.series(x, 0, 5)
        
        return {
            "title": "Taylor / Maclaurin Series Expansion",
            "summary_value": format_sympy_res(ser),
            "formula": "f(x) = Σ [f⁽ⁿ⁾(0) ÷ n!] · xⁿ",
            "rows": [
                ["Series Expansion (O(x⁵))", format_sympy_res(ser)],
                ["Original Function f(x)", format_sympy_res(expr)],
                ["Expansion Point", "x = 0 (Maclaurin)"]
            ],
            "steps": [
                f"Given function f(x) = {format_sympy_res(expr)}",
                "Evaluate higher derivatives at x = 0: f(0), f'(0), f''(0), f'''(0)...",
                f"Construct polynomial terms: {format_sympy_res(ser)}"
            ],
            "insights": "Taylor series approximates transcendental non-linear functions as infinite polynomials around a chosen center point.",
            "raw": None
        }
    except Exception:
        return None



# ==============================================================================
# 8. EXTREMA & OPTIMIZATION (Local Minima, Maxima & Inflection Points)
# ==============================================================================
def solve_optimization(query: str) -> Optional[Dict[str, Any]]:
    """Calculates local extrema (minima/maxima), critical points, and inflection points."""
    q = query.replace('−', '-')
    if not re.search(r'\b(?:extrema|maximum|maxima|minimum|minima|inflection|critical points?|optimization)\b', q, re.I):
        return None
    cleaned = re.sub(r'.*?(?:find\s*)?(?:local\s*)?(?:extrema|maximum and minimum|maxima and minima|maximum|maxima|minimum|minima|critical points|inflection points|optimization)\s*(?:of|for)?\s*', '', q, flags=re.I)
    cleaned = re.sub(r'^[fF]\s*\([a-zA-Z]\)\s*=\s*', '', cleaned)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    try:
        expr = safe_parse(cleaned)
        free = list(expr.free_symbols)
        x = free[0] if free else Symbol('x')
        
        # Derivatives
        df = diff(expr, x)
        d2f = diff(expr, x, 2)
        
        # Critical points: f'(x) = 0
        crit_raw = solve(df, x)
        crit_points = [c for c in crit_raw if c.is_real or c.is_number]
        
        steps = [
            f"Given function: f({x.name}) = {format_sympy_res(expr)}",
            f"Step 1: Compute first derivative: f'({x.name}) = {format_sympy_res(df)}",
            f"Step 2: Solve f'({x.name}) = 0 for critical points: {format_sympy_res(df)} = 0 ⟹ {x.name} = {[format_sympy_res(c) for c in crit_points]}",
            f"Step 3: Compute second derivative: f''({x.name}) = {format_sympy_res(d2f)}"
        ]
        
        card_rows = [
            ["Original Function f(x)", format_sympy_res(expr)],
            ["First Derivative f'(x)", format_sympy_res(df)],
            ["Second Derivative f''(x)", format_sympy_res(d2f)]
        ]
        
        extrema_summary = []
        minima = []
        maxima = []
        saddles = []
        
        for c in crit_points:
            f_val = expr.subs(x, c)
            sec_val = d2f.subs(x, c)
            
            # Classification
            if sec_val > 0:
                minima.append((c, f_val))
                extrema_summary.append(f"Local Min at ({format_sympy_res(c)}, {format_sympy_res(f_val)})")
                steps.append(f"At {x.name} = {format_sympy_res(c)}: f''({format_sympy_res(c)}) = {format_sympy_res(sec_val)} > 0 ⟹ Local Minimum with value {format_sympy_res(f_val)}")
                card_rows.append([f"Local Minimum at {x.name}={format_sympy_res(c)}", f"({format_sympy_res(c)}, {format_sympy_res(f_val)})"])
            elif sec_val < 0:
                maxima.append((c, f_val))
                extrema_summary.append(f"Local Max at ({format_sympy_res(c)}, {format_sympy_res(f_val)})")
                steps.append(f"At {x.name} = {format_sympy_res(c)}: f''({format_sympy_res(c)}) = {format_sympy_res(sec_val)} < 0 ⟹ Local Maximum with value {format_sympy_res(f_val)}")
                card_rows.append([f"Local Maximum at {x.name}={format_sympy_res(c)}", f"({format_sympy_res(c)}, {format_sympy_res(f_val)})"])
            else:
                saddles.append((c, f_val))
                extrema_summary.append(f"Stationary/Inconclusive at {x.name}={format_sympy_res(c)}")
                steps.append(f"At {x.name} = {format_sympy_res(c)}: f''({format_sympy_res(c)}) = 0 ⟹ Second derivative test inconclusive (Possible saddle or higher inflection)")
                card_rows.append([f"Stationary Point at {x.name}={format_sympy_res(c)}", f"({format_sympy_res(c)}, {format_sympy_res(f_val)})"])

        # Inflection points: f''(x) = 0
        infl_raw = solve(d2f, x)
        infl_points = [p for p in infl_raw if p.is_real or p.is_number]
        if infl_points:
            infl_str = ", ".join([f"({format_sympy_res(p)}, {format_sympy_res(expr.subs(x, p))})" for p in infl_points])
            card_rows.append(["Inflection Points (f''=0)", infl_str])
            steps.append(f"Step 4: Solve f''({x.name}) = 0 for inflection points: {infl_str}")
            
        summary_val = " · ".join(extrema_summary) if extrema_summary else f"No real local extrema; Inflection points: {len(infl_points)}"
        
        return {
            "title": "Extrema & Optimization (Minima, Maxima & Inflection)",
            "summary_value": summary_val,
            "formula": "Critical: f'(x) = 0;  Min: f''(x) > 0;  Max: f''(x) < 0;  Inflection: f''(x) = 0",
            "rows": card_rows,
            "steps": steps,
            "insights": "The Second Derivative Test classifies critical points: positive curvature indicates concave up (minimum), negative curvature indicates concave down (maximum).",
            "raw": float(maxima[0][1]) if maxima and maxima[0][1].is_number else (float(minima[0][1]) if minima and minima[0][1].is_number else None)
        }
    except Exception:
        return None


# ==============================================================================
# 9. COMPLEX NUMBERS (Modulus, Argument, Conjugate & Polar Form)
# ==============================================================================
def solve_complex(query: str) -> Optional[Dict[str, Any]]:
    """Analyzes complex numbers: modulus, argument, conjugate, polar and exponential forms."""
    q = query.replace('−', '-')
    is_kw = bool(re.search(r'\b(?:modulus and argument|polar form|conjugate of|complex number|modulus of|argument of|arg of)\b', q, re.I))
    if not is_kw and not re.search(r'\b\d*\s*[*+-]?\s*\d*\s*[iI]\b', q):
        return None
    cleaned = re.sub(r'.*?(?:modulus and argument of|polar form of|conjugate of|complex number|modulus of|argument of|arg of)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    try:
        expr = safe_parse(cleaned)
        z = simplify(expr)
        
        # Real and imaginary components
        a = sym_re(z)
        b = sym_im(z)
        
        # Modulus and argument
        mod_val = Abs(z)
        arg_val = sym_arg(z)
        conj_val = sym_conjugate(z)
        
        try:
            deg_val = float(arg_val.evalf() * 180 / pi.evalf())
        except Exception:
            deg_val = 0.0
            
        try:
            mod_float = float(mod_val.evalf())
        except Exception:
            mod_float = None
            
        polar_trig = f"{format_sympy_res(mod_val)} · (cos({format_sympy_res(arg_val)}) + i · sin({format_sympy_res(arg_val)}))"
        polar_exp = f"{format_sympy_res(mod_val)} · e^(i · {format_sympy_res(arg_val)})"
        
        steps = [
            f"Given complex expression: z = {format_sympy_res(expr)}",
            f"Step 1: Simplify into standard rectangular form (a + bi): z = {format_sympy_res(z)}",
            f"Step 2: Real part Re(z) = {format_sympy_res(a)}, Imaginary part Im(z) = {format_sympy_res(b)}",
            f"Step 3: Modulus |z| = √(a² + b²) = √(({format_sympy_res(a)})² + ({format_sympy_res(b)})²) = {format_sympy_res(mod_val)}" + (f" ≈ {mod_float:.4f}" if mod_float is not None else ""),
            f"Step 4: Argument θ = atan2(b, a) = {format_sympy_res(arg_val)} radians ({deg_val:.2f}°)",
            f"Step 5: Complex Conjugate z̄ = a − bi = {format_sympy_res(conj_val)}",
            f"Step 6: Polar Exponential Form: z = r · e^(iθ) = {polar_exp}"
        ]
        
        return {
            "title": "Complex Number Analysis (Modulus, Argument & Polar Form)",
            "summary_value": f"|z| = {format_sympy_res(mod_val)} · Arg(z) = {format_sympy_res(arg_val)} ({deg_val:.1f}°) · z̄ = {format_sympy_res(conj_val)}",
            "formula": "z = a + bi,  |z| = √(a² + b²),  Arg(z) = atan2(b, a),  z = r·e^(iθ)",
            "rows": [
                ["Rectangular Form (a + bi)", format_sympy_res(z)],
                ["Modulus |z| (Distance from origin)", f"{format_sympy_res(mod_val)}" + (f" (≈ {mod_float:.4f})" if mod_float else "")],
                ["Argument θ (Angle in radians)", f"{format_sympy_res(arg_val)} rad ({deg_val:.2f}°)"],
                ["Complex Conjugate (z̄)", format_sympy_res(conj_val)],
                ["Real Part Re(z)", format_sympy_res(a)],
                ["Imaginary Part Im(z)", format_sympy_res(b)],
                ["Polar Exponential Form", polar_exp],
                ["Trigonometric Form", polar_trig]
            ],
            "steps": steps,
            "insights": "In the Argand complex plane, the modulus is Euclidean distance to the origin and the argument is the counter-clockwise angle from the positive real axis.",
            "raw": mod_float
        }
    except Exception:
        return None


# ==============================================================================
# 10. DIFFERENTIAL EQUATIONS (1st Order ODEs via SymPy dsolve)
# ==============================================================================
def solve_ode(query: str) -> Optional[Dict[str, Any]]:
    """Solves 1st order ordinary differential equations (ODEs) with SymPy dsolve."""
    q = query.replace('−', '-')
    if not re.search(r'\b(?:differential equation|ode|dsolve|dy/dx)\b', q, re.I) and not re.search(r"\by'\b", q):
        return None
    
    # Extract initial conditions e.g. "with y(0) = 1" or "y(0) = 2"
    ics = {}
    ic_m = re.search(r'y\s*\(\s*([-+]?\d*\.?\d+)\s*\)\s*=\s*([-+]?\d*\.?\d+)', q)
    if ic_m:
        x0_val = float(ic_m.group(1))
        y0_val = float(ic_m.group(2))
        x0_sym = int(x0_val) if x0_val.is_integer() else x0_val
        y0_sym = int(y0_val) if y0_val.is_integer() else y0_val
    else:
        x0_sym, y0_sym = None, None
        
    cleaned = re.sub(r'.*?(?:solve\s*)?(?:differential equation|ode)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'\s*(?:with|where|given)\s*y\s*\(\s*[-+]?\d*\.?\d+\s*\)\s*=\s*[-+]?\d*\.?\d+.*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    try:
        x = Symbol('x')
        y = Function('y')
        
        # Prepare ODE string
        # Replace dy/dx or y' with Derivative(y(x), x)
        ode_s = cleaned
        ode_s = re.sub(r'\bdy/dx\b', 'Derivative(y(x), x)', ode_s)
        ode_s = re.sub(r"\by'\b", 'Derivative(y(x), x)', ode_s)
        # Replace bare y with y(x) when not y(
        ode_s = re.sub(r'\by\b(?!\s*\()', 'y(x)', ode_s)
        
        if '=' in ode_s:
            parts = ode_s.split('=')
            lhs_str, rhs_str = parts[0].strip(), parts[1].strip()
        else:
            lhs_str, rhs_str = ode_s.strip(), '0'
            
        local_dict = {'x': x, 'y': y, 'Derivative': Derivative, 'exp': exp, 'sin': sin, 'cos': cos, 'tan': tan, 'log': log}
        lhs_expr = parse_expr(lhs_str.replace('^', '**').replace('×', '*').replace('÷', '/'), local_dict=local_dict, transformations=TRANSFORMS)
        rhs_expr = parse_expr(rhs_str.replace('^', '**').replace('×', '*').replace('÷', '/'), local_dict=local_dict, transformations=TRANSFORMS)
        
        eq = Eq(lhs_expr, rhs_expr)
        
        ics_dict = {y(x0_sym): y0_sym} if x0_sym is not None else None
        sol = dsolve(eq, y(x), ics=ics_dict)
        
        ode_classes = classify_ode(eq, y(x))
        primary_class = ode_classes[0] if ode_classes else "1st Order ODE"
        
        sol_rhs = sol.rhs
        
        steps = [
            f"Differential Equation: {format_sympy_res(lhs_expr)} = {format_sympy_res(rhs_expr)}",
            f"Step 1: Classification: Identified as '{primary_class}' ordinary differential equation.",
            f"Step 2: Apply standard integration method for {primary_class}."
        ]
        
        if 'linear' in primary_class:
            steps.append("Step 3: Put into standard linear form: dy/dx + P(x)·y = Q(x), determine integrating factor I(x) = exp(∫ P(x) dx).")
            steps.append("Step 4: Multiply by integrating factor and integrate both sides.")
        elif 'separable' in primary_class:
            steps.append("Step 3: Separate variables: g(y) dy = f(x) dx and integrate both sides.")
            
        steps.append(f"Step 5: General Solution: y(x) = {format_sympy_res(sol_rhs)}")
        
        if ics_dict:
            steps.append(f"Step 6: Apply initial condition y({x0_sym}) = {y0_sym} to uniquely determine constant C₁.")
            steps.append(f"Step 7: Particular Solution: y(x) = {format_sympy_res(sol_rhs)}")
            
        return {
            "title": f"Differential Equation Solution ({'Particular' if ics_dict else 'General'})",
            "summary_value": f"y(x) = {format_sympy_res(sol_rhs)}",
            "formula": "Standard 1st Order ODE: y' + P(x)y = Q(x) ⟹ y(x) = [∫ Q(x)·I(x) dx + C] ÷ I(x)",
            "rows": [
                ["Solution y(x)", f"y(x) = {format_sympy_res(sol_rhs)}"],
                ["Original ODE", cleaned],
                ["ODE Classification", primary_class],
                ["Initial Condition", f"y({x0_sym}) = {y0_sym}" if ics_dict else "None (General Solution with C₁)"]
            ],
            "steps": steps,
            "insights": "First-order differential equations relate an unknown function to its rate of change; initial conditions pin down the specific integral curve.",
            "raw": None
        }
    except Exception:
        return None
