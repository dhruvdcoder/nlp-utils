"""Utils common to all datasets"""
from pathlib import Path
from torchtext.utils import download_from_url
from typing import Dict, Tuple, Optional, Union, List
import logging
import zipfile
import gzip
import tarfile
import shutil
import warnings

logger = logging.getLogger(__name__)


def download(url: str, file_name: Union[Path, str]):
    """Download a dataset from a url"""
    logger.info("Downloading from {} into {}".format(url, file_name))
    # convert to str before sending to torchtext

    if isinstance(file_name, Path):
        file_name = str(file_name.absolute())

    return download_from_url(url, file_name)


def download_if_missing(url: str, check: Path) -> bool:
    """Check if the file check exists, if yes, do nothing.
    If no, download using the url"""

    if check.exists():
        return False
    else:
        download(url, check)

        return True


def unzip(file_name: Path):
    suffixes = file_name.suffixes
    ext = ''.join(suffixes)
    ext_inner: Optional[str] = None

    if len(suffixes) > 1:
        ext_inner = suffixes[-2]
        ext = suffixes[-1]

    if ext == '.zip':
        with zipfile.ZipFile(file_name, 'r') as zfile:
            logger.info('extracting...')
            zfile.extractall(file_name.parent)
    # tarfile cannot handle bare .gz files
    elif ext == '.tgz' or ext == '.gz' and ext_inner == '.tar':
        warnings.warn(
            "Unpacking of file with extension {} has not been tested".format(
                ext))
        with tarfile.open(file_name, 'r:gz') as tar:
            dirs = [member for member in tar.getmembers()]
            tar.extractall(path=file_name.parent, members=dirs)
    elif ext == '.gz':
        warnings.warn(
            "Unpacking of file with extension {} has not been tested".format(
                ext))
        with gzip.open(file_name, 'rb') as gz:
            with open(file_name.parent / file_name.stem, 'wb') as uncompressed:
                shutil.copyfileobj(gz, uncompressed)
    else:
        raise ValueError("{} extension not supported".format(file_name.name))


def download_unzip(url: str, file_path: Path):
    folder: Path = file_path.parent
    folder.mkdir(parents=True, exist_ok=True)
    download(url, file_path)
    unzip(file_path)

    return file_path.parent
