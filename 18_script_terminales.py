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
