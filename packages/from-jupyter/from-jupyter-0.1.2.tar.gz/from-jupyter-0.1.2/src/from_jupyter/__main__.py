from pathlib import Path

import click

from from_jupyter.export import export_dataframes, export_images
from from_jupyter.gistify import gistify


@click.group()
@click.option("--output-dir", type=click.Path(file_okay=False), default="output")
@click.pass_context
def cli(ctx, output_dir):
    ctx.ensure_object(dict)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    ctx.obj["output_dir"] = output_dir


@cli.command()
@click.argument("file")
@click.argument("personal-token", envvar="GITHUB_PERSONAL_TOKEN")
def gist(file, personal_token):
    gistify(Path(file), personal_token)


@cli.command()
@click.argument("file")
@click.pass_context
def images(ctx, file):
    export_images(ctx.obj["output_dir"], Path(file))


@cli.command()
@click.argument("file")
@click.pass_context
def frames(ctx, file):
    export_dataframes(ctx.obj["output_dir"], Path(file))


if __name__ == "__main__":
    cli()
