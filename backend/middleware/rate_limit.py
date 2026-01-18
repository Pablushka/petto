from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from config import settings
import logging

# Get security logger
security_logger = logging.getLogger("security")

# Initialize rate limiter
# In production, you'd want to use Redis for distributed rate limiting
try:
    import redis
    redis_client = redis.Redis(
        host='localhost', 
        port=6379, 
        db=0, 
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True
    )
    # Test Redis connection
    redis_client.ping()
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri="redis://localhost:6379"
    )
    security_logger.info("Rate limiting initialized with Redis storage")
except Exception as e:
    # Fallback to memory storage for development
    limiter = Limiter(key_func=get_remote_address)
    security_logger.warning(f"Rate limiting using memory storage (Redis unavailable): {e}")


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom handler for rate limit exceeded errors"""
    security_logger.warning(
        f"Rate limit exceeded for IP: {request.client.host}, "
        f"Path: {request.url.path}, "
        f"Limit: {exc.detail}"
    )
    
    return Response(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
            "retry_after": str(exc.detail).split()[-1].replace("'", "")
        },
        headers={"Retry-After": "60"}
    )


# Rate limit configurations for different endpoints
RATE_LIMITS = {
    "auth": {
        "login": "5/minute",      # 5 login attempts per minute
        "register": "3/hour",     # 3 registrations per hour
        "password_reset": "3/hour", # 3 password resets per hour
    },
    "api": {
        "default": "100/minute",   # 100 requests per minute
        "upload": "10/minute",    # 10 uploads per minute
        "qrcode": "30/minute",    # 30 QR codes per minute
    },
    "strict": "10/minute"         # For sensitive operations
}


def get_rate_limit(category: str, endpoint: str = None) -> str:
    """Get rate limit for a specific category/endpoint"""
    if category in RATE_LIMITS:
        if isinstance(RATE_LIMITS[category], dict):
            if endpoint and endpoint in RATE_LIMITS[category]:
                return RATE_LIMITS[category][endpoint]
        else:
            return RATE_LIMITS[category]
    
    return RATE_LIMITS["api"]["default"]