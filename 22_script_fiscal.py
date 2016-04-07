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

def LoadFiscalYear():
    fiscal = Fiscal()
    today = datetime.today()
    name = 'AÑO FISCAL ' + str(today.year)
    fiscal.name = name
    fiscal.start_date = today.replace(month=1, day=1)
    fiscal.end_date = today.replace(month=12, day=31)
    
    if len(Sequence.find([('name', '=', 'AC 2016')])) == 1:
        post_move_sequence,   = Sequence.find([('name', '=', 'AC 2016')])
        fiscal.post_move_sequence  = post_move_sequence 
    
    if len(SequenceStrict.find([('name', '=', 'FC 2016 - TPV1')])) == 1:
        out_invoice_sequence,  = SequenceStrict.find([('name', '=', 'FC 2016 - TPV1')])
        fiscal.out_invoice_sequence = out_invoice_sequence 
        
    if len(SequenceStrict.find([('name', '=', 'NCP 2016')])) == 1:
        in_credit_note_sequence, = SequenceStrict.find([('name', '=', 'NCP 2016')])
        fiscal.in_credit_note_sequence = in_credit_note_sequence
        
    if len(SequenceStrict.find([('name', '=', 'FP 2016')])) == 1:
        in_invoice_sequence, = SequenceStrict.find([('name', '=', 'FP 2016')])
        fiscal.in_invoice_sequence = in_invoice_sequence
        
    if len(SequenceStrict.find([('name', '=', 'NCC 2016 - TPV1')])) == 1:
        out_credit_note_sequence,  = SequenceStrict.find([('name', '=', 'NCC 2016 - TPV1')])
        fiscal.out_credit_note_sequence = out_credit_note_sequence 
    
    journal_sequence = fiscal.journal_sequences.new()
    if len(Journal.find([('code', '=', 'REV')])) == 1:
        journal, = Journal.find([('code', '=', 'REV')])
        journal_sequence.journal = journal
    if len(SequenceStrict.find([('name', '=', 'FC 2016 - TPV2')])) == 1:
        out_invoice_sequence, = SequenceStrict.find([('name', '=', 'FC 2016 - TPV2')])
        journal_sequence.out_invoice_sequence = out_invoice_sequence 
    if len(SequenceStrict.find([('name', '=', 'NCC 2016 - TPV2')])) == 1:
        out_credit_note_sequence, = SequenceStrict.find([('name', '=', 'NCC 2016 - TPV2')])
        journal_sequence.out_credit_note_sequence = out_credit_note_sequence
    if len(Device.find([('name', '=', 'TPV2')])) == 1:
        user, = Device.find([('name', '=', 'TPV2')])
        journal_sequence.users= user
    
    fiscal.save()
    print "Created fiscal year ", fiscal
LoadFiscalYear()
