import json
from correction_script import get_correlations, prob_of_occurr, vocab

def handler(event, context):
    data = json.loads(event['body'])
    word = data.get('word')
    
    # Get suggestions with probabilities
    suggestions = get_correlations(word, prob_of_occurr, vocab)
    
    # Format the suggestions for the response
    corrections = [{"word": s[0], "probability": s[1]} for s in suggestions]
    
    return {
        'statusCode': 200,
        'body': json.dumps({'corrections': corrections})
    }
