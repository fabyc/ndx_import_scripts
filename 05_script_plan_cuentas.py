import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

def LoadPlanNIIF():
    AccountC = Model.get('account.create_chart.account')
    Company = Model.get('company.company')
    empresa = '1191758435001'
    Template = Model.get('account.account.template')
    Account = Model.get('account.account')
    account = Account()
    
    account_template = Template.find([('name', '=', 'PLAN DE CUENTAS NIIF ECUADOR'), ('parent','=', None)]) 
    if len(account_template) == 1:
        account_t, = account_template
        account_template = account_t
        
    if len(Company.find([('party.vat_number', '=', empresa)])) == 1:
        company, = Company.find([('party.vat_number', '=', empresa)])
        company = company
    
    create_chart = Wizard('account.create_chart')
    create_chart.execute('account')
    create_chart.form.account_template = account_template
    create_chart.form.company = company
    create_chart.execute('create_account') 
    print "Created chart account"
LoadPlanNIIF()

