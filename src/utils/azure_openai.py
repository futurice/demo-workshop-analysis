import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import openai conditionally to handle ImportError gracefully
try:
    from openai import AzureOpenAI
except ImportError:
    logging.error("OpenAI library not installed. Please run: pip install openai")
    AzureOpenAI = None

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global variables for client and deployment
client = None
DEFAULT_DEPLOYMENT = "gpt-4o"


def initialize_openai_client():
    """
    Initialize the Azure OpenAI client with proper error handling
    """
    global client, DEFAULT_DEPLOYMENT

    if AzureOpenAI is None:
        logger.error("OpenAI library not available. Cannot initialize client.")
        return

    # Get configuration from environment variables
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")

    # Check if essential configuration is available
    if not api_key or not azure_endpoint:
        logger.warning("Azure OpenAI credentials not found in environment variables")
        return

    try:
        # Initialize the client with minimal parameters
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )

        # Set default deployment name
        DEFAULT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

        logger.info("Azure OpenAI client initialized successfully")
    except TypeError as e:
        # Handle argument errors specifically
        logger.error(f"TypeError during Azure OpenAI client initialization: {e}")
        logger.info(
            "This may be due to an incompatible OpenAI library version. Try 'pip install --upgrade openai'"
        )
    except Exception as e:
        # Handle any other exceptions
        logger.error(f"Error initializing Azure OpenAI client: {e}")


# Initialize the client when module is loaded
initialize_openai_client()


def generate_phase_highlights(
    phase_data: Dict[str, Any], phase_number: int
) -> Dict[str, Any]:
    """
    Generate highlights and summaries for a specific phase's materials

    Args:
        phase_data: Dictionary containing the phase's document data
        phase_number: The phase number (1-4)

    Returns:
        Dictionary containing highlights, key themes, and notable points
    """
    # Phase names for better context
    phase_names = {
        1: "Setting the Stage",
        2: "Breakout Sessions",
        3: "Sharing Outcomes & Prioritization",
        4: "Wrap-up & Next Steps",
    }
    phase_name = phase_names.get(phase_number, f"Phase {phase_number}")

    if not client:
        # Provide demo data for development when Azure OpenAI is not configured
        return {
            "summary": f"This is a demo summary for {phase_name} generated without AI service.",
            "key_themes": [
                f"Key theme 1 for {phase_name}",
                f"Key theme 2 for {phase_name}",
                f"Key theme 3 for {phase_name}",
            ],
            "notable_points": [
                f"Notable point 1 for {phase_name}",
                f"Notable point 2 for {phase_name}",
                f"Notable point 3 for {phase_name}",
            ],
        }

    try:
        # Prepare context from the phase data
        context = _prepare_phase_context(phase_data)

        # Prepare the system message
        system_message = f"""
        You are an expert workshop analyst with experience in summarizing strategic workshop materials.
        Your task is to analyze the provided materials from Phase {phase_number}: {phase_name} 
        and extract key highlights, themes, and notable points.
        
        Be concise yet comprehensive in your analysis.
        Focus on the most important elements and insights from this phase.
        """

        # Prepare the user message
        user_message = f"""
        Create highlights and a summary for the following materials from Phase {phase_number}: {phase_name}
        of a sustainability strategy workshop for Sustainable Fashion Co.

        Extract the following:
        1. Summary: A concise 3-4 sentence summary of this phase's key outcomes
        2. Key Themes: 3-5 main themes or topics discussed in this phase
        3. Notable Points: 3-5 specific notable points, decisions, or insights from this phase
        
        Workshop Materials for Phase {phase_number}:
        {context}
        
        Format your response as a structured JSON with the following keys:
        "summary" (string), "key_themes" (array of strings), and "notable_points" (array of strings).
        """

        # Call the API
        response = client.chat.completions.create(
            model=DEFAULT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.5,
            max_tokens=1000,
            top_p=0.95,
        )

        # Extract and parse the response
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content

            # Try to parse JSON from the response
            try:
                # Find JSON in the response if there's additional text
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1

                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)

                    # Ensure all expected keys are present
                    if not all(
                        k in result for k in ["summary", "key_themes", "notable_points"]
                    ):
                        # Add missing keys with default values
                        result.setdefault(
                            "summary", f"Summary for Phase {phase_number}"
                        )
                        result.setdefault("key_themes", [])
                        result.setdefault("notable_points", [])

                    return result
            except json.JSONDecodeError:
                # If JSON parsing fails, extract insights manually
                logger.warning("Failed to parse JSON from response, using fallback")

            # Fallback method if JSON parsing fails
            summary = response_text
            return {"summary": summary, "key_themes": [], "notable_points": []}
        else:
            return {
                "summary": f"No analysis generated for Phase {phase_number}. Please try again.",
                "key_themes": [],
                "notable_points": [],
            }

    except Exception as e:
        logger.error(f"Error generating phase highlights: {e}")
        return {
            "summary": f"An error occurred while analyzing Phase {phase_number}: {str(e)}",
            "key_themes": [],
            "notable_points": [],
        }


