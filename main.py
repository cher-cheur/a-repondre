import logging
import os
import threading
import time
from collections import defaultdict, deque

from flask import Flask, render_template, request, jsonify
from question_collector import collect_questions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Chaque recherche déclenche plusieurs appels SerpAPI payants :
# on limite le nombre de recherches par adresse IP.
RATE_LIMIT_SEARCHES = int(os.getenv('RATE_LIMIT_SEARCHES', '5'))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv('RATE_LIMIT_WINDOW_SECONDS', '3600'))
MAX_QUERY_LENGTH = 200

_search_history = defaultdict(deque)
_rate_lock = threading.Lock()


def _rate_limited(client_ip):
    """True si cette IP a dépassé son quota de recherches sur la fenêtre."""
    now = time.monotonic()
    with _rate_lock:
        history = _search_history[client_ip]
        while history and now - history[0] > RATE_LIMIT_WINDOW_SECONDS:
            history.popleft()
        if len(history) >= RATE_LIMIT_SEARCHES:
            return True
        history.append(now)
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json(silent=True) or {}
    query = data.get('query')

    if not isinstance(query, str) or not query.strip():
        return jsonify({'error': 'Query is required'}), 400
    query = query.strip()
    if len(query) > MAX_QUERY_LENGTH:
        return jsonify({'error': f'Query too long (max {MAX_QUERY_LENGTH} characters)'}), 400

    if _rate_limited(request.remote_addr):
        return jsonify({'error': 'Too many searches, please try again later'}), 429

    try:
        questions = collect_questions(query)
        return jsonify({'questions': sorted(list(questions))})
    except Exception:
        # Détails dans les logs serveur uniquement, jamais renvoyés au client
        logger.exception("Erreur pendant la collecte des questions")
        return jsonify({'error': 'Internal error during search'}), 500


if __name__ == '__main__':
    # Le débogueur Werkzeug permet d'exécuter du code à distance :
    # il n'est activé que si FLASK_DEBUG=1 est défini explicitement.
    app.run(debug=os.getenv('FLASK_DEBUG') == '1')
