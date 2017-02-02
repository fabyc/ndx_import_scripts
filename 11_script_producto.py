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
ListPrice = Model.get('product.list_by_product')
PriceList =  Model.get('product.price_list')
ProductUom = Model.get('product.uom')
ProductSupplier = Model.get('purchase.product_supplier')
unit, = ProductUom.find([('symbol', '=', 'u')])
Brand = Model.get('product.brand')

def LoadProduct ():

    products = csv.reader(open('productos.csv', 'r'))
    header=True
    inicio=1

    Product = Model.get('product.product')

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
            if len(Category.find([('name', '=', Categoria)])) == 1:
                category, = Category.find([('name', '=', Categoria)])
                pt.category = category

            if len(Brand.find([('name', '=', row[10])])) == 1:
                brand, = Brand.find([('name', '=', row[10])])
                pt.brand = brand

            
         	pt.default_uom = unit

            if tipo != '':
                if tipo == 'Articulo':
                     pt.type = 'goods'
                if tipo == 'Servicios':
                     pt.type = 'service'

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

            if pt.list_price == Decimal(0.0):
                pt.list_price_with_tax = Decimal(0.0)
            else:
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

            priceslist = PriceList.find([('incluir_lista', '=', True)])
            for price in priceslist:
                percentage = 0
                if price.id == 1:
                    for line in price.lines:
                        if line.percentage > 0:
                            percentage = line.percentage/100

                    list_by_product = ListPrice()
                    list_by_product.template = pt
                    list_by_product.lista_precio = price
                    #list_by_product.fijo = Decimal(str(round((pt.cost_price *(1+percentage)), 4)))
                    list_by_product.fijo = Decimal(str(round((pt.list_price), 4)))
                    list_by_product.fijo_con_iva =  Decimal(str(round((list_by_product.fijo * Decimal(1.14)), 4)))
                    list_by_product.precio_venta = True
                    list_by_product.product = pd
                    list_by_product.save()
                    pt.listas_precios.append(list_by_product)


                if price.id == 3:
                    for line in price.lines:
                        if line.percentage > 0:
                            percentage = line.percentage/100


                    list_by_product = ListPrice()
                    list_by_product.template = pt
                    list_by_product.lista_precio = price
                    #list_by_product.fijo = Decimal(str(round((pt.cost_price *(1+percentage)), 4)))
                    list_by_product.fijo = Decimal(str(round(Decimal(row[7]), 4)))
                    list_by_product.fijo_con_iva =  Decimal(str(round((list_by_product.fijo * Decimal(1.14)), 4)))
                    list_by_product.precio_venta = False
                    list_by_product.product = pd
                    list_by_product.save()
                    pt.listas_precios.append(list_by_product)


                if price.id == 7:
                    for line in price.lines:
                        if line.percentage > 0:
                            percentage = line.percentage/100

                    list_by_product = ListPrice()
                    list_by_product.template = pt
                    list_by_product.lista_precio = price
                    #list_by_product.fijo = Decimal(str(round((pt.cost_price *(1+percentage)), 4)))
                    list_by_product.fijo =  Decimal(str(round(Decimal(row[8]), 4)))
                    list_by_product.fijo_con_iva =  Decimal(str(round((list_by_product.fijo * Decimal(1.14)), 4)))
                    list_by_product.precio_venta = False
                    list_by_product.product = pd
                    list_by_product.save()
                    pt.listas_precios.append(list_by_product)

                if price.id == 8:
                    for line in price.lines:
                        if line.percentage > 0:
                            percentage = line.percentage/100

                    list_by_product = ListPrice()
                    list_by_product.template = pt
                    list_by_product.lista_precio = price
                    #list_by_product.fijo = Decimal(str(round((pt.cost_price *(1+percentage)), 4)))
                    list_by_product.fijo =  Decimal(str(round(Decimal(row[9]), 4)))
                    list_by_product.fijo_con_iva = Decimal(str(round((list_by_product.fijo * Decimal(1.14)), 4)))
                    list_by_product.precio_venta = False
                    list_by_product.product = pd
                    list_by_product.save()
                    pt.listas_precios.append(list_by_product)

                pt.save()
            print "Created product ", pt, pt.name
LoadProduct()
