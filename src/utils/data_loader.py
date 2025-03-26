import os
import json
from typing import Dict, Any, List
from pathlib import Path


def load_all_phase_data() -> Dict[str, Dict[str, Any]]:
    """
    Load all phase data from the processed data directory

    Returns:
        Dictionary of phase data with keys like 'phase_1', 'phase_2', etc.
    """
    # Define the processed data directory and structure
    data_dir = Path("processed_data")

    # If processed data doesn't exist yet, process and save it
    if not data_dir.exists() or not any(data_dir.iterdir()):
        process_raw_data()

    # Load the processed data
    phase_data = {}
    for phase_num in range(1, 5):
        phase_file = data_dir / f"phase_{phase_num}.json"
        if phase_file.exists():
            with open(phase_file, "r", encoding="utf-8") as f:
                phase_data[f"phase_{phase_num}"] = json.load(f)
        else:
            # If file doesn't exist, include an empty dict
            phase_data[f"phase_{phase_num}"] = {}

    return phase_data


def process_raw_data():
    """
    Process raw workshop data from data directory and save as JSON
    in the processed_data directory for easy loading
    """
    # Define the source and target directories
    # Use absolute path for data directory
    raw_data_dir = Path("/Users/rali.ivanova/projects/demo-workshop-analysis/data")
    processed_data_dir = Path("processed_data")
    processed_data_dir.mkdir(exist_ok=True)

    # Process each phase directory
    for phase_num in range(1, 5):
        phase_dir = raw_data_dir / f"phase_{phase_num}"
        if not phase_dir.exists():
            # Create an empty JSON file for this phase to prevent issues
            output_file = processed_data_dir / f"phase_{phase_num}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({}, f)
            continue

        phase_data = {}

        # Process each file in the phase directory
        for file_path in phase_dir.glob("**/*"):
            if file_path.is_file():
                # Skip certain file types or temporary files
                if file_path.name.startswith(".") or file_path.name.endswith(
                    (".pyc", ".pyo", ".pyd")
                ):
                    continue

                # Use relative path as document key
                doc_key = file_path.name

                # Process based on file type
                if file_path.suffix.lower() in [".md", ".markdown", ".txt"]:
                    # Read text files
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    phase_data[doc_key] = content
                elif file_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".svg"]:
                    # For image files, store the path
                    phase_data[doc_key] = str(file_path)
                # Add more file type handlers as needed

        # Save the processed phase data
        output_file = processed_data_dir / f"phase_{phase_num}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(phase_data, f, ensure_ascii=False, indent=2)

    # Also process context data if needed
    context_dir = raw_data_dir / "context"
    if context_dir.exists():
        context_data = {}

        for file_path in context_dir.glob("**/*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                doc_key = file_path.name

                if file_path.suffix.lower() in [".md", ".markdown", ".txt"]:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    context_data[doc_key] = content

        # Save the processed context data
        output_file = processed_data_dir / "context.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(context_data, f, ensure_ascii=False, indent=2)
