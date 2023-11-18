import click

from bball_analysis.llm import (
    delete_assistant,
    get_assistant,
    make_assistant,
    update_assistant
)


ASSISTANT_NAME = "BBall Analyst"


@click.group()
def cli():
    pass

@cli.command()
def make_agent():
    existing = get_assistant()
    if existing is not None:
        click.echo(f"Assistant {ASSISTANT_NAME} already exists, skipping creation. {existing.id}")
        return existing.id

    assistant = make_assistant()
    click.echo(f"Created new assistant {ASSISTANT_NAME} with id {assistant.id}")

@cli.command()
def update_agent():
    existing = get_assistant()
    if existing is None:
        click.echo(f"Cannot update; {ASSISTANT_NAME} does not exist.")
        return

    response = update_assistant(existing.id)
    click.echo(response)

@cli.command()
def delete_agent():
    existing = get_assistant()
    if existing is None:
        click.echo(f"Cannot delete; {ASSISTANT_NAME} does not exist.")
        return

    response = delete_assistant(existing.id)
    click.echo(response)


if __name__ == "__main__":
    cli()
