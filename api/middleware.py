import hashlib
from django.http import JsonResponse
import os

def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

class BearerTokenAuthMiddleware:
    """
    Require Authorization: Bearer <token> for any /api/* endpoint.
    Token is validated by hashing and looking it up in ApiToken.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = os.environ.get("BACKEND_BEARER_TOKEN",False)

        if not token:
            return JsonResponse({"detail": "Authentication server error"}, status=500)

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail": "Authentication malformed"}, status=401)

        raw = auth.removeprefix("Bearer ").strip()
        if not raw:
            return JsonResponse({"detail": "Authentication missing"}, status=401)

        if raw != token:
            return JsonResponse({"detail": "Authentication failed"}, status=403)

        return self.get_response(request)
