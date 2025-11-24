"""
Test script to verify that different algorithms produce different results.
"""
from optimizer import CuttingOptimizer

# Test data that will show differences between algorithms
# More varied sizes to highlight algorithm differences
test_cuts = [
    2700, 2600,  # Large cuts (close to bar length)
    1800, 1700, 1650,  # Large-medium cuts
    1200, 1150, 1100, 1050,  # Medium cuts
    850, 820, 780, 750,  # Small-medium cuts
    500, 480, 450, 420, 400  # Small cuts
]

bar_length = 3000

print("=" * 80)
print("ALGORITHM COMPARISON TEST")
print("=" * 80)
print(f"Bar Length: {bar_length}mm")
print(f"Cuts: {test_cuts}")
print(f"Total cuts length: {sum(test_cuts)}mm")
print("=" * 80)

for algorithm in ['FFD', 'BFD', 'Heuristic']:
    print(f"\n{algorithm} Algorithm:")
    print("-" * 80)
    
    optimizer = CuttingOptimizer(bar_length=bar_length, algorithm=algorithm)
    bars = optimizer.optimize(test_cuts)
    
    print(f"Total bars used: {len(bars)}")
    print(f"Total waste: {sum(bar.waste for bar in bars):.1f}mm")
    print(f"Average efficiency: {sum(bar.efficiency for bar in bars) / len(bars):.1f}%")
    
    for bar in bars:
        cuts_str = ", ".join(f"{c:.0f}" for c in bar.cuts)
        print(f"  Bar {bar.bar_number}: [{cuts_str}] = {bar.total_used:.0f}mm used, {bar.waste:.0f}mm waste")

print("\n" + "=" * 80)
