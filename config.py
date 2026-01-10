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