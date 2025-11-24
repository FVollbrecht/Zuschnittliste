"""
Configuration settings for the cutting optimization application.
"""

# Default bar length in mm
DEFAULT_BAR_LENGTH = 3000

# Excel column mappings (0-indexed)
EXCEL_COLUMNS = {
    'length': 0,      # Column A: Length (Länge)
    'quantity': 1,    # Column B: Quantity (Anzahl)
    'material': 2,    # Column C: Material code
    'name': 3         # Column D: Material name
}

# Input/Output settings
INPUT_SHEET_NAME = "Stueckliste"
OUTPUT_SHEET_NAME = "Zuschnitt"

# Optimization settings
OPTIMIZATION_TOLERANCE = 0.1  # mm tolerance for cutting precision
