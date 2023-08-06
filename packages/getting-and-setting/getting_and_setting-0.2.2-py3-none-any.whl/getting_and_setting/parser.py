''' parser.py
The parser module, part of the getting-and-setting package contains functions
to ease the conversion of Infor ION API responses by convering XML to python
objects.

The reconmended way to use this module is by using the parse_mi_xml factory function
to generate a MiData object that contains relevant parameters such as metadata, records,
program and transaction.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3. See ../LICENCE '''

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional
from urllib import response
from xml.etree import ElementTree
import functools



class Status(Enum):
    ERROR = -1
    EMPTY = 0
    VALID = 1


@dataclass
class MiData:
    ''' Dataclass to populate with request data. Use the parseMiXml
    to parse XML and return an istance of this class'''

    program: str
    transaction: str
    metadata: List[Dict] = field(repr=False)
    records: List[Dict] = field(repr=False)
    status: Status = field(init=False)

    def __post_init__(self):
        if len(self.records):
            self.status = Status.VALID
        else:
            self.status = Status.EMPTY

@dataclass
class MiError:
    ''' Dataclass to populate with error codes from the API.
    Since errors can occur not only because of technical errors
    but also because of no search results, an error object is
    returned instead of raising it. isinstance(MiError) to check
    for this.    
    '''
    code: str
    description: str
    status: Status = field(default=Status.ERROR, init=False)


@functools.cache
def _parse_xml(xml_str: Union[str, bytes]) -> ElementTree.ElementTree:
    ''' Parses a xml string and returns the element tree. '''
    xml_element_tree = ElementTree.ElementTree(ElementTree.fromstring(xml_str))
    return xml_element_tree


@functools.cache
def _xml_ns_tag(xml_str: Union[str, bytes]) -> str:
    ''' Returns the XML name space as a string'''
    xml_ns_tag = _parse_xml(xml_str).getroot().tag.split('}')[0] + '}'
    return xml_ns_tag


def _has_mi_error(xml_str: str) -> Union[MiError, None]:
    xml_element_tree = _parse_xml(xml_str).getroot()

    if xml_element_tree.tag == (_xml_ns_tag(xml_str) + 'ErrorMessage'):
        mi_error_message = xml_element_tree.find(_xml_ns_tag(xml_str) + 'Message').text
        mi_error_type = xml_element_tree.get('type')

        return MiError(mi_error_type, mi_error_message)



def get_program(xml_str: Union[str, bytes]) -> Optional[str]:
    ''' Reurns the program name'''
    xml_root = _parse_xml(xml_str).getroot()

    program = xml_root.find(_xml_ns_tag(xml_str) + 'Program').text
    return str(program)


def get_transaction(xml_str: Union[str, bytes]) -> str:
    ''' Returns the transaction name'''
    xml_root = _parse_xml(xml_str).getroot()

    transaction = xml_root.find(_xml_ns_tag(xml_str) + 'Transaction').text
    return str(transaction)


def get_metadata(xml_str: Union[str, bytes]) -> List[Dict]:
    ''' Returns the metadata '''
    xml_root = _parse_xml(xml_str).getroot()

    return [
        child.attrib for child
        in xml_root.find(_xml_ns_tag(xml_str) + 'Metadata').iter()
        if child.attrib
    ]


def get_records(xml_str: Union[str, bytes]) -> List[Dict]:
    ''' Returns the records as a list of dicts '''
    xml_root = _parse_xml(xml_str).getroot()

    return [
        {
            mi_name_value.find(_xml_ns_tag(xml_str) + 'Name').text:
            mi_name_value.find(_xml_ns_tag(xml_str) + 'Value').text
            for mi_name_value in mi_record.findall(_xml_ns_tag(xml_str) + 'NameValue')
        }
        for mi_record in xml_root.findall(_xml_ns_tag(xml_str) + 'MIRecord')
    ]


def parse_mi_xml(xml_str: str) -> Union[MiData, MiError]:
    '''
    Parses a MI xml string and returns a MiData dataclass.
    If an error is detected in the result, then a MiError
    object is returned instead.
    '''
    miError = _has_mi_error(xml_str)

    if miError:
        return miError

    else:
        return MiData(
            program = get_program(xml_str),
            transaction = get_transaction(xml_str),
            metadata = get_metadata(xml_str),
            records = get_records(xml_str)
        )
