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

modules = csv.reader(open('modules_pymes.csv', 'r'))


Sequence = Model.get('ir.sequence')
JournalSequence = Model.get('account.journal.invoice.sequence')
Journal =  Model.get('account.journal') 
SequenceStrict = Model.get('ir.sequence.strict')
Device = Model.get('sale.device')
Fiscal = Model.get('account.fiscalyear')

def LoadSequence():
    Sequence = Model.get('ir.sequence')
    sequence = Sequence()
    sequence.name = 'AC 2016'
    sequence.code = 'account.move'
    sequence.padding = 0
    sequence.prefix = 'AC-2016-'
    sequence.type = 'incremental'
    sequence.active = True
    sequence.save()
    print "Created sequence ", sequence
LoadSequence()

