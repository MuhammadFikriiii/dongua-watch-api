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

from fastapi import APIRouter, Query, HTTPException
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import StatsResponse

router = APIRouter()

@router.get(
    "/stats",
    response_model=BaseResponse[StatsResponse],
    summary="API Statistics",
    description="Get comprehensive API usage statistics (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def get_api_stats(
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        from app.main import rate_limit_middleware
        
        admin_validation = rate_limit_middleware.api_key_validator.validate_key(apikey)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return ErrorResponse(
                status=401,
                success=False,
                message="Invalid admin API key"
            )
        
        stats = rate_limit_middleware.stats_middleware.get_stats()
        
        response_data = StatsResponse(
            success=True,
            total_requests=stats["total_requests"],
            unique_ips=stats["unique_ips_count"],
            active_keys=len(rate_limit_middleware.api_key_validator.free_keys),
            banned_ips=len(rate_limit_middleware.get_banned_ips()),
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