from fastapi import APIRouter, Query, HTTPException, Request
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import StatsResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()
api_key_validator = ApiKeyValidator()

@router.get(
    "/stats",
    response_model=BaseResponse[StatsResponse],
    summary="API Statistics",
    description="Get comprehensive API usage statistics (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def get_api_stats(
    request: Request,
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
        
        stats = stats_middleware.get_stats()
        banned_ips = rate_limit_middleware.get_banned_ips()
        
        response_data = StatsResponse(
            success=True,
            total_requests=stats["total_requests"],
            unique_ips=stats["unique_ips_count"],
            active_keys=len(api_key_validator.free_keys),
            banned_ips=len(banned_ips),
            requests_by_tier=stats["requests_by_tier"],
            top_endpoints=stats["top_endpoints"]
        )
        
        return BaseResponse[StatsResponse](
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
