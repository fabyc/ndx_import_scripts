#! -*- coding: utf8 -*-

import csv
from proteus import config, Model, Wizard

database = 'database_name'
user = 'nodux_admin_user'
password = 'nodux_admin_password'
config_file = 'path_to_file_nodux_config'

config = config.set_trytond(database=database, user=user, language='es_EC.UTF-8', password=password, config_file=config_file)
modules = csv.reader(open('modules_pymes.csv', 'r'))

Group = Model.get('res.group')
Ir = Model.get('ir.model')
Field = Model.get('ir.model.field')
User= Model.get('res.user')

def LoadGroupV():
    Menu = Model.get('ir.ui.menu')
    group = Group()
    group.name = "Nodux - Ventas"
    model_access= group.model_access.new()
    
    if len(Ir.find([('model', '=', 'sale.sale')])) == 1:
        modelo, = Ir.find([('model', '=', 'sale.sale')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
    
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'sale.line')])) == 1:
        modelo, = Ir.find([('model', '=', 'sale.line')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = True
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.invoice')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.invoice')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.invoice.line')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.invoice.line')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'stock.move')])) == 1:
        modelo, = Ir.find([('model', '=', 'stock.move')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'stock.shipment.out')])) == 1:
        modelo, = Ir.find([('model', '=', 'stock.shipment.out')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'stock.shipment.out.return')])) == 1:
        modelo, = Ir.find([('model', '=', 'stock.shipment.out.return')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = False
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.statement')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.statement')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = False
        model_access.perm_delete = False
        
    model_access= group.model_access.new()
    if len(Ir.find([('model', '=', 'account.statement.line')])) == 1:
        modelo, = Ir.find([('model', '=', 'account.statement.line')])
        model_access.model = modelo
        model_access.perm_read = True
        model_access.perm_write = True
        model_access.perm_create = True
        model_access.perm_delete = False
    
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price'), ('module', '=', 'product'), ('model.model', '=', 'product.template')])) == 1:
        field, = Field.find([('name', '=', 'cost_price'), ('module', '=', 'product'),  ('model.model', '=', 'product.template')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price_uom'), ('module', '=', 'product'),('model.model', '=', 'product.product')])) == 1:
        field, = Field.find([('name', '=', 'cost_price_uom'), ('module', '=', 'product'),  ('model.model', '=', 'product.product')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price_method'), ('module', '=', 'product'), ('model.model', '=', 'product.template')])) == 1:
        field, =(Field.find([('name', '=', 'cost_price_method'), ('module', '=', 'product'), ('model.model', '=', 'product.template')])) 
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=','stock.location')])) == 1:
        field, = Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=','stock.location')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.template' )])) == 1:
        field, = (Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.template' )]))
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
        
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.product')])) == 1:
        field, = Field.find([('name', '=', 'cost_value'), ('module', '=', 'stock'), ('model.model', '=', 'product.product')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
      
    field_access = group.field_access.new()
    if len(Field.find([('name', '=', 'cost_price'), ('module', '=', 'stock'), ('model.model', '=', 'stock.move')])) == 1:
        field, = Field.find([('name', '=', 'cost_price'), ('module', '=', 'stock'), ('model.model', '=', 'stock.move')])
        field_access.field = field
        field_access.perm_read = False
        field_access.perm_write = False
        field_access.perm_create = False
        field_access.perm_delete = False
    
    group.save()
    groups = Group.find([('name','=', 'Nodux - Ventas')])
    menus = Menu.find([('sequence','=', 5), ('parent', '=', None)])
    menus_v = Menu.find([('sequence','=', 10), ('parent.sequence', '=', 5)])
    for group in groups:
        group.menu_access.append(menus[0])
        group.menu_access.append(menus_v[0])
    group.save()
    print "Created group  ", group
LoadGroupV()
