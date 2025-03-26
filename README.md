# Workshop Analysis Tool

A Streamlit application for analyzing and categorizing discussion themes from workshop materials using Large Language Models (LLMs). This tool extracts key insights, decisions, and action items from workshop outputs.

## Project Overview

The Workshop Analysis Tool processes and displays synthetic output materials from a fictional strategy workshop for Sustainable Fashion Co. The application allows users to:

1. Browse workshop materials organized by phase
2. Chat with an AI assistant about specific phases or materials
3. Generate a comprehensive workshop analysis with key insights, engagement metrics, and action items

## Project Structure

```
.
├── data/               # Workshop materials organized by phase
│   ├── phase_1/        # Setting the Stage
│   ├── phase_2/        # Breakout Sessions
│   ├── phase_3/        # Sharing Outcomes & Prioritization
│   ├── phase_4/        # Wrap-up & Next Steps
│   └── context/        # Workshop context materials
├── processed_data/     # Processed workshop data for LLM consumption
├── src/                # Application source code
│   ├── components/     # UI components
│   ├── utils/          # Utility functions
│   └── app.py          # Main application entry point
├── .env                # Environment variables for API keys (create from .env.example)
├── .env.example        # Template for environment variables
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Setup Instructions

1. Clone this repository:
   ```
   git clone <repository-url>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Azure OpenAI API access:
   - Create an Azure OpenAI resource in the Azure portal
   - Deploy a GPT-4 model in your Azure OpenAI resource
   - Copy `.env.example` to `.env` and update with your Azure OpenAI credentials

4. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

## Using the Application

1. **Browse Workshop Materials**: Expand each phase tab to view the workshop materials from that phase. Select a document from the dropdown to view its contents.

2. **Chat with AI Assistant**: In each phase tab, use the chat interface to ask questions about the materials in that phase. The AI assistant will analyze the materials and provide relevant answers.

3. **Generate Workshop Analysis**: Click the "Generate Analysis" button in the "Workshop Overview Analysis" section to produce a comprehensive analysis of all workshop materials, including key insights, engagement metrics, and action items.

4. **Chat About Analysis**: After generating the analysis, use the chat interface in the "Workshop Overview Analysis" section to ask follow-up questions about the analysis.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM Integration**: Azure OpenAI (GPT-4)

## Notes

- This application uses synthetic workshop data for demonstration purposes
- The application is configured to use Azure OpenAI's GPT-4 model
- All API calls are made through the Azure OpenAI service
