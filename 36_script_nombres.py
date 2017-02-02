import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Party = Model.get('party.party')

def UpdateParties():
    parties = csv.reader(open('terceros.csv', 'r'))
    header=True
    inicio=1

    if (inicio == 1): inicio = 2
    for i in range(inicio - 1):
        parties.next()

    for index,row in enumerate(parties):
        party = Party()

        if len(party.find([('name', '=',row[1])])) == 1:
            pty, = party.find([('name', '=',row[1])])
            pty.name = row[0]
            pty.save()
            print "Modificado party ", pty.name

UpdateParties()
