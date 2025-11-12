import time
from collections import defaultdict

from fastapi import HTTPException, Request, status


class RateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)

    def _clean_old_requests(self, client_id: str) -> None:
        cutoff = time.time() - self.window
        self.clients[client_id] = [req_time for req_time in self.clients[client_id] if req_time > cutoff]

    def check_rate_limit(self, client_id: str) -> None:
        self._clean_old_requests(client_id)

        if len(self.clients[client_id]) >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

        self.clients[client_id].append(time.time())


def get_client_id(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
