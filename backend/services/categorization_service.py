import sys
import os
# Add root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

def categorize_transactions(df, categories):
    df["category"] = ""

    for idx, row in df.iterrows():
        merchant = str(row["merchant"])

        prompt = f"""
        Merchant: "{merchant}"
        Allowed categories: {categories}
        Respond with ONLY the exact category name.
        """

        try:
            res = client.chat.completions.create(
                model=config.MODEL_NAME_CATEGORIZER,
                temperature=0,
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT_CATEGORIZER},
                    {"role": "user", "content": prompt}
                ]
            )
            predicted = res.choices[0].message.content.strip()

            if predicted not in categories:
                predicted = "Other"

            df.at[idx, "category"] = predicted

        except Exception:
            df.at[idx, "category"] = "Other"

    return df