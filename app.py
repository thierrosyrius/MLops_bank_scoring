import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Chargement du modèle
try:
    model = pickle.load(open('model/lgbm_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Le fichier du modèle est introuvable. Veuillez vérifier le chemin et le nom du fichier.")
    st.stop()

def run():
    st.title("Application de prédiction de l'état d'un prêt")
    img = Image.open('logo.jpg')
    img = img.resize((156, 145))
    st.image(img, use_column_width=False)
    
    st.subheader("Saisissez les détails de la demande de prêt :")
    
    # Champs de saisie
    no_of_dependents = st.selectbox("Nombre de personnes à charge", [0, 1, 2, 3, 4, 5])
    income_annum = st.number_input("Revenu annuel ($)", min_value=0)
    loan_amount = st.number_input("Montant du prêt ($)", min_value=0)
    loan_term = st.selectbox("Durée du prêt (mois)", [6, 8, 10, 12, 14, 16, 18, 20])
    cibil_score = st.number_input("Score CIBIL (300-900)", min_value=300, max_value=900, value=500)
    residential_assets = st.number_input("Valeur des biens résidentiels ($)", min_value=0)
    commercial_assets = st.number_input("Valeur des biens commerciaux ($)", min_value=0)
    luxury_assets = st.number_input("Valeur des biens de luxe ($)", min_value=0)
    bank_assets = st.number_input("Valeur des actifs bancaires ($)", min_value=0)
    education = st.selectbox("Niveau d'éducation", ['Non diplômé', 'Diplômé'])
    self_employed = st.selectbox("Travailleur indépendant", ['Non', 'Oui'])
    
    # Encodage des variables catégorielles
    education = 1 if education == 'Diplômé' else 0
    self_employed = 1 if self_employed == 'Oui' else 0
    
    # Préparation des caractéristiques pour la prédiction
    features = np.array([[no_of_dependents, income_annum, loan_amount, loan_term, cibil_score, 
                          residential_assets, commercial_assets, luxury_assets, 
                          bank_assets, education, self_employed]])
    
    # Vérification de la forme des caractéristiques
    st.write(f"Forme des caractéristiques d'entrée : {features.shape}")
    
    if st.button("Prédire l'état du prêt"):
        try:
            prediction = model.predict(features)
            if prediction[0] == 1:
                st.success("✅ Nous vous félicitons ! Votre prêt a toutes les chances d'être approuvé.")
            else:
                st.error("❌ Désolé, votre demande de prêt peut être rejetée.")
        except Exception as e:
            st.error(f"Une erreur s'est produite lors de la prédiction : {e}")

if __name__ == '__main__':
    run()
