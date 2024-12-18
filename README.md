# Chess AI Bot with OpenAI API

This is a Python-based chess bot that uses the OpenAI API to suggest moves in order to see how well a LLM can play chess. The program ensures that the AI suggests only legal moves using the `python-chess` library and handles retries when illegal moves are suggested.

---

## Features

- Supports **UCI (Universal Chess Interface)** format for moves.
- Detects and prevents illegal moves from being played.
- Provides dynamic feedback to the AI about previous illegal moves to improve suggestions.
- Tracks and avoids repeating invalid moves within a turn.
- Uses the OpenAI GPT model for move generation.

---

## Prerequisites

1. Python 3.8 or above
2. Required libraries:
   - `chess` (Python chess library)
   - `openai` (OpenAI Python client)
3. OpenAI API Key with sufficient quota and access to a compatible model (e.g., `gpt-4`).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chess-ai-bot.git
   cd chess-ai-bot
   
2. Install required dependencies:

    ```bash
    pip install chess openai

3. Set your OpenAI API Key: Replace "your_openai_api_key" in the code with your API key.


