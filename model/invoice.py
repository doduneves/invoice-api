import uuid
from datetime import datetime
import decimal

class Invoice:    
    def __init__(self, body_json, id_inv = None):

        self.id = id_inv if id_inv else uuid.uuid1()
        self._document = body_json["document"] if "document" in body_json else None
        self.description = body_json["description"] if "description" in body_json else ""
        self._amount = body_json["amount"] if "amount" in body_json else None
        self._referenceMonth = body_json["referenceMonth"] if "referenceMonth" in body_json else None
        self._referenceYear = body_json["referenceYear"] if "referenceYear" in body_json else None
        self.createdAt = body_json["createdAt"] if "createdAt" in body_json else datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.isActive = body_json["isActive"] if "isActive" in body_json else True
        self.deactiveAt = body_json["deactiveAt"] if "deactiveAt" in body_json else None
        self._links = {
                "self": {
                    "href": "http://localhost:5000/invoices/" + str(self.id)
                }
            }

    

    # Validacoes
    @property
    def _document(self):
        return self.document

    @_document.setter
    def _document(self, doc):
        if not doc: raise Exception("Document cannot be null")
        self.document = doc


    @property
    def _amount(self):
        return self.amount

    @_amount.setter
    def _amount(self, amount):
        if not amount: raise Exception("Amount cannot be null")
        self.amount = str(decimal.Decimal(amount))


    @property
    def _referenceMonth(self):
        return self.referenceMonth

    @_referenceMonth.setter
    def _referenceMonth(self, referenceMonth):
        if not referenceMonth: raise Exception("Reference Month cannot be null")
        self.referenceMonth = referenceMonth


    @property
    def _referenceYear(self):
        return self.referenceYear

    @_referenceYear.setter
    def _referenceYear(self, referenceYear):
        if not referenceYear: raise Exception("Reference Year cannot be null")
        self.referenceYear = referenceYear

    @staticmethod
    def generate_from_row(row):
        body_json = {
            "document": row[1],
            "description": row[2],
            "amount": row[3],
            "referenceMonth": row[4],
            "referenceYear": row[5],
            "createdAt": row[6],
            "isActive": row[7],
            "deactiveAt": row[8],
        }
        return Invoice(body_json, row[0])
        
        