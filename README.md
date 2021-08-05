# xml_file_utils

## setup

install python

install poetry

```plaintext
pip3 install poetry
```

run poetry

```plaintext

poetry shell
poetry install

```

NOTE: for windows users, you need to add a folder to your PATH env variable, or just run it manually:

```plaintext

# either add this folder to your PATH and then run the above commands, 
# C:\Users\USERNAME_HERE\AppData\Roaming\Python\Python39\Scripts\
# or just run this
C:\Users\USERNAME_HERE\AppData\Roaming\Python\Python39\Scripts\poetry.exe shell
C:\Users\USERNAME_HERE\AppData\Roaming\Python\Python39\Scripts\poetry.exe install

```

## usage

```plaintext
> python cli.py --help
usage: cli.py [-h] [--print] [--xsd-schema XSD_SCHEMA] [--verbose] xml-to-verify

verify a XML file with the service fabric XSD schema

positional arguments:
  xml-to-verify         the XML file to verify against the schema

optional arguments:
  -h, --help            show this help message and exit
  --print               specify to print the XML after verification
  --xsd-schema XSD_SCHEMA
                        if specified, the XSD scherma to validate against
  --verbose             increase logging verbosity

Copyright 2020-10-26 - Mark Grandi
```

## examples

### verify syntax of a XML file #1

```plaintext
> python cli.py "C:\ApplicationManifest.xml"
2021-08-05T13:08:01.846107-07:00 MainThread app                  INFO    : XML file validated successfully
2021-08-05T13:08:01.846107-07:00 MainThread root                 INFO    : Done!

```

### verify syntax of a XML file #2

```plaintext
> python cli.py "C:\ApplicationManifest.xml"
2021-08-05T13:05:43.702642-07:00 MainThread app                  ERROR   : XML file did not pass validation! error: `Errors:
C:\ApplicationManifest.xml:514:5:FATAL:PARSER:ERR_NAME_REQUIRED: error parsing attribute name
C:\ApplicationManifest.xml:514:5:FATAL:PARSER:ERR_SPACE_REQUIRED: attributes construct error
C:\ApplicationManifest.xml:514:5:FATAL:PARSER:ERR_GT_REQUIRED: Couldn't find end of Start Tag Principals line 513
C:\ApplicationManifest.xml:521:16:FATAL:PARSER:ERR_TAG_NAME_MISMATCH: Opening and ending tag mismatch: ApplicationManifest line 2 and Principals
C:\ApplicationManifest.xml:522:3:FATAL:PARSER:ERR_DOCUMENT_END: Extra content at the end of the document`
2021-08-05T13:05:43.702642-07:00 MainThread root                 ERROR   : Something went wrong!
Traceback (most recent call last):
  File "C:\Users\mgrandi\Code\git\Personal\xml_file_utils\mgrandi\xml_file_utils\application.py", line 59, in main
    manifest_root = etree.parse(f, parser)
  File "src\lxml\etree.pyx", line 3521, in lxml.etree.parse
  File "src\lxml\parser.pxi", line 1880, in lxml.etree._parseDocument
  File "src\lxml\parser.pxi", line 1900, in lxml.etree._parseFilelikeDocument
  File "src\lxml\parser.pxi", line 1795, in lxml.etree._parseDocFromFilelike
  File "src\lxml\parser.pxi", line 1201, in lxml.etree._BaseParser._parseDocFromFilelike
  File "src\lxml\parser.pxi", line 615, in lxml.etree._ParserContext._handleParseResultDoc
  File "src\lxml\parser.pxi", line 725, in lxml.etree._handleParseResult
  File "src\lxml\parser.pxi", line 654, in lxml.etree._raiseParseError
  File "C:\Users\mgrandi\OneDrive - Microsoft\Documents\2021-07-21 - mycroft - ApplicationManifest.xml", line 514
lxml.etree.XMLSyntaxError: error parsing attribute name, line 514, column 5

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\mgrandi\Code\git\Personal\xml_file_utils\cli.py", line 81, in <module>
    app.main()
  File "C:\Users\mgrandi\Code\git\Personal\xml_file_utils\mgrandi\xml_file_utils\application.py", line 82, in main
    raise Exception("XML file did not pass validation") from e
Exception: XML file did not pass validation

```

### validate a XML file with a schema #1

```plaintext
> python cli.py "C:\ApplicationManifest.xml" --xsd-schema "C:\Program Files\Microsoft SDKs\Service Fabric\schemas\ServiceFabricServiceModel.xsd"
2021-08-05T13:02:51.095346-07:00 MainThread app                  INFO    : loading XSD schema at `C:\Program Files\Microsoft SDKs\Service Fabric\schemas\ServiceFabricServiceModel.xsd`
2021-08-05T13:02:51.111193-07:00 MainThread app                  INFO    : XML file validated successfully
2021-08-05T13:02:51.111193-07:00 MainThread root                 INFO    : Done!
```

