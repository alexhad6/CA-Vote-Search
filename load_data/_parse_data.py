"""Function used to parse legislator information."""

from typing import Any
from collections.abc import Iterator
from dataclasses import dataclass
import json
from datetime import datetime
from load_data._paths import (
    DOWNLOAD_DIR,
    LEGISLATORS_OUTPUT_PATH,
    BILLS_OUTPUT_PATH,
    VOTES_OUTPUT_DIR,
    DataFileName,
)


@dataclass
class LegislatorInfo:
    """Information for a legislator."""

    house: str
    district: str
    party: str
    display_name: str


@dataclass
class BillInfo:
    """Information for a bill."""

    measure_type: str
    session_num: int
    measure_num: int
    subject: str | None
    location: str
    status: str


def _parse_field(field: str) -> Any:
    field = field.strip().strip("`")
    return None if field == "NULL" else field


def _parse_fields(line: str) -> list[str]:
    return [_parse_field(field) for field in line.split("\t")]


def _parse_lines(file_name: DataFileName) -> Iterator[list[str]]:
    with open(DOWNLOAD_DIR / file_name, encoding="utf-8") as f:
        for line in f.readlines():
            yield _parse_fields(line)


def parse_legislators() -> list[str]:
    """
    Parse legislator information, save in a JSON file, and return a list of author
    names.

    File columns are interpreted according to the file legislator_tbl.sql in
    https://downloads.leginfo.legislature.ca.gov/pubinfo_load.zip.
    """
    author_names: list[str] = []
    legislators: dict[str, LegislatorInfo] = {}
    for fields in _parse_lines(DataFileName.LEGISLATORS):
        author_name = fields[4]
        *rest_name, first_name = fields[2].split(", ")
        author_names.append(author_name)
        legislators[author_name] = LegislatorInfo(
            house=fields[3],
            district=fields[0],
            party=fields[11],
            display_name=f"{first_name} {', '.join(rest_name)}",
        )
    author_names.sort(key=lambda author_name: legislators[author_name].district)
    legislators_by_house: dict[str, dict[str, Any]] = {"A": {}, "S": {}}
    for author_name in author_names:
        legislator = legislators[author_name]
        legislators_by_house[legislator.house][author_name] = {
            "district": legislator.district,
            "party": legislator.party,
            "displayName": legislator.display_name,
        }
    with open(LEGISLATORS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(legislators_by_house, f)
    return author_names


def parse_bills() -> None:
    """
    Parse bill information and save in a JSON file.

    File columns are interpreted according to the file bill_tbl.sql in
    https://downloads.leginfo.legislature.ca.gov/pubinfo_load.zip.
    """
    bill_subjects = {
        fields[0]: fields[6] for fields in _parse_lines(DataFileName.BILL_VERSIONS)
    }
    bills: dict[str, BillInfo] = {}
    for fields in _parse_lines(DataFileName.BILLS):
        bills[fields[0]] = BillInfo(
            measure_type=fields[3],
            session_num=int(fields[2]),
            measure_num=int(fields[4]),
            subject=bill_subjects[fields[10]],
            location=fields[16],
            status=fields[17],
        )
    bill_ids_sorted = sorted(
        bills,
        key=lambda bill_id: (
            bills[bill_id].measure_type,
            bills[bill_id].session_num,
            bills[bill_id].measure_num,
        ),
    )
    bills_sorted = {}
    for bill_id in bill_ids_sorted:
        bill = bills[bill_id]
        session_str = f"X{bill.session_num}" if bill.session_num > 0 else ""
        bills_sorted[bill_id] = {
            "measure": f"{bill.measure_type}{session_str}-{bill.measure_num}",
            "subject": bill.subject,
            "location": bill.location,
            "status": bill.status,
        }
    with open(BILLS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(bills_sorted, f)


# pylint: disable-next=too-many-locals
def parse_bill_votes(author_names: list[str]) -> None:
    """
    Parse bill vote information and save in a JSON file. This assumes the bill vote data
    and motion data files for the given session year has already been downloaded by
    ``download_files()``.

    File columns are interpreted according to the files bill_detail_vote_tbl.sql and
    bill_motion_tbl.sql in
    https://downloads.leginfo.legislature.ca.gov/pubinfo_load.zip.
    """
    motion_texts: dict[str, str] = {
        fields[0]: fields[1] for fields in _parse_lines(DataFileName.MOTIONS)
    }
    vote_results: dict[str, str] = {
        fields[4]: fields[8].strip("()")
        for fields in _parse_lines(DataFileName.VOTE_SUMMARIES)
    }
    all_votes: dict[str, dict[str, list[dict[str, Any]]]] = {
        author_name: {} for author_name in author_names
    }
    for fields in _parse_lines(DataFileName.VOTES):
        bill_id = fields[0]
        author_name = fields[2]
        motion_id = fields[6]
        time = datetime.strptime(fields[3], "%Y-%m-%d %H:%M:%S")
        vote = {
            "timestamp": int(time.timestamp()),
            "motion_id": int(motion_id),
            "vote": fields[5],
            "motion": motion_texts[motion_id],
            "result": vote_results[motion_id],
        }
        votes = all_votes[author_name]
        if bill_id in votes:
            votes[bill_id].append(vote)
        else:
            votes[bill_id] = [vote]
    for votes in all_votes.values():
        for bill_votes in votes.values():
            bill_votes.sort(key=lambda vote: vote["motion_id"], reverse=True)
    for author_name, votes in all_votes.items():
        sorted_bills = sorted(
            votes,
            # pylint: disable-next=cell-var-from-loop
            key=lambda bill_id: votes[bill_id][0]["motion_id"],
            reverse=True,
        )
        for bill_votes in votes.values():
            for vote in bill_votes:
                del vote["motion_id"]
        all_votes[author_name] = {bill_id: votes[bill_id] for bill_id in sorted_bills}
    for author_name, votes in all_votes.items():
        with open(VOTES_OUTPUT_DIR / f"{author_name}.json", "w", encoding="utf-8") as f:
            json.dump(votes, f)
