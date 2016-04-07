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


def LoadSequenceStrict():
    SequenceStrict = Model.get('ir.sequence.strict')
    header=True
    inicio=1
    secuencia_comprobantes = csv.reader(open('secuencia_comprobantes.csv', 'r'))
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        secuencia_comprobantes.next()
        
    for index,row in enumerate(secuencia_comprobantes):
        sequence_s = SequenceStrict()
        padding = int (row[2])
        sequence_s.name = row[0]
        sequence_s.code = 'account.invoice'
        sequence_s.prefix = row[1]
        sequence_s.padding = padding
        sequence_s.type = 'incremental'
        sequence_s.active = True
        sequence_s.save()
        print "Created sequence strict ", sequence_s
LoadSequenceStrict()

