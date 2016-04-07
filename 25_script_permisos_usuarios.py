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

def LoadVentasNodux():
    group = Group()
    groups = Group.find([('name','=', 'Nodux - Ventas')])
    vendedores = ('VENDEDOR 1', 'VENDEDOR 2')
    for vendedor in vendedores:
        users = User.find([('name', '=',  vendedor)])
        for group in groups:
            group.users.append(users[0])
            group.save()   
LoadVentasNodux()

def LoadAdministracion():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Nodux - Administración')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracion()

def LoadFinanciero():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Financiero')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
    
LoadFinanciero()
       
def LoadAdministracionContabilidad():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administración de Contabilidad')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionContabilidad()
   
def LoadAdministracionBancos():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administración de Bancos')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionBancos()
    
def LoadAdministracionProductos():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administración de Productos')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionProductos()

def LoadAdministracionStock():
    groups = Group.find([('name','=', 'Administración de Stock')])
    usuarios = ('CONTADOR', 'BODEGUERO')
    for usuario in usuarios:
        users = User.find([('name','=', usuario)])
        for group in groups:
            group.users.append(users[0])
            group.save()
LoadAdministracionStock()

def LoadStock():
    usuarios = ('CONTADOR', 'BODEGUERO')
    groups = Group.find([('name','=', 'Stock')])
    for usuario in usuarios:
        users = User.find([('name','=', usuario)])
        for group in groups:
            group.users.append(users[0])
            group.save()
LoadStock()

def LoadAsignacionStock():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Asignación Forzada de Stock')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAsignacionStock()

def LoadVentas():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Ventas')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadVentas()

def LoadAdministracionVentas():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administrador de Ventas')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionVentas()

def LoadAdministracionCompras():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Administrador de Compras')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadAdministracionCompras()
    
def LoadCompras():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Compras')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadCompras()

def LoadSolicitudCompras():
    usuario = 'CONTADOR'
    groups = Group.find([('name','=', 'Solicitud de Compras')])
    users = User.find([('name','=', usuario)])
    for group in groups:
        group.users.append(users[0])
        group.save()
LoadSolicitudCompras()


