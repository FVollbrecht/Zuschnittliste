"""
PDF-Generator für Arbeitspläne
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import List, Dict
import io

from optimizer import Bar


class WorkPlanPDFGenerator:
    """Generates work plan PDFs for cutting optimization results."""
    
    def __init__(self, results: Dict[str, Dict], bar_length: float, kerf: float, algorithm: str):
        """
        Initialize PDF generator.
        
        Args:
            results: Optimization results by material
            bar_length: Standard bar length
            kerf: Saw blade thickness
            algorithm: Algorithm used (FFD, BFD, Heuristic)
        """
        self.results = results
        self.bar_length = bar_length
        self.kerf = kerf
        self.algorithm = algorithm
        
    def generate_compact_plan(self, output_path: str = None) -> bytes:
        """
        Generate compact work plan (1 page per material).
        
        Args:
            output_path: Optional file path to save PDF
            
        Returns:
            PDF as bytes if output_path is None
        """
        if output_path:
            pdf = SimpleDocTemplate(output_path, pagesize=A4,
                                   rightMargin=15*mm, leftMargin=15*mm,
                                   topMargin=15*mm, bottomMargin=15*mm)
        else:
            buffer = io.BytesIO()
            pdf = SimpleDocTemplate(buffer, pagesize=A4,
                                   rightMargin=15*mm, leftMargin=15*mm,
                                   topMargin=15*mm, bottomMargin=15*mm)
        
        styles = getSampleStyleSheet()
        story = []
        
        for material_code, data in self.results.items():
            material_name = data['name']
            bars: List[Bar] = data['bars']
            
            if not bars:
                continue
            
            # Header
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=3*mm
            )
            
            story.append(Paragraph("ARBEITSPLAN ZUSCHNITT", title_style))
            story.append(Spacer(1, 3*mm))
            
            # Info box
            info_data = [
                ['Material:', f"{material_code} - {material_name}", 'Datum:', datetime.now().strftime('%d.%m.%Y')],
                ['Stangenlänge:', f"{self.bar_length:.0f} mm", 'Sägeblattstärke:', f"{self.kerf:.1f} mm"],
                ['Anzahl Stangen:', str(len(bars)), 'Algorithmus:', self.algorithm],
            ]
            
            info_table = Table(info_data, colWidths=[35*mm, 55*mm, 35*mm, 45*mm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
                ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 5*mm))
            
            # Cutting table
            table_data = [['Stab', 'Schnittlängen (mm)', 'Gesamt', 'Rest', '☐']]
            
            for bar in bars:
                cuts_str = ' / '.join(f"{c:.0f}" for c in bar.cuts)
                table_data.append([
                    str(bar.bar_number),
                    cuts_str,
                    f"{bar.total_used:.0f} mm",
                    f"{bar.waste:.0f} mm",
                    '☐'
                ])
            
            # Calculate statistics
            total_waste = sum(bar.waste for bar in bars)
            avg_efficiency = sum(bar.efficiency for bar in bars) / len(bars)
            
            # Summary row
            table_data.append([
                'Summe:',
                f"{len(bars)} Stangen | Ø Effizienz: {avg_efficiency:.1f}%",
                '',
                f"{total_waste:.0f} mm",
                ''
            ])
            
            cut_table = Table(table_data, colWidths=[15*mm, 95*mm, 25*mm, 25*mm, 10*mm])
            cut_table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                # Data rows
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
                ('ALIGN', (0, 1), (0, -2), 'CENTER'),
                ('ALIGN', (1, 1), (1, -2), 'LEFT'),
                ('ALIGN', (2, 1), (-1, -2), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -2), 9),
                # Summary row
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 9),
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
                ('TOPPADDING', (0, 0), (-1, -1), 1.5*mm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5*mm),
            ]))
            
            story.append(cut_table)
            story.append(Spacer(1, 5*mm))
            
            # Notes section
            notes_style = ParagraphStyle('Notes', parent=styles['Normal'], fontSize=8)
            notes = [
                "ANMERKUNGEN:",
                "• Schnitte von links nach rechts ausführen",
                f"• Sägeblattstärke von {self.kerf:.1f} mm ist bereits berücksichtigt",
                "• Reststücke > 500 mm markieren und lagern",
                "• Qualitätskontrolle: Länge ±1 mm"
            ]
            
            for note in notes:
                story.append(Paragraph(note, notes_style))
            
            story.append(Spacer(1, 5*mm))
            
            # Signature line
            sig_data = [['Ausgeführt von:', '____________________', 'Datum:', '__________', 'Unterschrift:', '____________________']]
            sig_table = Table(sig_data, colWidths=[30*mm, 40*mm, 15*mm, 25*mm, 25*mm, 35*mm])
            sig_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            
            story.append(sig_table)
            story.append(PageBreak())
        
        # Build PDF
        pdf.build(story)
        
        if output_path:
            return None
        else:
            buffer.seek(0)
            return buffer.getvalue()
    
    def generate_visual_plan(self, output_path: str = None) -> bytes:
        """
        Generate visual work plan with bar charts.
        
        Args:
            output_path: Optional file path to save PDF
            
        Returns:
            PDF as bytes if output_path is None
        """
        if output_path:
            pdf = SimpleDocTemplate(output_path, pagesize=A4,
                                   rightMargin=15*mm, leftMargin=15*mm,
                                   topMargin=15*mm, bottomMargin=15*mm)
        else:
            buffer = io.BytesIO()
            pdf = SimpleDocTemplate(buffer, pagesize=A4,
                                   rightMargin=15*mm, leftMargin=15*mm,
                                   topMargin=15*mm, bottomMargin=15*mm)
        
        styles = getSampleStyleSheet()
        story = []
        
        for material_code, data in self.results.items():
            material_name = data['name']
            bars: List[Bar] = data['bars']
            
            if not bars:
                continue
            
            # Header
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=3*mm
            )
            
            story.append(Paragraph(f"🔨 ZUSCHNITTPLAN VISUELL", title_style))
            story.append(Paragraph(f"Material: {material_code} - {material_name}", styles['Heading2']))
            story.append(Spacer(1, 5*mm))
            
            # Visual bars (first 10)
            for bar in bars[:10]:
                # Bar visualization as text
                cuts_visual = []
                total_width = 150  # mm for visualization
                
                for cut in bar.cuts:
                    cut_width = (cut / self.bar_length) * total_width
                    cuts_visual.append(f"[{cut:.0f}]")
                
                waste_width = (bar.waste / self.bar_length) * total_width
                
                bar_text = f"Stab {bar.bar_number}:  {' | '.join(cuts_visual)} ▓▓▓ Rest: {bar.waste:.0f}mm"
                
                bar_style = ParagraphStyle('BarText', parent=styles['Normal'], 
                                          fontSize=8, fontName='Courier')
                story.append(Paragraph(bar_text, bar_style))
                
                # Checkbox
                check_style = ParagraphStyle('Check', parent=styles['Normal'], fontSize=10)
                story.append(Paragraph("☐ Fertig", check_style))
                story.append(Spacer(1, 2*mm))
            
            if len(bars) > 10:
                story.append(Paragraph(f"... und {len(bars) - 10} weitere Stangen (siehe Detail-Liste)", 
                                      styles['Normal']))
            
            story.append(Spacer(1, 5*mm))
            
            # Legend
            legend_style = ParagraphStyle('Legend', parent=styles['Normal'], fontSize=8)
            story.append(Paragraph("Legende:  [####] = Schnitt  | = Sägeschnitt  ▓▓▓ = Verschnitt", legend_style))
            story.append(Spacer(1, 5*mm))
            
            # Cut list overview
            story.append(Paragraph("SCHNITTLISTEN-ÜBERSICHT", styles['Heading3']))
            story.append(Spacer(1, 3*mm))
            
            # Collect all unique cut lengths
            cut_counts = {}
            for bar in bars:
                for cut in bar.cuts:
                    cut_len = int(cut)
                    cut_counts[cut_len] = cut_counts.get(cut_len, 0) + 1
            
            # Create overview table
            overview_data = [['Länge', 'Anzahl', 'Abhaken']]
            for cut_len in sorted(cut_counts.keys(), reverse=True):
                count = cut_counts[cut_len]
                checkboxes = '☐ ' * count
                overview_data.append([
                    f"{cut_len} mm",
                    f"{count}x",
                    checkboxes[:50] + '...' if len(checkboxes) > 50 else checkboxes
                ])
            
            overview_table = Table(overview_data, colWidths=[30*mm, 20*mm, 120*mm])
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
                ('TOPPADDING', (0, 0), (-1, -1), 1.5*mm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5*mm),
            ]))
            
            story.append(overview_table)
            story.append(Spacer(1, 5*mm))
            
            # Statistics
            total_waste = sum(bar.waste for bar in bars)
            avg_efficiency = sum(bar.efficiency for bar in bars) / len(bars)
            
            stats_data = [
                ['Stangen gesamt:', str(len(bars))],
                ['Schnitte gesamt:', str(sum(len(bar.cuts) for bar in bars))],
                ['Verschnitt gesamt:', f"{total_waste:.0f} mm"],
                ['Ø Effizienz:', f"{avg_efficiency:.1f}%"]
            ]
            
            stats_table = Table(stats_data, colWidths=[40*mm, 30*mm])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
                ('TOPPADDING', (0, 0), (-1, -1), 1.5*mm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5*mm),
            ]))
            
            story.append(stats_table)
            story.append(PageBreak())
        
        # Build PDF
        pdf.build(story)
        
        if output_path:
            return None
        else:
            buffer.seek(0)
            return buffer.getvalue()
