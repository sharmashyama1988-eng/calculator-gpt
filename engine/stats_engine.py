"""Comprehensive Descriptive & Inferential Statistics Engine for Calculator GPT.
Analyzes datasets with full variance, standard deviation, quartiles, IQR, and step-by-step deviations.
"""

import math
from typing import Dict, Any, List, Optional
from .nlp_parser import extract_numbers, normalize_query


def fmt(n: float, decimals: int = 3) -> str:
    """Formats numeric values cleanly."""
    if not math.isfinite(n):
        return "Undefined"
    if n == int(n):
        return str(int(n))
    return f"{n:.{decimals}f}".rstrip('0').rstrip('.')


def solve_statistics(query: str) -> Optional[Dict[str, Any]]:
    """Analyzes a numerical dataset and returns full statistical measures and step-by-step breakdown."""
    nums = extract_numbers(normalize_query(query))
    if len(nums) < 2:
        return None
        
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    total_sum = sum(sorted_nums)
    mean = total_sum / n
    
    # Median
    if n % 2 == 1:
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2.0
        
    # Mode
    freq = {}
    for x in sorted_nums:
        freq[x] = freq.get(x, 0) + 1
    max_freq = max(freq.values())
    if max_freq == 1:
        mode_str = "No Mode (All elements unique)"
        mode_val = None
    else:
        modes = [x for x, f in freq.items() if f == max_freq]
        mode_str = ", ".join([fmt(m) for m in modes])
        mode_val = modes[0]
        
    # Range
    data_range = sorted_nums[-1] - sorted_nums[0]
    
    # Population & Sample Variance and Standard Deviation
    squared_diffs = [(x - mean) ** 2 for x in sorted_nums]
    sum_squared_diffs = sum(squared_diffs)
    
    pop_var = sum_squared_diffs / n
    pop_sd = math.sqrt(pop_var)
    
    sample_var = sum_squared_diffs / (n - 1) if n > 1 else 0.0
    sample_sd = math.sqrt(sample_var)
    
    # Quartiles (Q1, Q3, IQR)
    def get_median(arr):
        k = len(arr)
        if k == 0:
            return 0
        return arr[k // 2] if k % 2 == 1 else (arr[k // 2 - 1] + arr[k // 2]) / 2.0
        
    mid = n // 2
    lower_half = sorted_nums[:mid]
    upper_half = sorted_nums[mid + 1:] if n % 2 == 1 else sorted_nums[mid:]
    q1 = get_median(lower_half)
    q3 = get_median(upper_half)
    iqr = q3 - q1
    
    # Outliers (1.5 * IQR Rule)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in sorted_nums if x < lower_bound or x > upper_bound]
    outlier_str = ", ".join([fmt(x) for x in outliers]) if outliers else "None detected"
    
    steps = [
        f"Input Dataset: [{', '.join([fmt(x) for x in nums])}]",
        f"Sorted Dataset (N={n}): [{', '.join([fmt(x) for x in sorted_nums])}]",
        f"Step 1: Calculate Mean (Average) = Σx ÷ N = {fmt(total_sum)} ÷ {n} = {fmt(mean, 4)}",
        f"Step 2: Calculate Median: Middle element at position {(n+1)/2} = {fmt(median, 3)}",
        f"Step 3: Calculate Mode: Highest frequency element = {mode_str} ({max_freq} times)" if max_freq > 1 else "Step 3: Mode: None (all numbers occur once)",
        f"Step 4: Sum of squared deviations Σ(x - x̄)² = {fmt(sum_squared_diffs, 4)}",
        f"Step 5: Population Std Dev σ = √(Σ(x - x̄)² ÷ N) = √({fmt(sum_squared_diffs, 2)} ÷ {n}) = {fmt(pop_sd, 4)}",
        f"Step 6: Sample Std Dev s = √(Σ(x - x̄)² ÷ (N−1)) = √({fmt(sum_squared_diffs, 2)} ÷ {n-1}) = {fmt(sample_sd, 4)}",
        f"Step 7: Quartiles: Q1 = {fmt(q1)}, Q3 = {fmt(q3)}, IQR = {fmt(iqr)}"
    ]
    
    return {
        "title": f"Statistical Analysis (N={n} elements)",
        "summary_value": f"Mean: {fmt(mean, 2)} · Median: {fmt(median, 2)} · Mode: {mode_str}",
        "formula": "x̄ = Σx / N,  σ = √(Σ(x − x̄)² / N)",
        "rows": [
            ["Mean (Average)", fmt(mean, 3)],
            ["Median (Middle Value)", fmt(median, 3)],
            ["Mode (Most Frequent)", mode_str],
            ["Population Std Dev (σ)", fmt(pop_sd, 3)],
            ["Sample Std Dev (s)", fmt(sample_sd, 3)],
            ["Range (Max − Min)", fmt(data_range, 3)],
            ["Interquartile Range (IQR)", fmt(iqr, 3)],
            ["First Quartile (Q1)", fmt(q1, 3)],
            ["Third Quartile (Q3)", fmt(q3, 3)],
            ["Outliers (1.5 × IQR)", outlier_str],
            ["Sum of All Elements (Σx)", fmt(total_sum, 2)],
            ["Sample Count (N)", str(n)]
        ],
        "steps": steps,
        "insights": "The Standard Deviation measures the dispersion of data points around the mean. A low standard deviation indicates values cluster tightly near the average.",
        "raw": mean
    }
