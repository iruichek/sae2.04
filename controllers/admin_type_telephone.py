#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_telephone = Blueprint('admin_type_telephone', __name__,
                        template_folder='templates')

@admin_type_telephone.route('/admin/type-telephone/show')
def show_type_telephone():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_telephone = mycursor.fetchall()
    types_telephone=[]
    return render_template('admin/type_telephone/show_type_telephone.html', types_telephone=types_telephone)

@admin_type_telephone.route('/admin/type-telephone/add', methods=['GET'])
def add_type_telephone():
    return render_template('admin/type_telephone/add_type_telephone.html')

@admin_type_telephone.route('/admin/type-telephone/add', methods=['POST'])
def valid_add_type_telephone():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-telephone/show') #url_for('show_type_telephone')

@admin_type_telephone.route('/admin/type-telephone/delete', methods=['GET'])
def delete_type_telephone():
    id_type_telephone = request.args.get('id_type_telephone', '')
    mycursor = get_db().cursor()

    flash(u'suppression type telephone , id : ' + id_type_telephone, 'alert-success')
    return redirect('/admin/type-telephone/show')

@admin_type_telephone.route('/admin/type-telephone/edit', methods=['GET'])
def edit_type_telephone():
    id_type_telephone = request.args.get('id_type_telephone', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_telephone,))
    type_telephone = mycursor.fetchone()
    return render_template('admin/type_telephone/edit_type_telephone.html', type_telephone=type_telephone)

@admin_type_telephone.route('/admin/type-telephone/edit', methods=['POST'])
def valid_edit_type_telephone():
    libelle = request.form['libelle']
    id_type_telephone = request.form.get('id_type_telephone', '')
    tuple_update = (libelle, id_type_telephone)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type telephone modifié, id: ' + id_type_telephone + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-telephone/show')








