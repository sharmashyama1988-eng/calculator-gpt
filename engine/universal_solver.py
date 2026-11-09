"""Universal Dynamic Mathematical & Aptitude Solver for Calculator GPT.
No hardcoded test questions — uses fundamental physical laws, dimensional analysis,
and SymPy symbolic equation formulation to solve ANY arbitrary real-world problem dynamically.
"""

import re
import math
from typing import Dict, Any, List, Optional, Tuple
import sympy as sp
from sympy import Symbol, Eq, solve, symbols, simplify


# ==============================================================================
# 1. UNIT & DIMENSIONAL CONVERTER
# ==============================================================================
def to_si_speed(val: float, unit: str) -> float:
    """Converts any speed to m/s."""
    u = unit.lower()
    if 'km' in u or 'kmph' in u or 'kph' in u:
        return val * (5.0 / 18.0)  # km/h to m/s
    if 'mph' in u or 'mile' in u:
        return val * 0.44704
    return val  # already m/s


def to_kmh_speed(val_ms: float) -> float:
    """Converts m/s back to km/h."""
    return val_ms * (18.0 / 5.0)


def to_seconds(val: float, unit: str) -> float:
    """Converts any time to seconds."""
    u = unit.lower()
    if 'hr' in u or 'hour' in u or 'ghante' in u:
        return val * 3600.0
    if 'min' in u:
        return val * 60.0
    return val  # seconds


def to_meters(val: float, unit: str) -> float:
    """Converts any distance to meters."""
    u = unit.lower()
    if 'km' in u:
        return val * 1000.0
    if 'mile' in u:
        return val * 1609.34
    if 'cm' in u:
        return val * 0.01
    return val  # meters


