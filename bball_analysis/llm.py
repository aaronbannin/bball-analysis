from time import sleep
from typing import Optional

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI
from openai.types.beta import Assistant, AssistantDeleted

from bball_analysis.prompts import Prompts


load_dotenv()
client = OpenAI()

ASSISTANT_NAME = "BBall Analyst"


assistant_config = {
    "name": ASSISTANT_NAME,
    "instructions": Prompts.gpt_instructions.render(),
    "model": "gpt-3.5-turbo-1106"
}

def get_assistant() -> Optional[Assistant]:
    all = client.beta.assistants.list()
    existing = [a for a in all if a.name == ASSISTANT_NAME]
    if len(existing) == 0:
        return None

    return existing[0]

def update_assistant(assistant_id: str) -> Assistant:
    return client.beta.assistants.update(
        assistant_id=assistant_id,
        **assistant_config
    )

def make_assistant() -> Assistant:
    return client.beta.assistants.create(**assistant_config)

def delete_assistant(assistant_id: str) -> AssistantDeleted:
    return client.beta.assistants.delete(assistant_id=assistant_id)

class Agent:
    def __init__(self):
        self.client = client

        _assistant = get_assistant()
        if _assistant is None:
            raise Exception("Assistant does not exist; create one using the cli")

        self.assistant = _assistant
        self.set_thread()

    def set_thread(self):
        logger.info("resetting memory")
        self.thread = self.client.beta.threads.create()

    def chat(self, message: str) -> str:
        logger.info(f"begin chat {message}")
        client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        logger.info("submitting run")
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

        # poll of status
        while run.status in ("queued", "in_progress"):
            logger.info(f"wating for run status {run.status}")
            run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            sleep(0.5)

        if run.status != "completed":
            raise Exception(f"Run did not complete {run}")

        messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

        logger.info("LLM response")
        logger.info(messages)
        return messages.data[0].content[0].text.value
