import csv
from proteus import config, Model, Wizard
from decimal import Decimal

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Device = Model.get('sale.device') 
Journal = Model.get('account.journal')
JournalStatement = Model.get('account.statement.journal')
Shop = Model.get('sale.shop')
Sequence = Model.get('ir.sequence')
User= Model.get('res.user')

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
