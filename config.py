from dotenv import load_dotenv
import os

# Configuration for SpendWise
DEFAULT_CATEGORIES = [
    {"Category": "Housing & Utilities", "Priority": "Must Keep"},
    {"Category": "Groceries & Essentials", "Priority": "Must Keep"},
    {"Category": "Healthcare & Insurance", "Priority": "Must Keep"},
    {"Category": "Transportation", "Priority": "Should Keep"},
    {"Category": "Work & Education", "Priority": "Should Keep"},
    {"Category": "Dining & Cafés", "Priority": "Can Reduce"},
    {"Category": "Shopping & Personal", "Priority": "Can Reduce"},
    {"Category": "Entertainment & Subscriptions", "Priority": "Can Reduce"},
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

ANAMOLY_DETECTION_Z_THRESHOLD = 1.15