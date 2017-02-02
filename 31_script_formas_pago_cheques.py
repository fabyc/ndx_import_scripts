import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

formas_pago = csv.reader(open('formas_pago.csv', 'r'))

Bank = Model.get('sale.bank')

def LoadBank():
    inicio=1
    if (inicio == 1): inicio = 2

    for i in range(inicio - 1):
        formas_pago.next()

    for index,row in enumerate(formas_pago):
        if int(row[2]) == 0:
            bank = Bank()
            bank.name = row[0]
            bank.save()
            print "Creado forma de pago ", bank.name
LoadBank()
