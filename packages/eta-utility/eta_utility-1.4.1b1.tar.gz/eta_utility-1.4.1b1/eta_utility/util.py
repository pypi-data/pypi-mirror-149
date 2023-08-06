from __future__ import annotations

import csv
import json
import logging
import pathlib
import re
import sys
from typing import TYPE_CHECKING
from urllib.parse import urlparse, urlunparse

if TYPE_CHECKING:
    from typing import Any, Collection
    from urllib.parse import ParseResult

    from .type_hints import Path


def get_logger(
    name: str | None = None, level: int | None = None, format: str | None = None  # noqa: A002
) -> logging.Logger:
    """Get eta_utility specific logger

    Call this without specifying a name to initiate logging. Set the "level" and "format" parameters to determine
    log output.

    .. note::
        When using this function internally (inside eta_utility) a name should always be specified to avoid leaking
        logging info to external loggers. Also note that this can only be called once without specifying a name!
        Subsequent calls will have no effect.

    :param name: Name of the logger
    :param level: Logging level (higher is more verbose)
    :param format: Format of the log output. One of: simple, logname. (default: simple)
    :return: logger
    """
    prefix = "eta_utility"

    if name is not None and name != prefix:
        # Child loggers
        name = ".".join((prefix, name))
        log = logging.getLogger(name)
    else:
        # Main logger (only add handler if it does not have one already)
        log = logging.getLogger(prefix)
        log.propagate = False

        formats = {"simple": "[%(levelname)s] %(message)s", "logname": "[%(name)s: %(levelname)s] %(message)s"}
        fmt = formats[format] if format in formats else formats["simple"]

        if not log.hasHandlers():
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter(fmt=fmt))
            log.addHandler(handler)

    if level is not None:
        log.setLevel(int(level * 10))
    return log


log = get_logger("util", 2)


def json_import(path: Path) -> dict[str, Any]:
    """Extend standard json import to allow comments in json files

    :param path: path to json file
    :return: Parsed dictionary
    """
    path = pathlib.Path(path) if not isinstance(path, pathlib.Path) else path

    try:
        # Remove comments from the json file (using regular expression), then parse it into a dictionary
        cleanup = re.compile(r"^\s*(.*?)(?=/{2}|$)", re.MULTILINE)
        with path.open("r") as f:
            file = "".join(cleanup.findall(f.read()))
        result = json.loads(file)
        log.info(f"JSON file {path} loaded successfully.")
    except OSError as e:
        log.error(f"JSON file couldn't be loaded: {e.strerror}. Filename: {e.filename}")
        raise

    return result


def url_parse(url: str) -> tuple[ParseResult, str | None, str | None]:
    """Extend parsing of url strings to find passwords and remove them from the original URL

    :param url: URL string to be parsed
    :return: Tuple of ParseResult object and two strings for username and password
    """
    _url = urlparse(url)

    # Get username and password either from the arguments or from the parsed url string
    usr = _url.username if _url.username is not None else None
    pwd = _url.password if _url.password is not None else None

    # Find the "password-free" part of the netloc to prevent leaking secret info
    if usr is not None:
        match = re.search("(?<=@).+$", _url.netloc)
        if match:
            _url = urlparse(
                urlunparse((_url.scheme, match.group(), _url.path, _url.query, _url.fragment, _url.fragment))
            )

    return _url, usr, pwd


def csv_export_from_list(
    path: str | pathlib.Path,
    name: str,
    data: list[Any],
    fields: Collection[str],
) -> None:
    """
    Export csv data from list.

    :param path: directory path to export data
    :param name: name of the file (with or without preffix)
    :param data: data to be saved
    :param fields: names of the data columns
    """
    path = path if isinstance(path, pathlib.Path) else pathlib.Path(path)

    if len(name.split(".")) <= 1:
        name = name + ".csv"

    full_path = path / name

    with open(full_path, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)


def csv_export_from_dict(path: str | pathlib.Path, name: str, data: dict[str, Any]) -> None:
    """
    Export csv data from list.

    :param path: directory path to export data
    :param name: name of the file (with or without preffix)
    :param data: data to be saved
    :param fields: names of the data columns
    """

    path = path if isinstance(path, pathlib.Path) else pathlib.Path(path)
    fields = list(data.keys())

    if len(name.split(".")) <= 1:
        name = name + ".csv"

    full_path = path / name
    full_path_is_file = full_path.is_file()

    with open(full_path, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        if not full_path_is_file:
            writer.writeheader()
        writer.writerow(data)
