import csv
from proteus import config, Model, Wizard
from datetime import datetime, timedelta

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
    today = datetime.today()
    inventory = Inventory()
    location = Location.find([('type', '=', 'storage')])
    inventory.location = location[0]
    inventory.date = today
    lost_found, = Location.find([('type', '=', 'lost_found')])
    inventory.lost_found = lost_found
    products = csv.reader(open('productos.csv', 'r'))
    inicio = 2 
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        code = row[0]
        cantidad = float(row[2])
        producto = Product.find([('code', '=', code)])
        print "Agregare ", cantidad, producto[0]
        
        inventory.lines.new(product=producto[0], quantity=cantidad)
        
        
    inventory.save()
    print "Agregado inventario ", inventory
LoadInventory()
