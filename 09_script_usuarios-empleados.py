import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Lang = Model.get('ir.lang')
Comany= Model.get('company.company')

def LoadUserEmployee():

    User = Model.get('res.user')
    Employe = Model.get('company.employee')
    users = csv.reader(open('usuarios.csv', 'r'))
    header=True
    inicio=1
    user = User()
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        users.next()

    for index,row in enumerate(users):
        usuario = row[0]
        empleado = row[0]
        empresa = row[3]
        
        users = User.find([('name','=', usuario)])
        employees = Employe.find([('party.name','=',empleado)])
        
        if len(Employe.find([('party.name', '=', empleado)])) == 1:
            employee, = Employe.find([('party.name','=',empleado)])
        if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
            company, = Company.find([('party.vat_number','=',empresa)])
            
        for user in users:
            user.employees.append(employees[0])
            user.employee = employee
        user.save()

LoadUserEmployee()

