''' mi_parser.py
The parser module, part of the getting-and-setting package contains functions
to ease the conversion of Infor ION API responses by convering XML to python
objects.

The reconmended way to use this module is by using the parse_mi_xml factory function
to generate a MiData object that contains relevant parameters such as metadata, records,
program and transaction.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3. See ../LICENCE '''

from shutil import ExecError
from typing import Union, Any
from xml.etree import ElementTree
import functools

from .mi_models import MiRecords
from .mi_models import MiPrograms
from .mi_models import MiProgramMetadata
from .mi_models import MiTransactionMetadata
from .mi_models import MiFieldMetadata
from .mi_models import MiError


MI_TYPES = {
    'Alpha': str,
    'Date': str,
    'Integer': int,
    'Number': int,
    'Numeric': float
}

MI_VALUES = {
    'true': True,
    'false': False
}


def convert_mi_value(any_value: str) -> Any:
    ''' Convert strings containing boolan string to a bool '''
    if any_value in MI_VALUES.keys():
        return MI_VALUES[any_value]
    else:
        print(f'Could not convert {any_value}')
        return any_value


def convert_mi_fieldtype(type_str: str) -> object:
    ''' Convert strings containing type information to python types '''
    if type_str in MI_TYPES.keys():
        return MI_TYPES[type_str]

    else:
        print(f'{type_str} is not a recognized type')
        return Any


@functools.cache
def parse_xml(xml_str: Union[str, bytes]) -> ElementTree.ElementTree:
    ''' Parses a xml string and returns the element tree. '''
    xml_element_tree = ElementTree.ElementTree(ElementTree.fromstring(xml_str))
    return xml_element_tree


@functools.cache
def xml_ns_tag(xml_str: Union[str, bytes]) -> str:
    ''' Returns the XML name space as a string'''
    xml_ns_tag = parse_xml(xml_str).getroot().tag.split('}')[0] + '}'
    return xml_ns_tag


def has_mi_error(xml_str: str) -> Union[MiError, None]:
    ''' Checks if the xml has error messages from the api,
    and returns a MiError object if it exits '''
    xml_element_tree = parse_xml(xml_str).getroot()

    if xml_element_tree.tag == (xml_ns_tag(xml_str) + 'ErrorMessage'):
        mi_error_message = str(xml_element_tree.find(xml_ns_tag(xml_str) + 'Message').text)
        mi_error_type = str(xml_element_tree.get('type'))

        return MiError(mi_error_type, mi_error_message)

    else:
        return None


def mi_parse_execute(xml_str: str) -> Union[MiRecords, MiError]:
    '''
    Parses a MI xml string and returns a MiData dataclass.
    If an error is detected in the result, then a MiError
    object is returned instead.
    '''
    xml_root = parse_xml(xml_str).getroot()
    miError = has_mi_error(xml_str)

    if miError:
        return miError

    return MiRecords(
        program = xml_root.find(xml_ns_tag(xml_str) + 'Program').text,
        transaction = xml_root.find(xml_ns_tag(xml_str) + 'Transaction').text,
        metadata = [
           child.attrib for child
            in xml_root.find(xml_ns_tag(xml_str) + 'Metadata').iter()
            if child.attrib
        ],
        records = [
           {
                mi_name_value.find(xml_ns_tag(xml_str) + 'Name').text:
                mi_name_value.find(xml_ns_tag(xml_str) + 'Value').text
                for mi_name_value in mi_record.findall(xml_ns_tag(xml_str) + 'NameValue')
            }
            for mi_record in xml_root.findall(xml_ns_tag(xml_str) + 'MIRecord')
        ]
    )


def mi_parse_programs(xml_str: Union[str, bytes]) -> Union[MiPrograms, MiError]:
    ''' Parse a MI xml from a progam call. Returns a MiPrograms dataclass that
    contains the list of program names. '''
    xml_root = parse_xml(xml_str).getroot()

    records = [
        name.text for name in
        xml_root.findall(xml_ns_tag(xml_str) + 'Name')
    ]

    return MiPrograms(records)


def mi_parse_metadata(xml_str: Union[str, bytes]) -> Union[MiProgramMetadata, MiError]:
    mi_error = has_mi_error(xml_str)

    if mi_error:
        return mi_error

    xml_root = parse_xml(xml_str).getroot()
    xml_ns = xml_ns_tag(xml_str)

    miProgramMetadata = MiProgramMetadata(
        program = xml_root.attrib['Program'],
        description = xml_root.attrib['Description'],
        version = xml_root.attrib['Version'],
        transactions = [
            MiTransactionMetadata(
                program=mi_transaction.attrib['Program'],
                transaction=mi_transaction.attrib['Transaction'],
                description=mi_transaction.attrib['Description'],
                multi=convert_mi_value(mi_transaction.attrib['Multi']),
                outputs=[
                    MiFieldMetadata(
                        name=mi_field.attrib['Name'],
                        description=mi_field.attrib['Description'],
                        fieldtype=str(convert_mi_fieldtype(mi_field.attrib['FieldType'])),
                        length=int(mi_field.attrib['Length']),
                        mandetory=convert_mi_value(mi_field.attrib['Mandatory'])
                    )
                    for mi_field
                    in mi_transaction.find(xml_ns + 'OutputFieldList')
                ],
                inputs=[
                    MiFieldMetadata(
                        name=mi_field.attrib['Name'],
                        description=mi_field.attrib['Description'],
                        fieldtype=convert_mi_fieldtype(mi_field.attrib['FieldType']),
                        length=int(mi_field.attrib['Length']),
                        mandetory=convert_mi_value(mi_field.attrib['Mandatory'])
                    )
                    for mi_field
                    in mi_transaction.find(xml_ns + 'InputFieldList')
                ]
            )
            for mi_transaction in xml_root.findall(xml_ns + 'Transaction') 
        ]
    )
    
    return miProgramMetadata
