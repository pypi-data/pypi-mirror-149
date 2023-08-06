import click

from mlfoundry import get_client


@click.group(help="download model or artifacts")
def download():
    ...


@download.command(short_help="Download logged model")
@click.option(
    "--run_id",
    required=True,
    type=str,
    help="run id",
)
@click.option(
    "--path",
    type=click.Path(file_okay=False, dir_okay=True, exists=False),
    required=True,
    help="path where the model will be downloaded",
)
def model(run_id: str, path: str):
    """
    Download the logged model for a run.\n
    """
    client = get_client()
    run = client.get_run(run_id)
    run._download_model(path=path)
