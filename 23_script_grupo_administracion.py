#! -*- coding: utf8 -*-

import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)

Group = Model.get('res.group')
Ir = Model.get('ir.model')
User= Model.get('res.user')

def LoadGroupA():
    
    group = Group()
    group.name = "Nodux - Administración"
    model_access= group.model_access.new()
    
    if len(Ir.find([('model', '=', 'ir.sequence.strict')])) == 1:
        modelo, = Ir.find([('model', '=', 'ir.sequence.strict')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
    
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'ir.sequence.type')])) == 1:
        modelo, = Ir.find([('model', '=', 'ir.sequence.type')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'ir.sequence')])) == 1:
        modelo, = Ir.find([('model', '=', 'ir.sequence')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
    
    group.save()
    print "Created group  ", group
LoadGroupA()
