import streamlit as st
from typing import Dict, Any

from src.components.chat_interface import ChatInterface
from src.utils.azure_openai import generate_overview_analysis


class OverviewAnalysis:
    def __init__(self, all_phase_data: Dict[str, Dict[str, Any]]):
        """
        Initialize the Overview Analysis component

        Args:
            all_phase_data: Dictionary containing all phase data
        """
        self.all_phase_data = all_phase_data
        self.analysis_generated = False

        # Check if we have any documents across all phases
        self.has_documents = any(
            len(phase_data) > 0 for phase_data in all_phase_data.values()
        )

        # Initialize session state for analysis results if not already present
        if "key_insights" not in st.session_state:
            st.session_state.key_insights = None
        if "engagement_metrics" not in st.session_state:
            st.session_state.engagement_metrics = None
        if "action_items" not in st.session_state:
            st.session_state.action_items = None
        if "analysis_generated" not in st.session_state:
            st.session_state.analysis_generated = False

    def generate_analysis(self):
        """Generate workshop overview analysis"""
        with st.spinner("Generating workshop analysis..."):
            # Call Azure OpenAI API to generate the analysis
            analysis_results = generate_overview_analysis(self.all_phase_data)

            # Update session state with results
            st.session_state.key_insights = analysis_results.get("key_insights", [])
            st.session_state.engagement_metrics = analysis_results.get(
                "engagement_metrics", {}
            )
            st.session_state.action_items = analysis_results.get("action_items", [])
            st.session_state.analysis_generated = True

        # Force a rerun to refresh the UI immediately - moved outside spinner
        st.rerun()

    def render(self):
        """Render the overview analysis section"""
        # Add a title for this section
        st.header("Workshop Overview Analysis")

        # If no documents exist, show a clear message
        if not self.has_documents:
            st.warning(
                "No workshop documents are available yet. Please add documents to the phase folders to enable analysis."
            )
            return

        # Only show generate button if analysis hasn't been generated yet
        if not st.session_state.analysis_generated:
            st.write(
                "Click the button below to generate a comprehensive analysis of all workshop materials. "
                "This will include key insights, engagement metrics, and action items."
            )
            if st.button("Generate Analysis", type="primary"):
                self.generate_analysis()
        else:
            # Create two subtabs for Analysis and Chat
            analysis_tab, chat_tab = st.tabs(
                ["Analysis Results", "Chat with AI Assistant"]
            )

            with analysis_tab:
                # Display the generated analysis in columns
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Key Insights")
                    if st.session_state.key_insights:
                        for idx, insight in enumerate(st.session_state.key_insights, 1):
                            st.markdown(
                                f'<div class="key-point-card"><strong>{idx}.</strong> {insight}</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("No key insights generated")

                    st.subheader("Action Items")
                    if st.session_state.action_items:
                        for idx, action in enumerate(st.session_state.action_items, 1):
                            st.markdown(
                                f'<div class="notable-point-card"><strong>{idx}.</strong> {action}</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("No action items generated")

                with col2:
                    st.subheader("Engagement Metrics")
                    if st.session_state.engagement_metrics:
                        for (
                            category,
                            value,
                        ) in st.session_state.engagement_metrics.items():
                            st.markdown(
                                f'<div class="metric-container">{category}: <strong>{value}</strong></div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("No engagement metrics generated")

            with chat_tab:
                # Render chat interface in its own tab
                ChatInterface(
                    phase_id="overview",
                    phase_data=self.all_phase_data,
                    placeholder_text="Ask a question about the Overview Analysis",
                    key_suffix="overview",
                ).render()
