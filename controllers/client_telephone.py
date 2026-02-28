#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, session, request, flash, redirect
from connexion_db import get_db

client_telephone = Blueprint(
    'client_telephone',
    __name__,
    template_folder='templates'
)


@client_telephone.route('/client/index')
@client_telephone.route('/client/telephone/show')
def client_telephone_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    # Récupérer les filtres de la session
    filter_types = session.get('filter_types', [])
    filter_word = session.get('filter_word', '')
    filter_prix_min = session.get('filter_prix_min')
    filter_prix_max = session.get('filter_prix_max')

    # Requête avec filtres dynamiques
    sql = '''
        SELECT 
            t.id_telephone,
            t.nom_telephone AS nom,
            t.poids,
            t.taille,
            t.prix_telephone AS prix,
            t.fournisseur,
            t.marque,
            t.photo AS image,
            t.stock,
            c.libelle_couleur,
            tt.libelle_type_telephone
        FROM telephone t
        JOIN couleur c ON t.couleur_id = c.id_couleur
        JOIN type_telephone tt ON t.type_telephone_id = tt.id_type_telephone
        WHERE 1=1
    '''

    params = []

    # Filtre par type
    if filter_types and len(filter_types) > 0:
        placeholders = ','.join(['%s'] * len(filter_types))
        sql += f' AND t.type_telephone_id IN ({placeholders})'
        params.extend(filter_types)

    # Filtre par mot-clé
    if filter_word:
        sql += ' AND t.nom_telephone LIKE %s'
        params.append(f'%{filter_word}%')

    # Filtre par prix minimum
    if filter_prix_min:
        sql += ' AND t.prix_telephone >= %s'
        params.append(filter_prix_min)

    # Filtre par prix maximum
    if filter_prix_max:
        sql += ' AND t.prix_telephone <= %s'
        params.append(filter_prix_max)

    sql += ' ORDER BY t.nom_telephone, c.libelle_couleur'

    try:
        if params:
            mycursor.execute(sql, tuple(params))
        else:
            mycursor.execute(sql)

        telephone = mycursor.fetchall()

        print("=" * 50)
        print(f"Nombre de téléphones: {len(telephone)}")
        if telephone:
            print(f"Premier téléphone: {telephone[0]}")
            print(f"Chemin image: {telephone[0].get('image')}")
        print("=" * 50)
    except Exception as e:
        print(f"ERREUR SQL téléphones: {e}")
        import traceback
        traceback.print_exc()
        telephone = []

    # Types pour le filtre
    sql_types = '''
        SELECT id_type_telephone, libelle_type_telephone
        FROM type_telephone
    '''

    try:
        mycursor.execute(sql_types)
        types_telephone = mycursor.fetchall()
    except Exception as e:
        print(f"Erreur SQL types: {e}")
        types_telephone = []

    # Récupérer le panier (calcul SQL du prix total)
    sql_panier = '''
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
        WHERE lp.utilisateur_id = %s
    '''

    # Calculer le prix total en SQL
    sql_prix_total = '''
        SELECT COALESCE(SUM(lp.quantite * t.prix_telephone), 0) AS prix_total
        FROM ligne_panier lp
        JOIN telephone t ON lp.telephone_id = t.id_telephone
        WHERE lp.utilisateur_id = %s
    '''

    try:
        mycursor.execute(sql_panier, (id_client,))
        telephone_panier = mycursor.fetchall()

        mycursor.execute(sql_prix_total, (id_client,))
        result_prix = mycursor.fetchone()
        prix_total = result_prix['prix_total'] if result_prix else 0

        print(f"Nombre d'telephone dans le panier: {len(telephone_panier)}")
        print(f"Prix total (calculé en SQL): {prix_total}")
    except Exception as e:
        print(f"Erreur SQL panier: {e}")
        telephone_panier = []
        prix_total = 0

    return render_template(
        'client/boutique/panier_telephone.html',
        telephone=telephone,
        telephone_panier=telephone_panier,
        prix_total=prix_total,
        items_filtre=types_telephone
    )


@client_telephone.route('/client/telephone/details/<int:id_telephone>')
def client_telephone_details(id_telephone):
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    # Récupérer les détails du téléphone
    sql = '''
        SELECT 
            t.id_telephone AS id_telephone,
            t.nom_telephone AS nom,
            t.poids,
            t.taille,
            t.prix_telephone AS prix,
            t.fournisseur,
            t.marque,
            t.photo AS image,
            t.stock,
            c.libelle_couleur AS description,
            tt.libelle_type_telephone,
            NULL AS moyenne_notes,
            NULL AS nb_notes
        FROM telephone t
        JOIN couleur c ON t.couleur_id = c.id_couleur
        JOIN type_telephone tt ON t.type_telephone_id = tt.id_type_telephone
        WHERE t.id_telephone = %s
    '''

    try:
        mycursor.execute(sql, (id_telephone,))
        telephone = mycursor.fetchone()

        if not telephone:
            flash('Téléphone introuvable', 'alert-danger')
            return redirect('/client/telephone/show')
    except Exception as e:
        print(f"Erreur SQL détails: {e}")
        flash('Erreur lors du chargement', 'alert-danger')
        return redirect('/client/telephone/show')

    # Vérifier si le client a commandé cet telephone
    sql_commandes = '''
        SELECT COUNT(*) AS nb_commandes_telephone
        FROM commande c
        JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        WHERE c.utilisateur_id = %s AND lc.telephone_id = %s
    '''

    try:
        mycursor.execute(sql_commandes, (id_client, id_telephone))
        commandes_telephone = mycursor.fetchone()
    except Exception as e:
        print(f"Erreur SQL commandes: {e}")
        commandes_telephone = {'nb_commandes_telephone': 0}

    # TODO : Récupérer la note de l'utilisateur (quand implémenté)
    note = None

    # TODO : Récupérer les statistiques de commentaires
    nb_commentaires = {
        'nb_commentaires_utilisateur': 0,
        'nb_commentaires_total': 0,
        'nb_commentaires_utilisateur_valide': 0,
        'nb_commentaires_total_valide': 0
    }

    # TODO : Récupérer les commentaires
    commentaires = []

    return render_template(
        'client/telephone_info/telephone_details.html',  # ← CORRIGÉ ICI
        telephone=telephone,
        commandes_telephone=commandes_telephone,
        note=note,
        nb_commentaires=nb_commentaires,
        commentaires=commentaires
    )