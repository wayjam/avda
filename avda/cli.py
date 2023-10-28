import click
import logging
from . import retidy
from . import subtitle_mover

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
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, writable=True
    ),
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


if __name__ == "__main__":
    cli()
