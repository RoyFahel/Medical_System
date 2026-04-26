import json
import logging
import time
from typing import Any

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("app.requests")


class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start = time.perf_counter()
        response: HttpResponse | None = None
        try:
            response = self.get_response(request)
            return response
        finally:
            duration_ms = int((time.perf_counter() - start) * 1000)
            status_code = getattr(response, "status_code", 500)

            user_id = None
            try:
                if hasattr(request, "user") and getattr(request.user, "is_authenticated", False):
                    user_id = getattr(request.user, "id", None)
            except Exception:
                user_id = None

            extra: dict[str, Any] = {
                "method": request.method,
                "path": request.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "user_id": user_id,
            }

            if status_code >= 400:
                # Best-effort: include DRF-style validation details without risking crashes.
                try:
                    body = getattr(response, "data", None)
                    if body is None:
                        content = getattr(response, "content", b"")
                        if content:
                            extra["response_body"] = json.loads(content.decode("utf-8"))
                    else:
                        extra["response_body"] = body
                except Exception:
                    pass

            logger.info("request", extra=extra)
