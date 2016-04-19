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

def LoadProduct ():

    products = csv.reader(open('productos.csv', 'r'))
    header=True
    inicio=1
    
    Product = Model.get('product.product')
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        pt = ProductTemplate()
        product = Product()
        
        if len(ProductTemplate.find([('name', '=', row[1])])) >= 1:
            f = open('productos_duplicados.csv', 'a')
            obj = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            obj.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            f.close()
        else:    
            pt.name = row[1]
            nombreproducto=row[1]
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
            
            if len(product.find([('name', '=',nombreproducto)])) == 1:
	            pd, = product.find([('name', '=',nombreproducto)])
	            pd.description = Descripcion
	            pd.code=Codigo
           
            pd.save()
            print "Created product ", pd, pt.name
LoadProduct()
