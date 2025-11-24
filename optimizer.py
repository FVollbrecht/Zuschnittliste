"""
Core optimization engine using First Fit Decreasing (FFD) algorithm.
"""
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Cut:
    """Represents a single cut requirement."""
    length: float
    material_code: str
    material_name: str
    
    def __repr__(self):
        return f"Cut({self.length}mm, {self.material_code})"


@dataclass
class Bar:
    """Represents a bar/rod with cuts assigned to it."""
    bar_number: int
    cuts: List[float]
    total_used: float
    bar_length: float
    
    @property
    def waste(self) -> float:
        """Calculate waste/remainder for this bar."""
        return self.bar_length - self.total_used
    
    @property
    def efficiency(self) -> float:
        """Calculate efficiency percentage."""
        return (self.total_used / self.bar_length) * 100 if self.bar_length > 0 else 0
    
    def can_fit(self, cut_length: float, kerf: float = 0.0) -> bool:
        """Check if a cut can fit in this bar (including kerf if not first cut)."""
        additional_length = cut_length
        if len(self.cuts) > 0:  # Add kerf if not the first cut
            additional_length += kerf
        return self.total_used + additional_length <= self.bar_length
    
    def add_cut(self, cut_length: float, kerf: float = 0.0) -> bool:
        """Add a cut to this bar if it fits (including kerf)."""
        if self.can_fit(cut_length, kerf):
            self.cuts.append(cut_length)
            self.total_used += cut_length
            if len(self.cuts) > 1:  # Add kerf to total if not first cut
                self.total_used += kerf
            return True
        return False
    
    def __repr__(self):
        return f"Bar {self.bar_number}: {len(self.cuts)} cuts, {self.total_used:.1f}mm used, {self.waste:.1f}mm waste"