### validate a XML file with a schema #2

```plaintext
> python cli.py "C:\ApplicationManifest.xml" --xsd-schema "C:\Program Files\Microsoft SDKs\Service Fabric\schemas\ServiceFabricServiceModel.xsd"
2021-08-05T13:04:13.268157-07:00 MainThread app                  INFO    : loading XSD schema at `C:\Program Files\Microsoft SDKs\Service Fabric\schemas\ServiceFabricServiceModel.xsd`
2021-08-05T13:04:13.268157-07:00 MainThread app                  ERROR   : XML file did not pass validation! error: `Errors:
<string>:0:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element '{http://schemas.microsoft.com/2011/01/fabric}Principals': This element is not expected. Expected is one of ( {http://schemas.microsoft.com/2011/01/fabric}Description, {http://schemas.microsoft.com/2011/01/fabric}Parameters, {http://schemas.microsoft.com/2011/01/fabric}ServiceManifestImport ).`
2021-08-05T13:04:13.268157-07:00 MainThread root                 ERROR   : Something went wrong!
Traceback (most recent call last):
  File "C:\Users\mgrandi\Code\git\Personal\xml_file_utils\mgrandi\xml_file_utils\application.py", line 59, in main
    manifest_root = etree.parse(f, parser)
  File "src\lxml\etree.pyx", line 3521, in lxml.etree.parse
  File "src\lxml\parser.pxi", line 1880, in lxml.etree._parseDocument
  File "src\lxml\parser.pxi", line 1900, in lxml.etree._parseFilelikeDocument
  File "src\lxml\parser.pxi", line 1795, in lxml.etree._parseDocFromFilelike
  File "src\lxml\parser.pxi", line 1201, in lxml.etree._BaseParser._parseDocFromFilelike
  File "src\lxml\parser.pxi", line 615, in lxml.etree._ParserContext._handleParseResultDoc
  File "src\lxml\parser.pxi", line 725, in lxml.etree._handleParseResult
  File "src\lxml\parser.pxi", line 654, in lxml.etree._raiseParseError
  File "<string>", line 0
lxml.etree.XMLSyntaxError: Element '{http://schemas.microsoft.com/2011/01/fabric}Principals': This element is not expected. Expected is one of ( {http://schemas.microsoft.com/2011/01/fabric}Description, {http://schemas.microsoft.com/2011/01/fabric}Parameters, {http://schemas.microsoft.com/2011/01/fabric}ServiceManifestImport ).

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\mgrandi\Code\git\Personal\xml_file_utils\cli.py", line 81, in <module>
    app.main()
  File "C:\Users\mgrandi\Code\git\Personal\xml_file_utils\mgrandi\xml_file_utils\application.py", line 82, in main
    raise Exception("XML file did not pass validation") from e
Exception: XML file did not pass validation
```

### print XML file after validation

```plaintext
> python cli.py .\example_xml_files\test_xml_file_1.xml --print
2021-08-05T13:12:45.097328-07:00 MainThread app                  INFO    : XML file validated successfully
2021-08-05T13:12:45.100329-07:00 MainThread app                  INFO    : Parsed XML tree:
2021-08-05T13:12:45.100329-07:00 MainThread app                  INFO    :
<Library>
  <Book>
    <Title>Warriors #1: Into the Wild</Title>
    <Author>Erin Hunter</Author>
  </Book>
  <Book>
    <Title>Warriors #2: Fire and Ice</Title>
    <Author>Erin Hunter</Author>
  </Book>
  <Book>
    <Title>Warriors #3: Forest of Secrets</Title>
    <Author>Erin Hunter</Author>
  </Book>
</Library>
```


### run the script with verbose log output

```plaintext
> python cli.py .\example_xml_files\test_xml_file_1.xml --verbose
2021-08-05T13:14:26.518020-07:00 MainThread root                 DEBUG   : Parsed arguments: Namespace(xml_to_verify=WindowsPath('C:/Users/mgrandi/Code/git/Personal/xml_file_utils/example_xml_files/test_xml_file_1.xml'), print=False, xsd_schema=None, verbose=True)
2021-08-05T13:14:26.518020-07:00 MainThread app                  DEBUG   : parser: `<lxml.etree.XMLParser object at 0x0000025CD7417160>`
2021-08-05T13:14:26.518020-07:00 MainThread app                  DEBUG   : reading xml: `C:\Users\mgrandi\Code\git\Personal\xml_file_utils\example_xml_files\test_xml_file_1.xml`
2021-08-05T13:14:26.518020-07:00 MainThread app                  INFO    : XML file validated successfully
2021-08-05T13:14:26.518020-07:00 MainThread root
```