def _prepare_phase_context(phase_data: Dict[str, Any]) -> str:
    """
    Prepare context from phase data for AI analysis

    Args:
        phase_data: Dictionary containing the phase's document data

    Returns:
        Formatted context string
    """
    context_parts = []

    for doc_name, doc_content in sorted(phase_data.items()):
        if isinstance(doc_content, str) and not doc_name.endswith(
            (".png", ".jpg", ".jpeg", ".svg")
        ):
            # For text content, include a sample
            sample = (
                doc_content[:2000] + "..." if len(doc_content) > 2000 else doc_content
            )
            context_parts.append(f"--- {doc_name} ---\n{sample}")
        else:
            # For non-text content, just note its existence
            context_parts.append(f"--- {doc_name} (non-text document) ---")

    return "\n\n".join(context_parts)


def generate_chat_response(
    user_query: str,
    context_data: Dict[str, Any],
    chat_history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    Generate a response to a user query using Azure OpenAI

    Args:
        user_query: The user's query text
        context_data: Relevant context data for the query
        chat_history: Optional chat history for context

    Returns:
        Response text from the AI
    """
    if not client:
        return "AI service is not configured. Please set up Azure OpenAI credentials in your .env file."

    try:
        # Prepare system message with context
        system_message = _prepare_system_message(context_data)

        # Prepare messages array for the API call
        messages = [{"role": "system", "content": system_message}]

        # Add chat history if provided
        if chat_history:
            # Limit chat history to last 10 messages to avoid token limits
            for msg in chat_history[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user query
        messages.append({"role": "user", "content": user_query})

        # Call the API
        response = client.chat.completions.create(
            model=DEFAULT_DEPLOYMENT,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Extract and return the response text
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "No response generated. Please try again."

    except Exception as e:
        logger.error(f"Error generating chat response: {e}")
        return f"An error occurred when calling the AI service: {str(e)}"


def generate_overview_analysis(
    all_phase_data: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate a comprehensive analysis of all workshop materials

    Args:
        all_phase_data: Dictionary containing all phase data

    Returns:
        Dictionary containing key insights, engagement metrics, and action items
    """
    if not client:
        # Provide demo data for development when Azure OpenAI is not configured
        return {
            "key_insights": [
                "AI service is not configured. This is a demo response.",
                "Circular business models represent the greatest opportunity for sustainable growth.",
                "Digital transformation is essential for communicating sustainability efforts.",
                "Supply chain transparency is both a regulatory necessity and consumer demand.",
                "Employee engagement in sustainability initiatives drives innovation.",
            ],
            "engagement_metrics": {
                "Participation Rate": "90%",
                "Ideas Generated": "42",
                "Action Items Identified": "12",
                "Cross-Department Collaboration": "High",
            },
            "action_items": [
                "Launch product resale platform pilot by Q3 (Owner: Ben C.)",
                "Implement blockchain-based supply chain tracking system (Owner: David R.)",
                "Develop sustainability training program for all employees (Owner: Sarah C.)",
                "Create digital sustainability reporting dashboard (Owner: Raj P.)",
                "Establish materials innovation partnership with university (Owner: Kenji T.)",
            ],
        }

    try:
        # Prepare context from all phases
        context = _prepare_all_phases_context(all_phase_data)

        # Prepare the system message
        system_message = """
        You are an expert workshop analyst with experience analyzing strategic meetings and workshops.
        Your task is to analyze the provided workshop materials and extract key insights, 
        identify engagement metrics, and list clear action items.
        
        Focus on the most important and actionable outcomes from the workshop.
        Provide concise, clear, and specific information in your analysis.
        """

        # Prepare the user message
        user_message = f"""
        Analyze the following workshop materials from a sustainability strategy workshop for Sustainable Fashion Co.
        Extract the following:
        
        1. Key Insights: Identify 5-7 most important strategic insights from the workshop
        2. Engagement Metrics: Provide quantitative assessment of participation and engagement
        3. Action Items: List 5-10 specific and actionable next steps with clear ownership when possible
        
        Workshop Materials:
        {context}
        
        Format your response as a structured JSON with the following keys:
        "key_insights" (array of strings), "engagement_metrics" (object with metric names and values), and "action_items" (array of strings).
        """

        # Call the API
        response = client.chat.completions.create(
            model=DEFAULT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.5,
            max_tokens=2000,
            top_p=0.95,
        )

        # Extract and parse the response
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content

            # Try to parse JSON from the response
            try:
                # Find JSON in the response if there's additional text
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1

                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)

                    # Ensure all expected keys are present
                    if not all(
                        k in result
                        for k in ["key_insights", "engagement_metrics", "action_items"]
                    ):
                        # Add missing keys with default values
                        result.setdefault("key_insights", [])
                        result.setdefault("engagement_metrics", {})
                        result.setdefault("action_items", [])

                    return result

            except json.JSONDecodeError:
                # If JSON parsing fails, return a structured response based on text
                logger.warning("Failed to parse JSON from response, using fallback")

            # Fallback: return a structured response with the full text in insights
            return {
                "key_insights": [response_text],
                "engagement_metrics": {
                    "Analysis Generation Time": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                },
                "action_items": [
                    "Review the generated insights and formulate action items"
                ],
            }
        else:
            return {
                "key_insights": ["No analysis generated. Please try again."],
                "engagement_metrics": {},
                "action_items": [],
            }

    except Exception as e:
        logger.error(f"Error generating overview analysis: {e}")
        return {
            "key_insights": [f"An error occurred: {str(e)}"],
            "engagement_metrics": {
                "Error Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            "action_items": [
                "Contact support for assistance with the analysis generation"
            ],
        }


