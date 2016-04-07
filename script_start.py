#! -*- coding: utf8 -*-
import csv
from proteus import config, Model, Wizard
import random
from random import randrange
import os
import binascii
from datetime import datetime, timedelta
from decimal import Decimal
import time

empresas = csv.reader(open('empresas.csv', 'r'))
parties = csv.reader(open('terceros.csv', 'r'))
empleados = csv.reader(open('empleados.csv', 'r'))
usuarios = csv.reader(open('usuarios.csv', 'r'))
categories = csv.reader(open('sub_categorias.csv', 'r'))
modules = csv.reader(open('modules_pymes.csv', 'r'))


database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

#variable para asignar empresa a contexto
company_context = '1191758435001'

def InitDatabase ():
    Module = Model.get('ir.module.module')
    inicio=4
    
    for i in range(inicio - 1):
        modules.next()

    for index,row in enumerate(modules):
        print row[0]
        name = row[0]
        (module,) = Module.find([('name', '=', name)])
        Module.install([module.id], config.context)
        Wizard('ir.module.module.install_upgrade').execute('upgrade')
        print "Installing ", name
InitDatabase ()

Party = Model.get('party.party')
Address = Model.get ('party.address')
Contact = Model.get ('party.contact_mechanism')
Country = Model.get('country.country')
Lang = Model.get('ir.lang')
Currency = Model.get('currency.currency')
Company = Model.get('company.company')
Employe = Model.get('company.employee')
Product = Model.get('product.product')
ProductTemplate = Model.get('product.template')
Category = Model.get('product.category')
ProductUom = Model.get('product.uom')
unit, = ProductUom.find([('symbol', '=', 'u')])
List = Model.get('product.price_list')
TermPay = Model.get('account.invoice.payment_term')
Location = Model.get('stock.location')
Device = Model.get('sale.device') 
Journal = Model.get('account.journal')
JournalStatement = Model.get('account.statement.journal')
Shop = Model.get('sale.shop')
Sequence = Model.get('ir.sequence')
JournalSequence = Model.get('account.journal.invoice.sequence')
SequenceStrict = Model.get('ir.sequence.strict')
Fiscal = Model.get('account.fiscalyear')
Group = Model.get('res.group')
Ir = Model.get('ir.model')
User= Model.get('res.user')
Field = Model.get('ir.model.field')
SaleStatement = Model.get('sale.device.account.statement.journal')

