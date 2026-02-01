#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from controllers.auth_security import auth_security
from controllers.fixtures_load import fixtures_load

from controllers.client_telephone import client_telephone
from controllers.client_panier import client_panier
from controllers.client_commande import client_commande
from controllers.client_commentaire import client_commentaire
from controllers.client_coordonnee import client_coordonnee
from controllers.client_liste_envies import client_liste_envies

from controllers.admin_telephone import admin_telephone
from controllers.admin_declinaison_telephone import admin_declinaison_telephone
from controllers.admin_type_telephone import admin_type_telephone
from controllers.admin_commande import admin_commande
from controllers.admin_dataviz import admin_dataviz
from controllers.admin_commentaire import admin_commentaire

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
            return redirect('/client/telephone/show')
    return render_template('auth/layout.html')


@app.before_request
def before_request():
    """Middleware de sécurité pour vérifier les autorisations"""


    public_routes = ['/login', '/logout', '/register', '/static', '/']

    if any(request.path.startswith(route) for route in public_routes):
        return None


    if request.path.startswith('/admin') or request.path.startswith('/client'):
        print(f'Route protégée détectée: {request.path}')


        if 'role' not in session or 'id_user' not in session:
            print('Utilisateur non connecté - redirection vers /login')
            flash("Vous devez être connecté pour accéder à cette page", "alert-warning")
            return redirect('/login')

        print(f"Rôle utilisateur: {session.get('role')}, Path: {request.path}")


        if request.path.startswith('/client') and session['role'] != 'ROLE_client':
            print("Accès refusé: Admin tente d'accéder à une route client")
            flash("Accès non autorisé pour votre rôle", "alert-danger")
            return redirect('/admin/commande/index')


        if request.path.startswith('/admin') and session['role'] != 'ROLE_admin':
            print("Accès refusé: Client tente d'accéder à une route admin")
            flash("Accès non autorisé pour votre rôle", "alert-danger")
            return redirect('/client/telephone/show')

    return None



app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)


app.register_blueprint(client_telephone)
app.register_blueprint(client_panier)
app.register_blueprint(client_commande)
app.register_blueprint(client_commentaire)
app.register_blueprint(client_coordonnee)
app.register_blueprint(client_liste_envies)


app.register_blueprint(admin_telephone)
app.register_blueprint(admin_declinaison_telephone)
app.register_blueprint(admin_commande)
app.register_blueprint(admin_type_telephone)
app.register_blueprint(admin_dataviz)
app.register_blueprint(admin_commentaire)

if __name__ == '__main__':
    app.run(debug=True)