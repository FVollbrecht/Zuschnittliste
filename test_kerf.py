"""
Test saw kerf functionality
"""
from optimizer import CuttingOptimizer

# Test cuts
test_cuts = [1500, 1500, 1000, 1000, 1000]
bar_length = 3000

print("=" * 80)
print("SAW KERF TEST")
print("=" * 80)
print(f"Bar Length: {bar_length}mm")
print(f"Cuts: {test_cuts}")
print(f"Total cuts length (without kerf): {sum(test_cuts)}mm")
print("=" * 80)

for kerf in [0.0, 3.0, 5.0]:
    print(f"\n### Kerf: {kerf}mm ###\n")
    
    optimizer = CuttingOptimizer(bar_length=bar_length, algorithm='BFD', kerf=kerf)
    bars = optimizer.optimize(test_cuts)
    
    total_kerf_loss = sum(len(bar.cuts) - 1 for bar in bars) * kerf
    
    print(f"Bars used: {len(bars)}")
    print(f"Total kerf loss: {total_kerf_loss:.1f}mm")
    print(f"Total waste: {sum(bar.waste for bar in bars):.1f}mm")
    print(f"Average efficiency: {sum(bar.efficiency for bar in bars) / len(bars):.1f}%\n")
    
    for bar in bars:
        cuts_str = ", ".join(f"{c:.0f}" for c in bar.cuts)
        kerf_in_bar = (len(bar.cuts) - 1) * kerf
        print(f"  Bar {bar.bar_number}: [{cuts_str}]")
        print(f"    Cuts: {sum(bar.cuts):.0f}mm + Kerf: {kerf_in_bar:.0f}mm = {bar.total_used:.0f}mm")
        print(f"    Waste: {bar.waste:.0f}mm ({bar.efficiency:.1f}%)\n")

print("=" * 80)
