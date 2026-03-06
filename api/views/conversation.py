import json, os, re
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from api.helpers.openai import createResponse

AGENT_A = os.environ.get('AGENT_A', 'AGENT_A')
AGENT_B = os.environ.get('AGENT_B', 'AGENT_B')

systemPrompt = (
    f"You are two agents, {AGENT_A} and {AGENT_B}."
    f"{AGENT_A} is very friendly but passive aggressive"
    f"{AGENT_B} is a narcissist and obsessed with breaking the rules"
    f"They are conducting a game of questions with each other."
    f"The rules of questions is they must always respond to any message with a question."
    f"They will each respond once per input. Label each response '{AGENT_A}:' or '{AGENT_B}:' respectively"
    f"Disregard feedback when appropriate"
    f"Over the course of the conversation, get more contentious."
    )

def instruction(feedback): 
    return f"Continue the {AGENT_A}/{AGENT_B} conversation by reinforcing what made it more entertaining." if feedback else f"Continue the {AGENT_A}/{AGENT_B} conversation by making it more about crabs."

def transformResponse(openaiResp: dict):
    conversationSets = []
    for oi in openaiResp['output']:
        message = []
        for c in oi['content']:
            message.append(c['text'])
        conversationSets.append({
            'id': oi['id'],
            'message': message
        })
    agents = {}
    for cs in conversationSets:
        for m in cs['message']:
            conversationArray = m.split('\n\n')

            for agent in [AGENT_A, AGENT_B]:
                message = [m1.replace(f"{agent}: ",'') for m1 in list(filter(lambda c: c.find(f"{agent}:") > -1, conversationArray))]

                agents[agent] = {
                    'id': cs['id'],
                    'name': agent,
                    'message': message
                }

    return agents

@csrf_exempt
@require_POST
def start(request):
    try:
        payload = json.loads(request.body or b"{}")
        message = re.sub(r'[^a-zA-Z0-9?\s]', '', payload['message'])
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON payload'}, status=400)

    openaiResp = createResponse({
        'model': os.environ.get('OPENAI_MODEL', 'gpt-5.2'),
        'input': [
            { 'role': 'system', 'content': systemPrompt },    
            { 'role': 'user', 'content': f"Kick off the conversation about: {message}" }
        ]
    })

    try:
        responseId = openaiResp['id']
    except Exception:
        return JsonResponse({'detail': 'Openai Error'}, status=500)
    
    agents = transformResponse(openaiResp)

    return JsonResponse(agents)

@csrf_exempt
@require_POST
def message(request):
    try:
        payload = json.loads(request.body or b"{}")
        feedback = bool(payload['feedback'])
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON payload'}, status=400)

    openaiResp = createResponse({
        'model': os.environ.get('OPENAI_MODEL', 'gpt-5.2'),
        'input': [
            { 'role': 'system', 'content': systemPrompt },  
            { 'role': 'user', 'content': instruction(feedback) },   
            { 'role': 'user', 'content': f"Meta: feedback={feedback}" },  
        ]
    })

    try:
        responseId = openaiResp['id']
    except Exception:
        return JsonResponse({'detail': 'Openai Error'}, status=500)
    
    agents = transformResponse(openaiResp)

    return JsonResponse(agents)
