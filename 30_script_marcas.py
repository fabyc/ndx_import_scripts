import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

marcas = csv.reader(open('marcas.csv', 'r'))

Brand = Model.get('product.brand')


def LoadBrand():
    inicio=1
    if (inicio == 1): inicio = 2

    for i in range(inicio - 1):
        marcas.next()

    for index,row in enumerate(marcas):
        brand = Brand()
        brand.name = row[0]
        brand.save()
        print "Creada marca ", brand.name
LoadBrand()
