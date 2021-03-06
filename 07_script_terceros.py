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

        if len(Party.find([('vat_number', '=', row[0])])) >= 1:
            f = open('terceros_duplicados.csv', 'a')
            obj = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            obj.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row [7], row[8]])
            print "Duplicated party ", row[0], row[1]
            f.close()
        else:
            if row[2]:
                if len(str(row[2])) < 2:
                    tipo = '0'+str(row[2])
                else:
                    tipo = str(row[2])
            else:
                tipo = ''
            if row[7]:
                Correo = row[7]
            else:
                Correo = "info@toners.ec"
            if row[8]:
                comercial = row[8]
            else:
                comercial = ""

            party.name = row[1]
            party.commercial_name = comercial
            party.type_document = tipo
            party.vat_number = row[0]
            party.active = True
            Calle = row[4]
            Ciudad = row[6]
            Pais = row[5]
            Telefono = row[3]
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
            print "Created party ", party, party.name
LoadParties()
