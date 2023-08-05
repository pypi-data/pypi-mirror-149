import pytest
import src.api as api
import src.parser as parser

def test_api_construct_request_url() -> None:
    params = {'max_recs': 0, 'ROUT': 'AA0001', 'WHLO': 'ZZZ'}
    params_str = api.dict_to_param_str(params)
    request_url = api.create_url('server.company', 2200, 'DRS005MI', 'GetRoute', params_str)

    assert request_url == 'http://server.company:2200/m3api-rest/execute/DRS005MI/GetRoute;max_recs=0;?ROUT=AA0001&WHLO=ZZZ'


def test_parser_read_many():
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <miResult xmlns="http://lawson.com/m3/miaccess">
        <Program>XXX000MI</Program>
        <Transaction>GetMi</Transaction>
        <Metadata>
            <Field name="COL1" type="A" length="6" description="Column 1"/>
            <Field name="COL2" type="N" length="1" description="Column 2"/>
        </Metadata>
        <MIRecord>
            <RowIndex>0</RowIndex>
            <NameValue>
                <Name>COL1</Name>
                <Value>ABCDEF</Value>
            </NameValue>
            <NameValue>
                <Name>COL2</Name>
                <Value>6</Value>
            </NameValue>
        </MIRecord>
        <MIRecord>
            <RowIndex>1</RowIndex>
            <NameValue>
                <Name>COL1</Name>
                <Value>GHIJKL</Value>
            </NameValue>
            <NameValue>
                <Name>COL2</Name>
                <Value>1</Value>
            </NameValue>
        </MIRecord>
    </miResult>'''

    miData = parser.parse_mi_xml(xml)

    assert isinstance(miData, parser.MiData)
    assert len(miData.metadata) == 2
    assert len(miData.records) == 2
    assert miData.program == 'XXX000MI'
    assert miData.transaction == 'GetMi'
