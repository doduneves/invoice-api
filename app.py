from flask import Flask, jsonify, request
from datetime import datetime

from model.invoice import Invoice

import json

app = Flask(__name__)


@app.route('/invoices/', methods=['GET'])
def list_invoices():

    # Tratando o valor das paginas
    page = int(request.args.get('page')) if request.args.get('page') else 1
    page = page if page > 1 else 1

    # Obtendo o valor da query para ordenacao
    order_query = request.args.get('order')

    # Obtendo valores de filtro
    document_filter = request.args.get('document')
    year_filter = request.args.get('year')
    month_filter = request.args.get('month')
    
    filtered_invoices = mock_invoices.copy()
    
    if(document_filter or year_filter or month_filter):
        i = 0
        while i < len(filtered_invoices):

            item_removed = False

            # Filtro por documento
            if document_filter and document_filter.lower() not in filtered_invoices[i]['document'].lower():
                item_removed = True

            # # Filtro por Ano
            if year_filter and year_filter not in filtered_invoices[i]['referenceYear']:
                item_removed = True

            # # Filtro por Mes - "-09-" p.ex.
            if month_filter and ("-"+month_filter.zfill(2)+"-") not in filtered_invoices[i]['referenceMonth']:
                item_removed = True

            if item_removed:
                filtered_invoices.remove(filtered_invoices[i])                
            else:
                i += 1

    ordered_invoices = order_invoices(filtered_invoices, order_query)

    limit = 5 # Itens por pagina
    count_invoices = len(filtered_invoices)

    links_json = generate_links_json(page, limit, ordered_invoices)    

    invoices = separate_result_per_page(ordered_invoices, limit, page)

    result = create_list_result(links_json, limit, count_invoices, invoices)

    return jsonify(result), 200

def order_invoices(invoices_list, order_query):

    invoices_list.sort(key = lambda x: x.get('createdAt'))

    if (order_query):        
        order_by_mouth = True if 'referenceMonth' in order_query else False
        order_by_year = True if 'referenceYear' in order_query else False
        order_by_document = True if 'document' in order_query else False    
        
        invoices_list.sort(key = lambda x: (x.get('referenceMonth') if order_by_mouth else '',
            x.get('referenceYear') if order_by_year else '',
            x.get('document') if order_by_document else ''))


    return invoices_list


def generate_links_json(page, limit, mock_invoices):
    
    count_invoices = len(mock_invoices)

    previous_page = page - 1 if page > 1 else None 
    next_page = page + 1 if int(count_invoices/limit)+1 > page else None    

    links_json = {
        "self": {
            "href": "http://localhost:5000/invoices?page=" + str(page)
        },
        "first": {
            "href": "http://localhost:5000/invoices"
        },
        "last": {
            "href": "http://localhost:5000/invoices?page=" + str(int(count_invoices/limit)+1)
        }
    }

    if(previous_page):
        links_json["prev"] = {
            "href": "http://localhost:5000/invoices?page=" + str(previous_page)
        }    
    
    if(next_page):
        links_json["next"] = {
            "href": "http://localhost:5000/invoices?page=" + str(next_page)
        }

    return links_json

def separate_result_per_page(mock_invoices, limit, page):  

    invoices = []
    count_invoices = len(mock_invoices)
    
    # Lista de elementos na resposta
    first_element = (page-1) * limit
    last_element = (page * limit)
    last_element = count_invoices if (last_element > count_invoices) else last_element

    for i in range(first_element, last_element):
        invoices.append(mock_invoices[i])
    
    return invoices

def create_list_result(links, limit, count_invoices, invoices):
    return {
        "_links": links,
        "per_page": limit,
        "total": count_invoices,
        "invoices": invoices
    }

@app.route('/invoices/<string:invoice_id>', methods=['GET'])
def get_invoices_by_id(invoice_id):
    invoice = [inv for inv in mock_invoices if inv["id"] == invoice_id]
    return jsonify(invoice), 200

@app.route('/invoices', methods=['POST'])
def create_invoice():

    if request.get_json():
            invoice = Invoice(request.get_json())

            mock_invoices.append(invoice.__dict__)

            return jsonify(invoice.__dict__), 201
    else:
        return jsonify({'error': 'No requested body found'}), 400


@app.route('/invoices/<string:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    for invoice in mock_invoices:
        if invoice['id'] == invoice_id:

            for k in invoice.keys():
                if k in request.get_json():
                    invoice[k] = request.get_json()[k]

            new_invoice = Invoice(invoice,invoice_id)

            mock_invoices.remove(invoice)
            mock_invoices.append(new_invoice.__dict__)

            return jsonify(new_invoice.__dict__), 200

    return jsonify({'error': 'Invoice to update was not found'}), 404


@app.route('/invoices/<string:invoice_id>', methods=['DELETE'])
def deactivate_invoice(invoice_id):
    for invoice in mock_invoices:
        if invoice['id'] == invoice_id and invoice['isActive']:
            actual_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            invoice["deactiveAt"] = actual_date
            invoice["isActive"] = False

            return jsonify(invoice), 200

    return jsonify({'error': 'Invoice to remove was not found'}), 404

mock_invoices = ''
with open('mock_data.json') as json_file:
    mock_invoices = json.load(json_file)    

if __name__ == '__main__':
    app.run(debug = True)
