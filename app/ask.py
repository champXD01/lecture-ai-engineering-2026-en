"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)
"""


"""Lecture 01: ask an LLM, preserve chat history, and measure usage."""

import argparse
import time

from google import genai, genai
from google.genai import errors, types

from app.config import MODEL, api_error_message, get_api_key

DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def print_metrics(response, elapsed: float) -> None:
    """Print response time and token usage when the API provides it."""
    usage = getattr(response, "usage_metadata", None)

    input_tokens = getattr(usage, "prompt_token_count", None)
    output_tokens = getattr(usage, "candidates_token_count", None)

    print(f"\n[response time] {elapsed:.2f} seconds")
    print(f"[input tokens] {input_tokens if input_tokens is not None else 'unavailable'}")
    print(f"[output tokens] {output_tokens if output_tokens is not None else 'unavailable'}")


def ask(question: str, temperature: float | None = None) -> str:
    """Ask one independent question without conversation history."""
    client = genai.Client(api_key=get_api_key())
    start = time.perf_counter()

    config = (
        types.GenerateContentConfig(temperature=temperature)
        if temperature is not None
        else None
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=config,
    )

    elapsed = time.perf_counter() - start
    print_metrics(response, elapsed)
    return response.text or ""


def compare_temperatures(question: str) -> None:
    """Basic homework: ask the same question at three temperatures."""
    for temperature in (0.0, 0.7, 1.0):
        print(f"\n{'=' * 12} temperature={temperature} {'=' * 12}")
        print(f"[question] {question}")
        print(ask(question, temperature=temperature))


def chat_mode(first_question: str) -> None:
    """Implementation homework: retain conversation history between turns."""
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    question = first_question
    print(f"[model] {MODEL}")
    print("Type 'exit' or 'quit' to end the conversation.")

    while True:
        if question.strip().lower() in {"exit", "quit"}:
            break

        print(f"\n[question] {question}")
        start = time.perf_counter()
        response = chat.send_message(question)
        elapsed = time.perf_counter() - start

        print(f"\n[answer]\n{response.text or ''}")
        print_metrics(response, elapsed)

        question = input("\nFollow-up question: ").strip()
        if not question:
            question = input("Please enter a question, or type 'exit': ").strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask an LLM, chat with history, or compare temperatures."
    )
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Enable follow-up questions with conversation history.",
    )
    parser.add_argument(
        "--compare-temperatures",
        action="store_true",
        help="Run the same question at temperatures 0.0, 0.7, and 1.0.",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")

    try:
        if args.chat:
            chat_mode(args.question)
        elif args.compare_temperatures:
            compare_temperatures(args.question)
        else:
            print(f"[question] {args.question}\n")
            print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
