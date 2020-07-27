import os
import tempfile
import json

import pytest

from config import db_connect

from test_basic import client

data_json = dict(
    id = '94de4874-cf9b-11ea-87d0-0242ac130003',
    amount = 1200,
    description = "Testando um documento postado",
    document = "Documento Teste",
    referenceMonth = "2020-09-01T00:00:00.000Z",
    referenceYear = 2020
)

# POST TESTS
def test_post_invoice_empty_document_error(client):
    post_data = data_json.copy()
    post_data["document"] = None

    res = client.post('/invoices', 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        data = json.dumps(post_data),
        content_type = 'application/json')
        
    result_json = res.get_json()
    assert res.status_code == 503
    assert 'error' in result_json

    
def test_post_invoice_amount_error(client):
    post_data = data_json.copy()
    post_data["amount"] = "Valor errado"

    res = client.post('/invoices', 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        data = json.dumps(post_data),
        content_type = 'application/json')
        
    result_json = res.get_json()
    assert 'error' in result_json
    assert res.status_code == 503


    
def test_post_invoice_referenceyear_error(client):
    post_data = data_json.copy()
    post_data["referenceYear"] = "Valor errado"

    res = client.post('/invoices', 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        data = json.dumps(post_data),
        content_type = 'application/json')
        
    result_json = res.get_json()
    assert 'error' in result_json
    assert res.status_code == 503


def test_post_invoice_referencemonth_error(client):
    post_data = data_json.copy()
    post_data["referenceMonth"] = "Valor errado"

    res = client.post('/invoices', 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        data = json.dumps(post_data),
        content_type = 'application/json')
        
    result_json = res.get_json()
    assert res.status_code == 503
    assert 'error' in result_json

    
def test_post_invoice_success(client):

    res = client.post('/invoices', 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        data = json.dumps(data_json),
        content_type = 'application/json')
    
    result_json = res.get_json()
    assert res.status_code == 201

    assert result_json['id'] == '94de4874-cf9b-11ea-87d0-0242ac130003'
    assert result_json['amount'] == '1200'
    assert result_json['description'] == 'Testando um documento postado'
    assert result_json['document'] == 'Documento Teste'
    assert result_json['referenceMonth'] == '2020-09-01T00:00:00.000Z'
    assert result_json['referenceYear'] == 2020
    assert result_json['isActive'] == True
    assert result_json['deactiveAt'] == None


def test_post_repeated_invoice(client):
    post_data = data_json.copy()

    res = client.post('/invoices', 
        headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'},
        data = json.dumps(post_data),
        content_type = 'application/json')
    
    result_json = res.get_json()
    assert res.status_code == 503
    assert 'error' in result_json