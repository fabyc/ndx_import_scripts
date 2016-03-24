import csv
from proteus import config, Model, Wizard
import random
from random import randrange
import os
import binascii
from datetime import datetime, timedelta
from decimal import Decimal
from decimal import Decimal
import time

#categories = csv.reader(open('categories.csv', 'r'))
config = config.set_trytond(database='toners_catamayo', user='admin', language='es_EC.UTF-8', password='toners_catamayo', config_file='/home/noduxdev/.noduxenvs/nodux34devpymes/etc/nodux34pymes-server.conf')

Category = Model.get('product.category')

def InitDatabase ():
    Module = Model.get('ir.module.module')
    (product,) = Module.find([('name', '=', 'product')])
    Module.install([product.id], config.context)
    Wizard('ir.module.module.install_upgrade').execute('upgrade')

InitDatabase()

def LoadCategory ():
    """
    products = csv.reader(open('productos.csv', 'r'))
    header=True
    inicio=1
    if (inicio == 1): inicio = 2 #para evitar la cabezera del CSV
    for i in range(inicio - 1):
        products.next()
    """
    category = Category()
    
    category.name = "General"
    category.taxes_parent = False
    category.account_parent = False
    category.iva_tarifa = "2"
    category.save()

LoadCategory()

