# Workshop Analysis Demo - Synthetic Data

## Project Purpose

This repository contains synthetic output materials from a fictional strategy workshop for Sustainable Fashion Co., created to serve as demonstration data for an AI-powered workshop analysis tool. These materials simulate the outputs that would be generated during an actual sustainability strategy workshop, allowing for testing and showcasing analysis capabilities without requiring real workshop data.

## Technology Used

The synthetic workshop outputs were primarily generated using Claude 3.7 Sonnet, after initial experiments with Gemini 2.0 Flash which produced results that were less natural and realistic. The Claude-generated content better captures the conversational dynamics, strategic thinking processes, and natural flow of a workshop environment.

## Project Structure

### Background Materials
- `data/context/`: Contains foundational materials that informed the synthetic outputs
  - `workshop_outline.md`: Workshop outline detailing the format, agenda, and objectives
  - `participant_profiles.md`: Profiles for the 20 fictional attendees, including their roles and communication styles

### Workshop Outputs
The outputs are organized by workshop phase, following the structure outlined in the workshop plan:

- `data/phase_1/`: Setting the Stage
  - `setting_the_stage.md`: Transcript of workshop introduction, market overview, and SWOT analysis
  - `swot_analysis_visual_final.svg`: Visual representation of the SWOT analysis in SVG format
  
- `data/phase_2/`: Breakout Sessions
  - Transcripts from the four breakout groups:
    - `breakout_2_1.md`: Circular Business Models
    - `breakout_2_2.md`: Digital Transformation & Customer Experience
    - `breakout_2_3.md`: Sustainable Supply Chain & Materials Innovation
    - `breakout_2_4.md`: Brand Building & Communication
  - `breakout_4_whiteboard.svg`: Experimental brainstorming whiteboard from the Brand Building breakout session
  
- `data/phase_3/`: Synthesis & Prioritization
  - Breakout group report-backs:
    - `session_1_report.md`: Circular Business Models report
    - `session_2_report.md`: Digital Transformation report
    - `session_3_report.md`: Sustainable Supply Chain report
    - `session_4_report.md`: Brand Building report
  - `prioritization_session.md`: Transcript of the prioritization exercise
  - `priority_matrix.md`: Text outline of the priority initiatives
  - `priority_matrix_visual.svg`: Visual priority matrix (Impact vs. Effort) showing categorized initiatives
  
- `data/phase_4/`: Wrap-up & Next Steps
  - `wrap_up_next_steps.md`: Transcript of the CEO's summary, participant feedback, and defined next steps

## Visual Components

The repository includes experimental visual representations in SVG format:
- `swot_analysis_visual_final.svg`: SWOT analysis board (Phase 1)
- `breakout_4_whiteboard.svg`: Brainstorming whiteboard from Brand Building session (Phase 2)
- `priority_matrix_visual.svg`: Priority matrix categorizing initiatives (Phase 3)

These visuals are included for initial review, but may not be incorporated into the actual demonstration due to their realism which is mediocre at best.
