"""Advanced Quantitative Aptitude Reasoning Engine for Calculator GPT.
100% Offline, Pure Python & SymPy Mathematical Algorithms.

Covers:
1. Boats & Streams: Upstream, downstream, speed in still water, stream velocity, round trips.
2. Pipes & Cisterns: Inlets, outlets, leaks, filling & emptying times.
3. Mixtures & Alligation: Rule of alligation, repeated dilution & replacement, ratio mixing.
4. Probability & Combinatorics: Coin tosses, dice rolls, 52-card deck, urns/balls, nPr, nCr.
5. Progressive Commercial Math: Marked price, successive discounts, margin vs markup, net profit.
"""

import math
import re
from typing import Dict, Any, List, Optional, Tuple
import sympy as sp
from .nlp_parser import extract_numbers, normalize_query


def fmt(n: float, decimals: int = 2) -> str:
    """Formats numeric values cleanly."""
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
# 1. BOATS & STREAMS
# ==============================================================================
def solve_boat_stream(query: str) -> Optional[Dict[str, Any]]:
    """Solves Boats and Streams problems for any unknown:
    - Speed in still water (u)
    - Rate of stream / current (v)
    - Downstream speed (u + v)
    - Upstream speed (u - v)
    - Distance or Time taken
    """
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:boat|stream|current|upstream|downstream|still water|dhara|nau|naav|shant jal|anupravah|urdhvapravah)\b', q):
        return None

    raw_nums = extract_numbers(q)
    
    # Check for upstream / downstream distances and times
    # e.g., "A boat travels 24 km upstream in 4 hours and 36 km downstream in 3 hours"
    up_m = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kms)?\s*(?:upstream|urdhvapravah)\s*(?:in)?\s*(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|ghante)', q)
    down_m = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kms)?\s*(?:downstream|anupravah)\s*(?:in)?\s*(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|ghante)', q)
    
    # Or reverse order: "in 4 hours 24 km upstream"
    if not up_m:
        up_m = re.search(r'(?:in)?\s*(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(\d+(?:\.\d+)?)\s*(?:km|kms)?\s*(?:upstream|urdhvapravah)', q)
        if up_m:
            up_dist, up_time = float(up_m.group(2)), float(up_m.group(1))
        else:
            up_dist, up_time = None, None
    else:
        up_dist, up_time = float(up_m.group(1)), float(up_m.group(2))
        
    if not down_m:
        down_m = re.search(r'(?:in)?\s*(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(\d+(?:\.\d+)?)\s*(?:km|kms)?\s*(?:downstream|anupravah)', q)
        if down_m:
            down_dist, down_time = float(down_m.group(2)), float(down_m.group(1))
        else:
            down_dist, down_time = None, None
    else:
        down_dist, down_time = float(down_m.group(1)), float(down_m.group(2))

    # Case 1: Both upstream and downstream distances & times known
    if up_dist and up_time and down_dist and down_time and up_time > 0 and down_time > 0:
        up_speed = up_dist / up_time
        down_speed = down_dist / down_time
        boat_speed = (down_speed + up_speed) / 2.0
        stream_speed = (down_speed - up_speed) / 2.0
        
        return {
            "title": "Boats & Streams: Still Water & Stream Velocity",
            "summary_value": f"Boat in Still Water: {fmt(boat_speed)} km/h · Stream Speed: {fmt(stream_speed)} km/h",
            "formula": "u = (Downstream + Upstream) ÷ 2,  v = (Downstream − Upstream) ÷ 2",
            "rows": [
                ["Speed of Boat in Still Water (u)", f"{fmt(boat_speed)} km/h"],
                ["Speed of Stream / Current (v)", f"{fmt(stream_speed)} km/h"],
                ["Downstream Speed (D = u + v)", f"{fmt(down_speed)} km/h ({down_dist} km in {down_time}h)"],
                ["Upstream Speed (U = u − v)", f"{fmt(up_speed)} km/h ({up_dist} km in {up_time}h)"]
            ],
            "steps": [
                f"Step 1: Calculate Upstream speed: U = Distance ÷ Time = {up_dist} km ÷ {up_time} hrs = {fmt(up_speed)} km/h.",
                f"Step 2: Calculate Downstream speed: D = Distance ÷ Time = {down_dist} km ÷ {down_time} hrs = {fmt(down_speed)} km/h.",
                f"Step 3: Speed of Boat in Still Water u = (D + U) ÷ 2 = ({fmt(down_speed)} + {fmt(up_speed)}) ÷ 2 = {fmt(boat_speed)} km/h.",
                f"Step 4: Rate of Stream Current v = (D − U) ÷ 2 = ({fmt(down_speed)} − {fmt(up_speed)}) ÷ 2 = {fmt(stream_speed)} km/h."
            ],
            "insights": "Downstream travel is aided by the current (u + v), while upstream travel is opposed by the current (u - v).",
            "raw": boat_speed
        }

    # Case 2: Direct downstream and upstream speeds given (e.g. "downstream speed 15 km/h, upstream speed 9 km/h")
    d_speed_m = re.search(r'(?:downstream speed|downstream rate|anupravah gati)\s*(?:=|is|:)?\s*(\d+(?:\.\d+)?)', q)
    u_speed_m = re.search(r'(?:upstream speed|upstream rate|urdhvapravah gati)\s*(?:=|is|:)?\s*(\d+(?:\.\d+)?)', q)
    if d_speed_m and u_speed_m:
        d_val = float(d_speed_m.group(1))
        u_val = float(u_speed_m.group(1))
        b_speed = (d_val + u_val) / 2.0
        s_speed = (d_val - u_val) / 2.0
        return {
            "title": "Boats & Streams: Speed Breakdown",
            "summary_value": f"Boat Speed: {fmt(b_speed)} km/h · Stream: {fmt(s_speed)} km/h",
            "formula": "u = (D + U) ÷ 2,  v = (D − U) ÷ 2",
            "rows": [
                ["Boat in Still Water (u)", f"{fmt(b_speed)} km/h"],
                ["Stream Current (v)", f"{fmt(s_speed)} km/h"],
                ["Downstream Speed (D)", f"{fmt(d_val)} km/h"],
                ["Upstream Speed (U)", f"{fmt(u_val)} km/h"]
            ],
            "steps": [
                f"Step 1: Given Downstream speed D = {fmt(d_val)} km/h, Upstream speed U = {fmt(u_val)} km/h.",
                f"Step 2: Still water speed u = (D + U) / 2 = ({d_val} + {u_val}) / 2 = {fmt(b_speed)} km/h.",
                f"Step 3: Current rate v = (D − U) / 2 = ({d_val} − {u_val}) / 2 = {fmt(s_speed)} km/h."
            ],
            "insights": "Still water speed is the arithmetic mean of downstream and upstream velocities.",
            "raw": b_speed
        }

    # Case 3: Still water speed u and stream velocity v given -> find downstream/upstream or time
    # e.g., "boat speed in still water is 12 km/h and stream is 3 km/h. How long to travel 45 km downstream?"
    still_m = re.search(r'(?:still water|boat speed|boat in still water|shant jal|boat ki speed)\s*(?:mein|is|=|:|hai)?\s*(\d+(?:\.\d+)?)', q, re.I)
    stream_m = re.search(r'(?:stream|current|water speed|dhara|river speed)\s*(?:ki speed|ki chaal|mein|is|=|:|hai)?\s*(\d+(?:\.\d+)?)', q, re.I)
    dist_m = re.search(r'(\d+(?:\.\d+)?)\s*(?:kms?|kilometres?|kilometers?)\b(?!\s*[/ph])', q, re.I)
    
    if still_m and stream_m:
        u_val = float(still_m.group(1))
        v_val = float(stream_m.group(1))
        d_speed = u_val + v_val
        u_speed = u_val - v_val
        dist = float(dist_m.group(1)) if dist_m else None
        
        is_up = bool(re.search(r'upstream|urdhvapravah', q))
        is_down = bool(re.search(r'downstream|anupravah', q))
        
        if dist and (is_up or is_down):
            chosen_speed = u_speed if is_up else d_speed
            dir_name = "Upstream" if is_up else "Downstream"
            if chosen_speed <= 0:
                return {
                    "title": "Boats & Streams: Insufficient Speed",
                    "summary_value": "Cannot travel upstream (Stream speed exceeds or equals boat speed)",
                    "formula": "Upstream Speed = u − v ≤ 0",
                    "rows": [["Boat Speed", f"{u_val} km/h"], ["Stream Speed", f"{v_val} km/h"]],
                    "steps": ["The stream flows faster than the boat's propulsion, making upstream progress impossible."],
                    "insights": "For upstream motion, boat speed must strictly exceed stream speed.",
                    "raw": None
                }
            time_h = dist / chosen_speed
            hrs = int(time_h)
            mins = round((time_h - hrs) * 60)
            t_str = f"{hrs}h {mins}m ({fmt(time_h, 2)} hrs)" if hrs > 0 and mins > 0 else f"{fmt(time_h, 2)} hours"
            
            return {
                "title": f"Boats & Streams: {dir_name} Travel Time",
                "summary_value": t_str,
                "formula": f"Time = Distance ÷ {dir_name} Speed ({'u − v' if is_up else 'u + v'})",
                "rows": [
                    ["Time Taken", t_str],
                    [f"{dir_name} Speed", f"{fmt(chosen_speed)} km/h"],
                    ["Distance Covered", f"{fmt(dist)} km"],
                    ["Boat Speed in Still Water (u)", f"{fmt(u_val)} km/h"],
                    ["Stream Speed (v)", f"{fmt(v_val)} km/h"]
                ],
                "steps": [
                    f"Step 1: Identify velocities: Boat in still water u = {fmt(u_val)} km/h, Stream current v = {fmt(v_val)} km/h.",
                    f"Step 2: Effective {dir_name} velocity = {u_val} {'−' if is_up else '+'} {v_val} = {fmt(chosen_speed)} km/h.",
                    f"Step 3: Distance to cover: D = {fmt(dist)} km.",
                    f"Step 4: Time taken = Distance ÷ Speed = {fmt(dist)} ÷ {fmt(chosen_speed)} = {fmt(time_h, 3)} hours ({t_str})."
                ],
                "insights": f"{dir_name} motion {'resists' if is_up else 'assists'} boat speed by exactly the velocity of the water current.",
                "raw": time_h
            }
        else:
            return {
                "title": "Boats & Streams: Velocity Analysis",
                "summary_value": f"Downstream: {fmt(d_speed)} km/h · Upstream: {fmt(u_speed)} km/h",
                "formula": "Downstream = u + v,  Upstream = u − v",
                "rows": [
                    ["Downstream Velocity (u + v)", f"{fmt(d_speed)} km/h"],
                    ["Upstream Velocity (u − v)", f"{fmt(u_speed)} km/h"],
                    ["Boat in Still Water (u)", f"{fmt(u_val)} km/h"],
                    ["Stream Velocity (v)", f"{fmt(v_val)} km/h"]
                ],
                "steps": [
                    f"Step 1: Given boat speed in still water u = {fmt(u_val)} km/h, stream velocity v = {fmt(v_val)} km/h.",
                    f"Step 2: Downstream Speed D = u + v = {u_val} + {v_val} = {fmt(d_speed)} km/h.",
                    f"Step 3: Upstream Speed U = u − v = {u_val} − {v_val} = {fmt(u_speed)} km/h."
                ],
                "insights": "Still water speed is the midpoint between downstream and upstream speeds.",
                "raw": d_speed
            }

    # Case 4: General numbers fallback if 'boat' in query with 2 numbers
    if len(raw_nums) >= 2:
        u_val, v_val = max(raw_nums[0], raw_nums[1]), min(raw_nums[0], raw_nums[1])
        d_speed = u_val + v_val
        u_speed = u_val - v_val
        return {
            "title": "Boats & Streams Calculation",
            "summary_value": f"Downstream: {fmt(d_speed)} km/h · Upstream: {fmt(u_speed)} km/h",
            "formula": "Downstream = u + v,  Upstream = u − v",
            "rows": [
                ["Downstream Speed (u + v)", f"{fmt(d_speed)} km/h"],
                ["Upstream Speed (u − v)", f"{fmt(u_speed)} km/h"],
                ["Boat Speed (u)", f"{fmt(u_val)} km/h"],
                ["Stream Speed (v)", f"{fmt(v_val)} km/h"]
            ],
            "steps": [
                f"Step 1: Boat speed in still water u = {fmt(u_val)} km/h, Stream speed v = {fmt(v_val)} km/h",
                f"Step 2: Downstream = {u_val} + {v_val} = {fmt(d_speed)} km/h",
                f"Step 3: Upstream = {u_val} − {v_val} = {fmt(u_speed)} km/h"
            ],
            "insights": "Downstream speed is always greater than upstream speed by 2v (twice stream velocity).",
            "raw": d_speed
        }

    return None


