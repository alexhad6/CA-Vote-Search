"""Function used to download files."""

from remotezip import RemoteZip  # type: ignore
from load_data._paths import BASE_URL, DOWNLOAD_DIR, DataFileName


def download_files(zip_file: str) -> None:
    """Download data files for the given session year."""
    zip_url = f"{BASE_URL}/{zip_file}"
    with RemoteZip(zip_url) as remote_zip:
        remote_zip.extractall(path=DOWNLOAD_DIR, members=DataFileName)
