#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    sql = '''DROP TABLE IF EXISTS ligne_panier'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS ligne_commande'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS commande'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS telephone'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS couleur'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS type_telephone'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS etat'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS utilisateur'''
    mycursor.execute(sql)


    sql = '''
    CREATE TABLE utilisateur (
        id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
        login VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        nom VARCHAR(100),
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL,
        est_actif BOOLEAN DEFAULT TRUE
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom, est_actif) VALUES
    (1, 'admin', 'admin@admin.fr',
        'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
        'ROLE_admin', 'admin', 1),
    (2, 'client', 'client@client.fr',
        'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
        'ROLE_client', 'client', 1),
    (3, 'client2', 'client2@client2.fr',
        'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
        'ROLE_client', 'client2', 1)
    '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE etat (
        id_etat INT AUTO_INCREMENT PRIMARY KEY,
        libelle VARCHAR(50) NOT NULL
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO etat (libelle) VALUES
    ('En attente'),
    ('Expédié'),
    ('Validé'),
    ('Confirmé')
    '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE type_telephone (
        id_type_telephone INT AUTO_INCREMENT PRIMARY KEY,
        libelle_type_telephone VARCHAR(50) NOT NULL
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO type_telephone (libelle_type_telephone) VALUES
    ('Smartphone'),
    ('Feature Phone'),
    ('Phablet'),
    ('Téléphone pliable')
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE couleur (
        id_couleur INT AUTO_INCREMENT PRIMARY KEY,
        libelle_couleur VARCHAR(50) NOT NULL
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO couleur (libelle_couleur) VALUES
    ('Noir'),
    ('Blanc'),
    ('Bleu'),
    ('Rouge'),
    ('Vert'),
    ('Gris')
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE telephone (
        id_telephone INT AUTO_INCREMENT PRIMARY KEY,
        nom_telephone VARCHAR(100) NOT NULL,
        poids DECIMAL(5,2),
        taille VARCHAR(50),
        prix_telephone DECIMAL(8,2),
        couleur_id INT NOT NULL,
        type_telephone_id INT NOT NULL,
        fournisseur VARCHAR(100),
        marque VARCHAR(100),
        photo VARCHAR(255),
        stock INT DEFAULT 0,
        FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur),
        FOREIGN KEY (type_telephone_id) REFERENCES type_telephone(id_type_telephone)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO telephone (nom_telephone, poids, taille, prix_telephone, couleur_id, type_telephone_id, fournisseur, marque, photo, stock) VALUES
    ('Galaxy S21', 169.0, '151.7 x 71.2 x 7.9 mm', 799.99, 6, 1, 'Samsung', 'Samsung', 'galaxyS21gris.png', 10),
    ('Galaxy S21', 169.0, '151.7 x 71.2 x 7.9 mm', 799.99, 1, 1, 'Samsung', 'Samsung', 'galaxyS21lavande.png', 7),
    ('iPhone 13', 174.0, '146.7 x 71.5 x 7.7 mm', 899.99, 1, 1, 'Apple', 'Apple', 'iphone13rouge.png', 15),
    ('iPhone 13', 174.0, '146.7 x 71.5 x 7.7 mm', 899.99, 2, 1, 'Apple', 'Apple', 'iphone13rose.png', 8),
    ('Nokia 3310', 133.0, '115.6 x 51.0 x 12.8 mm', 59.99, 1, 2, 'Nokia', 'Nokia', 'nokia3310gris.png', 20),
    ('Redmi Note 10 Pro', 178.8, '160.5 x 74.5 x 8.3 mm', 199.99, 3, 1, 'Xiaomi', 'Xiaomi', 'redmipro.png', 25),
    ('Motorola Razr', 205.0, '172.0 x 72.6 x 6.9 mm', 1399.99, 5, 4, 'Motorola', 'Motorola', 'motorolarouge.png', 5),
    ('Pixel 6', 207.0, '158.6 x 74.8 x 8.9 mm', 599.99, 6, 1, 'Google', 'Google', 'pixel6gris.png', 12),
    ('Sony Xperia 10', 162.0, '154.0 x 68.0 x 8.4 mm', 349.99, 3, 1, 'Sony', 'Sony', 'sonyrose.png', 8),
    ('OnePlus Nord', 184.0, '158.3 x 73.3 x 8.2 mm', 399.99, 4, 1, 'OnePlus', 'OnePlus', 'oneplusbleu.png', 18),
    ('Asus ROG Phone 5', 238.0, '173.0 x 77.0 x 9.6 mm', 999.99, 1, 3, 'Asus', 'Asus', 'asus.png', 7),
    ('Huawei P40', 175.0, '148.9 x 71.1 x 8.5 mm', 799.99, 2, 1, 'Huawei', 'Huawei', 'huawei.png', 10),
    ('LG Velvet', 180.0, '167.1 x 74.1 x 7.9 mm', 599.99, 6, 1, 'LG', 'LG', 'lgvelvetblanc.png', 13),
    ('Realme GT', 186.0, '158.5 x 73.3 x 8.4 mm', 449.99, 5, 1, 'Realme', 'Realme', 'realme.png', 20),
    ('Oppo Find X3', 193.0, '160.0 x 74.0 x 8.3 mm', 699.99, 4, 1, 'Oppo', 'Oppo', 'opponoir.png', 11)
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande (
        id_commande INT AUTO_INCREMENT PRIMARY KEY,
        date_achat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        utilisateur_id INT NOT NULL,
        etat_id INT NOT NULL,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO commande (date_achat, utilisateur_id, etat_id) VALUES
    ('2025-01-15 10:30:00', 2, 1),
    ('2025-01-20 14:45:00', 3, 2),
    ('2025-01-22 09:15:00', 2, 3),
    ('2025-01-25 16:20:00', 3, 4)
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_commande (
        commande_id INT NOT NULL,
        telephone_id INT NOT NULL,
        prix DECIMAL(8,2) NOT NULL,
        quantite INT NOT NULL,
        PRIMARY KEY (commande_id, telephone_id),
        FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_commande (commande_id, telephone_id, prix, quantite) VALUES
    (1, 1, 799.99, 1),
    (1, 5, 59.99, 2),
    (2, 3, 899.99, 1),
    (3, 6, 199.99, 2),
    (3, 10, 399.99, 1),
    (4, 7, 1399.99, 1)
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_panier (
        id_ligne_panier INT AUTO_INCREMENT PRIMARY KEY,
        utilisateur_id INT NOT NULL,
        telephone_id INT NOT NULL,
        quantite INT NOT NULL,
        date_ajout DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_panier (utilisateur_id, telephone_id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_panier (utilisateur_id, telephone_id, quantite, date_ajout) VALUES
    (2, 8, 1, '2025-01-28 15:30:00'),
    (3, 9, 1, '2025-01-29 10:00:00'),
    (3, 11, 2, '2025-01-29 09:45:00')
    '''
    mycursor.execute(sql)

    get_db().commit()

    flash('Base de données réinitialisée avec succès !', 'alert-success')
    return redirect('/')
