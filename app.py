import sys
import os
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )


from flask import Flask, jsonify, request
from functools import wraps
from datetime import datetime

import psycopg2

from config.db_generate import create_table
from config.db_connect import connect_db, close_db
from config.config import config

from model.invoice import Invoice

import json

app = Flask(__name__)

app.config['SECRET_KEY']='822e75ef88572e1278a74621385280ec'

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if request.headers.get('Auth-Key') and request.headers.get('Auth-Key') == app.config['SECRET_KEY']:
            return func(*args, **kwargs)
        else:
            return jsonify({"message": "Access Denied"}), 403
        
    return check_token

@app.route('/invoices/', methods=['GET'])
@require_api_token
def list_invoices():

    try:
        
        # Obtendo o valor da query para ordenacao
        order_query = request.args.get('order')
        
        order_string = order_invoices(order_query)

        
    except:
        print("Error generating order query")
        return jsonify({"error":"Something went wrong. Please, Contact the admin"}), 503

    try:
       
        # Obtendo valores de filtro
        filter_string = filter_invoices(request.args)


    except:
        print("Error generating filter query")
        return jsonify({"error":"Something went wrong. Please, Contact the admin"}), 400
    try:
        (conn, cur) = connect_db()

        psql_query_string = """
            SELECT id, document, description, amount, referenceMonth, referenceYear, createdAt, isActive, deactiveAt
            FROM invoices
        """

        psql_query_string += filter_string + order_string

        cur.execute(psql_query_string)
        rows = cur.fetchall()

        print("The number of parts: ", cur.rowcount)
        
        list_invoices = []
        for row in rows:
            invoice = Invoice.generate_from_row(row)
            list_invoices.append(invoice.__dict__)
        
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({"error":"Could not connect to Database"}), 503

    finally:
        close_db(conn, cur)

    try:
        # Tratando o valor das paginas
        page = int(request.args.get('page')) if request.args.get('page') else 1
        page = page if page > 1 else 1
    
        limit = 5 # Itens por pagina
        
        links_json = generate_links_json(page, limit, list_invoices)    


        invoices = separate_result_per_page(list_invoices, limit, page)

        result = create_list_result(links_json, limit, cur.rowcount, invoices)

        return jsonify(result), 200
    except:
        print("Error while separeting itens per page")
        return jsonify({"error":"Something went wrong. Please, Contact the admin"}), 400



def order_invoices(order_query):
    
    order_string = "ORDER BY "

    if (order_query):
        if '-referenceMonth' in order_query:
            order_string += "referenceMonth DESC,"
        elif 'referenceMonth' in order_query:
            order_string += "referenceMonth ASC,"

        if '-referenceYear' in order_query:
            order_string += "referenceYear DESC,"
        if 'referenceYear' in order_query:
            order_string += "referenceYear ASC,"
            
        if '-document' in order_query:
            order_string += "document DESC,"
        if 'document' in order_query:
            order_string += "document ASC,"

    order_string += "createdAt ASC"

    return order_string


def filter_invoices(query_args):

    # Obtendo valores de filtro
    document_filter = query_args.get('document')
    year_filter = query_args.get('year')
    month_filter = query_args.get('month')
    
    filter_string = "WHERE "

    # Filtro por documento
    if document_filter:
        filter_string += "LOWER(document) LIKE '%" + document_filter.lower() + "%' AND"

    # # Filtro por Ano
    if year_filter:
        filter_string += "referenceyear = '" + year_filter + "' AND"

    # # Filtro por Mes - "-09-" p.ex.
    if month_filter:
        filter_string += "referencemonth = '" + month_filter + "' AND"

    if filter_string == "WHERE ":
        filter_string = ""
    else:
        filter_string = filter_string[:-3]
    

    return filter_string


def generate_links_json(page, limit, invoices):
    
    count_invoices = len(invoices)

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

