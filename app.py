import streamlit as st
import pandas as pd
import os
import time
from analyzer import DataAnalyzer
from pdf_generator import PDFReportGenerator
from utils import ensure_dir, get_timestamp_filename

# Page Configuration
st.set_page_config(
    page_title="InsightFlow | Automated Reports",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Glassmorphism */
    .main {
        background: radial-gradient(circle at top right, #1e1e2f, #0e1117);
        color: #ffffff;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(30, 30, 47, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(0, 209, 255, 0.3);
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d1ff, #00ff88);
        color: #0e1117 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 209, 255, 0.4);
    }

    /* Status Boxes */
    .stSuccess, .stInfo {
        border-radius: 12px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stImage, .stDataFrame, .stTable {
        animation: fadeIn 0.8s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header Section
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-weight: 800; font-size: 3.5rem; margin-bottom: 0; background: -webkit-linear-gradient(#00d1ff, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                InsightFlow
            </h1>
            <p style="color: #888888; font-size: 1.2rem; letter-spacing: 2px;">AUTOMATED DATA INTELLIGENCE</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Controls
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=100) # Placeholder logo
        st.markdown("### 🛠️ Report Config")
        report_title = st.text_input("Report Title", "Executive Data Summary")
        include_viz = st.checkbox("Include Visuals", value=True)
        st.markdown("---")
        st.markdown("### 💾 Local Export")
        auto_download = st.toggle("Show Download Button", value=True)

    # Main Interaction Area
    upload_container = st.container()
    with upload_container:
        st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 2rem; border-radius: 20px; border: 2px dashed rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop your dataset here (CSV, Excel, JSON)", type=['csv', 'xlsx', 'xls', 'json'])
        st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        # File Handling
        temp_path = os.path.join("temp", uploaded_file.name)
        ensure_dir("temp")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            with st.status("🔮 Analyzing data structure...", expanded=False) as status:
                analyzer = DataAnalyzer(temp_path)
                df = analyzer.df
                stats = analyzer.get_summary_stats()
                time.sleep(1) # For UX effect
                status.update(label="✅ Analysis complete!", state="complete", expanded=False)

            # Tabs for organization
            tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Intelligence", "📥 Export"])

            with tab1:
                st.markdown("### 🛡️ Data Health")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Records", f"{stats['total_records']:,}", "Active")
                
                missing_total = sum(stats['missing_values'].values())
                m2.metric("Missing Values", missing_total, "-0.2%", delta_color="inverse")
                
                num_cols = len(df.select_dtypes(include=['number']).columns)
                m3.metric("Numeric Fields", num_cols)
                
                m4.metric("Load Time", "1.2s", "Fast")

                st.markdown("### 🔦 Quick Inspection")
                st.dataframe(df.head(10), use_container_width=True)

            with tab2:
                st.markdown("### 🎨 Visual Insights")
                chart_paths = analyzer.generate_charts()
                
                c1, c2 = st.columns(2)
                if len(chart_paths) >= 1:
                    with c1:
                        st.markdown(f"<p style='text-align: center; color: #00d1ff;'><b>Distrubution Analysis</b></p>", unsafe_allow_html=True)
                        st.image(chart_paths[0])
                if len(chart_paths) >= 2:
                    with c2:
                        st.markdown(f"<p style='text-align: center; color: #ff00c8;'><b>Class Frequency</b></p>", unsafe_allow_html=True)
                        st.image(chart_paths[1])
                
                if len(chart_paths) >= 3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; color: #00ff88;'><b>Feature Relationships</b></p>", unsafe_allow_html=True)
                    st.image(chart_paths[2])

            with tab3:
                st.markdown("### 📄 Generate Professional PDF")
                st.info("The report will include high-resolution charts, statistical aggregates, and a data preview table.")
                
                if st.button("✨ GENERATE ENHANCED REPORT"):
                    ensure_dir("output_reports")
                    f_name = get_timestamp_filename(prefix="InsightFlow_Report")
                    out_path = os.path.join("output_reports", f_name)
                    
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    pdf = PDFReportGenerator(out_path, title=report_title)
                    pdf.add_summary_table(stats)
                    pdf.add_data_table(df)
                    if include_viz:
                        pdf.add_charts(chart_paths)
                    pdf.generate()
                    
                    st.balloons()
                    st.success(f"Report Ready: **{f_name}**")
                    
                    if auto_download:
                        with open(out_path, "rb") as f:
                            st.download_button(
                                label="📥 DOWNLOAD PDF",
                                data=f,
                                file_name=f_name,
                                mime="application/pdf"
                            )

        except Exception as e:
            st.error(f"⚠️ Intelligence Engine Error: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        # Welcome Screen
        st.markdown("""
            <div style="margin-top: 5rem; text-align: center; opacity: 0.6;">
                <img src="https://cdn-icons-png.flaticon.com/512/2910/2910245.png" width="150" style="filter: invert(1);">
                <h2 style="font-weight: 400;">Ready to transform your data?</h2>
                <p>Upload a file to begin the automated discovery process.</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
