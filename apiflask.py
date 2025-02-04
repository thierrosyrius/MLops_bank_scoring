from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Charger le modèle
with open("model/lgbm_model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()  # Données envoyées par l'application
    features = np.array(data["features"]).reshape(1, -1)  # Adapter les données
    prediction = model.predict(features)  # Faire une prédiction
    result = "Approbation" if prediction[0] == 1 else "Rejet"
    
    return jsonify({"decision": result})

if __name__ == "__main__":
    app.run(debug=True)
