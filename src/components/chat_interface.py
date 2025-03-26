import streamlit as st
from typing import Dict, List, Any, Optional
import json

from src.utils.azure_openai import generate_chat_response


class ChatInterface:
    def __init__(
        self,
        phase_id: str,
        phase_data: Dict[str, Any],
        placeholder_text: str,
        key_suffix: str,
    ):
        """
        Initialize the chat interface component

        Args:
            phase_id: Identifier for the phase or section
            phase_data: Data for the relevant phase
            placeholder_text: Help text to display in the input box
            key_suffix: Suffix for session state keys to avoid conflicts
        """
        self.phase_id = phase_id
        self.phase_data = phase_data
        self.placeholder_text = placeholder_text
        self.key_suffix = key_suffix

        # Initialize chat history in session state if not already present
        if f"chat_history_{key_suffix}" not in st.session_state:
            st.session_state[f"chat_history_{key_suffix}"] = []

    def get_enhanced_context(self) -> Dict[str, Any]:
        """
        Enhances the context with highlights and summaries if available

        Returns:
            Enhanced context data including both original documents and generated highlights
        """
        enhanced_context = dict(self.phase_data)  # Start with a copy of the phase data

        # For phase-specific chat interfaces, include the phase highlights
        if self.phase_id.startswith("phase_"):
            highlights_key = f"highlights_{self.phase_id}"
            if highlights_key in st.session_state and st.session_state[highlights_key]:
                # Create a structured representation of the highlights
                highlights = st.session_state[highlights_key]

                # Add the highlights as a structured document in the context
                highlights_text = f"""
                === PHASE HIGHLIGHTS AND SUMMARIES ===
                
                SUMMARY:
                {highlights.get('summary', 'No summary available')}
                
                KEY THEMES:
                {self._format_list(highlights.get('key_themes', []))}
                
                NOTABLE POINTS:
                {self._format_list(highlights.get('notable_points', []))}
                """

                enhanced_context["[GENERATED] Highlights and Summaries"] = (
                    highlights_text
                )

        # For overview chat interface, include the overview analysis
        elif self.phase_id == "overview":
            if (
                hasattr(st.session_state, "key_insights")
                and hasattr(st.session_state, "engagement_metrics")
                and hasattr(st.session_state, "action_items")
            ):
                # Create a structured representation of the overview analysis
                overview_text = f"""
                === WORKSHOP OVERVIEW ANALYSIS ===
                
                KEY INSIGHTS:
                {self._format_list(st.session_state.key_insights or [])}
                
                ENGAGEMENT METRICS:
                {self._format_dict(st.session_state.engagement_metrics or {})}
                
                ACTION ITEMS:
                {self._format_list(st.session_state.action_items or [])}
                """

                enhanced_context["[GENERATED] Workshop Overview Analysis"] = (
                    overview_text
                )

        # Add a special section for topic mapping
        if hasattr(st.session_state, "topic_mapping"):
            enhanced_context["[INDEX] Topic to Document Mapping"] = json.dumps(
                st.session_state.topic_mapping
            )

        return enhanced_context

    def _format_list(self, items: List[str]) -> str:
        """Format a list of items as a numbered list string"""
        if not items:
            return "None available"
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def _format_dict(self, data: Dict[str, Any]) -> str:
        """Format a dictionary as a string with key-value pairs"""
        if not data:
            return "None available"
        return "\n".join(f"- {key}: {value}" for key, value in data.items())

    def render(self):
        """Render the chat interface"""
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state[f"chat_history_{self.key_suffix}"]:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])

        # Chat input
        user_input = st.chat_input(
            placeholder=self.placeholder_text, key=f"chat_input_{self.key_suffix}"
        )

        # Handle user input
        if user_input:
            # Add user message to chat history
            st.session_state[f"chat_history_{self.key_suffix}"].append(
                {"role": "user", "content": user_input}
            )

            # Display user message
            st.chat_message("user").write(user_input)

            # Get enhanced context data including highlights/summaries
            enhanced_context = self.get_enhanced_context()

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_chat_response(
                        user_input,
                        enhanced_context,
                        st.session_state[f"chat_history_{self.key_suffix}"],
                    )
                    st.write(response)

            # Add assistant response to chat history
            st.session_state[f"chat_history_{self.key_suffix}"].append(
                {"role": "assistant", "content": response}
            )
