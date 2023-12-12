from enum import Enum
from os import getenv

from dotenv import load_dotenv
from loguru import logger
from llama_index.agent import OpenAIAgent
from llama_index.chat_engine.types import AgentChatResponse
from llama_index.llms import OpenAI as LIOpenAI
from llama_index.tools import FunctionTool
from llama_index.callbacks import (
    CallbackManager,
    LlamaDebugHandler,
)
from pandas import DataFrame
from openai import OpenAI

from bball_analysis.prompts import Prompts


load_dotenv()
client = OpenAI()


VERBOSE = True if getenv("VERBOSE") == "True" else False

class OpenAIModels(Enum):
    """
    Models availible from OpenAI
    Sadly, this is not availible in their library
    """

    gpt3_5_turbo_0613 = "gpt-3.5-turbo-0613"
    gpt3_5_turbo_1106 = "gpt-3.5-turbo-1106"
    gpt3_5_turbo = "gpt-3.5-turbo"
    gpt3_5_turbo_16k = "gpt-3.5-turbo-16k"
    gpt4 = "gpt-4"


class Agent:
    def __init__(self) -> None:
        self._llm = LIOpenAI(model=OpenAIModels.gpt3_5_turbo_1106.value)

        callbacks = None
        if VERBOSE:
            llama_debug = LlamaDebugHandler(print_trace_on_end=True)
            callbacks = CallbackManager([llama_debug])

        tools = [FunctionTool.from_defaults(fn=self.get_dataset)]

        self._li_agnet = OpenAIAgent.from_tools(
            tools=tools,
            llm=self._llm,
            verbose=VERBOSE,
            callback_manager=callbacks,
            system_prompt=Prompts.gpt_instructions.render()
        )
        self.datasets: dict[str, DataFrame] = {}

    def reset(self) -> None:
        """Reset conversation state; wraps llama_index"""
        self._li_agnet.reset()

    def add_datasets(self, datasets: dict[str, DataFrame]):
        logger.info(f"Adding datasets {datasets.keys()}")
        self.datasets.update(datasets)
        logger.info(f"Added datasets {self.datasets.keys()}")

    def get_dataset(self, name: str):
        """Fetch a dataset by name"""
        keys = self.datasets.keys()
        logger.info(f"Getting dataset {name} keys {keys}")
        if name in self.datasets:
            return self.datasets[name]

        return None

    def chat(self, message: str) -> str:
        logger.info(f"begin chat {message}")
        response: AgentChatResponse = self._li_agnet.chat(message)
        return response.response
