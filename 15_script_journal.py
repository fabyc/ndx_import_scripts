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

def LoadJournal():
    Account = Model.get('account.account')
    journal = Journal()
    journal.name = 'ESTADO DE CUENTA MATRIZ'
    journal.type = 'statement'
    journal.code = 'EDCM'
    if len(Sequence.find([('code', '=', 'account.journal')])) == 1:
        sequence, = (Sequence.find([('code', '=', 'account.journal')]))
        journal.sequence = sequence
        
    if len(Account.find([('name', '=','CUENTAS POR PAGAR PROVEEDORES')]))==1:
        debit, = Account.find([('name', '=','CUENTAS POR PAGAR PROVEEDORES')])
        journal.debit_account = debit
    
    if len(Account.find([('name', '=','DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')]))==1:
        credit, = Account.find([('name', '=','DOCUMENTOS Y CUENTAS POR COBRAR CLIENTES RELACIONADOS')])
        journal.credit_account = credit
        
    journal.save()
    print "Created journal ", journal
LoadJournal()
