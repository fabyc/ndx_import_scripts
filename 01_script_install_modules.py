import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)
modules = csv.reader(open('modules_pymes.csv', 'r'))

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
        
InitDatabase ()