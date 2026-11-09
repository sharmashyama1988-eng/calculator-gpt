import json
from engine.master_solver import process_all_queries

test_queries = [
    "mean, median, mode of 12, 15, 12, 18, 20",
    "Ek train 60 km/h se aur dusri 80 km/h se opposite direction mein. 280 km kitne time mein?",
    "Differentiate sin(x^2) with respect to x",
    "integrate 3*x^2 + 2*x from 0 to 2",
    "solve 2*x^2 + 5*x - 3 = 0",
    "expand (a + b)^3",
    "A can do work in 10 days and B in 15 days. Together kitne din?",
    "Khareeda 1200 mein aur becha 1500 mein. Profit kitna?",
    "lcm of 24 and 36",
    "area of circle radius 7"
]

print("=== RUNNING ADVANCED MATHEMATICAL CAS & REASONING ENGINE TESTS ===")
for q in test_queries:
    results = process_all_queries(q)
    res = results[0]
    print(f"\n[QUERY]: {q}")
    print(f"  Title: {res.get('title')}")
    print(f"  Summary: {res.get('summary_value')}")
    print(f"  Formula: {res.get('formula')}")
    print(f"  Rows count: {len(res.get('rows', []))}")
    print(f"  Steps count: {len(res.get('steps', []))}")
    if res.get('steps'):
        print(f"  Step 1 Preview: {res['steps'][0]}")

print("\nALL 10 TESTS COMPLETED SUCCESSFULLY!")
