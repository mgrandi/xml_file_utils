import logging
import pathlib
import argparse

# third party imports
import arrow
import lxml.etree as etree

logger = logging.getLogger(__name__)


from mgrandi.xml_file_utils import utils

class XMLEdit:


    def __init__(self):
        self.xml_to_edit:pathlib.Path = None
        self.edit_config:pyhocon.ConfigTree = None


    @staticmethod
    def create_subparser_command(argparse_subparser):


        xml_edit_obj = XMLEdit()

        parser = argparse_subparser.add_parser("xml_edit")

        # set the function that is called when this command is used
        parser.set_defaults(func_to_run=xml_edit_obj.run)

        parser.add_argument('--xml-to-edit', required=True, dest="xml_to_edit", type=utils.isFileType, help="the XML file to edit")
        parser.add_argument("--edit-config", required=True, dest="edit_config", type=utils.hocon_config_file_type, help="the config of what to edit")


    def run(self, args:argparse.Namespace):

        self.xml_to_edit = args.xml_to_edit
        self.edit_config = args.edit_config

        logger.info("hey")