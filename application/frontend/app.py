import streamlit as st
import requests

# URL de l'API Flask
API_URL = "http://127.0.0.1:5000/predict"

# Titre de l'application
st.title("Prédiction du Prix des Avocats")

# Formulaire pour saisir les données
st.sidebar.header("Saisir les Caractéristiques")
quality1 = st.sidebar.number_input("Quality1", min_value=0.0, step=0.1)
quality2 = st.sidebar.number_input("Quality2", min_value=0.0, step=0.1)
quality3 = st.sidebar.number_input("Quality3", min_value=0.0, step=0.1)
small_bags = st.sidebar.number_input("Small Bags", min_value=0.0, step=0.1)
large_bags = st.sidebar.number_input("Large Bags", min_value=0.0, step=0.1)
xlarge_bags = st.sidebar.number_input("XLarge Bags", min_value=0.0, step=0.1)
type_ = st.sidebar.selectbox("Type (0 ou 1)", [0, 1])
year = st.sidebar.number_input("Year", min_value=2000, max_value=2030, step=1)
region = st.sidebar.number_input("Region (numérique)", min_value=0, step=1)

# Bouton pour effectuer la prédiction
if st.sidebar.button("Prédire"):
    # Construire les données pour l'API
    data = {
        "Quality1": quality1,
        "Quality2": quality2,
        "Quality3": quality3,
        "Small Bags": small_bags,
        "Large Bags": large_bags,
        "XLarge Bags": xlarge_bags,
        "type": type_,
        "year": year,
        "region": region
    }

    # Appeler l'API Flask
    try:
        response = requests.post(API_URL, json=data)
        response_data = response.json()

        if response.status_code == 200:
            prediction = response_data.get("prediction", "Erreur inconnue")
            st.success(f"Le prix prédit des avocats est : {prediction:.2f} $")
        else:
            st.error(f"Erreur : {response_data.get('error', 'Erreur inconnue')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API : {e}")
