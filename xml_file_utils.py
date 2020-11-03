#!/usr/bin/env python3

# library imports
import argparse
import logging
import sys
import pathlib


# third party imports
import arrow
import lxml.etree as etree



class Application:
    '''verify a XML file with the service fabric XSD schema
    '''

    def __init__(self, logger, args):
        ''' constructor
        @param logger the Logger instance
        @param args - the namespace object we get from argparse.parse_args()
        '''

        self.logger = logger
        self.args = args

    def main(self):

        schema_root = None
        manifest_root = None

        parser = None

        # see if we are validating with a schema or not
        if self.args.xsd_schema:
            self.logger.info("loading XSD schema at `%s`", self.args.xsd_schema)

            # read as bytes, or else you get:
            # ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
            with open(self.args.xsd_schema, "rb") as f:
                schema_root = etree.fromstring(f.read())

            schema = etree.XMLSchema(schema_root)
            parser = etree.XMLParser(schema = schema)

        else:
            parser = etree.XMLParser()

        try:

            # see above about reading as bytes
            with open(self.args.xml_to_verify, "rb") as f:
                manifest_root = etree.fromstring(f.read(), parser)


            self.logger.info("XML file validated successfully")

            raw_pretty_bytes = etree.tostring(manifest_root, pretty_print=True)
            raw_pretty_str = raw_pretty_bytes.decode("utf-8")
            self.logger.debug("Parsed XML tree:")
            self.logger.debug(raw_pretty_str)

        except Exception as e:

            self.logger.exception("XML file did not pass validation!")

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

class ArrowLoggingFormatter(logging.Formatter):
    ''' logging.Formatter subclass that uses arrow, that formats the timestamp
    to the local timezone (but its in ISO format)
    '''

    def formatTime(self, record, datefmt=None):
        return arrow.get("{}".format(record.created), "X").to("local").isoformat()

if __name__ == "__main__":
    # if we are being run as a real program

    parser = argparse.ArgumentParser(
        description="verify a XML file with the service fabric XSD schema",
        epilog="Copyright 2020-10-26 - Mark Grandi")

    # set up logging stuff
    logging.captureWarnings(True) # capture warnings with the logging infrastructure
    root_logger = logging.getLogger()
    logging_formatter = ArrowLoggingFormatter("%(asctime)s %(threadName)-10s %(name)-20s %(levelname)-8s: %(message)s")
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging_formatter)
    root_logger.addHandler(logging_handler)


    # due to this bug: https://bugs.python.org/issue15125
    # i can't really have hyphens in the argument name because if its positional, it doesn't translate it
    # to underscores, so just make them have underscores and then set the metavar one to have hyphens
    parser.add_argument('xml_to_verify', metavar="xml-to-verify", type=isFileType, help="the XML file to verify against the schema")
    parser.add_argument("--xsd-schema", dest="xsd_schema", type=isFileType, help="if specified, the XSD scherma to validate against")
    parser.add_argument("--verbose", action="store_true", help="increase logging verbosity")


    try:
        parsed_args = parser.parse_args()

        # set logging level based on arguments
        if parsed_args.verbose:
            root_logger.setLevel("DEBUG")
        else:
            root_logger.setLevel("INFO")

        root_logger.debug("Parsed arguments: %s", parsed_args)

        # run the application
        app = Application(root_logger.getChild("app"), parsed_args)
        app.main()

        root_logger.info("Done!")
    except Exception as e:
        root_logger.exception("Something went wrong!")
        sys.exit(1)