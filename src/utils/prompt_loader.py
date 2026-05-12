from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

PROMPTS_DIR = BASE_DIR / "prompts"


def load_prompt(relative_path: str) -> str:
    """
    Load prompt file from prompts directory.

    Example:
        load_prompt(\"input/extraction_prompt.txt\")
    """

    prompt_path = PROMPTS_DIR / relative_path

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return prompt_path.read_text(
        encoding="utf-8"
    )