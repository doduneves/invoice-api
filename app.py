from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

mock_invoices = [
    {
        "id": "1",
        "document": "Ensino Superior, Cursos de Graduação e Demais Cursos", # STRING, 
        "description": "Mensalidade referente ao mês de junho, valor de R$1.500,00", #STRING,
        "amount": "1500.00", #CURRENCY,
        "referenceMonth": "2020-07-01T00:00:00.000Z", #DATETIME,
        "referenceYear": 2020, #INT,
        "createdAt": "2020-07-12T00:00:00.000Z", #DATETIME,
        "isActive": True, #True,
        "deactiveAt": "2020-01-01T00:00:00.000Z" #DATETIME
    }
]

@app.route('/invoices', methods=['GET'])
def list_invoices():
    return jsonify(mock_invoices), 200

@app.route('/invoices/<int:invoice_id>', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug = True)