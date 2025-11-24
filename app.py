"""
Streamlit web interface for cutting optimization application.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

from optimizer import CuttingOptimizer, Cut
from excel_handler import ExcelHandler
from config import DEFAULT_BAR_LENGTH


def create_efficiency_chart(results: dict):
    """Create a bar chart showing efficiency by material."""
    materials = []
    efficiencies = []
    bar_counts = []
    
    for material_code, data in results.items():
        bars = data['bars']
        if bars:
            avg_efficiency = sum(bar.efficiency for bar in bars) / len(bars)
            materials.append(f"{material_code}\n({data['name']})")
            efficiencies.append(avg_efficiency)
            bar_counts.append(len(bars))
    
    fig = go.Figure(data=[
        go.Bar(
            x=materials,
            y=efficiencies,
            text=[f"{eff:.1f}%" for eff in efficiencies],
            textposition='auto',
            marker_color='lightblue',
            hovertemplate='<b>%{x}</b><br>Effizienz: %{y:.1f}%<br>Stangen: %{customdata}<extra></extra>',
            customdata=bar_counts
        )
    ])
    
    fig.update_layout(
        title="Materialeffizienz",
        xaxis_title="Material",
        yaxis_title="Effizienz (%)",
        yaxis_range=[0, 100],
        height=400
    )
    
    return fig


def create_waste_chart(results: dict):
    """Create a bar chart showing total waste by material."""
    materials = []
    wastes = []
    
    for material_code, data in results.items():
        bars = data['bars']
        if bars:
            total_waste = sum(bar.waste for bar in bars)
            materials.append(f"{material_code}")
            wastes.append(total_waste)
    
    fig = go.Figure(data=[
        go.Bar(
            x=materials,
            y=wastes,
            text=[f"{waste:.0f} mm" for waste in wastes],
            textposition='auto',
            marker_color='lightcoral'
        )
    ])
    
    fig.update_layout(
        title="Verschnitt pro Material",
        xaxis_title="Material",
        yaxis_title="Verschnitt (mm)",
        height=400
    )
    
    return fig


def main():
    st.set_page_config(
        page_title="Zuschnittoptimierung",
        page_icon="📏",
        layout="wide"
    )
    
    st.title("📏 Zuschnittoptimierung")
    st.markdown("**First Fit Decreasing (FFD) Algorithmus für optimale Materialnutzung**")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Einstellungen")
    bar_length = st.sidebar.number_input(
        "Stangenlänge (mm)",
        min_value=100,
        max_value=12000,
        value=DEFAULT_BAR_LENGTH,
        step=100,
        help="Standard-Länge der Stangen/Rohre"
    )
    
    multiplier = st.sidebar.number_input(
        "Stücklistenmultiplikator",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        help="Alle Mengen mit diesem Faktor multiplizieren (z.B. 3 für 3-fache Menge)"
    )
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Optimierung", "📊 Statistiken", "ℹ️ Hilfe"])
    
    with tab1:
        st.header("Excel-Datei hochladen")
        st.markdown("""
        Laden Sie eine Excel-Datei mit folgender Struktur hoch:
        - **Spalte A:** Länge (mm)
        - **Spalte B:** Anzahl
        - **Spalte C:** Materialcode
        - **Spalte D:** Materialname
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Wählen Sie eine Excel-Datei",
                type=['xlsx', 'xls'],
                help="Das Blatt muss 'Stueckliste' heißen"
            )
        
        with col2:
            if st.button("📄 Beispieldatei erstellen", use_container_width=True):
                try:
                    ExcelHandler.create_example_input("example_input.xlsx")
                    st.success("✅ Beispieldatei 'example_input.xlsx' erstellt!")
                    with open("example_input.xlsx", "rb") as file:
                        st.download_button(
                            label="⬇️ Beispiel herunterladen",
                            data=file,
                            file_name="example_input.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                temp_path = "temp_input.xlsx"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Read cuts
                with st.spinner("Daten werden gelesen..."):
                    cuts = ExcelHandler.read_cuts_from_excel(temp_path)
                
                st.success(f"✅ {len(cuts)} Schnitte aus {len(set(c.material_code for c in cuts))} Materialien geladen")
                
                # Preview data
                with st.expander("📋 Datenvorschau"):
                    preview_data = []
                    material_summary = {}
                    
                    for cut in cuts:
                        key = (cut.material_code, cut.material_name)
                        if key not in material_summary:
                            material_summary[key] = []
                        material_summary[key].append(cut.length)
                    
                    for (mat_code, mat_name), lengths in material_summary.items():
                        preview_data.append({
                            'Material': mat_code,
                            'Name': mat_name,
                            'Anzahl Schnitte': len(lengths),
                            'Durchschn. Länge': f"{sum(lengths)/len(lengths):.1f} mm"
                        })
                    
                    st.dataframe(pd.DataFrame(preview_data), use_container_width=True)
                
                # Optimize
                if st.button("🚀 Optimierung starten", type="primary", use_container_width=True):
                    with st.spinner("Optimierung läuft..."):
                        optimizer = CuttingOptimizer(bar_length=bar_length)
                        results = optimizer.optimize_by_material(cuts, multiplier=multiplier)
                        
                        # Store in session state
                        st.session_state['results'] = results
                        st.session_state['bar_length'] = bar_length
                        st.session_state['multiplier'] = multiplier
                    
                    st.success("✅ Optimierung abgeschlossen!")
                    
                    # Display results
                    st.header("🎯 Ergebnisse")
                    
                    for material_code, data in results.items():
                        with st.expander(f"**{material_code}** - {data['name']}", expanded=True):
                            bars = data['bars']
                            
                            # Statistics
                            col1, col2, col3, col4 = st.columns(4)
                            
                            total_bars = len(bars)
                            total_cuts = sum(len(bar.cuts) for bar in bars)
                            total_waste = sum(bar.waste for bar in bars)
                            avg_efficiency = sum(bar.efficiency for bar in bars) / len(bars) if bars else 0
                            
                            col1.metric("Stangen", total_bars)
                            col2.metric("Schnitte", total_cuts)
                            col3.metric("Verschnitt", f"{total_waste:.0f} mm")
                            col4.metric("Ø Effizienz", f"{avg_efficiency:.1f}%")
                            
                            # Bar details table
                            bar_data = []
                            for bar in bars:
                                bar_data.append({
                                    'Stange': bar.bar_number,
                                    'Schnitte': ' / '.join(f"{c:.1f}" for c in bar.cuts),
                                    'Anzahl': len(bar.cuts),
                                    'Gesamt': f"{bar.total_used:.1f} mm",
                                    'Rest': f"{bar.waste:.1f} mm",
                                    'Effizienz': f"{bar.efficiency:.1f}%"
                                })
                            
                            st.dataframe(pd.DataFrame(bar_data), use_container_width=True)
                    
                    # Export results
                    output_path = "zuschnitt_optimiert.xlsx"
                    ExcelHandler.write_results_to_excel(results, output_path, bar_length)
                    
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Ergebnisse als Excel herunterladen",
                            data=file,
                            file_name="zuschnitt_optimiert.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"❌ Fehler bei der Verarbeitung: {str(e)}")
                st.exception(e)
    
    with tab2:
        st.header("📊 Statistiken & Visualisierungen")
        
        if 'results' in st.session_state:
            results = st.session_state['results']
            
            # Overall statistics
            st.subheader("Gesamtübersicht")
            
            total_materials = len(results)
            total_bars_all = sum(len(data['bars']) for data in results.values())
            total_cuts_all = sum(sum(len(bar.cuts) for bar in data['bars']) for data in results.values())
            total_waste_all = sum(sum(bar.waste for bar in data['bars']) for data in results.values())
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Materialien", total_materials)
            col2.metric("Stangen gesamt", total_bars_all)
            col3.metric("Schnitte gesamt", total_cuts_all)
            col4.metric("Verschnitt gesamt", f"{total_waste_all:.0f} mm")
            
            # Charts
            st.subheader("Visualisierungen")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_efficiency_chart(results), use_container_width=True)
            
            with col2:
                st.plotly_chart(create_waste_chart(results), use_container_width=True)
            
        else:
            st.info("ℹ️ Führen Sie zuerst eine Optimierung durch, um Statistiken zu sehen.")
    
    with tab3:
        st.header("ℹ️ Über diese Anwendung")
        
        st.markdown("""
        ### Zuschnittoptimierung mit Best Fit Decreasing (BFD)
        
        Diese Anwendung optimiert Schnittlisten für Stangenmaterial (Rohre, Profile, Stäbe) unter
        Verwendung des **Best Fit Decreasing (BFD)** Algorithmus.
        
        #### 🎯 Funktionsweise
        
        1. **Sortierung:** Alle Schnitte werden nach Länge sortiert (größte zuerst)
        2. **Best Fit:** Jeder Schnitt wird in die Stange mit dem kleinsten verbleibenden Rest platziert
        3. **Neue Stange:** Wenn ein Schnitt nirgends passt, wird eine neue Stange begonnen
        4. **Gruppierung:** Materialien werden separat optimiert
        5. **Multiplikator:** Optional können alle Mengen vervielfacht werden
        
        #### 📊 Vorteile
        
        - ✅ Minimiert Materialverschnitt
        - ✅ Reduziert Anzahl benötigter Stangen
        - ✅ Maximiert Materialausnutzung
        - ✅ Schnelle Berechnung auch für große Datensätze
        
        #### 💡 Tipps
        
        - Verwenden Sie einheitliche Einheiten (empfohlen: mm)
        - Gruppieren Sie ähnliche Materialien mit gleichen Codes
        - Prüfen Sie die Stangenlänge vor der Optimierung
        - Berücksichtigen Sie Sägeblattstärke bei der Längenangabe
        
        #### 🔧 Technische Details
        
        - **Algorithmus:** Best Fit Decreasing (BFD)
        - **Komplexität:** O(n log n + n·m) wobei n=Schnitte, m=Stangen
        - **Sprache:** Python 3.10+
        - **Framework:** Streamlit
        - **Features:** Multiplikator für Serienproduktion
        
        #### 📊 Stücklistenmultiplikator
        
        Der Multiplikator erlaubt es, die gesamte Stückliste mit einem Faktor zu multiplizieren.
        Perfekt für:
        - Serienproduktion (z.B. 10x die gleiche Stückliste)
        - Mehrere identische Aufträge
        - Materialbedarfsplanung
        
        ---
        
        **Version:** 2.0.0  
        **Basierend auf:** VBA Excel Optimierung  
        **Verbesserungen:** BFD-Algorithmus, Multiplikator, Web-UI, Visualisierungen
        """)


if __name__ == "__main__":
    main()
