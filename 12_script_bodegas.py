import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)
modules = csv.reader(open('modules_pymes.csv', 'r'))

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
