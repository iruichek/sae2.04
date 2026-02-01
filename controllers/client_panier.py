#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone')
    quantite = int(request.form.get('quantite', 1))

    if not id_telephone or quantite <= 0:
        flash('Données invalides', 'alert-danger')
        return redirect('/client/telephone/show')


    sql_stock = "SELECT stock FROM telephone WHERE id_telephone = %s"
    mycursor.execute(sql_stock, (id_telephone,))
    result = mycursor.fetchone()

    if not result or result['stock'] < quantite:
        flash('Stock insuffisant', 'alert-warning')
        return redirect('/client/telephone/show')


    sql_check = '''
        SELECT id_ligne_panier, quantite 
        FROM ligne_panier 
        WHERE user_id = %s AND telephone_id = %s
    '''
    mycursor.execute(sql_check, (id_client, id_telephone))
    ligne_existante = mycursor.fetchone()

    if ligne_existante:

        nouvelle_quantite = ligne_existante['quantite'] + quantite

        if nouvelle_quantite > result['stock']:
            flash('Stock insuffisant pour cette quantité', 'alert-warning')
            return redirect('/client/telephone/show')

        sql_update = '''
            UPDATE ligne_panier 
            SET quantite = %s 
            WHERE id_ligne_panier = %s
        '''
        mycursor.execute(sql_update, (nouvelle_quantite, ligne_existante['id_ligne_panier']))
    else:

        sql_insert = '''
            INSERT INTO ligne_panier (user_id, telephone_id, quantite) 
            VALUES (%s, %s, %s)
        '''
        mycursor.execute(sql_insert, (id_client, id_telephone, quantite))


    sql_update_stock = '''
        UPDATE telephone 
        SET stock = stock - %s 
        WHERE id_telephone = %s
    '''
    mycursor.execute(sql_update_stock, (quantite, id_telephone))

    get_db().commit()
    flash('Téléphone ajouté au panier', 'alert-success')
    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone', '')

    if not id_telephone:
        flash('Erreur', 'alert-danger')
        return redirect('/client/telephone/show')


    sql = '''
        SELECT id_ligne_panier, quantite, telephone_id
        FROM ligne_panier 
        WHERE user_id = %s AND telephone_id = %s
    '''
    mycursor.execute(sql, (id_client, id_telephone))
    telephone_panier = mycursor.fetchone()

    if telephone_panier:
        if telephone_panier['quantite'] > 1:

            sql_update = '''
                UPDATE ligne_panier 
                SET quantite = quantite - 1 
                WHERE id_ligne_panier = %s
            '''
            mycursor.execute(sql_update, (telephone_panier['id_ligne_panier'],))
        else:

            sql_delete = '''
                DELETE FROM ligne_panier 
                WHERE id_ligne_panier = %s
            '''
            mycursor.execute(sql_delete, (telephone_panier['id_ligne_panier'],))


        sql_stock = '''
            UPDATE telephone 
            SET stock = stock + 1 
            WHERE id_telephone = %s
        '''
        mycursor.execute(sql_stock, (id_telephone,))

        get_db().commit()
        flash('Téléphone retiré du panier', 'alert-success')

    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']


    sql = '''
        SELECT id_ligne_panier, telephone_id, quantite 
        FROM ligne_panier 
        WHERE user_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()

    for item in items_panier:

        sql_delete = '''
            DELETE FROM ligne_panier 
            WHERE id_ligne_panier = %s
        '''
        mycursor.execute(sql_delete, (item['id_ligne_panier'],))


        sql_stock = '''
            UPDATE telephone 
            SET stock = stock + %s 
            WHERE id_telephone = %s
        '''
        mycursor.execute(sql_stock, (item['quantite'], item['telephone_id']))

    get_db().commit()
    flash('Panier vidé', 'alert-success')
    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ligne_panier = request.form.get('id_ligne_panier')

    if not id_ligne_panier:
        flash('Erreur', 'alert-danger')
        return redirect('/client/telephone/show')


    sql = '''
        SELECT telephone_id, quantite 
        FROM ligne_panier 
        WHERE id_ligne_panier = %s AND user_id = %s
    '''
    mycursor.execute(sql, (id_ligne_panier, id_client))
    ligne = mycursor.fetchone()

    if ligne:

        sql_delete = '''
            DELETE FROM ligne_panier 
            WHERE id_ligne_panier = %s
        '''
        mycursor.execute(sql_delete, (id_ligne_panier,))


        sql_stock = '''
            UPDATE telephone 
            SET stock = stock + %s 
            WHERE id_telephone = %s
        '''
        mycursor.execute(sql_stock, (ligne['quantite'], ligne['telephone_id']))

        get_db().commit()
        flash('Ligne supprimée du panier', 'alert-success')

    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/show')
def client_panier_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')


    sql = '''
        SELECT 
            lp.id_ligne_panier,
            lp.quantite,
            t.id_telephone,
            t.nom_telephone AS nom,
            t.prix_telephone AS prix,
            t.photo AS image,
            t.stock,
            c.libelle_couleur,
            (lp.quantite * t.prix_telephone) AS prix_ligne
        FROM ligne_panier lp
        JOIN telephone t ON lp.telephone_id = t.id_telephone
        JOIN couleur c ON t.couleur_id = c.id_couleur
        WHERE lp.user_id = %s
    '''

    try:
        mycursor.execute(sql, (id_client,))
        telephone_panier = mycursor.fetchall()


        prix_total = sum(item['prix_ligne'] for item in telephone_panier) if telephone_panier else 0
    except Exception as e:
        print(f"Erreur panier: {e}")
        telephone_panier = []
        prix_total = 0

    return render_template(
        'client/boutique/panier_client.html',
        telephone_panier=telephone_panier,
        prix_total=prix_total
    )


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)


    if filter_word:
        session['filter_word'] = filter_word
    if filter_prix_min:
        session['filter_prix_min'] = filter_prix_min
    if filter_prix_max:
        session['filter_prix_max'] = filter_prix_max
    if filter_types:
        session['filter_types'] = filter_types

    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():

    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)

    print("Filtres supprimés")
    flash('Filtres supprimés', 'alert-info')
    return redirect('/client/telephone/show')


