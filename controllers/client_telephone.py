#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, session
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
        ORDER BY t.nom_telephone, c.libelle_couleur
    '''

    try:
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

    telephone_panier = []

    return render_template(
        'client/boutique/panier_telephone.html',
        telephone=telephone,
        telephone_panier=telephone_panier,
        items_filtre=types_telephone
    )