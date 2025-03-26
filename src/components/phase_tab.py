import os
import streamlit as st
from typing import Dict, List, Any

from src.components.chat_interface import ChatInterface
from src.utils.document_viewer import DocumentViewer
from src.utils.azure_openai import generate_phase_highlights


class PhaseTab:
    def __init__(self, phase_id: str, phase_data: Dict[str, Any], phase_number: int):
        """
        Initialize the Phase Tab component

        Args:
            phase_id: The identifier for this phase (e.g., 'phase_1')
            phase_data: Dictionary containing document data for this phase
            phase_number: The number of the phase (1-4)
        """
        self.phase_id = phase_id
        self.phase_data = phase_data
        self.phase_number = phase_number
        self.document_viewer = DocumentViewer()

        # Initialize session state for phase highlights if not already present
        if f"highlights_{phase_id}" not in st.session_state:
            st.session_state[f"highlights_{phase_id}"] = None
        if f"highlights_generated_{phase_id}" not in st.session_state:
            st.session_state[f"highlights_generated_{phase_id}"] = False

    def generate_highlights(self):
        """Generate highlights and summaries for this phase"""
        with st.spinner(f"Generating highlights for Phase {self.phase_number}..."):
            # Call Azure OpenAI to generate the highlights
            highlights = generate_phase_highlights(self.phase_data, self.phase_number)

            # Update session state with results
            st.session_state[f"highlights_{self.phase_id}"] = highlights
            st.session_state[f"highlights_generated_{self.phase_id}"] = True

    def render(self):
        """Render the phase tab content with documents and chat interface"""
        if not self.phase_data:
            st.warning(f"No data available for {self.phase_id}")
            return

        # Check if there are any documents in this phase
        has_documents = len(self.phase_data) > 0

        # Create tabs for Documents and Highlights
        doc_tab, highlights_tab = st.tabs(["Documents", "Highlights and Summaries"])

        with doc_tab:
            # Display documents for this phase
            st.markdown("<h3>Workshop Materials</h3>", unsafe_allow_html=True)

            # Check if there are any documents
            if not has_documents:
                st.info("No documents available for this phase yet.")
            else:
                # Create columns for better layout with documents on the left and previews on the right
                col1, col2 = st.columns([1, 2])

                with col1:
                    # List of documents with selectable items
                    doc_names = list(self.phase_data.keys())
                    selected_doc = st.selectbox(
                        "Select a document to view:",
                        doc_names,
                        key=f"{self.phase_id}_doc_select",
                    )

                with col2:
                    # Only display document if we have documents and one is selected
                    if doc_names and selected_doc:
                        # Render document directly without the container div
                        self.document_viewer.render_document(
                            self.phase_data[selected_doc], selected_doc
                        )
                    else:
                        st.info("Please select a document to view.")

        with highlights_tab:
            # Show Highlights and Summaries section
            st.markdown(
                f"<h3>Highlights and Summaries - Phase {self.phase_number}</h3>",
                unsafe_allow_html=True,
            )

            if not has_documents:
                st.info(
                    "No documents available to generate highlights. Please add documents to this phase first."
                )
            else:
                # Only show generate button if highlights haven't been generated yet
                if not st.session_state[f"highlights_generated_{self.phase_id}"]:
                    if st.button(
                        f"Generate Highlights for Phase {self.phase_number}",
                        key=f"generate_highlights_{self.phase_id}",
                    ):
                        self.generate_highlights()

                # Display the generated highlights if available
                if st.session_state[f"highlights_generated_{self.phase_id}"]:
                    highlights = st.session_state[f"highlights_{self.phase_id}"]

                    if highlights:
                        # Display summary in a styled container - fixed to avoid empty div
                        st.markdown(
                            '<div class="summary-section"><h4>Summary</h4>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(highlights.get("summary", "No summary available"))
                        st.markdown("</div>", unsafe_allow_html=True)

                        # Display key themes section
                        st.markdown("<h4>Key Themes</h4>", unsafe_allow_html=True)
                        key_themes = highlights.get("key_themes", [])
                        if key_themes:
                            for i, theme in enumerate(key_themes, 1):
                                st.markdown(
                                    f'<div class="key-point-card"><strong>{i}.</strong> {theme}</div>',
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("No key themes identified")

                        # Display notable points section
                        st.markdown("<h4>Notable Points</h4>", unsafe_allow_html=True)
                        notable_points = highlights.get("notable_points", [])
                        if notable_points:
                            for i, point in enumerate(notable_points, 1):
                                st.markdown(
                                    f'<div class="notable-point-card"><strong>{i}.</strong> {point}</div>',
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("No notable points identified")

        # Only show chat interface if we have documents
        if has_documents:
            # Add a divider before the chat interface
            st.divider()

            # Add chat interface for this phase
            st.markdown(f"<h3>Chat with AI Assistant</h3>", unsafe_allow_html=True)
            # Render chat interface directly without container
            ChatInterface(
                phase_id=self.phase_id,
                phase_data=self.phase_data,
                placeholder_text=f"Ask a question about Phase {self.phase_number} materials",
                key_suffix=f"phase_{self.phase_number}",
            ).render()
        else:
            st.info(
                "Chat interface will be available once documents are added to this phase."
            )
