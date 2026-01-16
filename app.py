import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="IoT23 Intrusion Detection", layout="wide")

st.title("🔐 IoT23 – Détection d’Intrusions (Hiérarchique)")
st.markdown("""
Ce modèle fonctionne en **2 étapes** :
1. Détection : Benign vs Attaque
2. Classification du type d’attaque
""")

# ============================
# CHARGEMENT DES MODÈLES
# ============================
@st.cache_resource
def load_models():
    model_stage1 = joblib.load("models/attack_classifier.joblib")
    model_stage2 = joblib.load("models/attack_detector.joblib")
    le_attacks = joblib.load("models/label_encoder_attack.joblib")
    return model_stage1, model_stage2, le_attacks

model_1, model_2, le_attacks = load_models()

st.success("✅ Modèles chargés avec succès")

# ============================
# UPLOAD CSV
# ============================
uploaded_file = st.file_uploader(
    "📤 Charger un fichier CSV de flux réseau",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Aperçu des données")
    st.dataframe(df.head())

    # ============================
    # PRÉPROCESSING MINIMAL
    # ============================
    cat_cols = ['proto', 'service', 'conn_state']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes

    # Colonnes à retirer si présentes
    drop_cols = ['label', 'id.orig_h', 'history']
    df_model = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # ============================
    # PRÉDICTION ÉTAPE 1
    # ============================
    st.subheader("🧠 Prédiction")

    y_pred_stage1 = model_1.predict(df_model)

    df_results = df.copy()
    df_results["stage1_prediction"] = y_pred_stage1
    df_results["stage1_label"] = df_results["stage1_prediction"].map({
        0: "Benign",
        1: "Attaque"
    })

    # ============================
    # PRÉDICTION ÉTAPE 2
    # ============================
    attack_mask = df_results["stage1_prediction"] == 1
    X_attacks = df_model.loc[attack_mask]

    if len(X_attacks) > 0:
        y_pred_stage2 = model_2.predict(X_attacks)
        attack_labels = le_attacks.inverse_transform(y_pred_stage2)

        df_results.loc[attack_mask, "attack_type"] = attack_labels
    else:
        df_results["attack_type"] = None

    # ============================
    # AFFICHAGE
    # ============================
    st.subheader("📊 Résultats")
    st.dataframe(df_results[[
        "stage1_label", "attack_type"
    ]].value_counts().reset_index(name="count"))

    st.subheader("📄 Détails par flux")
    st.dataframe(df_results.head(100))

    # ============================
    # TÉLÉCHARGEMENT
    # ============================
    csv = df_results.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Télécharger les prédictions",
        csv,
        "predictions_iot23.csv",
        "text/csv"
    )
