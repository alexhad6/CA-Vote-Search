"""Constants and helper functions used to download data."""

from enum import StrEnum
from pathlib import Path

BASE_URL = "https://downloads.leginfo.legislature.ca.gov"
"""Base URL for downloading data files."""

_PACKAGE_DIR = Path(__file__).parent
DOWNLOAD_DIR = _PACKAGE_DIR / "data"
"""Directory to download data files to."""

_OUTPUT_DIR = _PACKAGE_DIR.parent / "src" / "lib" / "data"
LEGISLATORS_OUTPUT_PATH = _OUTPUT_DIR / "legislators.json"
BILLS_OUTPUT_PATH = _OUTPUT_DIR / "bills.json"
VOTES_OUTPUT_DIR = _OUTPUT_DIR / "votes"


class DataFileName(StrEnum):
    """Names of data files of interest."""

    LEGISLATORS = "LEGISLATOR_TBL.dat"
    VOTES = "BILL_DETAIL_VOTE_TBL.dat"
    MOTIONS = "BILL_MOTION_TBL.dat"
    VOTE_SUMMARIES = "BILL_SUMMARY_VOTE_TBL.dat"
    BILLS = "BILL_TBL.dat"
    BILL_VERSIONS = "BILL_VERSION_TBL.dat"


def create_dirs() -> None:
    """Create the directories used to download and output data."""
    for dir_path in DOWNLOAD_DIR, _OUTPUT_DIR, VOTES_OUTPUT_DIR:
        dir_path.mkdir(exist_ok=True)
