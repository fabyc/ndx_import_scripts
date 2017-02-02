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
ProductUom = Model.get('product.uom')
ProductSupplier = Model.get('purchase.product_supplier')
unit, = ProductUom.find([('symbol', '=', 'u')])
Inventory = Model.get('stock.inventory')
Location = Model.get('stock.location')
InventoryLines = Model.get('stock.inventory.line')

def LoadInventory():
    timezone = pytz.timezone('America/Guayaquil')
    dt = datetime.today()
    fecha = datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone)

    inventory = Inventory()
    location = Location.find([('type', '=', 'storage'), ('id', '=', 3)])
    print "Location ", location
    inventory.location = location[0]
    inventory.date = fecha
    lost_found, = Location.find([('type', '=', 'lost_found')])
    inventory.lost_found = lost_found
    products = csv.reader(open('inventario.csv', 'r'))
    inicio = 2
    for i in range(inicio - 1):
        products.next()
    cont = 1
    for index,row in enumerate(products):
    
        code = row[0]
        cantidad = int(row[1])
        if cantidad < 1:
            cantidad = int(0)
        producto = Product.find([('code', '=', code)])
        if producto:
            if producto[0].template.type == "service":
                pass
            else:
                print "Product ",cont,  producto[0].code
                inventory.lines.new(product=producto[0], quantity=cantidad)
        cont = cont +1

    inventory.save()
    print "Creado inventario", inventory
LoadInventory()