# ==============================================================================
# 2. PIPES & CISTERNS
# ==============================================================================
def solve_pipe_cistern(query: str) -> Optional[Dict[str, Any]]:
    """Solves Pipe and Cistern problems:
    - Multiple inlet pipes filling together
    - Inlets filling and outlets emptying
    - Tank leak problems: tap fills in A hrs, with leak takes B hrs -> leak empties in ?
    """
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:pipe|pipes|cistern|tank|tanki|nal|leak|leakage|outlet|inlet|emptying|filling|chhed|risav)\b', q):
        return None

    raw_nums = extract_numbers(q)
    
    # --------------------------------------------------------------------------
    # Leak Problem: "A tap fills in 8 hours. Due to a leak it takes 10 hours. How long for leak to empty?"
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:leak|leakage|chhed|risav)\b', q) and len(raw_nums) >= 2:
        # Smaller number is normal fill time, larger number is time with leak
        t_fill = min(raw_nums[0], raw_nums[1])
        t_with_leak = max(raw_nums[0], raw_nums[1])
        
        # Rate of tap = 1 / t_fill
        # Combined rate = 1 / t_with_leak
        # Rate of leak = 1/t_fill - 1/t_with_leak = (t_with_leak - t_fill) / (t_fill * t_with_leak)
        # Time for leak to empty = (t_fill * t_with_leak) / (t_with_leak - t_fill)
        diff = t_with_leak - t_fill
        if diff > 0:
            t_leak = (t_fill * t_with_leak) / diff
            return {
                "title": "Pipes & Cisterns: Tank Leak Emptiness Time",
                "summary_value": f"{fmt(t_leak)} hours",
                "formula": "Time to Empty = (T_fill × T_leak_total) ÷ (T_leak_total − T_fill)",
                "rows": [
                    ["Time for Leak to Empty Full Tank", f"{fmt(t_leak)} hours ({fmt(t_leak*60)} mins)"],
                    ["Normal Filling Time", f"{fmt(t_fill)} hours (Rate: 1/{fmt(t_fill)}/hr)"],
                    ["Filling Time with Leak Active", f"{fmt(t_with_leak)} hours (Rate: 1/{fmt(t_with_leak)}/hr)"],
                    ["Net Leak Discharge Rate", f"1/{fmt(t_leak)} of tank capacity per hour"]
                ],
                "steps": [
                    f"Step 1: Normal filling rate of tap = 1/{t_fill} of tank per hour.",
                    f"Step 2: Effective filling rate with leak active = 1/{t_with_leak} per hour.",
                    f"Step 3: Emptying rate of leak alone = (Normal Rate) − (Effective Rate) = (1/{t_fill}) − (1/{t_with_leak}).",
                    f"Step 4: Common denominator: ({t_with_leak} − {t_fill}) ÷ ({t_fill} × {t_with_leak}) = {diff} ÷ {t_fill*t_with_leak} = 1/{fmt(t_leak)}.",
                    f"Step 5: Taking reciprocal: Leak alone empties the entire full cistern in {fmt(t_leak)} hours."
                ],
                "insights": "A leak subtracts from the net inflow rate; the leak rate is the difference between normal and observed inflow rates.",
                "raw": t_leak
            }

    # --------------------------------------------------------------------------
    # Mixed Inlets and Outlets: e.g. "Pipe A fills in 12 hrs, Pipe B in 15 hrs, Pipe C empties in 20 hrs"
    # --------------------------------------------------------------------------
    inlet_matches = re.findall(r'(?:pipe\s*[a-zA-Z0-9]?|tap\s*[a-zA-Z0-9]?|first|second)?\s*(?:fills?|fill)\s*(?:in|the tank in)?\s*(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|mins?|minutes?)', q)
    outlet_matches = re.findall(r'(?:pipe\s*[a-zA-Z0-9]?|tap\s*[a-zA-Z0-9]?|third|outlet|waste)?\s*(?:empt(?:y|ies)|empty)\s*(?:in|the tank in)?\s*(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|mins?|minutes?)', q)
    
    if outlet_matches and (inlet_matches or len(raw_nums) >= 2):
        inlets = [float(x) for x in inlet_matches] if inlet_matches else [raw_nums[0]]
        outlets = [float(x) for x in outlet_matches]
        
        in_rate = sum([1.0 / t for t in inlets if t > 0])
        out_rate = sum([1.0 / t for t in outlets if t > 0])
        net_rate = in_rate - out_rate
        
        if net_rate > 0:
            total_time = 1.0 / net_rate
            return {
                "title": "Pipes & Cisterns: Combined Inlets & Outlets",
                "summary_value": f"{fmt(total_time)} hours to fill",
                "formula": "Net Rate = Σ(1/T_inlet) − Σ(1/T_outlet),  Total Time = 1 ÷ Net Rate",
                "rows": [
                    ["Time to Fill Completely", f"{fmt(total_time)} hours"],
                    ["Inlet Rates Sum", f"{in_rate:.4f} tank/hr (from {inlets} hrs)"],
                    ["Outlet Rates Sum", f"{out_rate:.4f} tank/hr (from {outlets} hrs)"],
                    ["Net Filling Rate", f"{net_rate:.4f} tank/hr"]
                ],
                "steps": [
                    f"Step 1: Compute positive inflow rates from filling pipes: {inlets} ⟹ Inflow = {in_rate:.4f}/hr.",
                    f"Step 2: Compute negative outflow rates from emptying pipes: {outlets} ⟹ Outflow = {out_rate:.4f}/hr.",
                    f"Step 3: Net fill rate = Inflow − Outflow = {in_rate:.4f} − {out_rate:.4f} = {net_rate:.4f} tank/hour.",
                    f"Step 4: Total hours to fill tank = 1 ÷ {net_rate:.4f} = {fmt(total_time)} hours."
                ],
                "insights": "As long as net inflow is positive, the cistern will eventually fill. If negative, the tank drains.",
                "raw": total_time
            }
        elif net_rate < 0:
            drain_time = 1.0 / abs(net_rate)
            return {
                "title": "Pipes & Cisterns: Net Emptying Rate",
                "summary_value": f"{fmt(drain_time)} hours to empty completely",
                "formula": "Net Rate < 0 ⟹ Cistern Empties: Time = 1 ÷ |Net Rate|",
                "rows": [
                    ["Time to Empty Tank", f"{fmt(drain_time)} hours"],
                    ["Net Draining Rate", f"{abs(net_rate):.4f} tank/hr"]
                ],
                "steps": [
                    f"Outflow rate ({out_rate:.4f}/hr) exceeds inflow rate ({in_rate:.4f}/hr).",
                    f"Net emptying rate = {abs(net_rate):.4f} tank/hr.",
                    f"Time required to drain a full tank = 1 ÷ {abs(net_rate):.4f} = {fmt(drain_time)} hours."
                ],
                "insights": "When emptying capacity exceeds filling capacity, the tank cannot fill and will drain.",
                "raw": drain_time
            }

    # --------------------------------------------------------------------------
    # Standard 2 or 3 Inlet Pipes filling together
    # --------------------------------------------------------------------------
    if len(raw_nums) >= 2:
        if len(raw_nums) == 2:
            t1, t2 = raw_nums[0], raw_nums[1]
            comb = (t1 * t2) / (t1 + t2)
            unit = "minutes" if 'min' in q else "hours"
            return {
                "title": f"Pipes & Cisterns: 2 Pipes Together ({fmt(t1)} & {fmt(t2)} {unit})",
                "summary_value": f"{fmt(comb)} {unit}",
                "formula": "Total Time = (T₁ × T₂) ÷ (T₁ + T₂)",
                "rows": [
                    ["Combined Time to Fill", f"{fmt(comb)} {unit}"],
                    ["Pipe 1 Rate", f"1/{fmt(t1)} tank/{unit}"],
                    ["Pipe 2 Rate", f"1/{fmt(t2)} tank/{unit}"],
                    ["Combined Rate", f"1/{fmt(comb)} tank/{unit}"]
                ],
                "steps": [
                    f"Step 1: In 1 {unit}, Pipe 1 fills 1/{t1} of tank, Pipe 2 fills 1/{t2} of tank.",
                    f"Step 2: Combined rate in 1 {unit} = (1/{t1}) + (1/{t2}) = ({t1} + {t2}) / ({t1} × {t2}) = {t1+t2}/{t1*t2}.",
                    f"Step 3: Total time to fill full tank = ({t1} × {t2}) ÷ ({t1} + {t2}) = {t1*t2} ÷ {t1+t2} = {fmt(comb)} {unit}."
                ],
                "insights": "In parallel operation, filling capacities add linearly, reducing the required filling time.",
                "raw": comb
            }
        elif len(raw_nums) >= 3:
            t1, t2, t3 = raw_nums[0], raw_nums[1], raw_nums[2]
            comb_rate = (1.0/t1) + (1.0/t2) + (1.0/t3)
            tot_t = 1.0 / comb_rate
            unit = "minutes" if 'min' in q else "hours"
            return {
                "title": f"Pipes & Cisterns: 3 Inlets Together ({fmt(t1)}, {fmt(t2)}, {fmt(t3)} {unit})",
                "summary_value": f"{fmt(tot_t)} {unit}",
                "formula": "1/T_total = 1/T₁ + 1/T₂ + 1/T₃",
                "rows": [
                    ["Combined Time to Fill", f"{fmt(tot_t)} {unit}"],
                    ["Pipe 1 Time", f"{fmt(t1)} {unit}"],
                    ["Pipe 2 Time", f"{fmt(t2)} {unit}"],
                    ["Pipe 3 Time", f"{fmt(t3)} {unit}"],
                    ["Combined Rate", f"{comb_rate:.4f} tank/{unit}"]
                ],
                "steps": [
                    f"Step 1: Individual rates per {unit}: 1/{t1}, 1/{t2}, 1/{t3}.",
                    f"Step 2: Sum of rates = 1/{t1} + 1/{t2} + 1/{t3} = {comb_rate:.4f} tank/{unit}.",
                    f"Step 3: Reciprocal yields total duration = 1 ÷ {comb_rate:.4f} = {fmt(tot_t)} {unit}."
                ],
                "insights": "Three simultaneous inlet streams fill the reservoir in less than one-third of the slowest pipe's duration.",
                "raw": tot_t
            }

    return None


