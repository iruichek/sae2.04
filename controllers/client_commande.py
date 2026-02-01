#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                            template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Pour l'instant, retour de données vides (non fonctionnel)
    telephone_panier = []
    prix_total = None

    return render_template('client/boutique/panier_validation_adresses.html',
                           telephone_panier=telephone_panier,
                           prix_total=prix_total,
                           validation=1)


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Non fonctionnel pour l'instant
    items_ligne_panier = []

    get_db().commit()
    flash('Commande ajoutée', 'alert-success')
    return redirect('/client/telephone/show')  # ← CORRIGÉ ICI


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    """Page d'affichage des commandes - Version minimale qui fonctionne"""


    commandes = []
    telephone_commande = None
    commande_adresses = None

    id_commande = request.args.get('id_commande', None)


    if id_commande:
        print(f"ID Commande reçu: {id_commande}")

    return render_template('client/commandes/show.html',
                           commandes=commandes,
                           telephone_commande=telephone_commande,
                           commande_adresses=commande_adresses)

