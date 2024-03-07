from models.users import UserPrompt
import logging
from langchain_utils.prompts.initial_prompts import (
    blockchain_and_ai_template,
    stacks_template,
)


def fetch_user_generated_prompts(user_id):
    try:
        user_prompts = UserPrompt.query.filter_by(user_id=user_id).all()
        logging.info(f"User Prompts inside Prompt Utils {user_prompts}")
        return [
            {"question": prompt.prompt, "answer": prompt.response}
            for prompt in user_prompts
        ]
    except Exception as e:
        print(f"Error fetching user prompts: {e}")


def combine_prompt_sets(user_id, *prompt_sets):
    """
    These are a combination of predefined prompts and questions and answers save from
    the users interaction with the LLM to be turned into prompts
    """
    combined = []
    user_prompts = fetch_user_generated_prompts(user_id)
    if user_prompts:
        combined.extend(user_prompts)

    for prompts in prompt_sets:
        for prompt in prompts:
            # Ensure each propmt is in the correct format
            if isinstance(prompt, dict) and "question" in prompt and "answer" in prompt:
                combined.append(prompt)
            else:
                logging.warning(f"Prompt skipped due to format inconsitency")
    logging.info(f"Combined prompts in utils: {combined}")
    return combined


if __name__ == "__main__":
    fetch_user_generated_prompts()
    combine_prompt_sets()
