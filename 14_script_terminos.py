import csv
from proteus import config, Model, Wizard
from decimal import Decimal

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

def Term():
    terms = csv.reader(open('terminos.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        terms.next()

    for index,row in enumerate(terms):
        Term = Model.get('account.invoice.payment_term')
        term = Term(name=row[0])
        name = row[0]
        
        if name == 'AL CONTADO':
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 0
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 1
            term.save()
            print "Created pay term ", term
            
        elif name == 'PAGO A 30 DIAS':
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 30
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 1
            term.save()
            print "Created pay term ", term
            
        elif name == 'PAGO A 45 DIAS':
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 45
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 1
            term.save()
            print "Created pay term ", term
            
        elif name == '50% HOY - 50% EN 30 DIAS':
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 0
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(50.00)
            term_line.sequence = 1
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 30
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 2
            term.save()
            print "Created pay term ", term
            
        elif name == '20% HOY - 25% EN 15 DIAS - 25% EN 30 DIAS - 30% EN 40 DIAS': 
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 0
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(20.00)
            term_line.sequence = 1
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 15
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(25.00)
            term_line.sequence = 2
            term_line = term.lines.new()
            term_line.type = 'percent_on_total' 
            term_line.days = 30
            term_line.months = 0 
            term_line.weeks = 0
            term_line.percentage = Decimal(25.00)
            term_line.sequence = 3
            term_line = term.lines.new()
            term_line.type = 'remainder' 
            term_line.days = 40
            term_line.months = 0 
            term_line.weeks = 0
            term_line.sequence = 4
            term.save()
            print "Created pay term ", term
Term()
