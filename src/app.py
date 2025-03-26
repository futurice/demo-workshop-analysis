import os
import streamlit as st
from typing import Dict, List, Any
import datetime

from src.components.phase_tab import PhaseTab
from src.components.overview_analysis import OverviewAnalysis
from src.utils.data_loader import load_all_phase_data


def local_css(file_name):
    """Load and apply local CSS"""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    # Configure page settings
    st.set_page_config(
        page_title="Workshop Analysis Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), "static", "style.css")
    local_css(css_path)

    # Apply styling
    st.markdown(
        """
        <style>
        /* Set background color */
        .stApp {
            background-color: #EBF5FB;
        }
        
        /* Style for main content frame */
        section.main > div {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin: 20px;
            border: 1px solid #E5E8E8;
        }
        
        /* Remove default Streamlit paddings */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }
        
        /* Fix header padding */
        header {
            padding-left: 20px !important;
            padding-right: 20px !important;
        }
        
        /* Keep footer out of the way */
        footer {
            display: none !important;
        }
        
        /* Better tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            margin-top: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 4px 4px 0 0;
            padding: 10px 16px;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #2E86C1;
            color: white;
        }
        
        /* Direct styling for headers */
        h1 {
            color: #1A5276 !important;
            font-weight: 700 !important;
        }
        
        h2 {
            color: #2874A6 !important;
            font-weight: 600 !important;
        }
        
        h3 {
            color: #2E86C1 !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.title("Sustainable Fashion Co. - Workshop Analysis Tool")
    st.markdown("AI-powered insights from strategy workshop materials")

    # Load data
    phase_data = load_all_phase_data()

    # Main content
    tab1, tab2 = st.tabs(["Phase Details", "Workshop Overview"])

    with tab1:
        phases = [
            "Phase 1: Setting the Stage",
            "Phase 2: Breakout Sessions",
            "Phase 3: Sharing Outcomes & Prioritization",
            "Phase 4: Wrap-up & Next Steps",
        ]

        for i, phase_name in enumerate(phases, 1):
            with st.expander(phase_name, expanded=(i == 1)):
                PhaseTab(f"phase_{i}", phase_data[f"phase_{i}"], i).render()

    with tab2:
        OverviewAnalysis(phase_data).render()

    # Footer
    st.divider()
    year = datetime.datetime.now().year
    st.caption(f"Workshop Analysis Tool © {year} | Powered by Azure OpenAI")


if __name__ == "__main__":
    main()
