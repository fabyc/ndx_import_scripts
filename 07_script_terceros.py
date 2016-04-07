import csv
from proteus import config, Model, Wizard

parties = csv.reader(open('terceros.csv', 'r'))

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)
modules = csv.reader(open('modules_pymes.csv', 'r'))


Party = Model.get('party.party')
Category = Model.get('party.category')
Address = Model.get ('party.address')
Contact = Model.get ('party.contact_mechanism')
Country = Model.get('country.country')
Lang = Model.get('ir.lang')

def LoadParties ():

    Party = Model.get('party.party')
    parties = csv.reader(open('terceros.csv', 'r'))
    header=True
    inicio=1
    
    if (inicio == 1): inicio = 2 
    for i in range(inicio - 1):
        parties.next()

    for index,row in enumerate(parties):
        party = Party()
        if row[2]:
            tipo = '0'+str(row[2])
        else:
            tipo = ''
        party.name = row[1]
        party.type_document = tipo
        party.vat_number = row[0]
        party.active = True
        Calle = row[4]
        Ciudad = row[6]
        Pais = row[5]
        Telefono = row[3]
        Correo = "hola@nodux.ec"
        party.addresses.pop()
        (coun,) = Country.find([('code', '=', 'EC')])
        address = party.addresses.new(street=Calle, country=coun,city=Ciudad)
        (es,) = Lang.find([('code', '=', 'es_EC')])
        party.lang = es

        if (Telefono != ''):
            contactmecanism = party.contact_mechanisms.new(type='phone', value=Telefono)
        if (Correo != ''):
            contactmecanism = party.contact_mechanisms.new(type='email', value=Correo)
        party.save()
        print "Created party ", party
LoadParties()
