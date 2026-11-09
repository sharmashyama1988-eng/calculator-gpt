"""Geometry & Mensuration Engine for Calculator GPT.
Provides exact symbolic and high-precision numerical computations for 2D and 3D shapes:
Spheres, Hemispheres, Cylinders, Cones, Cuboids, Cubes, Ellipses, Trapezoids,
Right Triangles (Pythagoras), Circles, and Sectors.
Returns rich structured cards with formulas, step-by-step reasoning, and tabular rows.
"""

import math
import re
from typing import Dict, Any, List, Optional
import sympy as sp
from .nlp_parser import normalize_query, extract_numbers


def fmt(n: float, decimals: int = 3) -> str:
    """Formats numeric values cleanly."""
    if not math.isfinite(n):
        return "Undefined"
    if n == int(n):
        return f"{int(n):,}"
    formatted = f"{n:,.{decimals}f}".rstrip('0').rstrip('.')
    return formatted


def extract_labeled_dimensions(text: str) -> Dict[str, float]:
    """Extracts named parameters like radius, height, length, width, etc."""
    q = text.lower()
    dims = {}
    
    patterns = {
        'radius': [r'\b(?:radius|rad|r)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:cm|m|mm)?\s*\b(?:radius|rad)\b'],
        'diameter': [r'\b(?:diameter|dia|d)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:cm|m|mm)?\s*\b(?:diameter|dia)\b'],
        'height': [r'\b(?:height|ht|depth|gehrai|unchai|h)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:cm|m|mm)?\s*\b(?:height|high)\b'],
        'length': [r'\b(?:length|len|lamba|l)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:cm|m|mm)?\s*\b(?:length|long)\b'],
        'width': [r'\b(?:width|breadth|chaudai|b|w)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:cm|m|mm)?\s*\b(?:wide|broad|width|breadth)\b'],
        'slant_height': [r'\b(?:slant height|slant|tirchi unchai|l)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)'],
        'side': [r'\b(?:side|edge|bhuja|a)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:cm|m|mm)?\s*\b(?:side|edge)\b'],
        'base': [r'\b(?:base|aadhar)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)'],
        'hypotenuse': [r'\b(?:hypotenuse|hyp|karna)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)'],
        'angle': [r'\b(?:angle|theta|degree|deg)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*(?:°|degrees?|deg)\b'],
        'major': [r'\b(?:semi[- ]?major(?: axis)?|major axis|a)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)'],
        'minor': [r'\b(?:semi[- ]?minor(?: axis)?|minor axis|b)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)'],
        'parallel1': [r'\b(?:parallel side 1|parallel side a|first parallel side|a)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)'],
        'parallel2': [r'\b(?:parallel side 2|parallel side b|second parallel side|b)\b\s*(?:=|is|of|:)?\s*(\d+(?:\.\d+)?)']
    }
    
    for key, p_list in patterns.items():
        for pat in p_list:
            m = re.search(pat, q)
            if m:
                try:
                    dims[key] = float(m.group(1))
                    break
                except ValueError:
                    pass
                    
    return dims