def LoadPartieC():

    Party = Model.get('party.party')
    parties = csv.reader(open('empresas.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        parties.next()

    for index,row in enumerate(parties):
        party = Party()
        if row[2]:
            tipo = '0'+str(row[2])
        else:
            tipo = ''
        party.name = row[1]
        party.type_document = tipo
        party.vat_number = row[0]
        party.active = True
        Calle = row[4]
        Ciudad = row[6]
        Pais = row[5]
        Telefono = row[3]
        Correo = "hola@nodux.ec"
        party.addresses.pop()
        (coun,) = Country.find([('code', '=', 'EC')])
        address = party.addresses.new(street=Calle, country=coun,city=Ciudad)
        (es,) = Lang.find([('code', '=', 'es_EC')])
        party.lang = es

        if (Telefono != ''):
            contactmecanism = party.contact_mechanisms.new(type='phone', value=Telefono)
        if (Correo != ''):
            contactmecanism = party.contact_mechanisms.new(type='email', value=Correo)
        party.save()
        print "Created party-company ", party
LoadPartieC()

def LoadCompanies ():

    Company = Model.get('company.company')
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        empresas.next()

    for index,row in enumerate(empresas):
        company = Company()
        cedula = row[0]

        if len(Party.find([('vat_number', '=', cedula)])) == 1:
            party, = Party.find([('vat_number', '=', cedula)])
            company.party = party
        (currency,) = Currency.find([('code', '=', 'USD')])   
        company.timezone = 'America/Guayaquil'
        company.currency = currency
        
        company.save()
        print "Created company ", company
LoadCompanies()

def LoadUserC():
    inicio=1
    User = Model.get('res.user')
    Company = Model.get('company.company')
    empresa = '1191758435001'

    user = User()
    if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
        company, = Company.find([('party.vat_number', '=', empresa)])
    users = User.find([('login','=', 'admin')])
    for user in users:
        user.main_company = company
    user.save()

LoadUserC()

if len(Company.find([('party.vat_number', '=', company_context)])) == 1:
    company, = Company.find([('party.vat_number', '=', company_context)])
    config._context['company'] = company.id

def LoadUser():

    User = Model.get('res.user')
    users = csv.reader(open('usuarios.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        users.next()

    for index,row in enumerate(users):
        user = User()
        user.name = row[0]
        user.login = row[1]
        user.password = row[2]
        (es,) = Lang.find([('code', '=', 'es_EC')])
        user.language = es
        user.save()
        print "Created user ", user
LoadUser()

def LoadPlanNIIF():
    AccountC = Model.get('account.create_chart.account')
    Company = Model.get('company.company')
    empresa = '1191758435001'
    Template = Model.get('account.account.template')
    Account = Model.get('account.account')
    account = Account()
    
    account_template = Template.find([('name', '=', 'PLAN DE CUENTAS NIIF ECUADOR'), ('parent','=', None)]) 
    if len(account_template) == 1:
        account_t, = account_template
        account_template = account_t
        
    if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
        company, = Company.find([('party.vat_number', '=', empresa)])
        company = company
    
    create_chart = Wizard('account.create_chart')
    create_chart.execute('account')
    create_chart.form.account_template = account_template
    create_chart.form.company = company
    create_chart.execute('create_account') 
    print "Created chart account"
LoadPlanNIIF()

def AccountConfiguration():
    print "Load account configuration "
    Account = Model.get('account.account')
    AccountConfiguration = Model.get('account.configuration')
    account_configuration = AccountConfiguration()
    if len(Account.find([('name', '=', 'DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')])) == 1:
        default_account_receivable, = Account.find([('name', '=', 'DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')])
        account_configuration.default_account_receivable = default_account_receivable
    if len(Account.find([('name', '=', 'CUENTAS POR PAGAR PROVEEDORES')])) == 1:
        default_account_payable, = Account.find([('name', '=', 'CUENTAS POR PAGAR PROVEEDORES')])
        account_configuration.default_account_payable = default_account_payable
    
    tax_roundings = account_configuration.tax_roundings.new()
    if len(Company.find([('party.vat_number', '=', company_context)])) == 1:
        company, = Company.find([('party.vat_number','=',company_context)])
        tax_roundings.company = company
    tax_roundings.method = 'document'
    account_configuration.save()
    print "Created account configuration ", account_configuration
AccountConfiguration()

def LoadParties ():

    Party = Model.get('party.party')
    parties = csv.reader(open('terceros.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        parties.next()

    for index,row in enumerate(parties):
        party = Party()
        if row[2]:
            tipo = '0'+str(row[2])
        else:
            tipo = ''
        party.name = row[1]
        party.type_document = tipo
        party.vat_number = row[0]
        party.active = True
        Calle = row[4]
        Ciudad = row[6]
        Pais = row[5]
        Telefono = row[3]
        Correo = "hola@nodux.ec"
        party.addresses.pop()
        (coun,) = Country.find([('code', '=', 'EC')])
        address = party.addresses.new(street=Calle, country=coun,city=Ciudad)
        (es,) = Lang.find([('code', '=', 'es_EC')])
        party.lang = es

        if (Telefono != ''):
            contactmecanism = party.contact_mechanisms.new(type='phone', value=Telefono)
        if (Correo != ''):
            contactmecanism = party.contact_mechanisms.new(type='email', value=Correo)
        party.save()
        print "Created party ", party
LoadParties()
def LoadEmployes ():

    Employe = Model.get('company.employee')
    employe = Employe()
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        empleados.next()

    for index,row in enumerate(empleados):
        employe = Employe()
        tercero = row[0]
        empresa = row[2]
        
        if len(Party.find([('vat_number', '=', tercero)])) == 1:
            party, = Party.find([('vat_number', '=', tercero)])
            employe.party = party
            
        if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
            company, = Company.find([('party.vat_number', '=', empresa)])
            employe.company = company
        employe.save()
        print "Created employee ", employe
LoadEmployes()

def LoadUserEmployee():

    User = Model.get('res.user')
    Employe = Model.get('company.employee')
    users = csv.reader(open('usuarios.csv', 'r'))
    header=True
    inicio=1
    user = User()
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        users.next()

    for index,row in enumerate(users):
        usuario = row[0]
        empleado = row[0]
        empresa = row[3]
        
        users = User.find([('name','=', usuario)])
        employees = Employe.find([('party.name','=',empleado)])
        
        if len(Employe.find([('party.name', '=', empleado)])) == 1:
            employee, = Employe.find([('party.name','=',empleado)])
        if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
            company, = Company.find([('party.vat_number','=',empresa)])
            
        for user in users:
            user.employees.append(employees[0])
            user.employee = employee
        user.save()

LoadUserEmployee()

def LoadCategoryG():
    Account = Model.get('account.account')
    Tax = Model.get('account.tax')
    category = Category()
    category.name = "CATEGORIA GENERAL"
    category.taxes_parent = False
    category.account_parent = False
    category.iva_tarifa = "2"
    
    if len(Account.find([('name', '=', 'VENTA DE BIENES')])) == 1:
        revenue, = Account.find([('name', '=', 'VENTA DE BIENES')])
        category.account_revenue = revenue
    
    if len(Account.find([('name', '=', 'COSTO DE VENTAS')])) == 1:
        expense, = Account.find([('name', '=', 'COSTO DE VENTAS')])
        category.account_expense = expense
    
    category.save()
    categories = Category.find([('name','=', 'CATEGORIA GENERAL')])
    taxes_c = Tax.find([('description','=', 'IVA VENTAS LOCALES (EXCLUYE ACTIVOS FIJOS) GRAVADAS TARIFA 12%')])
    taxes_s = Tax.find([('description','=', 'IVA ADQUISICIONES Y PAGOS (EXCLUYE ACTIVOS FIJOS) GRAVADOS TARIFA 12% (CON DERECHO A CRÉDITO TRIBUTARIO)')])
    
    for category in categories:
        category.customer_taxes.append(taxes_c[0])
        category.supplier_taxes.append(taxes_s[0])
    
    category.save()
    print "Created category ", category
    
LoadCategoryG()
    
def LoadCategory():
    Account = Model.get('account.account')
    Tax = Model.get('account.tax')
    header=True
    inicio=1
    categories_csv = csv.reader(open('sub_categorias.csv', 'r'))
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        categories_csv.next()

    for index,row in enumerate(categories_csv):
        category = Category()
        category.name = row[0]
        taxes_parent = row[2]
        account_parent = row[3]
        iva_parent = row[4]
        categoria = row[1]
        tarifa = row[5]
        category.account_parent = True
        
        if len(Category.find([('name', '=', categoria)])) == 1:
            cat, = Category.find([('name', '=', categoria)])
            category.parent = cat
        category.save()
        
        if taxes_parent == 'TRUE':
            category.taxes_parent = True
        else:
            category.taxes_parent = False
            categories = Category.find([('name','=', 'PAPEL BOND')])
            taxes_c = Tax.find([('description','=', 'IVA VENTAS LOCALES (EXCLUYE ACTIVOS FIJOS) GRAVADAS TARIFA 0% QUE DAN DERECHO A CREDITO TRIBUTARIO')])
            taxes_s = Tax.find([('description','=', 'IVA ADQUISICIONES Y PAGOS (INCLUYE ACTIVOS FIJOS) GRAVADOS TARIFA 0%')])
            for category in categories:
                category.customer_taxes.append(taxes_c[0])
                category.supplier_taxes.append(taxes_s[0])

        if iva_parent == 'TRUE':
            category.iva_parent = True
        else:
            category.iva_parent = False
            if tarifa == 0:
                category.iva_tarifa='0'
            if tarifa == 12:
                category.iva_tarifa='2'
        
        category.save()
        print "Created category", category
LoadCategory()

def LoadProduct ():

    products = csv.reader(open('productos.csv', 'r'))
    header=True
    inicio=1
    
    Product = Model.get('product.product')
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        pt = ProductTemplate()
        product = Product()
        #Lprovedor = row[2]
        pt.name = row[1]
        nombreproducto=row[1]
        Codigo=row[0]
        tipo = row[5]
        Categoria = row[6]
        UnidadDefault=unit
        UnidadCompra=unit
        UnidadVenta=unit
        Pcosto= row[3]
        Lcosto = row[4]
        comprable= '1'
        vendible= '1'
        cuentaporcategoria = '1'
        Descripcion=''
        pt.iva_category = True
        costo = float(Pcosto.replace(',', '.')) #Me Convierte la , en . como separador decimal
        venta = float(Lcosto.replace(',', '.')) 
        pt.cost_price = Decimal(costo).quantize(Decimal('.001')) #Redondeo
        pt.list_price = Decimal(venta).quantize(Decimal('.001')) #Redondeo
        if len(Category.find([('name', '=', Categoria)])) == 1:
            category, = Category.find([('name', '=', Categoria)])
            pt.category = category

     	pt.default_uom = unit

        if tipo != '':
            if tipo == 'Articulo':
                 pt.type = 'goods'
            if tipo == 'Servicios':
                 pt.type = 'service'

        if comprable == '1':
            if comprable == '1':
                pt.purchasable = True
	    else:
	        pt.purchasable = False
	        
	    if vendible == '1':
	        pt.salable = True
	    else:
	        pt.salable = False

        if (comprable=='0' and vendible=='0' and cuentaporcategoria=='0'):
            pt.account_category = False
        else:
            pt.account_category = True

        pt.taxes_category = True

        pt.save()
        
        if len(product.find([('name', '=',nombreproducto)])) == 1:
	        pd, = product.find([('name', '=',nombreproducto)])
	        pd.description = Descripcion
	        pd.code=Codigo
       
        pd.save()
        print "Created product ", pd
LoadProduct()

def LoadLocation():

    Locations = Model.get('stock.location')
    locations = csv.reader(open('bodegas.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        locations.next()

    for index,row in enumerate(locations):
        location = Locations()
        
        name = row[0]
        code_new = row[1]
        code = row [2]
        
        if code:
            locations = Locations.find([('code','=',code)])
            for location in locations:
                location.code = code_new
                location.name = name
        else:
            locations = Locations.find([('type','=','lost_found')])
            for location in locations:
                location.code = code_new
                location.name = name
                
        location.save()
        print "Modified location ", location
LoadLocation()

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

def Term():
    terms = csv.reader(open('terminos.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        terms.next()

    for index,row in enumerate(terms):
        Term = Model.get('account.invoice.payment_term')
        term = Term(name=row[0])
        name = row[0]
        
        if name == 'AL CONTADO':
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 0
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 1
            term.save()
            print "Created pay term ", term
            
        elif name == 'PAGO A 30 DIAS':
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 30
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 1
            term.save()
            print "Created pay term ", term
            
        elif name == 'PAGO A 45 DIAS':
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 45
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 1
            term.save()
            print "Created pay term ", term
            
        elif name == '50% HOY - 50% EN 30 DIAS':
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 0
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(50.00)
            term_line.sequence = 1
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 30
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 2
            term.save()
            print "Created pay term ", term
            
        elif name == '20% HOY - 25% EN 15 DIAS - 25% EN 30 DIAS - 30% EN 40 DIAS': 
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 0
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(20.00)
            term_line.sequence = 1
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 15
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(25.00)
            term_line.sequence = 2
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 30
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(25.00)
            term_line.sequence = 3
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 40
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 4
            term.save()
            print "Created pay term ", term
Term()

def InitUser ():
    Module = Model.get('ir.module.module')
    #party
    (res,) = Module.find([('name', '=', 'res')])
    Module.install([res.id], config.context)
    Wizard('ir.module.module.install_upgrade').execute('upgrade')
    
    (ir,) = Module.find([('name', '=', 'ir')])
    Module.install([ir.id], config.context)
    Wizard('ir.module.module.install_upgrade').execute('upgrade')
InitUser()


def LoadJournal():
    Account = Model.get('account.account')
    journal = Journal()
    journal.name = 'ESTADO DE CUENTA MATRIZ'
    journal.type = 'statement'
    journal.code = 'EDCM'
    if len(Sequence.find([('code', '=', 'account.journal')])) == 1:
        sequence, = (Sequence.find([('code', '=', 'account.journal')]))
        journal.sequence = sequence
        
    if len(Account.find([('name', '=','CUENTAS POR PAGAR PROVEEDORES')]))==1:
        debit, = Account.find([('name', '=','CUENTAS POR PAGAR PROVEEDORES')])
        journal.debit_account = debit
    
    if len(Account.find([('name', '=','DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')]))==1:
        credit, = Account.find([('name', '=','DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')])
        journal.credit_account = credit
        
    journal.save()
    print "Created journal ", journal
LoadJournal()
        
def LoadJournalStatement():
    journals_s = csv.reader(open('libro_estados.csv', 'r'))
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        journals_s.next()

    for index,row in enumerate(journals_s):
        journal_statement = JournalStatement()
        journal_statement.name = row[0]
        journal_statement.validation = 'balance'
        
        if len(Journal.find([('name', '=', 'ESTADO DE CUENTA MATRIZ')])) == 1:
            journal, = Journal.find([('name', '=', 'ESTADO DE CUENTA MATRIZ')])
            journal_statement.journal = journal
        journal_statement.save()
        print "Created journal statement ", journal_statement
LoadJournalStatement()

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

def LoadDevice():
    journals = csv.reader(open('tpv.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        journals.next()
        
    for index,row in enumerate(journals):
        device = Device()
        device.name = row[0]
        terminal = row[1]
        if len(Shop.find([('name', '=', terminal)])) == 1:
            shop, = Shop.find([('name', '=', terminal)])
            device.shop = shop
        device.save()
        print "Created device ", device
LoadDevice()

def LoadDeviceJ():
    journals = csv.reader(open('libro_estados.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        journals.next()
        
    for index,row in enumerate(journals):
        terminal = row[1]
        journal = row[0]
        devices = Device.find([('name','=',terminal)])
        journals = JournalStatement.find([('name','=',journal)])
        
        for device in devices:
            device.journals.append(journals[0])
            device.save()
        
        print "Modified device ", device
        
LoadDeviceJ()

def LoadShop_User():
    shop = Shop()
    shops = Shop.find([('name', '=', 'TIENDA MATRIZ')])
    usuarios = ('VENDEDOR 1', 'VENDEDOR 2', 'CONTADOR')
    for usuario in usuarios:
        users = User.find([('name', '=',  usuario)])
        for shop in shops:
            shop.users.append(users[0])
            shop.save()   
            print "Modified ", shop
LoadShop_User()          


def LoadShop_User():
    shop = Shop()
    shop, = Shop.find([('name', '=', 'TIENDA MATRIZ')])
    device, = Device.find([('name', '=', 'TPV1')])
    device2, = Device.find([('name', '=', 'TPV2')])
    usuarios = ('VENDEDOR 1', 'VENDEDOR 2', 'CONTADOR')
    
    for usuario in usuarios:
        user = User.find([('name', '=',  usuario)])
        user[0].shop = shop
        if usuario == 'VENDEDOR 2':
            user[0].sale_device = device2
        else:
            user[0].sale_device = device
        user[0].save()
        print "Modified ", user[0]
LoadShop_User()  


def LoadSequence():
    Sequence = Model.get('ir.sequence')
    sequence = Sequence()
    sequence.name = 'AC 2016'
    sequence.code = 'account.move'
    sequence.padding = 0
    sequence.prefix = 'AC-2016-'
    sequence.type = 'incremental'
    sequence.active = True
    sequence.save()
    print "Created sequence ", sequence
LoadSequence()

def LoadSequenceStrict():
    SequenceStrict = Model.get('ir.sequence.strict')
    header=True
    inicio=1
    secuencia_comprobantes = csv.reader(open('secuencia_comprobantes.csv', 'r'))
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        secuencia_comprobantes.next()
        
    for index,row in enumerate(secuencia_comprobantes):
        sequence_s = SequenceStrict()
        padding = int (row[2])
        sequence_s.name = row[0]
        sequence_s.code = 'account.invoice'
        sequence_s.prefix = row[1]
        sequence_s.padding = padding
        sequence_s.type = 'incremental'
        sequence_s.active = True
        sequence_s.save()
        print "Created sequence strict ", sequence_s
LoadSequenceStrict()

def LoadFiscalYear():
    fiscal = Fiscal()
    today = datetime.today()
    name = 'AÑO FISCAL ' + str(today.year)
    fiscal.name = name
    fiscal.start_date = today.replace(month=1, day=1)
    fiscal.end_date = today.replace(month=12, day=31)
    
    if len(Sequence.find([('name', '=', 'AC 2016')])) == 1:
        post_move_sequence,   = Sequence.find([('name', '=', 'AC 2016')])
        fiscal.post_move_sequence  = post_move_sequence 
    
    if len(SequenceStrict.find([('name', '=', 'FC 2016 - TPV1')])) == 1:
        out_invoice_sequence,  = SequenceStrict.find([('name', '=', 'FC 2016 - TPV1')])
        fiscal.out_invoice_sequence = out_invoice_sequence 
        
    if len(SequenceStrict.find([('name', '=', 'NCP 2016')])) == 1:
        in_credit_note_sequence, = SequenceStrict.find([('name', '=', 'NCP 2016')])
        fiscal.in_credit_note_sequence = in_credit_note_sequence
        
    if len(SequenceStrict.find([('name', '=', 'FP 2016')])) == 1:
        in_invoice_sequence, = SequenceStrict.find([('name', '=', 'FP 2016')])
        fiscal.in_invoice_sequence = in_invoice_sequence
        
    if len(SequenceStrict.find([('name', '=', 'NCC 2016 - TPV1')])) == 1:
        out_credit_note_sequence,  = SequenceStrict.find([('name', '=', 'NCC 2016 - TPV1')])
        fiscal.out_credit_note_sequence = out_credit_note_sequence 
    
    journal_sequence = fiscal.journal_sequences.new()
    if len(Journal.find([('code', '=', 'REV')])) == 1:
        journal, = Journal.find([('code', '=', 'REV')])
        journal_sequence.journal = journal
    if len(SequenceStrict.find([('name', '=', 'FC 2016 - TPV2')])) == 1:
        out_invoice_sequence, = SequenceStrict.find([('name', '=', 'FC 2016 - TPV2')])
        journal_sequence.out_invoice_sequence = out_invoice_sequence 
    if len(SequenceStrict.find([('name', '=', 'NCC 2016 - TPV2')])) == 1:
        out_credit_note_sequence, = SequenceStrict.find([('name', '=', 'NCC 2016 - TPV2')])
        journal_sequence.out_credit_note_sequence = out_credit_note_sequence
    if len(Device.find([('name', '=', 'TPV2')])) == 1:
        user, = Device.find([('name', '=', 'TPV2')])
        journal_sequence.users= user
    
    fiscal.save()
    print "Created fiscal year ", fiscal
LoadFiscalYear()

def LoadGroupA():
    
    group = Group()
    group.name = "Nodux - Administración"
    model_access= group.model_access.new()
    
    if len(Ir.find([('model', '=', 'ir.sequence.strict')])) == 1:
        modelo, = Ir.find([('model', '=', 'ir.sequence.strict')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
    
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'ir.sequence.type')])) == 1:
        modelo, = Ir.find([('model', '=', 'ir.sequence.type')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'ir.sequence')])) == 1:
        modelo, = Ir.find([('model', '=', 'ir.sequence')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
    
    group.save()
    print "Created group  ", group
LoadGroupA()
   
def LoadGroupV():
    Menu = Model.get('ir.ui.menu')
    group = Group()
    group.name = "Nodux - Ventas"
    model_access= group.model_access.new()
    
    if len(Ir.find([('model', '=', 'sale.sale')])) == 1:
        modelo, = Ir.find([('model', '=', 'sale.sale')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
    
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'sale.line')])) == 1:
        modelo, = Ir.find([('model', '=', 'sale.line')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.invoice')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.invoice')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.invoice.line')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.invoice.line')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'stock.move')])) == 1:
        modelo, = Ir.find([('model', '=', 'stock.move')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'stock.shipment.out')])) == 1:
        modelo, = Ir.find([('model', '=', 'stock.shipment.out')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'stock.shipment.out.return')])) == 1:
        modelo, = Ir.find([('model', '=', 'stock.shipment.out.return')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.statement')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.statement')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.statement.line')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.statement.line')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = False
    
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price'), ('module', '=', 'product'), ('model.model', '=', 'product.template')])) == 1:
        field, = Field.find([('name', '=', 'cost_price'), ('module', '=', 'product'),  ('model.model', '=', 'product.template')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price_uom'), ('module', '=', 'product'),('model.model', '=', 'product.product')])) == 1:
        field, = Field.find([('name', '=', 'cost_price_uom'), ('module', '=', 'product'),  ('model.model', '=', 'product.product')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price_method'), ('module', '=', 'product'), ('model.model', '=', 'product.template')])) == 1:
        field, =(Field.find([('name', '=', 'cost_price_method'), ('module', '=', 'product'), ('model.model', '=', 'product.template')])) 
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=','stock.location')])) == 1:
        field, = Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=','stock.location')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.template' )])) == 1:
        field, = (Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.template' )]))
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.product')])) == 1:
        field, = Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.product')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
      
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price'), ('module', '=', 'stock'), ('model.model', '=', 'stock.move')])) == 1:
        field, = Field.find([('name', '=', 'cost_price'), ('module', '=', 'stock'), ('model.model', '=', 'stock.move')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
    
    group.save()
    groups = Group.find([('name','=', 'Nodux - Ventas')])
    menus = Menu.find([('sequence','=', 5), ('parent', '=', None)])
    menus_v = Menu.find([('sequence','=', 10), ('parent.sequence', '=', 5)])
    for group in groups:
        group.menu_access.append(menus[0])
        group.menu_access.append(menus_v[0])
    group.save()
    print "Created group  ", group
LoadGroupV()

def LoadVentasNodux():
    group = Group()
    groups = Group.find([('name','=', 'Nodux - Ventas')])
    vendedores = ('VENDEDOR 1', 'VENDEDOR 2')
    for vendedor in vendedores:
        users = User.find([('name', '=',  vendedor)])
        for group in groups:
            group.users.append(users[0])
            group.save()   
LoadVentasNodux()

def LoadAdministracion():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Nodux - Administración')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracion()

def LoadFinanciero():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Financiero')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
    
LoadFinanciero()
       
def LoadAdministracionContabilidad():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administración de Contabilidad')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionContabilidad()
   
def LoadAdministracionBancos():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administración de Bancos')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionBancos()
    
def LoadAdministracionProductos():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administración de Productos')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionProductos()

def LoadAdministracionStock():
    groups = Group.find([('name','=', 'Administración de Stock')])
    usuarios = ('CONTADOR', 'BODEGUERO')
    for usuario in usuarios:
        users = User.find([('name','=', usuario)])
        for group in groups:
            group.users.append(users[0])
            group.save()
LoadAdministracionStock()

def LoadStock():
    usuarios = ('CONTADOR', 'BODEGUERO')
    groups = Group.find([('name','=', 'Stock')])
    for usuario in usuarios:
        users = User.find([('name','=', usuario)])
        for group in groups:
            group.users.append(users[0])
            group.save()
LoadStock()

def LoadAsignacionStock():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Asignación Forzada de Stock')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAsignacionStock()

def LoadVentas():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Ventas')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadVentas()

def LoadAdministracionVentas():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administrador de Ventas')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionVentas()

def LoadAdministracionCompras():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administrador de Compras')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionCompras()
    
def LoadCompras():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Compras')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadCompras()

def LoadSolicitudCompras():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Solicitud de Compras')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadSolicitudCompras()


