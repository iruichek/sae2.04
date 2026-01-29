#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint

from controllers.auth_security import *
from controllers.fixtures_load import *

from controllers.client_article import *
from controllers.client_panier import *
from controllers.client_commande import *
from controllers.client_commentaire import *
from controllers.client_coordonnee import *

from controllers.admin_article import *
from controllers.admin_declinaison_article import *
from controllers.admin_commande import *
from controllers.admin_type_article import *
from controllers.admin_dataviz import *
from controllers.admin_commentaire import *
from controllers.client_liste_envies import *

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    if 'role' in session:
        if session['role'] == 'ROLE_admin':
            return redirect('/admin/commande/index')
        elif session['role'] == 'ROLE_client':
            return redirect('/client/article/show')
    return render_template('auth/layout.html')


##################
# Authentification
##################

# Middleware de sécurité
@app.before_request
def before_request():
    # Liste des routes publiques (qui ne nécessitent pas d'authentification)
    public_routes = ['/login', '/logout', '/register', '/static']

    # Si c'est une route publique, laisser passer
    if any(request.path.startswith(route) for route in public_routes):
        return None

    # Si la route commence par /admin ou /client
    if request.path.startswith('/admin') or request.path.startswith('/client'):
        print(f'Route protégée détectée: {request.path}')

        # Vérifier si l'utilisateur est connecté
        if 'role' not in session or 'id_user' not in session:
            print('Utilisateur non connecté - redirection vers /login')
            flash("Vous devez être connecté pour accéder à cette page", "alert-warning")
            return redirect('/login')

        # Vérifier les autorisations
        print(f"Rôle utilisateur: {session.get('role')}, Path: {request.path}")

        # Admin essaie d'accéder à une route client
        if request.path.startswith('/client') and session['role'] != 'ROLE_client':
            print(f"Accès refusé: Admin tente d'accéder à une route client")
            flash("Accès non autorisé pour votre rôle", "alert-danger")
            return redirect('/admin/commande/index')

        # Client essaie d'accéder à une route admin
        if request.path.startswith('/admin') and session['role'] != 'ROLE_admin':
            print(f"Accès refusé: Client tente d'accéder à une route admin")
            flash("Accès non autorisé pour votre rôle", "alert-danger")
            return redirect('/client/article/show')

    return None


# Enregistrement des blueprints
app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)

app.register_blueprint(client_article)
app.register_blueprint(client_commande)
app.register_blueprint(client_commentaire)
app.register_blueprint(client_panier)
app.register_blueprint(client_coordonnee)
app.register_blueprint(client_liste_envies)

app.register_blueprint(admin_article)
app.register_blueprint(admin_declinaison_article)
app.register_blueprint(admin_commande)
app.register_blueprint(admin_type_article)
app.register_blueprint(admin_dataviz)
app.register_blueprint(admin_commentaire)

# UN SEUL app.run()
if __name__ == '__main__':
    app.run(debug=True)