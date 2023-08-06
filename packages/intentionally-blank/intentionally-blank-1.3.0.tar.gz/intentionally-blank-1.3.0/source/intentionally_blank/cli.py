import logging
import sys
from exit_codes import ExitCode

import click

from intentionally_blank import api
from intentionally_blank.formatter import formatter_names

from .version import __version__

log_levels = tuple(logging._levelToName.values())

fmt_names = formatter_names()


def _validate_optional_positive_integer(ctx, param, value):
    message = f"{param.name} needs to be a positive integer"
    if value is None:
        return value
    try:
        float_inc = float(value)
        int_inc = int(value)
    except ValueError:
        raise click.BadParameter(message)
    if float_inc != int_inc:
        raise click.BadParameter(message)
    if int_inc < 1:
        raise click.BadParameter(message)
    return int_inc


@click.group()
@click.option(
    "--verbosity",
    default="WARNING",
    help="The logging level to use.",
    type=click.Choice(log_levels, case_sensitive=True),
)
@click.version_option(version=__version__)
def cli(verbosity):
    logging_level = getattr(logging, verbosity)
    logging.basicConfig(level=logging_level)


@cli.command(name="format")
@click.option("--format", type=click.Choice(fmt_names, case_sensitive=True), multiple=True)
@click.option("--tab-size", callback=_validate_optional_positive_integer, help="Tab size in spaces")
@click.option("--in-place", "-i", is_flag=True, default=False)
# TODO: Use nargs here
@click.argument('input', type=click.Path(exists=True, dir_okay=False, allow_dash=True, resolve_path=True))
@click.argument('output', type=click.Path(dir_okay=False, allow_dash=True, resolve_path=True), required=False)
def format(input, output, format, tab_size=None, in_place=False):
    try:
        api.format_from_path_to_path(in_filepath=input, out_filepath=output, format_names=format, tab_size=tab_size, in_place=in_place)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(ExitCode.NOINPUT)
    sys.exit(ExitCode.OK)


@cli.command(name="list-formats")
def list_format():
    names = api.list_formats()
    for name in names():
        print(name)
    return ExitCode.OK


@cli.command(name="describe-format")
@click.option("--format", type=click.Choice(fmt_names, case_sensitive=True), required=True)
def describe_format(format):
    description = api.describe_formatter(format_name=format)
    print(description)
    return ExitCode.OK


if __name__ == "__main__":
    cli()

