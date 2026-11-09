"""Comprehensive AI-Level Verification Test Suite for Calculator GPT.
Tests all newly added mathematical reasoning domains:
1. Geometry & Mensuration (2D & 3D Shapes: Sphere, Cylinder, Cone, Cuboid, Ellipse, Trapezoid, Right Triangle)
2. Advanced Quantitative Aptitude:
   - Boats & Streams (Upstream, Downstream, Still water speed, Current)
   - Pipes & Cisterns (Inlets, Outlets, Tank leaks)
   - Mixtures & Alligation (Repeated dilution, Rule of Alligation)
   - Probability & Combinatorics (Coin toss, Dice, 52-card deck, Balls/Urn)
   - Progressive Profit & Loss (Markup, Margin, Successive discounts, Cost price determination)
3. Advanced CAS & Higher Mathematics:
   - Extrema & Optimization (Local Minima, Maxima, Inflection points)
   - Linear Algebra (Determinant, Inverse, Trace, Eigenvalues, Eigenvectors)
   - Complex Numbers (Modulus, Argument, Conjugate, Polar form)
   - Differential Equations (1st Order ODEs with and without initial conditions)
4. Conversational English & Hinglish Natural Language Understanding
"""

import sys
from engine.master_solver import solve_query, process_all_queries


