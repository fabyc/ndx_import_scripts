import csv
from proteus import config, Model, Wizard
from decimal import Decimal

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Lang = Model.get('ir.lang')
Company = Model.get('company.company')
Employe = Model.get('company.employee')
List = Model.get('product.price_list')
Term = Model.get('account.invoice.payment_term')
Location = Model.get('stock.location')
Party = Model.get('party.party')
Shop = Model.get('sale.shop')

def LoadShop():
    header=True
    inicio=1
    shop= Shop()
    shop.name = "TIENDA MATRIZ"
    empresa = '1191758435001'
    if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
        company, = Company.find([('party.vat_number', '=', empresa)])
        shop.company = company
        
    if len(Location.find([('name', '=', 'BODEGA MATRIZ')])) == 1:
        warehouse, = Location.find([('name', '=', 'BODEGA MATRIZ')])
        shop.warehouse = warehouse
    
    if len(List.find([('name', '=', 'LISTA DE PRECIOS NORMAL')])) == 1:
        price_list, = List.find([('name', '=', 'LISTA DE PRECIOS NORMAL')])
        shop.price_list = price_list
        
    if len(TermPay.find([('name', '=', 'AL CONTADO')])) == 1:
        payment_term, = TermPay.find([('name', '=', 'AL CONTADO' )])
        shop.payment_term = payment_term
    
    if len(Party.find([('vat_number', '=','9999999999999')])) == 1:
        party, = Party.find([('vat_number', '=','9999999999999')])
        shop.party = party
        
    shop.self_pick_up = True
    shop.enough_stock_qty = 'quantity'
    shop.enough_stock = True
    shop.save()
    print "Created shop ", shop

LoadShop()

