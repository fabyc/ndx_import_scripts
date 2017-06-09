import csv
from proteus import config, Model, Wizard
from datetime import datetime, timedelta
import pytz
from decimal import Decimal

database = 'tecnycompsa'
user = 'admin'
password = 'admNdX58753'
config_file = '/home/noduxdev/.noduxenvs/nodux34devpymes/etc/nodux34pymes-server.conf'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Template = Model.get('product.template')

def LoadProductUpdatePrices():
    templates = Template.find([('id', '>', 0)])

    for template in templates:
        print "Actualizado precio producto ", template.name
        rate = 0
        use_new_formula = False
        percentage = 0
        precio_final = Decimal(0.0)
        new_list_price = Decimal(0.0)

        if template.taxes_category == True:
            if template.category.taxes_parent == True:
                for tax in template.category.parent.customer_taxes:
                    rate = tax.rate
            else:
                for tax in template.category.customer_taxes:
                    rate = tax.rate
        template.cost_price_with_tax = Decimal(str(round((template.cost_price * (1+rate)), 4)))

        for price_list in template.listas_precios:
            price_list.fijo_con_iva = Decimal(str(round((price_list.fijo *(1+rate)), 4)))
            price_list.save()
        template.list_price_with_tax = Decimal(str(round((template.list_price*(1+rate)), 4)))
        template.save()

LoadProductUpdatePrices()
