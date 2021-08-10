import logging
import pathlib
import argparse

# third party imports
import arrow
import lxml.etree as etree

logger = logging.getLogger(__name__)


from mgrandi.xml_file_utils import utils

class VerifyXSDSchema:


    def __init__(self):

        self.xml_to_verify:pathlib.Path = None
        self.should_print:bool = False
        self.xsd_schema:pathlib.Path = None

    @staticmethod
    def create_subparser_command(argparse_subparser):


        verify_schema_obj = VerifyXSDSchema()

        parser = argparse_subparser.add_parser("xsd_schema")

        # set the function that is called when this command is used
        parser.set_defaults(func_to_run=verify_schema_obj.run)

        parser.add_argument('--xml-to-verify', required=True, dest="xml_to_verify", type=utils.isFileType, help="the XML file to verify against the schema")
        parser.add_argument("--print", action="store_true", help="specify to print the XML after verification")
        parser.add_argument("--xsd-schema", dest="xsd_schema", type=utils.isFileType, help="if specified, the XSD scherma to validate against")


    def run(self, args:argparse.Namespace):

        self.xml_to_verify = args.xml_to_verify
        self.should_print = args.print
        self.xsd_schema = args.xsd_schema


        schema_root = None
        manifest_root = None

        parser = None

        # see if we are validating with a schema or not
        if self.xsd_schema:
            logger.info("loading XSD schema at `%s`", args.xsd_schema)

            # read as bytes, or else you get:
            # ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
            with open(self.xsd_schema, "rb") as f:
                schema_root = etree.fromstring(f.read())

            schema = etree.XMLSchema(schema_root)

            # see https://lxml.de/4.0/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
            parser = etree.XMLParser(schema = schema, remove_blank_text=True)
            logger.debug("parser: `%s`, with schema: `%s`", parser, schema)

        else:

            # see https://lxml.de/4.0/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
            parser = etree.XMLParser(remove_blank_text=True)
            logger.debug("parser: `%s`", parser)


        try:

            logger.debug("reading xml: `%s`", self.xml_to_verify)

            # see above about reading as bytes
            with open(self.xml_to_verify, "rb") as f:
                # manifest_root = etree.fromstring(f.read(), parser)
                manifest_root = etree.parse(f, parser)

            logger.info("XML file validated successfully")

            if self.should_print:
                raw_pretty_bytes = etree.tostring(manifest_root, pretty_print=True)
                raw_pretty_str = raw_pretty_bytes.decode("utf-8")
                logger.info("Parsed XML tree:")
                logger.info("\n" + raw_pretty_str)

        except etree.XMLSyntaxError as e:

            error_str = "unknown"

            if len(e.error_log) >= 1:
                error_str = "Errors: "
                for iter_error in e.error_log:
                    error_str += f"\n{iter_error}"

            # don't use `logger.exception` here as it seems to only include the to most error and that is kinda useless
            # we build the `error_str` with all the errors so we will just use that
            logger.error("XML file did not pass validation! error: `%s`", error_str)

            raise Exception("XML file did not pass validation") from e

        except Exception as e:
            logger.exception("unhandled exception!")

            raise e