# ==============================================================================
# 3. MIXTURES & ALLIGATION
# ==============================================================================
def solve_mixture_alligation(query: str) -> Optional[Dict[str, Any]]:
    """Solves:
    1. Repeated dilution / replacement:
       Q_remaining = Q_initial * (1 - y / Q_initial)^n
    2. Rule of Alligation (Cheaper, Dearer, Mean price):
       (Cheaper Quantity) : (Dearer Quantity) = (Dearer Price − Mean) : (Mean − Cheaper Price)
    3. Ratio mixture proportions
    """
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:mixture|alligation|dilution|diluted|replaced|replacement|milk and water|pure milk|wine|alcohol|acid|solution|mishran)\b', q):
        return None

    raw_nums = extract_numbers(q)
    
    # --------------------------------------------------------------------------
    # Repeated Dilution / Replacement Formula
    # e.g., "A container has 80 liters pure milk. 8 liters is replaced with water, repeated 2 more times (total 3 times)"
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:repeat|repeated|drawn|removed|replaced|replacement|times)\b', q) and len(raw_nums) >= 2:
        init_vol = raw_nums[0]
        drawn_vol = raw_nums[1]
        
        # Check number of iterations n
        n_times = 1
        n_match = re.search(r'(\d+)\s*(?:more\s*)?times', q)
        if 'repeated 2 more times' in q or '2 more times' in q:
            n_times = 3
        elif 'repeated 3 more times' in q:
            n_times = 4
        elif n_match:
            n_times = int(n_match.group(1))
            if 'more times' in q:
                n_times += 1
        elif len(raw_nums) >= 3:
            n_times = int(raw_nums[2])
            
        if init_vol > 0 and 0 < drawn_vol <= init_vol and n_times >= 1:
            fraction_remaining = (1.0 - (drawn_vol / init_vol)) ** n_times
            rem_pure = init_vol * fraction_remaining
            water_vol = init_vol - rem_pure
            pure_pct = (rem_pure / init_vol) * 100.0
            
            return {
                "title": f"Repeated Dilution & Replacement ({n_times} operations)",
                "summary_value": f"Remaining Pure Liquid: {fmt(rem_pure)} L ({fmt(pure_pct)}%)",
                "formula": "Pure Liquid Remaining = X × (1 − y/X)ⁿ",
                "rows": [
                    ["Remaining Pure Liquid", f"{fmt(rem_pure)} liters"],
                    ["Added Water / Diluent", f"{fmt(water_vol)} liters"],
                    ["Pure Concentration", f"{fmt(pure_pct)}%"],
                    ["Final Ratio (Pure : Water)", f"{fmt(rem_pure)} : {fmt(water_vol)}"],
                    ["Initial Volume (X)", f"{fmt(init_vol)} liters"],
                    ["Volume Replaced each time (y)", f"{fmt(drawn_vol)} liters"],
                    ["Number of Cycles (n)", str(n_times)]
                ],
                "steps": [
                    f"Step 1: Initial pure volume X = {fmt(init_vol)} L, Volume replaced per cycle y = {fmt(drawn_vol)} L.",
                    f"Step 2: Total replacement cycles n = {n_times}.",
                    f"Step 3: Dilution ratio factor per step = (1 − y/X) = (1 − {drawn_vol}/{init_vol}) = {1.0 - drawn_vol/init_vol:.4f}.",
                    f"Step 4: After {n_times} cycles: Fraction = ({1.0 - drawn_vol/init_vol:.4f})^{n_times} = {fraction_remaining:.6f}.",
                    f"Step 5: Remaining pure liquid = {fmt(init_vol)} × {fraction_remaining:.6f} = {fmt(rem_pure)} liters.",
                    f"Step 6: Remaining water volume = Total − Pure = {fmt(init_vol)} − {fmt(rem_pure)} = {fmt(water_vol)} liters."
                ],
                "insights": "Each dilution cycle removes a portion of the remaining pure liquid, causing the pure concentration to decay exponentially.",
                "raw": rem_pure
            }

    # --------------------------------------------------------------------------
    # Rule of Alligation (Cheaper, Dearer, Mean Price)
    # e.g., "In what ratio rice at 60/kg be mixed with rice at 80/kg to get mixture worth 68/kg?"
    # --------------------------------------------------------------------------
    if len(raw_nums) >= 3:
        # Sort out cheaper, dearer, and mean
        s_nums = sorted(raw_nums[:3])
        c_price = s_nums[0]  # Cheaper
        m_price = s_nums[1]  # Mean / Desired price
        d_price = s_nums[2]  # Dearer
        
        # Verify mean is between cheaper and dearer
        if c_price < m_price < d_price:
            cheaper_parts = d_price - m_price
            dearer_parts = m_price - c_price
            
            # Reduce ratio
            import math as mth
            g = mth.gcd(int(round(cheaper_parts * 100)), int(round(dearer_parts * 100)))
            r1 = (cheaper_parts * 100) / g
            r2 = (dearer_parts * 100) / g
            
            ratio_str = f"{int(r1)} : {int(r2)}" if r1.is_integer() and r2.is_integer() else f"{fmt(cheaper_parts)} : {fmt(dearer_parts)}"
            
            return {
                "title": "Rule of Alligation (Mixing Ratio)",
                "summary_value": f"Ratio (Cheaper : Dearer) = {ratio_str}",
                "formula": "(Quantity of Cheaper) ÷ (Quantity of Dearer) = (Dearer Price − Mean) ÷ (Mean − Cheaper Price)",
                "rows": [
                    ["Required Mixing Ratio (C : D)", ratio_str],
                    ["Cheaper Proportion Parts", fmt(cheaper_parts)],
                    ["Dearer Proportion Parts", fmt(dearer_parts)],
                    ["Cheaper Unit Cost (c)", fmt_curr(c_price)],
                    ["Dearer Unit Cost (d)", fmt_curr(d_price)],
                    ["Target Mean Cost (m)", fmt_curr(m_price)]
                ],
                "steps": [
                    f"Step 1: Identify costs: Cheaper price c = {fmt_curr(c_price)}, Dearer price d = {fmt_curr(d_price)}, Target mean price m = {fmt_curr(m_price)}.",
                    f"Step 2: Cross differences: (Dearer Price − Mean) = {d_price} − {m_price} = {fmt(cheaper_parts)}.",
                    f"Step 3: Cross differences: (Mean − Cheaper Price) = {m_price} − {c_price} = {fmt(dearer_parts)}.",
                    f"Step 4: Alligation ratio: (Cheaper) : (Dearer) = {fmt(cheaper_parts)} : {fmt(dearer_parts)} = {ratio_str}."
                ],
                "insights": "The Rule of Alligation is an inverted weighted-average method used to find the exact proportions needed to produce a target concentration or price.",
                "raw": cheaper_parts / dearer_parts if dearer_parts > 0 else None
            }

    return None


