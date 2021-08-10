#!/usr/bin/env python3
# library imports
import argparse
import logging
import sys
import pathlib


from mgrandi.xml_file_utils import utils
from mgrandi.xml_file_utils.modules import xsd_schema


def main():
     # if we are being run as a real program

    parser = argparse.ArgumentParser(
        description="verify a XML file with the service fabric XSD schema",
        epilog="Copyright 2020-10-26 - Mark Grandi")

    # set up logging stuff
    logging.captureWarnings(True) # capture warnings with the logging infrastructure
    root_logger = logging.getLogger()
    logging_formatter = utils.ArrowLoggingFormatter("%(asctime)s %(threadName)-10s %(name)-20s %(levelname)-8s: %(message)s")
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging_formatter)
    root_logger.addHandler(logging_handler)


    # due to this bug: https://bugs.python.org/issue15125
    # i can't really have hyphens in the argument name because if its positional, it doesn't translate it
    # to underscores, so just make them have underscores and then set the metavar one to have hyphens

    parser.add_argument("--verbose", action="store_true", help="increase logging verbosity")

    subparsers = parser.add_subparsers()
    xsd_schema_obj = xsd_schema.VerifyXSDSchema.create_subparser_command(subparsers)

    try:
        parsed_args = parser.parse_args()

        # set logging level based on arguments
        if parsed_args.verbose:
            root_logger.setLevel("DEBUG")
        else:
            root_logger.setLevel("INFO")

        root_logger.debug("Parsed arguments: %s", parsed_args)

        # run the application
        parsed_args.func_to_run(parsed_args)

        root_logger.info("Done!")
    except Exception as e:
        root_logger.exception("Something went wrong!")
        sys.exit(1)


        


