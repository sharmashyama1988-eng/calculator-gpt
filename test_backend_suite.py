import urllib.request
import urllib.parse
import json
import time
import concurrent.futures

BASE_URL = "http://127.0.0.1:8765/api/solve"

def send_post(query_dict_or_raw, is_raw=False, timeout=10):
    start = time.perf_counter()
    try:
        data = query_dict_or_raw.encode('utf-8') if is_raw else json.dumps(query_dict_or_raw).encode('utf-8')
        req = urllib.request.Request(
            BASE_URL,
            data=data,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            dur = (time.perf_counter() - start) * 1000
            status_code = resp.getcode()
            body = resp.read().decode('utf-8', errors='replace')
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = body
            return {"status_code": status_code, "duration_ms": dur, "data": parsed, "error": None}
    except Exception as e:
        dur = (time.perf_counter() - start) * 1000
        return {"status_code": getattr(e, 'code', None), "duration_ms": dur, "data": None, "error": str(e)}

def send_get(query_str, timeout=10):
    start = time.perf_counter()
    try:
        url = f"{BASE_URL}?q={urllib.parse.quote(query_str)}"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            dur = (time.perf_counter() - start) * 1000
            status_code = resp.getcode()
            body = resp.read().decode('utf-8', errors='replace')
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = body
            return {"status_code": status_code, "duration_ms": dur, "data": parsed, "error": None}
    except Exception as e:
        dur = (time.perf_counter() - start) * 1000
        return {"status_code": getattr(e, 'code', None), "duration_ms": dur, "data": None, "error": str(e)}

print("=== STARTING RIGOROUS BACKEND HTTP API TESTING ===")

test_cases_standard = [
    # 1. Standard Arithmetic & Precedence
    ("POST", {"q": "2 + 3 * 4 ^ 2"}, "Precedence and powers"),
    ("GET", "100 - 25 * 3 + 50 / 2", "Multi-operator arithmetic"),
    ("POST", {"q": "sqrt(144) + sin(pi/2) * cos(0)"}, "Trigonometric and roots"),
    
    # 2. Advanced CAS & Calculus
    ("POST", {"q": "differentiate x^4 - 3*x^2 + 5*x - 7 with respect to x"}, "Polynomial differentiation"),
    ("GET", "integrate 3*x^2 + 2*x from 0 to 2", "Definite integration"),
    ("POST", {"q": "solve 3*x^2 - 11*x - 4 = 0"}, "Quadratic equation"),
    ("POST", {"q": "expand (2*x + 3*y)^4"}, "Multinomial expansion"),
    ("POST", {"q": "factor x^3 - 6*x^2 + 11*x - 6"}, "Polynomial factoring"),
    ("POST", {"q": "determinant of [[2, 5], [1, 3]]"}, "Matrix determinant"),
    ("POST", {"q": "eigenvalues of [[1, 2], [2, 1]]"}, "Matrix eigenvalues"),
    ("POST", {"q": "limit sin(x)/x as x -> 0"}, "Limit computation"),
    
    # 3. Quantitative Aptitude & Word Problems
    ("POST", {"q": "A train 150m long is travelling at 54 km/h. How much time will it take to cross a platform 250m long?"}, "Train crossing platform"),
    ("POST", {"q": "A can finish a work in 12 days and B can do it in 18 days. If they work together for 4 days, what fraction remains?"}, "Time and work fraction"),
    ("POST", {"q": "Bought an article for 450 and sold it for 540. Find profit percentage."}, "Profit percentage"),
    ("POST", {"q": "Father is 4 times as old as his son. In 20 years, father will be twice as old as his son. Find present ages."}, "Age word problem"),
    ("POST", {"q": "Pipe A fills a tank in 10 hours and Pipe B empties it in 15 hours. How long if both open?"}, "Pipes and cisterns"),
    
    # 4. Statistics & Number Theory
    ("POST", {"q": "mean, median, mode, variance, std dev of 10, 12, 14, 16, 18, 20"}, "Complete descriptive stats"),
    ("POST", {"q": "lcm and gcd of 48, 72, 108"}, "LCM and GCD"),
    ("POST", {"q": "is 104729 prime?"}, "Primes"),
    
    # 5. Hinglish & Mixed Natural Language
    ("POST", {"q": "Ek car 40 km/h ki speed se 2 ghante chali, fir 60 km/h se 3 ghante. Average speed kya hogi?"}, "Hinglish weighted avg speed"),
    ("POST", {"q": "15000 ka 10% annual compound interest 2 saal ke liye kitna hoga?"}, "Hinglish compound interest"),
]

passed_standard = 0
for method, payload, label in test_cases_standard:
    if method == "POST":
        res = send_post(payload)
        q_label = payload['q']
    else:
        res = send_get(payload)
        q_label = payload
        
    status = res['status_code']
    dur = res['duration_ms']
    data = res['data']
    err = res['error']
    
    if status == 200 and isinstance(data, dict) and data.get('status') == 'success' and len(data.get('results', [])) > 0:
        r0 = data['results'][0]
        title = r0.get('title')
        summary = r0.get('summary_value')
        print(f"[PASS] ({dur:.1f}ms) {label}: '{q_label[:40]}' -> [{title}] {summary}")
        passed_standard += 1
    else:
        print(f"[FAIL] ({dur:.1f}ms) {label}: '{q_label}' -> Status: {status}, Error: {err}, Data: {data}")

print(f"\n--- Standard Queries: {passed_standard}/{len(test_cases_standard)} Passed ---\n")

# 6. Extreme Edge Cases & Malformed Inputs
edge_cases = [
    ("Division by zero", {"q": "1 / 0"}),
    ("Zero over zero", {"q": "0 / 0"}),
    ("Solve division by zero", {"q": "solve 1/x = 0"}),
    ("Undefined trig", {"q": "tan(pi/2)"}),
    ("Empty query", {"q": ""}),
    ("Whitespace only", {"q": "   \n\t  "}),
    ("Malformed syntax operators", {"q": "++--**//5"}),
    ("Unmatched parentheses", {"q": "(((((2 + 3) * 5"}),
    ("Malformed equation", {"q": "solve = = = = x"}),
    ("Nonsense words", {"q": "foobar banana strawberry elephant"}),
    ("XSS / Script injection", {"q": "<script>alert('xss')</script> solve x+1=2"}),
    ("SQL Injection pattern", {"q": "1'; DROP TABLE users; --"}),
    ("Massive integer power", {"q": "10^10000"}),
    ("Huge factorial attempt", {"q": "10000!"}),
    ("Extreme long input string", {"q": "1 + " * 500 + "1"}),
    ("Complex numbers", {"q": "sqrt(-4) * sqrt(-9)"}),
    ("Unicode Math", {"q": "∫ x² dx from 0 to 1"}),
]

print("=== TESTING EXTREME EDGE CASES & ADVERSARIAL PAYLOADS ===")
edge_results = []
for label, payload in edge_cases:
    res = send_post(payload, timeout=5)
    status = res['status_code']
    dur = res['duration_ms']
    data = res['data']
    err = res['error']
    edge_results.append((label, status, dur, data, err))
    print(f"[{'PASS' if status == 200 else 'ERR'}] ({dur:.1f}ms) Edge case '{label}': code={status}, error={err}")
    if isinstance(data, dict):
        results = data.get('results', [])
        if results:
            print(f"      Result: {results[0].get('title')} | Summary: {results[0].get('summary_value')}")
        else:
            print(f"      Status: {data.get('status')}, Msg: {data.get('message')}")

# 7. Non-JSON / Malformed HTTP payload
print("\n=== TESTING MALFORMED HTTP REQUESTS ===")
res_raw = send_post("This is definitely not valid JSON {{{", is_raw=True)
print(f"Non-JSON raw body -> code={res_raw['status_code']}, data={res_raw['data']}")

# 8. High-Concurrency Stress Test
print("\n=== EXECUTING CONCURRENT STRESS TEST (50 simultaneous requests) ===")
bench_queries = [
    "solve 5*x^2 - 14*x + 8 = 0",
    "differentiate sin(x)*exp(x) with respect to x",
    "Ek train 80 km/h se aur dusri 100 km/h se. 360 km opposite direction kitne time mein?",
    "mean, median, mode of 5, 12, 19, 21, 21, 28, 35",
    "integrate 4*x^3 from 1 to 3"
]

def fire_req(i):
    q = bench_queries[i % len(bench_queries)]
    return send_post({"q": q})

start_bench = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fire_req, i) for i in range(50)]
    bench_results = [f.result() for f in futures]
total_bench_dur = time.perf_counter() - start_bench

durations = [r['duration_ms'] for r in bench_results]
success_count = sum(1 for r in bench_results if r['status_code'] == 200 and r['data'] and r['data'].get('status') == 'success')
avg_lat = sum(durations) / len(durations)
min_lat = min(durations)
max_lat = max(durations)
p95_lat = sorted(durations)[int(len(durations) * 0.95)]

print(f"Completed 50 concurrent requests in {total_bench_dur:.2f}s ({50/total_bench_dur:.1f} req/sec)")
print(f"Successful: {success_count}/50")
print(f"Latency: Avg={avg_lat:.1f}ms, Min={min_lat:.1f}ms, Max={max_lat:.1f}ms, P95={p95_lat:.1f}ms")
