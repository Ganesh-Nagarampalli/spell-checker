import json
from correction_script import get_correlations, prob_of_occurr, vocab

def handler(event, context):
    # This replaces the Flask route handling
    data = json.loads(event['body'])
    word = data.get('word')
    suggestions = get_correlations(word, prob_of_occurr, vocab)
    correction = suggestions[0][0] if suggestions else word
    return {
        'statusCode': 200,
        'body': json.dumps({'correction': correction})
    }
