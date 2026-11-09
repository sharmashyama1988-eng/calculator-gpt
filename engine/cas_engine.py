"""Symbolic Computer Algebra System (CAS) for Calculator GPT.
Powered by SymPy with human-like step-by-step reasoning, derivation proofs, and verification.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
import sympy as sp
from sympy import (
    Symbol, symbols, diff, integrate, limit, solve, factor, expand,
    simplify, Matrix, latex, Eq, Rational, oo, pi, E, sqrt, sin, cos, tan,
    log, exp, Abs, nsimplify
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
    return parse_expr(s, transformations=TRANSFORMS)


def format_sympy_res(expr: Any) -> str:
    """Formats a SymPy expression into clean readable mathematical text."""
    s = str(expr)
    s = s.replace('**2', '²').replace('**3', '³').replace('**', '^')
    s = s.replace('*', ' · ')
    return s


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
    """Expands polynomials and algebraic products like (a + b)^2, (2x - 3)^3."""
    q = query.replace('−', '-')
    cleaned = re.sub(r'.*?(?:expand|expansion of|whole square|whole cube)\s*', '', q, flags=re.I)
    cleaned = re.sub(r'[?.,]$', '', cleaned).strip()
    
    expr = safe_parse(cleaned)
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
    """Calculates matrix determinant, inverse, trace, and eigenvalues."""
    import ast
    q = query.replace('−', '-')
    
    # Try finding matrix literal [[1, 2], [3, 4]]
    m_match = re.search(r'\[\[.*?\]\]', q)
    if not m_match:
        # Try finding semicolon notation [1 2; 3 4]
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
    q = query.replace('−', '-')
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

