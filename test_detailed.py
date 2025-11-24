"""
Detailed test to show algorithm decision-making process.
"""
from optimizer import CuttingOptimizer

# Test case where algorithms should differ
test_cuts = [
    1600, 1600,  # Two large
    1500,        # One medium-large
    1000, 1000, 1000,  # Three medium
    600, 600, 600, 600  # Four small
]

bar_length = 3000

print("=" * 80)
print("DETAILED ALGORITHM DECISION TEST")
print("=" * 80)
print(f"Bar Length: {bar_length}mm")
print(f"Cuts: {test_cuts}")
print("=" * 80)

for algorithm in ['FFD', 'BFD', 'Heuristic']:
    print(f"\n### {algorithm} ###")
    
    optimizer = CuttingOptimizer(bar_length=bar_length, algorithm=algorithm)
    bars = optimizer.optimize(test_cuts)
    
    print(f"Bars: {len(bars)}, Waste: {sum(b.waste for b in bars):.0f}mm\n")
    
    for i, bar in enumerate(bars, 1):
        cuts_detail = ", ".join(f"{c:.0f}" for c in bar.cuts)
        print(f"Bar {i}: [{cuts_detail}]")
        print(f"  Total: {bar.total_used:.0f}mm, Waste: {bar.waste:.0f}mm, "
              f"Efficiency: {bar.efficiency:.1f}%")
