#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_telephone = Blueprint('admin_declinaison_telephone', __name__,
                         template_folder='templates')


@admin_declinaison_telephone.route('/admin/declinaison_telephone/add')
def add_declinaison_telephone():
    id_telephone=request.args.get('id_telephone')
    mycursor = get_db().cursor()
    telephone=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/telephone/add_declinaison_telephone.html'
                           , telephone=telephone
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_telephone.route('/admin/declinaison_telephone/add', methods=['POST'])
def valid_add_declinaison_telephone():
    mycursor = get_db().cursor()

    id_telephone = request.form.get('id_telephone')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')

    get_db().commit()
    return redirect('/admin/telephone/edit?id_telephone=' + id_telephone)


@admin_declinaison_telephone.route('/admin/declinaison_telephone/edit', methods=['GET'])
def edit_declinaison_telephone():
    id_declinaison_telephone = request.args.get('id_declinaison_telephone')
    mycursor = get_db().cursor()
    declinaison_telephone=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/telephone/edit_declinaison_telephone.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_telephone=declinaison_telephone
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_telephone.route('/admin/declinaison_telephone/edit', methods=['POST'])
def valid_edit_declinaison_telephone():
    id_declinaison_telephone = request.form.get('id_declinaison_telephone','')
    id_telephone = request.form.get('id_telephone','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_telephone modifié , id:' + str(id_declinaison_telephone) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/telephone/edit?id_telephone=' + str(id_telephone))


@admin_declinaison_telephone.route('/admin/declinaison_telephone/delete', methods=['GET'])
def admin_delete_declinaison_telephone():
    id_declinaison_telephone = request.args.get('id_declinaison_telephone','')
    id_telephone = request.args.get('id_telephone','')

    flash(u'declinaison supprimée, id_declinaison_telephone : ' + str(id_declinaison_telephone),  'alert-success')
    return redirect('/admin/telephone/edit?id_telephone=' + str(id_telephone))
