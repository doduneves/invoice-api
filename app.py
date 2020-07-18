from flask import Flask, jsonify, request
from datetime import datetime

import json

app = Flask(__name__)


@app.route('/invoices/', methods=['GET'])
def list_invoices():

    invoices = []
    
    limit = 5 # Itens por pagina
    count_invoices = len(mock_invoices)

    # Tratando o valor das paginas
    page = int(request.args.get('page')) if request.args.get('page') else 1
    page = page if page > 1 else 1

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
    
    # Lista de elementos na resposta
    first_element = (page-1) * limit
    last_element = (page * limit)
    last_element = count_invoices if (last_element > count_invoices) else last_element

    for i in range(first_element, last_element):
        print(i)
        invoices.append(mock_invoices[i])

    result = {
        "_links": links_json,
        "per_page": limit,
        "total": count_invoices,
        "invoices": invoices
    }

    return jsonify(result), 200

@app.route('/invoices/<string:invoice_id>', methods=['GET'])
def get_invoices_by_id(invoice_id):
    invoice = [inv for inv in mock_invoices if inv["id"] == invoice_id]
    return jsonify(invoice), 200

@app.route('/invoices', methods=['POST'])
def create_invoice():
    new_invoice = request.get_json()

    return jsonify(new_invoice), 201

@app.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    for invoice in mock_invoices:
        if invoice['id'] == invoice_id:
            invoice = request.get_json()

            return jsonify(invoice), 200

    return jsonify({'error': 'Invoice to update was not found'}), 404



@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def deactivate_invoice(invoice_id):
    for invoice in mock_invoices:
        if invoice['id'] == invoice_id:
            actual_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            invoice["deactiveAt"] = actual_date

            return jsonify(invoice), 200

    return jsonify({'error': 'Invoice to remove was not found'}), 404

mock_invoices = ''
with open('mock_data.json') as json_file:
    mock_invoices = json.load(json_file)
    

if __name__ == '__main__':
    app.run(debug = True)