test_cases = [
    # --- 1. GEOMETRY & MENSURATION ---
    {
        "domain": "Geometry: Sphere",
        "query": "volume and surface area of a sphere with radius 6",
        "expected_in_title": "Sphere Mensuration",
        "verify": lambda r: "904.779" in r["summary_value"] and "452.389" in r["summary_value"]
    },
    {
        "domain": "Geometry: Cylinder",
        "query": "what is the volume of a cylinder with radius 7 and height 14",
        "expected_in_title": "Cylinder Mensuration",
        "verify": lambda r: "2,155.133" in r["summary_value"] and len(r["steps"]) >= 4
    },
    {
        "domain": "Geometry: Cone",
        "query": "find volume and surface area of a cone with radius 3 and height 4",
        "expected_in_title": "Cone Mensuration",
        "verify": lambda r: "37.699" in r["summary_value"] and "75.398" in r["summary_value"]
    },
    {
        "domain": "Geometry: Cuboid",
        "query": "calculate volume and diagonal of cuboid with length 12, width 4, height 3",
        "expected_in_title": "Cuboid Mensuration",
        "verify": lambda r: "144" in r["summary_value"] and "13" in r["summary_value"]
    },
    {
        "domain": "Geometry: Ellipse",
        "query": "area and perimeter of ellipse with semi-major axis 5 and semi-minor axis 3",
        "expected_in_title": "Ellipse Geometry",
        "verify": lambda r: "47.124" in r["summary_value"] and "25.527" in r["summary_value"]
    },
    {
        "domain": "Geometry: Trapezoid",
        "query": "area of trapezoid with parallel sides 10 and 16 and height 7",
        "expected_in_title": "Trapezoid Geometry",
        "verify": lambda r: "91" in r["summary_value"]
    },
    {
        "domain": "Geometry: Right Triangle (Pythagoras)",
        "query": "right triangle with hypotenuse 25 and base 15, find missing leg and area",
        "expected_in_title": "Right Triangle Missing Leg",
        "verify": lambda r: "20" in r["summary_value"] and "150" in r["summary_value"]
    },

    # --- 2. ADVANCED QUANTITATIVE APTITUDE ---
    {
        "domain": "Aptitude: Boats & Streams",
        "query": "A boat travels 24 km upstream in 4 hours and 36 km downstream in 3 hours. Find boat and stream speed.",
        "expected_in_title": "Boats & Streams",
        "verify": lambda r: "9 km/h" in r["summary_value"] and "3 km/h" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Boats & Streams (Travel Time)",
        "query": "boat speed in still water is 15 km/h and stream is 3 km/h. How long to travel 36 km downstream?",
        "expected_in_title": "Boats & Streams",
        "verify": lambda r: "2" in r["summary_value"] and "hours" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Pipes & Cisterns (Combined Inlets)",
        "query": "Pipe A fills in 12 hours and Pipe B fills in 18 hours. If both open together, how long to fill?",
        "expected_in_title": "Pipes & Cisterns",
        "verify": lambda r: "7.2" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Pipes & Cisterns (Leak at Bottom)",
        "query": "A tap fills a tank in 8 hours. Due to a leak at the bottom it takes 10 hours. How long for leak alone to empty?",
        "expected_in_title": "Tank Leak Emptiness Time",
        "verify": lambda r: "40 hours" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Mixtures (Repeated Dilution)",
        "query": "A container has 80 liters of pure milk. 8 liters is replaced with water, repeated 2 more times (total 3 times). How much pure milk left?",
        "expected_in_title": "Repeated Dilution",
        "verify": lambda r: "58.32 L" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Mixtures (Rule of Alligation)",
        "query": "In what ratio must tea at 60 per kg be mixed with tea at 80 per kg to get a mixture worth 68 per kg?",
        "expected_in_title": "Rule of Alligation",
        "verify": lambda r: "3 : 2" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Probability (Coin Toss)",
        "query": "probability of getting 2 heads when 3 coins are tossed",
        "expected_in_title": "Probability: Coin Toss",
        "verify": lambda r: "3/8" in r["summary_value"] and "37.5" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Probability (Dice Roll)",
        "query": "probability of getting sum of 7 when two dice are rolled",
        "expected_in_title": "Probability: Two Dice Sum",
        "verify": lambda r: "1/6" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Probability (52-Card Deck)",
        "query": "probability of drawing a face card from a deck of 52 cards",
        "expected_in_title": "Probability: Card Deck",
        "verify": lambda r: "3/13" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Progressive Profit & Loss (Markup + Discount)",
        "query": "A shopkeeper marks goods 40% above cost price and allows 20% discount. Find profit percentage.",
        "expected_in_title": "Commercial Math: Markup + Discount",
        "verify": lambda r: "12%" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Progressive Profit & Loss (Successive Discounts)",
        "query": "successive discounts of 20%, 10% and 5%",
        "expected_in_title": "Successive Discounts",
        "verify": lambda r: "31.6" in r["summary_value"]
    },
    {
        "domain": "Aptitude: Commercial Math (Margin vs Markup)",
        "query": "cost price 500, selling price 650. Find markup and margin",
        "expected_in_title": "Markup vs Margin",
        "verify": lambda r: "30%" in r["summary_value"] and "23.08%" in r["summary_value"]
    },

    # --- 3. ADVANCED CAS & HIGHER MATHEMATICS ---
    {
        "domain": "CAS: Extrema & Optimization",
        "query": "find maximum and minimum of x^3 - 3*x^2 + 2",
        "expected_in_title": "Extrema & Optimization",
        "verify": lambda r: "Local Max at (0, 2)" in r["summary_value"] and "Local Min at (2, -2)" in r["summary_value"]
    },
    {
        "domain": "CAS: Linear Algebra (Eigenvalues & Eigenvectors)",
        "query": "eigenvalues of [[4, 2], [1, 3]]",
        "expected_in_title": "Eigenvalues",
        "verify": lambda r: "λ = 5" in r["summary_value"] and "λ = 2" in r["summary_value"] and any("Eigenvectors Basis" in row[0] for row in r["rows"])
    },
    {
        "domain": "CAS: Complex Numbers (Modulus & Argument)",
        "query": "modulus and argument of 3 + 4*i",
        "expected_in_title": "Complex Number Analysis",
        "verify": lambda r: "|z| = 5" in r["summary_value"] and "z̄ = 3 - 4 · I" in r["summary_value"] and "53.1°" in r["summary_value"]
    },
    {
        "domain": "CAS: Differential Equations (1st Order ODE General Solution)",
        "query": "solve differential equation dy/dx + y = x",
        "expected_in_title": "Differential Equation Solution",
        "verify": lambda r: "C1 · exp(-x)" in r["summary_value"] or "x - 1" in r["summary_value"]
    },
    {
        "domain": "CAS: Differential Equations (ODE with Initial Condition)",
        "query": "solve differential equation dy/dx + y = 2 with y(0) = 1",
        "expected_in_title": "Differential Equation Solution (Particular)",
        "verify": lambda r: "2" in r["summary_value"] and "exp(-x)" in r["summary_value"]
    },

    # --- 4. CONVERSATIONAL ENGLISH & HINGLISH QUERIES ---
    {
        "domain": "Hinglish: Cylinder Mensuration",
        "query": "cylinder ka volume nikalo radius 7 height 14",
        "expected_in_title": "Cylinder Mensuration",
        "verify": lambda r: "2,155.133" in r["summary_value"]
    },
    {
        "domain": "Hinglish: Boat in Stream",
        "query": "Ek boat ki speed shant jal mein 15 km/h hai aur dhara ki speed 3 km/h. Anupravah mein 36 km kitne time mein?",
        "expected_in_title": "Boats & Streams",
        "verify": lambda r: "2" in r["summary_value"] and "hours" in r["summary_value"]
    },
    {
        "domain": "Conversational English: Complex Matrix Inversion",
        "query": "Please calculate the determinant, trace, and inverse of [[2, 1], [5, 3]]",
        "expected_in_title": "Matrix Linear Algebra",
        "verify": lambda r: "det(M) = 1" in r["summary_value"] and "Tr = 5" in r["summary_value"]
    }
]


