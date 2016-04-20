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

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Product = Model.get('product.product')
ProductTemplate = Model.get('product.template')
Category = Model.get('product.category')
ProductUom = Model.get('product.uom')
ProductSupplier = Model.get('purchase.product_supplier')
unit, = ProductUom.find([('symbol', '=', 'u')])

def LoadPrecio ():

    products = csv.reader(open('productos.csv', 'r'))
    header=True
    inicio=1
    
    Product = Model.get('product.product')
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        
        if len(ProductTemplate.find([('name', '=', row[1])])) == 1:
            pt, = ProductTemplate.find([('name', '=',row[1])])
            Pcosto= row[3]
            Lcosto = row[4]
            costo = float(Pcosto.replace(',', '.')) #Me Convierte la , en . como separador decimal
            venta = float(Lcosto.replace(',', '.')) 
            pt.cost_price = Decimal(costo).quantize(Decimal('.001')) #Redondeo
            pt.list_price = Decimal(venta).quantize(Decimal('.001')) #Redondeo
            pt.save()                    
            print "Modified product", pt, pt.name
LoadPrecio()
