import os
from typing import Optional

import click
from requests import Response

from zenodo_rest.entities import Deposition, Metadata
from zenodo_rest.entities.bucket_file import BucketFile
from zenodo_rest.exceptions import NoDraftFound

from . import actions


@click.group()
def depositions():
    pass


@depositions.command()
@click.option("--metadata", help="Optional json of metadata for the deposition.")
@click.option(
    "--metadata_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Optional json file of metadata for the deposition.",
)
@click.option(
    "--prereserve-doi",
    is_flag=True,
    help="Prereserve a DOI (not pushed to Datacite until deposition is published).",
)
@click.option(
    "--dest",
    type=click.Path(),
    default=None,
    help="A file to write the resulting deposition json representation to.",
)
def create(
    metadata: Optional[str] = None,
    metadata_file: Optional[str] = None,
    prereserve_doi: Optional[bool] = None,
    dest: Optional[str] = None,
):

    metadata_parsed: Metadata = Metadata()
    if isinstance(metadata, str):
        metadata_parsed = Metadata.parse_raw(metadata)
    elif isinstance(metadata, Metadata):
        metadata_parsed = metadata

    if metadata_file is not None:
        metadata_parsed = Metadata.parse_file(metadata_file)

    deposition: Deposition = actions.create(metadata_parsed, prereserve_doi)
    json_response = deposition.json(exclude_none=True, indent=4)
    click.echo(json_response)
    if dest is None:
        return
    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(json_response)


@depositions.command()
@click.argument("deposition-id", type=click.INT)
@click.option(
    "--dest",
    type=click.Path(),
    default=None,
    help="A file to write the resulting deposition json representation to.",
)
def retrieve(deposition_id: int, dest: Optional[str] = None):
    """Retrieve deposition by ID from server.

    DEPOSITION-ID is the id of the deposition to be fetched
    """
    deposition: Deposition = actions.retrieve(deposition_id)
    json_response = deposition.json(exclude_none=True, indent=4)
    click.echo(json_response)
    if dest is None:
        return
    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(json_response)


@depositions.command("list")
@click.option(
    "--query", "-q", help="Search query (using Elasticsearch query string syntax)."
)
@click.option(
    "--status", help="Filter result based on deposit status (either draft or published)"
)
@click.option(
    "--sort",
    help=(
        "Sort order (bestmatch or mostrecent)."
        "Prefix with minus to change form ascending to descending (e.g. -mostrecent)."
    ),
)
@click.option("--page", help="Page number for pagination")
@click.option("--size", help="Number of results to return per page.")
@click.option(
    "--all-versions",
    help="Show (true or 1) or hide (false or 0) all versions of deposits.",
)
def search_depositions(
    query: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    page: Optional[str] = None,
    size: Optional[int] = None,
    all_versions: bool = None,
):
    result: list[Deposition]
    result = actions.search(query, status, sort, page, size, all_versions)
    for x in result:
        click.echo(x.json(exclude_none=True, indent=2))


@depositions.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "metadata_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def update(
    deposition_json: str,
    metadata_file: str,
):
    """Update metadata for a not yet published deposition

    DEPOSITION_JSON the file with a json representation
    of the deposition to be updated

    METADATA_FILE the path to a metadata json file to be used as input
    """

    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.get_latest_draft()
    metadata = Metadata.parse_file(metadata_file)

    deposition = actions.update_metadata(deposition.id, metadata)
    json_response = deposition.json(exclude_none=True, indent=4)
    click.echo(json_response)


@depositions.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def delete(
    deposition_json: str,
):
    """Delete a not yet published deposition

    DEPOSITION_JSON json representation of the deposition to be deleted
    """

    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.get_latest_draft()
    response: Response = actions.delete_remote(deposition.id)
    json_response = response.json(exclude_none=True, indent=4)
    click.echo(json_response)


@depositions.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "file",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
def upload_file(
    deposition_json: str,
    file: str,
):
    """Upload a file to the bucket of a not yet published deposition

    DEPOSITION_JSON json representation of the deposition to be uploaded to.

    FILE the path to a file to be uploaded
    """
    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.get_latest_draft()
    bucket_file: BucketFile = actions.upload_file(deposition.id, file)
    json_response = bucket_file.json(exclude_none=True, indent=4)
    click.echo(json_response)


@depositions.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def delete_files(
    deposition_json: str,
):
    """Delete files from the bucket of a not yet published deposition

    DEPOSITION_JSON json representation of the deposition to be uploaded to.
    """
    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.get_latest_draft()
    responses = deposition.delete_files()
    click.echo(responses)


@depositions.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--dest",
    type=click.Path(),
    default=None,
    help="A file to write the resulting deposition json representation to.",
)
def publish(
    deposition_json: str,
    dest: Optional[str] = None,
):
    """Publish a pending deposition

    DEPOSITION_JSON json representation of the deposition to be published
    """

    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.get_latest_draft()
    deposition = actions.publish(deposition.id)
    json_response = deposition.json(exclude_none=True, indent=4)
    click.echo(json_response)
    if dest is None:
        return
    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(json_response)


@depositions.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--dest",
    type=click.Path(),
    default=None,
    help="A file to write the resulting deposition json representation to.",
)
def new_version(deposition_json: str, dest: Optional[str] = None):
    """Create a new version of a published disposition

    DEPOSITION_JSON json representation of the deposition to be published
    """

    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.refresh()
    deposition = deposition.get_latest()
    deposition = actions.new_version(deposition.id)
    json_response = deposition.json(exclude_none=True, indent=4)
    click.echo(json_response)
    if dest is None:
        return
    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(json_response)


@depositions.group()
def doi():
    """Get DOIs related to depositions"""
    pass


@doi.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--full-url",
    "-f",
    is_flag=True,
    help="Return the full url of the latest draft's DOI",
)
def latest(
    deposition_json: str,
    full_url: bool,
):
    """Print the doi of the latest published version of the given deposition.

    DEPOSITION_JSON json representation of the deposition
    """

    deposition: Deposition = Deposition.parse_file(deposition_json)
    deposition = deposition.get_latest()
    if full_url:
        click.echo(deposition.doi_url)
    else:
        click.echo(deposition.doi)


@doi.command()
@click.argument(
    "deposition-json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--full-url",
    "-f",
    is_flag=True,
    help="Return the full url of the latest draft's DOI",
)
def latest_draft(
    deposition_json: str,
    full_url: bool,
):
    """Print the DOI of the latest related deposition draft

    DEPOSITION_JSON json representation of the deposition
    """

    deposition: Deposition = Deposition.parse_file(deposition_json)
    draft: Deposition = deposition.get_latest_draft()
    if draft is None:
        raise NoDraftFound(deposition)
    if full_url:
        click.echo(draft.doi_url)
    else:
        click.echo(draft.doi)
