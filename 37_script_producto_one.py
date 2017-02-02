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
Template = Model.get('product.template')
Category = Model.get('product.category')
ProductUom = Model.get('product.uom')
unit, = ProductUom.find([('symbol', '=', 'u')])

def LoadProduct ():

    products = csv.reader(open('productos-para-demo.csv', 'r'))
    header=True
    inicio=1

    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        product = Product()
        if len(Template.find([('name', '=', row[1])])) >= 1:
            print "Duplicado ", row[1]
            f = open('productos_duplicados.csv', 'a')
            obj = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            obj.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            f.close()
        else:
            pt = Template()
            pt.name = row[1]

            nombreproducto = row[1]
            Codigo=row[0]
            tipo = row[5]
            Categoria = row[6]
            UnidadDefault=unit
            UnidadCompra=unit
            UnidadVenta=unit
            Pcosto= row[3]
            Lcosto = row[4]
            comprable= '1'
            vendible= '1'
            cuentaporcategoria = '1'
            Descripcion=''
            pt.iva_category = True
            costo = float(Pcosto.replace(',', '.')) #convierte la , en . como separador decimal
            venta = float(Lcosto.replace(',', '.'))
            pt.cost_price = Decimal(str(round((costo), 4)))#Redondeo
            pt.list_price = Decimal(str(round((venta), 4)))#Redondeo
            pt.total = int(row[2])
            if len(Category.find([('name', '=', Categoria)])) == 1:
                category, = Category.find([('name', '=', Categoria)])
                pt.category = category

         	pt.default_uom = unit

            if tipo != '':
                if tipo == 'Articulo':
                     pt.type = 'goods'
                if tipo == 'Servicios':
                     pt.type = 'service'

            pt.taxes_category = True

            if pt.list_price == Decimal(0.0):
                pt.list_price_with_tax = Decimal(0.0)
            else:
                values = pt.list_price_with_tax
                pt.list_price_with_tax = Decimal(str(round((pt.list_price_with_tax), 4)))

            if pt.cost_price == Decimal(0.0):
                pt.cost_price_with_tax = Decimal(0.0)
            else:
                pt.cost_price_with_tax = Decimal(str(round((pt.cost_price_with_tax), 4)))

            pt.save()

            if len(product.find([('name', '=',nombreproducto)])) == 1:
                pd, = product.find([('name', '=',nombreproducto)])
                if len(product.find([('code', '=',Codigo)])) >= 1:
                    f = open('variantes_duplicadas.csv', 'a')
                    obj = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    obj.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                    f.close()
                else:
	                pd.description = Descripcion
	                pd.code=Codigo
                pd.save()
            pt.save()

            print "Created product ", pt, pt.name
LoadProduct()
