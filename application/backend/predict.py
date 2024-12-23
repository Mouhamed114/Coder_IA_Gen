from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd  # N'oubliez pas d'importer pandas

# Créer l'application Flask
app = Flask(__name__)

# Charger le modèle une seule fois au démarrage de l'application
try:
    with open('backend/pipeline.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Le fichier 'pipeline.pkl' est introuvable dans le répertoire 'backend'.")

# Route d'accueil simple
@app.route('/')
def home():
    return "Bienvenue sur l'API Flask pour prédiction !"

# Route pour effectuer une prédiction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données envoyées en JSON
        data = request.get_json()

        # Vérifier que les clés nécessaires sont présentes
        expected_keys = ['Quality1', 'Quality2', 'Quality3', 'Small Bags', 'Large Bags', 'XLarge Bags', 'year', 'type', 'region']
        if not all(key in data for key in expected_keys):
            return jsonify({'error': f'Les clés nécessaires sont manquantes. Attendu : {expected_keys}'}), 400

        # Convertir les caractéristiques en DataFrame pour le modèle
        input_data = pd.DataFrame([data])  # [data] crée une ligne à partir des données

        # Faire une prédiction
        prediction = model.predict(input_data)

        return jsonify({"prediction": float(prediction[0])}), 200

    except Exception as e:
        return jsonify({'error': f"Erreur lors de la prédiction : {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
