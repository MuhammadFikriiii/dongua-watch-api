from fastapi import APIRouter, Query, Request
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import BanIpRequest, BanIpResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()

@router.post(
    "/ban_ip",
    response_model=BaseResponse[BanIpResponse],
    summary="Ban IP Address",
    description="Ban an IP address from accessing the API (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def ban_ip_address(
    request: Request,
    ip: str = Query(..., description="IP address to ban"),
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        api_key_validator = request.app.state.api_key_validator
        admin_validation = api_key_validator.validate_key(apikey)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return ErrorResponse(
                status=401,
                success=False,
                message="Invalid admin API key"
            )
        
        for middleware in request.app.user_middleware:
            if hasattr(middleware.cls, '__name__') and middleware.cls.__name__ == 'RateLimitMiddleware':
                rate_instance = middleware.cls(app=request.app)
                rate_instance.ban_ip(ip)
                break
        
        response_data = BanIpResponse(
            success=True,
            message=f"IP address {ip} has been banned"
        )
        
        return BaseResponse[BanIpResponse](
            status=200,
            success=True,
            data=response_data
        )
        
    except Exception as e:
        return ErrorResponse(
            status=500,
            success=False,
            message=f"Internal server error: {str(e)}"
        )
