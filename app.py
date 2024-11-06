from flask import Flask, request, jsonify
from correction_script import get_correlations, prob_of_occurr, vocab
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/check', methods=['POST'])
def check_spelling():
    data = request.get_json()
    word = data.get('word')
    
    # Get suggestions with probabilities
    suggestions = get_correlations(word, prob_of_occurr, vocab)
    
    # Format the response as a list of dictionaries with 'word' and 'probability'
    corrections = [{"word": s[0], "probability": s[1]} for s in suggestions]
    
    return jsonify({"corrections": corrections})

if __name__ == "__main__":
    app.run(debug=True)
