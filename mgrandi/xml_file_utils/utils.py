import pathlib
import argparse
import logging

import arrow

class ArrowLoggingFormatter(logging.Formatter):
    ''' logging.Formatter subclass that uses arrow, that formats the timestamp
    to the local timezone (but its in ISO format)
    '''

    def formatTime(self, record, datefmt=None):
        return arrow.get("{}".format(record.created), "X").to("local").isoformat()

def isFileType(filePath):
    ''' see if the file path given to us by argparse is a file
    @param filePath - the filepath we get from argparse
    @return the filepath as a pathlib.Path() if it is a file, else we raise a ArgumentTypeError'''

    path_maybe = pathlib.Path(filePath)
    path_resolved = None

    # try and resolve the path
    try:
        path_resolved = path_maybe.expanduser().resolve(strict=True)

    except Exception as e:
        raise argparse.ArgumentTypeError("Failed to parse `{}` as a path: `{}`".format(filePath, e))

    # double check to see if its a file
    if not path_resolved.is_file():
        raise argparse.ArgumentTypeError("The path `{}` is not a file!".format(path_resolved))

    return path_resolved