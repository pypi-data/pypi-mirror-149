"""Console script for miniscrapes."""
import sys
import click
from typing import TextIO

from miniscrapes.config import read_config
from miniscrapes.execution import run_scrapers
from miniscrapes.handlers import email_results


@click.group()
def miniscrapes(args=None):
    pass


@miniscrapes.command()
@click.option('--config-file', type=click.File('r'), required=True)
def execute_scrapers(config_file: TextIO):
    config = read_config(config_file)
    results = run_scrapers(config['scrapers'])
    assert(config['handler']['type'] == 'email')
    email_results(
        config['handler']['email'],
        config['name'],
        config['scrapers'], results)


if __name__ == "__main__":
    sys.exit(miniscrapes())  # pragma: no cover
