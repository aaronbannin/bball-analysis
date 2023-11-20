import click

from bball_analysis.llm import (
    ASSISTANT_NAME,
    delete_assistant,
    get_assistant,
    make_assistant,
    update_assistant
)


@click.group()
def cli():
    pass

@cli.command()
def deploy_agent():
    existing = get_assistant()
    if existing is not None:
        updated = update_assistant(existing.id)
        click.echo(f"Assistant {ASSISTANT_NAME} already exists, updating. {existing.id}")
        return updated.id

    created = make_assistant()
    click.echo(f"Created new assistant {ASSISTANT_NAME} with id {created.id}")
    return created.id

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