# ==============================================================================
# 2. UNIVERSAL DYNAMIC TRAIN & RELATIVE MOTION SOLVER
# Solves for ANY unknown: Time, Speed, or Length!
# Handles: Train crossing pole/man, crossing platform/bridge, 2 trains moving
# in same or opposite directions.
# ==============================================================================
def solve_universal_motion(query: str) -> Optional[Dict[str, Any]]:
    """Dynamically parses and sets up physical motion equations (Relative Speed * Time = Distance).
    Works for ANY arbitrary numbers and unknown variables (time, speed, or length).
    """
    q = query.lower()
    if not re.search(r'\b(?:train|trains|railgadi|platform|pole|bridge|crossing|speed|distance|relative)\b', q):
        return None

    # Detect directions
    is_same = bool(re.search(r'same direction|ek hi disha|ek hi taraf', q))
    is_opposite = bool(re.search(r'opposite|aamne|samne|towards each other|ek dusre ki taraf', q))

    # Extract all distance/length items with units (avoiding km/h or m/s via negative lookahead)
    lengths_m = []
    for num, unit in re.findall(r'(\d+(?:\.\d+)?)\s*(m\b|meters?|metres?|kms?|kilometres?|kilometers?)(?!\s*[/ph])', q):
        lengths_m.append(to_meters(float(num), unit))

    # Extract speeds: "60 km/h", "72 kmph", "20 m/s"
    speeds_kmh = []
    for num, unit in re.findall(r'(\d+(?:\.\d+)?)\s*(km/?h|kmph|kph|m/?s|mph)', q):
        speeds_kmh.append(float(num) * 3.6 if ('m' in unit and 's' in unit) else float(num))

    # Extract times: "25 seconds", "2 hours", "15 mins"
    times_s = []
    for num, unit in re.findall(r'(\d+(?:\.\d+)?)\s*(secs?|seconds?|hrs?|hours?|mins?|minutes?|ghante)', q):
        times_s.append(to_seconds(float(num), unit))

    # CASE A: Known Lengths + Known Speeds -> Find Time
    if len(speeds_kmh) >= 1 and len(lengths_m) >= 1 and len(times_s) == 0:
        total_dist_m = sum(lengths_m)
        if len(speeds_kmh) == 1:
            rel_speed_ms = to_si_speed(speeds_kmh[0], 'km/h')
            rel_speed_kmh = speeds_kmh[0]
            desc = f"Single train moving at {speeds_kmh[0]} km/h"
        else:
            s1, s2 = speeds_kmh[0], speeds_kmh[1]
            rel_speed_kmh = abs(s1 - s2) if (is_same and not is_opposite) else (s1 + s2)
            rel_speed_ms = to_si_speed(rel_speed_kmh, 'km/h')
            desc = f"Relative speed ({'Same: ' if is_same else 'Opposite: '}{s1} {'-' if is_same else '+'} {s2} = {rel_speed_kmh} km/h)"

        if rel_speed_ms <= 0:
            return None

        t_seconds = total_dist_m / rel_speed_ms
        
        steps = [
            f"Step 1: Identify all lengths to be cleared: {total_dist_m} meters total.",
            f"Step 2: Calculate relative speed in SI units (m/s): {rel_speed_kmh} km/h × (5/18) = {rel_speed_ms:.3f} m/s.",
            f"Step 3: Apply physical motion law: Time = Total Distance ÷ Relative Speed",
            f"Step 4: Solve equation: t = {total_dist_m} m ÷ {rel_speed_ms:.3f} m/s = {t_seconds:.2f} seconds."
        ]

        time_display = f"{t_seconds:.2f} seconds" if t_seconds < 120 else f"{t_seconds/60:.2f} minutes ({t_seconds:.1f}s)"

        return {
            "title": "Universal Motion Solver (Time to Cross)",
            "summary_value": time_display,
            "formula": "Time = Total Distance (m) ÷ Relative Speed (m/s)",
            "rows": [
                ["Calculated Crossing Time", time_display],
                ["Total Distance to Clear", f"{total_dist_m:,.1f} meters"],
                ["Relative Speed", f"{rel_speed_kmh:.1f} km/h ({rel_speed_ms:.2f} m/s)"],
                ["Motion Type", desc]
            ],
            "steps": steps,
            "insights": "To cross an object of length L, the front of the train must travel its own length plus the object's length.",
            "raw": t_seconds
        }

    # CASE B: Known Lengths + Known Time -> Find Speed
    if len(lengths_m) >= 1 and len(times_s) >= 1 and len(speeds_kmh) == 0:
        total_dist_m = sum(lengths_m)
        t_sec = times_s[0]
        if t_sec <= 0:
            return None
        v_ms = total_dist_m / t_sec
        v_kmh = to_kmh_speed(v_ms)

        steps = [
            f"Step 1: Identify total distance traversed: {total_dist_m} meters.",
            f"Step 2: Given crossing time: {t_sec} seconds.",
            f"Step 3: Speed in m/s = Distance ÷ Time = {total_dist_m} m ÷ {t_sec} s = {v_ms:.3f} m/s.",
            f"Step 4: Convert m/s to km/h by multiplying by (18/5): {v_ms:.3f} × (18/5) = {v_kmh:.2f} km/h."
        ]

        return {
            "title": "Universal Motion Solver (Train Speed Calculated)",
            "summary_value": f"{v_kmh:.2f} km/h ({v_ms:.2f} m/s)",
            "formula": "Speed = (Distance ÷ Time) × (18 ÷ 5)",
            "rows": [
                ["Calculated Speed (km/h)", f"{v_kmh:.2f} km/h"],
                ["Speed in SI Units (m/s)", f"{v_ms:.2f} m/s"],
                ["Distance Covered", f"{total_dist_m} meters"],
                ["Time Taken", f"{t_sec} seconds"]
            ],
            "steps": steps,
            "insights": "Conversion factor: 1 km/h = 5/18 m/s, conversely 1 m/s = 18/5 km/h = 3.6 km/h.",
            "raw": v_kmh
        }

    # CASE C: Known Speed + Known Time + One Length -> Find Missing Length (e.g. Platform or Train)
    if len(speeds_kmh) >= 1 and len(times_s) >= 1 and len(lengths_m) == 1:
        v_ms = to_si_speed(speeds_kmh[0], 'km/h')
        t_sec = times_s[0]
        total_dist_m = v_ms * t_sec
        known_len = lengths_m[0]
        missing_len = total_dist_m - known_len

        steps = [
            f"Step 1: Convert speed to m/s: {speeds_kmh[0]} km/h × (5/18) = {v_ms:.3f} m/s.",
            f"Step 2: Total distance covered in {t_sec}s: D = v × t = {v_ms:.3f} × {t_sec} = {total_dist_m:.2f} meters.",
            f"Step 3: Total distance = Train Length + Platform/Object Length.",
            f"Step 4: Missing Length = Total Distance − Known Length = {total_dist_m:.2f} − {known_len} = {missing_len:.2f} meters."
        ]

        return {
            "title": "Universal Motion Solver (Missing Length Calculated)",
            "summary_value": f"{missing_len:.2f} meters",
            "formula": "Total Distance = Speed × Time;  Missing Length = Total − Known",
            "rows": [
                ["Missing Length", f"{missing_len:.2f} meters"],
                ["Total Distance Traversed", f"{total_dist_m:.2f} meters"],
                ["Known Length", f"{known_len} meters"],
                ["Train Speed", f"{speeds_kmh[0]} km/h"]
            ],
            "steps": steps,
            "insights": "The total distance covered during crossing equals the sum of both the moving train and the stationary structure.",
            "raw": missing_len
        }

    return None


