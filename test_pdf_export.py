"""
Test-Script für PDF-Export
"""
from optimizer import CuttingOptimizer, Cut
from pdf_generator import WorkPlanPDFGenerator

# Test-Daten erstellen
cuts = [
    Cut(2500, "ST37", "Stahl S235JR"),
    Cut(2500, "ST37", "Stahl S235JR"),
    Cut(2500, "ST37", "Stahl S235JR"),
    Cut(1800, "ST37", "Stahl S235JR"),
    Cut(1800, "ST37", "Stahl S235JR"),
    Cut(1800, "ST37", "Stahl S235JR"),
    Cut(1800, "ST37", "Stahl S235JR"),
    Cut(1800, "ST37", "Stahl S235JR"),
    Cut(1200, "ST37", "Stahl S235JR"),
    Cut(1200, "ST37", "Stahl S235JR"),
    Cut(1200, "ST37", "Stahl S235JR"),
    Cut(1200, "ST37", "Stahl S235JR"),
    Cut(900, "ST37", "Stahl S235JR"),
    Cut(900, "ST37", "Stahl S235JR"),
    Cut(900, "ST37", "Stahl S235JR"),
    Cut(900, "ST37", "Stahl S235JR"),
    Cut(900, "ST37", "Stahl S235JR"),
    Cut(900, "ST37", "Stahl S235JR"),
    Cut(2400, "ALU", "Aluminium 6060"),
    Cut(2400, "ALU", "Aluminium 6060"),
    Cut(1500, "ALU", "Aluminium 6060"),
    Cut(1500, "ALU", "Aluminium 6060"),
    Cut(1500, "ALU", "Aluminium 6060"),
    Cut(1500, "ALU", "Aluminium 6060"),
    Cut(1000, "ALU", "Aluminium 6060"),
    Cut(1000, "ALU", "Aluminium 6060"),
    Cut(1000, "ALU", "Aluminium 6060"),
    Cut(1000, "ALU", "Aluminium 6060"),
    Cut(1000, "ALU", "Aluminium 6060"),
]

# Optimierung durchführen
optimizer = CuttingOptimizer(bar_length=6000, algorithm='BFD', kerf=3.0)
results = optimizer.optimize_by_material(cuts, multiplier=1)

print("="*60)
print("PDF-Export Test")
print("="*60)

# PDF-Generator erstellen
pdf_gen = WorkPlanPDFGenerator(results, bar_length=6000, kerf=3.0, algorithm='BFD')

# Kompakter Arbeitsplan
print("\n1. Erstelle kompakten Arbeitsplan...")
pdf_gen.generate_compact_plan("test_arbeitsplan_kompakt.pdf")
print("   ✓ Gespeichert: test_arbeitsplan_kompakt.pdf")

# Visueller Arbeitsplan
print("\n2. Erstelle visuellen Arbeitsplan...")
pdf_gen.generate_visual_plan("test_arbeitsplan_visuell.pdf")
print("   ✓ Gespeichert: test_arbeitsplan_visuell.pdf")

print("\n" + "="*60)
print("Test abgeschlossen!")
print("="*60)
print("\nÖffne die PDF-Dateien zum Ansehen:")
print("  • test_arbeitsplan_kompakt.pdf")
print("  • test_arbeitsplan_visuell.pdf")
