from flask import Flask, render_template, request
import mysql.connector as mariadb
import pandas as pd
import pickle
import matplotlib.image as mpimg
import base64



app = Flask(__name__)



# Index
@app.route("/")
def home():
    return render_template("pages/index.html")


# Exo 1
@app.route("/exo1")
def exo1():
    message = "Hello World !"
    return render_template("pages/exo1/exo1.html", message=message)


# Exo 2
@app.route("/exo2")
def exo2():
    message = "Hello World !"
    return render_template("pages/exo2/exo2.html", message=message)


# Exo 3
@app.route("/exo3")
def exo3():
    return render_template("pages/exo3/index.html")

@app.route("/exo3/page2")
def exo3_page2():
    return render_template("pages/exo3/page2.html")


# Exo 4
@app.route("/exo4")
def exo4():
    return render_template("pages/exo4/index.html")

@app.route("/exo4/page2", methods=["POST"])
def exo4_page2():
    data = dict(nom = request.form["nom"],
                prenom = request.form["prenom"],
                sexe = request.form["sexe"],
                pseudo = request.form["pseudo"])

    return render_template("pages/exo4/page2.html", data=data)


# Exo 5
@app.route("/exo5")
def exo5():
    return render_template("pages/exo5/index.html")


@app.route("/exo5/confirm", methods=["POST"])
def exo5_confirm():
    # Récupération des données
    data = {"nom" : request.form["nom"],
            "prenom" : request.form["prenom"],
            "sexe" : request.form["sexe"],
            "pseudo" : request.form["pseudo"]}

    # Connection à la base de données
    db_connect = mariadb.connect(host="172.19.0.2", user="root", password="root", database="docker_test")
    cursor = db_connect.cursor()

    # Vérification des doublons
    cursor.execute("SELECT * FROM users WHERE prenom = '{}' AND nom = '{}' AND sexe = '{}' AND pseudo = '{}'".format(data["prenom"], data["nom"], data["sexe"], data["pseudo"]))
    test = cursor.fetchone()
    if test :
        return render_template("pages/index.html", message="Vous êtes déjà enregistré !")

    # Insertion des infos dans la base
    cursor.execute("INSERT INTO users (prenom, nom, sexe, pseudo) VALUES ('{}', '{}', '{}', '{}')".format(data["prenom"], data["nom"], data["sexe"], data["pseudo"]))
    db_connect.commit()

    cursor.close()
    db_connect.close()

    return render_template("pages/exo5/page2.html", data=data)


# Exo6
@app.route("/exo6")
def exo6():
    # Connection à la base de données
    db_connect = mariadb.connect(host="172.19.0.2", user="root", password="root", database="docker_test")
    cursor = db_connect.cursor()

    cursor.execute("SELECT * FROM users")
    
    membres = []
    for x in cursor:
        dico = {"id" : x[0],
                "prenom": x[1],
                "nom": x[2],
                "sexe" : x[3],
                "pseudo": x[4]}
        membres.append(dico)

    cursor.close()
    db_connect.close()

    return render_template("pages/exo6/membres.html", membres=membres)


# Exo 7
@app.route("/exo7")
def exo7():
    return render_template("pages/exo7/stat.html")


@app.route("/exo7/analise", methods=["POST"])
def exo7_analise():
    fichier = request.files.get("dataset")
   
    # TODO Recupérer le séparateur grâce à des Regex
    sep = request.form["sep"]

    # TODO Extraire le nom du fichier grâce à des Regex
    name = str(fichier)[15:-15]

    df = pd.read_csv(fichier, sep=sep)
    describ = round(df.describe(),2)

    dico = {}
    for x in describ:
        dico[x] = describ[x].to_dict()

    a = list(dico.keys())[0]
    entete = list(dico[a].keys())

    return render_template("pages/exo7/stat.html", name=name, entete=entete, data=dico)


# Exo 8
@app.route("/exo8", methods=["GET", "POST"])
def exo8():
    # Récupération du modèle
    with open("/src/modele", "rb") as f:
        depik = pickle.Unpickler(f)
        model = depik.load()
    
    # Récupération de l'image
    image = request.files.get("image")

    # Traitement de l'image
    if image:
        base64img = "data:image/png;base64," + base64.b64encode(image.getvalue()).decode('ascii')

        # vrai = image.filename[0] # Pour les tests le nom du fichier
        vrai = request.form["vrai"]
        image = mpimg.imread(image)
        # Conversion 3D -> 2D
        # image = image[:,:,0]
        image = image.reshape(1,784)

        # Predire un résultat
        prediction = model.predict(image)[0]
    else:
        prediction = "Rien à prédire"
        vrai = "Aucun fichier"
        base64img = ""

    if str(vrai) in ["--", "Aucun fichier"]:
        valid = "text-light"
    elif str(prediction) == str(vrai):
        valid = "text-success"
    else:
        valid = "text-danger"

    return render_template("pages/exo8/index.html", prediction=prediction, vrai=vrai, image=base64img, valid=valid)


# Corobot
@app.route("/corobot")
def corobot():
    return render_template("pages/corobot/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)