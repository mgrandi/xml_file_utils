#!/usr/bin/env python3

import logging

# third party imports
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

            # see https://lxml.de/4.0/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
            parser = etree.XMLParser(schema = schema, remove_blank_text=True)
            self.logger.debug("parser: `%s`, with schema: `%s`", parser, schema)

        else:

            # see https://lxml.de/4.0/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
            parser = etree.XMLParser(remove_blank_text=True)
            self.logger.debug("parser: `%s`", parser)


        try:

            self.logger.debug("reading xml: `%s`", self.args.xml_to_verify)

            # see above about reading as bytes
            with open(self.args.xml_to_verify, "rb") as f:
                # manifest_root = etree.fromstring(f.read(), parser)
                manifest_root = etree.parse(f, parser)

            self.logger.info("XML file validated successfully")

            if self.args.print:
                raw_pretty_bytes = etree.tostring(manifest_root, pretty_print=True)
                raw_pretty_str = raw_pretty_bytes.decode("utf-8")
                self.logger.info("Parsed XML tree:")
                self.logger.info("\n" + raw_pretty_str)

        except etree.XMLSyntaxError as e:

            error_str = "unknown"

            if len(e.error_log) >= 1:
                error_str = "Errors: "
                for iter_error in e.error_log:
                    error_str += f"\n{iter_error}"

            # don't use `logger.exception` here as it seems to only include the to most error and that is kinda useless
            # we build the `error_str` with all the errors so we will just use that
            self.logger.error("XML file did not pass validation! error: `%s`", error_str)

            raise Exception("XML file did not pass validation") from e

        except Exception as e:
            self.logger.exception("unhandled exception!")

            raise e

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

