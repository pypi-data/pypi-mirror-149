# validator.py

from lxml import etree
import os


def check_xml(xml_to_check):
    # parse xml
    try:
        if not os.path.isfile(xml_to_check):
            raise FileNotFoundError

        with open(xml_to_check, "r", encoding="utf-8") as file:
            xml = file.read()
            xml = bytes(bytearray(xml, encoding="utf-8"))
            etree.XML(xml)

    # check for FileNotFoundError
    except FileNotFoundError:
        print("Can't find file {}".format(xml_to_check))
        exit(2)

    # check for file IO error
    except IOError as err:
        print("Invalid File")
        with open("error.log", "w", encoding="utf-8") as error_log_file:
            error_log_file.write(str(err))

        exit(2)

    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        print("XML Syntax Error, see error.log")
        with open("error.log", "w", encoding="utf-8") as error_log_file:
            error_log_file.write(str(err))
        exit(2)

    except Exception as err:
        print("Unknown error, see error.log")
        with open("error.log", "w", encoding="utf-8") as error_log_file:
            error_log_file.write(str(err))
        exit(2)
