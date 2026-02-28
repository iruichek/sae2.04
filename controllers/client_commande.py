#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                            template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['GET', 'POST'])
def client_commande_valide():
    """Page de validation avant de passer commande"""
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # ✅ AJOUT : Récupérer le panier avec calcul en SQL
    sql = '''
        SELECT 
            lp.id_ligne_panier,
            lp.quantite,
            t.id_telephone,
            t.nom_telephone AS nom,
            t.prix_telephone AS prix,
            t.photo AS image,
            c.libelle_couleur,
            (lp.quantite * t.prix_telephone) AS prix_ligne
        FROM ligne_panier lp
        JOIN telephone t ON lp.telephone_id = t.id_telephone
        JOIN couleur c ON t.couleur_id = c.id_couleur
        WHERE lp.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    telephone_panier = mycursor.fetchall()

    # ✅ AJOUT : Calculer le prix total en SQL
    if telephone_panier and len(telephone_panier) >= 1:
        sql_prix_total = '''
            SELECT SUM(lp.quantite * t.prix_telephone) AS prix_total
            FROM ligne_panier lp
            JOIN telephone t ON lp.telephone_id = t.id_telephone
            WHERE lp.utilisateur_id = %s
        '''
        mycursor.execute(sql_prix_total, (id_client,))
        result = mycursor.fetchone()
        prix_total = result['prix_total'] if result else 0
    else:
        prix_total = None
        flash('Votre panier est vide', 'alert-warning')
        return redirect('/client/telephone/show')

    return render_template('client/boutique/panier_validation_adresses.html',
                           telephone_panier=telephone_panier,
                           prix_total=prix_total,
                           validation=1)


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    """✅ Validation finale : créer la commande"""
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # ✅ AJOUT : Sélection du contenu du panier
    sql = '''
        SELECT 
            lp.id_ligne_panier,
            lp.telephone_id,
            lp.quantite,
            t.prix_telephone AS prix
        FROM ligne_panier lp
        JOIN telephone t ON lp.telephone_id = t.id_telephone
        WHERE lp.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier or len(items_ligne_panier) < 1:
        flash('Pas de téléphones dans le panier', 'alert-warning')
        return redirect('/client/telephone/show')

    # ✅ AJOUT : Création de la commande
    date_achat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql_commande = '''
        INSERT INTO commande (utilisateur_id, date_achat, etat_id) 
        VALUES (%s, %s, 1)
    '''
    mycursor.execute(sql_commande, (id_client, date_achat))

    # ✅ AJOUT : Récupération de l'ID de la dernière commande
    sql_last_id = 'SELECT LAST_INSERT_ID() as last_insert_id'
    mycursor.execute(sql_last_id)
    id_commande = mycursor.fetchone()['last_insert_id']

    # ✅ AJOUT : Ajout des lignes de commande + suppression du panier
    for item in items_ligne_panier:
        # Suppression de la ligne de panier
        sql_delete_panier = '''
            DELETE FROM ligne_panier 
            WHERE id_ligne_panier = %s
        '''
        mycursor.execute(sql_delete_panier, (item['id_ligne_panier'],))

        # ✅ Ajout d'une ligne de commande
        sql_insert_commande = '''
            INSERT INTO ligne_commande (commande_id, telephone_id, quantite, prix) 
            VALUES (%s, %s, %s, %s)
        '''
        mycursor.execute(sql_insert_commande,
                         (id_commande, item['telephone_id'], item['quantite'], item['prix']))

    get_db().commit()
    flash('Commande créée avec succès !', 'alert-success')
    return redirect('/client/commande/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    """✅ Affichage de la liste des commandes + détail si sélectionné"""
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # ✅ AJOUT : Sélection des commandes du client avec calculs en SQL
    sql = '''
        SELECT 
            c.id_commande,
            c.date_achat,
            c.etat_id,
            e.libelle,
            COUNT(lc.telephone_id) AS nbr_articles,
            SUM(lc.quantite * lc.prix) AS prix_total
        FROM commande c
        LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        LEFT JOIN etat e ON c.etat_id = e.id_etat
        WHERE c.utilisateur_id = %s
        GROUP BY c.id_commande
        ORDER BY c.date_achat DESC
    '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    telephone_commande = None
    commande_adresses = None

    # ✅ AJOUT : Si on clique sur une commande, afficher le détail
    id_commande = request.args.get('id_commande', None)

    if id_commande:
        print(f"ID Commande reçu: {id_commande}")

        # ✅ AJOUT : Sélection du détail d'une commande avec calcul en SQL
        sql_detail = '''
            SELECT 
                lc.quantite,
                lc.prix,
                (lc.quantite * lc.prix) AS prix_ligne,
                t.nom_telephone AS nom,
                t.photo AS image,
                c.libelle_couleur
            FROM ligne_commande lc
            JOIN telephone t ON lc.telephone_id = t.id_telephone
            JOIN couleur c ON t.couleur_id = c.id_couleur
            WHERE lc.commande_id = %s
        '''
        mycursor.execute(sql_detail, (id_commande,))
        telephone_commande = mycursor.fetchall()

    return render_template('client/commandes/show.html',
                           commandes=commandes,
                           telephone_commande=telephone_commande,
                           commande_adresses=commande_adresses)