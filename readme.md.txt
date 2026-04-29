# AI Trip Planner (LLM + Python)

## Overview
This project is a simple AI-powered trip planner that generates a structured travel itinerary based on user inputs.

The system combines:
- Deterministic logic (Python)
- LLM-based reasoning
- Structured JSON outputs
- Validation and evaluation layers

---

## How It Works

User Input → Validation → Budget Calculation → Prompt → LLM → JSON Parsing → Evaluation → Output

---

## Features

- User input validation (guardrails)
- Daily budget calculation (deterministic logic)
- Structured JSON output from LLM
- Output validation (evaluation layer)
- Clean and readable itinerary display

---

## Tech Stack

- Python
- OpenAI API
- JSON parsing

---

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt

2.Run the program:
python main.py

Example Output

Day 1 → Visit Eiffel Tower (Paris)
Day 2 → Louvre Museum (Paris)

Key Learning

This project demonstrates how to:

Combine deterministic logic with LLMs
Control LLM outputs using structured prompts
Validate and evaluate AI-generated responses
## Live Demo
https://ai-trip-planner-fenuyejthrpgkup5rv5uvk.streamlit.app/
