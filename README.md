# Invoices API

Api Restful de gerenciamento de notas fiscais (invoices).

### Instalação
É necessário ter o Python (v3) instalado em sua máquina para conseguir rodar o projeto.

Baixe o projeto:

`$ git clone https://github.com/doduneves/invoice-api.git`

Execute-o em ambiente virtual

`$ source .venv/Scripts/activate`

E instale todas as dependências do projeto no ambiente:

`$ pip install -r requirements.txt`


### Utilização
A API dispôe dos verbos e seus endpoints: 

**Lista todas os *invoices* disponíves**
- GET: http://127.0.0.1:5000/invoices

Filtrando listagem por ano, mês ou documento, através dos paramêtros da querystring:
- http://127.0.0.1:5000/invoices?document=garrafa
- http://127.0.0.1:5000/invoices?year=2020
- http://127.0.0.1:5000/invoices?month=9

Ordenando a listagem por ano, mês e/ou documento, através dos paramêtros da querystring:
- http://127.0.0.1:5000/invoices?order=referenceMonth
- http://127.0.0.1:5000/invoices?order=referenceYear,document

A listagem é exibida em páginas de 5 itens cada. Para selecionar o numero da página:
- http://127.0.0.1:5000/invoices?page=2


**Obtem o invoice pelo determinado [id]**

- GET: http://127.0.0.1:5000/invoices/[id]

**Insere um novo Invoice sendo declarado no body da requisição. **

- POST: http://127.0.0.1:5000/invoices

**Formato do body:**
{
  "amount": [number],
  "description": [string],
  "document": [string],
  "referenceMonth": [date],
  "referenceYear": [number]
}

**Atualiza um Invoice com o id declarado na querystring e os atributos a serem atualizados no body da requisição no mesmo formato do POST.**

- PUT: http://127.0.0.1:5000/invoices/[id]

** Desativa um invoice já inserido **

- DELETE: http://127.0.0.1:5000/invoices/[id]

### Últimas Atualizações
*18/jul - Mockando dados e fazendo paginacao*

*18/jul - LIST: Ordenar por mês, ano, documentos ou a combinação entre eles*

*19/jul - LIST: ajuste ordenação e filtros por documents, mouth e ano*

*20/jul - POST, PUT e DELETE*
