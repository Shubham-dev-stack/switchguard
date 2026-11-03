"""
Chaos Scenario: JWT Token Expiry Timestamp Regression
Service: auth-gateway (Tier-1)
Symptom: 100% of incoming authenticated requests reject with HTTP 401 Unauthorized.
Root Cause: Unit mismatch (milliseconds vs seconds) in token expiration computation.
"""
import time
from typing import Dict, Any, Optional

class TokenValidationError(Exception):
    pass

class JWTAuthService:
    def __init__(self, secret: str = "switchguard-secret-key"):
        self.secret = secret

    def create_token(self, user_id: str, ttl_seconds: int = 3600, buggy: bool = False) -> Dict[str, Any]:
        current_time = time.time()
        if buggy:
            # Bug: assigning seconds to millisecond comparison or inverted expiry
            # E.g., setting exp as current_time - ttl_seconds (expired immediately)
            exp = current_time - 1.0
        else:
            exp = current_time + ttl_seconds

        return {
            "sub": user_id,
            "iat": current_time,
            "exp": exp,
            "roles": ["developer", "operator"]
        }

    def verify_token(self, token: Dict[str, Any]) -> bool:
        current_time = time.time()
        exp = token.get("exp")
        if exp is None:
            raise TokenValidationError("Missing 'exp' claim in token")
        if current_time >= exp:
            raise TokenValidationError(f"Token expired at {exp}, current time is {current_time}")
        return True
