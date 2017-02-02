#! -*- coding: utf8 -*-
import csv
from proteus import config, Model, Wizard
import random
from random import randrange
import os
import binascii
from datetime import datetime, timedelta
from decimal import Decimal
import time
import re

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Party = Model.get('party.party')
Postdated = Model.get('account.postdated')
Linea = Model.get('account.postdated.line')
Journal = Model.get('account.journal')
Account = Model.get('account.account')

def LoadCheck ():

    cheques = csv.reader(open('cheques_clientes.csv', 'r'))
    header = True
    inicio = 1

    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        cheques.next()

    for index,row in enumerate(cheques):
        postdated = Postdated()
        if len(Party.find([('name', '=', row[0])])) >= 1:

            party, = Party.find([('name', '=', row[0])])
            postdated.party = party
            postdated.post_check_type = "receipt"
            if len(Journal.find([('id', '=', 1)])) >= 1:
                journal, = Journal.find([('id', '=', 1)])
                postdated.journal = journal
            def replace_character(cadena):
                reemplazo = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07','Aug':'08',
                    'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
                regex = re.compile("(%s)" % "|".join(map(re.escape, reemplazo.keys())))
                nueva_cadena = regex.sub(lambda x: str(reemplazo[x.string[x.start():x.end()]]), cadena)
                return nueva_cadena
            date_str = replace_character(str(row[2]))
            date_str = date_str[:6]+'20'+date_str[6:8]
            formatter_string = "%d-%m-%Y"
            datetime_object = datetime.strptime(date_str, formatter_string)
            fechaEmision = datetime_object.date()
            postdated.date = fechaEmision

            date_out_str = replace_character(str(row[3]))
            date_out_str = date_out_str[:6]+'20'+date_out_str[6:8]
            datetime_out_object = datetime.strptime(date_out_str, formatter_string)
            fechaVence = datetime_out_object.date()

            postdated.postdated_type = 'check'
            postdated.save()

            linea = Linea()
            linea.postdated = postdated
            linea.name = row[4]
            if len(Account.find([('id', '=', 10)])) >= 1:
                account, = Account.find([('id', '=', 1)])
                linea.account= account

            monto= row[7]
            monto_final = float(monto.replace(',', '.'))
            linea.amount = Decimal(str(round((monto_final), 2)))
            linea.date = fechaEmision
            linea.date_expire = fechaVence
            linea.save()
            postdated.lines.append(linea)
            postdated.save()

        print "Guardada cheque ", postdated
LoadCheck()
