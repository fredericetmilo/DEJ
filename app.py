from flask import Flask, render_template, request

app = Flask(__name__)

# ------------------------------
# TABLE DES METS PAR ACTIVITÉ
# (valeurs issues de ton fichier Excel)
# ------------------------------
met_sport = {
    "Aviron": 8.5,
    "Badminton": 4.5,
    "Basketball": 6,
    "Corde à sauter": 9,
    "Crossfit": 9,
    "Danse": 7,
    "Équitation": 4,
    "Escalade (temps de montée)": 10,
    "Escrime": 6,
    "Fitness (cours collectifs)": 8,
    "Football": 9,
    "Golf": 4,
    "Gymnastique": 4,
    "Handball": 8,
    "Hockey sur glace": 9,
    "Jogging (cross)": 9,
    "Jogging / marche": 6,
    "Jogging à 13 km/h (4,5 min/km)": 13.5,
    "Jogging à 8 km/h (7 min/km)": 8,
    "Jogging à 9,5 km/h (6 min/km)": 10,
    "Jogging sur tapis": 8,
    "Kayak": 6,
    "Marche": 3,
    "Marche (+5,5 km/h)": 4,
    "Marche (competition)": 6.5,
    "Moto": 2.5,
    "Musculation": 3,
    "Natation (intensité modérée à élevée)": 9,
    "Natation récréative": 6,
    "Paddle": 4,
    "Patinage": 5.5,
    "Patinage (competition)": 15,
    "Plongée sous-marine": 7,
    "Raquette à neige": 8,
    "Rugby": 10,
    "Skateboard": 5,
    "Ski alpin": 6,
    "Ski alpin (competition)": 8,
    "Ski de fond / skating": 8,
    "Ski de randonnée": 8,
    "Sports de combats": 10,
    "Squash": 8,
    "Taï-chi": 4,
    "Tennis": 7,
    "Tennis de table": 7,
    "Vélo (+30 km/h)": 14,
    "Vélo (19 à 22km/h)": 7,
    "Vélo (22 à 26 km/h)": 10,
    "Vélo (promenade)": 5,
    "Vélo d'appartement (+200w)": 11,
    "Vélo d'appartement (100w)": 5.5,
    "Vélo d'appartement (150w)": 7,
    "Vélo d'appartement (50w)": 3,
    "Volleyball": 4,
    "Yoga": 3
}

@app.route('/')
def index():
    """Affiche le formulaire principal"""
    return render_template('index.html', met_sport=met_sport)

@app.route('/result', methods=['POST'])
def result():
    """Récupère les données du formulaire et calcule la DEJ"""

    # --- Données de base ---
    sexe = request.form['sexe']
    age = float(request.form['age'])
    taille = float(request.form['taille'])
    poids = float(request.form['poids'])
    activite = request.form['activite']

    # --- Sélection des sports (jusqu’à 3) ---
    sport1 = request.form['sport1']
    duree1 = float(request.form['duree1']) if request.form['duree1'] else 0
    sport2 = request.form['sport2']
    duree2 = float(request.form['duree2']) if request.form['duree2'] else 0
    sport3 = request.form['sport3']
    duree3 = float(request.form['duree3']) if request.form['duree3'] else 0

    # ------------------------------
    # CALCULS
    # ------------------------------

    import math

    # 1️⃣ TMB (formule allométrique de Black et al., 1996)
    if sexe == "Homme":
        facteur = 1.083
    else:
        facteur = 0.963

    tmb = facteur * (poids ** 0.48) * ((taille / 100) ** 0.50) * (age ** -0.13) * (1000 / 4.1855)

    # 2️⃣ Niveau d’activité (NAP)
    nap_dict = {
        "Sédentaire": 1.2,
        "Peu actif": 1.375,
        "Actif": 1.55,
        "Très actif": 1.725,
        "Extrêmement actif": 1.9
    }
    nap = nap_dict.get(activite, 1.55)

    # 3️⃣ Dépense liée au sport (basée sur les MET)
    # Formule : MET × Poids (kg) × Durée (h/semaine) ÷ 7 jours
    depense_sportive_totale = (
        met_sport.get(sport1, 0) * poids * duree1 +
        met_sport.get(sport2, 0) * poids * duree2 +
        met_sport.get(sport3, 0) * poids * duree3
    )
    depense_sportive = depense_sportive_totale / 7

    # 4️⃣ DEJ total
    dej = (tmb * nap) + depense_sportive

    # ------------------------------
    # ENVOI DES RÉSULTATS
    # ------------------------------
    return render_template(
        'result.html',
        sexe=sexe,
        tmb=round(tmb, 1),
        nap=nap,
        depense_sportive=round(depense_sportive, 1),
        dej=round(dej, 1)
    )

if __name__ == '__main__':
    app.run(debug=True)
