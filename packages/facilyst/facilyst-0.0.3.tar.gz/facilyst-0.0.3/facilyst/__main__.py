"""CLI commands."""

import click


@click.group()
def cli():
    """CLI command with no arguments. Does nothing."""
    pass
