from jinja2 import Environment, PackageLoader, select_autoescape

class PromptManager:
    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("bball_analysis"),
            autoescape=select_autoescape()
        )

    @property
    def gpt_instructions(self):
        return self.env.get_template("gpt_instructions.jinja")

    @property
    def initial_user_prompt(self):
        return self.env.get_template("initial_user_prompt.jinja")

    @property
    def analysis_overview(self):
        return self.env.get_template("analysis_overview.jinja")


Prompts = PromptManager()
