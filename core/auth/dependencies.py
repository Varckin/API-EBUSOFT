from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.auth.settings import CONFIG
from logger.init_logger import get_logger


logger = get_logger('Token_auth_depend')
security = HTTPBearer()


def require_role(*allowed_roles: str):
    """
    Dependency to enforce role-based access control.

    Checks the token information stored in `request.state.token_info` and ensures
    that the token's role is in the list of allowed roles. Raises 403 if missing
    or insufficient permissions. Logs all access attempts.
    """
    def role_checker(request: Request) -> dict:
        token_info = getattr(request.state, "token_info", None)
        if not token_info:
            logger.warning(f"Access denied: missing token_info, path={request.url.path}")
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        if token_info["role"] not in allowed_roles:
            logger.warning(
                f"Access denied: token={token_info['token']}, role={token_info['role']}, "
                f"required_roles={allowed_roles}, path={request.url.path}"
            )
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        logger.info(f"Access granted: token={token_info['token']}, role={token_info['role']}, path={request.url.path}")
        return token_info
    return role_checker


async def verify_admin_master(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to verify the admin master token.

    Checks that the provided Bearer token matches the configured master token.
    Raises 403 if invalid. Logs successful and failed validations.
    """
    token = credentials.credentials
    if token != CONFIG.ADMIN_MASTER_TOKEN:
        logger.warning(f"Access denied: invalid admin master token, token={token}")
        raise HTTPException(status_code=403, detail="Only admin master token allowed")
    logger.info("Admin master token validated successfully")
    return token