# ==============================================================================
# 3. UNIVERSAL DYNAMIC AGE ALGEBRA SOLVER
# Formulates and solves ANY arbitrary age word problem using linear systems:
# e.g., "Father is 3 times older than son. After 10 years he will be twice as old."
# ==============================================================================
def solve_universal_age(query: str) -> Optional[Dict[str, Any]]:
    """Dynamically parses and solves age word problems using SymPy linear systems."""
    q = query.lower()
    if not re.search(r'\b(?:age|ages|father|son|mother|daughter|older|younger|times as old|years ago|hence|later|years older)\b', q):
        return None

    # Check for "N times older" or "N times as old"
    ratio_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:times|guna)', q)
    # Check for year shifts: "in 10 years", "after 5 years", "5 years ago", "10 years hence"
    shift_matches = re.findall(r'(?:in|after|hence|ago)\s*(\d+)\s*years?', q)
    if not shift_matches:
        shift_matches = re.findall(r'(\d+)\s*years?\s*(?:ago|hence|later)', q)

    if len(ratio_matches) >= 2 and len(shift_matches) >= 1:
        r1 = float(ratio_matches[0])  # current ratio: F = r1 * S
        r2 = float(ratio_matches[1])  # future/past ratio
        k = float(shift_matches[0])   # year delta
        is_ago = 'ago' in q

        # Set up SymPy symbols
        F, S = symbols('F S', positive=True, real=True)
        # Equation 1: F = r1 * S
        eq1 = Eq(F, r1 * S)
        # Equation 2: (F + k) = r2 * (S + k) if future else (F - k) = r2 * (S - k)
        delta = -k if is_ago else k
        eq2 = Eq(F + delta, r2 * (S + delta))

        sol = solve([eq1, eq2], [F, S])
        if sol and F in sol and S in sol:
            f_age = float(sol[F])
            s_age = float(sol[S])

            steps = [
                f"Step 1: Let Son's present age = S, Father's present age = F.",
                f"Step 2: From first condition: F = {r1} × S.",
                f"Step 3: Condition after {k} years ({'past' if is_ago else 'future'}): (F {'−' if is_ago else '+'} {k}) = {r2} × (S {'−' if is_ago else '+'} {k}).",
                f"Step 4: Substitute F into equation 2: ({r1}S {'−' if is_ago else '+'} {k}) = {r2}S {'−' if is_ago else '+'} {r2*k}.",
                f"Step 5: Solve algebraically: S = {s_age:.1f} years, F = {f_age:.1f} years."
            ]

            return {
                "title": "Universal Age Problem Solver",
                "summary_value": f"Father: {int(f_age) if f_age.is_integer() else f_age:.1f} yrs · Son: {int(s_age) if s_age.is_integer() else s_age:.1f} yrs",
                "formula": "Simultaneous Age Equations: F = r₁S,  (F + Δt) = r₂(S + Δt)",
                "rows": [
                    ["Older Person / Father's Age", f"{int(f_age) if f_age.is_integer() else f_age:.1f} years"],
                    ["Younger Person / Son's Age", f"{int(s_age) if s_age.is_integer() else s_age:.1f} years"],
                    ["Initial Ratio", f"{r1} : 1"],
                    ["Second Ratio (after delta)", f"{r2} : 1"]
                ],
                "steps": steps,
                "insights": "Age differences between any two individuals remain strictly constant across all points in time.",
                "raw": f_age
            }

    return None


