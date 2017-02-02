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

Advanced = Model.get('sale.advanced')
Party = Model.get('party.party')

def LoadAdvanced ():

    anticipos = csv.reader(open('anticipos.csv', 'r'))
    header = True
    inicio = 1

    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        anticipos.next()

    for index,row in enumerate(anticipos):
        advanced = Advanced()
        if len(Party.find([('name', '=', row[0])])) >= 1:
            party = Party.find([('name', '=', row[0])])
            advanced.party = party[0]
            advanced.amount = Decimal(row[1])
            advanced.save()
            Advanced.post([advanced.id], config.context)
            print "Creado anticipo ", advanced
LoadAdvanced()
