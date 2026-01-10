import sys
import os
# Add root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config
from openai import OpenAI


client = OpenAI(api_key=config.OPENAI_API_KEY)

def recommend_savings_actions(category_spending, priority_map, goal_amount):
    """
    Uses OpenAI to generate personalized saving suggestions
    based on:
      - category totals
      - priorities (Must Keep, Should Keep, Can Reduce)
      - user savings goal
    """

    if goal_amount <= 0:
        return "No savings goal provided."

    # Build prompt data
    spending_lines = "\n".join(
        f"{cat}: ${amt:.2f} ({priority_map.get(cat, 'Unknown')})"
        for cat, amt in category_spending.items()
    )

    prompt = f"""
    You are a financial budgeting assistant.

    The user wants to save ${goal_amount:.2f} this month.

    Here is the user's category spending and their priorities:
    {spending_lines}

    Rules:
    - MUST KEEP categories should not be reduced unless absolutely necessary.
    - SHOULD KEEP can be trimmed moderately.
    - CAN REDUCE categories are the first targets for savings.
    - Your job is to propose actionable changes describing exactly how the user can reach their savings goal.
    - Provide clear specific suggestions (e.g., "cut dining by $40", "reduce shopping by $60").
    - Keep the tone supportive and practical.

    Respond with 3–5 bullet points.
    """

    try:
        res = client.chat.completions.create(
            model=config.MODEL_NAME_CATEGORIZER,
            temperature=0.5,
            messages=[
                {"role": "system", "content": "You generate financial saving recommendations."},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content.strip()

    except Exception:
        return "OpenAI unavailable — unable to generate personalized recommendations."