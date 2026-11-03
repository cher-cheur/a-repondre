import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import json

class SerpAPIClient:
    def __init__(self, test_mode=False, max_requests=None):
        self.test_mode = test_mode
        # Budget d'appels SerpAPI (payants) : None = illimité
        self.max_requests = max_requests
        self.request_count = 0
        
        # Liste des mots de début de question
        self.question_starters = [
            "comment", "quel", "quelle", "quels", "quelles",
            "pourquoi", "où", "quand", "qui", "combien"
        ]
        
        if not test_mode:
            load_dotenv()
            self.api_key = os.getenv('SERPAPI_API_KEY')
            if not self.api_key:
                raise ValueError("La clé API SerpAPI n'est pas configurée dans le fichier .env")
            
        self.base_url = "https://serpapi.com/search"

    def budget_exhausted(self):
        return self.max_requests is not None and self.request_count >= self.max_requests

    def _get(self, params):
        """Un appel SerpAPI, compté et soumis au budget. None si le budget est épuisé."""
        if self.budget_exhausted():
            print(f"Budget de {self.max_requests} requêtes SerpAPI atteint, arrêt.")
            return None
        self.request_count += 1
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def search(self, query, google_domain="google.fr", gl="fr", hl="fr", location="France"):
        """
        Fait une recherche Google et retourne les questions liées trouvées.
        Si aucune question n'est trouvée, essaie avec différents mots de début de question.
        
        Args:
            query (str): La requête de recherche
            google_domain (str): Le domaine Google à utiliser (par défaut: google.fr)
            gl (str): Le code pays pour la recherche Google (par défaut: fr)
            hl (str): Le code langue pour la recherche Google (par défaut: fr)
            location (str): La localisation pour la recherche (par défaut: France)
        """
        if self.test_mode:
            with open('data/sample_response.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('related_questions', [])

        # Première recherche avec la requête originale
        params = {
            'q': query,
            'api_key': self.api_key,
            'engine': 'google',
            'google_domain': google_domain,
            'gl': gl,
            'hl': hl,
            'location': location
        }
            
        try:
            print(f"\nRequête pour : '{query}' (Domaine: {google_domain}, Pays: {gl}, Langue: {hl}, Location: {location})")
            data = self._get(params)
            if data is None:
                return []

            # Si aucune question n'est trouvée, essayer avec les mots de début de question
            related_questions = data.get('related_questions', [])
            if not related_questions:
                print("Aucune question trouvée, essai avec les mots de début de question...")
                
                for starter in self.question_starters:
                    modified_query = f"{starter} {query}"
                    params['q'] = modified_query
                    print(f"Essai avec : '{modified_query}'")
                    
                    data = self._get(params)
                    if data is None:
                        break
                    related_questions = data.get('related_questions', [])
                    
                    if related_questions:
                        print(f"Questions trouvées avec '{modified_query}'")
                        break
            
            return related_questions
            
        except requests.RequestException as e:
            print(f"Erreur lors de la requête à l'API: {e}")
            return []
