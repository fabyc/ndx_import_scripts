import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

categories = csv.reader(open('SUB_categorias.csv', 'r'))

Account = model.get('account.account')
Tax = model.get('account.tax')
Category = Model.get('product.category')

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
