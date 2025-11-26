# 📏 Zuschnittoptimierung (Cutting Optimization)

Modern Python application for optimizing material cutting lists using the **First Fit Decreasing (FFD)** algorithm.

## 🎯 Features

- ✅ **3 Algorithms**: BFD, FFD, and Heuristic - choose the best for your data
- ✅ **Material Grouping**: Separate optimization for different materials
- ✅ **Multiplier**: Scale entire cutting list for series production
- ✅ **Saw Kerf**: Accounts for blade thickness/cutting loss
- ✅ **Visual Bars**: SVG visualization of cuts on each bar
- ✅ **Excel I/O**: Read from and write to Excel files
- ✅ **PDF Export**: Professional work plans (Compact & Visual)
- ✅ **Web Interface**: User-friendly Streamlit UI
- ✅ **Charts**: Efficiency and waste analysis with plotly
- ✅ **Statistics**: Comprehensive optimization metrics
- ✅ **Multi-language**: German interface for cutting industry

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Web Interface (Recommended)
```powershell
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

#### Option 2: Command Line
```python
from optimizer import CuttingOptimizer, Cut
from excel_handler import ExcelHandler

# Read from Excel
cuts = ExcelHandler.read_cuts_from_excel("input.xlsx")

# Optimize
optimizer = CuttingOptimizer(bar_length=3000)
results = optimizer.optimize_by_material(cuts)

# Write results
ExcelHandler.write_results_to_excel(results, "output.xlsx", 3000)
```

## 📊 Input Format

Your Excel file should have a sheet named **"Stueckliste"** with the following columns:

| Column A | Column B | Column C | Column D |
|----------|----------|----------|----------|
| Länge (mm) | Anzahl | Material | Materialname |
| 2500 | 3 | ST37 | Stahl S235JR |
| 1800 | 5 | ST37 | Stahl S235JR |
| 1200 | 4 | ALU | Aluminium 6060 |

### Column Descriptions

- **Länge (mm)**: Length of each cut in millimeters
- **Anzahl**: Quantity of cuts needed
- **Material**: Material code (e.g., ST37, ALU, ST52)
- **Materialname**: Full material description

## 📤 Output Formats

The application provides three export options:

### 1. Excel Export
Excel file with sheet **"Zuschnitt"** containing:
- **Material sections**: Grouped by material type
- **Bar assignments**: Each bar with its cuts
- **Statistics**: Total bars, cuts, waste, and efficiency
- **Summary**: Overall optimization results

### 2. PDF Export - Kompakter Arbeitsplan
Professional work plan with:
- ✅ Clean table layout (1 page per material)
- ✅ Material information header
- ✅ Complete cutting list with checkboxes
- ✅ Statistics and efficiency metrics
- ✅ Notes and signature fields
- 📄 **Perfect for:** Workshop distribution, quality control

### 3. PDF Export - Visueller Arbeitsplan
Visual work plan with:
- ✅ Graphical bar representation
- ✅ Cut-by-cut checklist overview
- ✅ Visual progress tracking
- ✅ Grouped by cut lengths
- 📊 **Perfect for:** Visual learners, training, quick overview

### Example Output

```
Material: ST37 - Stahl S235JR

Stange | Längen              | Gesamtlänge | Rest   | Effizienz %
-------|---------------------|-------------|--------|-------------
1      | 2500.0 / 400.0     | 2900.0      | 100.0  | 96.7%
2      | 1800.0 / 1200.0    | 3000.0      | 0.0    | 100.0%

Zusammenfassung:
- Anzahl Stangen: 2
- Anzahl Schnitte: 4
- Gesamtverschnitt: 100.0 mm
- Durchschn. Effizienz: 98.3%
```

## 🛠️ Configuration

Edit `config.py` to customize settings:

```python
# Default bar length in mm
DEFAULT_BAR_LENGTH = 3000

# Excel column mappings
EXCEL_COLUMNS = {
    'length': 0,      # Column A
    'quantity': 1,    # Column B
    'material': 2,    # Column C
    'name': 3         # Column D
}

