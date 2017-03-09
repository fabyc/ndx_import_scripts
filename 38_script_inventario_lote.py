import csv
from proteus import config, Model, Wizard
from datetime import datetime, timedelta
import pytz

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Product = Model.get('product.product')
Template = Model.get('product.template')
ProductUom = Model.get('product.uom')
ProductSupplier = Model.get('purchase.product_supplier')
unit, = ProductUom.find([('symbol', '=', 'u')])
Inventory = Model.get('stock.inventory')
Location = Model.get('stock.location')
InventoryLines = Model.get('stock.inventory.line')
Lot = Model.get('stock.lot')

def LoadLot():   
    products = csv.reader(open('productos-tecnycompsa.csv', 'r'))
    inicio = 2
    for i in range(inicio - 1):
        products.next()
    cont = 1
    for index,row in enumerate(products):
        lot = Lot()
        if row[1]:
            (template,) = Template.find([('name', '=', row[2])])
            (product,) = Product.find([('template', '=', template.id)])
            lot.product = product
            lot.number = row[1]
            lot.save()
            print "Creado ",lot.number
LoadLot()

def LoadInventory():
    timezone = pytz.timezone('America/Guayaquil')
    dt = datetime.today()
    fecha = datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone)

    inventory = Inventory()
    location = Location.find([('type', '=', 'storage'), ('id', '=', 3)])
    inventory.location = location[0]
    inventory.date = fecha
    lost_found, = Location.find([('type', '=', 'lost_found')])
    inventory.lost_found = lost_found
    products = csv.reader(open('productos-tecnycompsa.csv', 'r'))
    inicio = 2
    for i in range(inicio - 1):
        products.next()
    for index,row in enumerate(products):
        if row[1]:
            code = row[0]
            cantidad = int(row[3])
            if cantidad < 1:
                cantidad = int(0)
            (template,) = Template.find([('name', '=', row[2])])
            producto = Product.find([('template', '=', template.id)])
            #producto = Product.find([('code', '=', code)])
            (lot,) = Lot.find([('number', '=', row[1])])
            if producto:
            	if producto[0].template.type == "service":
                	pass
            	else:
                	inventory.lines.new(product=producto[0], quantity=cantidad, lot=lot)
        else:
            code = row[0]
            cantidad = int(row[3])
            if cantidad < 1:
                cantidad = int(0)
            (template,) = Template.find([('name', '=', row[2])])
            producto = Product.find([('template', '=', template.id)])
            if producto:
            	if producto[0].template.type == "service":
                	pass
            	else:
                	inventory.lines.new(product=producto[0], quantity=cantidad)
        print "Agregado producto", producto[0].template.name
    inventory.save()
    print "Creado inventario", inventory
    Inventory.confirm([inventory.id], config.context)
LoadInventory()
