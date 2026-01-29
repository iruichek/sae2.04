#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_telephone = Blueprint('admin_telephone', __name__,
                          template_folder='templates')


@admin_telephone.route('/admin/telephone/show')
def show_telephone():
    mycursor = get_db().cursor()
    sql = '''  requête admin_telephone_1
    '''
    mycursor.execute(sql)
    telephones = mycursor.fetchall()
    return render_template('admin/telephone/show_telephone.html', telephones=telephones)


@admin_telephone.route('/admin/telephone/add', methods=['GET'])
def add_telephone():
    mycursor = get_db().cursor()

    return render_template('admin/telephone/add_telephone.html'
                           #,types_telephone=type_telephone,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_telephone.route('/admin/telephone/add', methods=['POST'])
def valid_add_telephone():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_telephone_id = request.form.get('type_telephone_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_telephone_2 '''

    tuple_add = (nom, filename, prix, type_telephone_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'telephone ajouté , nom: ', nom, ' - type_telephone:', type_telephone_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'telephone ajouté , nom:' + nom + '- type_telephone:' + type_telephone_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/telephone/show')


@admin_telephone.route('/admin/telephone/delete', methods=['GET'])
def delete_telephone():
    id_telephone=request.args.get('id_telephone')
    mycursor = get_db().cursor()
    sql = ''' requête admin_telephone_3 '''
    mycursor.execute(sql, id_telephone)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet telephone : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_telephone_4 '''
        mycursor.execute(sql, id_telephone)
        telephone = mycursor.fetchone()
        print(telephone)
        image = telephone['image']

        sql = ''' requête admin_telephone_5  '''
        mycursor.execute(sql, id_telephone)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un telephone supprimé, id :", id_telephone)
        message = u'un telephone supprimé, id : ' + id_telephone
        flash(message, 'alert-success')

    return redirect('/admin/telephone/show')


@admin_telephone.route('/admin/telephone/edit', methods=['GET'])
def edit_telephone():
    id_telephone=request.args.get('id_telephone')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_telephone_6    
    '''
    mycursor.execute(sql, id_telephone)
    telephone = mycursor.fetchone()
    print(telephone)
    sql = '''
    requête admin_telephone_7
    '''
    mycursor.execute(sql)
    types_telephone = mycursor.fetchall()

    # sql = '''
    # requête admin_telephone_6
    # '''
    # mycursor.execute(sql, id_telephone)
    # declinaisons_telephone = mycursor.fetchall()

    return render_template('admin/telephone/edit_telephone.html'
                           ,telephone=telephone
                           ,types_telephone=types_telephone
                         #  ,declinaisons_telephone=declinaisons_telephone
                           )


@admin_telephone.route('/admin/telephone/edit', methods=['POST'])
def valid_edit_telephone():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_telephone = request.form.get('id_telephone')
    image = request.files.get('image', '')
    type_telephone_id = request.form.get('type_telephone_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_telephone_8
       '''
    mycursor.execute(sql, id_telephone)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_telephone_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_telephone_id, description, id_telephone))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'telephone modifié , nom:' + nom + '- type_telephone :' + type_telephone_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/telephone/show')







@admin_telephone.route('/admin/telephone/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    telephone=[]
    commentaires = {}
    return render_template('admin/telephone/show_avis.html'
                           , telephone=telephone
                           , commentaires=commentaires
                           )


@admin_telephone.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    telephone_id = request.form.get('idtelephone', None)
    userId = request.form.get('idUser', None)

    return admin_avis(telephone_id)
