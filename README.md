# Arepondre

## Description
Arepondre est une application web Flask qui permet d'extraire et d'analyser des questions à partir de requêtes de recherche. Elle utilise l'API SerpAPI pour collecter des données et propose une interface web pour interagir avec le service.

## Structure du Projet
```
Arepondre/
├── templates/               # Templates HTML Flask
├── extract_questions.py     # Module d'extraction de questions
├── main.py                 # Application Flask principale
├── question_collector.py    # Collecteur de questions
├── requirements.txt        # Dépendances Python
└── serpapi_client.py       # Client pour l'API SerpAPI
```

## Prérequis
- Python 3.x
- Compte SerpAPI (pour la clé API)

## Installation
1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd Arepondre
```

2. Créer un environnement virtuel
```bash
python -m venv venv
```

3. Activer l'environnement virtuel
```bash
# Windows
venv\Scripts\activate
```

4. Installer les dépendances
```bash
pip install -r requirements.txt
```

5. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet avec :
```
SERPAPI_API_KEY=votre_clé_api_ici
```

## Utilisation
1. Démarrer le serveur Flask
```bash
python main.py
```
2. Ouvrir un navigateur et accéder à `http://localhost:5000`
3. Entrer une requête de recherche pour extraire les questions associées

## Fonctionnalités
- Interface web pour la saisie de requêtes
- Extraction de questions à partir des résultats de recherche
- Analyse et filtrage des questions pertinentes (bientôt)
- Support multilingue pour la détection des questions (bientôt)

## Contribution
Les contributions sont les bienvenues ! Pour contribuer :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## Licence
MIT License
