from fastapi import APIRouter, Query, HTTPException, Request
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import UnbanIpRequest, UnbanIpResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()
api_key_validator = ApiKeyValidator()

@router.delete(
    "/unban_ip",
    response_model=BaseResponse[UnbanIpResponse],
    summary="Unban IP Address",
    description="Unban an IP address (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def unban_ip_address(
    request: Request,
    ip: str = Query(..., description="IP address to unban"),
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        admin_validation = api_key_validator.validate_key(apikey)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return ErrorResponse(
                status=401,
                success=False,
                message="Invalid admin API key"
            )
        
        rate_limit_middleware.unban_ip(ip)
        
        response_data = UnbanIpResponse(
            success=True,
            message=f"IP address {ip} has been unbanned"
        )
        
        return BaseResponse[UnbanIpResponse](
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
