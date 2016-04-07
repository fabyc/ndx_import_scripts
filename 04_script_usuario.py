import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)


usuarios = csv.reader(open('usuarios.csv', 'r'))
Lang = Model.get('ir.lang')
Company = Model.get('company.company')
Employe = Model.get('company.employee')

def LoadUser():

    User = Model.get('res.user')
    users = csv.reader(open('usuarios.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        users.next()

    for index,row in enumerate(users):
        user = User()
        user.name = row[0]
        user.login = row[1]
        user.password = row[2]
        (es,) = Lang.find([('code', '=', 'es_EC')])
        user.language = es
        user.save()
        print "Created user ", user
LoadUser()
