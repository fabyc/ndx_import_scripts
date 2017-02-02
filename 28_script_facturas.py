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

Product = Model.get('product.product')
Template = Model.get('product.template')
Invoice = Model.get('account.invoice')
Party = Model.get('party.party')
Category = Model.get('party.category')
Address = Model.get ('party.address')
Contact = Model.get ('party.contact_mechanism')
Country = Model.get('country.country')
Lang = Model.get('ir.lang')
Linea = Model.get('account.invoice.line')
PaymentTerm = Model.get('account.invoice.payment_term')
PaymentTermLine = Model.get('account.invoice.payment_term.line')

def LoadInvoice ():

    products = csv.reader(open('facturas.csv', 'r'))
    header = True
    inicio = 1

    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        products.next()

    for index,row in enumerate(products):
        invoice = Invoice()
        if len(Party.find([('vat_number', '=', row[1])])) >= 1:
            party, = Party.find([('vat_number', '=', row[1])])
            invoice.party = party
        else:
            tipo = ''
            Correo = "info@toners.ec"
            comercial = ""
            party = Party()
            party.name = row[2]
            party.commercial_name = comercial
            party.type_document = tipo
            party.vat_number = row[1]
            party.active = True
            Calle = 'Loja'
            Ciudad = 'Loja'
            Pais = 'ECUADOR'
            Telefono = row[3]
            party.addresses.pop()
            (coun,) = Country.find([('code', '=', 'EC')])
            address = party.addresses.new(street=Calle,country=coun,city=Ciudad)
            (es,) = Lang.find([('code', '=', 'es_EC')])
            party.lang = es

            if (Correo != ''):
                contactmecanism = party.contact_mechanisms.new(type='email', value=Correo)
            party.save()
            invoice.party = party

        payment, = PaymentTerm.find([('id', '=', 16)])
        def replace_character(cadena):
            reemplazo = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07','Aug':'08',
                'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
            regex = re.compile("(%s)" % "|".join(map(re.escape, reemplazo.keys())))
            nueva_cadena = regex.sub(lambda x: str(reemplazo[x.string[x.start():x.end()]]), cadena)
            return nueva_cadena

        date_str = replace_character(str(row[5]))
        date_str = date_str[:6]+'20'+date_str[6:8]
        formatter_string = "%d-%m-%Y"
        datetime_object = datetime.strptime(date_str, formatter_string)
        fechaEmision = datetime_object.date()

        date_out_str = replace_character(str(row[6]))
        date_out_str = date_out_str[:6]+'20'+date_out_str[6:8]
        datetime_out_object = datetime.strptime(date_out_str, formatter_string)
        fechaVence = datetime_out_object.date()

        dias = fechaVence - fechaEmision
        dias = dias.days

        name = "Pago " + str(dias) + " dias"

        if len(PaymentTerm.find([('name', '=', name)])) >= 1:
            term, = PaymentTerm.find([('name','=', name)])
        else:
            term = PaymentTerm()
            term.name = name
            term.lines.new(type='remainder', days=dias, divisor=Decimal(0.0))
            term.save()

        invoice.payment_term = term
        invoice.reference = row[4]
        #invoice.number = row[4]
        invoice.invoice_date = fechaEmision
        invoice.save()



        if len(Product.find([('code', '=', 'PROMIGRA')])) >= 1:
            product, = Product.find([('code', '=', 'PROMIGRA')])
            linea = Linea()

            precio= row[3]
            precio_venta = float(precio.replace(',', '.'))
            linea.type = 'line'
            linea.product = product
            linea.quantity = 1
            linea.party = invoice.party
            linea.unit_price = Decimal(str(round((precio_venta), 4)))#Redondeo
            linea.invoice = invoice
            linea.save()
            invoice.lines.append(linea)
            invoice.save()

        print "Guardada factura ", invoice
        Invoice.post([invoice.id], config.context)
LoadInvoice()
