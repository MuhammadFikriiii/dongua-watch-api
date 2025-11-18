#
#             Zhadevv Project
#             --MIT License--
#
# Feed Me Starnya Bang:>
# Project 100% Open Source
# Bebas Recode, Deploy Production. KECUALI
# Diperjual-Belikan.
#
# Project ini Sepenuhnya Gratis, Makannua ksih Bintang Dong anj:>
# *bercanda ajahh
#
# Regards
# Zhadevv
#

from fastapi import APIRouter, Query, Request
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import StatsResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()

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
        api_key_validator = request.app.state.api_key_validator
        admin_validation = api_key_validator.validate_key(apikey)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return ErrorResponse(
                status=401,
                success=False,
                message="Invalid admin API key"
            )
        
        stats = {}
        banned_ips = []
        
        for middleware in request.app.user_middleware:
            if hasattr(middleware.cls, 'get_stats'):
                stats_instance = middleware.cls(app=request.app)
                stats = stats_instance.get_stats()
            if hasattr(middleware.cls, 'get_banned_ips'):
                rate_instance = middleware.cls(app=request.app)
                banned_ips = rate_instance.get_banned_ips()
        
        response_data = StatsResponse(
            success=True,
            total_requests=stats.get("total_requests", 0),
            unique_ips=stats.get("unique_ips_count", 0),
            active_keys=len(getattr(api_key_validator, 'free_keys', {})),
            banned_ips=len(banned_ips),
            requests_by_tier=stats.get("requests_by_tier", {}),
            top_endpoints=stats.get("top_endpoints", [])
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