def run_tests():
    print("=" * 80)
    print(" CALCULATOR GPT: AI-LEVEL MATHEMATICAL & REASONING VERIFICATION SUITE")
    print(" 100% Offline Pure Symbolic CAS & Heuristic Quantitative Aptitude")
    print("=" * 80)

    passed = 0
    total = len(test_cases)

    for idx, tc in enumerate(test_cases, 1):
        domain = tc["domain"]
        query = tc["query"]
        print(f"\n[Test {idx:02d}/{total:02d}] {domain}")
        print(f"  Input: \"{query}\"")

        try:
            res = solve_query(query)
            title = res.get("title", "")
            summary = res.get("summary_value", "")
            steps = res.get("steps", [])
            rows = res.get("rows", [])
            formula = res.get("formula", "")

            # Check expected title prefix
            if tc["expected_in_title"].lower() not in title.lower():
                print(f"  FAILED Title Check: Expected '{tc['expected_in_title']}', got '{title}'")
                continue

            # Run custom verification lambda
            if not tc["verify"](res):
                print(f"  FAILED Value Verification: Summary was: '{summary}'")
                print(f"  Rows: {rows}")
                continue

            print(f"  Title:   {title}")
            print(f"  Summary: {summary}")
            print(f"  Formula: {formula}")
            print(f"  Steps:   {len(steps)} steps generated | Rows: {len(rows)} data rows")
            print("  STATUS:  PASSED")
            passed += 1

        except Exception as e:
            print(f"  ERROR executing test: {e}")
            import traceback
            traceback.print_exc()

    # Test Batch Multi-Query capability with quotes and semicolons
    print("\n" + "-" * 80)
    print("[Test Batch Multi-Query] Semicolon-delimited & Quoted multi-query processing")
    multi_q = '"volume of sphere with radius 3"; "eigenvalues of [[1, 2], [2, 1]]"; "probability of sum 7 with 2 dice"'
    batch_results = process_all_queries(multi_q)
    print(f"  Batch queries processed: {len(batch_results)}")
    for i, r in enumerate(batch_results, 1):
        print(f"    Sub-result {i}: {r.get('title')} -> {r.get('summary_value')}")

    if len(batch_results) == 3:
        print("  STATUS:  BATCH PASSED")
        passed_batch = True
    else:
        print("  STATUS:  BATCH FAILED")
        passed_batch = False

    print("\n" + "=" * 80)
    print(f" FINAL RESULT: {passed}/{total} DOMAIN TESTS PASSED ({passed/total*100:.1f}%)")
    print(f" BATCH MULTI-QUERY TEST: {'PASSED' if passed_batch else 'FAILED'}")
    print("=" * 80)

    if passed == total and passed_batch:
        print("\nALL AI-LEVEL TESTS VERIFIED WITH 100% ACCURACY AND ZERO REGRESSIONS!")
        return 0
    else:
        print("\nSOME TESTS FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