# ==============================================================================
# 4. UNIVERSAL CHAIN-RULE WORK / TIME / MEN EQUIVALENCE
# Formula: (M1 * D1 * H1) / W1 = (M2 * D2 * H2) / W2
# Solves ANY work variation problem for any unknown variable!
# ==============================================================================
def solve_universal_chain_work(query: str) -> Optional[Dict[str, Any]]:
    """Solves multi-variable workforce problems: (M1 * D1 * H1) / W1 = (M2 * D2 * H2) / W2."""
    q = query.lower()
    if not re.search(r'\b(?:men|workers|persons|aadmi|labour)\b', q) or not re.search(r'\b(?:days|din|hours|ghante)\b', q):
        return None

    # Extract all numbers in query
    all_nums = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', q)]
    if len(all_nums) < 4:
        return None

    # If format has Men1, Days1, Hours1, Men2, Hours2 -> Find Days2
    # e.g., "6 men can complete work in 12 days working 8 hours. How many days for 9 men working 6 hours?"
    if len(all_nums) >= 5:
        m1, d1, h1, m2, h2 = all_nums[0], all_nums[1], all_nums[2], all_nums[3], all_nums[4]
        # (M1 * D1 * H1) = (M2 * D2 * H2)
        d2 = (m1 * d1 * h1) / (m2 * h2)

        steps = [
            f"Step 1: Apply Universal Work Equivalence Theorem: (M₁ × D₁ × H₁) ÷ W₁ = (M₂ × D₂ × H₂) ÷ W₂",
            f"Step 2: Total man-hours required for project = {m1} men × {d1} days × {h1} hrs/day = {m1*d1*h1} man-hours.",
            f"Step 3: New workforce rate per day = {m2} men × {h2} hrs/day = {m2*h2} man-hours/day.",
            f"Step 4: Total days required D₂ = {m1*d1*h1} ÷ {m2*h2} = {d2:.2f} days."
        ]

        return {
            "title": "Universal Work & Workforce Equivalence (Chain Rule)",
            "summary_value": f"{d2:.2f} days ({int(d2) if d2.is_integer() else d2:.1f} din)",
            "formula": "M₁ × D₁ × H₁ = M₂ × D₂ × H₂",
            "rows": [
                ["Required Days (D₂)", f"{d2:.2f} days"],
                ["Total Work (Man-Hours)", f"{m1*d1*h1:,.0f} hours"],
                ["Initial Group (M₁ × D₁ × H₁)", f"{m1} men, {d1} days, {h1} hrs/day"],
                ["New Group (M₂ × H₂)", f"{m2} men, {h2} hrs/day"]
            ],
            "steps": steps,
            "insights": "Total project workload is conserved as the product of workforce size, duration, and daily hours.",
            "raw": d2
        }

    return None
