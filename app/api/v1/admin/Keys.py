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
from app.api.models.AdminModel import FreeKeysResponse, BannedIpsResponse

router = APIRouter()

@router.get(
    "/free_keys",
    response_model=BaseResponse[FreeKeysResponse],
    summary="Free API Keys",
    description="Get all free API keys (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def get_free_keys(
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
        
        result = rate_limit_middleware.api_key_validator.get_all_free_keys(apikey)
        
        if not result["success"]:
            return ErrorResponse(
                status=400,
                success=False,
                message=result["error"]
            )
        
        response_data = FreeKeysResponse(**result)
        
        return BaseResponse[FreeKeysResponse](
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

@router.get(
    "/banned_ips",
    response_model=BaseResponse[BannedIpsResponse],
    summary="Banned IP Addresses",
    description="Get all banned IP addresses (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def get_banned_ips(
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
        
        banned_ips = rate_limit_middleware.get_banned_ips()
        
        response_data = BannedIpsResponse(
            success=True,
            banned_ips=banned_ips,
            total_banned=len(banned_ips)
        )
        
        return BaseResponse[BannedIpsResponse](
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