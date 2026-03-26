from fpdf import FPDF

FONT_REG  = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"
FONT_ITAL = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Italic.ttf"
FONT_BI   = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-BoldItalic.ttf"

class PDF(FPDF):
    def setup_fonts(self):
        self.add_font("JB", "",  FONT_REG)
        self.add_font("JB", "B", FONT_BOLD)
        self.add_font("JB", "I", FONT_ITAL)
        self.add_font("JB", "BI", FONT_BI)

    def header(self):
        self.set_fill_color(30, 30, 50)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font("JB", "B", 11)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 10, "SAE 2.04 - Rapport d'analyse des bugs", align="C")
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font("JB", "I", 7)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Analyse du 26/03/2026  |  Page {self.page_no()}", align="C")

    def section_title(self, title, color=(40, 80, 160)):
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font("JB", "B", 10)
        self.cell(0, 8, f"  {title}", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def subsection_title(self, title):
        self.set_font("JB", "B", 9)
        self.set_text_color(40, 80, 160)
        self.cell(0, 6, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def severity_badge(self, sev):
        colors = {
            "CRITIQUE": (200, 30, 30),
            "HAUTE":    (220, 100, 0),
            "MOYENNE":  (180, 150, 0),
            "BASSE":    (60, 140, 60),
            "BLOCKER":  (120, 0, 120),
        }
        c = colors.get(sev, (100, 100, 100))
        self.set_fill_color(*c)
        self.set_text_color(255, 255, 255)
        self.set_font("JB", "B", 6)
        self.cell(18, 5, sev, fill=True, align="C")
        self.set_text_color(0, 0, 0)

    def row(self, sev, description, fichier, ligne):
        x = self.get_x()
        y = self.get_y()
        self.severity_badge(sev)
        self.set_x(x + 20)
        self.set_font("JB", "", 7.5)
        self.multi_cell(103, 5, description, border=0)
        h = self.get_y() - y
        self.set_xy(x + 125, y)
        self.set_font("JB", "I", 7)
        self.set_text_color(80, 80, 80)
        self.multi_cell(52, 5, fichier, border=0)
        self.set_xy(x + 178, y)
        self.set_font("JB", "", 7.5)
        self.set_text_color(0, 0, 0)
        self.cell(15, h, ligne, border=0, align="C")
        self.set_y(y + max(h, 5))
        self.set_draw_color(210, 210, 210)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(1)

    def table_header(self):
        self.set_fill_color(220, 230, 245)
        self.set_font("JB", "B", 8)
        self.cell(20, 6, "Severite", fill=True, align="C")
        self.cell(105, 6, "Erreur / Description", fill=True)
        self.cell(50, 6, "Fichier", fill=True)
        self.cell(17, 6, "Ligne", fill=True, align="C")
        self.ln()


pdf = PDF()
pdf.setup_fonts()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# PAGE DE GARDE
pdf.set_y(55)
pdf.set_font("JB", "B", 20)
pdf.set_text_color(30, 30, 50)
pdf.cell(0, 12, "Rapport d'Analyse des Bugs", align="C", ln=True)
pdf.set_font("JB", "B", 13)
pdf.set_text_color(40, 80, 160)
pdf.cell(0, 10, "SAE 2.04 - Application e-commerce telephones", align="C", ln=True)
pdf.ln(6)
pdf.set_font("JB", "", 10)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, "Analyse n°1  |  Date : 26/03/2026", align="C", ln=True)
pdf.ln(10)
pdf.set_draw_color(40, 80, 160)
pdf.set_line_width(0.8)
pdf.line(30, pdf.get_y(), 180, pdf.get_y())
pdf.ln(10)
pdf.set_font("JB", "", 9)
pdf.set_text_color(60, 60, 60)
pdf.multi_cell(0, 6,
    "Ce rapport presente les resultats d'une analyse statique complete du projet\n"
    "realisee par 4 agents specialises couvrant le backend, le frontend,\n"
    "la base de donnees et les liens entre les couches.\n"
    "Les erreurs sont classees par severite.",
    align="C")
pdf.ln(12)
pdf.set_font("JB", "B", 9)
pdf.set_text_color(30, 30, 50)
# Tableau recap
recap = [
    ("Backend",             "11 critiques  |  6 hautes  |  6 moyennes  |  4 basses"),
    ("Frontend",            "3 critiques (ressources manquantes)  |  8 hautes  |  15+ moyennes"),
    ("Base de donnees",     "3 critiques  |  7 hautes/moyennes  |  tables manquantes"),
    ("Liens inter-couches", "7 desalignements critiques entre frontend / backend / BD"),
]
for cat, detail in recap:
    pdf.set_fill_color(245, 247, 252)
    pdf.cell(48, 7, cat, fill=True, border=1)
    pdf.set_font("JB", "", 8)
    pdf.cell(0, 7, detail, border=1, ln=True)
    pdf.set_font("JB", "B", 9)
pdf.set_text_color(0, 0, 0)

# ── BACKEND ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title("1. BACKEND (Flask / Python)")
pdf.subsection_title("Erreurs critiques")
pdf.table_header()

backend_critical = [
    ("CRITIQUE", "Identifiants MySQL en dur (user=root, password=secret)", "connexion_db.py", "8-10"),
    ("CRITIQUE", "Secret key Flask triviale et previsible", "app.py", "24"),
    ("CRITIQUE", "Mode debug=True actif (expose traceback + console interactive)", "app.py", "102"),
    ("CRITIQUE", "Route /base/init non protegee - reinitialise toute la BD sans auth", "fixtures_load.py", "12"),
    ("CRITIQUE", "IDOR : un client peut voir les commandes d'un autre utilisateur", "client_commande.py", "136-150"),
    ("CRITIQUE", "mycursor.execute(sql, commande_id) - string au lieu de tuple -> crash", "admin_commande.py", "69"),
    ("CRITIQUE", "client_historique_add() brisee (SQL vide, parametre reassigne en interne)", "client_liste_envies.py", "40-50"),
    ("CRITIQUE", "SQL vides dans client_commentaire.py : toutes les routes commentaires/notes", "client_commentaire.py", "60-129"),
    ("CRITIQUE", "SQL vides dans client_coordonnee.py : aucune logique adresse implementee", "client_coordonnee.py", "12-100"),
    ("CRITIQUE", "SQL vides dans admin_commentaire.py et admin_type_telephone.py", "admin_*.py", "-"),
    ("CRITIQUE", "SQL vides dans admin_declinaison_telephone.py (4 routes vides)", "admin_declinaison.py", "12-81"),
]
for r in backend_critical:
    pdf.row(*r)

pdf.ln(3)
pdf.subsection_title("Erreurs hautes")
pdf.table_header()
backend_high = [
    ("HAUTE", "Stock decremente a l'ajout panier (pas a la commande) - double vente possible", "client_panier.py", "59-64"),
    ("HAUTE", "Race condition sur le stock entre lecture et decrementation", "client_panier.py", "23-64"),
    ("HAUTE", "int(request.form.get('quantite')) sans try/except -> crash si valeur invalide", "client_panier.py", "17"),
    ("HAUTE", "Routes add/delete liste envies en methode GET au lieu de POST", "client_liste_envies.py", "12,19,26"),
    ("HAUTE", "Suppression commentaires sans verif que ca appartient a l'utilisateur", "client_commentaire.py", "81-91"),
    ("HAUTE", "Pas de validation des entrees (prix, stock, IDs non verifies comme numeriques)", "admin_telephone.py", "71-79"),
]
for r in backend_high:
    pdf.row(*r)

# ── FRONTEND ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title("2. FRONTEND (HTML / CSS / Jinja2)")
pdf.subsection_title("Ressources manquantes (critiques)")
pdf.table_header()
frontend_critical = [
    ("CRITIQUE", "perso_admin.js reference mais fichier inexistant -> erreur 404 console", "layout_admin.html", "25"),
    ("CRITIQUE", "star_rating.css reference mais fichier inexistant -> styles etoiles absents", "telephone_details.html", "4"),
    ("CRITIQUE", "Fonction loadFile() appelee via onchange mais non definie nulle part", "add/edit_telephone.html", "20,35"),
]
for r in frontend_critical:
    pdf.row(*r)

pdf.ln(3)
pdf.subsection_title("Erreurs hautes")
pdf.table_header()
frontend_high = [
    ("HAUTE", "Formulaires imbriques <form> dans <form> (HTML invalide - donnees non soumises)", "telephone_details.html", "100-110"),
    ("HAUTE", "<stong> au lieu de <strong> - balise non reconnue, style non applique", "declinaison_telephone.html", "28"),
    ("HAUTE", "{{ commentaire.__dict__ }} affiche en production - expose internes Python", "show_avis.html", "48"),
    ("HAUTE", "Filtre | safe sur donnees non validees (labels, values) -> XSS potentiel", "dataviz_etat_1.html", "72,76"),
    ("HAUTE", "Attribut value sur <input type='file'> - inoperant pour des raisons de securite", "edit_telephone.html", "35"),
    ("HAUTE", "minlength/maxlength sur <input type='number'> - attributs invalides (utiliser min/max)", "add_adresse.html", "21"),
    ("HAUTE", "Classe form-select appliquee sur <input type='text'> (destine aux <select>)", "add_type_article.html", "17"),
    ("HAUTE", "Champ email avec type='text' au lieu de type='email' - pas de validation HTML5", "signup.html", "22"),
]
for r in frontend_high:
    pdf.row(*r)

pdf.ln(3)
pdf.subsection_title("Erreurs moyennes (selection)")
pdf.table_header()
frontend_med = [
    ("MOYENNE", "Labels sans attribut for ou for ne correspondant a aucun id d'input", "signup.html", "18-24"),
    ("MOYENNE", "Lien 'Mot de passe oublie' avec href='' - ne mene nulle part", "_nav.html", "27"),
    ("MOYENNE", "Dropdown-toggle sur <a href='#'> au lieu d'un <button> (semantique incorrecte)", "_nav_*.html", "8,16"),
    ("MOYENNE", "CSS : br { color: blue; } - br est vide, la couleur n'a aucun effet", "mes_styles.css", "3"),
    ("MOYENNE", "type='button' sur des elements <a> - attribut invalide sur les liens", "_nav_*.html", "17-24"),
    ("MOYENNE", "Code commente en masse (40+ lignes Bulma) laisse en production", "login.html", "40-69"),
]
for r in frontend_med:
    pdf.row(*r)

# ── BASE DE DONNEES ───────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title("3. BASE DE DONNEES (MySQL)")
pdf.subsection_title("Erreurs critiques de schema")
pdf.table_header()
db_critical = [
    ("CRITIQUE", "Colonne id_ligne_panier absente du schema mais utilisee partout dans le code", "sae_sql.sql.txt", "78-86"),
    ("CRITIQUE", "Tables entieres manquantes : commentaire, note, historique, adresse, fournisseur, marque", "sae_sql.sql.txt", "-"),
    ("CRITIQUE", "Aucune transaction lors de la creation de commande - donnees partielles en cas d'erreur", "client_commande.py", "79-103"),
]
for r in db_critical:
    pdf.row(*r)

pdf.ln(3)
pdf.subsection_title("Erreurs hautes et moyennes")
pdf.table_header()
db_high = [
    ("HAUTE", "Aucun index sur les 8 colonnes de cles etrangeres - JOINs tres lents", "sae_sql.sql.txt", "43-86"),
    ("HAUTE", "Stock decremente a l'ajout panier et non a la commande - incoherence metier", "client_panier.py", "59-64"),
    ("HAUTE", "Pas de contrainte CHECK (stock >= 0) ni CHECK (quantite > 0) - valeurs negatives", "sae_sql.sql.txt", "54,72,81"),
    ("MOYENNE", "nom dans utilisateur sans NOT NULL - valeur NULL acceptee", "sae_sql.sql.txt", "22-23"),
    ("MOYENNE", "Pas de contrainte UNIQUE sur libelle dans etat, couleur, type_telephone", "sae_sql.sql.txt", "30,35,40"),
    ("MOYENNE", "marque et fournisseur en VARCHAR dans telephone au lieu de FK vers tables dediees", "sae_sql.sql.txt", "51-52"),
    ("MOYENNE", "poids DECIMAL(5,2) - max 999.99g, insuffisant pour certains appareils", "sae_sql.sql.txt", "46"),
    ("MOYENNE", "Normalisation : meme modele duplique par couleur, stock duplique par variante", "sae_sql.sql.txt", "119-134"),
]
for r in db_high:
    pdf.row(*r)

# ── LIENS ENTRE COUCHES ───────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title("4. LIENS ENTRE COUCHES (desalignements Frontend / Backend / BD)")
pdf.table_header()

links = [
    ("CRITIQUE", "Formulaire envoie 'idCommande' (camelCase) mais backend attend 'id_commande' -> None", "show.html:50 / admin_commande.py:62", "50/62"),
    ("CRITIQUE", "Template accede telephone_commande[0].id - cle inexistante dans le dict SQL", "show.html:50 / admin_commande.py:42", "50/42"),
    ("CRITIQUE", "URL /client/telephone/details/123 (path) mais route attend ?id_article=123 -> 404", "panier_telephone.html:36 / client_commentaire.py:14", "36/14"),
    ("CRITIQUE", "Template affiche commande.nbr_telephones mais SQL retourne nbr_articles (3 noms!)", "show.html:71 / client_commande.py:119", "71/119"),
    ("CRITIQUE", "SELECT id_ligne_panier dans le code mais colonne absente de la table ligne_panier", "_panier.html:47 / client_panier.py:32+", "47/32+"),
    ("CRITIQUE", "declinaison_telephone.html envoie ?id_telephone= mais backend attend ?id_article=", "declinaison_telephone.html:9 / client_commentaire.py:14", "9/14"),
    ("HAUTE",    "SELECT types sans alias AS libelle mais template accede type.libelle -> dropdown vide", "add_telephone.html:27 / admin_telephone.py:53", "27/53"),
]
for sev, desc, fichier, ligne in links:
    pdf.row(sev, desc, fichier, ligne)

pdf.ln(6)
pdf.section_title("5. PRIORITES DE CORRECTION", color=(140, 30, 30))
pdf.ln(2)

priorities = [
    ("1 - IMMEDIAT", "Ajouter id_ligne_panier AUTO_INCREMENT a ligne_panier OU revoir la logique (PK composite)"),
    ("2 - IMMEDIAT", "Corriger idCommande -> id_commande dans le template admin des commandes"),
    ("3 - IMMEDIAT", "Uniformiser les URLs /client/telephone/details (path param vs query param)"),
    ("4 - IMMEDIAT", "Creer les tables manquantes (commentaire, adresse, etc.) et implementer les SQL vides"),
    ("5 - URGENT",   "Deplacer la decrementation du stock de l'ajout panier vers la creation de commande"),
    ("6 - URGENT",   "Ajouter les transactions SQL sur la creation de commande (BEGIN / ROLLBACK / COMMIT)"),
    ("7 - URGENT",   "Creer les fichiers JS/CSS manquants (perso_admin.js, star_rating.css, loadFile())"),
    ("8 - SECURITE", "Sortir les identifiants BD dans des variables d'environnement (.env)"),
    ("9 - SECURITE", "Changer la secret_key Flask pour une valeur aleatoire forte"),
    ("10 - SECURITE","Desactiver debug=True et proteger la route /base/init par un role admin"),
]
pdf.set_font("JB", "B", 8)
for num, txt in priorities:
    pdf.set_fill_color(245, 247, 252)
    pdf.cell(30, 6, num, fill=True, border=1)
    pdf.set_font("JB", "", 8)
    pdf.cell(0, 6, txt, border=1, ln=True)
    pdf.set_font("JB", "B", 8)

pdf.ln(8)
pdf.set_font("JB", "I", 7)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 5, "Rapport genere automatiquement par analyse statique multi-agents - SAE 2.04 - 26/03/2026", align="C")

output_path = "/home/Dylan/BUT/S2/sae/sae2.04/Report_bug/Analyse_1_26-03-26.pdf"
pdf.output(output_path)
print(f"PDF genere : {output_path}")
