# 🛡️ IDS pour l'IoT : Détection d'Intrusions (Dataset IoT-23)

Ce projet propose une solution complète de détection d'intrusions pour les réseaux IoT, utilisant le Machine Learning pour identifier et classifier les menaces en temps réel.

## 📌 Présentation du Projet
L'objectif est de sécuriser les environnements IoT en analysant les flux réseaux. Le système repose sur une **architecture hiérarchique** :
1.  **Stage 1 (Détecteur) :** Filtre le trafic pour séparer le flux bénin des attaques (Rappel > 97%).
2.  **Stage 2 (Classifieur) :** Identifie la famille spécifique de l'attaque (C&C, DDoS, PortScan, etc.).

## 🚀 Fonctionnalités clés
* **Analyse de flux :** Prétraitement automatisé des logs réseaux.
* **Modèles performants :** Utilisation de Random Forest optimisés pour le déséquilibre des classes.
* **Interface Web :** Dashboard interactif avec **Streamlit** pour tester des fichiers de logs.
* **Conteneurisation :** Déploiement simplifié via **Docker**.

## 📁 Structure du dépôt
* `app.py` : Code de l'application Streamlit.
* `models/` : Modèles entraînés et sérialisés (.joblib).
* `notebooks/` : Travaux de recherche, EDA et entraînement des modèles.
* `src/` : Scripts de prétraitement et fonctions d'inférence.
* `data/` : Contient `sample_test.csv` pour tester l'outil.
* `Dockerfile` : Configuration pour la création de l'image Docker.

## 🛠️ Installation et Utilisation

### Via Docker (Méthode recommandée)
Pour lancer l'application sans installer de dépendances Python :
```bash
# Construction de l'image
docker build -t ids-iot-app .

# Lancement du conteneur
docker run -p 8501:8501 ids-iot-app