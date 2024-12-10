from flask import Flask, render_template, request, jsonify
from serpapi_client import SerpAPIClient
from question_collector import collect_questions

app = Flask(__name__)
serp_client = SerpAPIClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        questions = collect_questions(query)
        return jsonify({'questions': sorted(list(questions))})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
