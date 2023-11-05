import click
import logging
import os
from datetime import date
from . import retidy
from . import subtitle_mover
from . import jellyfin_to_notion
from .helper import JellyfinOptions, NotionOptions

CONTEXT_SETTINGS = dict(default_map={"runserver": {"port": 5000}})


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--dry-run/--no-dry-run", default=False)
@click.pass_context
def cli(ctx, debug: bool, dry_run: bool):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj["debug"] = debug
    ctx.obj["dry_run"] = dry_run

    logging.basicConfig()
    if debug:
        logging.getLogger().setLevel(logging.NOTSET)
    else:
        logging.getLogger().setLevel(logging.INFO)

    click.echo(f"debug is {'on' if ctx.obj['debug'] else 'off'}")
    click.echo(f"dry_run is {'on' if ctx.obj['dry_run'] else 'off'}")


@cli.command("retidy")
@click.option(
    "-i",
    "--input-dir",
    "input_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, writable=True
    ),
)
@click.option("--format", type=click.STRING, default="$(actor)/$(avid)/$(avid)")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(
        [retidy.RunMode.FLAT.value, retidy.RunMode.SEPARATED.value],
        case_sensitive=False,
    ),
    default=retidy.RunMode.FLAT.value,
)
@click.pass_context
def retidy_command(ctx, input_dir, output_dir, format, mode):
    runner = retidy.RetidyFilesRunner(
        dry_run=ctx.obj["dry_run"],
        input_dir=input_dir,
        output_dir=output_dir,
        video_file_path_opts=retidy.VideoFilePathOpts(
            format=format,
        ),
        run_mode=retidy.RunMode(mode),
    )
    runner.run()


@cli.command("subtitle_mover")
@click.option(
    "-s",
    "--subtitle-dir",
    "subtitle_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
@click.option(
    "-d",
    "--target-dir",
    "target_dir",
    type=click.STRING,
    default=lambda: os.environ.get("USER", ""),
)
@click.option(
    "--overwrite",
    type=click.BOOL,
    default=False,
)
@click.pass_context
def subtitle_mover_command(ctx, subtitle_dir, target_dir, overwrite):
    runner = subtitle_mover.SubtitleMover(
        dry_run=ctx.obj["dry_run"],
        subtitle_dir=subtitle_dir,
        target_dir=target_dir,
        overwrite=overwrite,
    )
    runner.run()


@cli.command("jellyfin_to_notion")
@click.option(
    "--jellyfin-endpoint",
    type=click.STRING,
    default=lambda: os.environ.get("JELLYFIN_ENDPOINT", ""),
    help="default to read `JELLYFIN_ENDPOINT`",
)
@click.option(
    "--jellyfin-username",
    type=click.STRING,
    default=lambda: os.environ.get("JELLYFIN_USERNAME", ""),
    help="default to read `JELLYFIN_USERNAME`",
)
@click.option(
    "--jellyfin-password",
    type=click.STRING,
    default=lambda: os.environ.get("JELLYFIN_PASSWORD", ""),
    help="default to read `JELLYFIN_PASSWORD`",
)
@click.option(
    "--jellyfin-ssl",
    type=click.BOOL,
    default=lambda: os.environ.get("JELLYFIN_SSL", "true") == "true",
    help="default to read `JELLYFIN_SSL`, false",
)
@click.option(
    "--notion-api-key",
    type=click.STRING,
    default=lambda: os.environ.get("NOTION_API_KEY", ""),
    help="default to read `NOTION_API_KEY`",
)
@click.option(
    "--notion-database-id",
    type=click.STRING,
    default=lambda: os.environ.get("NOTION_DATABASE_ID", ""),
    help="default to read `NOTION_DATABASE_ID`",
)
@click.option(
    "--jellyfin-parent-id",
    type=click.STRING,
)
@click.option(
    "--limit",
    type=click.INT,
    default=10,
    show_default=True,
)
@click.option(
    "--overwrite",
    type=click.BOOL,
    default=False,
    show_default=True,
)
@click.pass_context
def jellyfin_to_notion_command(
    ctx,
    jellyfin_endpoint: str,
    jellyfin_username: str,
    jellyfin_password: str,
    jellyfin_ssl: bool,
    notion_api_key: str,
    notion_database_id: str,
    jellyfin_parent_id: str,
    limit: int,
    overwrite: bool,
):
    logging.getLogger("httpx").setLevel(logging.WARNING)
    jellyfin_opts = JellyfinOptions(
        endpoint=jellyfin_endpoint,
        username=jellyfin_username,
        password=jellyfin_password,
        ssl=jellyfin_ssl,
    )
    notion_opts = NotionOptions(
        api_key=notion_api_key,
        database_id=notion_database_id,
    )
    runner = jellyfin_to_notion.Jellyfin2Notion(
        dry_run=ctx.obj["dry_run"],
        jellyfin_options=jellyfin_opts,
        notion_options=notion_opts,
        jellyfin_parent_id=jellyfin_parent_id,
        jellyfin_limit=limit,
        should_update=overwrite,
    )
    runner.run()


if __name__ == "__main__":
    cli()