def separate_result_per_page(list_invoices, limit, page):  

    invoices = []
    count_invoices = len(list_invoices)
    
    # Lista de elementos na resposta
    first_element = (page-1) * limit
    last_element = (page * limit)
    last_element = count_invoices if (last_element > count_invoices) else last_element

    for i in range(first_element, last_element):
        invoices.append(list_invoices[i])
    
    return invoices

def create_list_result(links, limit, count_invoices, invoices):
    return {
        "_links": links,
        "per_page": limit,
        "total": count_invoices,
        "invoices": invoices
    }

@app.route('/invoices/<string:invoice_id>', methods=['GET'])
@require_api_token
def get_invoices_by_id(invoice_id):
    try:
        conn, cur = connect_db()

        cur.execute("SELECT id, document, description, amount, referenceMonth, referenceYear, createdAt, isActive, deactiveAt "
        + "FROM invoices WHERE id = '" + invoice_id + "';")
        row = cur.fetchone()

        if row:
            invoice = Invoice.generate_from_row(row)  
        else:
            return jsonify({'error': 'Invoice not found'}), 503
          
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({"error":"Could not connect to Database"}), 503
    finally:
        close_db(conn, cur)

        
    return jsonify(invoice.__dict__), 200
    

@app.route('/invoices', methods=['POST'])
@require_api_token
def create_invoice():

    if request.get_json():
        
        try:
            conn, cur = connect_db()

            if 'id' in request.get_json():
                invoice = Invoice(request.get_json(), request.get_json()['id'])
            else:
                invoice = Invoice(request.get_json())


            insert_string = ("INSERT INTO invoices VALUES('" 
                    + str(invoice.id) + "', '"
                    + invoice.document + "', '"
                    + invoice.description + "', "
                    + str(invoice.amount) + ", '"
                    + str(invoice.referenceMonth) + "', '"
                    + str(invoice.referenceYear) + "', '"
                    + str(invoice.createdAt) + "', "
                    + str(invoice.isActive) + ");")

            cur.execute(insert_string)

            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return jsonify({'error': 'Some error inserting data'}), 503
        finally:
            close_db(conn, cur)


        return jsonify(invoice.__dict__), 201

    else:
        return jsonify({'error': 'No requested body found'}), 400


@app.route('/invoices/<string:invoice_id>', methods=['PUT'])
@require_api_token
def update_invoice(invoice_id):
    
    if request.get_json():

        try:
            conn, cur = connect_db()
                
            set_string = ""
            for k in request.get_json().keys():
                set_string += str(k) + " = '" + str(request.get_json()[k]) + "', "

            set_string = set_string[:-2]
            
            
            update_sql = ("UPDATE invoices " +
                    " SET " + set_string +
                    " WHERE id = '" + invoice_id + "';")

            cur.execute(update_sql)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return jsonify({'error': 'Invoice to update was not found'}), 503

        finally:
            close_db(conn, cur)

        
        return jsonify({"message":"Updated Succesfully"}), 200
    else:
        return jsonify({'error': 'No requested body found'}), 400
        


@app.route('/invoices/<string:invoice_id>', methods=['DELETE'])
@require_api_token
def deactivate_invoice(invoice_id):
    try:
        conn, cur = connect_db()

        actual_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


        if request.get_json() and 'force_delete' in request.get_json() and request.get_json()['force_delete']:
            delete_sql = ("DELETE FROM invoices " +
                "WHERE id = '" + invoice_id + "';")
            
            deleted_info = "Invoice Removed Succesfully"

        
        else:
            delete_sql = ("UPDATE invoices " +
                    " SET isactive = False, deactiveAt = '" + actual_date +
                    "' WHERE id = '" + invoice_id + "';")
        
            deleted_info = "Invoice Deactivated Succesfully"

        print(delete_sql)
        cur.execute(delete_sql)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'error': 'Invoice to remove was not found'}), 503
    finally:
        close_db(conn, cur)
    
    return jsonify({"message": deleted_info}), 200


if __name__ == '__main__':
    create_table()
    app.run(debug = True)
