"""CLI to download data."""

from load_data._paths import create_dirs
from load_data._download_files import download_files
from load_data._parse_data import (
    parse_legislators,
    parse_bills,
    parse_bill_votes,
)

ZIP_FILE = "pubinfo_daily_Sat.zip"


def main() -> None:
    """Download and process the latest data."""
    create_dirs()
    download_files(ZIP_FILE)
    author_names = parse_legislators()
    parse_bills()
    parse_bill_votes(author_names)