# ==============================================================================
# 4. PROBABILITY & COMBINATORICS
# ==============================================================================
def solve_probability(query: str) -> Optional[Dict[str, Any]]:
    """Solves:
    - Coin Toss: P(k heads in n tosses) = C(n, k) / 2^n
    - Dice Rolls: Sum of 2 dice, single die, prime sum, etc.
    - 52-Card Deck: Face cards, Aces, Suits (Spade/Heart/Diamond/Club), Red/Black
    - Balls / Marbles in an Urn
    """
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:probability|chance|toss|coins?|heads?|tails?|dice|die|rolling|deck|cards?|ace|king|queen|jack|spade|heart|diamond|club|pack of 52|marbles?|balls?)\b', q):
        return None

    raw_nums = extract_numbers(q)
    
    # --------------------------------------------------------------------------
    # Coin Toss Probability: n coins, k heads
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:coin|coins|toss|tossed|tossing)\b', q):
        n_coins = None
        k_heads = None
        
        # Detect "3 coins" or "tossed 3 times"
        n_m = re.search(r'(\d+)\s*(?:coins?|times)', q)
        if n_m:
            n_coins = int(n_m.group(1))
            
        # Detect "2 heads", "at least 1 head"
        k_m = re.search(r'(\d+)\s*(?:heads?|tails?)', q)
        if k_m:
            k_heads = int(k_m.group(1))
            
        if n_coins is None and raw_nums:
            n_coins = int(raw_nums[0])
        if k_heads is None and len(raw_nums) >= 2:
            k_heads = int(raw_nums[1]) if raw_nums[1] <= n_coins else int(raw_nums[0])
            n_coins = max(int(raw_nums[0]), int(raw_nums[1]))
            
        if n_coins is not None and 1 <= n_coins <= 50:
            if k_heads is None:
                k_heads = n_coins // 2
                
            total_outcomes = 2 ** n_coins
            
            # Check "at least" or "at most"
            if re.search(r'\bat least\b', q):
                fav_outcomes = sum([math.comb(n_coins, i) for i in range(k_heads, n_coins + 1)])
                desc = f"At least {k_heads} heads in {n_coins} coin tosses"
                formula = f"P(X ≥ {k_heads}) = Σ [ⁿCᵢ] ÷ 2ⁿ (for i = {k_heads} to {n_coins})"
            elif re.search(r'\bat most\b', q):
                fav_outcomes = sum([math.comb(n_coins, i) for i in range(0, k_heads + 1)])
                desc = f"At most {k_heads} heads in {n_coins} coin tosses"
                formula = f"P(X ≤ {k_heads}) = Σ [ⁿCᵢ] ÷ 2ⁿ (for i = 0 to {k_heads})"
            else:
                fav_outcomes = math.comb(n_coins, k_heads)
                desc = f"Exactly {k_heads} heads in {n_coins} coin tosses"
                formula = "P(X = k) = ⁿCₖ ÷ 2ⁿ"
                
            prob = fav_outcomes / total_outcomes
            prob_pct = prob * 100.0
            
            # Simplified fraction
            g = math.gcd(fav_outcomes, total_outcomes)
            frac_str = f"{fav_outcomes // g}/{total_outcomes // g}"
            
            return {
                "title": f"Probability: Coin Toss ({desc})",
                "summary_value": f"{frac_str} ({fmt(prob_pct, 2)}%)",
                "formula": formula,
                "rows": [
                    ["Probability P(E)", f"{frac_str} ({fmt(prob_pct, 2)}%)"],
                    ["Decimal Probability", f"{prob:.6f}"],
                    ["Favorable Outcomes", f"{fav_outcomes:,}"],
                    ["Total Sample Space (2ⁿ)", f"{total_outcomes:,}"],
                    ["Number of Tosses (n)", str(n_coins)],
                    ["Target Heads (k)", str(k_heads)]
                ],
                "steps": [
                    f"Step 1: Total elementary outcomes for {n_coins} binary coin tosses: 2^{n_coins} = {total_outcomes:,}.",
                    f"Step 2: Number of favorable combinations choosing {k_heads} heads: {fav_outcomes:,}.",
                    f"Step 3: Classical Probability Formula: P(E) = Favorable Outcomes ÷ Total Sample Space.",
                    f"Step 4: Calculation: {fav_outcomes} ÷ {total_outcomes} = {frac_str} = {prob:.4f} ({fmt(prob_pct, 2)}%)."
                ],
                "insights": "Coin tossing follows the binomial distribution B(n, 0.5) where each toss is an independent Bernoulli trial.",
                "raw": prob
            }

    # --------------------------------------------------------------------------
    # Dice Probability: Two dice sum or single die
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:dice|die|rolling)\b', q):
        sum_m = re.search(r'(?:sum(?: of)?|total)\s*(?:of|is|=)?\s*(\d+)', q)
        target_sum = int(sum_m.group(1)) if sum_m else (int(raw_nums[0]) if raw_nums and 2 <= raw_nums[0] <= 12 else 7)
        
        if 2 <= target_sum <= 12:
            # Two standard 6-sided dice: outcomes sum = target_sum
            favorable = []
            for d1 in range(1, 7):
                for d2 in range(1, 7):
                    if d1 + d2 == target_sum:
                        favorable.append((d1, d2))
                        
            fav_count = len(favorable)
            total_outcomes = 36
            prob = fav_count / total_outcomes
            prob_pct = prob * 100.0
            
            g = math.gcd(fav_count, total_outcomes)
            frac_str = f"{fav_count // g}/{total_outcomes // g}"
            
            return {
                "title": f"Probability: Two Dice Sum = {target_sum}",
                "summary_value": f"{frac_str} ({fmt(prob_pct, 2)}%)",
                "formula": "P(Sum = S) = (Number of pairs with sum S) ÷ 36",
                "rows": [
                    ["Probability P(Sum)", f"{frac_str} ({fmt(prob_pct, 2)}%)"],
                    ["Decimal Probability", f"{prob:.4f}"],
                    ["Favorable Pairs Count", str(fav_count)],
                    ["Favorable Outcomes", str(favorable)],
                    ["Total Outcomes (6 × 6)", "36"]
                ],
                "steps": [
                    "Step 1: Two independent 6-sided dice have a sample space of 6 × 6 = 36 equally likely outcomes.",
                    f"Step 2: Favorable pairs summing to {target_sum}: {favorable} ({fav_count} outcomes).",
                    f"Step 3: Probability P = {fav_count} ÷ 36 = {frac_str} ≈ {fmt(prob_pct, 2)}%."
                ],
                "insights": "A sum of 7 is the most probable outcome when rolling two dice (probability = 6/36 = 1/6) because it has the highest number of partitions.",
                "raw": prob
            }

    # --------------------------------------------------------------------------
    # 52-Card Deck Probability
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:deck|pack|cards?|ace|king|queen|jack|spade|heart|diamond|club)\b', q):
        card_fav = 0
        card_desc = ""
        
        if re.search(r'\b(?:face cards?)\b', q):
            card_fav = 12  # 4 Jacks, 4 Queens, 4 Kings
            card_desc = "Face Card (Jack, Queen, or King)"
        elif re.search(r'\b(?:aces?|ikha|ikka)\b', q):
            card_fav = 4
            card_desc = "Ace"
        elif re.search(r'\b(?:kings?|badshah)\b', q):
            card_fav = 4
            card_desc = "King"
        elif re.search(r'\b(?:queens?|begum)\b', q):
            card_fav = 4
            card_desc = "Queen"
        elif re.search(r'\b(?:jacks?|gulam)\b', q):
            card_fav = 4
            card_desc = "Jack"
        elif re.search(r'\b(?:red card|red cards|lal patta)\b', q):
            card_fav = 26  # Hearts + Diamonds
            card_desc = "Red Card (Hearts or Diamonds)"
        elif re.search(r'\b(?:black card|black cards|kala patta)\b', q):
            card_fav = 26  # Spades + Clubs
            card_desc = "Black Card (Spades or Clubs)"
        elif re.search(r'\b(?:spades?|hukum)\b', q):
            card_fav = 13
            card_desc = "Spade"
        elif re.search(r'\b(?:hearts?|paan)\b', q):
            card_fav = 13
            card_desc = "Heart"
        elif re.search(r'\b(?:diamonds?|eent)\b', q):
            card_fav = 13
            card_desc = "Diamond"
        elif re.search(r'\b(?:clubs?|chidi)\b', q):
            card_fav = 13
            card_desc = "Club"
        elif re.search(r'\b(?:honors?|honour cards?)\b', q):
            card_fav = 16  # 4 of each Ace, K, Q, J
            card_desc = "Honor Card (Ace, King, Queen, or Jack)"
            
        if card_fav > 0:
            total_cards = 52
            prob = card_fav / total_cards
            prob_pct = prob * 100.0
            g = math.gcd(card_fav, total_cards)
            frac_str = f"{card_fav // g}/{total_cards // g}"
            
            return {
                "title": f"Probability: Card Deck ({card_desc})",
                "summary_value": f"{frac_str} ({fmt(prob_pct, 2)}%)",
                "formula": "P(E) = (Favorable Cards) ÷ 52",
                "rows": [
                    ["Probability P(E)", f"{frac_str} ({fmt(prob_pct, 2)}%)"],
                    ["Decimal Probability", f"{prob:.4f}"],
                    ["Favorable Cards Count", str(card_fav)],
                    ["Total Cards in Deck", "52"],
                    ["Odds in Favor", f"{card_fav} : {total_cards - card_fav}"]
                ],
                "steps": [
                    "Step 1: A standard deck contains 52 cards divided into 4 suits of 13 cards each (26 Red, 26 Black).",
                    f"Step 2: Number of favorable {card_desc} cards in the deck = {card_fav}.",
                    f"Step 3: Probability P = {card_fav} ÷ 52 = {frac_str} = {prob:.4f} ({fmt(prob_pct, 2)}%)."
                ],
                "insights": "Each individual card in a well-shuffled 52-card deck has an equal independent draw probability of 1/52 ≈ 1.923%.",
                "raw": prob
            }

    # --------------------------------------------------------------------------
    # Urn / Balls in Bag Probability: e.g. "5 red and 3 green balls"
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:balls?|marbles?|bag|urn)\b', q) and len(raw_nums) >= 2:
        n1, n2 = raw_nums[0], raw_nums[1]
        tot = n1 + n2
        prob = n1 / tot
        g = math.gcd(int(n1), int(tot))
        frac_str = f"{int(n1)//g}/{int(tot)//g}"
        
        return {
            "title": "Probability: Urn / Colored Balls Draw",
            "summary_value": f"{frac_str} ({fmt(prob*100, 2)}%)",
            "formula": "P(Target Color) = (Target Color Balls) ÷ (Total Balls)",
            "rows": [
                ["Probability", f"{frac_str} ({fmt(prob*100, 2)}%)"],
                ["Target Balls", fmt(n1)],
                ["Other Balls", fmt(n2)],
                ["Total Balls in Bag", fmt(tot)]
            ],
            "steps": [
                f"Step 1: Total balls in container = {fmt(n1)} + {fmt(n2)} = {fmt(tot)} balls.",
                f"Step 2: Number of favorable target balls = {fmt(n1)}.",
                f"Step 3: Probability = {fmt(n1)} ÷ {fmt(tot)} = {frac_str} ({fmt(prob*100, 2)}%)."
            ],
            "insights": "In sampling without replacement, probabilities change dynamically with each subsequent draw.",
            "raw": prob
        }

    return None


