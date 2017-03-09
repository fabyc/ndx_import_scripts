import csv
from proteus import config, Model, Wizard

parties = csv.reader(open('clientes.csv', 'r'))
database = 'prueba_one'
user = 'admin'
password = 'admNdX58753'
config_file = '/home/noduxdev/.noduxenvs/nodux34devpymes/etc/nodux34pymes-server.conf'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Party = Model.get('party.party')
Category = Model.get('party.category')
Address = Model.get ('party.address')
Contact = Model.get ('party.contact_mechanism')
Country = Model.get('country.country')
Lang = Model.get('ir.lang')

def LoadParties ():

    Party = Model.get('party.party')
    parties = csv.reader(open('clientes.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 #para evitar la cabezera del CSV
    for i in range(inicio - 1):
        parties.next()

    for index,row in enumerate(parties):
        party = Party()
        party.vat_number = row[0]
        party.name = row[1]
        party.type_document = ''
        party.active = True
        Calle = row[3]
        Ciudad = row[5]
        Pais = row[4]
        Telefono = row[2]
        Correo = "etqm25@gmail.com"
        party.addresses.pop()
        (coun,) = Country.find([('code', '=', 'EC')])
        address = party.addresses.new(street=Calle, country=coun,city=Ciudad)
        (es,) = Lang.find([('code', '=', 'es_EC')])
        party.lang = es

        if (Telefono != ''):
            contactmecanism = party.contact_mechanisms.new(type='phone', value=Telefono)
        if (Correo != ''):
            contactmecanism = party.contact_mechanisms.new(type='email', value=Correo)
# Skip the header
        party.save()

LoadParties()

