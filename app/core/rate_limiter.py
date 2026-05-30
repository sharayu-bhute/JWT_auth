import time
from collections import defaultdict

request_counts = defaultdict(list)
LIMIT = 5
WINDOW = 60

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    request_counts[ip]=[
        t for t in request_counts[ip] if now - t < WINDOW
    ]

    if len(request_counts[ip]) >= LIMIT:
        return True
    
    request_counts[ip].append(now)
    return False