def solve_geometry(query: str) -> Optional[Dict[str, Any]]:
    """Master Geometry & Mensuration solver covering 2D and 3D geometric entities."""
    q = normalize_query(query).lower()
    raw_nums = extract_numbers(q)
    dims = extract_labeled_dimensions(q)
    
    # --------------------------------------------------------------------------
    # 1. SPHERE & HEMISPHERE
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:sphere|gola|hemisphere|ardhgola)\b', q):
        is_hemi = bool(re.search(r'\b(?:hemisphere|ardhgola|half sphere)\b', q))
        r = dims.get('radius')
        if r is None and dims.get('diameter'):
            r = dims['diameter'] / 2.0
        if r is None and len(raw_nums) >= 1:
            r = raw_nums[0]
            
        if r is not None and r > 0:
            if not is_hemi:
                vol = (4.0 / 3.0) * math.pi * (r ** 3)
                sa = 4.0 * math.pi * (r ** 2)
                return {
                    "title": f"Sphere Mensuration (Radius r = {fmt(r)})",
                    "summary_value": f"Volume = {fmt(vol)} · Surface Area = {fmt(sa)}",
                    "formula": "Volume = ⁴⁄₃πr³,  Surface Area = 4πr²",
                    "rows": [
                        ["Volume (⁴⁄₃πr³)", fmt(vol)],
                        ["Total Surface Area (4πr²)", fmt(sa)],
                        ["Radius (r)", fmt(r)],
                        ["Diameter (2r)", fmt(2 * r)],
                        ["Circumference of Great Circle (2πr)", fmt(2 * math.pi * r)]
                    ],
                    "steps": [
                        f"Step 1: Identify Sphere Radius: r = {fmt(r)} (Diameter d = {fmt(2*r)})",
                        f"Step 2: Volume V = (4/3) × π × r³ = (4/3) × π × ({fmt(r)})³ = (4/3) × π × {fmt(r**3)} = {fmt(vol)} cubic units.",
                        f"Step 3: Surface Area A = 4 × π × r² = 4 × π × ({fmt(r)})² = 4 × π × {fmt(r**2)} = {fmt(sa)} square units."
                    ],
                    "insights": "A sphere has the minimum surface area among all 3D shapes enclosing a given fixed volume.",
                    "raw": vol
                }
            else:
                vol = (2.0 / 3.0) * math.pi * (r ** 3)
                csa = 2.0 * math.pi * (r ** 2)
                tsa = 3.0 * math.pi * (r ** 2)
                return {
                    "title": f"Hemisphere Mensuration (Radius r = {fmt(r)})",
                    "summary_value": f"Volume = {fmt(vol)} · TSA = {fmt(tsa)} · CSA = {fmt(csa)}",
                    "formula": "Volume = ²⁄₃πr³,  CSA = 2πr²,  TSA = 3πr²",
                    "rows": [
                        ["Volume (²⁄₃πr³)", fmt(vol)],
                        ["Total Surface Area TSA (3πr²)", fmt(tsa)],
                        ["Curved Surface Area CSA (2πr²)", fmt(csa)],
                        ["Flat Circular Base Area (πr²)", fmt(math.pi * r * r)],
                        ["Radius (r)", fmt(r)]
                    ],
                    "steps": [
                        f"Step 1: Given hemisphere radius: r = {fmt(r)}",
                        f"Step 2: Volume = (2/3) × π × r³ = (2/3) × π × {fmt(r**3)} = {fmt(vol)}",
                        f"Step 3: Curved Surface Area (CSA) = 2 × π × r² = 2 × π × {fmt(r**2)} = {fmt(csa)}",
                        f"Step 4: Total Surface Area (TSA) = CSA + Base Area = 2πr² + πr² = 3πr² = {fmt(tsa)}"
                    ],
                    "insights": "Total surface area of a solid hemisphere includes both the curved dome (2πr²) and the flat circular bottom (πr²).",
                    "raw": vol
                }

    # --------------------------------------------------------------------------
    # 2. CYLINDER (Right Circular Cylinder)
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:cylinder|belan|cylindrical)\b', q):
        r = dims.get('radius')
        h = dims.get('height')
        if r is None and dims.get('diameter'):
            r = dims['diameter'] / 2.0
            
        if (r is None or h is None) and len(raw_nums) >= 2:
            r = raw_nums[0] if r is None else r
            h = raw_nums[1] if h is None else h
            
        if r is not None and h is not None and r > 0 and h > 0:
            vol = math.pi * (r ** 2) * h
            csa = 2.0 * math.pi * r * h
            tsa = 2.0 * math.pi * r * (h + r)
            base_area = math.pi * (r ** 2)
            
            return {
                "title": f"Cylinder Mensuration (Radius r = {fmt(r)}, Height h = {fmt(h)})",
                "summary_value": f"Volume = {fmt(vol)} · TSA = {fmt(tsa)} · CSA = {fmt(csa)}",
                "formula": "Volume = πr²h,  CSA = 2πrh,  TSA = 2πr(h + r)",
                "rows": [
                    ["Volume (πr²h)", fmt(vol)],
                    ["Curved Surface Area CSA (2πrh)", fmt(csa)],
                    ["Total Surface Area TSA (2πr(h + r))", fmt(tsa)],
                    ["Base Circular Area (πr²)", fmt(base_area)],
                    ["Radius (r)", fmt(r)],
                    ["Height (h)", fmt(h)]
                ],
                "steps": [
                    f"Step 1: Identify dimensions: radius r = {fmt(r)}, height h = {fmt(h)}",
                    f"Step 2: Base Area = π × r² = π × ({fmt(r)})² = {fmt(base_area)}",
                    f"Step 3: Volume V = Base Area × Height = {fmt(base_area)} × {fmt(h)} = {fmt(vol)} cubic units.",
                    f"Step 4: Curved Surface Area CSA = 2 × π × r × h = 2 × π × {fmt(r)} × {fmt(h)} = {fmt(csa)} square units.",
                    f"Step 5: Total Surface Area TSA = CSA + 2 × (Base Area) = {fmt(csa)} + {fmt(2*base_area)} = {fmt(tsa)} square units."
                ],
                "insights": "Unrolling the curved surface of a cylinder forms a rectangle of length 2πr (circumference) and height h.",
                "raw": vol
            }

    # --------------------------------------------------------------------------
    # 3. CONE (Right Circular Cone)
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:cone|shankhu|conical)\b', q):
        r = dims.get('radius')
        h = dims.get('height')
        l = dims.get('slant_height')
        if r is None and dims.get('diameter'):
            r = dims['diameter'] / 2.0
            
        if r is None and len(raw_nums) >= 1:
            r = raw_nums[0]
        if h is None and len(raw_nums) >= 2:
            h = raw_nums[1]
            
        if r is not None and (h is not None or l is not None) and r > 0:
            if l is None and h is not None:
                l = math.sqrt(r * r + h * h)
            elif h is None and l is not None:
                h = math.sqrt(max(0.0, l * l - r * r))
                
            vol = (1.0 / 3.0) * math.pi * (r ** 2) * h
            csa = math.pi * r * l
            tsa = math.pi * r * (l + r)
            
            return {
                "title": f"Cone Mensuration (r = {fmt(r)}, h = {fmt(h)}, l = {fmt(l)})",
                "summary_value": f"Volume = {fmt(vol)} · TSA = {fmt(tsa)} · CSA = {fmt(csa)}",
                "formula": "Volume = ⅓πr²h,  CSA = πrl,  TSA = πr(l + r),  l = √(r² + h²)",
                "rows": [
                    ["Volume (⅓πr²h)", fmt(vol)],
                    ["Curved Surface Area CSA (πrl)", fmt(csa)],
                    ["Total Surface Area TSA (πr(l + r))", fmt(tsa)],
                    ["Slant Height (l = √(r² + h²))", fmt(l)],
                    ["Vertical Height (h)", fmt(h)],
                    ["Base Radius (r)", fmt(r)]
                ],
                "steps": [
                    f"Step 1: Given radius r = {fmt(r)}, height h = {fmt(h)}",
                    f"Step 2: Calculate slant height via Pythagoras: l = √(r² + h²) = √({fmt(r*r)} + {fmt(h*h)}) = {fmt(l)}",
                    f"Step 3: Volume V = (1/3) × π × r² × h = (1/3) × π × {fmt(r*r)} × {fmt(h)} = {fmt(vol)} cubic units.",
                    f"Step 4: Curved Surface Area CSA = π × r × l = π × {fmt(r)} × {fmt(l)} = {fmt(csa)} square units.",
                    f"Step 5: Total Surface Area TSA = CSA + Base Area = {fmt(csa)} + π×{fmt(r)}² = {fmt(tsa)} square units."
                ],
                "insights": "The volume of a cone is exactly one-third of the volume of a cylinder with the same base radius and height.",
                "raw": vol
            }

    # --------------------------------------------------------------------------
    # 4. CUBOID / CUBE / RECTANGULAR PRISM
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:cuboid|cube|rectangular prism|box|ghana|ghanabh)\b', q):
        is_cube = bool(re.search(r'\b(?:cube|ghana)\b', q) and not re.search(r'cuboid|ghanabh', q))
        
        if is_cube:
            a = dims.get('side') or (raw_nums[0] if raw_nums else None)
            if a and a > 0:
                vol = a ** 3
                tsa = 6 * (a ** 2)
                lsa = 4 * (a ** 2)
                diag = a * math.sqrt(3)
                return {
                    "title": f"Cube Mensuration (Side a = {fmt(a)})",
                    "summary_value": f"Volume = {fmt(vol)} · TSA = {fmt(tsa)} · Diagonal = {fmt(diag)}",
                    "formula": "Volume = a³,  TSA = 6a²,  LSA = 4a²,  Space Diagonal = a√3",
                    "rows": [
                        ["Volume (a³)", fmt(vol)],
                        ["Total Surface Area TSA (6a²)", fmt(tsa)],
                        ["Lateral Surface Area LSA (4a²)", fmt(lsa)],
                        ["Space Diagonal (a√3)", fmt(diag)],
                        ["Side Length (a)", fmt(a)]
                    ],
                    "steps": [
                        f"Step 1: Given cube side edge: a = {fmt(a)}",
                        f"Step 2: Volume V = a³ = ({fmt(a)})³ = {fmt(vol)} cubic units.",
                        f"Step 3: Total Surface Area = 6 × a² = 6 × {fmt(a*a)} = {fmt(tsa)} square units.",
                        f"Step 4: Lateral Surface Area (4 walls) = 4 × a² = {fmt(lsa)} square units.",
                        f"Step 5: Space diagonal = a × √3 = {fmt(a)} × 1.73205 = {fmt(diag)} units."
                    ],
                    "insights": "A cube is a regular hexahedron with 6 congruent square faces, 12 equal edges, and 8 vertices.",
                    "raw": vol
                }
        else:
            # Cuboid (Length, Width, Height)
            l = dims.get('length')
            w = dims.get('width')
            h = dims.get('height')
            
            if (l is None or w is None or h is None) and len(raw_nums) >= 3:
                l = raw_nums[0] if l is None else l
                w = raw_nums[1] if w is None else w
                h = raw_nums[2] if h is None else h
                
            if l and w and h and l > 0 and w > 0 and h > 0:
                vol = l * w * h
                tsa = 2 * (l * w + w * h + h * l)
                lsa = 2 * h * (l + w)
                diag = math.sqrt(l * l + w * w + h * h)
                
                return {
                    "title": f"Cuboid Mensuration (L = {fmt(l)}, W = {fmt(w)}, H = {fmt(h)})",
                    "summary_value": f"Volume = {fmt(vol)} · TSA = {fmt(tsa)} · Diagonal = {fmt(diag)}",
                    "formula": "Volume = l·w·h,  TSA = 2(lw + wh + hl),  LSA = 2h(l + w),  Diagonal = √(l² + w² + h²)",
                    "rows": [
                        ["Volume (l × w × h)", fmt(vol)],
                        ["Total Surface Area (TSA)", fmt(tsa)],
                        ["Lateral Surface Area / 4 Walls (LSA)", fmt(lsa)],
                        ["Space Diagonal", fmt(diag)],
                        ["Length (l)", fmt(l)],
                        ["Width / Breadth (w)", fmt(w)],
                        ["Height (h)", fmt(h)]
                    ],
                    "steps": [
                        f"Step 1: Identify dimensions: Length l = {fmt(l)}, Width w = {fmt(w)}, Height h = {fmt(h)}",
                        f"Step 2: Volume = l × w × h = {fmt(l)} × {fmt(w)} × {fmt(h)} = {fmt(vol)} cubic units.",
                        f"Step 3: TSA = 2(lw + wh + hl) = 2({fmt(l*w)} + {fmt(w*h)} + {fmt(h*l)}) = {fmt(tsa)} square units.",
                        f"Step 4: LSA (Area of 4 vertical walls) = 2h(l + w) = 2({fmt(h)})({fmt(l+w)}) = {fmt(lsa)} square units.",
                        f"Step 5: Longest rod / Space diagonal = √(l² + w² + h²) = √({fmt(l*l + w*w + h*h)}) = {fmt(diag)} units."
                    ],
                    "insights": "The space diagonal represents the maximum straight-line length that can fit inside the cuboid.",
                    "raw": vol
                }

    # --------------------------------------------------------------------------
    # 5. ELLIPSE
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:ellipse|elliptical|deerghavritta)\b', q):
        a = dims.get('major')
        b = dims.get('minor')
        if (a is None or b is None) and len(raw_nums) >= 2:
            a = max(raw_nums[0], raw_nums[1])
            b = min(raw_nums[0], raw_nums[1])
            
        if a and b and a > 0 and b > 0:
            area = math.pi * a * b
            # Ramanujan's high-precision approximation for perimeter
            h_val = ((a - b) ** 2) / ((a + b) ** 2)
            peri = math.pi * (a + b) * (1 + (3 * h_val) / (10 + math.sqrt(4 - 3 * h_val)))
            eccentricity = math.sqrt(1 - (b * b) / (a * a)) if a >= b else math.sqrt(1 - (a * a) / (b * b))
            
            return {
                "title": f"Ellipse Geometry (Semi-major a = {fmt(a)}, Semi-minor b = {fmt(b)})",
                "summary_value": f"Area = {fmt(area)} · Perimeter ≈ {fmt(peri)} · Eccentricity e = {fmt(eccentricity)}",
                "formula": "Area = πab,  Perimeter ≈ π(a + b)[1 + 3h / (10 + √(4 − 3h))],  e = √(1 − b²/a²)",
                "rows": [
                    ["Area (π × a × b)", fmt(area)],
                    ["Perimeter (Ramanujan Approximation)", fmt(peri)],
                    ["Eccentricity (e)", fmt(eccentricity)],
                    ["Semi-major Axis (a)", fmt(a)],
                    ["Semi-minor Axis (b)", fmt(b)],
                    ["Focal Distance (c = √(a² − b²))", fmt(math.sqrt(abs(a*a - b*b)))]
                ],
                "steps": [
                    f"Step 1: Given semi-major axis a = {fmt(a)}, semi-minor axis b = {fmt(b)}",
                    f"Step 2: Area = π × a × b = π × {fmt(a)} × {fmt(b)} = {fmt(area)} square units.",
                    f"Step 3: Ramanujan's Perimeter Formula: h = (a − b)² / (a + b)² = {fmt(h_val, 5)}",
                    f"Step 4: Perimeter P ≈ π(a + b)(1 + 3h / (10 + √(4 − 3h))) = {fmt(peri)} units.",
                    f"Step 5: Eccentricity e = √(1 − b²/a²) = {fmt(eccentricity)} (Degree of elongation: 0 is circle, 1 is parabola)."
                ],
                "insights": "Planetary orbits around the Sun follow Kepler's first law as ellipses with the Sun at one focus.",
                "raw": area
            }

    # --------------------------------------------------------------------------
    # 6. TRAPEZOID / TRAPEZIUM
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:trapezoid|trapezium|samlamb|samlamba)\b', q):
        h = dims.get('height')
        a = dims.get('parallel1')
        b = dims.get('parallel2')
        
        if (a is None or b is None or h is None) and len(raw_nums) >= 3:
            # Usually parallel sides a, b and height h
            a = raw_nums[0] if a is None else a
            b = raw_nums[1] if b is None else b
            h = raw_nums[2] if h is None else h
            
        if a and b and h and a > 0 and b > 0 and h > 0:
            area = 0.5 * (a + b) * h
            return {
                "title": f"Trapezoid Geometry (Parallel Sides: {fmt(a)}, {fmt(b)}, Height: {fmt(h)})",
                "summary_value": f"Area = {fmt(area)}",
                "formula": "Area = ½ × (a + b) × h",
                "rows": [
                    ["Area of Trapezoid", fmt(area)],
                    ["Parallel Side a", fmt(a)],
                    ["Parallel Side b", fmt(b)],
                    ["Perpendicular Height (h)", fmt(h)],
                    ["Average Parallel Width ((a + b) / 2)", fmt((a + b) / 2)]
                ],
                "steps": [
                    f"Step 1: Identify parallel bases: a = {fmt(a)}, b = {fmt(b)}, distance between them h = {fmt(h)}",
                    f"Step 2: Sum of parallel sides = a + b = {fmt(a)} + {fmt(b)} = {fmt(a + b)}",
                    f"Step 3: Apply formula: Area = 1/2 × (sum of parallel sides) × height",
                    f"Step 4: Area = 0.5 × {fmt(a + b)} × {fmt(h)} = {fmt(area)} square units."
                ],
                "insights": "The area of a trapezoid equals the average of its parallel bases multiplied by its vertical height.",
                "raw": area
            }

    # --------------------------------------------------------------------------
    # 7. RIGHT TRIANGLE & PYTHAGOREAN THEOREM
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:right triangle|pythagoras|pythagorean|hypotenuse|karna|samkon)\b', q):
        hyp = dims.get('hypotenuse')
        base = dims.get('base') or dims.get('length')
        height = dims.get('height')
        
        if hyp is None and base is None and height is None and len(raw_nums) >= 2:
            base, height = raw_nums[0], raw_nums[1]
            
        if base and height and hyp is None and base > 0 and height > 0:
            hyp = math.hypot(base, height)
            area = 0.5 * base * height
            peri = base + height + hyp
            return {
                "title": f"Right Triangle (Base = {fmt(base)}, Perpendicular = {fmt(height)})",
                "summary_value": f"Hypotenuse c = {fmt(hyp)} · Area = {fmt(area)} · Perimeter = {fmt(peri)}",
                "formula": "c = √(a² + b²),  Area = ½ × a × b,  Perimeter = a + b + c",
                "rows": [
                    ["Hypotenuse (c)", fmt(hyp)],
                    ["Area (½ · a · b)", fmt(area)],
                    ["Perimeter (a + b + c)", fmt(peri)],
                    ["Base (a)", fmt(base)],
                    ["Perpendicular / Altitude (b)", fmt(height)]
                ],
                "steps": [
                    f"Step 1: Given legs: a = {fmt(base)}, b = {fmt(height)}",
                    f"Step 2: Pythagorean theorem: c² = a² + b² = ({fmt(base)})² + ({fmt(height)})² = {fmt(base*base)} + {fmt(height*height)} = {fmt(base*base + height*height)}",
                    f"Step 3: Hypotenuse c = √({fmt(base*base + height*height)}) = {fmt(hyp)} units.",
                    f"Step 4: Area = 1/2 × {fmt(base)} × {fmt(height)} = {fmt(area)} square units.",
                    f"Step 5: Perimeter = {fmt(base)} + {fmt(height)} + {fmt(hyp)} = {fmt(peri)} units."
                ],
                "insights": "In any Euclidean right-angled triangle, the square of the hypotenuse is strictly equal to the sum of the squares of the other two sides.",
                "raw": hyp
            }
        elif hyp and (base or height) and hyp > 0:
            known = base if base else height
            if hyp > known:
                other = math.sqrt(hyp * hyp - known * known)
                area = 0.5 * known * other
                peri = known + other + hyp
                return {
                    "title": f"Right Triangle Missing Leg (Hypotenuse = {fmt(hyp)}, Known Leg = {fmt(known)})",
                    "summary_value": f"Missing Leg = {fmt(other)} · Area = {fmt(area)}",
                    "formula": "b = √(c² − a²),  Area = ½ × a × b",
                    "rows": [
                        ["Calculated Missing Leg", fmt(other)],
                        ["Hypotenuse (c)", fmt(hyp)],
                        ["Given Leg", fmt(known)],
                        ["Area of Triangle", fmt(area)],
                        ["Perimeter", fmt(peri)]
                    ],
                    "steps": [
                        f"Step 1: Known hypotenuse c = {fmt(hyp)} and leg a = {fmt(known)}",
                        f"Step 2: Apply Pythagoras: b² = c² − a² = {fmt(hyp*hyp)} − {fmt(known*known)} = {fmt(hyp*hyp - known*known)}",
                        f"Step 3: Missing leg b = √({fmt(hyp*hyp - known*known)}) = {fmt(other)} units.",
                        f"Step 4: Area = 1/2 × {fmt(known)} × {fmt(other)} = {fmt(area)} square units."
                    ],
                    "insights": "When the hypotenuse is known, subtract the square of the known leg to find the square of the remaining leg.",
                    "raw": other
                }

    # --------------------------------------------------------------------------
    # 8. CIRCLE & SECTOR
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:circle|vritta|circular|sector)\b', q):
        r = dims.get('radius')
        if r is None and dims.get('diameter'):
            r = dims['diameter'] / 2.0
        if r is None and raw_nums:
            r = raw_nums[0]
            
        theta = dims.get('angle')
        if theta is None and 'sector' in q and len(raw_nums) >= 2:
            theta = raw_nums[1]
            
        if r and r > 0:
            area = math.pi * (r ** 2)
            circ = 2 * math.pi * r
            
            if theta and theta > 0:
                arc_len = (theta / 360.0) * circ
                sector_area = (theta / 360.0) * area
                return {
                    "title": f"Circular Sector (Radius r = {fmt(r)}, Angle θ = {fmt(theta)}°)",
                    "summary_value": f"Sector Area = {fmt(sector_area)} · Arc Length = {fmt(arc_len)}",
                    "formula": "Sector Area = (θ/360) × πr²,  Arc Length = (θ/360) × 2πr",
                    "rows": [
                        ["Sector Area", fmt(sector_area)],
                        ["Arc Length", fmt(arc_len)],
                        ["Full Circle Area", fmt(area)],
                        ["Full Circumference", fmt(circ)],
                        ["Central Angle (θ)", f"{fmt(theta)}°"],
                        ["Radius (r)", fmt(r)]
                    ],
                    "steps": [
                        f"Step 1: Circle radius r = {fmt(r)}, central angle θ = {fmt(theta)}°",
                        f"Step 2: Total Circle Area = π × r² = π × ({fmt(r)})² = {fmt(area)}",
                        f"Step 3: Sector Fraction = θ / 360° = {fmt(theta)} / 360 = {fmt(theta/360, 4)}",
                        f"Step 4: Sector Area = ({fmt(theta)}/360) × {fmt(area)} = {fmt(sector_area)} square units.",
                        f"Step 5: Arc Length = ({fmt(theta)}/360) × 2πr = {fmt(arc_len)} units."
                    ],
                    "insights": "A sector is the portion of a disk enclosed by two radii and an arc.",
                    "raw": sector_area
                }
            else:
                return {
                    "title": f"Circle Geometry (Radius r = {fmt(r)})",
                    "summary_value": f"Area = {fmt(area)} · Circumference = {fmt(circ)}",
                    "formula": "Area = πr²,  Circumference = 2πr,  Diameter = 2r",
                    "rows": [
                        ["Area (πr²)", fmt(area)],
                        ["Circumference (2πr)", fmt(circ)],
                        ["Radius (r)", fmt(r)],
                        ["Diameter (2r)", fmt(2 * r)]
                    ],
                    "steps": [
                        f"Step 1: Given radius: r = {fmt(r)} (Diameter d = {fmt(2*r)})",
                        f"Step 2: Area = π × r² = π × ({fmt(r)})² = π × {fmt(r*r)} = {fmt(area)} square units.",
                        f"Step 3: Circumference = 2 × π × r = 2 × π × {fmt(r)} = {fmt(circ)} units."
                    ],
                    "insights": "The ratio of a circle's circumference to its diameter is the mathematical constant π ≈ 3.14159265.",
                    "raw": area
                }

    # --------------------------------------------------------------------------
    # 9. GENERAL TRIANGLE (Heron's Formula or Base/Height)
    # --------------------------------------------------------------------------
    if re.search(r'\b(?:triangle|tribhuj)\b', q) and not re.search(r'right', q):
        if len(raw_nums) >= 3:
            # Three sides: Heron's formula
            a, b, c = raw_nums[0], raw_nums[1], raw_nums[2]
            if a + b > c and a + c > b and b + c > a:
                s = (a + b + c) / 2.0
                area = math.sqrt(s * (s - a) * (s - b) * (s - c))
                peri = a + b + c
                return {
                    "title": f"Triangle Geometry via Heron's Formula (Sides: {fmt(a)}, {fmt(b)}, {fmt(c)})",
                    "summary_value": f"Area = {fmt(area)} · Perimeter = {fmt(peri)}",
                    "formula": "Area = √(s(s − a)(s − b)(s − c)) where s = (a + b + c) / 2",
                    "rows": [
                        ["Area (Heron's Formula)", fmt(area)],
                        ["Perimeter", fmt(peri)],
                        ["Semi-perimeter (s)", fmt(s)],
                        ["Side a", fmt(a)],
                        ["Side b", fmt(b)],
                        ["Side c", fmt(c)]
                    ],
                    "steps": [
                        f"Step 1: Verify Triangle Inequality: {a}+{b} > {c}, {a}+{c} > {b}, {b}+{c} > {a} (Valid triangle).",
                        f"Step 2: Semi-perimeter s = ({a} + {b} + {c}) / 2 = {fmt(s)}",
                        f"Step 3: Differences: (s − a) = {fmt(s-a)}, (s − b) = {fmt(s-b)}, (s − c) = {fmt(s-c)}",
                        f"Step 4: Area = √({fmt(s)} × {fmt(s-a)} × {fmt(s-b)} × {fmt(s-c)}) = √({fmt(s*(s-a)*(s-b)*(s-c))}) = {fmt(area)} square units."
                    ],
                    "insights": "Heron's formula allows exact calculation of any triangle's area using exclusively its three side lengths.",
                    "raw": area
                }
        elif len(raw_nums) >= 2:
            b, h = raw_nums[0], raw_nums[1]
            area = 0.5 * b * h
            return {
                "title": f"Triangle Geometry (Base = {fmt(b)}, Height = {fmt(h)})",
                "summary_value": f"Area = {fmt(area)}",
                "formula": "Area = ½ × Base × Height",
                "rows": [
                    ["Area of Triangle", fmt(area)],
                    ["Base", fmt(b)],
                    ["Height", fmt(h)]
                ],
                "steps": [
                    f"Step 1: Given base = {fmt(b)}, height = {fmt(h)}",
                    f"Step 2: Area = 1/2 × {fmt(b)} × {fmt(h)} = {fmt(area)} square units."
                ],
                "insights": "Any triangle's area is half of the area of a parallelogram with the same base and height.",
                "raw": area
            }

    return None
