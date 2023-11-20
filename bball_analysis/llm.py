import json
from os import getenv
from time import sleep
from typing import Any, Optional

from dotenv import load_dotenv
from loguru import logger
from pandas import DataFrame
from openai import OpenAI
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.threads.run import RequiredAction, Run
from openai.types.beta.threads.runs.function_tool_call import Function as oaiFunction

from bball_analysis.prompts import Prompts


load_dotenv()
client = OpenAI()

ASSISTANT_NAME = getenv("ASSISTANT_NAME", "BBall Analyst")

# This has to be kept in sync with the Agent.get_dataset() method
# Would be great to have this defined once
get_dataset_definition = {
    "type": "function",
    "function": {
        "name": "get_dataset",
        "description": "Fetch a dataset by name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the dataset"},
            },
            "required": ["name"]
        }
    }
}

assistant_config = {
    "name": ASSISTANT_NAME,
    "instructions": Prompts.gpt_instructions.render(),
    "model": "gpt-3.5-turbo-1106",
    "tools": [get_dataset_definition]
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
        self.datasets: dict[str, DataFrame] = {}

    def add_datasets(self, datasets: dict[str, DataFrame]):
        logger.info(f"Adding datasets {datasets.keys()}")
        self.datasets.update(datasets)
        logger.info(f"Added datasets {self.datasets.keys()}")

    def get_dataset(self, name: str):
        keys = self.datasets.keys()
        logger.info(f"Getting dataset {name} keys {keys}")
        if name in self.datasets:
            return self.datasets[name]

        return None

    def execute_required_action(self, run: Run, action: RequiredAction):
        for tool_call in action.submit_tool_outputs.tool_calls:
            logger.info(f"Executing {tool_call.id} {tool_call.function.name}")
            # execute
            output = self.execute_function_call(tool_call.function)
            if output is None:
                logger.error(f"No response from {tool_call.id} {tool_call.function.name}")

            # submit response to thread
            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=[{
                    "tool_call_id": tool_call.id,
                    "output": str(output)
                }]
            )

    def execute_function_call(self, func: oaiFunction):
        _args = json.loads(func.arguments)
        logger.info(f"Executing {func.name} args {_args}")
        if func.name == "get_dataset":
            return self.get_dataset(**_args)
        else:
            return None

    def set_thread(self):
        logger.info("resetting memory")
        self.thread = self.client.beta.threads.create()

    def chat(self, message: str) -> str:
        """
        Send a message to the assistant and return the response.
        This is forcing an async function into a sync function.
        It would probably be better to have a publisher/subscriber pattern.
        Where subscriber is a background task that polls OpenAI for updates.
        """
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

        """
        poll for status
        "pending", "requires_action" for function calling
        """
        while run.status in ("queued", "in_progress", "pending", "requires_action"):
            logger.info(f"wating for run status {run.status}")

            if run.status == "requires_action":
                self.execute_required_action(run, run.required_action)

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

        return messages.data[0].content[0].text.value
