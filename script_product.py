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

parties = csv.reader(open('productos.csv', 'r'))
config = config.set_trytond(database='toners_catamayo', user='admin', language='es_EC.UTF-8', password='toners_catamayo', config_file='/home/noduxdev/.noduxenvs/nodux34devpymes/etc/nodux34pymes-server.conf')

Product = Model.get('product.product')
ProductTemplate = Model.get('product.template')
Category = Model.get('product.category')
ProductUom = Model.get('product.uom')
ProductSupplier = Model.get('purchase.product_supplier')
unit, = ProductUom.find([('symbol', '=', 'u')])

def InitDatabase ():
    Module = Model.get('ir.module.module')
    (product,) = Module.find([('name', '=', 'product')])
    Module.install([product.id], config.context)
    Wizard('ir.module.module.install_upgrade').execute('upgrade')

InitDatabase()

def LoadProduct ():

    products = csv.reader(open('productos.csv', 'r'))
    header=True
    inicio=1
    
    Product = Model.get('product.product')
    if (inicio == 1): inicio = 2 #para evitar la cabezera del CSV
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        PS = ProductSupplier()
        pt = ProductTemplate()
        product = Product()
        #Lprovedor = row[2]
        pt.name = row[1]
        nombreproducto=row[1]
        Codigo=row[0]
        tipo = row[9]
        Categoria = 'General'
        UnidadDefault=unit
        UnidadCompra=unit
        UnidadVenta=unit
        Pcosto= '1,0'
        Lcosto = '1,0'
        comprable= '1'
        vendible= '1'
        cuentaporcategoria = '1'
        Descripcion=''
        pt.iva_category = True
        costo = float(Pcosto.replace(',', '.')) #Me Convierte la , en . como separador decimal
        venta = float(Lcosto.replace(',', '.')) 
        
        pt.cost_price = Decimal(costo).quantize(Decimal('.001')) #Redondeo
        pt.list_price = Decimal(venta).quantize(Decimal('.001')) #Redondeo
        if len(Category.find([('name', '=', Categoria)])) == 1:
            category, = Category.find([('name', '=', Categoria)])
            pt.category = category

     	pt.default_uom = unit

        if tipo != '':
            if tipo == 'Articulo':
                 pt.type = 'goods'
            if tipo == 'Servicios':
                 pt.type = 'service'

        if comprable == '1':
            if comprable == '1':
                pt.purchasable = True
	    else:
	        pt.purchasable = False
	        
	    if vendible == '1':
	        pt.salable = True
	    else:
	        pt.salable = False

        if (comprable=='0' and vendible=='0' and cuentaporcategoria=='0'):
            pt.account_category = False
        else:
            pt.account_category = True

        pt.taxes_category = True

        pt.save()
        
        print "Producto ",(product.find([('name', '=',nombreproducto)]))
        if len(product.find([('name', '=',nombreproducto)])) == 1:
	        pd, = product.find([('name', '=',nombreproducto)])
	        pd.description = Descripcion
	        pd.code=Codigo
        pd.save()


LoadProduct()

