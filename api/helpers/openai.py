import requests,os

def createResponse(message: dict):
    api_key = os.environ.get('OPENAI_API_KEY', False)
    if not api_key:
        return {
            'response': 500,
            'message': 'Missing Openai API key'
        }
        
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json',
    }
    res = requests.post(url='https://api.openai.com/v1/responses',json=message, headers=headers)

    resJson = res.json()

    if 'error' in resJson.keys() and resJson['error'] is not None:
        return {
            'response': 500,
            'message': f"Openai api error {resJson['error']['message']}"
        }

    return resJson