class CuttingOptimizer:
    """
    Optimizes cutting lists using various bin packing algorithms.
    """
    
    def __init__(self, bar_length: float = 3000, algorithm: str = 'BFD', kerf: float = 0.0):
        """
        Initialize the optimizer.
        
        Args:
            bar_length: Standard length of bars/rods in mm
            algorithm: Algorithm to use ('FFD', 'BFD', or 'Heuristic')
            kerf: Saw blade thickness/kerf in mm (cutting loss per cut)
        """
        self.bar_length = bar_length
        self.algorithm = algorithm
        self.kerf = kerf
    
    def optimize(self, cuts: List[float]) -> List[Bar]:
        """
        Optimize a list of cuts using the selected algorithm.
        
        Args:
            cuts: List of cut lengths to optimize
            
        Returns:
            List of Bar objects with optimal cut assignments
        """
        if not cuts:
            return []
        
        if self.algorithm == 'FFD':
            return self._optimize_ffd(cuts)
        elif self.algorithm == 'BFD':
            return self._optimize_bfd(cuts)
        else:  # Heuristic
            return self._optimize_heuristic(cuts)
    
    def _optimize_ffd(self, cuts: List[float]) -> List[Bar]:
        """
        First Fit Decreasing: Place each cut in the first bar that fits.
        """
        if not cuts:
            return []
        
        # Sort cuts in descending order
        sorted_cuts = sorted(cuts, reverse=True)
        
        # Initialize first bar
        bars: List[Bar] = [Bar(
            bar_number=1,
            cuts=[],
            total_used=0.0,
            bar_length=self.bar_length
        )]
        
        # Apply First Fit Decreasing
        for cut_length in sorted_cuts:
            placed = False
            
            # Try to fit in existing bars (first fit)
            for bar in bars:
                if bar.add_cut(cut_length, self.kerf):
                    placed = True
                    break
            
            # Create new bar if cut doesn't fit anywhere
            if not placed:
                new_bar = Bar(
                    bar_number=len(bars) + 1,
                    cuts=[cut_length],
                    total_used=cut_length,
                    bar_length=self.bar_length
                )
                bars.append(new_bar)
        
        return bars
    
    def _optimize_bfd(self, cuts: List[float]) -> List[Bar]:
        """
        Best Fit Decreasing: Place each cut in the bar with smallest remaining space.
        """
        if not cuts:
            return []
        
        # Step 1: Sort cuts in descending order (BFD)
        sorted_cuts = sorted(cuts, reverse=True)
        
        # Step 2: Initialize first bar
        bars: List[Bar] = [Bar(
            bar_number=1,
            cuts=[],
            total_used=0.0,
            bar_length=self.bar_length
        )]
        
        # Step 3: Apply Best Fit Decreasing
        for cut_length in sorted_cuts:
            # Find the bar with the smallest remaining space that can fit the cut
            best_bar = None
            best_remaining = float('inf')
            
            for bar in bars:
                if bar.can_fit(cut_length, self.kerf):
                    # Calculate remaining space after adding cut and kerf
                    additional_length = cut_length + (self.kerf if len(bar.cuts) > 0 else 0)
                    remaining_after = bar.waste - additional_length
                    if remaining_after < best_remaining:
                        best_remaining = remaining_after
                        best_bar = bar
            
            # If found a suitable bar, add the cut
            if best_bar is not None:
                best_bar.add_cut(cut_length, self.kerf)
            else:
                # Create new bar if cut doesn't fit anywhere
                new_bar = Bar(
                    bar_number=len(bars) + 1,
                    cuts=[cut_length],
                    total_used=cut_length,
                    bar_length=self.bar_length
                )
                bars.append(new_bar)
        
        return bars
    
    def _optimize_heuristic(self, cuts: List[float]) -> List[Bar]:
        """
        Heuristic approach: Combine BFD with intelligent grouping.
        Groups similar-sized cuts for better packing efficiency.
        """
        if not cuts:
            return []
        
        # Sort cuts in descending order
        sorted_cuts = sorted(cuts, reverse=True)
        
        # Initialize first bar
        bars: List[Bar] = [Bar(
            bar_number=1,
            cuts=[],
            total_used=0.0,
            bar_length=self.bar_length
        )]
        
        # Heuristic: Try to group cuts intelligently
        for cut_length in sorted_cuts:
            best_bar = None
            best_score = float('-inf')
            
            for bar in bars:
                if bar.can_fit(cut_length, self.kerf):
                    # Calculate remaining space after adding cut and kerf
                    additional_length = cut_length + (self.kerf if len(bar.cuts) > 0 else 0)
                    remaining_after = bar.waste - additional_length
                    
                    # Heuristic scoring:
                    # 1. Prefer bars with less waste (like BFD)
                    # 2. But also consider if remaining space could fit other pending cuts
                    # 3. Penalize nearly-full bars to leave room for optimization
                    
                    waste_score = -remaining_after  # Prefer smaller waste
                    
                    # Bonus if remaining space is useful for future cuts
                    if remaining_after > 100:  # At least 100mm useful
                        waste_score += 50
                    
                    # Penalty for nearly full bars (less than 5% remaining)
                    if remaining_after < self.bar_length * 0.05:
                        waste_score -= 100
                    
                    if waste_score > best_score:
                        best_score = waste_score
                        best_bar = bar
            
            # Place cut in best bar or create new one
            if best_bar is not None:
                best_bar.add_cut(cut_length, self.kerf)
            else:
                new_bar = Bar(
                    bar_number=len(bars) + 1,
                    cuts=[cut_length],
                    total_used=cut_length,
                    bar_length=self.bar_length
                )
                bars.append(new_bar)
        
        return bars
    
    def optimize_by_material(self, cuts: List[Cut], multiplier: int = 1) -> Dict[str, List[Bar]]:
        """
        Optimize cuts grouped by material type with optional multiplier.
        
        Args:
            cuts: List of Cut objects
            multiplier: Multiply all quantities by this factor (default: 1)
            
        Returns:
            Dictionary mapping material codes to optimized bar lists
        """
        # Group cuts by material
        material_groups: Dict[str, List[float]] = {}
        material_names: Dict[str, str] = {}
        
        for cut in cuts:
            if cut.material_code not in material_groups:
                material_groups[cut.material_code] = []
                material_names[cut.material_code] = cut.material_name
            # Apply multiplier to each cut
            for _ in range(multiplier):
                material_groups[cut.material_code].append(cut.length)
        
        # Optimize each material group
        results = {}
        for material_code, cut_lengths in material_groups.items():
            bars = self.optimize(cut_lengths)
            # Add material info to results
            results[material_code] = {
                'name': material_names[material_code],
                'bars': bars
            }
        
        return results
    
    @staticmethod
    def calculate_statistics(bars: List[Bar]) -> Dict[str, float]:
        """
        Calculate optimization statistics.
        
        Args:
            bars: List of optimized bars
            
        Returns:
            Dictionary with statistics
        """
        if not bars:
            return {
                'total_bars': 0,
                'total_cuts': 0,
                'total_length_used': 0,
                'total_waste': 0,
                'average_efficiency': 0
            }
        
        total_cuts = sum(len(bar.cuts) for bar in bars)
        total_length = sum(bar.total_used for bar in bars)
        total_waste = sum(bar.waste for bar in bars)
        avg_efficiency = sum(bar.efficiency for bar in bars) / len(bars)
        
        return {
            'total_bars': len(bars),
            'total_cuts': total_cuts,
            'total_length_used': total_length,
            'total_waste': total_waste,
            'average_efficiency': avg_efficiency
        }