# Sheet names
INPUT_SHEET_NAME = "Stueckliste"
OUTPUT_SHEET_NAME = "Zuschnitt"
```

## 📁 Project Structure

```
Zuschnittliste/
├── app.py                 # Streamlit web interface
├── optimizer.py           # FFD algorithm implementation
├── excel_handler.py       # Excel I/O operations
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
└── .github/
    └── copilot-instructions.md
```

## 🔧 Technical Details

### Algorithm: Best Fit Decreasing (BFD)

1. **Sort** all cuts in descending order by length
2. **Iterate** through each cut
3. **Find** the bar with the smallest remaining space that can fit the cut
4. **Place** cut in that bar (best fit)
5. **Create** new bar if cut doesn't fit anywhere
6. **Repeat** for all materials separately

### Complexity

- **Time:** O(n log n + n·m) where n = cuts, m = bars
- **Space:** O(n + m)

### Why BFD?

- Better than FFD for material efficiency
- Minimizes waste by filling gaps more effectively
- Near-optimal results (typically better than FFD)
- Industry-proven for cutting optimization
- Easy to understand and verify

## 🎨 Web Interface Features

### 📤 Upload & Optimization Tab
- Upload Excel files
- Preview loaded data
- Start optimization
- Download results

### 📊 Statistics Tab
- Overall metrics
- Efficiency charts by material
- Waste analysis
- Visual comparisons

### ℹ️ Help Tab
- Algorithm explanation
- Usage instructions
- Tips and best practices

## 🆚 Improvements over VBA Version

1. **Multiple Algorithms**: BFD, FFD, and Heuristic - not just one approach
2. **Saw Kerf Support**: Realistic cutting loss calculation
3. **Visual Bars**: See exactly how cuts are arranged on each bar
4. **Multiplier Feature**: Scale entire cutting list for series production
5. **Web Interface**: No Excel required for operation
6. **Interactive Charts**: Real-time efficiency and waste visualization
7. **Better Structure**: Modular, maintainable code
8. **Modern Stack**: Python, Streamlit, pandas, plotly
9. **Cross-platform**: Works on Windows, Mac, Linux
10. **Type Safety**: Type hints for better code quality
11. **Documentation**: Comprehensive inline documentation
12. **Error Handling**: Robust error management
13. **Testing Ready**: Structure supports unit tests
14. **Extensible**: Easy to add new features

## 📝 Example Usage

### Creating Example Input File

```python
from excel_handler import ExcelHandler

ExcelHandler.create_example_input("example_input.xlsx")
```

### Programmatic Usage

```python
from optimizer import CuttingOptimizer, Cut

# Create cuts manually
cuts = [
    Cut(2500, "ST37", "Stahl S235JR"),
    Cut(1800, "ST37", "Stahl S235JR"),
    Cut(1200, "ALU", "Aluminium 6060"),
]

# Optimize with optional multiplier
optimizer = CuttingOptimizer(bar_length=3000)
results = optimizer.optimize_by_material(cuts, multiplier=3)  # 3x quantity

# Access results
for material_code, data in results.items():
    print(f"Material: {material_code} - {data['name']}")
    for bar in data['bars']:
        print(f"  Bar {bar.bar_number}: {bar.cuts}")
        print(f"    Used: {bar.total_used}mm, Waste: {bar.waste}mm")
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Unit tests for all modules
- [ ] Different bin packing algorithms (Best Fit, Next Fit)
- [ ] Multi-length bar support (different standard lengths)
- [ ] Saw blade thickness consideration
- [ ] PDF export functionality
- [ ] Database integration
- [ ] REST API
- [ ] Docker containerization

## 📄 License

This project is open source. Feel free to use and modify for your needs.

## 🙏 Acknowledgments

Based on the original VBA Excel solution, improved with:
- Modern Python architecture
- Web-based interface
- Enhanced visualizations
- Better user experience

---

**Version:** 2.1.0  
**Algorithms:** BFD, FFD, Heuristic  
**New Features:** Saw kerf support, visual bar representation  
**Author:** Converted from VBA to Python  
**Date:** November 2025
