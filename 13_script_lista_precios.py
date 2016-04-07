import csv
from proteus import config, Model, Wizard
from decimal import Decimal

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Company = Model.get('company.company')

def ListPrice():
    PriceList = Model.get('product.price_list')
    price_list = csv.reader(open('lista_precios.csv', 'r'))
    header=True
    inicio=1
    empresa = '1191758435001'
    if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
        company, = Company.find([('party.vat_number', '=', empresa)])
        company = company
        
    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        price_list.next()

    for index,row in enumerate(price_list):
        price_list = PriceList()
        price_list.name = row[0]
        price_list.company=company
        formula = row[1]
        if formula == '0':
            price_list.save()
            print "Created price list ", price_list
        else:
            price_list_line = price_list.lines.new()
            if formula == '5':
                price_list_line.formula = 'unit_price * (1 - 0.05)'
            elif formula == '10':
                price_list_line.formula = 'unit_price * (1 - 0.10)'
            price_list.save()
            print "Created price list ", price_list
ListPrice()

