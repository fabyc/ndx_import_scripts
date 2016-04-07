import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

empresas = csv.reader(open('empresas.csv', 'r'))

Party = Model.get('party.party')
Lang = Model.get('ir.lang')
Currency = Model.get('currency.currency')
Company = Model.get('company.company')

def LoadCompanies ():

    Company = Model.get('company.company')
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        empresas.next()

    for index,row in enumerate(empresas):
        company = Company()
        cedula = row[0]

        if len(Party.find([('vat_number', '=', cedula)])) == 1:
            party, = Party.find([('vat_number', '=', cedula)])
            company.party = party
        (currency,) = Currency.find([('code', '=', 'USD')])   
        company.timezone = 'America/Guayaquil'
        company.currency = currency
        
        company.save()
        print "Created company ", company
LoadCompanies()

def LoadUserC():
    inicio=1
    User = Model.get('res.user')
    Company = Model.get('company.company')
    empresa = '1191758435001'

    user = User()
    if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
        company, = Company.find([('party.vat_number', '=', empresa)])
    users = User.find([('login','=', 'admin')])
    for user in users:
        user.main_company = company
    user.save()
