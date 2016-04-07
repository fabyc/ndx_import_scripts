import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

def AccountConfiguration():
    print "Load account configuration "
    Account = Model.get('account.account')
    AccountConfiguration = Model.get('account.configuration')
    account_configuration = AccountConfiguration()
    if len(Account.find([('name', '=', 'DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')])) == 1:
        default_account_receivable, = Account.find([('name', '=', 'DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')])
        account_configuration.default_account_receivable = default_account_receivable
    if len(Account.find([('name', '=', 'CUENTAS POR PAGAR PROVEEDORES')])) == 1:
        default_account_payable, = Account.find([('name', '=', 'CUENTAS POR PAGAR PROVEEDORES')])
        account_configuration.default_account_payable = default_account_payable
    
    tax_roundings = account_configuration.tax_roundings.new()
    if len(Company.find([('party.vat_number', '=', company_context)])) == 1:
        company, = Company.find([('party.vat_number','=',company_context)])
        tax_roundings.company = company
    tax_roundings.method = 'document'
    account_configuration.save()
    print "Created account configuration ", account_configuration
AccountConfiguration()
