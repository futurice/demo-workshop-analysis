import os
import streamlit as st
from typing import Dict, Any


class DocumentViewer:
    """Utility for rendering different document types in the Streamlit interface"""

    def render_document(self, document_data: Any, document_name: str):
        """
        Render a document based on its type and content

        Args:
            document_data: The document data to render
            document_name: The name of the document
        """
        # Check if document data is None or empty
        if document_data is None or (
            isinstance(document_data, str) and document_data.strip() == ""
        ):
            st.info(f"No content available for {document_name}")
            return

        # Determine document type by extension or format
        if document_name.endswith((".md", ".markdown")):
            self._render_markdown(document_data)
        elif document_name.endswith(".svg"):
            self._render_svg(document_data, document_name)
        elif document_name.endswith((".png", ".jpg", ".jpeg")):
            self._render_image(document_data, document_name)
        else:
            # Default to rendering as text
            self._render_text(document_data)

    def _render_markdown(self, content: str):
        """Render markdown content"""
        st.markdown(content)

    def _render_text(self, content: str):
        """Render plain text content"""
        st.text_area("Document Content", value=content, height=400, disabled=True)

    def _render_image(self, image_data: str, image_name: str):
        """
        Render image content

        For actual implementation, image_data would be the file path or bytes
        For this demo, we're assuming it's a file path
        """
        st.image(image_data, use_column_width=True)

    def _render_svg(self, svg_data: str, svg_name: str):
        """
        Render SVG content

        For actual implementation, svg_data would be the file content or path
        For this demo, we're assuming it's a file path
        """
        # In a real implementation, you might want to use st.components.v1.html
        # to render the SVG directly. For simplicity, displaying as link here.
        st.write(f"SVG Document: {svg_name}")

        # If svg_data contains the actual SVG content, we could render it with:
        # st.components.v1.html(svg_data, height=400)
