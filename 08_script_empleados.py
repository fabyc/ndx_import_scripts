import csv
from proteus import config, Model, Wizard

empleados = csv.reader(open('empleados.csv', 'r'))

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Company = Model.get('company.company')
Party = Model.get('party.party')
Lang = Model.get('ir.lang')


def LoadEmployes ():

    Employe = Model.get('company.employee')
    employe = Employe()
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        empleados.next()

    for index,row in enumerate(empleados):
        employe = Employe()
        tercero = row[0]
        empresa = row[2]
        
        if len(Party.find([('vat_number', '=', tercero)])) == 1:
            party, = Party.find([('vat_number', '=', tercero)])
            employe.party = party
            
        if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
            company, = Company.find([('party.vat_number', '=', empresa)])
            employe.company = company
        employe.save()
        print "Created employee ", employe
LoadEmployes()