def _prepare_system_message(context_data: Dict[str, Any]) -> str:
    """
    Prepare a system message with relevant context data

    Args:
        context_data: Dictionary of context data

    Returns:
        Formatted system message string
    """
    # First, extract any generated highlights or summary data
    generated_content = []
    document_content = []

    for doc_name, doc_content in context_data.items():
        if isinstance(doc_content, str):
            if doc_name.startswith("[GENERATED]"):
                # This is AI-generated content like highlights and summaries
                generated_content.append((doc_name, doc_content))
            else:
                # This is a regular document
                document_content.append((doc_name, doc_content))

    # Build the system message with generated content first
    system_message = """
    You are an expert AI assistant analyzing materials from a sustainability strategy workshop for Sustainable Fashion Co.
    
    Answer questions based on the following workshop materials and their analyses:
    """

    # Add generated content (highlights, summaries) first for priority
    if generated_content:
        system_message += "\n\n=== AI-GENERATED ANALYSES ===\n"
        for doc_name, doc_content in generated_content:
            # Include the full content for generated analyses
            system_message += f"\n{doc_name}:\n{doc_content}\n"

    # Add regular document content
    if document_content:
        system_message += "\n\n=== WORKSHOP DOCUMENTS ===\n"
        for doc_name, doc_content in document_content:
            # Create a condensed version of regular documents
            sample = (
                doc_content[:1000] + "..." if len(doc_content) > 1000 else doc_content
            )
            system_message += f"\n--- Document: {doc_name} ---\n{sample}\n"

    # Add final instructions
    system_message += """
    
    Provide concise, factual responses based on the information in these materials.
    When answering questions about highlights, summaries, or analyses, prioritize information from the AI-generated analyses.
    If asked about specific document details not covered in the analyses, reference the workshop documents.
    If you don't know or the information is not in the materials, say so clearly.
    """

    return system_message


def _prepare_all_phases_context(all_phase_data: Dict[str, Dict[str, Any]]) -> str:
    """
    Prepare a consolidated context from all phase data

    Args:
        all_phase_data: Dictionary containing all phase data

    Returns:
        Consolidated context string
    """
    context_parts = []

    for phase_id, phase_data in sorted(all_phase_data.items()):
        phase_context = f"\n\n=== {phase_id.upper()} ===\n"

        for doc_name, doc_content in sorted(phase_data.items()):
            if isinstance(doc_content, str) and not doc_name.endswith(
                (".png", ".jpg", ".jpeg", ".svg")
            ):
                # For text content, include a sample
                sample = (
                    doc_content[:2000] + "..."
                    if len(doc_content) > 2000
                    else doc_content
                )
                phase_context += f"\n--- {doc_name} ---\n{sample}\n"
            else:
                # For non-text content, just note its existence
                phase_context += f"\n--- {doc_name} (non-text document) ---\n"

        context_parts.append(phase_context)

    return "\n".join(context_parts)
