from serpapi_client import SerpAPIClient
from collections import Counter
import json
from datetime import datetime

COST_PER_REQUEST = 0.015  # Coût en USD par requête SerpAPI

def collect_questions(initial_keyword, max_depth=2):
    """
    Collecte récursivement les questions à partir d'un mot-clé initial en utilisant l'API de recherche Google.
    
    Args:
        initial_keyword: Le mot-clé initial pour la recherche
        max_depth: Profondeur maximale de récursion (défaut: 2)
    """
    def _collect_recursive(query, depth, all_questions, request_count):
        """Fonction récursive interne pour collecter les questions"""
        if depth >= max_depth:
            return request_count
        
        # Faire la recherche pour la requête actuelle
        questions = client.search(query)
        request_count += 1
        
        if not questions:
            return request_count
        
        # Pour chaque nouvelle question trouvée
        new_questions = 0
        for q in questions:
            question_text = q['question']
            if question_text not in all_questions:
                all_questions.add(question_text)
                new_questions += 1
                # Rechercher récursivement pour cette nouvelle question
                request_count = _collect_recursive(question_text, depth + 1, all_questions, request_count)
        
        if new_questions > 0:
            print(f"Niveau {depth}: {new_questions} nouvelles questions trouvées")
        
        return request_count
    
    client = SerpAPIClient()
    all_questions = set()  # Pour stocker les questions uniques
    request_count = 0  # Compteur de requêtes
    
    print(f"\nRecherche initiale pour : '{initial_keyword}'")
    request_count = _collect_recursive(initial_keyword, 0, all_questions, request_count)
    
    # Calculer le coût total
    total_cost = request_count * COST_PER_REQUEST
    
    # Afficher les résultats
    print(f"\nRésultats :")
    print(f"Nombre total de requêtes effectuées : {request_count}")
    print(f"Coût total estimé : ${total_cost:.2f} USD")
    print(f"Nombre total de questions uniques : {len(all_questions)}")
    print(f"Coût par question unique : ${(total_cost/len(all_questions)):.3f} USD")
    print("\nQuestions collectées :")
    for q in sorted(all_questions):
        print(f"- {q}")
    
    return all_questions

if __name__ == '__main__':
    initial_keyword = input("Entrez votre mot-clé initial : ")
    collect_questions(initial_keyword)
