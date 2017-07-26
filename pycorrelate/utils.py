"""
Various utilities.
"""

import sys
from pathlib import Path
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError


def download_file(url, save_dir='./'):
    """Download a file from `url` saving it to disk.

    The file name is taken from `url` and left unchanged.
    The destination dir can be set using `save_dir`
    (Default: the current dir).
    """
    # Check if local path already exist
    fname = url.split('/')[-1]
    print('URL:  %s' % url)
    print('File: %s\n ' % fname)

    path = Path(save_dir, fname)
    if path.exists():
        print('File already on disk: %s \nDelete it to re-download.' % path)
        return

    # Check if the URL is valid
    try:
        urlopen(url)
    except URLError as e:
        print('Wrong URL or no connection.\n\nError:\n%s\n' % e)
    except HTTPError:
        print('URL not found: ' + url)
        return

    # Donwload the file
    def _report(blocknr, blocksize, size):
        current = blocknr * blocksize / 2**20
        sys.stdout.write(
            "\rDownloaded {0:4.1f} / {1:4.1f} MB"
            .format(current, size / 2**20))

    Path(save_dir).mkdir(parents=True, exist_ok=True)
    urlretrieve(url, str(path), _report)
