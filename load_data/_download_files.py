"""Function used to download files."""

from typing import Any
import sys
import ssl
import requests
from requests.adapters import HTTPAdapter
import urllib3
from urllib3.util import create_urllib3_context
from remotezip import RemoteZip  # type: ignore
from load_data._paths import BASE_URL, DOWNLOAD_DIR, DataFileName

if sys.version_info < (3, 12):
    # Backport for Python 3.11
    ssl.OP_LEGACY_SERVER_CONNECT = 0x4


class _CustomSslContextHttpAdapter(HTTPAdapter):
    """
    HTTPAdapter with the legacy server connect option for SSL turned on. This is
    required to access the government website where the data files are hosted.

    Adapted from https://github.com/urllib3/urllib3/issues/2653#issuecomment-1733417634.
    """

    def init_poolmanager(
        self, connections: int, maxsize: int, block: bool = False, **pool_kwargs: Any
    ) -> None:
        ctx = create_urllib3_context()
        ctx.load_default_certs()
        ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
        self.poolmanager = urllib3.PoolManager(ssl_context=ctx)


def _get_custom_ssl_session() -> requests.Session:
    """
    Get a custom SSL session with legacy server connect.

    Adapted from https://github.com/urllib3/urllib3/issues/2653#issuecomment-1733417634.
    """
    session = requests.Session()
    session.mount(BASE_URL, _CustomSslContextHttpAdapter())
    return session


def download_files(zip_file: str) -> None:
    """Download data files for the given session year."""
    ssl_session = _get_custom_ssl_session()
    zip_url = f"{BASE_URL}/{zip_file}"
    with RemoteZip(zip_url, session=ssl_session) as remote_zip:
        remote_zip.extractall(path=DOWNLOAD_DIR, members=DataFileName)
