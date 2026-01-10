from dotenv import load_dotenv
import os

# Configuration for SpendWise
DEFAULT_CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Entertainment",
    "Groceries",
    "Bills",
]

PRIORITY_OPTIONS = ["Must Keep", "Should Keep", "Can Reduce"]



load_dotenv()  # load from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# System prompt used for strict merchant-to-category classification.
SYSTEM_PROMPT_CATEGORIZER = """
You are a strict financial transaction classifier.
Your ONLY job is to assign each merchant to exactly one category
from the allowed list provided by the user.

RULES:
- You MUST choose one of the allowed categories.
- NEVER output a category that is not in the allowed list.
- NEVER create or invent new categories.
- NEVER output explanations or reasoning.
- Output ONLY the exact category text.
- If unsure, choose the closest reasonable category.
"""
# OpenAI model for merchant-to-category classification.
MODEL_NAME_CATEGORIZER = "gpt-4o-mini"