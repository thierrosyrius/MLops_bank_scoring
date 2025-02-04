import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Load trained model
model = pickle.load(open('model/lgbm_model.pkl', 'rb'))

def run():
    st.title("Application de prédiction de l'état d'un prêt")
    img = Image.open('logo.jpg')
    img = img.resize((156, 145))
    st.image(img, use_column_width=False)
    
    st.subheader("Saisir les détails de la demande de prêt:")
    
    # Input fields
    no_of_dependents = st.selectbox("no_of_dependents", [0, 1, 2, 3, 4, 5])
    income_annum = st.number_input("Annual Income ($)", value=0)
    loan_amount = st.number_input("Loan Amount ($)", value=0)
    loan_term = st.selectbox("Loan Term (Months)", [12, 24, 36, 48, 60, 72])
    cibil_score = st.number_input("CIBIL Score (300-900)", min_value=300, max_value=900, value=500)
    residential_assets = st.number_input("Residential Assets Value ($)", value=0)
    commercial_assets = st.number_input("Commercial Assets Value ($)", value=0)
    luxury_assets = st.number_input("Luxury Assets Value ($)", value=0)
    bank_assets = st.number_input("Bank Asset Value ($)", value=0)
    
    education = st.selectbox("Education", ['Not Graduate', 'Graduate'])
    self_employed = st.selectbox("Self Employed", ['No', 'Yes'])
    
    # Encoding categorical values
    education = 1 if education == 'Graduate' else 0
    self_employed = 1 if self_employed == 'Yes' else 0
    
    if st.button("Predict Loan Status"):
        features = np.array([[no_of_dependents, income_annum, loan_amount, loan_term, cibil_score, 
                              residential_assets, commercial_assets, luxury_assets, 
                              bank_assets, education, self_employed]])
        
        prediction = model.predict(features)
        
        if prediction[0] == 1:
            st.success("✅  Nous vous félicitons ! Votre prêt a toutes les chances d'être approuvé.")
        else:
            st.error("❌ Désolé, votre demande de prêt peut être rejetée.")

if __name__ == '__main__':
    run()
