from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta import Assistant, AssistantDeleted, assistant_create_params

load_dotenv()
client = OpenAI()

ASSISTANT_NAME = "BBall Analyst"
INSTRUCTIONS = "You are assisting an analyst for basketball. Give simple and succinct analysis of provided data and suggest strategies to find deeper insights."


def get_assistant() -> Optional[Assistant]:
    all = client.beta.assistants.list()
    existing = [a for a in all if a.name == ASSISTANT_NAME]
    if len(existing) == 0:
        return None

    return existing[0]

def make_assistant() -> Assistant:
    return client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=INSTRUCTIONS,
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview"
    )

class Agent:
    def __init__(self):
        self.client = client

        _assistant = get_assistant()
        if _assistant is None:
            raise Exception("Assistant does not exist; create one using the cli")

        self.assistant = _assistant
        self.thread = self.client.beta.threads.create()

    def chat(self, message: str) -> str:
        return client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
