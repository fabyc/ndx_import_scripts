#! -*- coding: utf8 -*-

import csv
from proteus import config, Model, Wizard
from decimal import Decimal
import datetime

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Sequence = Model.get('ir.sequence')
JournalSequence = Model.get('account.journal.invoice.sequence')
Journal =  Model.get('account.journal') 
SequenceStrict = Model.get('ir.sequence.strict')
Device = Model.get('sale.device')
Fiscal = Model.get('account.fiscalyear')

def LoadJournalStatement():
    journals_s = csv.reader(open('libro_estados.csv', 'r'))
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        journals_s.next()

    for index,row in enumerate(journals_s):
        journal_statement = JournalStatement()
        journal_statement.name = row[0]
        journal_statement.validation = 'balance'
        
        if len(Journal.find([('name', '=', 'ESTADO DE CUENTA MATRIZ')])) == 1:
            journal, = Journal.find([('name', '=', 'ESTADO DE CUENTA MATRIZ')])
            journal_statement.journal = journal
        journal_statement.save()
        print "Created journal statement ", journal_statement
LoadJournalStatement()

