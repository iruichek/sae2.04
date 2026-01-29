#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, session
from connexion_db import get_db

client_article = Blueprint(
    'client_article',
    __name__,
    template_folder='templates'
)

@client_article.route('/client/index')
@client_article.route('/client/article/show')  # remplace /client
def client_article_show():  # remplace client_index
    mycursor = get_db().cursor()

    # Récupération de l'id client (sécurisé avec get)
    id_client = session.get('id_user')

    # Requête pour récupérer les téléphones avec couleur et type
    sql = '''
        SELECT
            t.id_telephone,
            t.nom_telephone,
            t.poids,
            t.taille,
            t.prix_telephone,
            t.fournisseur,
            t.marque,
            t.photo,
            t.stock,
            c.libelle_couleur,
            tt.libelle_type_telephone
        FROM telephone t
        JOIN couleur c ON t.couleur_id = c.id_couleur
        JOIN type_telephone tt ON t.type_telephone_id = tt.id_type_telephone
        ORDER BY t.nom_telephone, c.libelle_couleur
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    # Récupération des types d'article pour le filtre
    sql_types = '''
        SELECT id_type_telephone, libelle_type_telephone
        FROM type_telephone
    '''
    mycursor.execute(sql_types)
    types_article = mycursor.fetchall()

    articles_panier = []
    prix_total = None  # pas encore utilisé

    return render_template(
        'client/boutique/panier_article.html',
        articles=articles,
        articles_panier=articles_panier,
        # prix_total=prix_total,
        items_filtre=types_article
    )
