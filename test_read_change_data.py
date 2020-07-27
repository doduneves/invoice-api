import os
import tempfile
import json

import pytest

from config import db_connect
import dateutil.parser

from test_basic import client

   
data_json = dict(
    id = '94de4874-cf9b-11ea-87d0-0242ac130003',
    amount = 8800,
    description = "Testando um documento alterado",
    document = "Documento Teste Alterado",
    referenceMonth = "2020-09-01T00:00:00.000Z",
    referenceYear = 2022
)

def test_read_invoice(client):

    res = client.get('/invoices/' + data_json['id'], 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'})
        
    result_json = res.get_json()
    assert res.status_code == 200
    assert 'error' not in result_json

    assert result_json['id'] == '94de4874-cf9b-11ea-87d0-0242ac130003'
    assert result_json['amount'] == '1200'
    assert result_json['description'] == 'Testando um documento postado'
    assert result_json['document'] == 'Documento Teste'
    
    referenceMonth = dateutil.parser.parse(result_json['referenceMonth'])
    
    assert referenceMonth.strftime('%Y-%m-%d') == '2020-09-01'
    assert result_json['referenceYear'] == 2020
    assert result_json['isActive'] == True
    assert result_json['deactiveAt'] == None

    
def test_update_inserted_invoice(client):
    
    res = client.put('/invoices/'+ data_json['id'],
        data = json.dumps(data_json.copy()),
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        content_type = 'application/json')
        
    result_json = res.get_json()
    print(result_json)
    assert res.status_code == 200
    assert 'message' in result_json
    assert result_json['message'] == "Updated Succesfully"
    

def test_deactivate_inserted_invoice(client):
    
    res = client.delete('/invoices/'+ data_json['id'],
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'})
        
    result_json = res.get_json()
    assert res.status_code == 200
    assert 'message' in result_json
    assert result_json['message'] == "Invoice Deactivated Succesfully"


def test_delete_inserted_invoice(client):
    
    res = client.delete('/invoices/'+ data_json['id'],
        data = json.dumps({"force_delete": "true"}),
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        content_type = 'application/json')
        
    result_json = res.get_json()
    assert res.status_code == 200
    assert 'message' in result_json
    assert result_json['message'] == "Invoice Removed Succesfully"