# ==============================================================================
# 5. PROGRESSIVE COMMERCIAL MATH: MARKED PRICE, DISCOUNTS & MARGIN VS MARKUP
# ==============================================================================
def solve_profit_loss_advanced(query: str) -> Optional[Dict[str, Any]]:
    """Solves advanced commercial math:
    - Marked price, Cost price, and Discounts
    - Margin vs Markup comparisons:
      Markup % = (MP or SP − CP) / CP * 100
      Margin % = (SP − CP) / SP * 100
    - Multi-discount successive combinations: d1%, d2%, d3%
    - Finding Cost Price when Selling Price and Profit% are known
    """
    q = normalize_query(query).lower()
    if not re.search(r'\b(?:marked price|markup|margin|successive discounts?|discount|cp|sp|mp|chhut|faida|khareeda|becha|profit percentage|loss percentage)\b', q):
        return None

    raw_nums = extract_numbers(q)
    
    # --------------------------------------------------------------------------
    # Three or more successive discounts: e.g. "discounts of 20%, 10% and 5%"
    # --------------------------------------------------------------------------
    if re.search(r'successive', q) and len(raw_nums) >= 2:
        discounts = raw_nums[:4]
        # Equivalent discount: 1 - product(1 - d/100)
        rem_factor = 1.0
        for d in discounts:
            rem_factor *= (1.0 - (d / 100.0))
        equiv_discount = (1.0 - rem_factor) * 100.0
        
        return {
            "title": f"Successive Discounts ({len(discounts)} Tier Discounting)",
            "summary_value": f"Single Equivalent Discount = {fmt(equiv_discount, 2)}%",
            "formula": "Equivalent Discount = [1 − (1 − d₁)(1 − d₂) ... (1 − dₙ)] × 100",
            "rows": [
                ["Single Equivalent Discount", f"{fmt(equiv_discount, 2)}%"],
                ["Remaining Price Factor", f"{rem_factor * 100:.2f}% of Original"],
                ["Individual Discounts", ", ".join([f"{d}%" for d in discounts])]
            ],
            "steps": [
                f"Step 1: Assume initial reference list price = ₹100.",
                f"Step 2: Multiplicative remainder factor = " + " × ".join([f"(1 − {d}/100)" for d in discounts]) + f" = {rem_factor:.4f}.",
                f"Step 3: Final price after discounts = ₹100 × {rem_factor:.4f} = ₹{rem_factor*100:.2f}.",
                f"Step 4: Net equivalent single discount = 100 − {rem_factor*100:.2f} = {fmt(equiv_discount, 2)}%."
            ],
            "insights": "Successive discounts are compounding; a 20% + 10% discount gives 28% total discount, not 30%.",
            "raw": equiv_discount
        }

    # --------------------------------------------------------------------------
    # Markup on CP and Discount on MP -> Net Profit %
    # e.g., "marks goods 40% above cost price and allows 20% discount. Find profit %"
    # --------------------------------------------------------------------------
    markup_m = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:above|markup|more than cp)', q)
    discount_m = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:discount|chhut|off)', q)
    
    if markup_m and discount_m:
        m_pct = float(markup_m.group(1))
        d_pct = float(discount_m.group(1))
        
        # Let CP = 100
        # MP = 100 * (1 + m_pct/100)
        # SP = MP * (1 - d_pct/100)
        # Profit% = SP - 100
        mp_factor = 1.0 + (m_pct / 100.0)
        sp_factor = mp_factor * (1.0 - (d_pct / 100.0))
        net_profit_pct = (sp_factor - 1.0) * 100.0
        
        is_profit = net_profit_pct >= 0
        state = "Profit (Gain)" if is_profit else "Loss"
        
        return {
            "title": f"Commercial Math: Markup + Discount ⟹ Net {state}",
            "summary_value": f"Net {state}: {fmt(abs(net_profit_pct), 2)}%",
            "formula": "Profit % = [Markup − Discount − (Markup × Discount) ÷ 100]",
            "rows": [
                [f"Net {state} Percentage", f"{fmt(abs(net_profit_pct), 2)}%"],
                ["Markup above CP", f"{m_pct}%"],
                ["Discount on MP", f"{d_pct}%"],
                ["Effective Price Index", f"{sp_factor * 100:.2f}% of CP"]
            ],
            "steps": [
                "Step 1: Let Cost Price (CP) = ₹100.",
                f"Step 2: Marked Price (MP) = 100 + {m_pct}% of 100 = ₹{mp_factor*100:.2f}.",
                f"Step 3: Selling Price after {d_pct}% discount on MP = ₹{mp_factor*100:.2f} × (1 − {d_pct}/100) = ₹{sp_factor*100:.2f}.",
                f"Step 4: Net Gain / Loss = SP − CP = {sp_factor*100:.2f} − 100 = {fmt(net_profit_pct, 2)}%."
            ],
            "insights": "Net profit percentage from markup M and discount D equals: M − D − (M × D) / 100.",
            "raw": net_profit_pct
        }

    # --------------------------------------------------------------------------
    # Markup vs Margin Comparison
    # e.g., "cost price 500, selling price 650. Find markup and margin"
    # --------------------------------------------------------------------------
    if len(raw_nums) >= 2 and re.search(r'\b(?:markup|margin)\b', q):
        val1, val2 = raw_nums[0], raw_nums[1]
        cp = min(val1, val2)
        sp = max(val1, val2)
        diff = sp - cp
        
        markup_pct = (diff / cp) * 100.0
        margin_pct = (diff / sp) * 100.0
        
        return {
            "title": "Commercial Analysis: Markup vs Margin",
            "summary_value": f"Markup = {fmt(markup_pct, 2)}% · Margin = {fmt(margin_pct, 2)}%",
            "formula": "Markup % = (Profit ÷ CP) × 100,  Margin % = (Profit ÷ SP) × 100",
            "rows": [
                ["Markup Percentage (on CP)", f"{fmt(markup_pct, 2)}%"],
                ["Profit Margin (on SP)", f"{fmt(margin_pct, 2)}%"],
                ["Absolute Profit", fmt_curr(diff)],
                ["Cost Price (CP)", fmt_curr(cp)],
                ["Selling Price (SP)", fmt_curr(sp)]
            ],
            "steps": [
                f"Step 1: Cost Price (CP) = {fmt_curr(cp)}, Selling Price (SP) = {fmt_curr(sp)}.",
                f"Step 2: Gross Profit = SP − CP = {fmt_curr(sp)} − {fmt_curr(cp)} = {fmt_curr(diff)}.",
                f"Step 3: Markup % (relative to CP) = (Profit ÷ CP) × 100 = ({diff} ÷ {cp}) × 100 = {fmt(markup_pct, 2)}%.",
                f"Step 4: Profit Margin % (relative to SP) = (Profit ÷ SP) × 100 = ({diff} ÷ {sp}) × 100 = {fmt(margin_pct, 2)}%."
            ],
            "insights": "Margin is always strictly smaller than markup for any profitable transaction: Margin = Markup / (1 + Markup).",
            "raw": margin_pct
        }

    # --------------------------------------------------------------------------
    # Finding Cost Price when SP and Profit% or Loss% are given
    # e.g., "sold for 1500 with 25% profit. Find cost price"
    # --------------------------------------------------------------------------
    sp_m = re.search(r'(?:sold (?:for|at)|selling price|sp|becha)\s*(?:=|is|:)?\s*(\d+(?:\.\d+)?)', q)
    p_pct_m = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:profit|gain|faida)', q)
    l_pct_m = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:loss|nuksan)', q)
    
    if sp_m and (p_pct_m or l_pct_m):
        sp_val = float(sp_m.group(1))
        if p_pct_m:
            p_val = float(p_pct_m.group(1))
            cp_val = sp_val / (1.0 + (p_val / 100.0))
            profit_amt = sp_val - cp_val
            return {
                "title": f"Cost Price Determination (Sold with {p_val}% Profit)",
                "summary_value": f"Cost Price = {fmt_curr(cp_val)}",
                "formula": "CP = SP ÷ (1 + Profit% / 100)",
                "rows": [
                    ["Calculated Cost Price (CP)", fmt_curr(cp_val)],
                    ["Selling Price (SP)", fmt_curr(sp_val)],
                    ["Profit Percentage", f"{p_val}%"],
                    ["Absolute Profit", fmt_curr(profit_amt)]
                ],
                "steps": [
                    f"Step 1: Selling Price SP = {fmt_curr(sp_val)}, Profit Rate = {p_val}%.",
                    f"Step 2: Relation: SP = CP × (1 + {p_val}/100) = CP × {1.0 + p_val/100:.2f}.",
                    f"Step 3: Cost Price CP = SP ÷ {1.0 + p_val/100:.2f} = {sp_val} ÷ {1.0 + p_val/100:.2f} = {fmt_curr(cp_val)}."
                ],
                "insights": "Profit percentage is based on Cost Price; thus SP represents (100 + P)% of the original CP.",
                "raw": cp_val
            }
        else:
            l_val = float(l_pct_m.group(1))
            cp_val = sp_val / (1.0 - (l_val / 100.0))
            loss_amt = cp_val - sp_val
            return {
                "title": f"Cost Price Determination (Sold with {l_val}% Loss)",
                "summary_value": f"Cost Price = {fmt_curr(cp_val)}",
                "formula": "CP = SP ÷ (1 − Loss% / 100)",
                "rows": [
                    ["Calculated Cost Price (CP)", fmt_curr(cp_val)],
                    ["Selling Price (SP)", fmt_curr(sp_val)],
                    ["Loss Percentage", f"{l_val}%"],
                    ["Absolute Loss Amount", fmt_curr(loss_amt)]
                ],
                "steps": [
                    f"Step 1: Selling Price SP = {fmt_curr(sp_val)}, Loss Rate = {l_val}%.",
                    f"Step 2: Relation: SP = CP × (1 − {l_val}/100) = CP × {1.0 - l_val/100:.2f}.",
                    f"Step 3: Cost Price CP = SP ÷ {1.0 - l_val/100:.2f} = {sp_val} ÷ {1.0 - l_val/100:.2f} = {fmt_curr(cp_val)}."
                ],
                "insights": "In a loss scenario, Cost Price is always higher than Selling Price: CP = SP / (1 - L/100).",
                "raw": cp_val
            }

    return None
