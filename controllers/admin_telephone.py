# ! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash

from connexion_db import get_db

admin_telephone = Blueprint('admin_telephone', __name__,
                            template_folder='templates')


@admin_telephone.route('/admin/telephone/show')
def show_telephone():
    mycursor = get_db().cursor()


    sql = '''
        SELECT 
            t.id_telephone,
            t.nom_telephone,
            t.prix_telephone,
            t.stock,
            t.marque,
            t.fournisseur,
            t.photo AS image,
            c.libelle_couleur,
            tt.libelle_type_telephone
        FROM telephone t
        LEFT JOIN couleur c ON t.couleur_id = c.id_couleur
        LEFT JOIN type_telephone tt ON t.type_telephone_id = tt.id_type_telephone
        ORDER BY t.nom_telephone
    '''

    try:
        mycursor.execute(sql)
        telephone = mycursor.fetchall()
    except Exception as e:
        print(f"Erreur SQL show_telephone: {e}")
        telephone = []

    return render_template('admin/telephone/show_telephone.html', telephone=telephone)


@admin_telephone.route('/admin/telephone/add', methods=['GET'])
def add_telephone():
    mycursor = get_db().cursor()


    sql_types = 'SELECT id_type_telephone, libelle_type_telephone FROM type_telephone'
    mycursor.execute(sql_types)
    types_telephone = mycursor.fetchall()


    sql_couleurs = 'SELECT id_couleur, libelle_couleur FROM couleur'
    mycursor.execute(sql_couleurs)
    couleurs = mycursor.fetchall()

    return render_template('admin/telephone/add_telephone.html',
                           types_telephone=types_telephone,
                           couleurs=couleurs)


@admin_telephone.route('/admin/telephone/add', methods=['POST'])
def valid_add_telephone():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_telephone_id = request.form.get('type_telephone_id', '')
    couleur_id = request.form.get('couleur_id', 1)
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', 0)
    marque = request.form.get('marque', '')
    fournisseur = request.form.get('fournisseur', '')
    poids = request.form.get('poids', '')
    taille = request.form.get('taille', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        filename = None

    sql = '''
        INSERT INTO telephone 
        (nom_telephone, photo, prix_telephone, type_telephone_id, couleur_id, stock, marque, fournisseur, poids, taille)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    tuple_add = (nom, filename, prix, type_telephone_id, couleur_id, stock, marque, fournisseur, poids, taille)

    try:
        mycursor.execute(sql, tuple_add)
        get_db().commit()

        message = f'Téléphone ajouté : {nom} - Type: {type_telephone_id} - Prix: {prix}€'
        flash(message, 'alert-success')
    except Exception as e:
        print(f"Erreur ajout téléphone: {e}")
        flash("Erreur lors de l'ajout du téléphone", 'alert-danger')

    return redirect('/admin/telephone/show')


@admin_telephone.route('/admin/telephone/delete', methods=['GET'])
def delete_telephone():
    id_telephone = request.args.get('id_telephone')
    mycursor = get_db().cursor()


    sql = '''
        SELECT COUNT(*) as nb_ventes
        FROM ligne_commande
        WHERE telephone_id = %s
    '''
    mycursor.execute(sql, (id_telephone,))
    nb_ventes = mycursor.fetchone()

    if nb_ventes['nb_ventes'] > 0:
        message = 'Ce téléphone a été vendu : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:

        sql = '''
            SELECT photo AS image
            FROM telephone
            WHERE id_telephone = %s
        '''
        mycursor.execute(sql, (id_telephone,))
        telephone = mycursor.fetchone()

        if telephone:
            image = telephone['image']


            sql = 'DELETE FROM telephone WHERE id_telephone = %s'
            mycursor.execute(sql, (id_telephone,))
            get_db().commit()


            if image is not None and os.path.exists('static/images/' + image):
                os.remove('static/images/' + image)

            message = f'Téléphone supprimé, id : {id_telephone}'
            flash(message, 'alert-success')

    return redirect('/admin/telephone/show')


@admin_telephone.route('/admin/telephone/edit', methods=['GET'])
def edit_telephone():
    id_telephone = request.args.get('id_telephone')
    mycursor = get_db().cursor()

    sql = '''
        SELECT 
            t.id_telephone,
            t.nom_telephone  AS nom,
            t.prix_telephone AS prix,
            t.stock,
            t.marque,
            t.fournisseur,
            t.poids,
            t.taille         AS description,
            t.photo          AS image,
            t.type_telephone_id,
            t.couleur_id
        FROM telephone t
        WHERE t.id_telephone = %s
    '''
    mycursor.execute(sql, (id_telephone,))
    telephone = mycursor.fetchone()


    sql = '''
        SELECT id_type_telephone, libelle_type_telephone AS libelle
        FROM type_telephone
    '''
    mycursor.execute(sql)
    types_telephone = mycursor.fetchall()

    sql = 'SELECT id_couleur, libelle_couleur FROM couleur'
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    declinaisons_telephone = []

    return render_template('admin/telephone/edit_telephone.html',
                           telephone=telephone,
                           types_telephone=types_telephone,
                           couleurs=couleurs,
                           declinaisons_telephone=declinaisons_telephone)


@admin_telephone.route('/admin/telephone/edit', methods=['POST'])
def valid_edit_telephone():
    mycursor = get_db().cursor()

    nom             = request.form.get('nom')
    id_telephone    = request.form.get('id_telephone')
    image           = request.files.get('image')
    type_telephone_id = request.form.get('type_telephone_id')
    prix            = request.form.get('prix')
    stock           = request.form.get('stock', 0)
    taille          = request.form.get('description', '')

    sql = 'SELECT photo AS image FROM telephone WHERE id_telephone = %s'
    mycursor.execute(sql, (id_telephone,))
    result = mycursor.fetchone()
    image_nom = result['image'] if result else None

    if image and image.filename != '':
        if image_nom and os.path.exists(os.path.join('static/images/', image_nom)):
            os.remove(os.path.join('static/images/', image_nom))
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
        image_nom = filename

    sql = '''
        UPDATE telephone 
        SET nom_telephone     = %s, 
            photo             = %s, 
            prix_telephone    = %s, 
            type_telephone_id = %s, 
            stock             = %s,
            taille            = %s
        WHERE id_telephone = %s
    '''

    try:
        mycursor.execute(sql, (nom, image_nom, prix, type_telephone_id, stock, taille, id_telephone))
        get_db().commit()
        flash(f'Téléphone "{nom}" modifié avec succès', 'alert-success')
    except Exception as e:
        print(f"Erreur modification téléphone: {e}")
        flash("Erreur lors de la modification", 'alert-danger')

    return redirect('/admin/telephone/show')


@admin_telephone.route('/admin/telephone/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()


    sql = '''
        SELECT id_telephone, nom_telephone
        FROM telephone
        WHERE id_telephone = %s
    '''
    mycursor.execute(sql, (id,))
    telephone = mycursor.fetchone()


    commentaires = []

    return render_template('admin/telephone/show_avis.html',
                           telephone=telephone,
                           commentaires=commentaires)


@admin_telephone.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    telephone_id = request.form.get('idtelephone', None)
    userId = request.form.get('idUser', None)



    return redirect(f'/admin/telephone/avis/{telephone_id}')