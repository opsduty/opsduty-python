from enum import StrEnum
from io import IOBase
from typing import Literal, TextIO, TypeVar, overload

import click
import pydantic
from opsduty_client.client import AuthenticatedClient, Client
from pydantic_yaml import parse_yaml_file_as, to_yaml_file

from opsduty_python.settings import settings

#
# API client
#


@overload
def get_client(
    ctx: click.Context, *, require_authentication: Literal[True]
) -> AuthenticatedClient: ...


@overload
def get_client(
    ctx: click.Context, *, require_authentication: Literal[False]
) -> Client: ...


def get_client(
    ctx: click.Context, *, require_authentication: Literal[True, False]
) -> AuthenticatedClient | Client | None:
    """
    Get API client in a safe way. This method causes the command to fail
    if the access token is requires, but no token was provided.
    """

    client = settings.get_client(require_authentication=require_authentication)

    if require_authentication and not client:
        ctx.fail("Access token is required, please provide the --access-token option.")
        raise RuntimeError

    return client


#
# Document renderer
#


class FileFormat(StrEnum):
    JSON = "json"
    YAML = "yaml"


FILE_FORMATS = [f.value for f in FileFormat]


def render_document(
    *,
    document: pydantic.BaseModel,
    file_format: FileFormat,
    stream: IOBase | TextIO,
) -> None:
    """Render document to stream, given the output format."""
    if file_format == FileFormat.JSON:
        stream.write(
            document.model_dump_json(
                indent=2, exclude_unset=True, exclude_defaults=True
            )
        )

    elif file_format == FileFormat.YAML:
        to_yaml_file(
            stream,  # type: ignore
            document,
            default_flow_style=False,
            indent=2,
            map_indent=2,
            sequence_indent=2,
            sequence_dash_offset=0,
            exclude_unset=True,
            exclude_defaults=True,
        )

    else:
        raise NotImplementedError("File format not supported.")


TDocument = TypeVar("TDocument", bound=pydantic.BaseModel)


def parse_document(document: IOBase | TextIO, type: type[TDocument]) -> TDocument:
    """Parse document file as type."""

    return parse_yaml_file_as(
        type,
        document,  # type: ignore
    )
